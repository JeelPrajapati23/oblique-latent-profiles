# Prompt hand-test: math

- Variant: `math-265081__Qwen2.5-7B-Instruct-AWQ` (prompts: doc=`math_problem`, query=`math_problem`)
- Model: `Qwen/Qwen2.5-7B-Instruct-AWQ`, greedy decoding
- Words per profile: min 30, median 39, max 53 (target 60-120); in range: 0/20
- Format compliant (3 fields): 20/20
- Profiles with copied content words: 14/20

| Cosine (Qwen3-0.6B) | same group | different group | gap |
|---|---|---|---|
| raw text | 0.468 | 0.342 | +0.127 |
| profile | 0.653 | 0.513 | +0.140 |

A bigger gap means profiles separate the hidden property better than raw text does.

## Group 1

**query `q00740`** (45 words)

> Evaluate \[ \int_0^1 \frac{\log\bigl(\cos(\pi x/2)\bigr)}{x(1+x)}\,dx. \]

Profile: Techniques: substitution, series expansion, symmetry

Proof move: assume an integral form -> expand logarithm and cosine -> identify symmetric terms -> simplify using symmetry -> recognize telescoping series

Key insight: The integrand can be decomposed into symmetric components that cancel out, leaving a telescoping series.

Copied words: -

**doc `american-math-monthly___2019___12012`** (43 words)

> Let $k$ be a nonnegative integer. Find the set of real numbers $x$ for which the power series \[ \sum_{n=k}^{\infty}\binom{n}{k}\left(e-1-\frac{1}{1!}-\frac{1}{2!}-\cdots-\frac{1}{n!}\right)x^n \] converges, and determine the sum.

Profile: Techniques: Power series analysis, binomial coefficient properties, exponential series recognition
Proof move: Recognize the exponential series -> isolate the constant term -> apply binomial theorem -> identify convergence radius
Key insight: The series simplifies to a form involving $e$ and a binomial expansion.

Copied words: power, series

**doc `american-math-monthly___2004___10977`** (47 words)

