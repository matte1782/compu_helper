# pymaster_quests.py

import json
import os
import sqlite3
from typing import Dict, List, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from datetime import datetime

# Quest campaign data
ZONES = {
    "green_valley": {
        "name": "Green Valley 🌱",
        "color": "green",
        "emoji": "🌱",
        "description": "Master the fundamentals of Python programming",
        "steps": [
            {
                "id": "gv_step1",
                "title": "The First Function",
                "description": "Write your first Python function to add two numbers together.",
                "challenge_id": "core_001",
                "narrative": "Welcome to Green Valley, young programmer! Your journey begins with the most fundamental concept - functions. Create a function that takes two parameters and returns their sum."
            },
            {
                "id": "gv_step2",
                "title": "String Manipulation",
                "description": "Process text strings to extract specific information.",
                "challenge_id": None,  # Placeholder for future challenge
                "narrative": "In the meadows of Green Valley, you encounter ancient texts that need processing. Your task is to manipulate strings to extract meaningful information."
            },
            {
                "id": "gv_step3",
                "title": "List Basics",
                "description": "Work with lists to store and manipulate collections of data.",
                "challenge_id": None,  # Placeholder for future challenge
                "narrative": "The villagers of Green Valley need help organizing their harvest. Use your list skills to manage collections of fruits and vegetables."
            }
        ]
    },
    "azure_city": {
        "name": "Azure City 🏙️",
        "color": "cyan",
        "emoji": "🏙️",
        "description": "Dive into data structures and advanced list operations",
        "steps": [
            {
                "id": "ac_step1",
                "title": "List Comprehensions",
                "description": "Use list comprehensions to filter and transform data efficiently.",
                "challenge_id": "ds_001",
                "narrative": "Welcome to the technological heart of Python land - Azure City! Here, efficiency is key. Master list comprehensions to process data like a pro."
            },
            {
                "id": "ac_step2",
                "title": "Dictionary Operations",
                "description": "Manipulate dictionaries to store key-value relationships.",
                "challenge_id": None,  # Placeholder for future challenge
                "narrative": "The city's database systems require your expertise with dictionaries. Organize citizen records using key-value pairs."
            },
            {
                "id": "ac_step3",
                "title": "Data Processing Challenge",
                "description": "Combine multiple data structures to solve a complex problem.",
                "challenge_id": None,  # Placeholder for future challenge
                "narrative": "The mayor of Azure City has a special task for you. Process complex datasets using all the skills you've learned."
            }
        ]
    },
    "scarlet_tower": {
        "name": "Scarlet Tower 🗼",
        "color": "red",
        "emoji": "🗼",
        "description": "Conquer object-oriented programming and class design",
        "steps": [
            {
                "id": "st_step1",
                "title": "Class Creation",
                "description": "Design and implement your first Python class.",
                "challenge_id": "oop_001",
                "narrative": "At the top of Scarlet Tower, you'll master the art of Object-Oriented Programming. Begin by creating your first class with attributes and methods."
            },
            {
                "id": "st_step2",
                "title": "Inheritance",
                "description": "Use inheritance to create specialized classes.",
                "challenge_id": None,  # Placeholder for future challenge
                "narrative": "The ancient wizards of Scarlet Tower used inheritance to pass down magical knowledge. Create class hierarchies to organize your code."
            },
            {
                "id": "st_step3",
                "title": "Design Patterns",
                "description": "Implement common design patterns in Python.",
                "challenge_id": None,  # Placeholder for future challenge
                "narrative": "Your final challenge in Scarlet Tower is to implement proven design patterns that make your code robust and maintainable."
            }
        ]
    }
}

