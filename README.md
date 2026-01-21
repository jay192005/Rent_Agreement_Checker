# lekha.ai - AI-Powered Rent Agreement Analyzer

![lekha.ai](https://img.shields.io/badge/lekha.ai-AI%20Legal%20Assistant-blue)
![Python](https://img.shields.io/badge/Python-3.13-green)
![Flask](https://img.shields.io/badge/Flask-2.3.3-red)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)

An intelligent web application that analyzes rent agreements using AI to identify potential red flags, unfair clauses, and provides recommendations for tenants in India.

## 🌟 Features

### 🔍 **AI-Powered Analysis**
- **Document Processing**: Upload PDF, DOCX, or paste text directly
- **OCR Support**: Analyze scanned documents using Tesseract OCR
- **Gemini AI Integration**: Advanced clause analysis using Google's Gemini AI
- **Risk Assessment**: 0-100 danger rating scale
- **Red Flag Detection**: Identifies potentially unfair or illegal clauses
- **Fair Clause Highlighting**: Recognizes standard and fair terms

### 👤 **User Management**
- **Secure Registration/Login**: Password hashing with Werkzeug
- **Analysis History**: Track all previous document analyses
- **User Dashboard**: Personal analysis history and management

### 🏛️ **Legal Intelligence**
- **India-Specific**: Tailored for Indian rental laws and regulations
- **State-Aware Analysis**: Location-specific legal considerations
- **Comprehensive Recommendations**: Actionable next steps for users

### 🎨 **Modern Interface**
- **Responsive Design**: Works on desktop and mobile devices
- **Intuitive UI**: Clean, professional interface
- **Real-time Feedback**: Loading states and progress indicators

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- MySQL Server 8.0+
- Tesseract OCR
- Poppler Utils (for PDF processing)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/jay192005/Rent_Agreement_Checker.git
   cd Rent_Agreement_Checker
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file:
   ```env
   # API Keys
   GEMINI_API_KEY=your_gemini_api_key_here
   
   # Database Configuration
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_NAME=rent_agreements_db
   DB_PORT=3306
   
   # OCR Configuration
   POPPLER_PATH=path_to_poppler_bin_directory
   ```

5. **Set up the database**
   ```bash
   python setup_database.py
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   Open your browser and go to `http://localhost:5000`

## 🏗️ Project Structure

```
lekha.ai/
├── app.py                 # Main Flask application
├── ai.py                  # AI analysis logic
├── setup_database.py     # Database setup script
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── static/               # Static files (CSS, JS, HTML)
│   ├── index.html        # Main landing page
│   ├── analyzer.html     # Document analysis page
│   ├── history.html      # Analysis history page
│   ├── style.css         # Main stylesheet
│   ├── analyzer.css      # Analysis page styles
│   ├── script.js         # Main JavaScript
│   ├── analyzer.js       # Analysis page logic
│   └── history.js        # History page logic
├── databases/            # Database schema files
│   ├── data.sql          # Users table schema
│   └── analysis_history.sql # Analysis history schema
└── tests/               # Test files
    ├── test_api_direct.py
    ├── final_test.py
    └── fix_fetch_issues.py
```

## 🔧 Configuration

### Database Setup

The application uses MySQL to store user accounts and analysis history:

```sql
-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Analysis history table
CREATE TABLE analysis_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    analysis_result TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### API Configuration

Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey) and add it to your `.env` file.

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Test database connectivity
python test_database_connection.py

# Test API endpoints
python test_api_direct.py

# Run final comprehensive test
python final_test.py

# Test fetch API functionality
python fix_fetch_issues.py
```

### Test Pages

- **Main Application**: `http://localhost:5000`
- **API Test Page**: `http://localhost:5000/test_fetch.html`
- **User Icon Test**: `http://localhost:5000/test_user_icon.html`

## 📱 Usage

1. **Register/Login**: Create an account or log in to save your analysis history
2. **Upload Document**: Upload a PDF/DOCX file or paste text directly
3. **Select Location**: Choose your state for location-specific analysis
4. **Get Analysis**: Receive AI-powered analysis with risk rating
5. **Review Results**: Check red flags, fair clauses, and recommendations
6. **View History**: Access all your previous analyses

## 🔒 Security Features

- **Password Hashing**: Secure password storage using Werkzeug
- **Input Validation**: Server-side validation for all user inputs
- **SQL Injection Protection**: Parameterized queries
- **CORS Configuration**: Proper cross-origin resource sharing
- **Environment Variables**: Sensitive data stored securely

## 🤖 AI Analysis Features

### Risk Assessment Scale
- **0-20**: Critical (Immediate legal review recommended)
- **21-40**: Danger (Multiple concerning clauses)
- **41-60**: Caution (Some issues to address)
- **61-80**: Safe (Minor concerns)
- **81-100**: Perfect (Fair and standard agreement)

### Analysis Components
- **Preliminary Rule-Based Scan**: Quick keyword detection
- **AI Deep Analysis**: Comprehensive clause evaluation
- **Legal Recommendations**: Actionable next steps
- **Priority Classification**: High/Medium/Low priority issues

## 🌐 API Endpoints

- `GET /api/health` - Health check
- `POST /api/register` - User registration
- `POST /api/login` - User login
- `POST /api/analyze` - Document analysis
- `GET /api/history/<email>` - Analysis history

## 🛠️ Development

### Running in Development Mode

```bash
# Enable debug mode
export FLASK_ENV=development
python app.py
```

### Code Quality

The project follows Python best practices:
- Type hints where applicable
- Comprehensive error handling
- Modular code structure
- Extensive documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

For support, email jay192005@example.com or create an issue on GitHub.

## 🙏 Acknowledgments

- **Google Gemini AI** for advanced text analysis
- **Tesseract OCR** for document text extraction
- **Flask** for the web framework
- **MySQL** for data storage

---

**Made with ❤️ for Indian tenants by lekha.ai**

*Empowering tenants through AI-powered legal document analysis*