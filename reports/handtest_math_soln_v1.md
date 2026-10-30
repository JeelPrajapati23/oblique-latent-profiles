# Prompt hand-test: math_soln

- Variant: `math_soln-095689__Qwen2.5-7B-Instruct-AWQ` (prompts: doc=`math_problem_solution`, query=`math_problem`)
- Model: `Qwen/Qwen2.5-7B-Instruct-AWQ`, greedy decoding
- Words per profile: min 26, median 36, max 53 (target 60-120); in range: 0/20
- Format compliant (3 fields): 20/20
- Profiles with copied content words: 13/20

| Cosine (Qwen3-0.6B) | same group | different group | gap |
|---|---|---|---|
| raw text | 0.468 | 0.342 | +0.127 |
| profile | 0.683 | 0.533 | +0.150 |

A bigger gap means profiles separate the hidden property better than raw text does.

## Group 1

**query `q00740`** (45 words)

> Evaluate \[ \int_0^1 \frac{\log\bigl(\cos(\pi x/2)\bigr)}{x(1+x)}\,dx. \]

Profile: Techniques: substitution, series expansion, symmetry

Proof move: assume an integral form -> expand logarithm and cosine -> identify symmetric terms -> simplify using symmetry -> recognize telescoping series

Key insight: The integrand can be decomposed into symmetric components that cancel out, leaving a telescoping series.

Copied words: -

**doc `american-math-monthly___2019___12012`** (36 words)

> Let $k$ be a nonnegative integer. Find the set of real numbers $x$ for which the power series \[ \sum_{n=k}^{\infty}\binom{n}{k}\left(e-1-\frac{1}{1!}-\frac{1}{2!}-\cdots-\frac{1}{n!}\right)x^n \] converges, and determine the sum.

Profile: Techniques: bounding, integral representation, series manipulation
Proof move: assume a series form -> integral representation -> bounding -> simplification -> case distinction
Key insight: transforming the series into an integral form allows for bounding and simplification.

Copied words: series

**doc `american-math-monthly___2004___10977`** (50 words)