> Let $\beta$ and $t$ be real numbers with $t>0$. Let $\operatorname{erf}(x)=\frac{2}{\sqrt{\pi}}\int_0^x e^{-u^2}\,du$, let $\gamma(x,y)=\int_0^y u^{x-1}e^{-u}\,du$, and let $\Gamma(x)=\int_0^{\infty} u^{x-1}e^{-u}\,du$. Show that \[ \sum_{n=0}^{\infty}\left(\frac{\beta^2}{1+\beta^2}\right)^n\frac{\gamma\left(n+\tfrac12,(1+\beta^2)t\right)}{\Gamma\left(n+\tfrac12\right)} =(1+\beta^2)\operatorname{e...

Profile: Techniques: Generating function, integral representation, series manipulation
Proof move: Recognize the series as a generating function -> match terms using integral representations -> simplify using properties of the error function
Key insight: The series can be interpreted as a weighted sum of error functions with specific parameters.

Copied words: -

**doc `american-math-monthly___1999___10575`** (40 words)

> Prove that \[ \sum_{\ell=0}^n (-1)^\ell\binom{n}{\ell}(2\ell)!\sum_{m=0}^{2\ell}\frac{(-1)^m}{m!} = \sum_{\ell=0}^n (-1)^\ell\binom{n}{\ell}2^{\,n-\ell}(n+\ell)! \] for every nonnegative integer $n$.

Profile: Techniques: binomial theorem, series manipulation, factorial properties
Proof move: assume the sum form -> apply series expansion -> simplify using factorial identities -> match terms
Key insight: The alternating series and factorials create a telescoping effect that simplifies the expression.

Copied words: -

## Group 2

**query `q01528`** (32 words)

> Prove \[ \sum_{n=1}^{\infty}\frac{2^{2n-1}}{2n+1}\left(\frac{(n-1)!}{(2n-1)!!}\right)^2=\pi-2, \] where $(2n-1)!!$ is defined as usual to be $\prod_{k=1}^n(2k-1)$.

Profile: Techniques: telescoping, series manipulation
Proof move: identify a telescoping pattern -> simplify infinite series -> match target expression
Key insight: Each term can be expressed as a difference of two other terms.

Copied words: -

**doc `american-math-monthly___2025___12396`** (30 words)

> Let $F_n$ be the $n$th Fibonacci number, where $F_0=0$, $F_1=1$, and $F_n=F_{n-1}+F_{n-2}$ when $n\ge 2$. Prove \[ \sum_{n=1}^{\infty}\arctan\left(\frac{1}{3F_n^2}\right)=\frac{\pi}{4}. \]

Profile: Techniques: telescoping, arctan identity
Proof move: assume an infinite series -> use arctan addition formula -> telescoping sum -> evaluate limit
Key insight: adjacent terms cancel, leaving a constant difference.

Copied words: arctan

**doc `american-math-monthly___2008___11260`** (47 words)

> Find those nonnegative values of $\alpha$ and $\beta$ for which \[ \sum_{n=1}^{\infty}\prod_{k=1}^{n}\frac{\alpha+k\log k}{\beta+(k+1)\log(k+1)} \] converges. For those values of $\alpha$ and $\beta$, evaluate the sum.

Profile: Techniques: Comparison test, asymptotic analysis, limit comparison

Proof move: Analyze the ratio of consecutive terms -> Identify the dominant logarithmic terms -> Apply limit comparison to a known convergent series

Key insight: The growth rate of $\log n$ balances the linear terms, leading to a telescoping effect.

Copied words: -

**doc `american-math-monthly___2011___11515`** (30 words)

> Find a closed-form expression for \[ \sum_{n=1}^{\infty}4^n\sin^4\bigl(2^{-n}\theta\bigr). \]

Profile: Techniques: telescoping, series manipulation
Proof move: assume a series form -> apply trigonometric identity -> telescope terms -> recognize finite sum
Key insight: adjacent terms cancel, leaving a simple expression

Copied words: expression, form

## Group 3

**query `q00408`** (36 words)

> Let $X_1=1$, and for $m\ge 1$ let \[ X_{m+1}=(m+3/2)^{-1}\sum_{k=1}^{m}X_kX_{m+1-k}. \] Evaluate $\lim_{m\to\infty}X_m/X_{m+1}$.

Profile: Techniques: induction on m, telescoping
Proof move: assume a limit exists -> apply induction step -> simplify using telescoping sum -> find a constant ratio
Key insight: the ratio between consecutive terms stabilizes as m grows.

Copied words: -

**doc `american-math-monthly___2025___12418`** (40 words)

> Let $\Phi$ be the cumulative distribution function of a standard normal random variable, defined by \[ \Phi(x)=\frac{1}{\sqrt{2\pi}}\int_{-\infty}^x e^{-t^2/2}\,dt. \] (a) For positive real numbers $\sigma_1,\dots,\sigma_n$ and $w_1,\dots,w_n$ with $\sum_{i=1}^n w_i=1$, determine \[ \lim_{x\to\infty}\frac{1}{x}\,\Phi^{-1}\left(\sum_{i=1}^n w_i\Phi\left(\frac{x}{\sigma_i}\right)\right). \] (b) Let ...

Profile: Techniques: Central limit theorem, asymptotic analysis, change of variables

Proof move: Apply central limit theorem -> analyze leading terms -> identify asymptotic behavior

Key insight: The weighted sum of scaled standard normals approximates a standard normal as $x \to \infty$.

Copied words: infty, limit, normal, standard

**doc `harvard-quals___2014___S14.II.3`** (37 words)

> Suppose that $f$ is holomorphic in an open set containing the closed unit disk $\{|z|\le 1\}$ in $\mathbb{C}$, except for a pole at $z_0$ on the unit circle $\{|z|=1\}$. Show that if \[ \sum_{n=0}^{\infty} a_n z^n \] denote the power series expansion of $f$ in the open unit disk $\{|z|<1\}$, then \[ \lim_{n\to\infty}\frac{a_n}{a_{n+1}}=z_0. \]

Profile: Techniques: residue theorem, asymptotic analysis, singularity analysis
Proof move: apply residue theorem at pole -> analyze asymptotic behavior of coefficients -> derive limit relation
Key insight: The growth rate of coefficients near a pole dictates the limit.

Copied words: pole

**doc `american-math-monthly___2025___12392`** (30 words)

> For which positive integers $a$ is there a nonzero polynomial $P(x,y)\in\mathbb{C}[x,y]$ such that \[ P\left(\binom{2n}{n},\binom{an}{n}\right)=0 \] for all nonnegative integers $n$?

Profile: Techniques: Polynomial identity, extremal principle

Proof move: Assume an extremal polynomial -> consider its degree -> derive a contradiction

Key insight: No nontrivial polynomial can vanish on infinitely many points.

Copied words: polynomial

## Group 4

**query `q01165`** (42 words)

> Let $A_0,B_0$, and $C_0$ be noncollinear points in the plane. Let $p$ be a line that meets lines $B_0C_0$, $C_0A_0$, and $A_0B_0$ at $A^*$, $B^*$, and $C^*$ respectively. For $n\ge1$, let $A_n$ be the intersection of $B^*B_{n-1}$ with $C^*C_{n-1}$, and define $B_n$ and $C_n$ similarly. Show that all three sequences converge, and describe their respective limits.

Profile: Techniques: extremal principle, induction on n, proof by contradiction

Proof move: assume an extremal object -> induction step -> contradiction

Key insight: The sequences of points are constrained to converge due to the finite plane area and the nature of line intersections.

Copied words: converge, line, plane, points, sequences

**doc `harvard-quals___2024___F24.3`** (39 words)

> Suppose $R_1,R_2$ are bounded, simply-connected open subsets of $\mathbb C$. Let $z_1\in R_1$ and $z_2\in R_2$.  i) Prove that there is a holomorphic bijective function $f:R_1\to R_2$ such that $f(z_1)=z_2$.  ii) Suppose that $g:R_1\to R_2$ is a holomorphic function such that $g(z_1)=z_2$. Prove that $|g'(z_1)|\le |f'(z_1)|$.

