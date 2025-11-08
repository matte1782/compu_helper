# pymaster_arcade.py

import time
import random
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.text import Text
from datetime import datetime

# Import at module level to avoid circular import issues
try:
    from pymaster import CodeAnalyzer, ChallengeResult
except ImportError:
    # Fallback for type checking or when pymaster is not available
    CodeAnalyzer = None
    ChallengeResult = None

@dataclass
class ArcadeChallenge:
    """Lightweight challenge class for arcade mode"""
    id: str
    title: str
    description: str
    function_name: str
    test_cases: List[Dict]
    expected_outputs: List[Any]
    template: str

def create_arcade_challenges() -> List[ArcadeChallenge]:
    """Create a pool of arcade challenges"""
    challenges = [
        ArcadeChallenge(
            id="arcade_001",
            title="Quick Sum",
            description="Create a function that returns the sum of two integers",
            function_name="solution",
            test_cases=[
                {'function': 'solution', 'args': [1, 2]},
                {'function': 'solution', 'args': [-5, 10]},
                {'function': 'solution', 'args': [0, 0]}
            ],
            expected_outputs=[3, 5, 0],
            template="""def solution(a: int, b: int) -> int:
    # Return the sum of a and b
    pass"""
        ),
        ArcadeChallenge(
            id="arcade_002",
            title="Even Numbers",
            description="Return a list of even numbers from the input list",
            function_name="solution",
            test_cases=[
                {'function': 'solution', 'args': [[1, 2, 3, 4, 5]]},
                {'function': 'solution', 'args': [[1, 3, 5]]},
                {'function': 'solution', 'args': [[2, 4, 6, 8]]}
            ],
            expected_outputs=[[2, 4], [], [2, 4, 6, 8]],
            template="""def solution(numbers: List[int]) -> List[int]:
    # Return only the even numbers from the input list
    pass"""
        ),
        ArcadeChallenge(
            id="arcade_003",
            title="String Reverser",
            description="Reverse the input string",
            function_name="solution",
            test_cases=[
                {'function': 'solution', 'args': ["hello"]},
                {'function': 'solution', 'args': ["Python"]},
                {'function': 'solution', 'args': [""]}
            ],
            expected_outputs=["olleh", "nohtyP", ""],
            template="""def solution(s: str) -> str:
    # Return the reversed string
    pass"""
        ),
        ArcadeChallenge(
            id="arcade_004",
            title="Max Value",
            description="Find the maximum value in a list of integers",
            function_name="solution",
            test_cases=[
                {'function': 'solution', 'args': [[1, 5, 3, 9, 2]]},
                {'function': 'solution', 'args': [[-1, -5, -3]]},
                {'function': 'solution', 'args': [[42]]}
            ],
            expected_outputs=[9, -1, 42],
            template="""def solution(numbers: List[int]) -> int:
    # Return the maximum value in the list
    pass"""
        ),
        ArcadeChallenge(
            id="arcade_005",
            title="Word Counter",
            description="Count the number of words in a sentence",
            function_name="solution",
            test_cases=[
                {'function': 'solution', 'args': ["Hello world"]},
                {'function': 'solution', 'args': ["Python is awesome"]},
                {'function': 'solution', 'args': [""]}
            ],
            expected_outputs=[2, 3, 0],
            template="""def solution(sentence: str) -> int:
    # Return the number of words in the sentence
    pass"""
        )
    ]
    return challenges

def get_user_code(console: Console, challenge: ArcadeChallenge) -> str:
    """Get user code input for a challenge"""
    console.print(Panel(challenge.template, title="Code Template", border_style="bright_blue"))
    
    console.print("\n[bold bright_yellow]Enter your solution (type 'END' alone on a line to finish):[/bold bright_yellow]")
    lines = []
    while True:
        try:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        except KeyboardInterrupt:
            console.print("\n[yellow]Input cancelled.[/yellow]")
            return ""
    return "\n".join(lines).strip()

