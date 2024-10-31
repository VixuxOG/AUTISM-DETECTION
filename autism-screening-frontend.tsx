import { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';

const questions = [
  {
    id: 'name_response',
    text: 'Does your child look at you when you call his/her name?',
    options: ['always', 'usually', 'sometimes', 'rarely', 'never']
  },
  {
    id: 'eye_contact',
    text: 'How easy is it for you to get eye contact with your child?',
    options: ['very easy', 'quite easy', 'quite difficult', 'very difficult', 'impossible']
  },
  {
    id: 'line_objects',
    text: 'When your child is playing alone, does s/he line objects up?',
    options: ['always', 'usually', 'sometimes', 'rarely', 'never']
  },
  {
    id: 'speech_clarity',
    text: "Can other people easily understand your child's speech?",
    options: ['always', 'usually', 'sometimes', 'rarely', 'never', 'my child does not speak']
  },
  {
    id: 'pointing_request',
    text: 'Does your child point to indicate that s/he wants something (e.g. a toy that is out of reach)?',
    options: ['many times a day', 'a few times a day', 'a few times a week', 'less than once a week', 'never']
  },
  {
    id: 'pointing_interest',
    text: 'Does your child point to share interest with you (e.g. pointing at an interesting sight)?',
    options: ['many times a day', 'a few times a day', 'a few times a week', 'less than once a week', 'never']
  },
  {
    id: 'spinning_interest',
    text: "How long can your child's interest be maintained by a spinning object?",
    options: ['several hours', 'half an hour', 'ten minutes', 'a couple of minutes', 'less than a minute']
  },
  {
    id: 'word_count',
    text: 'How many words can your child say?',
    options: ['none---s/he has not started speaking yet', 'less than 10 words', '10--50 words', '51--100 words', 'over 100 words']
  },
  {
    id: 'pretend_play',
    text: 'Does your child pretend (e.g. care for dolls, talk on a toy phone)?',
    options: ['many times a day', 'a few times a day', 'a few times a week', 'less than once a week', 'never']
  },
  {
    id: 'follow_look',
    text: "Does your child follow where you're looking?",
    options: ['many times a day', 'a few times a day', 'a few times a week', 'less than once a week', 'never']
  },
  {
    id: 'unusual_sensory',
    text: 'How often does your child sniff or lick unusual objects?',
    options: ['many times a day', 'a few times a day', 'a few times a week', 'less than once a week', 'never']
  },
  {
    id: 'hand_placing',
    text: 'Does your child place your hand on an object when s/he wants you to use it?',
    options: ['many times a day', 'a few times a day', 'a few times a week', 'less than once a week', 'never']
  },
  {
    id: 'tiptoe_walking',
    text: 'Does your child walk on tiptoe?',
    options: ['always', 'usually', 'sometimes', 'rarely', 'never']
  },
  {
    id: 'routine_adaptation',
    text: 'How easy is it for your child to adapt when his/her routine changes?',
    options: ['very easy', 'quite easy', 'quite difficult', 'very difficult', 'impossible']
  },
  {
    id: 'comfort_others',
    text: 'If you or someone else in the family is visibly upset, does your child show signs of wanting to comfort them?',
    options: ['always', 'usually', 'sometimes', 'rarely', 'never']
  },
  {
    id: 'repetitive_actions',
    text: 'Does your child do the same thing over and over again?',
    options: ['many times a day', 'a few times a day', 'a few times a week', 'less than once a week', 'never']
  },
  {
    id: 'first_words',
    text: "Would you describe your child's first words as:",
    options: ['very typical', 'quite typical', 'slightly unusual', 'very unusual', "my child doesn't speak"]
  },
  {
    id: 'echo_speech',
    text: 'Does your child echo things s/he hears?',
    options: ['many times a day', 'a few times a day', 'a few times a week', 'less than once a week', 'never']
  },
  {
    id: 'simple_gestures',
    text: 'Does your child use simple gestures (e.g. wave goodbye)?',
    options: ['many times a day', 'a few times a day', 'a few times a week', 'less than once a week', 'never']
  },
  {
    id: 'unusual_finger_movements',
    text: 'Does your child make unusual finger movements near his/her eyes?',
    options: ['many times a day', 'a few times a day', 'a few times a week', 'less than once a week', 'never']
  },
  {
    id: 'check_reaction',
    text: 'Does your child spontaneously look at your face to check your reaction when faced with something unfamiliar?',
    options: ['always', 'usually', 'sometimes', 'rarely', 'never']
  },
  {
    id: 'object_interest',
    text: "How long can your child's interest be maintained by just one or two objects?",
    options: ['most of the day', 'several hours', 'half an hour', 'ten minutes', 'a couple of minutes']
  },
  {
    id: 'repetitive_twiddling',
    text: 'Does your child twiddle objects repetitively?',
    options: ['many times a day', 'a few times a day', 'a few times a week', 'less than once a week', 'never']
  },
  {
    id: 'noise_sensitivity',
    text: 'Does your child seem oversensitive to noise?',
    options: ['always', 'usually', 'sometimes', 'rarely', 'never']
  },
  {
    id: 'staring',
    text: 'Does your child stare at nothing with no apparent purpose?',
    options: ['many times a day', 'a few times a day', 'a few times a week', 'less than once a week', 'never']
  }
];

export default function AutismScreeningTool() {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [screeningComplete, setScreeningComplete] = useState(false);
  const [results, setResults] = useState(null);

  const handleAnswer = (answer) => {
    setAnswers(prev => ({
      ...prev,
      [questions[currentQuestion].id]: answer
    }));

    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(prev => prev + 1);
    } else {
      setScreeningComplete(true);
      calculateResults();
    }
  };

  const calculateResults = () => {
    setResults({
      riskLevel: 'Pending Analysis',
      score: 0,
      confidence: 0
    });
  };

  const renderQuestion = () => (
    <div className="space-y-6">
      <Progress 
        value={(currentQuestion / questions.length) * 100} 
        className="w-full"
      />
      <div className="text-center space-y-4">
        <h2 className="text-xl font-medium">
          Question {currentQuestion + 1} of {questions.length}
        </h2>
        <p className="text-lg">{questions[currentQuestion].text}</p>
        <div className="grid grid-cols-1 gap-3 mt-4">
          {questions[currentQuestion].options.map((option) => (
            <Button 
              key={option} 
              onClick={() => handleAnswer(option)}
              variant="outline"
              className="w-full text-left px-4 py-2 normal-case"
            >
              {option}
            </Button>
          ))}
        </div>
      </div>
    </div>
  );

  const renderResults = () => (
    <div className="text-center space-y-6">
      <h2 className="text-2xl font-bold">Screening Complete</h2>
      <div className="p-6 bg-gray-50 rounded-lg">
        <p className="text-lg mb-2">Risk Level: {results?.riskLevel}</p>
        <p className="text-sm text-gray-600">
          Please note: This screening tool is not a diagnostic instrument. 
          A professional evaluation is recommended for a proper assessment.
        </p>
      </div>
      <Button 
        onClick={() => {
          setCurrentQuestion(0);
          setAnswers({});
          setScreeningComplete(false);
          setResults(null);
        }}
        className="mt-4"
      >
        Start New Screening
      </Button>
    </div>
  );

  return (
    <div className="max-w-2xl mx-auto p-4">
      <Card className="w-full">
        <CardHeader>
          <CardTitle className="text-center">Autism Screening Assessment</CardTitle>
        </CardHeader>
        <CardContent>
          {!screeningComplete ? renderQuestion() : renderResults()}
        </CardContent>
      </Card>
    </div>
  );
}
