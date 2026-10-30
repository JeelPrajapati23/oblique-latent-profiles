# Prompt hand-test: math

- Variant: `math-ee895b__Qwen2.5-7B-Instruct-AWQ` (prompts: doc=`math_problem`, query=`math_problem`)
- Model: `Qwen/Qwen2.5-7B-Instruct-AWQ`, greedy decoding
- Words per profile: min 39, median 55, max 74 (target 60-120); in range: 8/20
- Format compliant (4 fields): 20/20
- Profiles containing formula symbols ($ \ ^ _ { } =): 9/20
- Profiles with copied content words: 15/20

| Cosine (Qwen3-0.6B) | same group | different group | gap |
|---|---|---|---|
| raw text | 0.468 | 0.342 | +0.127 |
| profile | 0.659 | 0.529 | +0.130 |

A bigger gap means profiles separate the hidden property better than raw text does.

## Group 1

**query `q00740`** (57 words)

> Evaluate \[ \int_0^1 \frac{\log\bigl(\cos(\pi x/2)\bigr)}{x(1+x)}\,dx. \]

Profile: Techniques: Substitution, Integration by Parts, Series Expansion
Proof move: Recognize the integral as a form of Frullani's integral -> Identify the logarithmic function's properties -> Expand the series and integrate term by term
Key insight: The integral can be transformed into a product of two simpler functions through a clever substitution.
Also known as: Logarithmic Differentiation, Functional Equation Solution

Copied words: -

**doc `american-math-monthly___2019___12012`** (74 words)

> Let $k$ be a nonnegative integer. Find the set of real numbers $x$ for which the power series \[ \sum_{n=k}^{\infty}\binom{n}{k}\left(e-1-\frac{1}{1!}-\frac{1}{2!}-\cdots-\frac{1}{n!}\right)x^n \] converges, and determine the sum.

Profile: Techniques: Binomial Coefficient Simplification, Series Comparison, Exponential Series Recognition
Proof move: Identify the exponential series, compare with known series, simplify using binomial theorem -> Recognize the series as a shifted version of the exponential function's Taylor series -> Apply the ratio test for convergence
Key insight: The series can be simplified to a form involving \(e^x\), leveraging the properties of the exponential function.
Also known as: Exponential Function Identification, Ratio Test Application, Binomial Expansion Recognition

Copied words: series

**doc `american-math-monthly___2004___10977`** (73 words)

