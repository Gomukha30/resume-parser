# Resume Parser Application

This is a resume parsing application that extracts key information from PDF resumes using Python and React.

## Features

- Upload PDF resumes
- Extract name, email, phone, skills, and work experience
- Display extracted data in a clean format
- Store and view multiple resumes
- Modern and responsive UI

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download and install spaCy model:
```bash
python -m spacy download en_core_web_sm
```

5. Run the Flask server:
```bash
python app.py
```

The backend will run on http://localhost:5000

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd resume-parser
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will run on http://localhost:3000

## Project Structure

```
resume-parser/
├── backend/
│   ├── app.py              # Flask backend server
│   ├── requirements.txt    # Python dependencies
│   └── venv/               # Python virtual environment
├── resume-parser/          # Frontend React app
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── ResumeUpload.js
│   │   │   └── AllResumes.js
│   │   └── App.js
│   └── public/
└── README.md
```
