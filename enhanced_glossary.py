"""
Enhanced glossary with Z3/SMT concepts and improved mathematical definitions
"""

from typing import Dict, List

def get_enhanced_glossary() -> List[Dict[str, str]]:
    """Get enhanced glossary with Z3/SMT and quotient set concepts"""
    return [
        # Original mathematical concepts (improved)
        {
            "term": "Cartesian Product of two sets X and Y",
            "definition": "It is the set X × Y formed by the pairs (a, b) where a ∈ X and b ∈ Y (such pairs are ordered, in the sense that (a, b) is not the same pair as (b, a) even if X and Y coincide). We can, for example, realize that the set of suits is the Cartesian product of the set of jackets and the set of trousers. The Cartesian product can be generalised to more than two sets: if we have a third set Z, the Cartesian product X × Y × Z is the set of triples (a, b, c) where a ∈ X, b ∈ Y and c ∈ Z. Even more generally, if n ≥ 2 sets X₁, …, Xₙ are given, their Cartesian product X₁ × ··· × Xₙ is the set of n-tuples (a₁, …, aₙ) where aᵢ ∈ Xᵢ."
        },
        {
            "term": "Cartesian Power of a set X",
            "definition": "It is an iterated Cartesian product of X with itself. Thus X² is X × X, X³ is X × X × X, etc. For the sake of completeness we define X¹ as X itself, while X⁰ is taken to be equal to the singleton set {∗} which has ∗ as its unique element (the choice of denoting such a unique element by ∗ is purely conventional)."
        },
        {
            "term": "Characteristic Function (of a subset S of a set X)",
            "definition": "It is the function χ_S : X → 2 which associates with a ∈ X the value 1 if a ∈ S and the value 0 otherwise. Here 2 = {0,1} is the set with two elements, called the set of truth-values or the set of Booleans. It is easily seen that every function χ : X → 2 is of the type χ_S for a (unique) S ⊆ X. Thus all subsets can be uniquely specified via their characteristic function. This is precisely what happens in the SMT-LIB2 standard where predicates and relations are seen as functions with values in Bool."
        },
        {
            "term": "Composition (of two functions)",
            "definition": "Given two functions f : X → Y and g : Y → Z (note that the codomain of f is equal to the domain of g), their composition is the function g ∘ f : X → Z which is obtained by executing first f and then g, i.e. (g ∘ f)(a) = g(f(a))."
        },
        {
            "term": "Countable",
            "definition": "A set X is said to be countable when there exists a bijective function f : N → X. For example, Z, Q and N are countable; by contrast, R is not. If X is finite or countable, the set of lists of elements of X is itself countable."
        },
        {
            "term": "Equivalence Relation",
            "definition": "It is a binary relation E on X that is reflexive, symmetric and transitive: (r) ∀a ∈ X  E(a,a); (s) ∀a,b ∈ X  (E(a,b) → E(b,a)); (t) ∀a,b,c ∈ X  (E(a,b) ∧ E(b,c) → E(a,c)). Examples include 'speaking the same language'."
        },
        {
            "term": "Function (Bijective)",
            "definition": "A function f : X → Y is bijective when it is both injective and surjective. This holds iff there exists an inverse function g : Y → X such that g(f(a)) = a and f(g(b)) = b for all a ∈ X and b ∈ Y."
        },
        {
            "term": "Function (Injective)",
            "definition": "A function f : X → Y is injective when distinct elements of the domain map to distinct elements of the codomain. Formally: ∀a₁,a₂ ∈ X  (f(a₁) = f(a₂) → a₁ = a₂)."
        },
        {
            "term": "Function (Surjective)",
            "definition": "A function f : X → Y is surjective when every b ∈ Y lies in the image of f, i.e. ∀b ∈ Y ∃a ∈ X  f(a) = b."
        },
        {
            "term": "Graph",
            "definition": "A set X endowed with a binary relation R. When R is symmetric, the graph is undirected; otherwise, directed. Elements of X are vertices, and pairs (a,b) ∈ R are edges."
        },
        {
            "term": "Lexicographic Ordering",
            "definition": "Given strict orders (P₁,<₁), (P₂,<₂), …, (Pₙ,<ₙ), define an order <ₗₑₓ on P₁×⋯×Pₙ such that (a₁,…,aₙ)<ₗₑₓ(b₁,…,bₙ) iff ∃k ≤ n (a_k <ₖ b_k ∧ ∀i<k aᵢ = bᵢ)."
        },
        {
            "term": "List (or String)",
            "definition": "A finite sequence a₁a₂…aₙ of elements of X. Order matters and repetition is allowed."
        },
        {
            "term": "Operation on a set X",
            "definition": "A function f : Xⁿ → X."
        },
        {
            "term": "Multiset",
            "definition": "A subset of X with repetitions, where each element has a positive multiplicity."
        },
        {
            "term": "Multiset Ordering",
            "definition": "If (X,<) is a strict order, define M > N when N is obtained from M by replacing an element a with elements all smaller than a."
        },
        {
            "term": "Powerset of a set X",
            "definition": "The set P(X) of all subsets of X, with union, intersection and difference operations."
        },
        {
            "term": "Relation",
            "definition": "A binary relation on X is a subset of X×X. For example, < and ≤ on numbers."
        },
        {
            "term": "Strict Ordering Relation",
            "definition": "A binary relation < on X that is irreflexive and transitive. Total if ∀a,b ∈ X (a<b ∨ a=b ∨ b<a)."
        },
        {
            "term": "Subset of a set X",
            "definition": "A set S containing some (possibly all or none) elements of X, denoted S ⊆ X."
        },
        
        # New Z3/SMT concepts
        {
            "term": "SMT Solver",
            "definition": "A satisfiability modulo theories solver that determines if mathematical formulas are satisfiable with respect to background theories like arithmetic, arrays, bit-vectors, etc. SMT solvers extend SAT solvers by incorporating decision procedures for various mathematical theories."
        },
        {
            "term": "SMT-LIB Standard",
            "definition": "A standardized input format for SMT solvers that defines syntax and semantics for expressing logical formulas in various theories. The standard specifies how to represent sorts, functions, predicates, and logical connectives in a uniform way across different solvers."
        },
        {
            "term": "Theory Combination",
            "definition": "The technique used by SMT solvers to combine decision procedures for different theories to solve formulas involving multiple theories. The Nelson-Oppen method is a common approach for theory combination when the theories are disjoint and stably infinite."
        },
        {
            "term": "Model Construction",
            "definition": "The process by which an SMT solver produces a concrete interpretation that satisfies a given formula when it is determined to be satisfiable. The model assigns values to all uninterpreted symbols in a way that makes the formula true."
        },
        {
            "term": "Satisfiability",
            "definition": "A logical formula is satisfiable if there exists at least one interpretation (model) under which the formula evaluates to true. In SMT solving, this means finding values for variables that make the formula hold according to the theory constraints."
        },
        {
            "term": "Uninterpreted Function",
            "definition": "A function symbol in SMT that has no predefined meaning and can be assigned any interpretation in a model, subject only to the constraints imposed by the formula. Uninterpreted functions are key to representing abstract specifications."
        },
        {
            "term": "Quantifier-Free Formulas",
            "definition": "Logical formulas that contain no universal (∀) or existential (∃) quantifiers. Many SMT solvers are particularly efficient at solving quantifier-free formulas in decidable theories."
        },
        {
            "term": "Bit-Vectors Theory",
            "definition": "An SMT theory that represents fixed-width binary numbers and operations on them, such as addition, subtraction, bitwise AND/OR/XOR, shifts, and comparisons. Essential for reasoning about low-level software and hardware."
        },
        {
            "term": "Array Theory",
            "definition": "An SMT theory that models memory-like structures with read and write operations. Arrays are functions from indices to values, with the select (read) and store (write) operations satisfying extensionality axioms."
        },
        {
            "term": "Linear Arithmetic",
            "definition": "An SMT theory dealing with linear constraints over integer or real variables, such as 2x + 3y ≤ 5. Linear arithmetic is decidable and admits efficient decision procedures based on the simplex algorithm or Fourier-Motzkin elimination."
        },
        
        # Quotient Set Concepts
        {
            "term": "Quotient Set",
            "definition": "The set of all equivalence classes of a set X with respect to an equivalence relation ∼. Denoted X/∼, it represents the partitioning of X into disjoint subsets where elements in the same subset are considered equivalent. In logic, quotient sets are used to handle synonymy by grouping equivalent identifiers."
        },
        {
            "term": "Equivalence Class",
            "definition": "A subset of a set X containing all elements that are equivalent to a given element a under an equivalence relation ∼. Denoted [a], it consists of all elements b such that a ∼ b. Different equivalence classes are disjoint, and their union is the entire set X."
        },
        {
            "term": "Modular Arithmetic",
            "definition": "A system of arithmetic for integers where numbers 'wrap around' after reaching a certain value (the modulus n). Two integers x and y are congruent modulo n (x ≡n y) if they have the same remainder when divided by n. This defines an equivalence relation whose quotient set Z/≡n has n elements."
        },
        {
            "term": "Congruence Closure",
            "definition": "An algorithm for determining equivalence in the theory of uninterpreted functions and equality. Given a set of equalities, congruence closure computes the equivalence classes of all terms by applying reflexivity, symmetry, transitivity, and congruence rules until no new equivalences can be derived."
        }
    ]