Profile: Techniques: Riemann mapping theorem, Schwarz lemma

Proof move: apply Riemann mapping theorem -> map to unit disk -> apply Schwarz lemma -> compare derivatives

Key insight: The derivative's magnitude is bounded by the geometry of the domain and target.

Copied words: bounded

**doc `berkeley-quals___1990___F6.1.6`** (37 words)

> Does the set $G=\{a\in\mathbb{R}\mid a>0,\ a\neq 1\}$ form a group with the operation $a*b=a^{\log b}$?

Profile: Techniques: group axioms, logarithmic properties, functional equations

Proof move: assume $G$ is a group -> check closure -> find identity -> examine inverses -> identify failure

Key insight: the operation does not satisfy the group's inverse property.

Copied words: group, operation

**doc `american-math-monthly___1998___10554`** (37 words)

> Suppose that the functions $f(r)$ and $g(r)$ are positive and continuous for $0\le r<1$. Using polar coordinates $(r,\theta)$, define a metric on the open unit disk by \[ ds^2=f(r)^2\,dr^2+g(r)^2 r^2\,d\theta^2. \] For what choices of $f(r)$ and $g(r)$ does the open unit disk with this metric furnish a model of the hyperbolic plane?

Profile: Techniques: extremal principle, comparison with standard model

Proof move: assume an extremal metric -> compare warping functions -> match Gaussian curvature formula

Key insight: the warping functions must induce the same curvature as the Poincaré disk model.

Copied words: disk, functions, metric, model

## Group 5

**query `q03053`** (53 words)

> Let $V_k(\mathbb{R}^n) = \{A \in M_{n\times k}(\mathbb{R}) \mid A^\top A = I_k\}$.  (a) Show that $V_k(\mathbb{R}^n)$ is a smooth submanifold of $M_{n\times k}(\mathbb{R})$ and compute its dimension.  (b) Show that $T_A V_k(\mathbb{R}^n) = \{X \in M_{n\times k}(\mathbb{R}) \mid A^\top X + X^\top A = 0\}$.  (c) Using the inner product $\langle X, Y \rangle := \operatorname{tr}(X^\top Y)$ in $M_{n\t...

Profile: Techniques: Implicit function theorem, tangent space computation, invariant metric construction
Proof move: assume an extremal object -> apply implicit function theorem -> compute tangent space -> verify invariance under orthogonal action
Key insight: The structure of the constraint $A^\top A = I_k$ dictates the tangent space and allows for an invariant metric construction.

Copied words: action, invariance, invariant, metric, verify

**doc `harvard-quals___2024___S24.13`** (49 words)

> Show that the orthogonal group \[ O(n)=\{A\in M(n,\mathbf{R})\mid A^T A=\mathrm{id}\} \] for integer $n>1$ is a smooth manifold, where $M(n,\mathbf{R})$ consists of $n$ by $n$ matrices with entries in $\mathbf{R}$. (Hint: use the implicit function theorem.)  Syllabus topics: smooth manifold, implicit function theorem.

Profile: Techniques: implicit function theorem, differential of a function

Proof move: assume a matrix in $O(n)$ -> consider the function $f(A) = A^T A - \mathrm{id}$ -> apply implicit function theorem -> conclude the existence of a smooth chart

Key insight: the Jacobian determinant of $f$ is non-zero on $O(n)$.

Copied words: function, implicit, mathrm, smooth, theorem

**doc `harvard-quals___2015___S15.3`** (35 words)

> Let \[ M = \{(x,y,z)\in \mathbb{R}^3 \mid x^2 - y^2 - z^3 - z = 0\}. \]  (a) Prove that $M$ is a smooth surface in $\mathbb{R}^3$.  (b) For what values of $c\in \mathbb{R}$ does the plane $z=c$ intersect $M$ transversely?

Profile: Techniques: Implicit function theorem, transversality
Proof move: Assume a smooth function -> apply implicit function theorem -> check transversality condition -> conclude intersection properties
Key insight: Analyze the Jacobian to ensure non-degeneracy of the intersection.

Copied words: smooth

**doc `harvard-quals___2020___S20.6`** (46 words)

> (DG)  Let $f:\mathbb{R}^3\to \mathbb{R}$ be defined by $f(x,y,z)=x^2+y^2-1$.  (i) Prove that $M=f^{-1}(0)$ is a two-dimensional embedded submanifold of $\mathbb{R}^3$.  (ii) For $a,b,c\in \mathbb{R}$, consider the vector field \[ X=a\frac{\partial}{\partial x}+b\frac{\partial}{\partial y}+c\frac{\partial}{\partial z}. \] For which values of $a,b,c$ is $X$ tangent to $M$ at the point $(1,0,1)$? 

Profile: Techniques: Implicit function theorem, tangent space computation
Proof move: Assume $X$ is tangent -> Evaluate $X$ at $(1,0,1)$ -> Compute partial derivatives -> Set equal to zero -> Solve for $a,b,c$
Key insight: The tangent space condition reduces to a system of linear equations in $a,b,c$.

Copied words: partial, tangent
