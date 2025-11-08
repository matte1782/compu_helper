"""
Enhanced question generation with better distractors and mathematical precision
"""

import random
from typing import Tuple, List, Dict, Optional
from dataclasses import dataclass

@dataclass
class GlossaryEntry:
    """Data class for glossary entries"""
    term: str
    definition: str
    category: str
    difficulty: int  # 1-5
    related_terms: List[str]

class EnhancedQuestionGenerator:
    """Generates high-quality questions for theoretical computer science concepts"""
    
    def __init__(self, glossary_entries: Dict[str, GlossaryEntry]):
        self.glossary = glossary_entries
        self._prepare_distractors()
    
    def _prepare_distractors(self):
        """Prepare plausible distractors for different categories"""
        self.category_distractors = {
            "Set Theory": ["Functions", "Relations", "Orderings", "Graphs", "Multisets"],
            "Functions": ["Set Theory", "Relations", "Orderings", "Data Structures", "Multisets"],
            "Relations": ["Set Theory", "Functions", "Orderings", "Graphs", "Data Structures"],
            "Orderings": ["Set Theory", "Functions", "Relations", "Graphs", "Data Structures"],
            "Graphs": ["Set Theory", "Functions", "Relations", "Orderings", "Data Structures"],
            "Multisets": ["Set Theory", "Functions", "Relations", "Orderings", "Graphs"],
            "Data Structures": ["Set Theory", "Functions", "Relations", "Orderings", "Graphs"],
            "General": ["Set Theory", "Functions", "Relations", "Orderings", "Graphs"]
        }
        
        # Common misconception patterns
        self.misconceptions = {
            "Cartesian Product": [
                "A Cartesian product is commutative, so X × Y = Y × X",
                "The Cartesian product of a set with itself is just the set",
                "Cartesian products can only be formed between two sets"
            ],
            "Equivalence Relation": [
                "An equivalence relation only needs to be reflexive and symmetric",
                "Transitivity means if aRb then bRa",
                "Any symmetric relation is automatically an equivalence relation"
            ],
            "Function": [
                "All functions are bijective",
                "Injective functions must also be surjective",
                "Functions can map one input to multiple outputs"
            ],
            "SMT Solver": [
                "SMT solvers can solve any logical formula",
                "SMT solvers always return a model for satisfiable formulas",
                "SMT solvers work by trying all possible assignments"
            ]
        }
    
    def generate_definition_question(self, term: str) -> Tuple[str, str, List[str]]:
        """Generate a precise definition-based question"""
        entry = self.glossary.get(term.lower())
        if not entry:
            return "", "", []
            
        question = f"What is the precise mathematical definition of '{entry.term}'?"
        correct_answer = entry.definition
        
        # Generate sophisticated distractors
        distractors = self._generate_definition_distractors(entry)
        options = [correct_answer[:120] + "..."] + distractors
        random.shuffle(options)
        
        return question, correct_answer, options
    
    def _generate_definition_distractors(self, entry: GlossaryEntry) -> List[str]:
        """Generate plausible definition distractors"""
        distractors = []
        all_terms = list(self.glossary.keys())
        
        # Add category-based misconceptions if available
        for misconception_term, misconceptions in self.misconceptions.items():
            if misconception_term.lower() in entry.term.lower():
                distractors.extend(misconceptions)
                break
        
        # Add related term definitions (wrongly applied)
        for related_term in entry.related_terms[:2]:
            related_entry = self.glossary.get(related_term.lower())
            if related_entry and len(distractors) < 3:
                # Take a portion that sounds plausible but is wrong
                parts = related_entry.definition.split('.')
                if len(parts) > 1:
                    distractors.append(parts[0].strip() + ".")
        
        # Add generic mathematical misconceptions
        generic_misconceptions = [
            "This concept is only applicable in theoretical mathematics with no practical use",
            "This is a simple concept that doesn't require formal definition",
            "This concept is equivalent to its opposite in all contexts"
        ]
        distractors.extend(generic_misconceptions)
        
        # Truncate and ensure uniqueness
        truncated_distractors = []
        for d in distractors[:3]:
            truncated = d[:120] + "..." if len(d) > 120 else d
            if truncated not in truncated_distractors:
                truncated_distractors.append(truncated)
        
        return truncated_distractors[:3]
    
    def generate_relationship_question(self, term: str) -> Tuple[str, str, List[str]]:
        """Generate a relationship-based question with mathematical precision"""
        entry = self.glossary.get(term.lower())
        if not entry or not entry.related_terms:
            return "", "", []
            
        related_term = random.choice(entry.related_terms)
        related_entry = self.glossary.get(related_term.lower())
        
        if not related_entry:
            return "", "", []
            
        question = f"What is the precise mathematical relationship between '{entry.term}' and '{related_entry.term}'?"
        correct_answer = f"According to the definition: {entry.definition}"
        
        # Generate mathematically plausible distractors
        distractors = [
            f"{entry.term} is a special case of {related_entry.term} when additional constraints are applied",
            f"{related_entry.term} and {entry.term} are completely independent concepts with no relationship",
            f"{entry.term} can always be transformed into {related_entry.term} through a simple mapping"
        ]
        
        options = [correct_answer[:150] + "..."] + distractors
        random.shuffle(options)
        
        return question, correct_answer, options
    
    def generate_category_question(self, term: str) -> Tuple[str, str, List[str]]:
        """Generate a category-based question"""
        entry = self.glossary.get(term.lower())
        if not entry:
            return "", "", []
            
        question = f"Which mathematical category does '{entry.term}' fundamentally belong to?"
        correct_answer = entry.category
        
        # Generate plausible category distractors
        distractors = self.category_distractors.get(entry.category, ["Set Theory", "Functions", "Relations"])
        distractors = [cat for cat in distractors if cat != entry.category]
        distractors = random.sample(distractors, min(3, len(distractors)))
        
        options = [correct_answer] + distractors
        random.shuffle(options)
        
        return question, correct_answer, options
    
    def generate_application_question(self, term: str) -> Tuple[str, str, List[str]]:
        """Generate an application-based question with theoretical grounding"""
        entry = self.glossary.get(term.lower())
        if not entry:
            return "", "", []
            
        question = f"In what theoretical or practical context is '{entry.term}' most significantly applied?"
        correct_answer = entry.definition  # The definition often contains application context
        
        # Generate application-focused distractors
        distractors = [
            "Exclusively in quantum computing algorithms",
            "Only in database management systems with no theoretical significance",
            "Purely in abstract mathematics with no computational applications",
            "Only in hardware design and not in software verification"
        ]
        
        options = [correct_answer[:150] + "..."] + distractors[:3]
        random.shuffle(options)
        
        return question, correct_answer, options
    
    def generate_example_question(self, term: str) -> Tuple[str, str, List[str]]:
        """Generate an example-based question"""
        entry = self.glossary.get(term.lower())
        if not entry:
            return "", "", []
            
        question = f"Which of the following is a correct example of '{entry.term}'?"
        # Extract example from definition if available
        definition_parts = entry.definition.split('.')
        example_part = None
        for part in definition_parts:
            if 'example' in part.lower() or 'for example' in part.lower():
                example_part = part.strip()
                break
        
        if example_part:
            correct_answer = example_part
        else:
            correct_answer = entry.definition.split('.')[0] + "."  # First sentence often contains key info
        
        # Generate plausible but incorrect examples
        distractors = [
            "A trivial case that doesn't demonstrate the full concept",
            "An edge case that violates the definition",
            "A related concept that is often confused with the actual term"
        ]
        
        options = [correct_answer[:150] + "..."] + distractors
        random.shuffle(options)
        
        return question, correct_answer, options
