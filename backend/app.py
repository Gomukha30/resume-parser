from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
import PyPDF2
import re
import json
import spacy
import os
import datetime

app = Flask(__name__, static_url_path='', static_folder='../frontend/build')

# Configure CORS to allow all origins for development
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:8000", "http://frontend:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Create a Blueprint for API routes
api = Blueprint('api', __name__, url_prefix='/api')

# Load spacy model
nlp = spacy.load("en_core_web_sm")

# Define regex patterns
PHONE_PATTERN = r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

# Skills to look for
SKILLS = [
    "Python", "Java", "JavaScript", "React", "Node.js", "SQL",
    "Django", "Flask", "AWS", "Docker", "Kubernetes",
    "Machine Learning", "Deep Learning", "Data Science"
]

@api.route('/upload-resume', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if not file.filename.endswith('.pdf'):
        return jsonify({"error": "File must be a PDF"}), 400
    
    try:
        # Read PDF
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
            
        # Extract information
        name = extract_name(text)
        email = extract_email(text)
        phone = extract_phone(text)
        skills = extract_skills(text)
        experience = extract_experience(text)
        
        # Create resume data
        resume_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "skills": skills,
            "experience": experience,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        # Save to JSON
        save_resume(resume_data)
        
        return jsonify(resume_data), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/resumes', methods=['GET'])
def get_resumes():
    try:
        with open('data.json', 'r') as f:
            resumes = json.load(f)
        return jsonify(resumes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def extract_name(text):
    # Try to get the first non-empty line that is not a section header
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    section_headers = [
        'EDUCATION', 'SKILLS', 'CERTIFICATIONS', 'INTERNSHIP EXPERIENCE',
        'EXPERIENCE', 'PROJECTS', 'ACHIEVEMENTS', 'WORK EXPERIENCE', 'PROFILE',
        'SUMMARY', 'CONTACT', 'LANGUAGES'
    ]
    for line in lines:
        if (
            line.upper() == line and
            len(line.split()) <= 4 and
            not any(h in line.upper() for h in section_headers)
        ) or (line.istitle() and not any(h in line.upper() for h in section_headers)):
            return line.strip()
    # Fallback to spaCy NER
    doc = nlp(text)
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    return names[0] if names else ""

def extract_email(text):
    # More robust: find all and return the first
    matches = re.findall(EMAIL_PATTERN, text)
    return matches[0] if matches else ""

def extract_phone(text):
    # Improved: match various phone formats
    phone_pattern = r"((?:\+\d{1,3}[\s-]?)?(?:\(?\d{2,4}\)?[\s-]?)?\d{3,4}[\s-]?\d{3,4}[\s-]?\d{3,4})"
    phones = re.findall(phone_pattern, text)
    # Filter out too-short matches
    phones = [p.strip() for p in phones if len(re.sub(r'\D', '', p)) >= 10]
    return phones[0] if phones else ""

def extract_skills(text):
    # Clean the text first
    text = clean_text(text)
    
    # Section-based extraction
    skills_section = extract_section(text, 
        ["SKILLS", "TECHNICAL SKILLS", "PROGRAMMING SKILLS", "TECHNOLOGIES"],
        ["EXPERIENCE", "EDUCATION", "CERTIFICATIONS", "PROJECTS"]
    )
    
    found_skills = set()
    
    if skills_section:
        # Try to find skills in a structured format (comma/colon separated)
        if ":" in skills_section:
            for line in skills_section.split('\n'):
                if ":" in line:
                    _, skills = line.split(":", 1)
                    skills = re.split(r'[,•\-\u2022]', skills)
                    for skill in skills:
                        skill = skill.strip()
                        if 2 < len(skill) < 32 and not any(x in skill.lower() for x in ["skill", "language"]):
                            found_skills.add(skill)
        
        # Also check for common skills
        for skill in SKILLS:
            if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text.lower()):
                found_skills.add(skill)
    
    # Fallback to global search if no skills found in skills section
    if not found_skills:
        for skill in SKILLS:
            if skill.lower() in text.lower():
                found_skills.add(skill)
    
    return list(found_skills)

def clean_text(text):
    """Clean and format the extracted text by adding spaces between words."""
    # First, handle common patterns that might be split across lines
    text = text.replace('-\n', '')  # Handle hyphenated words
    text = text.replace('\n', ' ')  # Replace newlines with spaces
    
    # Add spaces between camelCase and PascalCase words
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    
    # Add spaces between words that run together
    # Look for lowercase followed by uppercase (start of new word)
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    # Look for digit followed by letter
    text = re.sub(r'(\d)([A-Za-z])', r'\1 \2', text)
    # Look for letter followed by digit
    text = re.sub(r'([A-Za-z])(\d)', r'\1 \2', text)
    
    # Fix common abbreviations and acronyms
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with one
    
    # Fix common patterns
    patterns = [
        (r'C\s*G\s*P\s*A', 'CGPA'),
        (r'A\s*I', 'AI'),
        (r'U\s*I', 'UI'),
        (r'U\s*X', 'UX'),
        (r'J\s*S', 'JS'),
        (r'H\s*T\s*M\s*L', 'HTML'),
        (r'C\s*S\s*S', 'CSS'),
        (r'A\s*W\s*S', 'AWS'),
        (r'S\s*Q\s*L', 'SQL'),
        (r'J\s*a\s*v\s*a\s*s\s*c\s*r\s*i\s*p\s*t', 'JavaScript'),
        (r'R\s*e\s*a\s*c\s*t', 'React'),
        (r'N\s*o\s*d\s*e', 'Node')
    ]
    
    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    # Fix spacing around punctuation
    text = re.sub(r'\s+([.,;:!?])', r'\1', text)  # Remove space before punctuation
    text = re.sub(r'([(])\s+', r'\1', text)  # Remove space after (
    text = re.sub(r'\s+([)])', r'\1', text)  # Remove space before )
    
    # Add space after periods that don't have a space (but not for abbreviations)
    text = re.sub(r'\.([a-zA-Z])', r'. \1', text)
    
    # Fix common multi-word phrases
    text = text.replace('Machine Learning', 'MachineLearning')
    text = text.replace('Data Science', 'DataScience')
    text = text.replace('Web Development', 'WebDevelopment')
    
    return text.strip()

def extract_experience(text):
    # Clean the text first
    text = clean_text(text)
    
    # Section-based extraction for experience/internships
    exp_section = extract_section(text, 
        ["EXPERIENCE", "INTERNSHIP EXPERIENCE", "WORK EXPERIENCE", "INTERNSHIPS"],
        ["PROJECTS", "EDUCATION", "SKILLS", "CERTIFICATIONS", "ACHIEVEMENTS", "PROJECTS"]
    )
    
    result = []
    if exp_section:
        # Split into bullet points or lines
        for line in exp_section.split('\n'):
            line = line.strip()
            if line and not line.isspace() and len(line) > 10:
                # Clean up bullet points
                line = re.sub(r'^[•\-\*]\s*', '', line)  # Remove bullet points
                line = re.sub(r'\s+', ' ', line).strip()  # Normalize spaces
                if line and line not in ["Experience", "Work Experience", "Internship Experience"]:
                    result.append(line)
    
    # If no experience found, try to extract from the whole text
    if not result:
        # Look for experience-related keywords
        exp_keywords = ["experience", "worked at", "intern", "job", "position", "role"]
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', text)
        for sent in sentences:
            if any(keyword in sent.lower() for keyword in exp_keywords):
                cleaned = re.sub(r'\s+', ' ', sent).strip()
                if len(cleaned) > 20:  # Skip very short sentences
                    result.append(cleaned)
    
    return result[:5]  # Return at most 5 experience points

def extract_section(text, start_keywords, end_keywords):
    # Find section between headers
    lines = text.split('\n')
    start_idx = -1
    end_idx = len(lines)
    for i, line in enumerate(lines):
        if any(k in line.upper() for k in start_keywords):
            start_idx = i
            break
    if start_idx == -1:
        return ""
    for j in range(start_idx+1, len(lines)):
        if any(k in lines[j].upper() for k in end_keywords):
            end_idx = j
            break
    return "\n".join(lines[start_idx+1:end_idx]).strip()

def save_resume(resume_data):
    try:
        if not os.path.exists('data.json'):
            with open('data.json', 'w') as f:
                json.dump([], f)
        
        with open('data.json', 'r+') as f:
            data = json.load(f)
            data.append(resume_data)
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
    except Exception as e:
        print(f"Error saving resume: {str(e)}")
        raise

# Register the blueprint
app.register_blueprint(api)

# Serve React App
@app.route('/')
def serve_root():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def serve_static(path):
    if path.startswith('api/'):
        return 'Not Found', 404
    return app.send_static_file(path) or app.send_static_file('index.html')

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(host='0.0.0.0', port=8000, debug=False)
