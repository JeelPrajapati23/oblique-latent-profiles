# Prompt hand-test: math_soln

- Variant: `math_soln-33bb08__Qwen2.5-7B-Instruct-AWQ` (prompts: doc=`math_problem_solution`, query=`math_problem`)
- Model: `Qwen/Qwen2.5-7B-Instruct-AWQ`, decoding `greedy-freqpen0.3`
- Words per profile: min 36, median 54, max 73 (target 60-120); in range: 7/20
- Format compliant (4 fields): 20/20
- Profiles containing formula symbols ($ \ ^ _ { } =): 7/20
- Profiles with copied content words: 12/20

| Cosine (Qwen3-0.6B) | same group | different group | gap |
|---|---|---|---|
| raw text | 0.468 | 0.342 | +0.127 |
| profile | 0.702 | 0.555 | +0.147 |

A bigger gap means profiles separate the hidden property better than raw text does.

| Leave-one-out P@3 (chance 0.158) | BM25 | dense |
|---|---|---|
| raw text | 0.317 | 0.450 |
| profile | 0.683 | 0.650 |

P@3 is closer to retrieval: for each item, how many of its top-3 neighbours share its hidden property. Cosine gap alone undersold BM25-friendly profiles (round 2).

## Group 1

**query `q00740`** (57 words)

> Evaluate \[ \int_0^1 \frac{\log\bigl(\cos(\pi x/2)\bigr)}{x(1+x)}\,dx. \]

Profile: Techniques: Substitution, Integration by Parts, Series Expansion
Proof move: Recognize the integral as a form of Frullani's integral -> Identify the logarithmic function's properties -> Expand the series and integrate term by term
Key insight: The integral can be transformed into a product of two simpler functions through a clever substitution.
Also known as: Logarithmic Differentiation, Functional Equation Solution

Copied words: -

**doc `american-math-monthly___2019___12012`** (53 words)

> Let $k$ be a nonnegative integer. Find the set of real numbers $x$ for which the power series \[ \sum_{n=k}^{\infty}\binom{n}{k}\left(e-1-\frac{1}{1!}-\frac{1}{2!}-\cdots-\frac{1}{n!}\right)x^n \] converges, and determine the sum.

Profile: Techniques: Comparison, Integration, Series Manipulation
Proof move: Define a sequence -> Express the sequence in terms of integrals -> Use bounds to show convergence -> Integrate the series term by term -> Apply integration by parts
Key insight: The integral representation simplifies the series and allows for easy evaluation.
Also known as: Induction, Integral Transformation, Series Expansion

Copied words: series

**doc `american-math-monthly___2004___10977`** (53 words)

