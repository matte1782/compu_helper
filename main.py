"""
COMPU LOGIC - Advanced Theoretical Computer Science Learning Assistant

A comprehensive interactive learning tool for theoretical computer science concepts,
particularly focused on SMT solvers like Z3, set theory, logic, and formal methods.

Features:
- Interactive glossary with detailed definitions
- Adaptive questioning system
- Progress tracking and mastery assessment
- Rich visual interface with ASCII art
- Secure and performant architecture
"""

import json
import os
import sys
import time
import random
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import hashlib

# Import enhanced modules
from answer_validator import AnswerValidator
from enhanced_glossary import get_enhanced_glossary
from enhanced_question_generator import EnhancedQuestionGenerator
from spaced_repetition import SpacedRepetitionScheduler, LearningItem

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.markdown import Markdown
    from rich.text import Text
    from rich.progress import track
    import colorama
    from colorama import Fore, Style
except ImportError:
    print("Error: Required packages not installed.")
    print("Please run: pip install rich colorama")
    sys.exit(1)

# Initialize colorama for cross-platform colored output
colorama.init()

# Configuration
CONFIG = {
    'DB_PATH': os.getenv('COMPU_LOGIC_DB_PATH', 'compulogic.db'),
    'REPORTS_DIR': 'reports',
    'MAX_HINTS': 3,
    'QUESTIONS_PER_SESSION': 10,
}

# COMPU LOGIC ART DESIGN - BOLD AND ITALIAN GRAPHIC STYLE
COMPU_LOGIC_ART = r"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  ██████╗ ██████╗ ███╗   ███╗██████╗ ██╗   ██╗    ██╗      ██████╗██╗ ██████╗ ║
║ ██╔════╝██╔═══██╗████╗ ████║██╔══██╗╚██╗ ██╔╝    ██║     ██╔════╝██║██╔════╝ ║
║ ██║     ██║   ██║██╔████╔██║██████╔╝ ╚████╔╝     ██║     ██║     ██║██║      ║
║ ██║     ██║   ██║██║╚██╔╝██║██╔═══╝   ╚██╔╝      ██║     ██║     ██║██║      ║
║ ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║        ██║       ███████╗╚██████╗██║╚██████╗ ║
║  ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝        ╚═╝       ╚══════╝ ╚═════╝╚═╝ ╚═════╝ ║
║                                                                              ║
║              Theoretical Computer Science Learning Assistant                 ║
║                        Mastering Logic & Computation                         ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

@dataclass
class GlossaryEntry:
    """Data class for glossary entries"""
    term: str
    definition: str
    category: str
    difficulty: int  # 1-5
    related_terms: List[str]

@dataclass
class UserProgress:
    """Data class to track user progress"""
    user_id: str
    term: str
    attempts: int
    correct_attempts: int
    last_attempt: datetime
    mastery_level: float  # 0.0 to 1.0

    def get_mastery_percentage(self) -> int:
        return int(self.mastery_level * 100)

@dataclass
class QuestionResult:
    """Data class to store question results"""
    question_id: str
    term: str
    question_type: str
    user_answer: str
    correct_answer: str
    passed: bool
    time_taken: float
    feedback: str

