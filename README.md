# Resume Parser Application

A modern resume parsing application that extracts and analyzes key information from PDF resumes using Python (Flask) for the backend and React for the frontend. The application is containerized using Docker for easy deployment.

## Features

- Upload and parse PDF resumes
- Extract key information including:
  - Contact details (name, email, phone)
  - Skills and technologies
  - Work experience
  - Education
  - Certifications
- Modern, responsive user interface
- Docker support for easy deployment
- RESTful API for integration with other systems

## Prerequisites

- Docker and Docker Compose
- Node.js (for local development)
- Python 3.8+ (for local development)

## Quick Start with Docker

The easiest way to get started is using Docker:

1. Clone the repository:
```bash
git clone <repository-url>
cd resume-parser
```

2. Build and start the application:
```bash
chmod +x build.sh  # Make the build script executable
./build.sh
```

The application will be available at:
- Frontend: http://localhost:8000
//- API: http://localhost:8000/api //

## Development Setup

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
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

5. Run the Flask development server:
```bash
python app.py
```

The backend will run on http://localhost:8000

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

The frontend will be available at http://localhost:8000

## Deployment

### Docker Hub

To push the application to Docker Hub:

1. Login to Docker Hub:
```bash
docker login
```

2. Tag your image (replace `yourusername` with your Docker Hub username):
```bash
docker tag resume-parser yourusername/resume-parser:latest
```

3. Push the image:
```bash
docker push yourusername/resume-parser:latest
```

### Production Deployment

For production, use the `docker-compose.prod.yml` file which is optimized for production use:

```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```
FLASK_ENV=production
PORT=8000
```

## API Documentation

The API is available at `/api` with the following endpoints:

- `POST /api/upload-resume` - Upload and parse a resume
- `GET /api/health` - Health check endpoint

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License.

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will run on http://localhost:8000

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
