# pymaster_gamification.py

from typing import List, Dict, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
import sqlite3

# Badge definitions
BADGES = {
    "first_blood": {"name": "First Blood ⚡", "description": "Complete your first challenge", "emoji": "⚡"},
    "streak_starter": {"name": "Streak Starter 🔥", "description": "Attempt 3 or more challenges", "emoji": "🔥"},
    "style_seeker": {"name": "Style Seeker ✨", "description": "Score over 80% on PEP8", "emoji": "✨"},
    "speed_demon": {"name": "Speed Demon 🏎️", "description": "Execution time under 0.5s", "emoji": "🏎️"},
    "perfectionist": {"name": "Perfectionist 🎯", "description": "Pass a challenge with 100% scores", "emoji": "🎯"},
    "level_up": {"name": "Level Up! 📈", "description": "Reach level 2 or higher", "emoji": "📈"},
}

def calculate_xp(challenge_results: List[Dict[str, Any]]) -> int:
    """Calculate total XP based on challenge results"""
    xp = 0
    for result in challenge_results:
        xp += 10  # Base XP for attempt
        if result.get('passed'):
            xp += 40  # Bonus for passing
        # Bonus for high scores
        if result.get('pep8_score', 0) > 0.8:
            xp += 10
        if result.get('performance_score', 0) > 0.8:
            xp += 10
    return xp

def get_level_from_xp(xp: int) -> int:
    """Convert XP to level"""
    return 1 + xp // 100

def get_xp_for_next_level(level: int) -> int:
    """Get XP required for next level"""
    return level * 100

def get_xp_progress_in_level(xp: int, level: int) -> int:
    """Get XP progress within current level"""
    return xp % 100

def create_progress_bar(progress: int, total: int, width: int = 20) -> str:
    """Create a visual progress bar"""
    filled = int((progress / total) * width) if total > 0 else 0
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {progress}/{total}"

def get_user_badges(challenge_results: List[Dict[str, Any]], level: int) -> List[str]:
    """Determine which badges user has earned"""
    badges = []
    
    if len(challenge_results) >= 1:
        badges.append("first_blood")
    
    if len(challenge_results) >= 3:
        badges.append("streak_starter")
    
    if level >= 2:
        badges.append("level_up")
    
    # Check for high scores in any challenge
    for result in challenge_results:
        if result.get('pep8_score', 0) > 0.8:
            badges.append("style_seeker")
        if result.get('execution_time', 1) < 0.5:
            badges.append("speed_demon")
        if (result.get('passed') and 
            result.get('pep8_score', 0) >= 1.0 and 
            result.get('performance_score', 0) >= 1.0):
            badges.append("perfectionist")
    
    # Remove duplicates while preserving order
    return list(dict.fromkeys(badges))