class DatabaseManager:
    """Manages SQLite database for user progress tracking"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or CONFIG['DB_PATH']
        self.init_database()

    def init_database(self):
        """Initialize database tables"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create user progress table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                term TEXT NOT NULL,
                attempts INTEGER DEFAULT 0,
                correct_attempts INTEGER DEFAULT 0,
                last_attempt TIMESTAMP,
                mastery_level REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, term)
            )
        ''')

        # Create question results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS question_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                term TEXT NOT NULL,
                question_type TEXT NOT NULL,
                user_answer TEXT,
                correct_answer TEXT,
                passed BOOLEAN,
                time_taken REAL,
                feedback TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()

    def save_progress(self, progress: UserProgress):
        """Save user progress to database"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO user_progress
            (user_id, term, attempts, correct_attempts, last_attempt, mastery_level)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id, term) DO UPDATE SET
                attempts = excluded.attempts,
                correct_attempts = excluded.correct_attempts,
                last_attempt = excluded.last_attempt,
                mastery_level = excluded.mastery_level
        ''', (
            progress.user_id,
            progress.term,
            progress.attempts,
            progress.correct_attempts,
            progress.last_attempt.isoformat() if progress.last_attempt else None,
            progress.mastery_level
        ))

        conn.commit()
        conn.close()

    def get_user_progress(self, user_id: str, term: str = None) -> List[UserProgress]:
        """Retrieve user progress from database"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if term:
            cursor.execute('''
                SELECT * FROM user_progress 
                WHERE user_id = ? AND term = ?
            ''', (user_id, term))
        else:
            cursor.execute('''
                SELECT * FROM user_progress 
                WHERE user_id = ?
            ''', (user_id,))

        rows = cursor.fetchall()
        conn.close()

        progress_list = []
        for row in rows:
            progress = UserProgress(
                user_id=row[1],
                term=row[2],
                attempts=row[3] or 0,
                correct_attempts=row[4] or 0,
                last_attempt=datetime.fromisoformat(row[5]) if row[5] else None,
                mastery_level=row[6] or 0.0
            )
            progress_list.append(progress)

        return progress_list

    def save_question_result(self, result: QuestionResult, user_id: str):
        """Save question result to database"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO question_results
            (question_id, user_id, term, question_type, user_answer, 
             correct_answer, passed, time_taken, feedback)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            result.question_id,
            user_id,
            result.term,
            result.question_type,
            result.user_answer,
            result.correct_answer,
            result.passed,
            result.time_taken,
            result.feedback
        ))

        conn.commit()
        conn.close()

class GlossaryManager:
    """Manages the theoretical computer science glossary"""
    
    def __init__(self):
        self.entries: Dict[str, GlossaryEntry] = {}
        self._load_glossary()

    def _load_glossary(self):
        """Load glossary entries from the provided text"""
        glossary_definitions = get_enhanced_glossary()
        
        # Process each entry with progress bar
        console = Console()
        for entry_data in track(glossary_definitions, description="Loading glossary entries..."):
            term = entry_data["term"]
            definition = entry_data["definition"]
            
            # Determine category and difficulty
            category = self._categorize_term(term)
            difficulty = self._assess_difficulty(term)
            
            # Find related terms
            related_terms = self._find_related_terms(definition, term, glossary_definitions)
            
            # Create entry
            entry = GlossaryEntry(
                term=term,
                definition=definition,
                category=category,
                difficulty=difficulty,
                related_terms=related_terms
            )
            
            self.entries[term.lower()] = entry

    def _categorize_term(self, term: str) -> str:
        """Categorize a term based on its name"""
        term_lower = term.lower()
        if any(word in term_lower for word in ['function', 'bijective', 'injective', 'surjective', 'composition']):
            return 'Functions'
        elif any(word in term_lower for word in ['set', 'subset', 'powerset', 'cartesian', 'characteristic']):
            return 'Set Theory'
        elif any(word in term_lower for word in ['relation', 'equivalence', 'congruence']):
            return 'Relations'
        elif any(word in term_lower for word in ['order', 'ordering', 'lexicographic']):
            return 'Orderings'
        elif any(word in term_lower for word in ['graph']):
            return 'Graphs'
        elif any(word in term_lower for word in ['list', 'string', 'tuple']):
            return 'Data Structures'
        elif any(word in term_lower for word in ['multiset']):
            return 'Multisets'
        elif any(word in term_lower for word in ['smt', 'solver', 'satisfiability', 'theory', 'model', 'bit-vector', 'array']):
            return 'SMT Solvers'
        else:
            return 'General'

    def _assess_difficulty(self, term: str) -> int:
        """Assess the difficulty level of a term (1-5)"""
        term_lower = term.lower()
        complex_terms = ['characteristic function', 'composition', 'bijective', 'equivalence relation', 
                        'lexicographic ordering', 'multiset ordering', 'strict ordering relation',
                        'smt solver', 'theory combination', 'congruence closure', 'quotient set']
        
        if any(ct in term_lower for ct in complex_terms):
            return 5
        elif any(word in term_lower for word in ['function', 'relation', 'ordering', 'smt-lib']):
            return 4
        elif any(word in term_lower for word in ['set', 'cartesian', 'powerset', 'model']):
            return 3
        elif any(word in term_lower for word in ['list', 'graph', 'multiset', 'bit-vector']):
            return 2
        else:
            return 1

    def _find_related_terms(self, definition: str, current_term: str, all_definitions: List[Dict]) -> List[str]:
        """Find related terms mentioned in the definition"""
        related = []
        definition_lower = definition.lower()
        current_term_words = set(current_term.lower().split())
        
        for entry in all_definitions:
            term = entry["term"]
            if term.lower() == current_term.lower():
                continue
                
            # Check for term mentions in definition
            if term.lower() in definition_lower:
                related.append(term)
                continue
                
            # Check for shared conceptual words
            term_words = set(term.lower().split())
            if len(current_term_words.intersection(term_words)) >= 2:
                related.append(term)
        
        return related[:5]  # Limit to 5 related terms

    def get_entry(self, term: str) -> Optional[GlossaryEntry]:
        """Get a glossary entry by term"""
        return self.entries.get(term.lower())

    def search_entries(self, query: str) -> List[GlossaryEntry]:
        """Search for entries matching a query"""
        query_lower = query.lower()
        results = []
        
        for entry in self.entries.values():
            if (query_lower in entry.term.lower() or 
                query_lower in entry.definition.lower() or
                query_lower in entry.category.lower()):
                results.append(entry)
                
        return results

    def get_terms_by_category(self, category: str) -> List[GlossaryEntry]:
        """Get all terms in a specific category"""
        return [entry for entry in self.entries.values() if entry.category == category]

    def get_terms_by_difficulty(self, difficulty: int) -> List[GlossaryEntry]:
        """Get all terms of a specific difficulty level"""
        return [entry for entry in self.entries.values() if entry.difficulty == difficulty]

    def get_random_term_of_the_day(self) -> GlossaryEntry:
        """Get a random term for the 'Term of the Day' feature"""
        terms = list(self.entries.values())
        return random.choice(terms) if terms else None