> Let $\beta$ and $t$ be real numbers with $t>0$. Let $\operatorname{erf}(x)=\frac{2}{\sqrt{\pi}}\int_0^x e^{-u^2}\,du$, let $\gamma(x,y)=\int_0^y u^{x-1}e^{-u}\,du$, and let $\Gamma(x)=\int_0^{\infty} u^{x-1}e^{-u}\,du$. Show that \[ \sum_{n=0}^{\infty}\left(\frac{\beta^2}{1+\beta^2}\right)^n\frac{\gamma\left(n+\tfrac12,(1+\beta^2)t\right)}{\Gamma\left(n+\tfrac12\right)} =(1+\beta^2)\operatorname{e...

Profile: Techniques: Series Expansion, Integral Transformation, Gamma Function Properties
Proof move: Recognize the series as a power series expansion -> Identify the integral as a form of the Gamma function -> Use the definition of the error function to simplify
Key insight: The series and integrals can be linked through the properties of the error function and the Gamma function.
Also known as: Euler's Formula for Power Series, Reduction to Fundamental Integral Forms, Error Function Representation

Copied words: gamma

**doc `american-math-monthly___1999___10575`** (70 words)

> Prove that \[ \sum_{\ell=0}^n (-1)^\ell\binom{n}{\ell}(2\ell)!\sum_{m=0}^{2\ell}\frac{(-1)^m}{m!} = \sum_{\ell=0}^n (-1)^\ell\binom{n}{\ell}2^{\,n-\ell}(n+\ell)! \] for every nonnegative integer $n$.

Profile: Techniques: Binomial Theorem, Exponential Generating Functions, Inclusion-Exclusion Principle

Proof move: Apply the Binomial Theorem to expand the binomial term, then transform each side using Exponential Generating Functions to simplify the sums, -> identify a common exponential form, -> recognize the Inclusion-Exclusion Principle in the alternating series.

Key insight: The alternating series can be seen as a combinatorial inclusion-exclusion process.

Also known as: Principle of Inclusion-Exclusion, Exponential Series Transformation

Copied words: -

## Group 2

**query `q01528`** (69 words)

> Prove \[ \sum_{n=1}^{\infty}\frac{2^{2n-1}}{2n+1}\left(\frac{(n-1)!}{(2n-1)!!}\right)^2=\pi-2, \] where $(2n-1)!!$ is defined as usual to be $\prod_{k=1}^n(2k-1)$.

Profile: Techniques: Series manipulation, factorial simplification, double factorial properties
Proof move: Recognize the series as a telescoping series -> Simplify the general term using factorial and double factorial -> Identify the telescoping nature by canceling intermediate terms -> Realize the remaining terms sum to $\pi-2$
Key insight: The series can be simplified to a form that telescopes, leaving only boundary terms.
Also known as: Telescoping series recognition, factorial reduction, double factorial cancellation

Copied words: -

**doc `american-math-monthly___2025___12396`** (54 words)

> Let $F_n$ be the $n$th Fibonacci number, where $F_0=0$, $F_1=1$, and $F_n=F_{n-1}+F_{n-2}$ when $n\ge 2$. Prove \[ \sum_{n=1}^{\infty}\arctan\left(\frac{1}{3F_n^2}\right)=\frac{\pi}{4}. \]

Profile: Techniques: Series Transformation, Trigonometric Identity Application
Proof move: Recognize the series as a telescoping series -> Apply the tangent addition formula -> Notice the pattern simplifies to a constant difference
Key insight: Each term's arctangent can be expressed as a difference of two arctangents, leading to cancellation.
Also known as: Arctangent Telescoping, Angle Addition Formula Insight

Copied words: -

**doc `american-math-monthly___2008___11260`** (71 words)

> Find those nonnegative values of $\alpha$ and $\beta$ for which \[ \sum_{n=1}^{\infty}\prod_{k=1}^{n}\frac{\alpha+k\log k}{\beta+(k+1)\log(k+1)} \] converges. For those values of $\alpha$ and $\beta$, evaluate the sum.

Profile: Techniques: Comparison Test, Logarithmic Growth Analysis, Asymptotic Behavior

Proof move: Identify the dominant terms in the product -> Compare each term to a simpler divergent or convergent series -> Determine the conditions on $\alpha$ and $\beta$ for convergence -> Evaluate the sum using known series results

Key insight: The product's behavior is dominated by the logarithmic terms, leading to a harmonic-like series.

Also known as: Limit Comparison, Logarithmic Series Analysis, Harmonic Series Analogy

Copied words: alpha, beta, evaluate

**doc `american-math-monthly___2011___11515`** (48 words)

> Find a closed-form expression for \[ \sum_{n=1}^{\infty}4^n\sin^4\bigl(2^{-n}\theta\bigr). \]

Profile: Techniques: Trigonometric Identity, Series Transformation
Proof move: Recognize a trig identity -> Simplify the sine term -> Transform the series into a telescoping form -> Sum the series
Key insight: The sine term can be expressed as a polynomial in sine, facilitating series simplification.
Also known as: Angle Reduction, Polynomial Approximation

Copied words: form

## Group 3

**query `q00408`** (51 words)

> Let $X_1=1$, and for $m\ge 1$ let \[ X_{m+1}=(m+3/2)^{-1}\sum_{k=1}^{m}X_kX_{m+1-k}. \] Evaluate $\lim_{m\to\infty}X_m/X_{m+1}$.

Profile: Techniques: Recurrence relation, Limit analysis, Symmetry in sequences

Proof move: Identify a stable ratio,-> apply limit to both sides,-> recognize telescoping pattern,-> exploit symmetry in recursive definition

Key insight: The ratio $X_m/X_{m+1}$ stabilizes as $m$ increases.

Also known as: Fixed point iteration, Asymptotic behavior analysis, Recursive equilibrium

Copied words: -

**doc `american-math-monthly___2025___12418`** (59 words)

> Let $\Phi$ be the cumulative distribution function of a standard normal random variable, defined by \[ \Phi(x)=\frac{1}{\sqrt{2\pi}}\int_{-\infty}^x e^{-t^2/2}\,dt. \] (a) For positive real numbers $\sigma_1,\dots,\sigma_n$ and $w_1,\dots,w_n$ with $\sum_{i=1}^n w_i=1$, determine \[ \lim_{x\to\infty}\frac{1}{x}\,\Phi^{-1}\left(\sum_{i=1}^n w_i\Phi\left(\frac{x}{\sigma_i}\right)\right). \] (b) Let ...

Profile: Techniques: Change of Variables, Asymptotic Analysis, Taylor Expansion

Proof move: Identify the dominant term -> Apply change of variables -> Use asymptotic properties of the inverse normal -> Apply Taylor expansion to the remainder

Key insight: The behavior of the inverse function near its limit can be approximated by its derivative.

Also known as: Leading Order Term Analysis, Local Linearization, Asymptotic Scaling

Copied words: function, limit, normal

**doc `harvard-quals___2014___S14.II.3`** (64 words)

> Suppose that $f$ is holomorphic in an open set containing the closed unit disk $\{|z|\le 1\}$ in $\mathbb{C}$, except for a pole at $z_0$ on the unit circle $\{|z|=1\}$. Show that if \[ \sum_{n=0}^{\infty} a_n z^n \] denote the power series expansion of $f$ in the open unit disk $\{|z|<1\}$, then \[ \lim_{n\to\infty}\frac{a_n}{a_{n+1}}=z_0. \]

Profile: Techniques: Residue theorem, Laurent series expansion, asymptotic analysis
Proof move: Apply residue theorem to the annulus -> Expand $f$ in Laurent series -> Compare coefficients of $z^n$ and $z^{n+1}$ -> Use asymptotic behavior of coefficients
Key insight: The ratio of successive coefficients captures the location of the pole.
Also known as: Ratio test for series convergence, coefficient comparison in complex analysis, residue-based asymptotics

Copied words: expansion, pole, series

**doc `american-math-monthly___2025___12392`** (71 words)

> For which positive integers $a$ is there a nonzero polynomial $P(x,y)\in\mathbb{C}[x,y]$ such that \[ P\left(\binom{2n}{n},\binom{an}{n}\right)=0 \] for all nonnegative integers $n$?

Profile: Techniques: Polynomial Identity, Degree Analysis, Symmetry Argument

Proof move: Assume $P(x,y)$ exists, then "->" consider the degrees of $x$ and $y" ->" deduce the ratio of degrees must be rational" ->" conclude the ratio must be an integer due to symmetry.

Key insight: The polynomial must have a degree ratio that aligns with the combinatorial growth rates of binomial coefficients.

Also known as: Rational Degree Ratio, Integer Degree Proportion, Combinatorial Symmetry Argument

Copied words: polynomial

## Group 4

**query `q01165`** (50 words)

> Let $A_0,B_0$, and $C_0$ be noncollinear points in the plane. Let $p$ be a line that meets lines $B_0C_0$, $C_0A_0$, and $A_0B_0$ at $A^*$, $B^*$, and $C^*$ respectively. For $n\ge1$, let $A_n$ be the intersection of $B^*B_{n-1}$ with $C^*C_{n-1}$, and define $B_n$ and $C_n$ similarly. Show that all three sequences converge, and describe their respective limits.

Profile: Techniques: Homothety, Invariant Points, Asymptotic Behavior

Proof move: Identify homothety -> Recognize invariant points -> Analyze asymptotic behavior of sequences

Key insight: The sequences converge to the intersection of the lines through the original points and their respective opposite sides.

Also known as: Fixed Point Analysis, Convergence to Invariant Elements, Asymptotic Homothety

Copied words: converge, intersection, lines, points, respective, sequences

**doc `harvard-quals___2024___F24.3`** (49 words)

> Suppose $R_1,R_2$ are bounded, simply-connected open subsets of $\mathbb C$. Let $z_1\in R_1$ and $z_2\in R_2$.  i) Prove that there is a holomorphic bijective function $f:R_1\to R_2$ such that $f(z_1)=z_2$.  ii) Suppose that $g:R_1\to R_2$ is a holomorphic function such that $g(z_1)=z_2$. Prove that $|g'(z_1)|\le |f'(z_1)|$.

