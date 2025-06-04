# Dual-Approach Web Application for Preliminary ASD Screening

This project implements a web-based application designed to offer two distinct preliminary screening approaches for Autism Spectrum Disorder (ASD): a behavioral questionnaire and an AI-based image analysis using a Vision Transformer (ViT) model. The system is built using Python with the Flask web framework for the backend and HTML, CSS (including Tailwind CSS and custom styles), and JavaScript for the frontend.

**Disclaimer:** This application is a proof-of-concept and a technical demonstration. It is **NOT a diagnostic tool** and should **NOT** be used for self-diagnosis or to make any medical decisions. The results are preliminary and require interpretation by qualified healthcare professionals. The AI model for image analysis has **NOT been clinically validated**, and its accuracy and fairness are unknown.

## Table of Contents

1.  [Project Overview](#project-overview)
2.  [Features](#features)
3.  [System Architecture](#system-architecture)
    *   [Backend](#backend)
    *   [Frontend](#frontend)
    *   [AI Model](#ai-model)
4.  [Modules](#modules)
    *   [Landing Page (`landing.py`, `landing.html`)](#landing-page)
    *   [Questionnaire Screening (`app.py`, `index2.html`)](#questionnaire-screening)
    *   [Image-Based Screening (`flask_app.py`, `index.html`)](#image-based-screening)
5.  [Technologies Used](#technologies-used)
6.  [Setup and Installation](#setup-and-installation)
    *   [Prerequisites](#prerequisites)
    *   [Installation Steps](#installation-steps)
    *   [Model and Feature Extractor](#model-and-feature-extractor)
7.  [Running the Application](#running-the-application)
8.  [Project Structure](#project-structure)
9.  [Key Code Files](#key-code-files)
10. [Limitations and Future Work](#limitations-and-future-work)
11. [Ethical Considerations](#ethical-considerations)

## 1. Project Overview

The primary goal of this project is to explore the integration of traditional questionnaire-based screening methods with modern AI techniques for providing accessible, preliminary insights related to Autism Spectrum Disorder. The application presents users with two distinct paths:

*   **Questionnaire-Based Screening:** Users answer a series of 10 yes/no questions inspired by common ASD screening tools. The system calculates a score and provides a general interpretation of the likelihood (Low, Moderate, High).
*   **Image-Based Screening:** Users can upload an image (the specific type of image the model is trained for is undefined in this iteration). A pre-trained and fine-tuned Vision Transformer (ViT) model analyzes the image and provides a binary classification (e.g., "Autistic" or "Non-Autistic").

## 2. Features

*   **Dual Screening Modalities:** Offers both questionnaire and image-based approaches.
*   **Web-Based Interface:** Accessible via a standard web browser.
*   **Modular Design:** Separate Flask applications for different functionalities.
*   **Questionnaire Module:**
    *   10 behavioral screening questions.
    *   Automated scoring and percentage calculation.
    *   Interpretation of results (Low, Moderate, High likelihood).
    *   Clear disclaimers regarding non-diagnostic nature.
*   **Image Screening Module:**
    *   Image upload functionality.
    *   Integration of a Vision Transformer (ViT) model for classification.
    *   Frontend image preview.
    *   Dynamic prediction display.
    *   Visually distinct UI with animated background and neumorphic elements.
*   **Landing Page:** Central navigation point to access either screening tool.
*   **Responsive Design Hints:** Uses Tailwind CSS in parts for better adaptability (though full responsiveness testing may be needed).

## 3. System Architecture

The system follows a client-server architecture.

### Backend

*   Developed using **Python** and the **Flask** microframework.
*   Comprises three distinct Flask applications:
    *   `landing.py`: Serves the main landing page.
    *   `app.py`: Handles the questionnaire logic, scoring, and results.
    *   `flask_app.py`: Manages the image upload, ViT model inference, and prediction.
*   Utilizes **PyTorch** and the **Hugging Face Transformers** library for loading and running the ViT model.
*   **Pillow (PIL)** is used for image processing.
*   **Pickle** is used for loading the pre-saved ViT feature extractor.
*   Communication with the frontend is primarily through JSON responses.

### Frontend

*   Standard **HTML5** for structure.
*   **CSS3** for styling:
    *   **Tailwind CSS** is used for the landing page and questionnaire UI (`landing.html`, `index2.html`) for utility-first styling.
    *   **Custom CSS** is extensively used for the image screening UI (`index.html`) to create animated backgrounds, interactive elements, and neumorphic button styles.
*   **JavaScript (Vanilla JS)** is used for:
    *   Client-side interactions (button clicks, form submissions).
    *   Asynchronous communication with the backend (Fetch API).
    *   Dynamic DOM manipulation (displaying image previews, loading states, results, error messages).

### AI Model

*   A **Vision Transformer (ViT)** model (`google/vit-base-patch16-224-in21k`) is used.
*   The model is **pre-trained** and assumed to be **fine-tuned** for a binary classification task relevant to ASD screening (specifics of fine-tuning data are unknown).
*   Model weights are loaded from `vit_model.pt`.
*   A corresponding feature extractor, crucial for preprocessing images for the ViT model, is loaded from `vit_feature_extractor.pkl`.

## 4. Modules

### Landing Page (`landing.py`, `landing.html`)

*   **Functionality:** Serves as the initial entry point for users.
*   **Interface:** Provides two clear navigation options to either the Questionnaire-Based Screening or the Image-Based Screening modules. Includes a general disclaimer about the tool's purpose.
*   **Backend (`landing.py`):** A simple Flask app that renders `landing.html`.

### Questionnaire Screening (`app.py`, `index2.html`)

*   **Functionality:** Guides the user through a 10-item behavioral questionnaire.
*   **Questions (`SCREENING_QUESTIONS` in `app.py`):** Inspired by common ASD indicators. Each question has a "Yes" or "No" response.
*   **Scoring & Interpretation:**
    *   `calculate_autism_score()`: Counts "Yes" answers.
    *   `calculate_autism_percentage()`: Converts the score to a percentage.
    *   `interpret_results()`: Provides a textual interpretation (Low, Moderate, High likelihood) based on percentage thresholds.
*   **Interface (`index2.html`):** Displays questions, collects answers via radio buttons, and shows results dynamically after submission. Includes a progress bar simulation.
*   **Backend (`app.py`):** Handles form submission, performs calculations, and returns results as JSON.

### Image-Based Screening (`flask_app.py`, `index.html`)

*   **Functionality:** Allows users to upload an image for AI-based analysis.
*   **Model Inference:**
    *   Loads the pre-trained ViT model (`vit_model.pt`) and feature extractor (`vit_feature_extractor.pkl`).
    *   Preprocesses the uploaded image using the feature extractor.
    *   Performs inference using the ViT model on the specified device (CPU/GPU).
    *   Outputs a binary classification (e.g., "Autistic", "Non-Autistic").
*   **Interface (`index.html`):** Provides an image upload button, image preview, and displays the prediction. Features a unique animated background and neumorphic design elements.
*   **Backend (`flask_app.py`):** Handles image uploads, manages the model and feature extractor, performs prediction, and returns the result as JSON. Includes a route for `favicon.ico`.

## 5. Technologies Used

*   **Backend:** Python 3, Flask, PyTorch, Hugging Face Transformers, Pillow, Gunicorn (implied for deployment, not explicitly in dev code).
*   **Frontend:** HTML5, CSS3, JavaScript (Vanilla), Tailwind CSS.
*   **AI Model:** Vision Transformer (ViT).
*   **Serialization:** Pickle (for feature extractor).
*   **Data Exchange:** JSON.
*   **Version Control:** Git (assumed).

## 6. Setup and Installation

### Prerequisites

*   Python 3.7+
*   pip (Python package installer)
*   Access to a terminal or command prompt.
*   (Optional but Recommended) A virtual environment (e.g., `venv`, `conda`).

### Installation Steps

1.  **Clone the repository (if applicable) or download the project files.**
    ```bash
    git clone <repository-url>
    cd <project-directory>
    ```

2.  **(Recommended) Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Python dependencies:**
    A `requirements.txt` file would be ideal. If not present, you'll need to install them manually based on the imports in the Python files:
    ```bash
    pip install Flask torch torchvision torchaudio transformers Pillow
    # Note: PyTorch installation might vary based on your system (CPU/GPU).
    # Refer to the official PyTorch website: https://pytorch.org/get-started/locally/
    ```
    Based on the `flask_app.py`, you also need `transformers` with a compatible PyTorch version.

### Model and Feature Extractor

Ensure the following files are present in the root directory of the `Image-Based Screening` module (or where `flask_app.py` expects them):

*   `vit_model.pt`: The trained PyTorch model weights.
*   `vit_feature_extractor.pkl`: The pickled feature extractor object.

These files are critical for the image-based screening functionality and are **not** typically included in standard library installations. They would need to be obtained or generated separately.

## 7. Running the Application

The project consists of three separate Flask applications. You'll need to run them, ideally on different ports if running simultaneously for a fully integrated experience (though the landing page links to relative HTML files, suggesting they might be served by one main Flask app in a more complex setup or just navigated locally).

**For development:**

1.  **Run the Landing Page App:**
    ```bash
    cd <directory-of-landing.py>
    python landing.py
    ```
    This will typically start on `http://127.0.0.1:5000/`.

2.  **Run the Questionnaire App:**
    If `landing.html` links directly to `index2.html` and `index.html` as relative paths, you might intend for a single Flask app to serve all static HTML or for the user to navigate these as local files after accessing the landing page.
    However, given `app.py` for the questionnaire:
    ```bash
    cd <directory-of-app.py>
    python app.py
    ```
    This would also try to start on `http://127.0.0.1:5000/` by default. You'd need to configure it for a different port if running alongside `landing.py` managed by its own Flask instance (e.g., `app.run(debug=True, port=5001)`).

3.  **Run the Image Screening App:**
    ```bash
    cd <directory-of-flask_app.py>
    python flask_app.py
    ```
    The `flask_app.py` is configured to run on port `5001` (`app.run(debug=True, host='0.0.0.0', port=5001)`).

**Accessing the Application:**
*   Start by navigating to the URL of the Landing Page app (e.g., `http://127.0.0.1:5000/`).
*   From there, links should direct you to the questionnaire (`index2.html`) or image screening (`index.html`) pages. Ensure these HTML files are correctly pathed or served by their respective Flask apps if the links are absolute URLs.

*Note: For a production-like deployment, a WSGI server like Gunicorn or Waitress would be used in front of the Flask applications.*

*(The `templates` and `static` directory structure is conventional for Flask. The HTML files might be directly in the root in this simpler setup if `render_template` is used with just the filename.)*

## 9. Key Code Files

*   **`app.py`**:
    *   Defines `SCREENING_QUESTIONS`.
    *   Contains Flask routes for serving `index2.html` and handling `/submit`.
    *   Includes logic for `calculate_autism_score`, `calculate_autism_percentage`, and `interpret_results`.
*   **`flask_app.py`**:
    *   Loads ViT model (`vit_model.pt`) and feature extractor (`vit_feature_extractor.pkl`).
    *   Defines Flask routes for serving `index.html` and handling image predictions via `/predict`.
    *   Manages image preprocessing and model inference.
*   **`landing.py`**:
    *   Simple Flask app to serve `landing.html`.
*   **`index.html`**: Frontend for image screening, including complex CSS for animations and neumorphic design, and JavaScript for image upload, preview, and prediction requests.
*   **`index2.html`**: Frontend for questionnaire, using Tailwind CSS, and JavaScript for form submission, progress simulation, and result display.
*   **`landing.html`**: Simple HTML page with Tailwind CSS providing navigation to the other two modules.

## 10. Limitations and Future Work

*   **Not a Diagnostic Tool:** The system is for informational and preliminary screening purposes only.
*   **Lack of Clinical Validation:** Neither the questionnaire scoring nor the ViT model has undergone clinical validation. Accuracy and reliability are unknown.
*   **ViT Model Opacity:** The training data and methodology for the provided `vit_model.pt` are unknown, making it impossible to assess its biases, generalizability, or the specific image features it targets.
*   **Heuristic Scoring:** Questionnaire thresholds are arbitrary.
*   **Ethical Concerns:** Significant ethical implications regarding data privacy, misinterpretation of results, and algorithmic bias need thorough consideration.
*   **Scalability and Security:** The current implementation is for development/demonstration and lacks production-grade security and scalability features.

**Future Work:**

*   **Rigorous Clinical Validation:** Essential for both modules.
*   **ViT Model Development:** If pursuing image-based screening: define image type, curate an ethical and diverse dataset, train/fine-tune transparently, and report performance comprehensively.
*   **Explainable AI (XAI):** Integrate XAI techniques for the ViT model.
*   **User Studies & Feedback:** Conduct usability testing.
*   **Enhanced Security & Privacy:** Implement robust data protection measures.
*   **Resource Integration:** Provide links to reputable ASD information and support services.
*   **Deployment Strategy:** Develop a robust deployment plan using WSGI servers.

## 11. Ethical Considerations

Users and developers should be acutely aware of the ethical implications:

*   **Data Privacy:** Especially concerning image uploads. Clear policies and secure handling are paramount.
*   **Informed Consent:** Users must understand how their data is used.
*   **Algorithmic Bias:** The AI model may reflect biases from its unknown training data.
*   **Psychological Impact:** Potential for anxiety or false reassurance from unvalidated results.
*   **Responsible Communication:** Results must be clearly framed as preliminary and non-diagnostic.

This project serves as a starting point for exploring how technology can aid in preliminary ASD screening, but underscores the critical need for rigorous scientific validation, ethical design, and responsible deployment.
