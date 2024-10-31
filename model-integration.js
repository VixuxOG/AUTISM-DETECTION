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

// Update the calculateResults function in AutismScreeningTool component:
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
