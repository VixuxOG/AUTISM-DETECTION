# import streamlit as st
# import time

# # Screening questions (inspired by common ASD screening tools like AQ-10)
# SCREENING_QUESTIONS = [
#     {"text": "Does the individual often prefer to be alone rather than with others?", "type": "boolean"},
#     {"text": "Does the individual struggle to understand other people's feelings or emotions?", "type": "boolean"},
#     {"text": "Does the individual show intense interest in specific topics or objects?", "type": "boolean"},
#     {"text": "Does the individual find it hard to follow or join conversations?", "type": "boolean"},
#     {"text": "Does the individual engage in repetitive behaviors (e.g., hand-flapping, rocking)?", "type": "boolean"},
#     {"text": "Is the individual sensitive to loud noises, bright lights, or certain textures?", "type": "boolean"},
#     {"text": "Does the individual have difficulty with changes in routine or transitions?", "type": "boolean"},
#     {"text": "Does the individual avoid eye contact during conversations?", "type": "boolean"},
#     {"text": "Does the individual take things very literally or struggle with sarcasm?", "type": "boolean"},
#     {"text": "Does the individual have delayed speech or communication skills?", "type": "boolean"},
# ]

# def calculate_autism_score(answers):
#     """Calculate autism screening score based on answers."""
#     score = sum(1 for answer in answers if answer == "Yes")
#     return score

# def calculate_autism_percentage(score, max_score=10):
#     """Convert score to percentage."""
#     return (score / max_score) * 100

# def interpret_results(percentage):
#     """Interpret the autism likelihood based on percentage."""
#     if percentage < 30:
#         return "Low likelihood of autism. Consult a professional for a comprehensive evaluation if concerns persist."
#     elif 30 <= percentage <= 60:
#         return "Moderate likelihood of autism. Consider a professional evaluation for further assessment."
#     else:
#         return "High likelihood of autism. A professional evaluation is strongly recommended."

# # Streamlit app setup
# asdd = "Autism Spectrum Disorder Screening"
# st.set_page_config(page_title=asdd, page_icon=':brain:', initial_sidebar_state="expanded")

# # Custom CSS for styling
# page_bg_img = """
# <style>
# [data-testid="stAppViewContainer"] {
#     background-image: url("https://img.freepik.com/premium-photo/bright-puzzles-kids-white_23-2147689859.jpg?w=1060");
# }
# [data-testid="stHeader"] {
#     background-color: rgba(0,0,0,0.4);
# }
# [data-testid="stVerticalBlock"] {
#     background-color: rgba(0,0,0,0.7);
#     border-radius: 13px;
#     box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
#     padding-right: 15px;
#     padding-left: 0.6em;
#     backdrop-filter: blur(10px);
#     -webkit-backdrop-filter: blur(4px);
#     padding-bottom: 10px;
# }
# [data-testid="stSidebar"] {
#     background-color: rgba(0,0,0,0.6);
#     border-radius: 13px;
#     box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
#     backdrop-filter: blur(10px);
#     -webkit-backdrop-filter: blur(4px);
# }
# [data-testid="stForm"] {
#     background-color: rgb(0,0,0);
# }
# </style>
# """
# st.markdown(page_bg_img, unsafe_allow_html=True)

# st.title(asdd)
# st.write(
#     "This is a preliminary screening tool for Autism Spectrum Disorder. Answer the "
#     "following questions honestly. This tool is not a substitute for a professional diagnosis."
# )

# # Initialize answers
# answers = ["" for _ in range(len(SCREENING_QUESTIONS))]

# # Form for user input
# with st.form("screening_survey"):
#     st.subheader("Screening Questions")
#     st.text("Please answer the following questions as honestly as possible:")

#     for idx, question in enumerate(SCREENING_QUESTIONS):
#         if question["type"] == "boolean":
#             answers[idx] = st.radio(question["text"], ("Yes", "No"), key=f"q_{idx}")

#     submitted = st.form_submit_button("Submit")

# # Process submission
# if submitted:
#     # Check if all questions are answered
#     if "" in answers:
#         st.error("Please answer all questions before submitting.")
#     else:
#         with st.spinner("Processing your responses..."):
#             progress_bar = st.progress(0)
#             progress_bar.progress(25)

#             # Calculate score and percentage
#             score = calculate_autism_score(answers)
#             percentage = calculate_autism_percentage(score)
#             progress_bar.progress(50)

#             # Interpret results
#             interpretation = interpret_results(percentage)
#             progress_bar.progress(100)

#         # Display results
#         st.header("Screening Results")
#         st.success(f"Likelihood of autism: {percentage:.2f}%")
#         st.info(interpretation)
#         st.warning(
#             "This result is for informational purposes only. Please consult a healthcare "
#             "professional for a formal diagnosis."
#         )
from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)

# Screening questions
SCREENING_QUESTIONS = [
    {"text": "Does the individual often prefer to be alone rather than with others?", "name": "q1"},
    {"text": "Does the individual struggle to understand other people's feelings or emotions?", "name": "q2"},
    {"text": "Does the individual show intense interest in specific topics or objects?", "name": "q3"},
    {"text": "Does the individual find it hard to follow or join conversations?", "name": "q4"},
    {"text": "Does the individual engage in repetitive behaviors (e.g., hand-flapping, rocking)?", "name": "q5"},
    {"text": "Is the individual sensitive to loud noises, bright lights, or certain textures?", "name": "q6"},
    {"text": "Does the individual have difficulty with changes in routine or transitions?", "name": "q7"},
    {"text": "Does the individual avoid eye contact during conversations?", "name": "q8"},
    {"text": "Does the individual take things very literally or struggle with sarcasm?", "name": "q9"},
    {"text": "Does the individual have delayed speech or communication skills?", "name": "q10"},
]

def calculate_autism_score(answers):
    """Calculate autism screening score based on answers."""
    return sum(1 for answer in answers if answer == "Yes")

def calculate_autism_percentage(score, max_score=10):
    """Convert score to percentage."""
    return (score / max_score) * 100

def interpret_results(percentage):
    """Interpret the autism likelihood based on percentage."""
    if percentage < 30:
        return "Low likelihood of autism. Consult a professional for a comprehensive evaluation if concerns persist."
    elif 30 <= percentage <= 60:
        return "Moderate likelihood of autism. Consider a professional evaluation for further assessment."
    else:
        return "High likelihood of autism. A professional evaluation is strongly recommended."

@app.route('/')
def index():
    """Render the screening form."""
    return render_template('index2.html', questions=SCREENING_QUESTIONS)

@app.route('/submit', methods=['POST'])
def submit():
    """Process form submission and return results."""
    answers = [request.form.get(f'q{i+1}') for i in range(10)]
    
    # Check for incomplete answers
    if None in answers or "" in answers:
        return jsonify({"error": "Please answer all questions before submitting."}), 400

    # Simulate processing delay
    time.sleep(1)

    # Calculate results
    score = calculate_autism_score(answers)
    percentage = calculate_autism_percentage(score)
    interpretation = interpret_results(percentage)

    return jsonify({
        "percentage": round(percentage, 2),
        "interpretation": interpretation,
        "disclaimer": "This result is for informational purposes only. Please consult a healthcare professional for a formal diagnosis."
    })

if __name__ == '__main__':
    app.run(debug=True)