def run_arcade_challenge(console: Console, validator: 'ChallengeValidator', 
                        challenge: ArcadeChallenge) -> Tuple[bool, float, List[str]]:
    """Run a single arcade challenge"""
    start_time = time.time()
    
    console.print(f"\n[bold magenta]⚡ {challenge.title}[/bold magenta]")
    console.print(f"[italic bright_blue]{challenge.description}[/italic bright_blue]\n")
    
    user_code = get_user_code(console, challenge)
    if not user_code:
        return False, 0, ["Challenge skipped"]
    
    # Validate syntax
    ok, syn_feedback = CodeAnalyzer.validate_syntax(user_code)
    if not ok:
        console.print("[red]❌ Syntax Errors:[/red]")
        for e in syn_feedback:
            console.print(f"  [red]{e}[/red]")
        return False, time.time() - start_time, syn_feedback
    
    # Validate solution
    passed, feedback = validator.validate_solution(
        user_code, challenge.test_cases, challenge.expected_outputs
    )
    
    # Display results
    console.print("\n[bold bright_cyan]=== Test Results ===[/bold bright_cyan]")
    for line in feedback:
        if line.startswith("✅"):
            console.print(f"[green]{line}[/green]")
        elif line.startswith("❌"):
            console.print(f"[red]{line}[/red]")
        elif line.startswith("🎉"):
            console.print(f"[bold green]{line}[/bold green]")
        else:
            console.print(line)
    
    execution_time = time.time() - start_time
    return passed, execution_time, feedback

def show_arcade_summary(console: Console, stats: Dict[str, Any], username: str):
    """Show the arcade mode summary screen"""
    console.clear()
    
    # Big title
    title = Text("🎮 ARCADE MODE COMPLETE 🎮", style="bold magenta")
    console.print(Panel(title, border_style="bright_magenta"))
    
    # Stats panel
    stats_text = Text()
    stats_text.append(f"Player: ", style="bright_cyan")
    stats_text.append(f"{username}\n\n", style="bold white")
    
    stats_text.append(f"Time Played: ", style="bright_cyan")
    stats_text.append(f"{stats['duration']:.1f} seconds\n", style="bold yellow")
    
    stats_text.append(f"Challenges Attempted: ", style="bright_cyan")
    stats_text.append(f"{stats['attempted']}\n", style="bold yellow")
    
    stats_text.append(f"Challenges Solved: ", style="bright_cyan")
    stats_text.append(f"{stats['solved']}\n", style="bold yellow")
    
    stats_text.append(f"Success Rate: ", style="bright_cyan")
    rate = (stats['solved'] / stats['attempted'] * 100) if stats['attempted'] > 0 else 0
    stats_text.append(f"{rate:.1f}%\n\n", style="bold yellow")
    
    stats_text.append(f"Best Streak: ", style="bright_cyan")
    stats_text.append(f"{stats['best_streak']}\n", style="bold yellow")
    
    stats_text.append(f"Average Time/Challenge: ", style="bright_cyan")
    avg_time = stats['total_time'] / stats['attempted'] if stats['attempted'] > 0 else 0
    stats_text.append(f"{avg_time:.2f} seconds", style="bold yellow")
    
    console.print(Panel(stats_text, title="📊 Your Performance", border_style="bright_blue"))
    
    # Achievement message
    if stats['solved'] >= 5:
        achievement = "🏆 Coding Master!"
    elif stats['solved'] >= 3:
        achievement = "⭐ Speed Coder!"
    elif stats['solved'] >= 1:
        achievement = "🔥 Getting Started!"
    else:
        achievement = "🌱 Keep Practicing!"
    
    console.print(Panel(f"[bold bright_yellow]{achievement}[/bold bright_yellow]", 
                       border_style="bright_green"))
    
    console.print("\n[italic dim]Press Enter to return to the main menu...[/italic dim]")
    input()