def init_campaign_database(db_path: str):
    """Initialize the campaign progress table in the database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS campaign_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            zone_id TEXT NOT NULL,
            step_id TEXT NOT NULL,
            completed BOOLEAN DEFAULT FALSE,
            completed_at TIMESTAMP,
            UNIQUE(user_id, zone_id, step_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_user_progress(db_path: str, username: str) -> Dict[str, List[str]]:
    """Get user's campaign progress from database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT zone_id, step_id FROM campaign_progress 
        WHERE user_id = ? AND completed = 1
    ''', (username,))
    
    rows = cursor.fetchall()
    conn.close()
    
    progress = {}
    for zone_id, step_id in rows:
        if zone_id not in progress:
            progress[zone_id] = []
        progress[zone_id].append(step_id)
    
    return progress

def mark_step_completed(db_path: str, username: str, zone_id: str, step_id: str):
    """Mark a quest step as completed"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR REPLACE INTO campaign_progress 
        (user_id, zone_id, step_id, completed, completed_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, zone_id, step_id, True, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()

def is_step_completed(progress: Dict[str, List[str]], zone_id: str, step_id: str) -> bool:
    """Check if a specific step is completed"""
    return zone_id in progress and step_id in progress[zone_id]

def is_zone_unlocked(progress: Dict[str, List[str]], zone_id: str) -> bool:
    """Check if a zone is unlocked (first zone always unlocked)"""
    if zone_id == "green_valley":
        return True
    
    # Define unlock requirements
    unlock_requirements = {
        "azure_city": ("green_valley", 1),  # Need 1 completed step in Green Valley
        "scarlet_tower": ("azure_city", 1)   # Need 1 completed step in Azure City
    }
    
    if zone_id not in unlock_requirements:
        return False
        
    required_zone, required_steps = unlock_requirements[zone_id]
    return (required_zone in progress and 
            len(progress[required_zone]) >= required_steps)

def show_campaign_map(console: Console, progress: Dict[str, List[str]]):
    """Display the campaign map with zone statuses"""
    console.clear()
    
    title = Text("🗺️ QUEST CAMPAIGN MAP 🗺️", style="bold magenta")
    console.print(Panel(title, border_style="bright_magenta"))
    
    for zone_id, zone_data in ZONES.items():
        # Determine zone status
        if is_zone_unlocked(progress, zone_id):
            status = "✅ UNLOCKED"
            status_style = "bold green"
        else:
            status = "🔒 LOCKED"
            status_style = "bold red"
        
        # Count completed steps
        completed_steps = len(progress.get(zone_id, []))
        total_steps = len(zone_data["steps"])
        
        # Create zone panel
        zone_text = Text()
        zone_text.append(f"{zone_data['emoji']} {zone_data['name']}\n", style=f"bold {zone_data['color']}")
        zone_text.append(f"{zone_data['description']}\n\n", style="white")
        zone_text.append(f"Progress: {completed_steps}/{total_steps} steps completed\n", style="cyan")
        zone_text.append(status, style=status_style)
        
        console.print(Panel(zone_text, border_style=zone_data['color']))
    
    console.print(Panel("🧭 [bold cyan]Navigate through zones to complete quests![/bold cyan]", 
                       border_style="blue"))

def show_zone_details(console: Console, zone_id: str, progress: Dict[str, List[str]]):
    """Show details for a specific zone"""
    if zone_id not in ZONES:
        console.print("[red]Invalid zone selected.[/red]")
        return
    
    zone_data = ZONES[zone_id]
    console.clear()
    
    # Zone header
    title = Text(f"{zone_data['emoji']} {zone_data['name']} {zone_data['emoji']}", 
                 style=f"bold {zone_data['color']}")
    console.print(Panel(title, border_style=zone_data['color']))
    
    # Zone description
    console.print(Panel(zone_data['description'], border_style=zone_data['color']))
    
    # Steps table
    table = Table(title="📜 Quest Steps", border_style=zone_data['color'])
    table.add_column("Step", style="cyan", justify="right")
    table.add_column("Title", style="white")
    table.add_column("Status", style="white")
    table.add_column("Description", style="dim")
    
    for i, step in enumerate(zone_data['steps'], 1):
        # Determine step status
        if is_step_completed(progress, zone_id, step['id']):
            status = "✅ Completed"
            status_style = "bold green"
        elif i == 1 or is_step_completed(progress, zone_id, zone_data['steps'][i-2]['id']):
            status = "🔄 In Progress"
            status_style = "bold yellow"
        else:
            status = "🔒 Locked"
            status_style = "bold red"
        
        table.add_row(
            str(i),
            step['title'],
            status,
            step['description']
        )
    
    console.print(table)
    
    # Zone progress
    completed_steps = len(progress.get(zone_id, []))
    total_steps = len(zone_data['steps'])
    progress_text = Text(f"\nProgress: {completed_steps}/{total_steps} steps completed", style="bold cyan")
    console.print(progress_text)

def show_step_details(console: Console, zone_id: str, step_index: int, progress: Dict[str, List[str]]):
    """Show details for a specific step"""
    if zone_id not in ZONES:
        console.print("[red]Invalid zone selected.[/red]")
        return
    
    zone_data = ZONES[zone_id]
    if step_index < 0 or step_index >= len(zone_data['steps']):
        console.print("[red]Invalid step selected.[/red]")
        return
    
    step = zone_data['steps'][step_index]
    
    # Check if step is unlocked
    if step_index > 0 and not is_step_completed(progress, zone_id, zone_data['steps'][step_index-1]['id']):
        console.print("[red]🔒 This step is locked. Complete the previous step first.[/red]")
        return
    
    console.clear()
    
    # Step header
    title = Text(f"Step {step_index + 1}: {step['title']}", style=f"bold {zone_data['color']}")
    console.print(Panel(title, border_style=zone_data['color']))
    
    # Narrative
    narrative = Text(step['narrative'], style="italic white")
    console.print(Panel(narrative, title="📖 Quest Narrative", border_style=zone_data['color']))
    
    # Objective
    objective = Text(step['description'], style="bold white")
    console.print(Panel(objective, title="🎯 Objective", border_style="blue"))
    
    # Challenge information
    if step['challenge_id']:
        challenge_info = Text(f"To complete this quest step, go to the main menu and select:\n", style="white")
        challenge_info.append(f"Start Challenge → Find challenge with ID: ", style="cyan")
        challenge_info.append(f"{step['challenge_id']}\n\n", style="bold yellow")
        challenge_info.append("After completing the challenge, return here and mark this step as completed.", style="white")
        console.print(Panel(challenge_info, title="⚡ How to Proceed", border_style="green"))
    else:
        console.print(Panel("This quest step will be available in a future update!", 
                           title="🚧 Coming Soon", border_style="yellow"))
    
    # Status
    if is_step_completed(progress, zone_id, step['id']):
        status = Text("✅ This step is already completed!", style="bold green")
    elif step_index == 0 or is_step_completed(progress, zone_id, zone_data['steps'][step_index-1]['id']):
        status = Text("🔄 This step is ready to be completed", style="bold yellow")
    else:
        status = Text("🔒 This step is locked", style="bold red")
    
    console.print(Panel(status, border_style=zone_data['color']))

def mark_step_as_completed_ui(console: Console, db_path: str, username: str, zone_id: str, step_index: int, progress: Dict[str, List[str]]):
    """UI flow to mark a step as completed"""
    if zone_id not in ZONES:
        console.print("[red]Invalid zone selected.[/red]")
        return progress
    
    zone_data = ZONES[zone_id]
    if step_index < 0 or step_index >= len(zone_data['steps']):
        console.print("[red]Invalid step selected.[/red]")
        return progress
    
    step = zone_data['steps'][step_index]
    
    # Check if step is already completed
    if is_step_completed(progress, zone_id, step['id']):
        console.print("[yellow]This step is already marked as completed.[/yellow]")
        return progress
    
    # Check if step is unlocked
    if step_index > 0 and not is_step_completed(progress, zone_id, zone_data['steps'][step_index-1]['id']):
        console.print("[red]🔒 This step is locked. Complete the previous step first.[/red]")
        return progress
    
    # Confirm completion
    console.print(f"[bold yellow]Mark '{step['title']}' as completed?[/bold yellow]")
    choice = Prompt.ask("Enter 'y' to confirm or any other key to cancel", default="n")
    
    if choice.lower() == 'y':
        mark_step_completed(db_path, username, zone_id, step['id'])
        console.print("[green]✅ Step marked as completed![/green]")
        
        # Update progress in memory
        if zone_id not in progress:
            progress[zone_id] = []
        progress[zone_id].append(step['id'])
        
        # Pause to let user see the confirmation
        input("\nPress Enter to continue...")
    
    return progress

def run_quest_campaign(console: Console, db: 'DatabaseManager', validator: 'ChallengeValidator', username: str) -> None:
    """Interactive quest/campaign mode for PyMaster."""
    
    # Initialize campaign database
    init_campaign_database(db.db_path)
    
    # Get user progress
    progress = get_user_progress(db.db_path, username)
    
    while True:
        show_campaign_map(console, progress)
        
        # Menu options
        console.print("\n[bold cyan]=== Quest Campaign Menu ===[/bold cyan]")
        console.print("1. View Zone Details")
        console.print("2. View Step Details")
        console.print("3. Mark Step as Completed")
        console.print("4. Return to Main Menu")
        
        choice = Prompt.ask("[bold yellow]Select an option[/bold yellow]", 
                           choices=["1", "2", "3", "4"], default="4")
        
        if choice == "1":
            # View zone details
            zone_choices = list(ZONES.keys())
            console.print("\n[bold]Available Zones:[/bold]")
            for i, zone_id in enumerate(zone_choices, 1):
                zone_name = ZONES[zone_id]['name']
                if is_zone_unlocked(progress, zone_id):
                    status = "✅"
                else:
                    status = "🔒"
                console.print(f"{i}. {status} {zone_name}")
            
            try:
                zone_idx = int(Prompt.ask("Select a zone", 
                                        choices=[str(i) for i in range(1, len(zone_choices)+1)])) - 1
                selected_zone = zone_choices[zone_idx]
                
                if not is_zone_unlocked(progress, selected_zone):
                    console.print("[red]🔒 This zone is locked. Complete previous zones to unlock it.[/red]")
                    input("\nPress Enter to continue...")
                    continue
                
                show_zone_details(console, selected_zone, progress)
                input("\nPress Enter to continue...")
            except (ValueError, IndexError):
                console.print("[red]Invalid selection.[/red]")
                input("\nPress Enter to continue...")
        
        elif choice == "2":
            # View step details
            zone_choices = [zone_id for zone_id in ZONES.keys() if is_zone_unlocked(progress, zone_id)]
            if not zone_choices:
                console.print("[red]No zones are currently unlocked.[/red]")
                input("\nPress Enter to continue...")
                continue
            
            console.print("\n[bold]Available Zones:[/bold]")
            for i, zone_id in enumerate(zone_choices, 1):
                zone_name = ZONES[zone_id]['name']
                console.print(f"{i}. {zone_name}")
            
            try:
                zone_idx = int(Prompt.ask("Select a zone", 
                                        choices=[str(i) for i in range(1, len(zone_choices)+1)])) - 1
                selected_zone = zone_choices[zone_idx]
                
                zone_data = ZONES[selected_zone]
                console.print(f"\n[bold]Steps in {zone_data['name']}:[/bold]")
                for i, step in enumerate(zone_data['steps'], 1):
                    console.print(f"{i}. {step['title']}")
                
                step_idx = int(Prompt.ask("Select a step", 
                                        choices=[str(i) for i in range(1, len(zone_data['steps'])+1)])) - 1
                
                show_step_details(console, selected_zone, step_idx, progress)
                input("\nPress Enter to continue...")
            except (ValueError, IndexError):
                console.print("[red]Invalid selection.[/red]")
                input("\nPress Enter to continue...")
        
        elif choice == "3":
            # Mark step as completed
            zone_choices = [zone_id for zone_id in ZONES.keys() if is_zone_unlocked(progress, zone_id)]
            if not zone_choices:
                console.print("[red]No zones are currently unlocked.[/red]")
                input("\nPress Enter to continue...")
                continue
            
            console.print("\n[bold]Available Zones:[/bold]")
            for i, zone_id in enumerate(zone_choices, 1):
                zone_name = ZONES[zone_id]['name']
                console.print(f"{i}. {zone_name}")
            
            try:
                zone_idx = int(Prompt.ask("Select a zone", 
                                        choices=[str(i) for i in range(1, len(zone_choices)+1)])) - 1
                selected_zone = zone_choices[zone_idx]
                
                zone_data = ZONES[selected_zone]
                console.print(f"\n[bold]Steps in {zone_data['name']}:[/bold]")
                for i, step in enumerate(zone_data['steps'], 1):
                    if is_step_completed(progress, selected_zone, step['id']):
                        status = "✅"
                    elif i == 1 or is_step_completed(progress, selected_zone, zone_data['steps'][i-2]['id']):
                        status = "🔄"
                    else:
                        status = "🔒"
                    console.print(f"{i}. {status} {step['title']}")
                
                step_idx = int(Prompt.ask("Select a step to mark as completed", 
                                        choices=[str(i) for i in range(1, len(zone_data['steps'])+1)])) - 1
                
                progress = mark_step_as_completed_ui(console, db.db_path, username, selected_zone, step_idx, progress)
            except (ValueError, IndexError):
                console.print("[red]Invalid selection.[/red]")
                input("\nPress Enter to continue...")
        
        elif choice == "4":
            # Return to main menu
            break
