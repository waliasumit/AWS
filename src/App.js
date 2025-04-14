import React, { useState } from 'react';
import {
  Container,
  Typography,
  Box,
  TextField,
  Button,
  Card,
  CardContent,
  Radio,
  RadioGroup,
  FormControlLabel,
  FormControl,
  Alert,
} from '@mui/material';

// Sample questions database - In a real application, this would come from an API
const questionsDatabase = {
  's3': [
    {
      question: 'Which S3 storage class is most suitable for data that is accessed less frequently but requires rapid access when needed?',
      options: [
        'S3 Standard',
        'S3 Standard-IA',
        'S3 Glacier',
        'S3 One Zone-IA'
      ],
      correctAnswer: 1,
      explanation: 'S3 Standard-IA is ideal for infrequently accessed data that requires millisecond access when needed.'
    },
    // Add more S3 questions here
  ],
  'redshift': [
    {
      question: 'What is the maximum size of a single Amazon Redshift cluster?',
      options: [
        '2 PB',
        '4 PB',
        '8 PB',
        '16 PB'
      ],
      correctAnswer: 1,
      explanation: 'A single Amazon Redshift cluster can hold up to 4 PB of data using RA3 node types.'
    },
    // Add more Redshift questions here
  ],
  'glue': [
    {
      question: 'Which AWS Glue component is responsible for automatically discovering and cataloging metadata from data sources?',
      options: [
        'AWS Glue Data Catalog',
        'AWS Glue Crawler',
        'AWS Glue ETL',
        'AWS Glue Job'
      ],
      correctAnswer: 1,
      explanation: 'AWS Glue Crawler automatically discovers and catalogs metadata from data sources and stores it in the AWS Glue Data Catalog.'
    },
    // Add more Glue questions here
  ],
};

function App() {
  const [topic, setTopic] = useState('');
  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [showResults, setShowResults] = useState(false);
  const [answers, setAnswers] = useState({});
  const [error, setError] = useState('');

  const handleTopicSubmit = () => {
    if (!topic) {
      setError('Please enter a topic');
      return;
    }

    const topicLower = topic.toLowerCase();
    if (!questionsDatabase[topicLower]) {
      setError('No questions available for this topic. Try: s3, redshift, or glue');
      return;
    }

    setError('');
    setQuestions(questionsDatabase[topicLower]);
    setShowResults(false);
    setAnswers({});
    setCurrentQuestion(0);
  };

  const handleAnswerSelect = (event) => {
    setAnswers({
      ...answers,
      [currentQuestion]: parseInt(event.target.value)
    });
  };

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    } else {
      setShowResults(true);
    }
  };

  const calculateScore = () => {
    let correct = 0;
    Object.keys(answers).forEach(questionIndex => {
      if (answers[questionIndex] === questions[questionIndex].correctAnswer) {
        correct++;
      }
    });
    return correct;
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom align="center">
          AWS Data Engineer Certification Practice
        </Typography>
        
        <Box sx={{ mb: 4 }}>
          <TextField
            fullWidth
            label="Enter topic (e.g., s3, redshift, glue)"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            sx={{ mb: 2 }}
          />
          <Button
            variant="contained"
            color="primary"
            onClick={handleTopicSubmit}
            fullWidth
          >
            Get Questions
          </Button>
          {error && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {error}
            </Alert>
          )}
        </Box>

        {questions.length > 0 && !showResults && (
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Question {currentQuestion + 1} of {questions.length}
              </Typography>
              <Typography variant="body1" sx={{ mb: 2 }}>
                {questions[currentQuestion].question}
              </Typography>
              
              <FormControl component="fieldset">
                <RadioGroup
                  value={answers[currentQuestion] || ''}
                  onChange={handleAnswerSelect}
                >
                  {questions[currentQuestion].options.map((option, index) => (
                    <FormControlLabel
                      key={index}
                      value={index}
                      control={<Radio />}
                      label={option}
                    />
                  ))}
                </RadioGroup>
              </FormControl>

              <Box sx={{ mt: 2 }}>
                <Button
                  variant="contained"
                  onClick={handleNext}
                  disabled={answers[currentQuestion] === undefined}
                >
                  {currentQuestion < questions.length - 1 ? 'Next' : 'Show Results'}
                </Button>
              </Box>
            </CardContent>
          </Card>
        )}

        {showResults && (
          <Card>
            <CardContent>
              <Typography variant="h5" gutterBottom>
                Results
              </Typography>
              <Typography variant="h6">
                Score: {calculateScore()} out of {questions.length}
              </Typography>
              {questions.map((q, index) => (
                <Box key={index} sx={{ mt: 2 }}>
                  <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
                    Question {index + 1}: {answers[index] === q.correctAnswer ? '✅' : '❌'}
                  </Typography>
                  <Typography variant="body2">
                    {q.question}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Correct Answer: {q.options[q.correctAnswer]}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Explanation: {q.explanation}
                  </Typography>
                </Box>
              ))}
              <Button
                variant="contained"
                onClick={() => {
                  setShowResults(false);
                  setAnswers({});
                  setCurrentQuestion(0);
                }}
                sx={{ mt: 2 }}
              >
                Try Again
              </Button>
            </CardContent>
          </Card>
        )}
      </Box>
    </Container>
  );
}

export default App; 