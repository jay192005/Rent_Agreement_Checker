# app.py (Complete, Updated, and Secured Version)

from flask import Flask, request, jsonify, g
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
import re # Import the regular expression module for validation
from dotenv import load_dotenv

# --- IMPORTS for handling PDF and DOCX files ---
import PyPDF2
import docx

# --- IMPORTS for OCR (to read scanned documents) ---
from pdf2image import convert_from_path
import pytesseract

# --- CONFIGURATION for OCR tools ---
# Set the path to your Tesseract installation if it's not in your system's PATH
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
POPPLER_PATH = r'C:\Users\JAY GAVALI\Downloads\rent agreement checker\bin' # 👈 **UPDATE THIS** to your Poppler bin directory

# Import the AI analysis logic from your ai.py file
import ai

# Load environment variables from a .env file (for your Gemini API Key)
load_dotenv()

app = Flask(__name__)
CORS(app)

# --- STATIC FILE ROUTES ---
@app.route('/')
def index():
    """Serve the main index.html file"""
    return app.send_static_file('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files (HTML, CSS, JS, images)"""
    try:
        return app.send_static_file(filename)
    except:
        return "File not found", 404

# --- HELPER FUNCTIONS for Validation ---

def is_valid_email(email):
    """Checks if the email format is valid using a simple regex."""
    # This regex is a common, practical choice for email validation.
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None

def is_strong_password(password):
    """Checks if the password meets minimum strength requirements."""
    # For this example, we'll just check for a minimum length of 8 characters.
    return len(password) >= 8

# --- DATABASE CONNECTION MANAGEMENT ---

def get_db():
    """
    Opens a new database connection if there is none yet for the
    current application context. This is the best practice for Flask.
    """
    if 'db' not in g:
        try:
            # Connects to your MySQL Workbench database.
            # Ensure these details match your local MySQL setup.
            g.db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Jay@2005', # 👈 **UPDATE THIS**
                database='rent_agreements_db'
                # The port is typically 3306 by default, so it's not needed unless you changed it.
            )
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            # This will be caught by the routes if the connection fails.
            return None
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    """
    Closes the database connection at the end of the request to free up resources.
    This function is automatically called by Flask.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()


# --- User Authentication Endpoints (with Validation) ---
@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # --- NEW: Backend Validation ---
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    if not is_valid_email(email):
        return jsonify({"error": "Please enter a valid email address"}), 400
    if not is_strong_password(password):
        return jsonify({"error": "Password must be at least 8 characters long"}), 400

    db = get_db()
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = db.cursor(dictionary=True)
    
    try:
        # Check if user already exists
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({"error": "An account with this email already exists"}), 409

        # Create new user
        password_hash = generate_password_hash(password)
        cursor.execute("INSERT INTO users (email, password_hash) VALUES (%s, %s)", (email, password_hash))
        
        new_user_id = cursor.lastrowid
        db.commit()
        
        # Return user info to automatically log them in on the frontend
        return jsonify({
            "message": "Account created successfully!",
            "email": email,
            "id": new_user_id
        }), 201
        
    except Error as e:
        db.rollback() # Roll back changes if an error occurs
        print(f"Registration Error: {e}")
        print(f"Error Code: {e.errno}")
        print(f"SQL State: {e.sqlstate}")
        return jsonify({"error": "An internal error occurred during registration."}), 500
    finally:
        cursor.close()

@app.route('/api/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    db = get_db()
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = db.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT id, email, password_hash FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password_hash'], password):
            return jsonify({
                "message": "Login successful!",
                "email": user['email'],
                "id": user['id']
            }), 200
        else:
            # Use a generic error message for security
            return jsonify({"error": "Invalid credentials"}), 401
    except Error as e:
        print(f"Login Error: {e}")
        return jsonify({"error": "An internal error occurred during login."}), 500
    finally:
        cursor.close()


# --- Document Analysis Endpoint ---
@app.route('/api/analyze', methods=['POST'])
def analyze_document():
    document_text = ""
    
    # Extract text from either pasted content or an uploaded file
    if 'text' in request.form and request.form['text']:
        document_text = request.form['text']
    elif 'file' in request.files:
        file = request.files['file']
        if not file or file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        try:
            if file.filename.lower().endswith('.pdf'):
                pdf_reader = PyPDF2.PdfReader(file.stream)
                # Check for encrypted PDFs that cannot be read
                if pdf_reader.is_encrypted:
                    return jsonify({"error": "Cannot process encrypted PDF files."}), 400 # Keep this check
                
                # First, try the fast text extraction
                for page in pdf_reader.pages:
                    document_text += page.extract_text() or ""

                # --- OCR FALLBACK ---
                # If the text is still empty, it's likely a scanned PDF.
                if not document_text.strip():
                    print("--- Text extraction failed, falling back to OCR. ---")
                    # We need to save the file temporarily to use its path
                    file.stream.seek(0) # Go back to the start of the file stream
                    images = convert_from_path(file.stream.name, poppler_path=POPPLER_PATH)
                    for image in images:
                        document_text += pytesseract.image_to_string(image) + "\n"

            elif file.filename.lower().endswith('.docx'):
                doc = docx.Document(file.stream)
                document_text = '\n'.join([para.text for para in doc.paragraphs])
            else: # Assume .txt or other plain text formats
                document_text = file.read().decode('utf-8')
        except Exception as e:
            # Provide a more user-friendly error for corrupted files
            print(f"File Read Error: {e}")
            return jsonify({"error": "Could not read the uploaded file. It may be corrupted or in an unsupported format."}), 400
    
    if not document_text.strip():
        return jsonify({"error": "Could not extract any text from the document. It might be empty or a scanned image."}), 400

    state = request.form.get('state', '')
    email = request.form.get('email', None)

    # Step 1: Get the analysis from your AI module (ai.py)
    preliminary_findings = ai.analyze_text_with_rules(document_text)
    gemini_result = ai.analyze_with_gemini(document_text, preliminary_findings, state)
    
    if "error" in gemini_result:
        return jsonify(gemini_result), 500

    # Step 2: Create the complete final result object to be sent and saved
    final_result = gemini_result
    final_result['redFlagsCount'] = len(gemini_result.get('redFlags', []))
    final_result['fairClausesCount'] = len(gemini_result.get('fairClauses', []))

    # Step 3: Save the complete result to the database if the user is logged in
    if email:
        db = get_db()
        if db:
            cursor = db.cursor()
            try:
                cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
                user = cursor.fetchone()
                if user:
                    user_id = user[0] # The user ID
                    # Convert the final result dictionary to a JSON string for storage.
                    # This is the standard way to insert into a JSON column.
                    result_json_string = json.dumps(final_result)
                    
                    cursor.execute(
                        "INSERT INTO analysis_history (user_id, analysis_result) VALUES (%s, %s)",
                        (user_id, result_json_string)
                    )
                    db.commit()
                    print(f"Analysis saved for user_id: {user_id}")
            except Error as e:
                db.rollback()
                print(f"Error saving analysis to DB: {e}")
            finally:
                cursor.close()

    # Step 4: Return the complete result to the frontend
    return jsonify(final_result)


# --- Get Analysis History Endpoint ---
@app.route('/api/history/<email>', methods=['GET'])
def get_history(email):
    db = get_db()
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = db.cursor(dictionary=True)
    try:
        query = """
            SELECT h.id, h.analysis_result, h.created_at
            FROM analysis_history h
            JOIN users u ON h.user_id = u.id
            WHERE u.email = %s
            ORDER BY h.created_at DESC
        """
        cursor.execute(query, (email,))
        history = cursor.fetchall()
        
        # Format the date and parse the analysis_result JSON string into a dictionary
        # before sending it to the frontend.
        for item in history:
            item['created_at'] = item['created_at'].isoformat()
            item['analysis_result'] = json.loads(item['analysis_result']) # Convert JSON string to dict

        return jsonify(history), 200
    except Error as e:
        print(f"History Fetch Error: {e}")
        return jsonify({"error": "An internal error occurred while fetching history."}), 500
    finally:
        cursor.close()

# This is the standard entry point for running a Flask application.
if __name__ == '__main__':
    # debug=True automatically reloads the server when you make changes.
    # Turn this off for production deployment.
    app.run(port=5000, debug=True)