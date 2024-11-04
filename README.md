# AUTISM-DETECTION
This is a simple machine learning model for detection of autism based on a mathematical model which is based on relative weights of the answers to the set of questions.
This set consists of 25 Questions regarding the behaviour of the Toddlers.
This set of 25 Questions is taken from a research test of Autism research centre - UNIVERSITY OF CAMBRIDGE

Link - https://www.autismresearchcentre.com/tests/quantitative-checklist-for-autism-in-toddlers-q-chat

# Key features of this ML model:

1. Parameter Weighting:

- Social Communication: 48%
- Speech and Language: 29%
- Repetitive Behaviors: 18%
- Sensory Patterns: 15%


2. Multiple Model Ensemble:

- Random Forest (40% weight)
- Gradient Boosting (40% weight)
- Neural Network (20% weight)

3. Numerical risk score (0-1)

------------------------------------------------------------

1. **Set up the Python Environment**:
   - Make sure you have Python 3.7 or a compatible version installed on your machine.
   - It's recommended to use a virtual environment to isolate the project dependencies. You can create and activate a virtual environment using a tool like `venv` or `conda`.

2. **Install the Required Dependencies**:
   - Open a terminal or command prompt and navigate to the directory containing the `autism-detection-model.py` file.
   - Install the required Python packages by running the following command:
     ```
     pip install numpy pandas scikit-learn flask
     ```

3. **Run the Flask API**:
   - In the terminal, navigate to the directory containing the `autism-detection-model.py` file.
   - Run the Flask API by executing the following command:
     ```
     python autism-detection-model.py
     ```
   - This will start the Flask development server, and the API will be available at `http://localhost:5000/predict`.

4. **Interact with the API**:
   - To test the API, you can use a tool like Postman or curl. Send a POST request to `http://localhost:5000/predict` with the following JSON payload:
     ```json
     {
       "answers": {
         "name_response": "always",
         "eye_contact": "very easy",
         "line_objects": "sometimes",
         "speech_clarity": "always",
         "pointing_request": "many times a day",
         "pointing_interest": "a few times a week",
         "spinning_interest": "several hours",
         "word_count": "over 100 words",
         "pretend_play": "a few times a day",
         "follow_look": "many times a day",
         "unusual_sensory": "never",
         "hand_placing": "never",
         "tiptoe_walking": "sometimes",
         "routine_adaptation": "quite difficult",
         "comfort_others": "sometimes",
         "repetitive_actions": "a few times a day",
         "first_words": "quite typical",
         "echo_speech": "a few times a day",
         "simple_gestures": "many times a day",
         "unusual_finger_movements": "never",
         "check_reaction": "usually",
         "object_interest": "most of the day",
         "repetitive_twiddling": "a few times a day",
         "noise_sensitivity": "sometimes",
         "staring": "a few times a week"
       }
     }
     ```
   - The API will respond with a JSON object containing the risk level, risk score, confidence, and domain scores for the provided answers.

5. **Integrate the Frontend**:
   - The `autism-screening-frontend.tsx` file contains a React component that you can integrate into your project's frontend.
   - Make sure you have the necessary dependencies installed, such as React and the `shadcn/ui` library.
   - You can import the `AutismScreeningTool` component from the `autism-screening-frontend.tsx` file and use it in your application.
   - The frontend component will handle the user interface and communication with the Flask API you just set up.
     
----------------------------------------------------------------------------------------------------------------------------------------


Here's how you can integrate the backend API into your `AutismScreeningTool` component:

1. Create a new file called `api.js` (or use the existing one if it's named differently) and add the `calculateAutismRisk` function:

```javascript
// api.js
const API_URL = 'http://localhost:5000';

export async function calculateAutismRisk(answers) {
  try {
    const response = await fetch(`${API_URL}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ answers }),
    });
    
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error calculating risk:', error);
    throw error;
  }
}
```

2. In your `AutismScreeningTool` component, import the `calculateAutismRisk` function from `api.js`:

```javascript
import { calculateAutismRisk } from './api';
```

3. Update the `calculateResults` function in your `AutismScreeningTool` component to use the `calculateAutismRisk` function:

```javascript
const calculateResults = async () => {
  try {
    const results = await calculateAutismRisk(answers);
    setResults(results);
  } catch (error) {
    setResults({
      riskLevel: 'Error',
      error: 'Unable to calculate results. Please try again.',
    });
  }
};
```

This updated `calculateResults` function will now use the `calculateAutismRisk` function from the `api.js` file to communicate with the backend API and retrieve the results.

Here's the complete `AutismScreeningTool` component with the updated `calculateResults` function:

```javascript
import { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { calculateAutismRisk } from './api';

const questions = [
  // ... (unchanged)
];

export default function AutismScreeningTool() {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [screeningComplete, setScreeningComplete] = useState(false);
  const [results, setResults] = useState(null);

  const handleAnswer = (answer) => {
    // ... (unchanged)
  };

  const calculateResults = async () => {
    try {
      const results = await calculateAutismRisk(answers);
      setResults(results);
    } catch (error) {
      setResults({
        riskLevel: 'Error',
        error: 'Unable to calculate results. Please try again.',
      });
    }
  };

  const renderQuestion = () => (
    // ... (unchanged)
  );

  const renderResults = () => (
    // ... (unchanged)
  );

  return (
    // ... (unchanged)
  );
}
```

Now, when the user completes the screening, the `calculateResults` function will call the `calculateAutismRisk` function from the `api.js` file to send the answers to the backend API and retrieve the results, which will then be displayed to the user.
