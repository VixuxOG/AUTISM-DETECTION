from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def landing():
    """Render the landing page."""
    return render_template('landing.html')

@app.route('/questionnaire')
def questionnaire():
    """Placeholder for questionnaire-based screening."""
    return "Add your questionnaire-based screening implementation here."

@app.route('/image')
def image():
    """Placeholder for image-based screening."""
    return "Add your image-based screening implementation here."

if __name__ == '__main__':
    app.run(debug=True)