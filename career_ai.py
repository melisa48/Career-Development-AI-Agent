import os
import json
import re
from datetime import datetime
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox

class CareerDevelopmentAgent:
    """AI agent for assisting with career development tasks."""
    
    def __init__(self):
        """Initialize the Career Development Agent with necessary resources."""
        self.user_profile = {}
        self.resources_path = "resources/"
        self.load_resources()
        
    def load_resources(self):
        """Load career development resources from files."""
        # Ensure resources directory exists
        os.makedirs(self.resources_path, exist_ok=True)
        
        # Create default resources if they don't exist
        self._ensure_resource_exists("job_search_tips.json", {
            "resume_keywords": ["experienced", "skilled", "proficient", "managed", "led", "developed", "improved"],
            "networking_tips": ["Attend industry events", "Connect with alumni", "Engage on LinkedIn", "Join professional groups"],
            "job_boards": ["LinkedIn", "Indeed", "Glassdoor", "Monster", "Company websites", "Industry-specific boards"]
        })
        
        self._ensure_resource_exists("interview_questions.json", {
            "common_questions": [
                "Tell me about yourself",
                "Why are you interested in this position?",
                "What are your strengths and weaknesses?",
                "Describe a challenge you faced and how you overcame it",
                "Where do you see yourself in 5 years?",
                "Why should we hire you?"
            ],
            "technical_topics": {
                "programming": ["Data structures", "Algorithms", "System design", "Problem-solving process"],
                "project_management": ["Risk management", "Agile methodologies", "Stakeholder communication"],
                "marketing": ["Campaign analytics", "SEO knowledge", "Social media strategy"]
            }
        })
        
        self._ensure_resource_exists("career_paths.json", {
            "tech": ["Software Engineer", "Data Scientist", "Product Manager", "UX Designer", "DevOps Engineer"],
            "business": ["Business Analyst", "Financial Analyst", "Management Consultant", "Marketing Specialist"],
            "healthcare": ["Nurse", "Physician Assistant", "Health Informatics", "Healthcare Administrator"]
        })
    
    def _ensure_resource_exists(self, filename, default_content):
        """Create resource file with default content if it doesn't exist."""
        filepath = os.path.join(self.resources_path, filename)
        if not os.path.exists(filepath):
            with open(filepath, 'w') as f:
                json.dump(default_content, f, indent=4)
    
    def load_user_profile(self, filepath):
        """Load user profile from a JSON file."""
        try:
            with open(filepath, 'r') as f:
                self.user_profile = json.load(f)
            return True
        except Exception as e:
            print(f"Error loading profile: {e}")
            return False
    
    def save_user_profile(self, filepath):
        """Save current user profile to a JSON file."""
        try:
            with open(filepath, 'w') as f:
                json.dump(self.user_profile, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving profile: {e}")
            return False
    
    def update_profile(self, key, value):
        """Update a specific field in the user profile."""
        self.user_profile[key] = value
    
    def analyze_resume(self, resume_text):
        """Analyze a resume and provide improvement suggestions."""
        with open(os.path.join(self.resources_path, "job_search_tips.json"), 'r') as f:
            resources = json.load(f)
        
        keywords = resources["resume_keywords"]
        results = {
            "keyword_count": 0,
            "keywords_found": [],
            "missing_keywords": [],
            "suggestions": []
        }
        
        # Check for keywords
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', resume_text, re.IGNORECASE):
                results["keyword_count"] += 1
                results["keywords_found"].append(keyword)
            else:
                results["missing_keywords"].append(keyword)
        
        # Basic suggestions
        if len(resume_text.split()) < 200:
            results["suggestions"].append("Your resume seems short. Consider adding more details about your experience.")
        
        if "objective" not in resume_text.lower() and "summary" not in resume_text.lower():
            results["suggestions"].append("Consider adding a career objective or professional summary.")
        
        if not re.search(r'\b(achieved|accomplishment|improved|increased|decreased|reduced|saved|delivered)\b', resume_text, re.IGNORECASE):
            results["suggestions"].append("Add more achievement-oriented language with measurable results.")
        
        # Calculate basic score
        score = min(100, (results["keyword_count"] / len(keywords)) * 70 + 30)
        results["score"] = round(score)
        
        return results
    
    def get_interview_tips(self, job_title=""):
        """Get interview preparation tips, optionally tailored to a specific job."""
        with open(os.path.join(self.resources_path, "interview_questions.json"), 'r') as f:
            interview_data = json.load(f)
            
        tips = {
            "common_questions": interview_data["common_questions"],
            "preparation_tips": [
                "Research the company thoroughly",
                "Practice your answers out loud",
                "Prepare questions to ask the interviewer",
                "Plan your outfit and travel route in advance",
                "Bring extra copies of your resume"
            ],
            "technical_topics": []
        }
        
        # Add relevant technical topics based on job title
        job_title_lower = job_title.lower()
        if "software" in job_title_lower or "developer" in job_title_lower or "engineer" in job_title_lower:
            tips["technical_topics"] = interview_data["technical_topics"]["programming"]
        elif "project" in job_title_lower or "manager" in job_title_lower:
            tips["technical_topics"] = interview_data["technical_topics"]["project_management"]
        elif "market" in job_title_lower:
            tips["technical_topics"] = interview_data["technical_topics"]["marketing"]
        
        return tips
    
    def suggest_career_paths(self, interests, skills):
        """Suggest potential career paths based on interests and skills."""
        with open(os.path.join(self.resources_path, "career_paths.json"), 'r') as f:
            career_paths = json.load(f)
        
        suggestions = []
        interests_lower = [i.lower() for i in interests]
        skills_lower = [s.lower() for s in skills]
        
        # Simple matching algorithm
        if any(tech_term in interests_lower + skills_lower for tech_term in ["coding", "programming", "software", "computer", "technology", "data"]):
            suggestions.extend(career_paths["tech"])
            
        if any(business_term in interests_lower + skills_lower for business_term in ["business", "finance", "management", "marketing", "sales"]):
            suggestions.extend(career_paths["business"])
            
        if any(health_term in interests_lower + skills_lower for health_term in ["health", "medicine", "care", "patient", "biology"]):
            suggestions.extend(career_paths["healthcare"])
        
        # If no matches, return a mix of options
        if not suggestions:
            for category in career_paths:
                suggestions.append(career_paths[category][0])
        
        return suggestions
    
    def generate_job_search_plan(self, job_title, location, experience_level):
        """Generate a personalized job search plan."""
        with open(os.path.join(self.resources_path, "job_search_tips.json"), 'r') as f:
            resources = json.load(f)
        
        plan = {
            "daily_tasks": [
                "Check new job postings on 2-3 platforms",
                "Send follow-ups on pending applications",
                "Connect with 1-2 new professionals in your field"
            ],
            "weekly_tasks": [
                "Apply to 5-10 relevant positions",
                "Attend one networking event (virtual or in-person)",
                "Update job search tracking document"
            ],
            "resources": {
                "job_boards": resources["job_boards"],
                "networking_opportunities": resources["networking_tips"]
            },
            "timeline": {
                "week1": "Research companies and update resume/LinkedIn",
                "week2": "Begin applications and networking",
                "week3": "Follow up on applications and continue applying",
                "week4": "Begin interview preparations while continuing applications"
            }
        }
        
        # Customize based on experience level
        if experience_level.lower() == "entry":
            plan["daily_tasks"].append("Spend 30 minutes on skill development")
            plan["resources"]["additional"] = ["Entry-level job fairs", "University career services"]
        elif experience_level.lower() == "mid":
            plan["weekly_tasks"].append("Research industry trends to mention in interviews")
            plan["resources"]["additional"] = ["Professional associations", "Industry conferences"]
        elif experience_level.lower() == "senior":
            plan["weekly_tasks"].append("Schedule informational interviews with target companies")
            plan["resources"]["additional"] = ["Executive recruiters", "Industry speaking opportunities"]
        
        return plan


class CareerAgentGUI:
    """GUI interface for the Career Development Agent."""
    
    def __init__(self, root):
        self.root = root
        self.agent = CareerDevelopmentAgent()
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the graphical user interface."""
        self.root.title("Career Development AI Agent")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.profile_tab = ttk.Frame(self.notebook)
        self.resume_tab = ttk.Frame(self.notebook)
        self.interview_tab = ttk.Frame(self.notebook)
        self.career_tab = ttk.Frame(self.notebook)
        self.job_search_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.profile_tab, text="Profile")
        self.notebook.add(self.resume_tab, text="Resume Analysis")
        self.notebook.add(self.interview_tab, text="Interview Prep")
        self.notebook.add(self.career_tab, text="Career Paths")
        self.notebook.add(self.job_search_tab, text="Job Search Plan")
        
        # Set up each tab
        self.setup_profile_tab()
        self.setup_resume_tab()
        self.setup_interview_tab()
        self.setup_career_tab()
        self.setup_job_search_tab()
    
    def setup_profile_tab(self):
        """Set up the profile tab content."""
        frame = ttk.Frame(self.profile_tab, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Profile information
        ttk.Label(frame, text="User Profile", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        labels = ["Name:", "Current Title:", "Years of Experience:", "Education:", "Skills (comma separated):"]
        self.profile_entries = {}
        
        for i, label in enumerate(labels):
            ttk.Label(frame, text=label).grid(row=i+1, column=0, sticky=tk.W, pady=5)
            entry = ttk.Entry(frame, width=50)
            entry.grid(row=i+1, column=1, sticky=tk.W, padx=5, pady=5)
            self.profile_entries[label.replace(":", "").lower().replace(" ", "_")] = entry
        
        # Buttons for loading/saving profile
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=len(labels)+1, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Save Profile", command=self.save_profile).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Load Profile", command=self.load_profile).pack(side=tk.LEFT, padx=5)
    
    def setup_resume_tab(self):
        """Set up the resume analysis tab content."""
        frame = ttk.Frame(self.resume_tab, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Resume Analysis", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Text area for resume input
        ttk.Label(frame, text="Paste your resume text below:").grid(row=1, column=0, sticky=tk.W)
        
        self.resume_text = scrolledtext.ScrolledText(frame, width=60, height=10)
        self.resume_text.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Analysis results area
        ttk.Label(frame, text="Analysis Results:").grid(row=3, column=0, sticky=tk.W, pady=(10, 5))
        
        self.analysis_results = scrolledtext.ScrolledText(frame, width=60, height=10, state='disabled')
        self.analysis_results.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Analyze button
        ttk.Button(frame, text="Analyze Resume", command=self.analyze_resume).grid(row=5, column=0, pady=10)
    
    def setup_interview_tab(self):
        """Set up the interview preparation tab content."""
        frame = ttk.Frame(self.interview_tab, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Interview Preparation", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Job title input
        ttk.Label(frame, text="Target Job Title:").grid(row=1, column=0, sticky=tk.W)
        self.job_title_entry = ttk.Entry(frame, width=40)
        self.job_title_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Get tips button
        ttk.Button(frame, text="Get Interview Tips", command=self.get_interview_tips).grid(row=2, column=0, pady=10)
        
        # Tips display area
        self.interview_tips_display = scrolledtext.ScrolledText(frame, width=60, height=20, state='disabled')
        self.interview_tips_display.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
    
    def setup_career_tab(self):
        """Set up the career paths tab content."""
        frame = ttk.Frame(self.career_tab, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Career Path Suggestions", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Interests input
        ttk.Label(frame, text="Your Interests (comma separated):").grid(row=1, column=0, sticky=tk.W)
        self.interests_entry = ttk.Entry(frame, width=50)
        self.interests_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Skills input
        ttk.Label(frame, text="Your Skills (comma separated):").grid(row=2, column=0, sticky=tk.W)
        self.skills_entry = ttk.Entry(frame, width=50)
        self.skills_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Get suggestions button
        ttk.Button(frame, text="Get Career Suggestions", command=self.get_career_suggestions).grid(row=3, column=0, pady=10)
        
        # Suggestions display area
        self.career_suggestions_display = scrolledtext.ScrolledText(frame, width=60, height=15, state='disabled')
        self.career_suggestions_display.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
    
    def setup_job_search_tab(self):
        """Set up the job search plan tab content."""
        frame = ttk.Frame(self.job_search_tab, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Job Search Plan Generator", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Job title input
        ttk.Label(frame, text="Target Job Title:").grid(row=1, column=0, sticky=tk.W)
        self.search_job_title = ttk.Entry(frame, width=40)
        self.search_job_title.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Location input
        ttk.Label(frame, text="Preferred Location:").grid(row=2, column=0, sticky=tk.W)
        self.location_entry = ttk.Entry(frame, width=40)
        self.location_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Experience level dropdown
        ttk.Label(frame, text="Experience Level:").grid(row=3, column=0, sticky=tk.W)
        self.experience_var = tk.StringVar()
        experience_combo = ttk.Combobox(frame, textvariable=self.experience_var, width=15)
        experience_combo['values'] = ('Entry', 'Mid', 'Senior')
        experience_combo.current(0)
        experience_combo.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Generate plan button
        ttk.Button(frame, text="Generate Job Search Plan", command=self.generate_search_plan).grid(row=4, column=0, pady=10)
        
        # Plan display area
        self.plan_display = scrolledtext.ScrolledText(frame, width=60, height=15, state='disabled')
        self.plan_display.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
    
    def save_profile(self):
        """Save the user profile to a file."""
        # Gather profile data from entries
        profile_data = {}
        for key, entry in self.profile_entries.items():
            profile_data[key] = entry.get()
            
        # Add timestamp
        profile_data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Update agent's profile
        for key, value in profile_data.items():
            self.agent.update_profile(key, value)
        
        # Save to file
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save Profile As"
        )
        
        if filename:
            success = self.agent.save_user_profile(filename)
            if success:
                messagebox.showinfo("Success", "Profile saved successfully!")
            else:
                messagebox.showerror("Error", "Failed to save profile.")
    
    def load_profile(self):
        """Load a user profile from a file."""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Select Profile File"
        )
        
        if filename:
            success = self.agent.load_user_profile(filename)
            if success:
                # Update UI with loaded profile
                for key, entry in self.profile_entries.items():
                    if key in self.agent.user_profile:
                        entry.delete(0, tk.END)
                        entry.insert(0, self.agent.user_profile[key])
                messagebox.showinfo("Success", "Profile loaded successfully!")
            else:
                messagebox.showerror("Error", "Failed to load profile.")
    
    def analyze_resume(self):
        """Analyze the resume text and display results."""
        resume_text = self.resume_text.get("1.0", tk.END)
        
        if len(resume_text.strip()) < 50:
            messagebox.showwarning("Warning", "Please enter a longer resume text for better analysis.")
            return
        
        results = self.agent.analyze_resume(resume_text)
        
        # Display results
        self.analysis_results.config(state='normal')
        self.analysis_results.delete("1.0", tk.END)
        
        self.analysis_results.insert(tk.END, f"Resume Score: {results['score']}/100\n\n")
        
        self.analysis_results.insert(tk.END, "Keywords Found:\n")
        for keyword in results["keywords_found"]:
            self.analysis_results.insert(tk.END, f"✓ {keyword}\n")
        
        self.analysis_results.insert(tk.END, "\nSuggested Keywords to Add:\n")
        for keyword in results["missing_keywords"]:
            self.analysis_results.insert(tk.END, f"- {keyword}\n")
        
        self.analysis_results.insert(tk.END, "\nImprovement Suggestions:\n")
        for suggestion in results["suggestions"]:
            self.analysis_results.insert(tk.END, f"• {suggestion}\n")
        
        self.analysis_results.config(state='disabled')
    
    def get_interview_tips(self):
        """Get and display interview preparation tips."""
        job_title = self.job_title_entry.get()
        
        tips = self.agent.get_interview_tips(job_title)
        
        # Display tips
        self.interview_tips_display.config(state='normal')
        self.interview_tips_display.delete("1.0", tk.END)
        
        self.interview_tips_display.insert(tk.END, "COMMON INTERVIEW QUESTIONS\n")
        self.interview_tips_display.insert(tk.END, "=========================\n\n")
        
        for i, question in enumerate(tips["common_questions"], 1):
            self.interview_tips_display.insert(tk.END, f"{i}. {question}\n")
        
        self.interview_tips_display.insert(tk.END, "\n\nPREPARATION TIPS\n")
        self.interview_tips_display.insert(tk.END, "===============\n\n")
        
        for i, tip in enumerate(tips["preparation_tips"], 1):
            self.interview_tips_display.insert(tk.END, f"{i}. {tip}\n")
        
        if tips["technical_topics"]:
            self.interview_tips_display.insert(tk.END, "\n\nRELEVANT TECHNICAL TOPICS TO STUDY\n")
            self.interview_tips_display.insert(tk.END, "===============================\n\n")
            
            for i, topic in enumerate(tips["technical_topics"], 1):
                self.interview_tips_display.insert(tk.END, f"{i}. {topic}\n")
        
        self.interview_tips_display.config(state='disabled')
    
    def get_career_suggestions(self):
        """Get and display career path suggestions."""
        interests_text = self.interests_entry.get()
        skills_text = self.skills_entry.get()
        
        if not interests_text or not skills_text:
            messagebox.showwarning("Warning", "Please enter both interests and skills.")
            return
        
        interests = [i.strip() for i in interests_text.split(",")]
        skills = [s.strip() for s in skills_text.split(",")]
        
        suggestions = self.agent.suggest_career_paths(interests, skills)
        
        # Display suggestions
        self.career_suggestions_display.config(state='normal')
        self.career_suggestions_display.delete("1.0", tk.END)
        
        self.career_suggestions_display.insert(tk.END, "SUGGESTED CAREER PATHS\n")
        self.career_suggestions_display.insert(tk.END, "======================\n\n")
        
        self.career_suggestions_display.insert(tk.END, "Based on your interests and skills, you might consider:\n\n")
        
        for i, career in enumerate(suggestions, 1):
            self.career_suggestions_display.insert(tk.END, f"{i}. {career}\n")
        
        self.career_suggestions_display.insert(tk.END, "\n\nNext Steps:\n")
        self.career_suggestions_display.insert(tk.END, "1. Research these roles to learn more about daily responsibilities\n")
        self.career_suggestions_display.insert(tk.END, "2. Identify any skill gaps and create a learning plan\n")
        self.career_suggestions_display.insert(tk.END, "3. Connect with professionals in these fields for informational interviews\n")
        
        self.career_suggestions_display.config(state='disabled')
    
    def generate_search_plan(self):
        """Generate and display a job search plan."""
        job_title = self.search_job_title.get()
        location = self.location_entry.get()
        experience = self.experience_var.get()
        
        if not job_title or not location:
            messagebox.showwarning("Warning", "Please enter both job title and location.")
            return
        
        plan = self.agent.generate_job_search_plan(job_title, location, experience)
        
        # Display plan
        self.plan_display.config(state='normal')
        self.plan_display.delete("1.0", tk.END)
        
        self.plan_display.insert(tk.END, f"JOB SEARCH PLAN: {job_title.upper()} IN {location.upper()}\n")
        self.plan_display.insert(tk.END, "=" * 50 + "\n\n")
        
        self.plan_display.insert(tk.END, "DAILY TASKS:\n")
        for task in plan["daily_tasks"]:
            self.plan_display.insert(tk.END, f"• {task}\n")
        
        self.plan_display.insert(tk.END, "\nWEEKLY TASKS:\n")
        for task in plan["weekly_tasks"]:
            self.plan_display.insert(tk.END, f"• {task}\n")
        
        self.plan_display.insert(tk.END, "\nRECOMMENDED RESOURCES:\n")
        self.plan_display.insert(tk.END, "- Job Boards: " + ", ".join(plan["resources"]["job_boards"][:4]) + "\n")
        self.plan_display.insert(tk.END, "- Networking: " + ", ".join(plan["resources"]["networking_opportunities"][:3]) + "\n")
        
        if "additional" in plan["resources"]:
            self.plan_display.insert(tk.END, "- Additional: " + ", ".join(plan["resources"]["additional"]) + "\n")
        
        self.plan_display.insert(tk.END, "\nTIMELINE:\n")
        for week, activity in plan["timeline"].items():
            self.plan_display.insert(tk.END, f"- {week.capitalize()}: {activity}\n")
        
        self.plan_display.config(state='disabled')


def main():
    """Main function to run the Career Development AI Agent."""
    root = tk.Tk()
    app = CareerAgentGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()