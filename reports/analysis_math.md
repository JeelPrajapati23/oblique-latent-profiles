# Week 3 analysis: math

All runs masked with `per_query_excluded_ids.json`.

## Headline numbers (masked; gold/pooled for Math)

| system | nDCG@10 all | nDCG@10 test | R@50 all | R@100 all | p vs E1 (test) |
|---|---|---|---|---|---|
| E1 qwen3-0.6b_text_none | 0.117/0.147 | 0.113/0.144 | 0.227/0.257 | 0.313/0.341 | - |
| E4 RRF all 4 (main) | 0.142/0.175 | 0.139/0.173 | 0.282/0.306 | 0.383/0.410 | 0.0234/0.0126 |
| E5 = E4 + LLM re-rank top 50 | 0.126/0.156 | 0.129/0.159 | 0.282/0.306 | 0.383/0.410 | 0.186/0.228 |

E5 vs E4, all queries, nDCG@10: gold: 25 better / 40 worse, p = 0.0839; pool: 23 better / 46 worse, p = 0.0671. Recall@50/100 are equal by construction (only the top 50 is reordered).

Paper reference (nDCG@10, Math pooled): Gemini-2-Embedding .147, GPT-5.2 rewriter + Gemini .185, GPT-5.2 multi-hop agent .207, oracle GPT-5.2 re-ranker with gold injected .329.

## Cost

| Step | Items | Wall time | GPU-minutes | GPU-seconds per item |
|---|---|---|---|---|
| Profile math (query+doc) on 2x Tesla T4 | 3639 | 8.2 min | 16.4 | 0.27 |
| Profile math_soln (doc) on 2x Tesla T4 | 3493 | 35.7 min | 71.4 | 1.23 |
| E5 re-rank top 50 (151 queries) | 604 windows | 45.1 min | 45.1 | 17.92 per query |

GPU-seconds per item is batched throughput on Kaggle T4s (includes vLLM start-up), not single-request latency. Profiling is a one-off, offline cost per corpus.

## Online latency per query (laptop CPU, after the query is profiled)

| Step | ms per query |
|---|---|
| BM25 text | 56.9 |
| BM25 profile | 38.1 |
| Dense text (FAISS search) | 0.8 |
| Dense profile (FAISS search) | 0.9 |
| RRF of 4 lists | 1.7 |
| **Total** | **98.4** |

Not included: encoding the query and its profile with Qwen3-0.6B (one forward pass each) and the LLM call that writes the query profile (~100 output tokens; a few seconds on one T4).

## Where profiles help and hurt

Per-query nDCG@10 (pool) of `E4_RRF_all_4_k_60` vs `qwen3-0.6b_text_none`, all 151 queries: **59 better, 35 worse, 57 tied** (ties are mostly queries where both systems score 0).

### Helped most

**q01890**: nDCG@10 0.000 -> 0.398 (+0.398)

> Given real numbers $x_1,\dots,x_{2n}$, let $A$ be the skew-symmetric $2n\times 2n$ matrix with entries $a_{i,j}=(x_i-x_j)^2$ for $1\le i<j\le 2n$. Prove \[ \det(A)=4^{n-1}\Bigl((x_1-x_2)(x_2-x_3)\cdots(x_{2n-1}-x_{2n})(x_{2n}-x_1)\Bigr)^2. \]

Query profile: Techniques: Determinant expansion, Matrix transformation, Symmetry exploitation Proof move: Recognize the matrix as a block structure -> Apply determinant properties of block matrices -> Simplify using symmetry and scaling -> Identify the product of differences as a determinant of a simpler matrix Key insight: The determinant of a skew-symmetric matrix can be expressed in terms of its eigenvalues or through a specific transformation that reveals its structure. Also known as: Eigenvalue approach, Transformation to a simpler form, Symmetric polynomial evaluation

Relevant doc `american-math-monthly___1997___10387`: rank 35 (baseline) -> 7 (E4)