Profile: Techniques: Riemann Mapping Theorem, Schwarz-Pick Lemma
Proof move: Apply Riemann mapping theorem -> Map to unit disk -> Use Schwarz-Pick to compare derivatives
Key insight: The derivative's magnitude is bounded by the distance between images under the optimal map.
Also known as: Optimal conformal equivalence, Best possible distortion bound

Copied words: bounded

**doc `berkeley-quals___1990___F6.1.6`** (43 words)

> Does the set $G=\{a\in\mathbb{R}\mid a>0,\ a\neq 1\}$ form a group with the operation $a*b=a^{\log b}$?

Profile: Techniques: Invariance, Identity Element, Closure

Proof move: Define operation -> Check closure -> Identify potential identity -> Verify identity properties -> Check inverses

Key insight: The operation must preserve the set's structure, ensuring all results are within $G$.

Also known as: Fixed Point, Homomorphism Preservation, Structural Consistency

Copied words: operation

**doc `american-math-monthly___1998___10554`** (42 words)

> Suppose that the functions $f(r)$ and $g(r)$ are positive and continuous for $0\le r<1$. Using polar coordinates $(r,\theta)$, define a metric on the open unit disk by \[ ds^2=f(r)^2\,dr^2+g(r)^2 r^2\,d\theta^2. \] For what choices of $f(r)$ and $g(r)$ does the open unit disk with this metric furnish a model of the hyperbolic plane?

