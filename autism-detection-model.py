import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

class AutismDetectionModel:
    def __init__(self):
        # Define parameter groups and their weights
        self.parameter_groups = {
            'social_communication': {
                'name_response': 0.08,
                'eye_contact': 0.08,
                'pointing_interest': 0.07,
                'pointing_request': 0.07,
                'follow_look': 0.06,
                'simple_gestures': 0.06,
                'check_reaction': 0.06,
                'comfort_others': 0.05
            },
            'speech_and_language': {
                'speech_clarity': 0.07,
                'word_count': 0.06,
                'first_words': 0.06,
                'echo_speech': 0.05,
                'pretend_play': 0.05
            },
            'repetitive_behaviors': {
                'line_objects': 0.04,
                'spinning_interest': 0.04,
                'repetitive_actions': 0.04,
                'repetitive_twiddling': 0.03,
                'object_interest': 0.03
            },
            'sensory_patterns': {
                'unusual_sensory': 0.03,
                'noise_sensitivity': 0.03,
                'unusual_finger_movements': 0.03,
                'tiptoe_walking': 0.02,
                'staring': 0.02,
                'hand_placing': 0.02,
                'routine_adaptation': 0.02
            }
        }
        
        # Initialize models for ensemble
        self.models = {
            'random_forest': RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                random_state=42
            ),
            'gradient_boosting': GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42
            ),
            'neural_network': MLPClassifier(
                hidden_layer_sizes=(64, 32, 16),
                activation='relu',
                max_iter=1000,
                random_state=42
            )
        }
        
        self.scaler = StandardScaler()
        
    def _convert_response_to_score(self, response, question_type):
        """Convert categorical responses to numerical scores"""
        frequency_mapping = {
            'always': 4,
            'usually': 3,
            'sometimes': 2,
            'rarely': 1,
            'never': 0,
            'many times a day': 4,
            'a few times a day': 3,
            'a few times a week': 2,
            'less than once a week': 1,
            'very easy': 4,
            'quite easy': 3,
            'quite difficult': 1,
            'very difficult': 0,
            'impossible': 0,
            'very typical': 0,
            'quite typical': 1,
            'slightly unusual': 2,
            'very unusual': 3,
            'over 100 words': 0,
            '51--100 words': 1,
            '10--50 words': 2,
            'less than 10 words': 3,
            'none---s/he has not started speaking yet': 4,
            'my child does not speak': 4
        }
        
        # Reverse scoring for some questions where "never" indicates risk
        reverse_score_questions = [
            'name_response', 'eye_contact', 'speech_clarity', 
            'pointing_request', 'pointing_interest', 'pretend_play',
            'follow_look', 'simple_gestures', 'check_reaction', 
            'comfort_others'
        ]
        
        score = frequency_mapping.get(response.lower(), 2)  # Default to middle score if mapping not found
        
        if question_type in reverse_score_questions:
            score = 4 - score
            
        return score
        
    def preprocess_answers(self, answers):
        """Convert survey answers to feature vector"""
        features = {}
        
        for group, questions in self.parameter_groups.items():
            for question, weight in questions.items():
                if question in answers:
                    score = self._convert_response_to_score(answers[question], question)
                    weighted_score = score * weight
                    features[question] = weighted_score
                else:
                    features[question] = 0
                    
        return np.array(list(features.values())).reshape(1, -1)
        
    def calculate_risk_score(self, answers):
        """Calculate risk score and confidence level"""
        features = self.preprocess_answers(answers)
        scaled_features = self.scaler.transform(features)
        
        # Get predictions from each model
        predictions = {}
        probabilities = []
        
        for name, model in self.models.items():
            pred_prob = model.predict_proba(scaled_features)[0]
            predictions[name] = pred_prob
            probabilities.append(pred_prob)
            
        # Ensemble predictions using weighted average
        ensemble_weights = {
            'random_forest': 0.4,
            'gradient_boosting': 0.4,
            'neural_network': 0.2
        }
        
        final_probability = np.zeros(2)  # Binary classification (0: No ASD, 1: ASD)
        for name, prob in predictions.items():
            final_probability += prob * ensemble_weights[name]
            
        risk_score = final_probability[1]  # Probability of ASD
        
        # Calculate confidence based on model agreement
        model_variance = np.var([p[1] for p in probabilities])
        confidence = 1 - min(model_variance * 2, 0.5)  # Transform variance to confidence
        
        # Determine risk level
        risk_levels = {
            (0.0, 0.3): 'Low Risk',
            (0.3, 0.6): 'Medium Risk',
            (0.6, 1.0): 'High Risk'
        }
        
        risk_level = next(
            level for (lower, upper), level in risk_levels.items()
            if lower <= risk_score < upper
        )
        
        # Calculate sub-scores for each domain
        domain_scores = {}
        feature_idx = 0
        for domain, questions in self.parameter_groups.items():
            domain_score = sum(features[0][feature_idx:feature_idx + len(questions)])
            domain_scores[domain] = round(domain_score / len(questions), 2)
            feature_idx += len(questions)
            
        return {
            'risk_level': risk_level,
            'risk_score': round(float(risk_score), 3),
            'confidence': round(float(confidence), 3),
            'domain_scores': domain_scores
        }
        
    def train(self, training_data, labels):
        """Train the ensemble models"""
        X = self.scaler.fit_transform(training_data)
        X_train, X_test, y_train, y_test = train_test_split(
            X, labels, test_size=0.2, random_state=42
        )
        
        for name, model in self.models.items():
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            print(f"\nModel: {name}")
            print("Accuracy:", accuracy_score(y_test, y_pred))
            print("\nClassification Report:")
            print(classification_report(y_test, y_pred))
            
    def save_models(self, path):
        """Save trained models and scaler"""
        for name, model in self.models.items():
            joblib.dump(model, f"{path}/{name}.joblib")
        joblib.dump(self.scaler, f"{path}/scaler.joblib")
        
    def load_models(self, path):
        """Load trained models and scaler"""
        for name in self.models.keys():
            self.models[name] = joblib.load(f"{path}/{name}.joblib")
        self.scaler = joblib.load(f"{path}/scaler.joblib")

# Flask API for the model
from flask import Flask, request, jsonify

app = Flask(__name__)
model = AutismDetectionModel()

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        answers = data['answers']
        results = model.calculate_risk_score(answers)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