class CompuLogic:
    """Main CompuLogic application class"""
    
    def __init__(self):
        self.console = Console()
        self.db_manager = DatabaseManager()
        self.glossary_manager = GlossaryManager()
        self.question_generator = EnhancedQuestionGenerator(self.glossary_manager.entries)
        self.current_user = None
        self.session_questions = 0

    def start(self):
        """Start the CompuLogic application with animation"""
        self._show_startup_animation()
        self.console.print(COMPU_LOGIC_ART, style="bold blue")
        self.console.print("\n[bold green]Welcome to COMPU LOGIC - Your Theoretical Computer Science Learning Assistant![/bold green]\n")
        self.console.print("[italic]Mastering Logic, Sets, Functions, and Formal Methods[/italic]\n")
        
        # Show Term of the Day
        term_of_day = self.glossary_manager.get_random_term_of_the_day()
        if term_of_day:
            self.console.print("[bold cyan]🌟 Term of the Day:[/bold cyan]")
            self.console.print(f"[bold]{term_of_day.term}[/bold] - {term_of_day.definition[:100]}...\n")
        
        # Get user ID
        self.current_user = Prompt.ask("[bold yellow]Enter your username[/bold yellow]")
        if not self.current_user:
            self.current_user = "anonymous_user"
            
        self._main_menu()

    def _show_startup_animation(self):
        """Show startup animation with typewriter effect"""
        initialization_messages = [
            "Initializing logical modules...",
            "Loading theoretical foundations...",
            "Preparing interactive environment...",
            "Connecting to knowledge base...",
            "System ready!"
        ]
        
        for message in initialization_messages:
            for char in message:
                self.console.print(char, end="", style="cyan")
                time.sleep(0.05)  # Typewriter effect
            time.sleep(0.3)
            self.console.print()
        time.sleep(0.5)

    def _main_menu(self):
        """Display and handle main menu"""
        while True:
            self.console.print("\n[bold cyan]=== COMPU LOGIC Main Menu ===[/bold cyan]")
            self.console.print("1. Interactive Glossary")
            self.console.print("2. Take Quiz")
            self.console.print("3. View Progress")
            self.console.print("4. Search Terms")
            self.console.print("5. Study by Category")
            self.console.print("6. Help")
            self.console.print("7. Exit")
            
            choice = Prompt.ask("[bold yellow]Select an option[/bold yellow]", choices=["1", "2", "3", "4", "5", "6", "7"])
            
            if choice == "1":
                self._interactive_glossary()
            elif choice == "2":
                self._take_quiz()
            elif choice == "3":
                self._view_progress()
            elif choice == "4":
                self._search_terms()
            elif choice == "5":
                self._study_by_category()
            elif choice == "6":
                self._show_help()
            elif choice == "7":
                self._exit()
                break

    def _show_help(self):
        """Show help information"""
        self.console.print("\n[bold cyan]=== Help ===[/bold cyan]")
        help_text = """
[bold]COMPU LOGIC Help[/bold]

This application helps you learn theoretical computer science concepts through interactive exploration.

[yellow]Main Features:[/yellow]
• [bold]Interactive Glossary[/bold] - Browse and search definitions
• [bold]Take Quiz[/bold] - Test your knowledge with adaptive questions
• [bold]View Progress[/bold] - Track your learning mastery
• [bold]Search Terms[/bold] - Find specific concepts
• [bold]Study by Category[/bold] - Focus on specific topic areas

[yellow]Navigation:[/yellow]
• Use number keys to select menu options
• Follow on-screen prompts for input
• Press Ctrl+C to exit at any time

[yellow]Learning Tips:[/yellow]
• Review terms regularly to improve mastery
• Take quizzes frequently to test understanding
• Use the search feature to find related concepts
        """
        self.console.print(help_text)

    def _interactive_glossary(self):
        """Interactive glossary browsing"""
        self.console.print("\n[bold cyan]=== Interactive Glossary ===[/bold cyan]")
        
        # Show categories
        categories = list(set(entry.category for entry in self.glossary_manager.entries.values()))
        self.console.print("[bold]Available Categories:[/bold]")
        for i, category in enumerate(sorted(categories), 1):
            count = len(self.glossary_manager.get_terms_by_category(category))
            self.console.print(f"{i}. {category} ({count} terms)")
        
        try:
            cat_choice = int(Prompt.ask("[bold yellow]Select a category[/bold yellow]", 
                                      choices=[str(i) for i in range(1, len(categories) + 1)]))
            selected_category = sorted(categories)[cat_choice - 1]
            
            # Show terms in category
            terms = self.glossary_manager.get_terms_by_category(selected_category)
            # Sort terms alphabetically
            terms.sort(key=lambda x: x.term)
            
            self.console.print(f"\n[bold]{selected_category} Terms:[/bold]")
            
            for i, entry in enumerate(terms, 1):
                difficulty_stars = "★" * entry.difficulty + "☆" * (5 - entry.difficulty)
                self.console.print(f"{i}. [bold]{entry.term}[/bold] {difficulty_stars}")
            
            term_choice = int(Prompt.ask("[bold yellow]Select a term to view details[/bold yellow]", 
                                       choices=[str(i) for i in range(1, len(terms) + 1)]))
            selected_entry = terms[term_choice - 1]
            
            self._display_term_details(selected_entry)
            
        except (ValueError, IndexError):
            self.console.print("[red]Invalid selection. Please try again.[/red]")

    def _display_term_details(self, entry: GlossaryEntry):
        """Display detailed information about a term"""
        self.console.print(f"\n[bold blue]=== {entry.term} ===[/bold blue]")
        self.console.print(f"[italic]Category: {entry.category} | Difficulty: {'★' * entry.difficulty}[/italic]\n")
        
        # Format definition with better readability
        definition_lines = entry.definition.split('. ')
        for line in definition_lines:
            if line.strip():
                self.console.print(f"• {line.strip()}.")
        
        # Show related terms
        if entry.related_terms:
            self.console.print(f"\n[bold]Related Terms:[/bold]")
            for related in entry.related_terms[:3]:  # Show first 3
                self.console.print(f"  → {related}")
        
        # Show user progress
        progress = self.db_manager.get_user_progress(self.current_user, entry.term)
        if progress:
            p = progress[0]
            mastery = p.get_mastery_percentage()
            self.console.print(f"\n[bold]Your Progress:[/bold] {mastery}% mastery ({p.correct_attempts}/{p.attempts} correct)")

    def _take_quiz(self):
        """Take an adaptive quiz"""
        self.console.print("\n[bold cyan]=== Adaptive Quiz ===[/bold cyan]")
        self.console.print("[italic]Answer questions to test your knowledge[/italic]\n")
        
        # Select terms for quiz
        all_terms = list(self.glossary_manager.entries.keys())
        selected_terms = random.sample(all_terms, min(CONFIG['QUESTIONS_PER_SESSION'], len(all_terms)))
        
        correct_count = 0
        total_questions = len(selected_terms)
        
        for i, term in enumerate(selected_terms, 1):
            self.console.print(f"\n[bold blue]Question {i}/{total_questions}[/bold blue]")
            
            # Randomly select question type
            question_types = [
                self.question_generator.generate_definition_question,
                self.question_generator.generate_category_question,
                self.question_generator.generate_relationship_question,
                self.question_generator.generate_application_question,
                self.question_generator.generate_example_question
            ]
            
            question_func = random.choice(question_types)
            question, correct_answer, options = question_func(term)
            
            if not question:
                continue
                
            self.console.print(f"[bold]{question}[/bold]\n")
            
            # Display options
            for j, option in enumerate(options, 1):
                self.console.print(f"{j}. {option}")
            
            # Get user answer
            start_time = time.time()
            try:
                user_choice = int(Prompt.ask("\n[yellow]Your answer (1-4)[/yellow]", 
                                           choices=[str(i) for i in range(1, 5)]))
                user_answer = options[user_choice - 1]
            except (ValueError, IndexError):
                user_answer = "Invalid selection"
                
            time_taken = time.time() - start_time
            
            # Check answer
            validator = AnswerValidator()
            is_correct, feedback_msg = validator.validate_answer(user_answer, correct_answer)
            
            if is_correct:
                correct_count += 1
                self.console.print(f"[green]✓ Correct! {feedback_msg}[/green]")
            else:
                self.console.print("[red]✗ Incorrect.[/red]")
                self.console.print(f"[italic]Correct answer: {correct_answer[:100]}...[/italic]")
            
            # Save result
            result = QuestionResult(
                question_id=f"quiz_{datetime.now().timestamp()}",
                term=term,
                question_type=question_func.__name__,
                user_answer=user_answer,
                correct_answer=correct_answer,
                passed=is_correct,
                time_taken=time_taken,
                feedback=feedback_msg if is_correct else "Incorrect"
            )
            
            self.db_manager.save_question_result(result, self.current_user)
            
            # Update progress
            self._update_progress(term, is_correct)
            
            # Pause between questions
            time.sleep(1)
        
        # Show results
        score = (correct_count / total_questions) * 100 if total_questions > 0 else 0
        self.console.print(f"\n[bold cyan]=== Quiz Results ===[/bold cyan]")
        self.console.print(f"Score: {correct_count}/{total_questions} ({score:.1f}%)")
        
        if score >= 90:
            self.console.print("[bold green]Excellent work! You have mastered these concepts.[/bold green]")
        elif score >= 70:
            self.console.print("[bold yellow]Good job! Keep practicing to improve.[/bold yellow]")
        else:
            self.console.print("[bold red]Keep studying! Review the glossary entries for more practice.[/bold red]")

    def _update_progress(self, term: str, correct: bool):
        """Update user progress for a term with improved mastery calculation"""
        progress_list = self.db_manager.get_user_progress(self.current_user, term)
        
        if progress_list:
            progress = progress_list[0]
            progress.attempts += 1
            if correct:
                progress.correct_attempts += 1
                # Improved mastery calculation with diminishing returns
                improvement = 0.1 * (1.0 - progress.mastery_level)
                progress.mastery_level = min(1.0, progress.mastery_level + improvement)
            else:
                # Decrease mastery when incorrect, but not below 0.1
                decrement = 0.05 * progress.mastery_level
                progress.mastery_level = max(0.1, progress.mastery_level - decrement)
        else:
            progress = UserProgress(
                user_id=self.current_user,
                term=term,
                attempts=1,
                correct_attempts=1 if correct else 0,
                last_attempt=datetime.now(),
                mastery_level=0.1 if correct else 0.0
            )
        
        progress.last_attempt = datetime.now()
        self.db_manager.save_progress(progress)

    def _view_progress(self):
        """View user progress"""
        self.console.print("\n[bold cyan]=== Your Learning Progress ===[/bold cyan]")
        
        progress_list = self.db_manager.get_user_progress(self.current_user)
        
        if not progress_list:
            self.console.print("[yellow]No progress data available yet. Take a quiz to get started![/yellow]")
            return
            
        # Sort by mastery level
        progress_list.sort(key=lambda p: p.mastery_level, reverse=True)
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Term", style="cyan")
        table.add_column("Category", style="green")
        table.add_column("Attempts", style="yellow")
        table.add_column("Success Rate", style="blue")
        table.add_column("Mastery", style="red")
        
        for progress in progress_list[:15]:  # Show top 15
            entry = self.glossary_manager.get_entry(progress.term)
            category = entry.category if entry else "Unknown"
            
            success_rate = (progress.correct_attempts / progress.attempts * 100) if progress.attempts > 0 else 0
            table.add_row(
                progress.term,
                category,
                str(progress.attempts),
                f"{success_rate:.1f}%",
                f"{progress.get_mastery_percentage()}%"
            )
        
        self.console.print(table)
        
        # Summary statistics
        total_terms = len(progress_list)
        avg_mastery = sum(p.mastery_level for p in progress_list) / total_terms if total_terms > 0 else 0
        total_attempts = sum(p.attempts for p in progress_list)
        total_correct = sum(p.correct_attempts for p in progress_list)
        overall_success = (total_correct / total_attempts * 100) if total_attempts > 0 else 0
        
        self.console.print(f"\n[bold]Summary:[/bold]")
        self.console.print(f"Terms Studied: {total_terms}")
        self.console.print(f"Average Mastery: {avg_mastery*100:.1f}%")
        self.console.print(f"Overall Success Rate: {overall_success:.1f}%")

    def _search_terms(self):
        """Search for terms in the glossary"""
        self.console.print("\n[bold cyan]=== Search Glossary ===[/bold cyan]")
        
        query = Prompt.ask("[bold yellow]Enter search term[/bold yellow]")
        if not query:
            return
            
        results = self.glossary_manager.search_entries(query)
        
        if not results:
            self.console.print("[yellow]No matching terms found.[/yellow]")
            return
            
        self.console.print(f"\n[bold]Found {len(results)} matching terms:[/bold]")
        
        # Sort results alphabetically
        results.sort(key=lambda x: x.term)
        
        for i, entry in enumerate(results[:10], 1):  # Show first 10 results
            difficulty_stars = "★" * entry.difficulty + "☆" * (5 - entry.difficulty)
            self.console.print(f"{i}. [bold]{entry.term}[/bold] ({entry.category}) {difficulty_stars}")
            
        if len(results) > 10:
            self.console.print(f"[italic]... and {len(results) - 10} more results[/italic]")

    def _study_by_category(self):
        """Study terms organized by category"""
        self.console.print("\n[bold cyan]=== Study by Category ===[/bold cyan]")
        
        categories = list(set(entry.category for entry in self.glossary_manager.entries.values()))
        categories.sort()  # Sort alphabetically
        
        for i, category in enumerate(categories, 1):
            terms = self.glossary_manager.get_terms_by_category(category)
            avg_difficulty = sum(t.difficulty for t in terms) / len(terms) if terms else 0
            self.console.print(f"{i}. [bold]{category}[/bold] ({len(terms)} terms, avg difficulty: {'★' * round(avg_difficulty)})")
        
        try:
            choice = int(Prompt.ask("[bold yellow]Select a category to study[/bold yellow]", 
                                  choices=[str(i) for i in range(1, len(categories) + 1)]))
            selected_category = categories[choice - 1]
            
            self.console.print(f"\n[bold blue]=== {selected_category} ===[/bold blue]")
            terms = self.glossary_manager.get_terms_by_category(selected_category)
            # Sort terms alphabetically
            terms.sort(key=lambda x: x.term)
            
            for entry in terms:
                difficulty_stars = "★" * entry.difficulty + "☆" * (5 - entry.difficulty)
                self.console.print(f"• [bold]{entry.term}[/bold] {difficulty_stars}")
                # Show brief definition
                brief_def = entry.definition[:80] + "..." if len(entry.definition) > 80 else entry.definition
                self.console.print(f"  {brief_def}\n")
                
        except (ValueError, IndexError):
            self.console.print("[red]Invalid selection.[/red]")

    def _exit(self):
        """Exit the application"""
        self.console.print("\n[bold green]Thank you for using COMPU LOGIC! Arrivederci![/bold green]")
        self.console.print("[italic]Keep exploring the fascinating world of theoretical computer science![/italic]")

def main():
    """Main entry point"""
    try:
        app = CompuLogic()
        app.start()
    except KeyboardInterrupt:
        print("\n\n[bold red]COMPU LOGIC interrupted. Arrivederci![/bold red]")
        sys.exit(0)
    except Exception as e:
        print(f"\n[bold red]Fatal error: {e}[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
