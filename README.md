# COMPU LOGIC

```
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
```

> An advanced, interactive learning assistant for mastering theoretical computer science concepts, including SMT solvers, set theory, logic, and formal methods.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## 📚 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies](#technologies)
- [Learning Methodology](#learning-methodology)
- [Configuration](#configuration)
- [Database Schema](#database-schema)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

**COMPU LOGIC** is a comprehensive, terminal-based learning platform designed to help students, researchers, and enthusiasts master theoretical computer science concepts. The application focuses on:

- **Set Theory**: Cartesian products, powersets, subsets, characteristic functions
- **Functions**: Injective, surjective, bijective functions and compositions
- **Relations**: Equivalence relations, orderings, congruence closure
- **SMT Solvers**: Z3, satisfiability, theory combination, model construction
- **Formal Methods**: Bit-vectors, arrays, linear arithmetic, quotient sets
- **Data Structures**: Lists, graphs, multisets

The platform uses **adaptive learning algorithms**, **spaced repetition**, and **progress tracking** to optimize knowledge retention and mastery.

---

## ✨ Features

### 🎓 Core Learning Features

- **Interactive Glossary**: Browse 30+ theoretical CS concepts organized by category and difficulty
- **Adaptive Quiz System**: Dynamic question generation with 5 question types
- **Progress Tracking**: SQLite-based persistence of learning metrics and mastery levels
- **Spaced Repetition**: Scientifically-backed scheduling for optimal review intervals
- **Advanced Answer Validation**: Fuzzy matching, substring detection, and normalization

### 🎨 User Experience

- **Rich Terminal UI**: Beautiful, colorful interface using the Rich library
- **ASCII Art Design**: Custom logo and typewriter animation effects
- **Term of the Day**: Random concept highlighting on startup
- **Category-Based Study**: Focused learning sessions by topic area
- **Difficulty Ratings**: 5-star difficulty system (★★★★★)
- **Related Terms**: Automatic linking of conceptually related topics

### 📊 Analytics & Insights

- **Mastery Levels**: 0-100% mastery tracking per concept
- **Success Rates**: Detailed attempt vs. correct attempt statistics
- **Learning Summaries**: Average mastery and overall performance metrics
- **Historical Data**: Question results with timestamps and feedback

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Terminal with UTF-8 encoding support

### Step 1: Clone the Repository

```bash
git clone https://github.com/matte1782/compu-logic.git
cd compu-logic
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- `rich>=13.0.0` - Terminal UI and formatting
- `colorama>=0.4.6` - Cross-platform colored output

### Step 3: Verify Installation

```bash
python main.py
```

You should see the COMPU LOGIC startup animation and main menu.

---

## ⚡ Quick Start

### Basic Usage

```bash
# Start the application
python main.py

# Enter your username when prompted
# Navigate using numbered menu options (1-7)
```

### First-Time User Flow

1. **Launch COMPU LOGIC**: Run `python main.py`
2. **Enter Username**: Create your user profile
3. **Browse Glossary**: Select option 1 to explore concepts
4. **Take Quiz**: Select option 2 to test your knowledge
5. **View Progress**: Select option 3 to see your mastery levels

---

## 📖 Usage

### Main Menu Options

```
1. Interactive Glossary  - Browse and explore definitions
2. Take Quiz            - Adaptive questioning system
3. View Progress        - Track mastery and statistics
4. Search Terms         - Find specific concepts
5. Study by Category    - Focus on topic areas
6. Help                 - View detailed instructions
7. Exit                 - Close the application
```

### Interactive Glossary

Navigate through categorized terms:

```
Available Categories:
1. Set Theory (8 terms)
2. Functions (5 terms)
3. Relations (3 terms)
4. SMT Solvers (10 terms)
5. Orderings (3 terms)
...
```

Each term displays:
- **Definition**: Comprehensive mathematical explanation
- **Category**: Conceptual grouping
- **Difficulty**: 1-5 star rating
- **Related Terms**: Linked concepts
- **Personal Progress**: Your mastery percentage

### Adaptive Quiz System

The quiz system generates questions using 5 different types:

1. **Definition Questions**: "What is the precise mathematical definition of..."
2. **Category Questions**: "Which category does this term belong to..."
3. **Relationship Questions**: "What is the relationship between..."
4. **Application Questions**: "In what context is this concept applied..."
5. **Example Questions**: "Which is a correct example of..."

**Answer Validation:**
- Exact match detection
- Substring matching
- Fuzzy similarity matching (80% threshold)
- Intelligent feedback messages

### Progress Tracking

View detailed statistics:

```
Term                              Category      Attempts  Success Rate  Mastery
─────────────────────────────────────────────────────────────────────────────
SMT Solver                        SMT Solvers   5         80.0%         92%
Cartesian Product                 Set Theory    8         87.5%         88%
Equivalence Relation              Relations     6         66.7%         75%
...

Summary:
Terms Studied: 15
Average Mastery: 78.3%
Overall Success Rate: 76.5%
```

---

## 📁 Project Structure

```
compu-logic/
├── main.py                           # Main application entry point
├── answer_validator.py               # Answer checking logic
├── enhanced_glossary.py              # Glossary definitions
├── enhanced_question_generator.py    # Question generation engine
├── spaced_repetition.py              # Learning scheduler
├── compulogic.db                     # SQLite database (auto-generated)
├── requirements.txt                  # Python dependencies
├── README.md                         # This file
└── reports/                          # Generated reports directory
```

### Module Descriptions

| Module | Purpose |
|--------|---------|
| `main.py` | Application core, UI, and menu system |
| `answer_validator.py` | Multi-strategy answer validation |
| `enhanced_glossary.py` | 30+ theoretical CS term definitions |
| `enhanced_question_generator.py` | Adaptive question generation |
| `spaced_repetition.py` | Spaced repetition algorithm (Leitner system) |

---

## 🛠️ Technologies

### Core Technologies

- **Python 3.8+**: Primary programming language
- **SQLite3**: Embedded database for progress tracking
- **Rich**: Terminal UI framework
- **Colorama**: Cross-platform color support

### Design Patterns

- **Dataclasses**: Structured data representation
- **Factory Pattern**: Question generation
- **Repository Pattern**: Database access layer
- **Strategy Pattern**: Answer validation methods

### Algorithms

- **Spaced Repetition**: Modified Leitner system with ease factors
- **Fuzzy Matching**: SequenceMatcher with 80% threshold
- **Mastery Calculation**: Diminishing returns algorithm
- **Adaptive Difficulty**: Based on user performance

---

## 📚 Learning Methodology

### Spaced Repetition System

COMPU LOGIC implements a scientifically-backed spaced repetition system:

```python
Base Intervals: [1, 3, 7, 14, 30, 90] days
Ease Factors:
  - Again (incorrect): 0.8x
  - Hard: 1.2x
  - Good: 1.5x
  - Easy: 2.0x
```

### Mastery Calculation

Mastery levels (0.0 to 1.0) are updated using:

**Correct Answer:**
```python
improvement = 0.1 * (1.0 - current_mastery)
new_mastery = min(1.0, current_mastery + improvement)
```

**Incorrect Answer:**
```python
decrement = 0.05 * current_mastery
new_mastery = max(0.1, current_mastery - decrement)
```

This ensures:
- Diminishing returns as mastery increases
- Minimum 10% mastery floor
- Gradual knowledge decay on errors

---

## ⚙️ Configuration

### Environment Variables

```bash
# Custom database path
export COMPU_LOGIC_DB_PATH=/path/to/custom/database.db

# Reports directory
export COMPU_LOGIC_REPORTS_DIR=/path/to/reports
```

### Configuration Dictionary

Edit `CONFIG` in `main.py`:

```python
CONFIG = {
    'DB_PATH': 'compulogic.db',
    'REPORTS_DIR': 'reports',
    'MAX_HINTS': 3,
    'QUESTIONS_PER_SESSION': 10,
}
```

---

## 🗄️ Database Schema

### `user_progress` Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key |
| `user_id` | TEXT | Username |
| `term` | TEXT | Concept term |
| `attempts` | INTEGER | Total attempts |
| `correct_attempts` | INTEGER | Successful attempts |
| `last_attempt` | TIMESTAMP | Last interaction time |
| `mastery_level` | REAL | 0.0 to 1.0 mastery |
| `created_at` | TIMESTAMP | Record creation time |

### `question_results` Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key |
| `question_id` | TEXT | Unique question identifier |
| `user_id` | TEXT | Username |
| `term` | TEXT | Concept term |
| `question_type` | TEXT | Question generation method |
| `user_answer` | TEXT | User's response |
| `correct_answer` | TEXT | Correct response |
| `passed` | BOOLEAN | Success indicator |
| `time_taken` | REAL | Response time (seconds) |
| `feedback` | TEXT | Validation feedback |
| `created_at` | TIMESTAMP | Record creation time |

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

### Reporting Issues

- Use the GitHub issue tracker
- Include Python version, OS, and error messages
- Provide steps to reproduce

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to functions and classes
- Write descriptive commit messages

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Inspired by formal methods and SMT solver research
- Built with the excellent [Rich](https://github.com/Textualize/rich) library
- Spaced repetition based on Leitner system research
- Glossary content derived from theoretical CS curricula

---

## 📧 Contact

**Maintainer**: matte1782  
**GitHub**: [@matte1782](https://github.com/matte1782)

---

<div align="center">

**[⬆ Back to Top](#compu-logic)**

Made with ❤️ for computer science education

*Mastering Logic & Computation, One Concept at a Time*

</div>