def run_arcade_mode(console: Console, db: 'DatabaseManager', validator: 'ChallengeValidator', username: str) -> None:
    """Interactive arcade / speedrun mode for quick coding practice."""
    
    # Clear screen and show arcade title
    console.clear()
    arcade_title = Text("🎮 PYMASTER ARCADE MODE 🎮", style="bold magenta")
    console.print(Panel(arcade_title, border_style="bright_magenta"))
    
    # Get duration
    console.print("[bold bright_cyan]Select your coding sprint duration:[/bold bright_cyan]")
    console.print("1. ⚡ 3 minutes (Beginner)")
    console.print("2. 💥 5 minutes (Intermediate)")
    console.print("3. 🚀 10 minutes (Advanced)")
    
    duration_choice = Prompt.ask("[bold bright_yellow]Choose duration[/bold bright_yellow]", 
                                choices=["1", "2", "3"], default="2")
    
    duration_map = {"1": 180, "2": 300, "3": 600}  # in seconds
    duration = duration_map[duration_choice]
    
    # Initialize game state
    challenges = create_arcade_challenges()
    start_time = time.time()
    attempted = 0
    solved = 0
    current_streak = 0
    best_streak = 0
    total_time = 0.0
    challenge_times = []
    
    console.print(f"\n[bold bright_green]🏁 Starting {duration//60}-minute coding sprint![/bold bright_green]")
    console.print("[dim]Press Ctrl+C at any time to exit early[/dim]")
    input("\nPress Enter to begin...")
    
    # Main arcade loop
    try:
        while time.time() - start_time < duration:
            remaining_time = duration - (time.time() - start_time)
            if remaining_time <= 0:
                break
                
            # Select random challenge
            challenge = random.choice(challenges)
            
            # Display round info
            console.clear()
            round_title = Text(f"🕹️  ROUND {attempted + 1}", style="bold bright_blue")
            console.print(Panel(round_title, border_style="bright_blue"))
            
            # Show stats
            stats_text = Text()
            stats_text.append(f"⏱️  Time Remaining: ", style="bright_yellow")
            stats_text.append(f"{remaining_time:.0f}s\n", style="bold white")
            stats_text.append(f"🔥 Current Streak: ", style="bright_yellow")
            stats_text.append(f"{current_streak}\n", style="bold white")
            stats_text.append(f"✅ Solved: ", style="bright_yellow")
            stats_text.append(f"{solved}/{attempted} challenges\n", style="bold white")
            
            if attempted > 0:
                avg_time = sum(challenge_times) / len(challenge_times)
                stats_text.append(f"⏱️  Avg Time: ", style="bright_yellow")
                stats_text.append(f"{avg_time:.2f}s/challenge", style="bold white")
            
            console.print(Panel(stats_text, border_style="bright_green"))
            
            # Run the challenge
            passed, exec_time, feedback = run_arcade_challenge(console, validator, challenge)
            
            # Update stats
            attempted += 1
            total_time += exec_time
            challenge_times.append(exec_time)
            
            if passed:
                solved += 1
                current_streak += 1
                best_streak = max(best_streak, current_streak)
                console.print("[bold green]✅ Challenge completed![/bold green]")
            else:
                current_streak = 0
                console.print("[bold red]❌ Challenge failed.[/bold red]")
            
            # Save result to database
            result = ChallengeResult(
                challenge_id=challenge.id,
                user_code="",  # We don't store user code in arcade mode for privacy
                passed=passed,
                syntax_valid=True,
                performance_score=1.0 if passed else 0.0,
                pep8_score=1.0 if passed else 0.0,
                execution_time=exec_time,
                feedback=feedback
            )
            db.save_challenge_result(result, username)
            
            # Pause before next round
            if time.time() - start_time < duration:
                console.print("\n[bold bright_cyan]Preparing next challenge...[/bold bright_cyan]")
                time.sleep(2)
    
    except KeyboardInterrupt:
        console.print("\n\n[yellow] Arcade mode interrupted by user.[/yellow]")
    
    # Show summary
    final_stats = {
        'duration': time.time() - start_time,
        'attempted': attempted,
        'solved': solved,
        'best_streak': best_streak,
        'total_time': total_time
    }
    
    show_arcade_summary(console, final_stats, username)