def run_gamification_hub(console: Console, db: 'DatabaseManager', username: str) -> None:
    """Render an interactive gamification dashboard for the given user."""
    
    console.clear()
    
    # Title
    title = Text("🎮 GAMIFICATION HUB 🎮", style="bold magenta")
    console.print(Panel(title, border_style="bright_magenta"))
    
    # Get user data
    try:
        # Get all challenge results for this user
        conn = sqlite3.connect(db.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM challenge_results WHERE user_id = ? ORDER BY created_at DESC", 
            (username,)
        )
        raw_challenge_results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
    except Exception as e:
        console.print(Panel(f"Error loading user data: {e}", border_style="red"))
        input("\nPress Enter to return to main menu...")
        return
    
    # Calculate XP and level
    total_xp = calculate_xp(raw_challenge_results)
    current_level = get_level_from_xp(total_xp)
    xp_for_next = get_xp_for_next_level(current_level)
    xp_in_level = get_xp_progress_in_level(total_xp, current_level)
    
    # User stats panel
    stats = db.get_user_stats(username)
    
    stats_text = Text()
    stats_text.append(f"Total Challenges: ", style="cyan")
    stats_text.append(f"{stats['total_challenges']}\n", style="bold white")
    
    stats_text.append(f"Success Rate: ", style="cyan")
    stats_text.append(f"{stats['success_rate']:.1f}%\n", style="bold white")
    
    stats_text.append(f"Average Execution Time: ", style="cyan")
    stats_text.append(f"{stats['avg_execution_time']:.3f}s\n", style="bold white")
    
    stats_text.append(f"Average PEP8 Score: ", style="cyan")
    stats_text.append(f"{stats['avg_pep8_score']:.1f}%\n", style="bold white")
    
    stats_text.append(f"Average Performance Score: ", style="cyan")
    stats_text.append(f"{stats['avg_performance_score']:.1f}%", style="bold white")
    
    console.print(Panel(stats_text, title="📊 Stats Overview", border_style="bright_blue"))
    
    # XP and Level panel
    xp_text = Text()
    xp_text.append(f"Current Level: ", style="green")
    xp_text.append(f"{current_level}\n", style="bold yellow")
    
    xp_text.append(f"Total XP: ", style="green")
    xp_text.append(f"{total_xp}\n", style="bold yellow")
    
    xp_text.append(f"Next Level: ", style="green")
    xp_text.append(f"{xp_for_next} XP\n", style="bold yellow")
    
    progress_bar = create_progress_bar(xp_in_level, 100)
    xp_text.append(f"Progress: ", style="green")
    xp_text.append(f"{progress_bar}", style="bold white")
    
    console.print(Panel(xp_text, title="⭐ Experience Points", border_style="bright_green"))
    
    # Recent activity
    if raw_challenge_results:
        table = Table(title="🕒 Recent Activity", border_style="yellow")
        table.add_column("Challenge ID", style="cyan")
        table.add_column("Passed", style="green")
        table.add_column("PEP8", style="magenta")
        table.add_column("Performance", style="blue")
        table.add_column("Time (s)", style="red")
        table.add_column("Date", style="dim")
        
        # Show last 5 challenges
        for result in raw_challenge_results[:5]:
            passed = "✅" if result.get('passed') else "❌"
            pep8 = f"{result.get('pep8_score', 0) * 100:.0f}%"
            perf = f"{result.get('performance_score', 0) * 100:.0f}%"
            time = f"{result.get('execution_time', 0):.3f}"
            date = result.get('created_at', '')[:19]  # Trim to date only
            
            table.add_row(
                result.get('challenge_id', 'N/A')[:12],  # Truncate long IDs
                passed,
                pep8,
                perf,
                time,
                date
            )
        
        console.print(table)
    else:
        console.print(Panel("No recent activity", title="🕒 Recent Activity", border_style="yellow"))
    
    # Badges section
    earned_badges = get_user_badges(raw_challenge_results, current_level)
    
    if earned_badges:
        badges_text = Text()
        for badge_key in earned_badges:
            badge = BADGES.get(badge_key, {})
            badges_text.append(f"{badge.get('emoji', '🏆')} {badge.get('name', badge_key)}  ", style="bold yellow")
        
        # Add a line break for better formatting
        badges_text.append("\n\n")
        
        # Add descriptions
        for badge_key in earned_badges:
            badge = BADGES.get(badge_key, {})
            badges_text.append(f"{badge.get('emoji')} ", style="yellow")
            badges_text.append(f"{badge.get('name', badge_key)}: ", style="cyan")
            badges_text.append(f"{badge.get('description', '')}\n", style="white")
        
        console.print(Panel(badges_text, title="🏅 Achievements", border_style="bright_yellow"))
    else:
        console.print(Panel("Complete more challenges to earn badges!", 
                           title="🏅 Achievements", border_style="bright_yellow"))
    
    # Footer
    console.print(Panel("Keep coding to earn more XP and unlock achievements!", 
                       border_style="magenta"))
    
    input("\nPress Enter to return to main menu...")
