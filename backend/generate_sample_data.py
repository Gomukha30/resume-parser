import json
import random
from datetime import datetime

def generate_sample_resume():
    names = [
        "John Smith",
        "Jane Doe",
        "Robert Johnson",
        "Emily Wilson",
        "Michael Brown",
        "Sarah Taylor",
        "David Anderson",
        "Jessica Martinez",
        "William Davis",
        "Laura Garcia"
    ]

    emails = [
        "john.smith@example.com",
        "jane.doe@example.com",
        "robert.johnson@example.com",
        "emily.wilson@example.com",
        "michael.brown@example.com",
        "sarah.taylor@example.com",
        "david.anderson@example.com",
        "jessica.martinez@example.com",
        "william.davis@example.com",
        "laura.garcia@example.com"
    ]

    phones = [
        "+1 (555) 123-4567",
        "+1 (555) 234-5678",
        "+1 (555) 345-6789",
        "+1 (555) 456-7890",
        "+1 (555) 567-8901",
        "+1 (555) 678-9012",
        "+1 (555) 789-0123",
        "+1 (555) 890-1234",
        "+1 (555) 901-2345",
        "+1 (555) 012-3456"
    ]

    skills = [
        "Python", "Java", "JavaScript", "React", "Node.js", "SQL",
        "Django", "Flask", "AWS", "Docker", "Kubernetes",
        "Machine Learning", "Deep Learning", "Data Science",
        "HTML", "CSS", "Git", "REST APIs", "Agile"
    ]

    companies = [
        "TechCorp", "Innovate Solutions", "CodeCraft", "WebWise",
        "DevGenius", "DigitalMinds", "TechNova", "CodeSphere",
        "WebPro", "TechPulse"
    ]

    positions = [
        "Software Engineer", "Full Stack Developer", "DevOps Engineer",
        "Data Scientist", "Machine Learning Engineer", "Product Manager",
        "UI/UX Designer", "Quality Assurance Engineer", "Backend Developer",
        "Frontend Developer"
    ]

    # Generate sample data
    sample_data = []
    for i in range(5):  # Generate 5 sample resumes
        resume = {
            "name": names[i],
            "email": emails[i],
            "phone": phones[i],
            "skills": random.sample(skills, random.randint(3, 6)),
            "experience": [
                f"{random.choice(positions)} at {random.choice(companies)}",
                f"{random.choice(positions)} at {random.choice(companies)}"
            ],
            "timestamp": datetime.now().isoformat()
        }
        sample_data.append(resume)

    # Save to data.json
    with open('data.json', 'w') as f:
        json.dump(sample_data, f, indent=4)

if __name__ == '__main__':
    generate_sample_resume()
