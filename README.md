# Lekha.ai - AI-Powered Rental Agreement Analyzer

A web application that uses AI to analyze rental agreements and identify potentially problematic clauses, helping tenants understand their rights and make informed decisions.

## Features

- 🤖 **AI-Powered Analysis**: Uses Google Gemini AI to analyze rental agreements
- 📄 **Multi-Format Support**: Supports PDF, DOCX, and plain text documents, including scanned PDFs via OCR.
- 🚩 **Risk Assessment**: Provides danger ratings and identifies red flags
- ✅ **Fair Clause Detection**: Highlights standard and fair clauses
- 🔐 **User Authentication**: Secure login and registration system
- 🌍 **Location-Aware**: Considers Indian tenancy laws and state-specific regulations
- 📊 **Detailed Reports**: Comprehensive analysis with actionable recommendations
- 🗄️ **Analysis History**: Saves and retrieves past analysis reports for logged-in users.

## Technology Stack

- **Backend**: Python (Flask)
- **Frontend**: HTML, CSS, JavaScript (vanilla)
- **AI**: Google Gemini API
- **Database**: MySQL
- **File Processing**: PyPDF2, python-docx
- **OCR**: `pytesseract` (Tesseract) & `pdf2image` (Poppler)
- **Authentication**: Werkzeug security

## Installation

### Prerequisites

- Python 3.7+
- MySQL Server
- **Google Gemini API Key**: Get one from [Google AI Studio](https://aistudio.google.com/app/apikey).
- **Tesseract-OCR**: Required for reading scanned documents.
    - **Windows**: Download and run the installer from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki). Make sure to add the installation directory to your system's `PATH`.
    - **macOS**: `brew install tesseract`
    - **Linux (Debian/Ubuntu)**: `sudo apt-get install tesseract-ocr`
- **Poppler**: Required for converting PDFs to images for OCR.
    - **Windows**: Download the latest binary from [this blog](http://blog.alivate.com.au/poppler-windows/). Extract it, and add the `bin` directory to your `.env` file (see `POPPLER_PATH`).
    - **macOS**: `brew install poppler`
    - **Linux (Debian/Ubuntu)**: `sudo apt-get install poppler-utils`

### Setup

1.  **Clone the repository**
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2.  **Create and activate a virtual environment**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Python dependencies**
    ```bash
    pip install flask flask-cors mysql-connector-python python-dotenv PyPDF2 python-docx google-generativeai werkzeug pytesseract pdf2image
    ```

4.  **Set up environment variables**
    Copy `.env.example` to a new file named `.env` and fill in the details:
    ```dotenv
    # Your Google Gemini API Key
    GEMINI_API_KEY="your_gemini_api_key_here"

    # Your MySQL database password
    DB_PASSWORD="your_database_password_here"

    # (Windows Only) The full path to your Poppler 'bin' directory
    # Example: C:\Users\YourUser\Downloads\poppler-22.04.0\bin
    POPPLER_PATH="path_to_your_poppler_bin_directory"
    ```

5.  **Set up the MySQL database**
    - Make sure your MySQL server is running.
    - Run the database setup script. This will create the `rent_agreements_db` database and all required tables.
    ```bash
    python setup_database.py
    ```

6.  **Run the application**
    ```bash
    flask run
    # Or, for development mode with auto-reloading:
    # flask --app app --debug run
    ```

7.  **Access the application**
    Open your browser and go to `http://127.0.0.1:5000`.

## Usage

1.  **Register/Login**: Create an account or log in to access the analyzer and save your history.
2.  **Upload or Paste**: Go to the "Analyzer" page. You can either upload a rental agreement (`.pdf`, `.docx`, `.txt`) or paste the text directly.
3.  **Select State**: Choose your state for location-specific legal analysis.
4.  **Analyze**: Click the "Analyze" button to get your AI-powered report.
5.  **Review Results**: Review the comprehensive report, which includes an overall "danger rating," a list of red flags, fair clauses, and actionable recommendations.

## Database Schema

The application uses two tables:

### `users` table
```sql
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### `analysis_history` table
```sql
CREATE TABLE IF NOT EXISTS analysis_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    analysis_result TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

## Security Notes

-   Never commit your `.env` file to version control. It contains sensitive secrets.
-   Use a strong, unique password for your database connection in production.
-   The application uses password hashing (`scrypt`) via Werkzeug to protect user passwords.

## Disclaimer

This tool provides AI-generated analysis for educational purposes only. It is **not** a substitute for legal advice. Always consult with a qualified legal professional for important legal matters.