> Let $\beta$ and $t$ be real numbers with $t>0$. Let $\operatorname{erf}(x)=\frac{2}{\sqrt{\pi}}\int_0^x e^{-u^2}\,du$, let $\gamma(x,y)=\int_0^y u^{x-1}e^{-u}\,du$, and let $\Gamma(x)=\int_0^{\infty} u^{x-1}e^{-u}\,du$. Show that \[ \sum_{n=0}^{\infty}\left(\frac{\beta^2}{1+\beta^2}\right)^n\frac{\gamma\left(n+\tfrac12,(1+\beta^2)t\right)}{\Gamma\left(n+\tfrac12\right)} =(1+\beta^2)\operatorname{e...

Profile: Techniques: Laplace transform, integral manipulation, series summation

Proof move: Define a function, apply its Laplace transform, use properties to simplify, recognize a geometric series

Key insight: Transforming the integral into a form suitable for Laplace transform and recognizing the geometric series sum

Also known as: Integral representation technique, transform and simplify, series recognition

Copied words: -

**doc `american-math-monthly___1999___10575`** (55 words)

> Prove that \[ \sum_{\ell=0}^n (-1)^\ell\binom{n}{\ell}(2\ell)!\sum_{m=0}^{2\ell}\frac{(-1)^m}{m!} = \sum_{\ell=0}^n (-1)^\ell\binom{n}{\ell}2^{\,n-\ell}(n+\ell)! \] for every nonnegative integer $n$.

Profile: Techniques: Umbral calculus, Integral representation, Generating functions

Proof move: Define operators to simplify expressions -> Apply binomial theorem to operators -> Use properties of the shift operator -> Evaluate at specific points

Key insight: Transforming the sum into an operator form allows simplification using algebraic identities.

Also known as: Finite difference calculus, Operational calculus, Symbolic manipulation of operators

Copied words: -

## Group 2

**query `q01528`** (69 words)

> Prove \[ \sum_{n=1}^{\infty}\frac{2^{2n-1}}{2n+1}\left(\frac{(n-1)!}{(2n-1)!!}\right)^2=\pi-2, \] where $(2n-1)!!$ is defined as usual to be $\prod_{k=1}^n(2k-1)$.

Profile: Techniques: Series manipulation, factorial simplification, double factorial properties
Proof move: Recognize the series as a telescoping series -> Simplify the general term using factorial and double factorial -> Identify the telescoping nature by canceling intermediate terms -> Realize the remaining terms sum to $\pi-2$
Key insight: The series can be simplified to a form that telescopes, leaving only boundary terms.
Also known as: Telescoping series recognition, factorial reduction, double factorial cancellation

Copied words: -

**doc `american-math-monthly___2025___12396`** (46 words)

> Let $F_n$ be the $n$th Fibonacci number, where $F_0=0$, $F_1=1$, and $F_n=F_{n-1}+F_{n-2}$ when $n\ge 2$. Prove \[ \sum_{n=1}^{\infty}\arctan\left(\frac{1}{3F_n^2}\right)=\frac{\pi}{4}. \]

Profile: Techniques: Telescoping Series, Trigonometric Identity

Proof move: Recognize a telescoping pattern -> Apply a trigonometric identity -> Simplify the sum

Key insight: The chosen $G_n$ allows the sum to telescope, simplifying the infinite series to a finite difference.

Also known as: Difference of Arctangents, Angle Subtraction Formula

Copied words: -

**doc `american-math-monthly___2008___11260`** (60 words)

> Find those nonnegative values of $\alpha$ and $\beta$ for which \[ \sum_{n=1}^{\infty}\prod_{k=1}^{n}\frac{\alpha+k\log k}{\beta+(k+1)\log(k+1)} \] converges. For those values of $\alpha$ and $\beta$, evaluate the sum.

Profile: Techniques: Comparison test, Telescoping series, Limit of product

Proof move: Identify divergent series -> Use comparison to show divergence -> Transform product into difference of sums -> Recognize telescoping nature -> Conclude convergence by limit of product

Key insight: The product simplifies to a telescoping form that converges to zero.

Also known as: Limiting ratio test, Logarithmic decrement method, Infinite product convergence through cancellation

Copied words: converges

**doc `american-math-monthly___2011___11515`** (50 words)

> Find a closed-form expression for \[ \sum_{n=1}^{\infty}4^n\sin^4\bigl(2^{-n}\theta\bigr). \]

Profile: Techniques: Telescoping Series, Limit Evaluation

Proof move: Recognize series pattern -> Simplify using trigonometric identity -> Evaluate remaining terms -> Take limit as n approaches infinity

Key insight: The series simplifies due to overlapping terms, leaving only the initial and final terms.

Also known as: Difference of Squares, Limit of Ratio, Trigonometric Reduction

Copied words: -

## Group 3

**query `q00408`** (51 words)

> Let $X_1=1$, and for $m\ge 1$ let \[ X_{m+1}=(m+3/2)^{-1}\sum_{k=1}^{m}X_kX_{m+1-k}. \] Evaluate $\lim_{m\to\infty}X_m/X_{m+1}$.

Profile: Techniques: Recurrence relation, Limit analysis, Symmetry in sequences

Proof move: Identify a stable ratio,-> apply limit to both sides,-> recognize telescoping pattern,-> exploit symmetry in recursive definition

Key insight: The ratio $X_m/X_{m+1}$ stabilizes as $m$ increases.

Also known as: Fixed point iteration, Asymptotic behavior analysis, Recursive equilibrium

Copied words: -

**doc `american-math-monthly___2025___12418`** (66 words)

> Let $\Phi$ be the cumulative distribution function of a standard normal random variable, defined by \[ \Phi(x)=\frac{1}{\sqrt{2\pi}}\int_{-\infty}^x e^{-t^2/2}\,dt. \] (a) For positive real numbers $\sigma_1,\dots,\sigma_n$ and $w_1,\dots,w_n$ with $\sum_{i=1}^n w_i=1$, determine \[ \lim_{x\to\infty}\frac{1}{x}\,\Phi^{-1}\left(\sum_{i=1}^n w_i\Phi\left(\frac{x}{\sigma_i}\right)\right). \] (b) Let ...

Profile: Techniques: Limit manipulation, asymptotic equivalence, infinitesimal substitution

Proof move: Identify the dominant term in the limit expression, simplify the expression by substituting the dominant term, and use known limits to evaluate the remaining terms.

Key insight: The ratio of differences in cumulative distribution functions can be approximated by a constant factor as \(x\) approaches infinity.

Also known as: Dominant term analysis, asymptotic scaling, infinitesimal substitution technique

Copied words: cumulative, distribution, limit

**doc `harvard-quals___2014___S14.II.3`** (73 words)

> Suppose that $f$ is holomorphic in an open set containing the closed unit disk $\{|z|\le 1\}$ in $\mathbb{C}$, except for a pole at $z_0$ on the unit circle $\{|z|=1\}$. Show that if \[ \sum_{n=0}^{\infty} a_n z^n \] denote the power series expansion of $f$ in the open unit disk $\{|z|<1\}$, then \[ \lim_{n\to\infty}\frac{a_n}{a_{n+1}}=z_0. \]

Profile: Techniques: Dominant Term Analysis, Binomial Expansion, Limit Dominance

Proof move: Identify the dominant term in the expression as $n$ approaches infinity -> Simplify the ratio of consecutive terms by canceling out non-dominant terms -> The remaining expression evaluates to the pole location

Key insight: The behavior of the ratio of coefficients is determined by the term with the highest power of $n$.

Also known as: Asymptotic Behavior Analysis, Leading Coefficient Dominance, Power Term Predominance

Copied words: expansion, pole, power

**doc `american-math-monthly___2025___12392`** (60 words)

> For which positive integers $a$ is there a nonzero polynomial $P(x,y)\in\mathbb{C}[x,y]$ such that \[ P\left(\binom{2n}{n},\binom{an}{n}\right)=0 \] for all nonnegative integers $n$?

Profile: Techniques: Injectivity, Asymptotic Analysis, Monomial Growth Comparison

Proof move: Show that for $2\le a<b$, some monomial term in $P(x,y)$ grows exponentially faster than the rest, leading to a contradiction.

Key insight: The function $f(s,t)$ is injective, implying distinct monomials cannot cancel out asymptotically.

Also known as: Exponential Dominance, Injective Function Argument, Asymptotic Monomial Comparison

Copied words: -

## Group 4

**query `q01165`** (50 words)

> Let $A_0,B_0$, and $C_0$ be noncollinear points in the plane. Let $p$ be a line that meets lines $B_0C_0$, $C_0A_0$, and $A_0B_0$ at $A^*$, $B^*$, and $C^*$ respectively. For $n\ge1$, let $A_n$ be the intersection of $B^*B_{n-1}$ with $C^*C_{n-1}$, and define $B_n$ and $C_n$ similarly. Show that all three sequences converge, and describe their respective limits.

Profile: Techniques: Homothety, Invariant Points, Asymptotic Behavior

Proof move: Identify homothety -> Recognize invariant points -> Analyze asymptotic behavior of sequences

Key insight: The sequences converge to the intersection of the lines through the original points and their respective opposite sides.

Also known as: Fixed Point Analysis, Convergence to Invariant Elements, Asymptotic Homothety

Copied words: converge, intersection, lines, points, respective, sequences

**doc `harvard-quals___2024___F24.3`** (51 words)

> Suppose $R_1,R_2$ are bounded, simply-connected open subsets of $\mathbb C$. Let $z_1\in R_1$ and $z_2\in R_2$.  i) Prove that there is a holomorphic bijective function $f:R_1\to R_2$ such that $f(z_1)=z_2$.  ii) Suppose that $g:R_1\to R_2$ is a holomorphic function such that $g(z_1)=z_2$. Prove that $|g'(z_1)|\le |f'(z_1)|$.

