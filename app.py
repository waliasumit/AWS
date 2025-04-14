from flask import Flask, render_template, request, redirect, url_for, session
import json
import random
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')  # Use environment variable in production

# Questions database
questions_database = {
    's3': [
        {
            'question': 'Which S3 storage class is most suitable for data that is accessed less frequently but requires rapid access when needed?',
            'options': [
                'S3 Standard',
                'S3 Standard-IA',
                'S3 Glacier',
                'S3 One Zone-IA'
            ],
            'correct_answer': 1,
            'explanation': 'S3 Standard-IA is ideal for infrequently accessed data that requires millisecond access when needed.'
        },
        {
            'question': 'What is the maximum size of a single object in S3?',
            'options': [
                '5 GB',
                '5 TB',
                '10 TB',
                'Unlimited'
            ],
            'correct_answer': 1,
            'explanation': 'The maximum size of a single object in S3 is 5 TB.'
        },
        {
            'question': 'Which S3 feature provides strong consistency for all PUT and DELETE requests?',
            'options': [
                'S3 Eventual Consistency',
                'S3 Strong Consistency',
                'S3 Cross-Region Replication',
                'S3 Versioning'
            ],
            'correct_answer': 1,
            'explanation': 'S3 Strong Consistency ensures that any read after a write will return the most recent data.'
        },
        {
            'question': 'What is the minimum duration for S3 Glacier storage class?',
            'options': [
                '30 days',
                '90 days',
                '180 days',
                '365 days'
            ],
            'correct_answer': 1,
            'explanation': 'S3 Glacier requires a minimum storage duration of 90 days.'
        },
        {
            'question': 'Which S3 feature helps protect against accidental deletion of objects?',
            'options': [
                'S3 Lifecycle Rules',
                'S3 Versioning',
                'S3 Cross-Region Replication',
                'S3 Transfer Acceleration'
            ],
            'correct_answer': 1,
            'explanation': 'S3 Versioning helps protect against accidental deletion by keeping multiple variants of an object.'
        },
        {
            'question': 'What is the maximum number of buckets you can create in an AWS account?',
            'options': [
                '50',
                '100',
                '500',
                'Unlimited'
            ],
            'correct_answer': 1,
            'explanation': 'You can create up to 100 buckets per AWS account.'
        }
    ],
    'redshift': [
        {
            'question': 'What is the maximum size of a single Amazon Redshift cluster?',
            'options': [
                '2 PB',
                '4 PB',
                '8 PB',
                '16 PB'
            ],
            'correct_answer': 1,
            'explanation': 'A single Amazon Redshift cluster can hold up to 4 PB of data using RA3 node types.'
        },
        {
            'question': 'Which compression encoding is automatically applied by Redshift?',
            'options': [
                'LZO',
                'ZSTD',
                'Run-length encoding',
                'Delta encoding'
            ],
            'correct_answer': 2,
            'explanation': 'Redshift automatically applies run-length encoding to columns with repeated values.'
        },
        {
            'question': 'What is the maximum number of columns allowed in a Redshift table?',
            'options': [
                '100',
                '200',
                '400',
                '1600'
            ],
            'correct_answer': 3,
            'explanation': 'Redshift allows up to 1600 columns per table.'
        },
        {
            'question': 'Which Redshift feature helps improve query performance by physically organizing data?',
            'options': [
                'Sort Keys',
                'Distribution Keys',
                'Compression Encoding',
                'Workload Management'
            ],
            'correct_answer': 0,
            'explanation': 'Sort Keys help improve query performance by physically organizing data in a specific order.'
        },
        {
            'question': 'What is the maximum number of nodes in a Redshift cluster?',
            'options': [
                '32',
                '64',
                '128',
                '256'
            ],
            'correct_answer': 2,
            'explanation': 'Redshift clusters can have up to 128 nodes.'
        },
        {
            'question': 'Which Redshift feature helps manage query priorities and resource allocation?',
            'options': [
                'WLM (Workload Management)',
                'Query Monitoring',
                'Concurrency Scaling',
                'Maintenance Windows'
            ],
            'correct_answer': 0,
            'explanation': 'Workload Management (WLM) helps manage query priorities and resource allocation.'
        }
    ],
    'glue': [
        {
            'question': 'Which AWS Glue component is responsible for automatically discovering and cataloging metadata from data sources?',
            'options': [
                'AWS Glue Data Catalog',
                'AWS Glue Crawler',
                'AWS Glue ETL',
                'AWS Glue Job'
            ],
            'correct_answer': 1,
            'explanation': 'AWS Glue Crawler automatically discovers and catalogs metadata from data sources and stores it in the AWS Glue Data Catalog.'
        },
        {
            'question': 'What programming language is used for AWS Glue ETL jobs?',
            'options': [
                'Python',
                'Java',
                'Scala',
                'All of the above'
            ],
            'correct_answer': 3,
            'explanation': 'AWS Glue ETL jobs can be written in Python, Java, or Scala.'
        },
        {
            'question': 'What is the maximum number of concurrent Glue jobs allowed?',
            'options': [
                '50',
                '100',
                '200',
                '500'
            ],
            'correct_answer': 2,
            'explanation': 'AWS Glue allows up to 200 concurrent jobs.'
        },
        {
            'question': 'Which Glue feature helps optimize ETL job performance?',
            'options': [
                'Job Bookmarks',
                'Dynamic Frames',
                'Continuous Logging',
                'All of the above'
            ],
            'correct_answer': 3,
            'explanation': 'Job Bookmarks, Dynamic Frames, and Continuous Logging all help optimize ETL job performance.'
        },
        {
            'question': 'What is the maximum timeout for a Glue job?',
            'options': [
                '1 hour',
                '2 hours',
                '4 hours',
                '8 hours'
            ],
            'correct_answer': 3,
            'explanation': 'Glue jobs can run for up to 8 hours before timing out.'
        },
        {
            'question': 'Which Glue feature helps track processed data and resume from the last processed point?',
            'options': [
                'Job Bookmarks',
                'Checkpoints',
                'State Management',
                'Progress Tracking'
            ],
            'correct_answer': 0,
            'explanation': 'Job Bookmarks help track processed data and allow jobs to resume from the last processed point.'
        }
    ]
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    topic = request.form.get('topic', '').lower()
    if topic not in questions_database:
        return render_template('index.html', error='Invalid topic. Please choose from: s3, redshift, or glue')
    
    # Select 5 random questions from the topic
    all_questions = questions_database[topic]
    selected_questions = random.sample(all_questions, min(5, len(all_questions)))
    
    session['topic'] = topic
    session['questions'] = selected_questions
    session['current_question'] = 0
    session['answers'] = {}
    session['score'] = 0
    
    return redirect(url_for('question'))

@app.route('/question')
def question():
    if 'questions' not in session:
        return redirect(url_for('index'))
    
    current_q = session['current_question']
    questions = session['questions']
    
    if current_q >= len(questions):
        return redirect(url_for('results'))
    
    return render_template('question.html',
                         question=questions[current_q],
                         current=current_q + 1,
                         total=len(questions))

@app.route('/answer', methods=['POST'])
def answer():
    try:
        answer = int(request.form.get('answer', -1))
        current_q = session['current_question']
        questions = session['questions']
        
        # Convert answers to string keys for JSON serialization
        answers = session.get('answers', {})
        answers[str(current_q)] = answer
        session['answers'] = answers
        
        if answer == questions[current_q]['correct_answer']:
            session['score'] = session.get('score', 0) + 1
        
        session['current_question'] = current_q + 1
        
        return redirect(url_for('question'))
    except (ValueError, TypeError):
        return redirect(url_for('question'))

@app.route('/results')
def results():
    if 'questions' not in session:
        return redirect(url_for('index'))
    
    questions = session['questions']
    answers = session['answers']
    score = session['score']
    
    return render_template('results.html',
                         questions=questions,
                         answers=answers,
                         score=score,
                         total=len(questions))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 