> Let $T_n=(t_{i,j})$ be the $n\times n$ matrix with $t_{i,j}=\tan(i+j-1)x$, i.e., \[ T_n=\begin{pmatrix} \tan x & \tan 2x & \tan 3x & \cdots & \tan nx\\ \tan 2x & \tan 3x & \tan 4x & \cdots & \tan(n+1)x\\ \tan 3x & \tan 4x & \tan 5x & \cdots & \tan(n+2)x\\ \vdots & \vdots & \vdots & & \vdots\\ \tan n...

Doc profile: Techniques: Determinant properties, Trigonometric identities, Recursive relations Proof move: Identify the pattern in the determinant's structure -> Utilize trigonometric product-to-sum identities -> Recognize the recursive nature of the determinant -> Apply symmetry and periodicity of trigonometric functions Key insight: The determinant can be expressed as a product of simpler determinants with known values. Also known as: Eigenvalue analysis, Orthogonality relations, Symmetry exploitation

**q01094**: nDCG@10 0.276 -> 0.630 (+0.354)

> Find a closed-form expression for \[ \sum_{n=1}^{\infty}4^n\sin^4\bigl(2^{-n}\theta\bigr). \]

Query profile: Techniques: Trigonometric Identity, Series Transformation Proof move: Recognize a trig identity -> Simplify the sine term -> Transform the series into a telescoping form -> Sum the series Key insight: The sine term can be expressed as a polynomial in sine, facilitating series simplification. Also known as: Angle Reduction, Polynomial Approximation

Relevant doc `american-math-monthly___2011___11438`: rank 77 (baseline) -> 1 (E4)

> Let \[ P(x)=\sum_{k=1}^{\infty}\arctan\left(\frac{x-1}{(k+x+1)\sqrt{k+1}+(k+2)\sqrt{k+x}}\right). \] (a) Find a closed-form expression for $P(n)$ when $n$ is a nonnegative integer. (b) Show that $\lim_{x\to -1^+}P(x)$ exists, and find a closed-form expression for it.

Doc profile: Techniques: Series Manipulation, Limit Evaluation, Trigonometric Identity Application Proof move: Identify a telescoping series -> Simplify each term using trigonometric identities -> Recognize a pattern in the remaining terms -> Evaluate the limit as x approaches -1 from the right Key insight: Each term in the series can be expressed as a difference of two arctangents, leading to cancellation. Also known as: Arctangent Addition Formula, Sine and Cosine Substitution

**q00530**: nDCG@10 0.000 -> 0.336 (+0.336)

> For $n\in\mathbb N$, let $[n]=\{1,\dots,n\}$. For $A\subseteq [n]$, let $B=[n]-A$. Let \[ P(x)=\sum_{j\in A} x^j + \sum_{j\in B} x^{-j}. \] Let $\omega=\exp\big(2\pi i/(2n+1)\big)$. Prove that \[ \sum_{k=0}^{2n} P(\omega^k)^3 = \frac12 n(n+1)(2n+1). \]

Query profile: Techniques: Symmetry, Roots of Unity, Polynomial Evaluation Proof move: Identify the polynomial's roots, exploit symmetry in the sum, use roots of unity to simplify, apply polynomial evaluation at specific points, recognize telescoping series. Key insight: The sum of cubes of the polynomial evaluated at powers of a primitive root of unity can be decomposed into a telescoping series. Also known as: Cyclotomic Polynomial Analysis, Root Summation Technique, Unity Root Simplification

Relevant doc `american-math-monthly___1999___10448`: rank 16 (baseline) -> 1 (E4)

> Fix a positive integer $n$. Let $x_j=\cos\bigl((2j-1)\pi/(2n)\bigr)$ for $1\le j\le n$, and let \[ C_k=\frac{1}{n}\sum_{j=1}^n x_j^k\quad\text{for }k\in\mathbb{N}. \] Show that \[ C_k= \begin{cases} 0,&\text{if }k=1,3,\dots,2n-1;\\ \binom{k}{k/2}2^{-k},&\text{if }k=0,2,\dots,2n-2. \end{cases} \]

Doc profile: Techniques: Symmetry, Polynomial Roots, Binomial Coefficient Expansion Proof move: Identify the roots of unity -> Recognize the sum as a power sum of roots -> Apply symmetry to simplify odd powers -> Use binomial theorem for even powers Key insight: The cosine values are symmetric around the unit circle, allowing odd powers to cancel out. Also known as: Root Sum Simplification, Symmetric Polynomial Evaluation, Binomial Power Expansion

**q02938**: nDCG@10 0.000 -> 0.301 (+0.301)

> Let $D^n$ be a closed disc in $\mathbf{R}^n$ and $S^{n-1}=\partial D^n$ its boundary. For any topological space $X$ and map $\alpha:S^{n-1}\to X$, we define the space $Y$ obtained from $X$ by attaching an $n$-cell via the map $\alpha$ to be the quotient of the disjoint union $D^n \sqcup X$ by the eq...

Query profile: Techniques: Cellular attachment, Mayer-Vietoris sequence, Long exact sequence of homology Proof move: Consider the cellular chain complex -> Apply the long exact sequence of homology -> Analyze the change in Betti numbers Key insight: Attaching an $n$-cell to $X$ increases the $n$th Betti number by 1 or decreases the $(n-1)$st Betti number by 1. Also known as: Homology extension, Chain complex augmentation, Dimensional shift

Relevant doc `harvard-quals___2010___S10.9`: rank 51 (baseline) -> 9 (E4)

> Let $\Lambda_1$ and $\Lambda_2\subset \mathbf R^4$ be complementary $2$-planes, and let $X=\mathbf R^4\setminus (\Lambda_1\cup \Lambda_2)$ be the complement of their union. Find the homology and cohomology groups of $X$ with integer coefficients.

Doc profile: Techniques: Mayer-Vietoris sequence, excision, Poincaré duality Proof move: Decompose X using Mayer-Vietoris->Apply excision to each $\Lambda_i$->Use Poincaré duality on $\mathbf R^4$ Key insight: The homology of $X$ can be computed by considering the intersection of $\Lambda_1$ and $\Lambda_2$ and applying duality. Also known as: Complementary plane decomposition, Complementary space analysis, Intersection-based duality application

**q03027**: nDCG@10 0.139 -> 0.437 (+0.298)

> Suppose $R_1,R_2$ are bounded, simply-connected open subsets of $\mathbb C$. Let $z_1\in R_1$ and $z_2\in R_2$. i) Prove that there is a holomorphic bijective function $f:R_1\to R_2$ such that $f(z_1)=z_2$. ii) Suppose that $g:R_1\to R_2$ is a holomorphic function such that $g(z_1)=z_2$. Prove that ...

