# AWS Data Engineer Certification Practice

A Flask web application that helps you prepare for the AWS Data Engineer certification exam by providing practice questions based on specific topics.

## Features

- Topic-based question selection
- Multiple choice questions
- Immediate feedback
- Score tracking
- Detailed explanations for each answer

## Available Topics

Currently, the application supports questions for the following topics:
- S3
- Redshift
- Glue

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone this repository
2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Install the required packages:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Make sure your virtual environment is activated
2. Run the Flask application:
```bash
python app.py
```

3. Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage

1. Enter a topic in the text field (e.g., "s3", "redshift", or "glue")
2. Click "Start Quiz" to begin
3. Answer each question by selecting one of the provided options
4. Click "Next Question" to proceed
5. View your results and explanations at the end of the quiz

## Contributing

Feel free to submit issues and enhancement requests! 