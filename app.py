# app.py (Corrected for Efficient DB Connections)

from flask import Flask, request, jsonify, g, send_from_directory, render_template_string
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

# --- NEW IMPORTS for handling PDF and DOCX files ---
import PyPDF2
import docx

# Import the new AI analysis logic
import ai

# Load environment variables from a .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Debug route to list all available routes
@app.route('/debug/routes')
def list_routes():
    """Debug route to show all available routes"""
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': list(rule.methods),
            'rule': str(rule)
        })
    return jsonify(routes)

# --- STATIC FILE ROUTES ---
@app.route('/')
def index():
    """Serve the main index.html page"""
    try:
        return send_from_directory('.', 'index.html')
    except FileNotFoundError:
        return "index.html file not found", 404

@app.route('/analyzer')
def analyzer():
    """Serve the analyzer.html page"""
    try:
        return send_from_directory('.', 'analyzer.html')
    except FileNotFoundError:
        return "analyzer.html file not found", 404

# Serve specific static files
@app.route('/style.css')
def serve_style_css():
    return send_from_directory('.', 'style.css')

@app.route('/analyzer.css')
def serve_analyzer_css():
    return send_from_directory('.', 'analyzer.css')

@app.route('/script.js')
def serve_script_js():
    return send_from_directory('.', 'script.js')

@app.route('/analyzer.js')
def serve_analyzer_js():
    return send_from_directory('.', 'analyzer.js')

# Generic static file handler (should be last)
@app.route('/<path:filename>')
def static_files(filename):
    """Serve static files (CSS, JS, images, etc.)"""
    try:
        return send_from_directory('.', filename)
    except FileNotFoundError:
        return f"File {filename} not found", 404

# --- DATABASE CONNECTION MANAGEMENT ---

def get_db():
    """
    Opens a new database connection if there is none yet for the
    current application context.
    """
    if 'db' not in g:
        try:
            # MySQL Workbench connection
            g.db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Jay@2005',  # Your MySQL password
                database='rent_agreements_db',
                port=3306,  # Standard MySQL Workbench port
                autocommit=False,
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci'
            )
            print("✅ Connected to MySQL Workbench database")
        except Error as e:
            print(f"❌ Error connecting to MySQL: {e}")
            print("💡 Please check your MySQL Workbench connection settings")
            # In case of connection error, we return None.
            # The routes should handle this.
            return None
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    """
    Closes the database again at the end of the request.
    This function is automatically called by Flask.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()


# --- User Authentication Endpoints (Fixed for actual table structure) ---
@app.route('/api/register', methods=['POST'])
def register_user():
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
        # Check if user already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({"error": "An account with this email already exists"}), 409

        # Hash the password and insert new user
        password_hash = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (email, password_hash) VALUES (%s, %s)", 
            (email, password_hash)
        )
            
        db.commit()
        print(f"✅ User registered: {email}")
        return jsonify({"message": "Account created successfully!"}), 201
        
    except Error as e:
        db.rollback()
        print(f"❌ Registration error: {e}")
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500
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
        # Find user by email
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password_hash'], password):
            print(f"✅ User logged in: {email}")
            return jsonify({"message": "Login successful!", "email": user['email']}), 200
        else:
            print(f"❌ Invalid login attempt: {email}")
            return jsonify({"error": "Invalid email or password"}), 401
            
    except Error as e:
        print(f"❌ Login error: {e}")
        return jsonify({"error": f"Login failed: {str(e)}"}), 500
    finally:
        cursor.close()


# --- UPDATED: Document Analysis Endpoint ---
@app.route('/api/analyze', methods=['POST'])
def analyze_document():
    # This part does not use the database, so it remains unchanged.
    document_text = ""
    
    if 'text' in request.form and request.form['text']:
        document_text = request.form['text']
    
    elif 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        try:
            if file.filename.endswith('.pdf'):
                pdf_reader = PyPDF2.PdfReader(file.stream)
                for page in pdf_reader.pages:
                    document_text += page.extract_text()
            elif file.filename.endswith('.docx'):
                doc = docx.Document(file.stream)
                full_text = []
                for para in doc.paragraphs:
                    full_text.append(para.text)
                document_text = '\n'.join(full_text)
            else:
                document_text = file.read().decode('utf-8')

        except Exception as e:
            return jsonify({"error": f"Could not read file. It might be corrupted or in an unsupported format. Error: {e}"}), 400
    
    if not document_text.strip():
        return jsonify({"error": "No document content could be extracted. The file might be empty or scanned as an image."}), 400

    state = request.form.get('state', '')

    preliminary_findings = ai.analyze_text_with_rules(document_text)
    gemini_result = ai.analyze_with_gemini(document_text, preliminary_findings, state)
    
    if "error" in gemini_result:
        return jsonify(gemini_result), 500

    final_result = gemini_result
    final_result['redFlagsCount'] = len(gemini_result.get('redFlags', []))
    final_result['fairClausesCount'] = len(gemini_result.get('fairClauses', []))

    return jsonify(final_result)


if __name__ == '__main__':
    app.run(port=5000, debug=True)