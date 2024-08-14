import io
import csv
from flask import Flask, render_template, redirect, url_for, flash, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from wordcloud import WordCloud
import sqlite3
import os
import nltk

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///babylonia.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

# Analysis model
class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    pos_tags = db.Column(db.Text, nullable=False)
    trigrams = db.Column(db.Text, nullable=False)
    questions = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes for authentication
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email is already registered. Please log in or use a different email.', 'danger')
            return redirect(url_for('register'))
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        # Check if user exists and password matches
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

# Route for file upload and analysis
@app.route('/upload', methods=['POST'])
@login_required
def upload():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file:
        text = file.read().decode('utf-8')
        questions = extract_questions(text)
        
        # Generate word cloud
        wordcloud_path = os.path.join(app.config['UPLOAD_FOLDER'], 'wordcloud.png')
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        
        # Ensure the upload folder exists
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        
        # Save the word cloud image
        wordcloud.to_file(wordcloud_path)

        # Log analysis to SQLite database
        analysis = Analysis(content=text, pos_tags='', trigrams='', questions=str(questions))
        db.session.add(analysis)
        db.session.commit()

        return render_template('results.html', wordcloud='uploads/wordcloud.png', questions=questions)

# Function to extract questions from text
def extract_questions(text):
    sentences = nltk.sent_tokenize(text)
    questions = [sentence for sentence in sentences if sentence.endswith('?')]
    return questions

# Route to display recent questions
@app.route('/recent_questions')
@login_required
def recent_questions():
    recent_analyses = Analysis.query.order_by(Analysis.timestamp.desc()).limit(100).all()
    questions = [eval(analysis.questions) for analysis in recent_analyses]
    flat_questions = [question for sublist in questions for question in sublist]
    return render_template('recent_questions.html', questions=flat_questions)

# Route to export recent questions
@app.route('/export_recent_questions')
@login_required
def export_recent_questions():
    recent_analyses = Analysis.query.order_by(Analysis.timestamp.desc()).limit(100).all()
    questions = [eval(analysis.questions) for analysis in recent_analyses]
    flat_questions = [question for sublist in questions for question in sublist]

    response = make_response("\n".join(flat_questions))
    response.headers["Content-Disposition"] = "attachment; filename=recent_questions.txt"
    response.headers["Content-Type"] = "text/plain"
    return response

# Route to export selected questions to CSV
@app.route('/export_selected_questions', methods=['POST'])
@login_required
def export_selected_questions():
    selected_questions = request.form.getlist('selected_questions')

    if not selected_questions:
        flash('No questions selected for export.', 'warning')
        return redirect(url_for('recent_questions'))

    # Create CSV file response
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Question'])
    for question in selected_questions:
        writer.writerow([question])

    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=selected_questions.csv"
    response.headers["Content-Type"] = "text/csv"
    return response

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)