Profile: Techniques: Change of Variables, Differential Geometry, Metric Tensor Analysis
Proof move: Identify invariant property -> Compare to known metric -> Solve for functions
Key insight: The metric must be conformally equivalent to the Poincaré disk model.
Also known as: Conformal Mapping, Hyperbolic Geometry Equivalence

Copied words: disk, functions, hyperbolic, metric, model

## Group 5

**query `q03053`** (62 words)

> Let $V_k(\mathbb{R}^n) = \{A \in M_{n\times k}(\mathbb{R}) \mid A^\top A = I_k\}$.  (a) Show that $V_k(\mathbb{R}^n)$ is a smooth submanifold of $M_{n\times k}(\mathbb{R})$ and compute its dimension.  (b) Show that $T_A V_k(\mathbb{R}^n) = \{X \in M_{n\times k}(\mathbb{R}) \mid A^\top X + X^\top A = 0\}$.  (c) Using the inner product $\langle X, Y \rangle := \operatorname{tr}(X^\top Y)$ in $M_{n\t...

Profile: Techniques: Implicit Function Theorem, Tangent Space Computation, Invariant Metric Construction
Proof move: Apply Implicit Function Theorem -> Compute differential of constraint -> Identify tangent space -> Use invariance property -> Construct metric invariant under orthogonal action
Key insight: The constraint $A^\top A = I_k$ defines a submanifold via the Implicit Function Theorem.
Also known as: Normal Form Reduction, Constraint Manifold Analysis, Symmetry Preserving Metric Construction

Copied words: action, construct, invariance, invariant, metric, submanifold

**doc `harvard-quals___2024___S24.13`** (39 words)

> Show that the orthogonal group \[ O(n)=\{A\in M(n,\mathbf{R})\mid A^T A=\mathrm{id}\} \] for integer $n>1$ is a smooth manifold, where $M(n,\mathbf{R})$ consists of $n$ by $n$ matrices with entries in $\mathbf{R}$. (Hint: use the implicit function theorem.)  Syllabus topics: smooth manifold, implicit function theorem.

Profile: Techniques: Implicit function theorem, differential map, manifold structure
Proof move: Define smooth map -> Compute Jacobian -> Apply implicit function theorem -> Conclude manifold
Key insight: The Jacobian's full rank ensures local diffeomorphism.
Also known as: Jacobian rank condition, local invertibility criterion

Copied words: function, implicit, manifold, smooth, theorem

**doc `harvard-quals___2015___S15.3`** (43 words)

> Let \[ M = \{(x,y,z)\in \mathbb{R}^3 \mid x^2 - y^2 - z^3 - z = 0\}. \]  (a) Prove that $M$ is a smooth surface in $\mathbb{R}^3$.  (b) For what values of $c\in \mathbb{R}$ does the plane $z=c$ intersect $M$ transversely?

Profile: Techniques: Implicit Function Theorem, Transversality
Proof move: Apply Implicit Function Theorem -> Check Jacobian rank -> Analyze plane intersection -> Ensure transversality condition
Key insight: The gradient of the defining function is never zero on $M$.
Also known as: Regular Value Theorem, Non-zero Derivative Condition

Copied words: plane

**doc `harvard-quals___2020___S20.6`** (49 words)

> (DG)  Let $f:\mathbb{R}^3\to \mathbb{R}$ be defined by $f(x,y,z)=x^2+y^2-1$.  (i) Prove that $M=f^{-1}(0)$ is a two-dimensional embedded submanifold of $\mathbb{R}^3$.  (ii) For $a,b,c\in \mathbb{R}$, consider the vector field \[ X=a\frac{\partial}{\partial x}+b\frac{\partial}{\partial y}+c\frac{\partial}{\partial z}. \] For which values of $a,b,c$ is $X$ tangent to $M$ at the point $(1,0,1)$? 

Profile: Techniques: Implicit Function Theorem, Tangency Condition

Proof move: Apply Implicit Function Theorem -> Check Jacobian rank -> Evaluate vector field components -> Compare with normal vector

Key insight: The vector field is tangent to the manifold if it aligns with the manifold's normal.

Also known as: Regular Value Argument, Normal Vector Comparison

Copied words: field, tangent, vector
