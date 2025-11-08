"""
Answer validation utilities for COMPU LOGIC
Provides robust answer checking with normalization and fuzzy matching
"""

import re
from typing import Tuple
from difflib import SequenceMatcher

class AnswerValidator:
    """Validates user answers against correct answers with multiple strategies"""
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """Normalize text for comparison"""
        if not text:
            return ""
        # Convert to lowercase and strip whitespace
        normalized = text.lower().strip()
        # Remove extra whitespace
        normalized = re.sub(r'\s+', ' ', normalized)
        # Remove punctuation that doesn't affect meaning
        normalized = re.sub(r'[.,;:!?"]', '', normalized)
        return normalized
    
    @staticmethod
    def check_exact_match(user_answer: str, correct_answer: str) -> bool:
        """Check for exact match after normalization"""
        return AnswerValidator.normalize_text(user_answer) == AnswerValidator.normalize_text(correct_answer)
    
    @staticmethod
    def check_substring_match(user_answer: str, correct_answer: str) -> bool:
        """Check if user answer is contained in correct answer"""
        user_norm = AnswerValidator.normalize_text(user_answer)
        correct_norm = AnswerValidator.normalize_text(correct_answer)
        
        if not user_norm or not correct_norm:
            return False
            
        return user_norm in correct_norm
    
    @staticmethod
    def check_fuzzy_match(user_answer: str, correct_answer: str, threshold: float = 0.8) -> bool:
        """Check similarity using fuzzy matching"""
        user_norm = AnswerValidator.normalize_text(user_answer)
        correct_norm = AnswerValidator.normalize_text(correct_answer)
        
        if not user_norm or not correct_norm:
            return False
            
        similarity = SequenceMatcher(None, user_norm, correct_norm).ratio()
        return similarity >= threshold
    
    @staticmethod
    def validate_answer(user_answer: str, correct_answer: str) -> Tuple[bool, str]:
        """
        Validate user answer with multiple strategies
        
        Returns:
            Tuple of (is_correct, feedback_message)
        """
        if AnswerValidator.check_exact_match(user_answer, correct_answer):
            return True, "Exact match!"
        
        if AnswerValidator.check_substring_match(user_answer, correct_answer):
            return True, "Correct concept identified!"
        
        if AnswerValidator.check_fuzzy_match(user_answer, correct_answer):
            return True, "Close enough - good understanding!"
        
        return False, "Answer needs improvement"

# Convenience function for backward compatibility
def validate_answer(user_answer: str, correct_answer: str) -> bool:
    """Simple boolean validation for existing code"""
    validator = AnswerValidator()
    is_correct, _ = validator.validate_answer(user_answer, correct_answer)
    return is_correct