Query profile: Techniques: Riemann Mapping Theorem, Schwarz-Pick Lemma Proof move: Apply Riemann mapping theorem -> Map to unit disk -> Use Schwarz-Pick to compare derivatives Key insight: The derivative's magnitude is bounded by the distance-preserving property of holomorphic maps. Also known as: Conformal equivalence, Distance distortion theorem

Relevant doc `harvard-quals___2026___S26.10`: rank 2 (baseline) -> 1 (E4)

> Let $D:=\{z\in\mathbb{C}\mid |z|<1\}$ be the unit disk. Suppose $f:D\to D$ is a holomorphic function with two distinct fixed points $a\ne b\in D$. Prove that $f(z)=z$ for all $z\in D$.

Doc profile: Techniques: Schwarz Lemma, Fixed Point Theorem Proof move: Apply Schwarz Lemma to $f(z)$ -> Map unit disk to itself -> Use fixed points to normalize -> Conclude $f(z)=z$ -> Invoke rigidity of identity map Key insight: A holomorphic self-map with two fixed points must be the identity. Also known as: Identity Principle, Rigidity of Analytic Maps

**q02887**: nDCG@10 0.000 -> 0.296 (+0.296)

> (DG) Let $f:\mathbb{R}^3\to \mathbb{R}$ be defined by $f(x,y,z)=x^2+y^2-1$. (i) Prove that $M=f^{-1}(0)$ is a two-dimensional embedded submanifold of $\mathbb{R}^3$. (ii) For $a,b,c\in \mathbb{R}$, consider the vector field \[ X=a\frac{\partial}{\partial x}+b\frac{\partial}{\partial y}+c\frac{\parti...

Query profile: Techniques: Implicit Function Theorem, Tangency Condition Proof move: Apply Implicit Function Theorem -> Check Jacobian rank -> Solve for coefficients -> Verify tangent condition Key insight: The gradient of $f$ at $(1,0,1)$ must be proportional to the vector field $X$. Also known as: Regular Value Argument, Level Set Tangency

Relevant doc `harvard-quals___2015___S15.3`: rank 24 (baseline) -> 2 (E4)

> Let \[ M = \{(x,y,z)\in \mathbb{R}^3 \mid x^2 - y^2 - z^3 - z = 0\}. \] (a) Prove that $M$ is a smooth surface in $\mathbb{R}^3$. (b) For what values of $c\in \mathbb{R}$ does the plane $z=c$ intersect $M$ transversely?

Doc profile: Techniques: Implicit Function Theorem, Transversality Proof move: Apply Implicit Function Theorem -> Check Jacobian rank -> Analyze plane intersection -> Ensure transversality condition Key insight: The gradient of the defining function is never zero on $M$. Also known as: Regular Value Theorem, Non-zero Derivative Condition

**q01020**: nDCG@10 0.258 -> 0.535 (+0.277)

> Let \[ P(x)=\sum_{k=1}^{\infty}\arctan\left(\frac{x-1}{(k+x+1)\sqrt{k+1}+(k+2)\sqrt{k+x}}\right). \] (a) Find a closed-form expression for $P(n)$ when $n$ is a nonnegative integer. (b) Show that $\lim_{x\to -1^+}P(x)$ exists, and find a closed-form expression for it.

Query profile: Techniques: Series Manipulation, Limit Evaluation, Trigonometric Identity Application Proof move: Identify a telescoping series -> Simplify each term using trigonometric identities -> Recognize a pattern in the remaining terms -> Evaluate the limit as x approaches -1 from the right Key insight: Each term in the series can be expressed as a difference of two arctangents, leading to cancellation. Also known as: Arctangent Addition Formula, Sine and Cosine Substitution

Relevant doc `american-math-monthly___2011___11515`: rank 13 (baseline) -> 1 (E4)

> Find a closed-form expression for \[ \sum_{n=1}^{\infty}4^n\sin^4\bigl(2^{-n}\theta\bigr). \]

Doc profile: Techniques: Trigonometric Identity, Series Transformation Proof move: Recognize a trig identity -> Simplify the sine term -> Transform the series into a telescoping form -> Sum the series Key insight: The sine term can be expressed as a polynomial in sine, facilitating series simplification. Also known as: Angle Reduction, Polynomial Approximation

**q01949**: nDCG@10 0.139 -> 0.413 (+0.274)

> Prove \[ \sum_{n=1}^{\infty}\frac{\binom{2n}{n}\binom{4n}{2n}}{64^n(2n-1)}=1-\frac{1}{\pi}\left(\sqrt{2}+\ln(1+\sqrt{2})\right). \]

Query profile: Techniques: Series manipulation, combinatorial identities, logarithmic differentiation Proof move: Recognize the series as a special function expansion -> Identify the function through known series representations -> Apply logarithmic properties to simplify the expression -> Connect the constants through complex analysis techniques Key insight: The series can be expressed as a derivative of a known function evaluated at a specific point. Also known as: Logarithmic evaluation, special function transformation, series recognition through derivatives

Relevant doc `american-math-monthly___2024___12337`: rank 19 (baseline) -> 2 (E4)

> For $k\in\{0,1,2\}$, let \[ S_k=\sum \frac{(-4)^n}{2n+1}\binom{2n}{n}^{-1}, \] where the sum is taken over all nonnegative integers $n$ that are congruent to $k$ modulo $3$. Prove (a) $S_0=\dfrac{\ln(1+\sqrt{2})}{3\sqrt{2}}+\dfrac{\pi}{6}$; (b) $S_1=\dfrac{\ln(1+\sqrt{2})}{3\sqrt{2}}-\dfrac{\ln(2+\s...

Doc profile: Techniques: Series manipulation, logarithmic identities, trigonometric substitution Proof move: Identify a series that can be transformed into a known function -> Use properties of logarithms and trigonometric functions -> Recognize the series as a Fourier series or related to special values of the arctangent function Key insight: The series can be expressed in terms of logarithms and arctangents by recognizing its connection to known trigonometric identities. Also known as: Logarithmic transformation, Trigonometric representation, Fourier series recognition

**q00076**: nDCG@10 0.000 -> 0.237 (+0.237)

> Let $T_n=(t_{i,j})$ be the $n\times n$ matrix with $t_{i,j}=\tan(i+j-1)x$, i.e., \[ T_n=\begin{pmatrix} \tan x & \tan 2x & \tan 3x & \cdots & \tan nx\\ \tan 2x & \tan 3x & \tan 4x & \cdots & \tan(n+1)x\\ \tan 3x & \tan 4x & \tan 5x & \cdots & \tan(n+2)x\\ \vdots & \vdots & \vdots & & \vdots\\ \tan n...

Query profile: Techniques: Determinant properties, Trigonometric identities, Recursive relations Proof move: Identify the pattern in the determinant's structure -> Utilize trigonometric product-to-sum identities -> Recognize the recursive nature of the determinant -> Apply symmetry and periodicity of trigonometric functions Key insight: The determinant can be expressed as a product of simpler determinants with known values. Also known as: Eigenvalue analysis, Orthogonality relations, Symmetry exploitation

Relevant doc `american-math-monthly___2024___12322`: rank 21 (baseline) -> 5 (E4)

> Given real numbers $x_1,\dots,x_{2n}$, let $A$ be the skew-symmetric $2n\times 2n$ matrix with entries $a_{i,j}=(x_i-x_j)^2$ for $1\le i<j\le 2n$. Prove \[ \det(A)=4^{n-1}\Bigl((x_1-x_2)(x_2-x_3)\cdots(x_{2n-1}-x_{2n})(x_{2n}-x_1)\Bigr)^2. \]

Doc profile: Techniques: Determinant expansion, Matrix transformation, Symmetry exploitation Proof move: Recognize the matrix as a block structure -> Apply determinant properties of block matrices -> Simplify using symmetry and scaling -> Identify the product of differences as a determinant of a simpler matrix Key insight: The determinant of a skew-symmetric matrix can be expressed in terms of its eigenvalues or through a specific transformation that reveals its structure. Also known as: Eigenvalue approach, Transformation to a simpler form, Difference product recognition

**q02279**: nDCG@10 0.000 -> 0.237 (+0.237)

> Let $\mathbb R[x_1,\dots,x_n]$ be the polynomial ring over $\mathbb R$ in variables $x_1,\dots,x_n$. Let $A$ be the $n\times n$ matrix whose $i$th row is $(1,x_i,x_i^2,\dots,x_i^{n-1})$, $i=1,\dots,n$. Show that \[ \det A = \prod_{i>j}(x_i-x_j). \]

Query profile: Techniques: Change of Variables, Determinant Expansion, Polynomial Factorization Proof move: Recognize Vandermonde matrix -> Expand determinant along first row -> Identify polynomial as product of linear factors -> Match coefficients Key insight: The determinant's value is a polynomial in the variables $x_i$ that vanishes when any two $x_i$ are equal. Also known as: Polynomial Root Identification, Linear Factorization Recognition

Relevant doc `american-math-monthly___2024___12322`: rank 39 (baseline) -> 5 (E4)

> Given real numbers $x_1,\dots,x_{2n}$, let $A$ be the skew-symmetric $2n\times 2n$ matrix with entries $a_{i,j}=(x_i-x_j)^2$ for $1\le i<j\le 2n$. Prove \[ \det(A)=4^{n-1}\Bigl((x_1-x_2)(x_2-x_3)\cdots(x_{2n-1}-x_{2n})(x_{2n}-x_1)\Bigr)^2. \]

Doc profile: Techniques: Determinant expansion, Matrix transformation, Symmetry exploitation Proof move: Recognize the matrix as a block structure -> Apply determinant properties of block matrices -> Simplify using symmetry and scaling -> Identify the product of differences as a determinant of a simpler matrix Key insight: The determinant of a skew-symmetric matrix can be expressed in terms of its eigenvalues or through a specific transformation that reveals its structure. Also known as: Eigenvalue approach, Transformation to a simpler form, Difference product recognition

### Hurt most

**q01549**: nDCG@10 0.542 -> 0.173 (-0.369)

> Catalan’s constant $G$ is defined to be $\sum_{n=0}^{\infty} \frac{(-1)^n}{(2n+1)^2}$. Prove \[ G=\frac{\pi}{2}\sum_{n=0}^{\infty} \frac{\zeta(2n)}{(2n+1)4^n}\left(1-\frac{2}{4^n}\right), \] where $\zeta$ is the Riemann zeta function, defined by $\zeta(s)=\sum_{n=1}^{\infty} \frac{1}{n^s}$ for $s>1$...

Query profile: Techniques: Series manipulation, zeta function properties, Euler product Proof move: Recognize the series as a product of simpler series -> Express the original series in terms of known series -> Utilize the definition of the zeta function and its properties -> Simplify the expression to match the desired form Key insight: The original series can be decomposed into a product of two series, one involving the zeta function and the other a geometric progression. Also known as: Fourier series expansion, Dirichlet series transformation, Euler's identity application

Relevant doc `american-math-monthly___2023___12254`: rank 1 (baseline) -> 33 (E4)

E4's top hit `american-math-monthly___2023___12287` (not relevant):

> Prove \[ \sum_{n=1}^{\infty}\left(n\left(\sum_{k=n}^{\infty}\frac{1}{k^2}\right)^2-\frac{1}{n}\right)=\frac{3}{2}-\frac{1}{2}\zeta(2)+\frac{3}{2}\zeta(3), \] where $\zeta$ is the Riemann zeta function, defined by $\zeta(s)=\sum_{k=1}^{\infty}1/k^s$.

Its profile: Techniques: Series manipulation, Telescoping series, Zeta function properties Proof move: Identify a nested series structure -> Express the inner sum in a closed form -> Use properties of the zeta function to simplify -> Recognize a telescoping pattern in the outer sum Key insight: The nested sums can be simplified using known series properties, leading to a telescoping effect. Also known as: Summation by parts, Series reduction, Zeta function evaluation

**q01342**: nDCG@10 0.682 -> 0.393 (-0.288)

> Let $C_n$ be the $n$th Catalan number, given by $C_n=\frac{1}{n+1}\binom{2n}{n}$. Show that: (a) $\sum_{n=0}^{\infty} \frac{2^n}{C_n}=5+\frac{3}{2\pi};$ (b) $\sum_{n=0}^{\infty} \frac{3^n}{C_n}=22+\frac{8}{\sqrt{3\pi}}.$

Query profile: Techniques: Generating Function, Series Expansion, Integral Representation Proof move: Identify the generating function for Catalan numbers -> Expand the series using known generating function properties -> Recognize the resulting integrals as standard forms involving π. Key insight: The generating function for Catalan numbers can be expressed as a simple rational function. Also known as: Inversion Formula, Analytic Continuation, Fundamental Theorem of Calculus for Series

Relevant doc `american-math-monthly___2020___12094`: rank 1 (baseline) -> 1 (E4)

E4's top hit `american-math-monthly___2020___12094` (relevant):

> Let $G$ be Catalan's constant, defined to be $\sum_{n=0}^{\infty}(-1)^n/(2n+1)^2$. Prove \[ \sum_{n=0}^{\infty}\frac{{2n\choose n}^2}{16^n (n+1)^3}=16\log 2-\frac{32G}{\pi}+\frac{48}{\pi}-16. \]

Its profile: Techniques: Series Transformation, Integral Representation, Special Function Evaluation Proof move: Recognize the series as a special case of a hypergeometric function -> Use integral representations to connect to known constants -> Evaluate the integral in terms of logarithms and Catalan's constant Key insight: The series can be expressed as an integral involving a rational function that simplifies to a combination of logarithms and Catalan's constant. Also known as: Logarithmic-Constant Decomposition, Hypergeometric Simplification

**q01079**: nDCG@10 0.359 -> 0.095 (-0.264)

> Let $H_n$ be the $n$th harmonic number, given by $H_n=\sum_{k=1}^n 1/k$. Let \[ S_k=\sum_{n=1}^{\infty}(-1)^{n-1}\bigl(\log k-(H_{kn}-H_n)\bigr). \] Prove that for $k\ge 2$, \[ S_k=\frac{k-1}{2k}\log 2+\frac{1}{2}\log k-\frac{\pi}{2k^2}\sum_{l=1}^{\lfloor k/2\rfloor}(k+1-2l)\cot\left(\frac{(2l-1)\pi...

Query profile: Techniques: Series Manipulation, Logarithmic Series, Harmonic Number Properties, Trigonometric Summation Proof move: Recognize the alternating series, separate the constant terms, apply harmonic number difference, transform into a telescoping series, use logarithmic identities, introduce a trigonometric sum, apply cotangent properties. Key insight: The alternating series can be decomposed into a sum of constants and a telescoping part involving harmonic numbers. Also known as: Telescoping Series Decomposition, Logarithmic Series Expansion, Trigonometric Cotangent Sum Formula

Relevant doc `american-math-monthly___2023___12254`: rank 1 (baseline) -> 18 (E4)

E4's top hit `american-math-monthly___2023___12246` (not relevant):

> Let $\zeta$ be the Riemann zeta function, defined for $n\ge2$ by $\zeta(n)=\sum_{k=1}^{\infty}\frac1{k^n}$. Let $H_n$ be the $n$th harmonic number, defined by $H_n=\sum_{k=1}^n\frac1k$. Prove \[ \sum_{n=2}^{\infty}\frac{\zeta(n)}{n^2}+\sum_{n=2}^{\infty}\frac{(-1)^n\zeta(n)H_n}{n}=\frac{\pi^2}{6}. \...

Its profile: Techniques: Series manipulation, alternating series, zeta function properties Proof move: Recognize the zeta function's relationship to the harmonic series -> Express each term as a double sum -> Identify the resulting series as a known alternating series -> Sum the series using properties of the Riemann zeta function and Euler's formula Key insight: The double sum representation reveals an alternating pattern that can be summed using complex analysis techniques. Also known as: Telescoping series, complex plane evaluation, Euler's identity application

**q02001**: nDCG@10 0.319 -> 0.085 (-0.234)

> For $x>1$, prove \[ \frac{i}{2}\int_{-\infty}^{\infty} \frac{\tanh(\pi t)}{\left(\frac{1}{2}+it\right)^x}\,dt = \zeta(x), \] where $\zeta$ is the Riemann zeta function.

Query profile: Techniques: Contour Integration, Residue Theorem, Functional Equation Proof move: Define a complex function -> Choose a contour -> Evaluate residues -> Relate to the original integral Key insight: The integral along the real axis transforms into a sum over residues. Also known as: Pole Analysis, Complex Path Shift, Residue Summation

Relevant doc `american-math-monthly___2024___12317`: rank 3 (baseline) -> 27 (E4)

E4's top hit `american-math-monthly___2024___12332` (not relevant):

> Prove \[ \int_0^{\infty}\frac{\tanh^2 x}{x^2}\,dx=\frac{14\,\zeta(3)}{\pi^2}, \] where $\zeta(3)$ is Ap\'ery’s constant $\sum_{k=1}^{\infty}1/k^3$.

Its profile: Techniques: Contour Integration, Residue Calculation, Series Expansion Proof move: Define a complex function with branch cuts, integrate around a keyhole contour, equate real and imaginary parts, simplify using series. Key insight: The integral can be transformed into a sum of residues, leveraging the series expansion of $\tanh^2 x$. Also known as: Summing Residues, Complex Path Integration, Analytic Continuation Technique

**q03064**: nDCG@10 0.286 -> 0.066 (-0.220)

> Prove that \[ \sum_{n\ge 1}\frac{1}{n^2}=\frac{\pi^2}{6} \] by applying the residue theorem to the meromorphic function \[ f(z)=\frac{\pi\cot(\pi z)}{z^2} \] integrated over the boundary of the rectangle $R_N$ with vertices $\pm\left(N+\tfrac12\right)\pm i\left(N+\tfrac12\right)$, and letting $N\to\...

Query profile: Techniques: Contour Integration, Residue Calculation, Series Expansion Proof move: Define contour -> Integrate function -> Apply residue theorem -> Expand residues -> Relate to series Key insight: The residues of the cotangent function at integer points sum to the series. Also known as: Summation via residues, Complex analysis evaluation, Periodic function analysis

Relevant doc `american-math-monthly___2022___12180`: rank 1 (baseline) -> 36 (E4)

E4's top hit `harvard-quals___2021___F21.4` (not relevant):

> Evaluate the series \[ \sum_{n=-\infty}^{\infty} \frac{n^2+n+1}{n^4+1} \] by integrating $R(z)\cot \pi z$ for some appropriate rational function $R(z)$ over the boundary of the square $C_n\subset \mathbf{C}$ whose four vertices are $(n+\tfrac12)(\pm 1\pm i)$ and then letting $n\to\infty$.

Its profile: Techniques: Residue Theorem, Contour Integration, Series Evaluation via Complex Analysis Proof move: Identify poles -> Calculate residues -> Sum residues -> Relate to original series Key insight: The sum of residues equals the original series in the limit. Also known as: Summing by residues, Complex analysis evaluation, Contour summation

**q00570**: nDCG@10 0.275 -> 0.066 (-0.208)

> Let $\beta$ and $t$ be real numbers with $t>0$. Let $\operatorname{erf}(x)=\frac{2}{\sqrt{\pi}}\int_0^x e^{-u^2}\,du$, let $\gamma(x,y)=\int_0^y u^{x-1}e^{-u}\,du$, and let $\Gamma(x)=\int_0^{\infty} u^{x-1}e^{-u}\,du$. Show that \[ \sum_{n=0}^{\infty}\left(\frac{\beta^2}{1+\beta^2}\right)^n\frac{\g...

Query profile: Techniques: Series Expansion, Integral Transformation, Gamma Function Properties Proof move: Recognize the series as a power series expansion -> Identify the integral as a form of the Gamma function -> Use the definition of the error function to simplify Key insight: The series and integrals can be linked through the properties of the error function and the Gamma function. Also known as: Euler's Formula for Power Series, Reduction to Fundamental Integral Forms, Error Function Representation

Relevant doc `american-math-monthly___2022___12180`: rank 2 (baseline) -> 9 (E4)

E4's top hit `american-math-monthly___2004___11000` (not relevant):

> Let $a$ be a real number. Evaluate in closed form \[ \int_{0}^{\pi/2} \operatorname{erf}(a\cos\theta)\,\operatorname{erf}(a\sin\theta)\,\sin(2\theta)\,d\theta, \] where $\operatorname{erf}(x)=2\pi^{-1/2}\int_0^x e^{-t^2}\,dt$.

Its profile: Techniques: Change of Variables, Symmetry, Integration by Parts Proof move: Identify the integrand's symmetry -> Apply change of variables -> Recognize the integral as a product of error functions over symmetric intervals Key insight: The integral can be simplified by exploiting the symmetry in the error function products. Also known as: Polar Coordinates Transformation, Error Function Pairing, Symmetric Interval Reduction

**q00104**: nDCG@10 0.183 -> 0.000 (-0.183)

> The Bernoulli numbers $B_n$ (for $n=0,1,2,\dots$) are defined by \[ \frac{t}{e^t-1}=\sum_{n=0}^\infty \frac{B_n t^n}{n!}, \] which converges for $|t|<2\pi$. Also, for each nonnegative integer $n$, the Bernoulli polynomial $B_n(x)$ is defined by \[ B_n(x)=\sum_{k=0}^n \binom{n}{k} B_{n-k}x^k. \] For ...

Query profile: Techniques: Generating functions, Polynomial expansion, Recurrence relations Proof move: Identify the generating function for Bernoulli numbers, expand the product of two such functions, match coefficients, apply the recurrence relation for Bernoulli polynomials. Key insight: The coefficients of the expanded product match those of the linear combination involving Bernoulli polynomials at shifted arguments. Also known as: Coefficient comparison, Polynomial convolution, Symmetry in polynomial expansions

Relevant doc `american-math-monthly___1999___10575`: rank 3 (baseline) -> 25 (E4)

E4's top hit `american-math-monthly___2016___11791` (not relevant):

> Show that for $r\ge 1$, \[ \sum_{s=1}^{r}\binom{6r+1}{6s-2}B_{6s-2}=-\frac{6r+1}{6}, \] where $B_n$ denotes the $n$th Bernoulli number.

Its profile: Techniques: Generating Functions, Series Manipulation, Symmetry Arguments Proof move: Define generating function -> Substitute Bernoulli numbers -> Recognize telescoping series -> Apply symmetry in binomial coefficients -> Conclude with constant term extraction Key insight: The alternating sum of coefficients of a specific power in the generating function for Bernoulli numbers reveals a linear relationship. Also known as: Residue Calculation, Coefficient Extraction, Power Series Analysis

**q01506**: nDCG@10 0.555 -> 0.384 (-0.171)

> Find \[ \sum_{n=1}^{\infty}\sinh^{-1}\left(\frac{1}{\sqrt{2^{n+2}+2}+\sqrt{2^{n+1}+2}}\right). \]

Query profile: Techniques: Series Transformation, Hyperbolic Function Simplification Proof move: Recognize the series as telescoping -> Simplify each term using hyperbolic identity -> Observe cancellation pattern in partial sums Key insight: Each term can be expressed as difference of two hyperbolic arcsines Also known as: Telescoping Series, Partial Fraction Decomposition in Hyperbolic Space

Relevant doc `american-math-monthly___2017___11853`: rank 1 (baseline) -> 1 (E4)

E4's top hit `american-math-monthly___2017___11853` (relevant):

> Find \[ \sum_{n=1}^{\infty}\frac{1}{\sinh 2^n}\,. \]

Its profile: Techniques: Series Transformation, Hyperbolic Function Manipulation Proof move: Recognize hyperbolic sine as exponential -> Use series expansion of exponential -> Transform into telescoping series -> Sum finite portion Key insight: The hyperbolic sine term can be expressed using exponentials, leading to a telescoping series when expanded. Also known as: Exponential Substitution, Telescoping Series Trick

**q01630**: nDCG@10 0.234 -> 0.073 (-0.160)

> Prove \[ \int_0^1 \frac{\arctan x}{x}\log\left(\frac{1+x^2}{(1-x)^2}\right)\,dx=\frac{\pi^3}{16}. \]

Query profile: Techniques: Substitution, Integration by Parts, Logarithmic Differentiation Proof move: Recognize the integral as a result of a specific function's derivative, apply integration by parts, simplify using logarithmic properties Key insight: The integrand is the derivative of a product involving arctan and a logarithmic function Also known as: Logarithmic Derivative Recognition, Derivative Pairing

Relevant doc `american-math-monthly___2024___12317`: rank 2 (baseline) -> 15 (E4)

E4's top hit `american-math-monthly___2023___12274` (not relevant):

> Evaluate \[ \int_0^1 \frac{\arctan x}{1+x^2}\left(\ln\left(\frac{2x}{1-x^2}\right)\right)^2\,dx. \]

Its profile: Techniques: Substitution, Integration by Parts, Logarithmic Differentiation Proof move: Recognize the integrand as a derivative of a product -> Identify u and dv -> Apply integration by parts formula -> Simplify using logarithmic properties Key insight: The integrand resembles the derivative of a product of functions involving arctan and logarithms. Also known as: Logarithmic Exponent Manipulation, Derivative Recognition

**q00239**: nDCG@10 0.220 -> 0.064 (-0.156)

> Suppose that the functions $f(r)$ and $g(r)$ are positive and continuous for $0\le r<1$. Using polar coordinates $(r,\theta)$, define a metric on the open unit disk by \[ ds^2=f(r)^2\,dr^2+g(r)^2 r^2\,d\theta^2. \] For what choices of $f(r)$ and $g(r)$ does the open unit disk with this metric furnis...

Query profile: Techniques: Change of Variables, Differential Geometry, Metric Tensor Analysis Proof move: Identify invariant property -> Compare to known metric -> Solve for functions Key insight: The metric must be conformally equivalent to the Poincaré disk model. Also known as: Conformal Mapping, Hyperbolic Geometry Equivalence

Relevant doc `harvard-quals___2023___S23.5`: rank 1 (baseline) -> 10 (E4)

E4's top hit `harvard-quals___2013___F13.I.5` (not relevant):

> Let $\mathbb H=\{(x,y)\in\mathbf R^2:y>0\}$ be the upper half plane. Let $g$ be the Riemannian metric on $\mathbb H$ given by \[ g=\frac{(dx)^2+(dy)^2}{y^2}. \] $(\mathbb H,g)$ is known as the half-plane model of the hyperbolic plane. (a) Let $\gamma(\theta)=(\cos\theta,\sin\theta)$ and $\eta(\theta...

Its profile: Techniques: Invariance, Differential Invariants, Geodesic Equivalence Proof move: Identify invariant properties -> Derive differential equations -> Solve for geodesics Key insight: The metric's form implies a specific differential equation whose solutions are geodesics. Also known as: Symmetry Argument, Covariant Derivative Analysis