Profile: Techniques: Change of Variables, Complex Differentiation, Integral Inequality

Proof move: Define a function through composition -> Use Cauchy's integral formula -> Derive the derivative relationship -> Apply the inequality

Key insight: The derivative of a function can be bounded by the derivative of its transformation.

Also known as: Jacobian Determinant, Holomorphic Transformation, Derivative Comparison

Copied words: bounded, function, holomorphic

**doc `berkeley-quals___1990___F6.1.6`** (36 words)

> Does the set $G=\{a\in\mathbb{R}\mid a>0,\ a\neq 1\}$ form a group with the operation $a*b=a^{\log b}$?

Profile: Techniques: Isomorphism, Transformation, Equivalence

Proof move: Define a mapping -> Apply the mapping -> Verify the properties -> Conclude isomorphism

Key insight: Mapping one operation to another equivalent operation preserves group structure.

Also known as: Homeomorphism, Correspondence, Structural equivalence

Copied words: group, operation

**doc `american-math-monthly___1998___10554`** (63 words)

> Suppose that the functions $f(r)$ and $g(r)$ are positive and continuous for $0\le r<1$. Using polar coordinates $(r,\theta)$, define a metric on the open unit disk by \[ ds^2=f(r)^2\,dr^2+g(r)^2 r^2\,d\theta^2. \] For what choices of $f(r)$ and $g(r)$ does the open unit disk with this metric furnish a model of the hyperbolic plane?

