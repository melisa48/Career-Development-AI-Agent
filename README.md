# Career Development AI Agent

A Python-based AI assistant to help users with their career development needs, including job searching, resume building, interview preparation, and career growth advice.

## Features

- **User Profile Management**: Create, save, and load personalized user profiles
- **Resume Analysis**: Get feedback and improvement suggestions for your resume
- **Interview Preparation**: Access common interview questions and preparation tips tailored to specific job roles
- **Career Path Suggestions**: Discover potential career paths based on your interests and skills
- **Job Search Planning**: Generate a customized job search plan with daily and weekly tasks

## Prerequisites

- Python 3.6 or higher
- Tkinter (usually comes with Python installation)

## Installation

1. Clone this repository or download the source code
2. Navigate to the project directory
3. Run the application:

```bash
python career_agent.py
```

## How to Use

### User Profile

1. Fill in your personal information including name, current job title, experience, education, and skills
2. Click "Save Profile" to save your profile for future use
3. Use "Load Profile" to retrieve previously saved profiles

### Resume Analysis

1. Paste your resume text into the text area
2. Click "Analyze Resume" to receive:
   - An overall score
   - Keywords found in your resume
   - Suggested keywords to add
   - General improvement suggestions

### Interview Preparation

1. Enter your target job title
2. Click "Get Interview Tips" to receive:
   - Common interview questions
   - Preparation tips
   - Technical topics to study based on your job title

### Career Path Suggestions

1. Enter your interests and skills (comma separated)
2. Click "Get Career Suggestions" to receive:
   - Suggested career paths based on your input
   - Next steps for exploring these paths

### Job Search Plan

1. Enter your target job title, preferred location, and experience level
2. Click "Generate Job Search Plan" to receive:
   - Daily and weekly tasks
   - Recommended resources
   - A timeline for your job search

## Customization

- The application uses JSON files in the "resources" directory to store career development information. You can customize these files to match your specific needs better:

- `job_search_tips.json

## License
- This project is open-source and available under the MIT License.
