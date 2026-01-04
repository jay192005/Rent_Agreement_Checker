# ClearTenant - AI-Powered Rental Agreement Analyzer

A web application that uses AI to analyze rental agreements and identify potentially problematic clauses, helping tenants understand their rights and make informed decisions.

## Features

- 🤖 **AI-Powered Analysis**: Uses Google Gemini AI to analyze rental agreements
- 📄 **Multi-Format Support**: Supports PDF, DOCX, and plain text documents
- 🚩 **Risk Assessment**: Provides danger ratings and identifies red flags
- ✅ **Fair Clause Detection**: Highlights standard and fair clauses
- 🔐 **User Authentication**: Secure login and registration system
- 🌍 **Location-Aware**: Considers Indian tenancy laws and state-specific regulations
- 📊 **Detailed Reports**: Comprehensive analysis with actionable recommendations

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **AI**: Google Gemini API
- **Database**: MySQL
- **File Processing**: PyPDF2, python-docx
- **Authentication**: Werkzeug security

## Installation

### Prerequisites

- Python 3.7+
- MySQL Server
- Google Gemini API Key

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cleartenant
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install flask flask-cors mysql-connector-python python-dotenv PyPDF2 python-docx google-generativeai werkzeug
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```
   GEMINI_API_KEY="your_gemini_api_key_here"
   ```

5. **Set up MySQL database**
   - Create a database named `rent_agreements_db`
   - Update database credentials in `app.py` if needed
   - Run the application to auto-create tables

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   Open your browser and go to `http://127.0.0.1:5000`

## Usage

1. **Register/Login**: Create an account or log in to access the analyzer
2. **Upload Document**: Go to the analyzer page and upload a rental agreement (PDF/DOCX) or paste text
3. **Select Location**: Choose your state for location-specific legal analysis
4. **Analyze**: Click "Analyze Lease & Get Danger Rating" to get AI-powered insights
5. **Review Results**: Get a comprehensive report with:
   - Overall danger rating (0-100)
   - Red flags and problematic clauses
   - Fair and standard clauses
   - Actionable recommendations

## API Endpoints

- `GET /` - Homepage
- `GET /analyzer` - Document analyzer page
- `POST /api/register` - User registration
- `POST /api/login` - User login
- `POST /api/analyze` - Document analysis

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## Configuration

### MySQL Connection
Update the database connection settings in `app.py`:
```python
g.db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='your_password',
    database='rent_agreements_db',
    port=3306
)
```

### Gemini API
Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey) and add it to your `.env` file.

## Security Notes

- Never commit your `.env` file to version control
- Use strong passwords for database connections
- Keep your Gemini API key secure
- The application uses password hashing for user authentication

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational and personal use. Please ensure compliance with Google Gemini API terms of service.

## Disclaimer

This tool provides AI-generated analysis for educational purposes only. Always consult with a qualified legal professional for important legal decisions. The analysis should not be considered as legal advice.

## Support

For issues and questions, please create an issue in the GitHub repository.