Profile: Techniques: Change of Variables, Integration, Hyperbolic Functions

Proof move: Recognize the metric's invariance under rotations and reflections -> Identify geodesics through the origin -> Use hyperbolic geometry properties to derive functional equations -> Transform variables to match the Poincaré disc model

Key insight: The given metric can be transformed into the Poincaré disc model using hyperbolic functions.

Also known as: Invariant Metric Transformation, Hyperbolic Geometry Mapping

Copied words: functions, hyperbolic, metric, model, using

## Group 5

**query `q03053`** (62 words)

> Let $V_k(\mathbb{R}^n) = \{A \in M_{n\times k}(\mathbb{R}) \mid A^\top A = I_k\}$.  (a) Show that $V_k(\mathbb{R}^n)$ is a smooth submanifold of $M_{n\times k}(\mathbb{R})$ and compute its dimension.  (b) Show that $T_A V_k(\mathbb{R}^n) = \{X \in M_{n\times k}(\mathbb{R}) \mid A^\top X + X^\top A = 0\}$.  (c) Using the inner product $\langle X, Y \rangle := \operatorname{tr}(X^\top Y)$ in $M_{n\t...

Profile: Techniques: Implicit Function Theorem, Tangent Space Computation, Invariant Metric Construction
Proof move: Apply Implicit Function Theorem -> Compute differential of constraint -> Identify tangent space -> Use invariance property -> Construct metric invariant under orthogonal action
Key insight: The constraint $A^\top A = I_k$ defines a submanifold via the Implicit Function Theorem.
Also known as: Normal Form Reduction, Constraint Manifold Analysis, Symmetry Preserving Metric Construction

Copied words: action, construct, invariance, invariant, metric, submanifold

**doc `harvard-quals___2024___S24.13`** (55 words)

> Show that the orthogonal group \[ O(n)=\{A\in M(n,\mathbf{R})\mid A^T A=\mathrm{id}\} \] for integer $n>1$ is a smooth manifold, where $M(n,\mathbf{R})$ consists of $n$ by $n$ matrices with entries in $\mathbf{R}$. (Hint: use the implicit function theorem.)  Syllabus topics: smooth manifold, implicit function theorem.

Profile: Techniques: Implicit Function Theorem, Jacobian Matrix, Tangent Space Mapping

Proof move: Define a smooth map -> Compute its Jacobian -> Show the Jacobian is surjective -> Apply Implicit Function Theorem

Key insight: For any symmetric matrix, there exists a corresponding tangent vector that maps to it under the Jacobian.

Also known as: Linearization, Local Invertibility, Smoothness via Derivatives

Copied words: function, implicit, smooth, theorem

**doc `harvard-quals___2015___S15.3`** (36 words)

> Let \[ M = \{(x,y,z)\in \mathbb{R}^3 \mid x^2 - y^2 - z^3 - z = 0\}. \]  (a) Prove that $M$ is a smooth surface in $\mathbb{R}^3$.  (b) For what values of $c\in \mathbb{R}$ does the plane $z=c$ intersect $M$ transversely?

Profile: Techniques: Implicit Function Theorem, Transversality
Proof move: Define function -> Apply Implicit Function Theorem -> Check transversality condition
Key insight: The gradient of the defining function is never zero.
Also known as: Regular Value Theorem, Smooth Submanifold Intersection

Copied words: smooth

**doc `harvard-quals___2020___S20.6`** (51 words)

> (DG)  Let $f:\mathbb{R}^3\to \mathbb{R}$ be defined by $f(x,y,z)=x^2+y^2-1$.  (i) Prove that $M=f^{-1}(0)$ is a two-dimensional embedded submanifold of $\mathbb{R}^3$.  (ii) For $a,b,c\in \mathbb{R}$, consider the vector field \[ X=a\frac{\partial}{\partial x}+b\frac{\partial}{\partial y}+c\frac{\partial}{\partial z}. \] For which values of $a,b,c$ is $X$ tangent to $M$ at the point $(1,0,1)$? 

Profile: Techniques: Implicit Function Theorem, Tangency Condition

Proof move: Apply Implicit Function Theorem -> Check rank condition -> Verify tangent vector condition -> Solve for coefficients

Key insight: A vector field is tangent to a level set if its directional derivative along the level set vanishes.

Also known as: Level Set Tangency, Vanishing Directional Derivative

Copied words: field, tangent, vector