> Let $\beta$ and $t$ be real numbers with $t>0$. Let $\operatorname{erf}(x)=\frac{2}{\sqrt{\pi}}\int_0^x e^{-u^2}\,du$, let $\gamma(x,y)=\int_0^y u^{x-1}e^{-u}\,du$, and let $\Gamma(x)=\int_0^{\infty} u^{x-1}e^{-u}\,du$. Show that \[ \sum_{n=0}^{\infty}\left(\frac{\beta^2}{1+\beta^2}\right)^n\frac{\gamma\left(n+\tfrac12,(1+\beta^2)t\right)}{\Gamma\left(n+\tfrac12\right)} =(1+\beta^2)\operatorname{e...

Profile: Techniques: Laplace transform, integral properties, series manipulation

Proof move: assume the Laplace transform -> apply properties (3), (4), (5) -> simplify expressions -> recognize geometric series

Key insight: transforming the integral and series into a common form allows leveraging the properties of the Laplace transform to equate the two sides.

Copied words: -

**doc `american-math-monthly___1999___10575`** (36 words)

> Prove that \[ \sum_{\ell=0}^n (-1)^\ell\binom{n}{\ell}(2\ell)!\sum_{m=0}^{2\ell}\frac{(-1)^m}{m!} = \sum_{\ell=0}^n (-1)^\ell\binom{n}{\ell}2^{\,n-\ell}(n+\ell)! \] for every nonnegative integer $n$.

Profile: Techniques: umbral calculus, operator algebra, integral representation

Proof move: define operators -> apply binomial theorem -> simplify using commutativity -> evaluate at zero

Key insight: transforming the sum into operator algebra allows simplification through algebraic identities.

Copied words: -

## Group 2

**query `q01528`** (32 words)

> Prove \[ \sum_{n=1}^{\infty}\frac{2^{2n-1}}{2n+1}\left(\frac{(n-1)!}{(2n-1)!!}\right)^2=\pi-2, \] where $(2n-1)!!$ is defined as usual to be $\prod_{k=1}^n(2k-1)$.

Profile: Techniques: telescoping, series manipulation
Proof move: identify a telescoping pattern -> simplify infinite series -> match target expression
Key insight: Each term can be expressed as a difference of two other terms.

Copied words: -

**doc `american-math-monthly___2025___12396`** (43 words)

> Let $F_n$ be the $n$th Fibonacci number, where $F_0=0$, $F_1=1$, and $F_n=F_{n-1}+F_{n-2}$ when $n\ge 2$. Prove \[ \sum_{n=1}^{\infty}\arctan\left(\frac{1}{3F_n^2}\right)=\frac{\pi}{4}. \]

Profile: Techniques: telescoping, identity manipulation
Proof move: assume an appropriate form for $G_n$ -> verify it satisfies the given identity -> use telescoping to simplify the sum
Key insight: the chosen $G_n$ allows the sum to telescope, revealing the telescoping nature of the series.

Copied words: -

**doc `american-math-monthly___2008___11260`** (26 words)

> Find those nonnegative values of $\alpha$ and $\beta$ for which \[ \sum_{n=1}^{\infty}\prod_{k=1}^{n}\frac{\alpha+k\log k}{\beta+(k+1)\log(k+1)} \] converges. For those values of $\alpha$ and $\beta$, evaluate the sum.

Profile: Techniques: extremal principle, telescoping

Proof move: assume $\beta>\alpha\ge 0$ -> manipulate product -> telescoping sum -> evaluate limit

Key insight: the infinite product telescopes to zero.

Copied words: alpha, beta, evaluate

**doc `american-math-monthly___2011___11515`** (30 words)

> Find a closed-form expression for \[ \sum_{n=1}^{\infty}4^n\sin^4\bigl(2^{-n}\theta\bigr). \]

Profile: Techniques: telescoping series, limit evaluation

Proof move: assume a series form -> express in telescoping terms -> evaluate limits -> simplify

Key insight: consecutive terms cancel, leaving only boundary values.

Copied words: form

## Group 3

**query `q00408`** (36 words)

> Let $X_1=1$, and for $m\ge 1$ let \[ X_{m+1}=(m+3/2)^{-1}\sum_{k=1}^{m}X_kX_{m+1-k}. \] Evaluate $\lim_{m\to\infty}X_m/X_{m+1}$.

Profile: Techniques: induction on m, telescoping
Proof move: assume a limit exists -> apply induction step -> simplify using telescoping sum -> find a constant ratio
Key insight: the ratio between consecutive terms stabilizes as m grows.

Copied words: -

**doc `american-math-monthly___2025___12418`** (36 words)

> Let $\Phi$ be the cumulative distribution function of a standard normal random variable, defined by \[ \Phi(x)=\frac{1}{\sqrt{2\pi}}\int_{-\infty}^x e^{-t^2/2}\,dt. \] (a) For positive real numbers $\sigma_1,\dots,\sigma_n$ and $w_1,\dots,w_n$ with $\sum_{i=1}^n w_i=1$, determine \[ \lim_{x\to\infty}\frac{1}{x}\,\Phi^{-1}\left(\sum_{i=1}^n w_i\Phi\left(\frac{x}{\sigma_i}\right)\right). \] (b) Let ...

Profile: Techniques: asymptotic analysis, limit manipulation, infinitesimal substitution

Proof move: assume an infinitesimal difference -> asymptotic equivalence -> limit convergence

Key insight: the ratio of differences in the CDFs approaches a constant as the argument grows large.

Copied words: limit

**doc `harvard-quals___2014___S14.II.3`** (35 words)

> Suppose that $f$ is holomorphic in an open set containing the closed unit disk $\{|z|\le 1\}$ in $\mathbb{C}$, except for a pole at $z_0$ on the unit circle $\{|z|=1\}$. Show that if \[ \sum_{n=0}^{\infty} a_n z^n \] denote the power series expansion of $f$ in the open unit disk $\{|z|<1\}$, then \[ \lim_{n\to\infty}\frac{a_n}{a_{n+1}}=z_0. \]

Profile: Techniques: Dominant term analysis, binomial expansion, limit manipulation

Proof move: Identify dominant term -> cancel common factors -> take limit

Key insight: The limit of ratios of coefficients is determined by the dominant term's behavior.

Copied words: expansion

**doc `american-math-monthly___2025___12392`** (42 words)

> For which positive integers $a$ is there a nonzero polynomial $P(x,y)\in\mathbb{C}[x,y]$ such that \[ P\left(\binom{2n}{n},\binom{an}{n}\right)=0 \] for all nonnegative integers $n$?

Profile: Techniques: injective function, asymptotic analysis, logarithmic properties

Proof move: assume $2\le a<b$ -> show $f(s,t)$ is injective -> derive contradiction -> conclude $a=1$ or $b=1$ or $a=b$

Key insight: the ratio $(a-1)\log(a-1)/(a\log a)$ is strictly increasing for $a>2$, leading to a contradiction.

Copied words: -

## Group 4

**query `q01165`** (42 words)

> Let $A_0,B_0$, and $C_0$ be noncollinear points in the plane. Let $p$ be a line that meets lines $B_0C_0$, $C_0A_0$, and $A_0B_0$ at $A^*$, $B^*$, and $C^*$ respectively. For $n\ge1$, let $A_n$ be the intersection of $B^*B_{n-1}$ with $C^*C_{n-1}$, and define $B_n$ and $C_n$ similarly. Show that all three sequences converge, and describe their respective limits.

Profile: Techniques: extremal principle, induction on n, proof by contradiction

Proof move: assume an extremal object -> induction step -> contradiction

Key insight: The sequences of points are constrained to converge due to the finite plane area and the nature of line intersections.

Copied words: converge, line, plane, points, sequences

**doc `harvard-quals___2024___F24.3`** (36 words)

> Suppose $R_1,R_2$ are bounded, simply-connected open subsets of $\mathbb C$. Let $z_1\in R_1$ and $z_2\in R_2$.  i) Prove that there is a holomorphic bijective function $f:R_1\to R_2$ such that $f(z_1)=z_2$.  ii) Suppose that $g:R_1\to R_2$ is a holomorphic function such that $g(z_1)=z_2$. Prove that $|g'(z_1)|\le |f'(z_1)|$.

