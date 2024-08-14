Here's a draft for a README file that you can use for your project:

---

# Babylonia Text Analysis Application

## Overview

The **Babylonia Text Analysis Application** is a Flask-based web application designed to analyze text, extract questions, and generate a word cloud. It provides a user-friendly interface for uploading text files, viewing the most recent questions, and exporting selected questions to a CSV file. The application also includes user authentication to ensure secure access.

## Features

- **User Authentication**: Secure login and registration system with password hashing.
- **Text Upload and Analysis**: Upload text files for analysis, where the application extracts questions and generates a word cloud.
- **Recent Questions**: View the most recent 100 questions extracted from uploaded text files.
- **Export Functionality**: Export selected questions to a CSV file.
- **Responsive Design**: The application is designed to be responsive, working smoothly on various screen sizes.
- **Visual Enhancements**: Recent questions are displayed as cards with padding and a hover animation for an engaging user experience.

## Installation

### Prerequisites

- Python 3.x
- Flask
- Flask-Login
- Flask-SQLAlchemy
- Flask-Bcrypt
- WordCloud
- NLTK

### Clone the Repository

```bash
git clone https://github.com/your-username/babylonia-text-analysis.git
cd babylonia-text-analysis
```

### Set Up the Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
flask run
```

The application should now be running at `http://127.0.0.1:5000/`.

## Usage

### Registration and Login

1. **Register**: Create a new account by providing a username, email, and password.
2. **Login**: Log in using your registered email and password.

### Text Upload and Analysis

1. **Upload Text**: Once logged in, navigate to the upload page and submit a text file.
2. **View Results**: The application will extract questions from the text and generate a word cloud.
3. **Recent Questions**: View the most recent 100 questions on the "Recent Questions" page.

### Exporting Questions

1. **Select Questions**: On the "Recent Questions" page, select the questions you wish to export.
2. **Export to CSV**: Click the "Export Selected to CSV" button to download the selected questions as a CSV file.

## Screenshots

_Add screenshots of the application here if necessary._

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Flask**: For the web framework that powers this application.
- **NLTK**: For the natural language processing tools used in text analysis.
- **WordCloud**: For generating word clouds from the uploaded text.

## Contact

If you have any questions or feedback, feel free to reach out.

---

You can customize this README further to suit your project's specific needs. If you need anything else, feel free to ask!