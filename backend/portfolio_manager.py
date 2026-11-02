"""
Portfolio Data Manager
Handles all portfolio data operations with JSON persistence.

This module provides a PortfolioManager class that manages:
- Skills and progress tracking
- Projects
- Learning log entries
- Contact form submissions
- Analytics and reporting
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any


class PortfolioManager:
    """
    Manages portfolio data with CRUD operations and JSON persistence.
    
    Attributes:
        data_file (str): Path to the JSON data file
        data (dict): In-memory portfolio data
    """
    
    def __init__(self, data_file: str = 'data/portfolio.json'):
        """
        Initialize the PortfolioManager.
        
        Args:
            data_file: Path to the JSON file for data persistence
        """
        self.data_file = data_file
        self._ensure_data_directory()
        self.data = self._load_data()
    
    def _ensure_data_directory(self) -> None:
        """Create data directory if it doesn't exist."""
        directory = Path(self.data_file).parent
        directory.mkdir(parents=True, exist_ok=True)
    
    def _load_data(self) -> Dict[str, Any]:
        """
        Load portfolio data from JSON file.
        
        Returns:
            Dictionary containing portfolio data
        """
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    print(f"✅ Loaded data from {self.data_file}")
                    return data
            except json.JSONDecodeError as e:
                print(f"⚠️ Corrupted JSON file: {e}")
                print("📁 Creating new portfolio data file...")
                return self._create_default_data()
            except Exception as e:
                print(f"❌ Error loading data: {e}")
                return self._create_default_data()
        else:
            print(f"📁 Creating new portfolio data file: {self.data_file}")
            return self._create_default_data()
    
    def _create_default_data(self) -> Dict[str, Any]:
        """
        Create and save default portfolio data structure.
        
        Returns:
            Dictionary containing default portfolio data
        """
        default_data = {
            "personal_info": {
                "name": "Your Name",
                "title": "Cloud Developer in Training",
                "bio": "Learning essential languages for cloud computing",
                "email": "your.email@example.com",
                "github": "https://github.com/yourusername",
                "linkedin": "https://linkedin.com/in/yourprofile"
            },
            "skills": [
                {"name": "English", "level": 100, "category": "Communication", "status": "Completed"},
                {"name": "Mathematics", "level": 100, "category": "Logic", "status": "Completed"},
                {"name": "HTML", "level": 100, "category": "Markup", "status": "Completed"},
                {"name": "CSS", "level": 100, "category": "Styling", "status": "Completed"},
                {"name": "JavaScript", "level": 75, "category": "Programming", "status": "Learning"},
                {"name": "Python", "level": 75, "category": "Programming", "status": "Learning"},
                {"name": "Java", "level": 0, "category": "Programming", "status": "Upcoming"},
                {"name": "Linux", "level": 0, "category": "Systems", "status": "Upcoming"},
                {"name": "SQL", "level": 0, "category": "Database", "status": "Upcoming"},
                {"name": "Kubernetes", "level": 0, "category": "DevOps", "status": "Upcoming"},
                {"name": "Git", "level": 0, "category": "Version Control", "status": "Upcoming"}
            ],
            "projects": [
                {
                    "id": 1,
                    "name": "Portfolio Website",
                    "description": "Interactive portfolio built while learning cloud languages",
                    "technologies": ["HTML", "CSS", "JavaScript", "Python", "Flask"],
                    "status": "In Progress",
                    "github_url": "",
                    "live_url": "",
                    "created_at": datetime.now().isoformat()
                }
            ],
            "learning_log": [
                {
                    "date": datetime.now().isoformat(),
                    "day": 6,
                    "topic": "Python Basics",
                    "entry": "Started learning Python for backend development and cloud automation"
                }
            ],
            "contact_messages": []
        }
        
        self._save_data(default_data)
        return default_data
    
    def _save_data(self, data: Optional[Dict[str, Any]] = None) -> bool:
        """
        Save portfolio data to JSON file.
        
        Args:
            data: Data to save (uses self.data if None)
            
        Returns:
            True if save was successful, False otherwise
        """
        data_to_save = data if data is not None else self.data
        
        try:
            with open(self.data_file, 'w', encoding='utf-8') as file:
                json.dump(data_to_save, file, indent=2, ensure_ascii=False)
            print(f"💾 Data saved to {self.data_file}")
            return True
        except Exception as e:
            print(f"❌ Error saving data: {e}")
            return False
    
    # ==================== SKILL OPERATIONS ====================
    
    def get_all_skills(self) -> List[Dict[str, Any]]:
        """
        Get all skills.
        
        Returns:
            List of skill dictionaries
        """
        return self.data.get("skills", [])
    
    def get_skill(self, skill_name: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific skill by name (case-insensitive).
        
        Args:
            skill_name: Name of the skill to find
            
        Returns:
            Skill dictionary if found, None otherwise
        """
        for skill in self.data.get("skills", []):
            if skill["name"].lower() == skill_name.lower():
                return skill
        return None
    
    def update_skill_progress(self, skill_name: str, new_level: int) -> bool:
        """
        Update a skill's progress level.
        
        Args:
            skill_name: Name of the skill to update
            new_level: New progress level (0-100)
            
        Returns:
            True if update was successful, False if skill not found
            
        Raises:
            ValueError: If level is not between 0 and 100
        """
        if not isinstance(new_level, int) or not 0 <= new_level <= 100:
            raise ValueError("Level must be an integer between 0 and 100")
        
        for skill in self.data.get("skills", []):
            if skill["name"].lower() == skill_name.lower():
                old_level = skill["level"]
                skill["level"] = new_level
                skill["last_updated"] = datetime.now().isoformat()
                
                # Update status based on level
                if new_level >= 75:
                    skill["status"] = "Completed"
                elif new_level > 0:
                    skill["status"] = "Learning"
                else:
                    skill["status"] = "Upcoming"
                
                # Log the progress update
                self.add_learning_log(
                    entry=f"Updated {skill_name} progress from {old_level}% to {new_level}%",
                    topic=skill_name
                )
                
                self._save_data()
                return True
        
        return False
    
    def get_skills_by_category(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Group skills by category.
        
        Returns:
            Dictionary with category names as keys and lists of skills as values
        """
        categories: Dict[str, List[Dict[str, Any]]] = {}
        
        for skill in self.data.get("skills", []):
            category = skill.get("category", "Other")
            if category not in categories:
                categories[category] = []
            categories[category].append(skill)
        
        return categories
    
    def get_skills_by_status(self, status: str) -> List[Dict[str, Any]]:
        """
        Get skills filtered by status.
        
        Args:
            status: Status to filter by (Completed, Learning, Upcoming)
            
        Returns:
            List of skills matching the status
        """
        return [
            skill for skill in self.data.get("skills", [])
            if skill.get("status", "").lower() == status.lower()
        ]
    
    # ==================== PROJECT OPERATIONS ====================
    
    def get_all_projects(self) -> List[Dict[str, Any]]:
        """
        Get all projects.
        
        Returns:
            List of project dictionaries
        """
        return self.data.get("projects", [])
    
    def get_project(self, project_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific project by ID.
        
        Args:
            project_id: ID of the project to find
            
        Returns:
            Project dictionary if found, None otherwise
        """
        for project in self.data.get("projects", []):
            if project.get("id") == project_id:
                return project
        return None
    
    def add_project(
        self,
        name: str,
        description: str,
        technologies: List[str],
        status: str = "In Progress"
    ) -> Dict[str, Any]:
        """
        Add a new project.
        
        Args:
            name: Project name
            description: Project description
            technologies: List of technologies used
            status: Project status (default: "In Progress")
            
        Returns:
            The created project dictionary
        """
        # Generate new ID
        existing_ids = [p.get("id", 0) for p in self.data.get("projects", [])]
        new_id = max(existing_ids, default=0) + 1
        
        project = {
            "id": new_id,
            "name": name,
            "description": description,
            "technologies": technologies,
            "status": status,
            "github_url": "",
            "live_url": "",
            "created_at": datetime.now().isoformat()
        }
        
        if "projects" not in self.data:
            self.data["projects"] = []
        
        self.data["projects"].append(project)
        self._save_data()
        
        return project
    
    # ==================== LEARNING LOG ====================
    
    def add_learning_log(
        self,
        entry: str,
        topic: Optional[str] = None,
        day: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Add an entry to the learning log.
        
        Args:
            entry: Log entry text
            topic: Topic of the entry (optional)
            day: Day number (auto-calculated if not provided)
            
        Returns:
            The created log entry dictionary
        """
        if "learning_log" not in self.data:
            self.data["learning_log"] = []
        
        log_entry = {
            "date": datetime.now().isoformat(),
            "day": day if day is not None else len(self.data["learning_log"]) + 1,
            "topic": topic or "General",
            "entry": entry
        }
        
        self.data["learning_log"].append(log_entry)
        self._save_data()
        
        return log_entry
    
    def get_learning_log(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get learning log entries.
        
        Args:
            limit: Maximum number of entries to return (returns last N entries)
            
        Returns:
            List of log entry dictionaries
        """
        logs = self.data.get("learning_log", [])
        
        if limit is not None and limit > 0:
            return logs[-limit:]
        
        return logs
    
    # ==================== CONTACT MESSAGES ====================
    
    def save_contact_message(
        self,
        name: str,
        email: str,
        message: str,
        subject: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Save a contact form submission.
        
        Args:
            name: Sender's name
            email: Sender's email
            message: Message content
            subject: Message subject (optional)
            
        Returns:
            The created contact message dictionary
        """
        if "contact_messages" not in self.data:
            self.data["contact_messages"] = []
        
        # Generate new ID
        existing_ids = [m.get("id", 0) for m in self.data["contact_messages"]]
        new_id = max(existing_ids, default=0) + 1
        
        contact = {
            "id": new_id,
            "name": name,
            "email": email,
            "subject": subject or "No Subject",
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "read": False
        }
        
        self.data["contact_messages"].append(contact)
        self._save_data()
        
        return contact
    
    def get_contact_messages(
        self,
        unread_only: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Get contact messages.
        
        Args:
            unread_only: If True, return only unread messages
            
        Returns:
            List of contact message dictionaries
        """
        messages = self.data.get("contact_messages", [])
        
        if unread_only:
            return [m for m in messages if not m.get("read", False)]
        
        return messages
    
    # ==================== ANALYTICS ====================
    
    def generate_progress_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive progress report.
        
        Returns:
            Dictionary containing various analytics metrics
        """
        skills = self.data.get("skills", [])
        
        if not skills:
            return {
                "total_skills": 0,
                "completed_skills": 0,
                "learning_skills": 0,
                "upcoming_skills": 0,
                "average_progress": 0,
                "completion_rate": 0,
                "total_projects": 0,
                "learning_log_entries": 0,
                "contact_messages": 0
            }
        
        total_skills = len(skills)
        completed = len([s for s in skills if s.get("level", 0) >= 75])
        learning = len([s for s in skills if 0 < s.get("level", 0) < 75])
        upcoming = len([s for s in skills if s.get("level", 0) == 0])
        
        total_progress = sum(s.get("level", 0) for s in skills)
        average_progress = total_progress / total_skills if total_skills > 0 else 0
        completion_rate = (completed / total_skills * 100) if total_skills > 0 else 0
        
        return {
            "total_skills": total_skills,
            "completed_skills": completed,
            "learning_skills": learning,
            "upcoming_skills": upcoming,
            "average_progress": round(average_progress, 1),
            "completion_rate": round(completion_rate, 1),
            "total_projects": len(self.data.get("projects", [])),
            "learning_log_entries": len(self.data.get("learning_log", [])),
            "contact_messages": len(self.data.get("contact_messages", []))
        }
    
    # ==================== PERSONAL INFO ====================
    
    def get_personal_info(self) -> Dict[str, str]:
        """
        Get personal information.
        
        Returns:
            Dictionary containing personal info
        """
        return self.data.get("personal_info", {})
    
    def update_personal_info(self, **kwargs) -> Dict[str, str]:
        """
        Update personal information.
        
        Args:
            **kwargs: Key-value pairs to update
            
        Returns:
            Updated personal info dictionary
        """
        if "personal_info" not in self.data:
            self.data["personal_info"] = {}
        
        for key, value in kwargs.items():
            if value is not None:
                self.data["personal_info"][key] = value
        
        self._save_data()
        return self.data["personal_info"]


# ==================== TESTING ====================

if __name__ == "__main__":
    """Test the PortfolioManager when run directly."""
    
    print("\n" + "=" * 50)
    print("🧪 Testing PortfolioManager")
    print("=" * 50)
    
    # Create manager instance
    manager = PortfolioManager()
    
    # Test 1: Get all skills
    print("\n📋 All Skills:")
    skills = manager.get_all_skills()
    for skill in skills:
        status_emoji = "✅" if skill["level"] >= 75 else "⏳" if skill["level"] > 0 else "📅"
        print(f"  {status_emoji} {skill['name']}: {skill['level']}%")
    
    # Test 2: Update a skill
    print("\n📊 Updating Python skill to 80%...")
    success = manager.update_skill_progress("Python", 80)
    print(f"  Result: {'Success' if success else 'Failed'}")
    
    # Test 3: Get skills by category
    print("\n🎯 Skills by Category:")
    by_category = manager.get_skills_by_category()
    for category, cat_skills in by_category.items():
        print(f"\n  {category}:")
        for skill in cat_skills:
            print(f"    - {skill['name']}: {skill['level']}%")
    
    # Test 4: Generate progress report
    print("\n📈 Progress Report:")
    report = manager.generate_progress_report()
    for key, value in report.items():
        print(f"  {key}: {value}")
    
    # Test 5: Add a learning log entry
    print("\n📝 Adding learning log entry...")
    log = manager.add_learning_log(
        entry="Tested PortfolioManager class successfully",
        topic="Python Testing"
    )
    print(f"  Added: {log['entry']}")
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")
    print("=" * 50 + "\n")