Profile: Techniques: Riemann mapping theorem, Cauchy's integral formula, chain rule

Proof move: assume holomorphic bijections -> map to unit disc -> apply Cauchy's formula -> derive inequality

Key insight: derivative magnitudes relate through composition and inverse mappings

Copied words: holomorphic

**doc `berkeley-quals___1990___F6.1.6`** (30 words)

> Does the set $G=\{a\in\mathbb{R}\mid a>0,\ a\neq 1\}$ form a group with the operation $a*b=a^{\log b}$?

Profile: Techniques: bijection, transformation

Proof move: map operation -> equivalent operation -> known group -> original group

Key insight: Relating the original operation to a simpler, known group through a bijection.

Copied words: group, operation

**doc `american-math-monthly___1998___10554`** (53 words)

> Suppose that the functions $f(r)$ and $g(r)$ are positive and continuous for $0\le r<1$. Using polar coordinates $(r,\theta)$, define a metric on the open unit disk by \[ ds^2=f(r)^2\,dr^2+g(r)^2 r^2\,d\theta^2. \] For what choices of $f(r)$ and $g(r)$ does the open unit disk with this metric furnish a model of the hyperbolic plane?

Profile: Techniques: invariant, bijection, change of variables
Proof move: assume hyperbolic plane model -> invariant under rotations and reflections -> geodesics through origin -> infinite length -> integral condition -> match hyperbolic circle circumference -> satisfy stated conditions
Key insight: transform metric to match Poincaré disc model through bijective correspondence and change of variables

Copied words: hyperbolic, metric, model, plane

## Group 5

**query `q03053`** (53 words)

> Let $V_k(\mathbb{R}^n) = \{A \in M_{n\times k}(\mathbb{R}) \mid A^\top A = I_k\}$.  (a) Show that $V_k(\mathbb{R}^n)$ is a smooth submanifold of $M_{n\times k}(\mathbb{R})$ and compute its dimension.  (b) Show that $T_A V_k(\mathbb{R}^n) = \{X \in M_{n\times k}(\mathbb{R}) \mid A^\top X + X^\top A = 0\}$.  (c) Using the inner product $\langle X, Y \rangle := \operatorname{tr}(X^\top Y)$ in $M_{n\t...

Profile: Techniques: Implicit function theorem, tangent space computation, invariant metric construction
Proof move: assume an extremal object -> apply implicit function theorem -> compute tangent space -> verify invariance under orthogonal action
Key insight: The structure of the constraint $A^\top A = I_k$ dictates the tangent space and allows for an invariant metric construction.

Copied words: action, invariance, invariant, metric, verify

**doc `harvard-quals___2024___S24.13`** (42 words)

> Show that the orthogonal group \[ O(n)=\{A\in M(n,\mathbf{R})\mid A^T A=\mathrm{id}\} \] for integer $n>1$ is a smooth manifold, where $M(n,\mathbf{R})$ consists of $n$ by $n$ matrices with entries in $\mathbf{R}$. (Hint: use the implicit function theorem.)  Syllabus topics: smooth manifold, implicit function theorem.

Profile: Techniques: implicit function theorem, tangent space identification, Jacobian computation

Proof move: assume $F^{-1}(\mathrm{id})$ -> compute Jacobian -> show subjective -> apply implicit function theorem

Key insight: for any symmetric matrix, there exists a tangent vector that maps to it through the Jacobian.

Copied words: function, implicit, mathrm, theorem

**doc `harvard-quals___2015___S15.3`** (36 words)

> Let \[ M = \{(x,y,z)\in \mathbb{R}^3 \mid x^2 - y^2 - z^3 - z = 0\}. \]  (a) Prove that $M$ is a smooth surface in $\mathbb{R}^3$.  (b) For what values of $c\in \mathbb{R}$ does the plane $z=c$ intersect $M$ transversely?

Profile: Techniques: Implicit function theorem, transversality
Proof move: Apply implicit function theorem -> check transversality condition -> conclude smooth surface -> analyze plane intersection -> find critical $c$ values
Key insight: Local behavior determines global intersection properties.

Copied words: plane, smooth, surface

**doc `harvard-quals___2020___S20.6`** (29 words)

> (DG)  Let $f:\mathbb{R}^3\to \mathbb{R}$ be defined by $f(x,y,z)=x^2+y^2-1$.  (i) Prove that $M=f^{-1}(0)$ is a two-dimensional embedded submanifold of $\mathbb{R}^3$.  (ii) For $a,b,c\in \mathbb{R}$, consider the vector field \[ X=a\frac{\partial}{\partial x}+b\frac{\partial}{\partial y}+c\frac{\partial}{\partial z}. \] For which values of $a,b,c$ is $X$ tangent to $M$ at the point $(1,0,1)$? 

Profile: Techniques: Implicit function theorem, tangent space computation
Proof move: Assume vector field $X$ tangent -> Evaluate $X(f)$ at $(1,0,1)$ -> Conclude $a=0$
Key insight: Vanishing directional derivative implies tangency.

Copied words: field, tangent, vector
