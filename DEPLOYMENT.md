# Deployment Guide for lekha.ai

This guide covers deploying the lekha.ai application to various platforms.

## 🚀 Local Development Deployment

### Prerequisites
- Python 3.13+
- MySQL Server 8.0+
- Tesseract OCR
- Poppler Utils

### Steps
1. Clone and setup (see README.md)
2. Run `python app.py`
3. Access at `http://localhost:5000`

## ☁️ Cloud Deployment Options

### 1. Heroku Deployment

#### Prepare for Heroku
```bash
# Install Heroku CLI
# Create Procfile
echo "web: python app.py" > Procfile

# Create runtime.txt
echo "python-3.13.7" > runtime.txt

# Update app.py for Heroku
# Change: app.run(host='0.0.0.0', port=5000, debug=True)
# To: app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
```

#### Deploy to Heroku
```bash
heroku create your-app-name
heroku addons:create cleardb:ignite  # MySQL addon
heroku config:set GEMINI_API_KEY=your_api_key
git push heroku main
```

### 2. Railway Deployment

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### 3. DigitalOcean App Platform

1. Connect GitHub repository
2. Set environment variables
3. Configure build and run commands
4. Deploy

### 4. AWS EC2 Deployment

#### Setup EC2 Instance
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv mysql-server -y

# Install Tesseract and Poppler
sudo apt install tesseract-ocr poppler-utils -y

# Clone repository
git clone https://github.com/jay192005/Rent_Agreement_Checker.git
cd Rent_Agreement_Checker

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup MySQL
sudo mysql_secure_installation
mysql -u root -p < databases/data.sql
mysql -u root -p < databases/analysis_history.sql

# Configure environment
cp .env.example .env
# Edit .env with your values

# Setup systemd service
sudo nano /etc/systemd/system/lekha-ai.service
```

#### Systemd Service File
```ini
[Unit]
Description=lekha.ai Flask Application
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/Rent_Agreement_Checker
Environment=PATH=/home/ubuntu/Rent_Agreement_Checker/venv/bin
ExecStart=/home/ubuntu/Rent_Agreement_Checker/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable lekha-ai
sudo systemctl start lekha-ai
```

### 5. Docker Deployment

#### Dockerfile
```dockerfile
FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

#### Docker Compose
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DB_HOST=db
      - DB_USER=root
      - DB_PASSWORD=password
      - DB_NAME=rent_agreements_db
    depends_on:
      - db
    volumes:
      - .:/app

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: rent_agreements_db
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

## 🔧 Production Configuration

### Environment Variables
```env
# Production settings
FLASK_ENV=production
DEBUG=False

# Database (use production database)
DB_HOST=your_production_db_host
DB_USER=your_db_user
DB_PASSWORD=your_secure_password
DB_NAME=rent_agreements_db

# API Keys
GEMINI_API_KEY=your_production_api_key

# Security
SECRET_KEY=your_very_secure_secret_key
```

### Security Considerations

1. **HTTPS**: Always use HTTPS in production
2. **Environment Variables**: Never commit sensitive data
3. **Database Security**: Use strong passwords and restrict access
4. **API Rate Limiting**: Implement rate limiting for API endpoints
5. **Input Validation**: Ensure all inputs are validated
6. **Error Handling**: Don't expose internal errors to users

### Performance Optimization

1. **Use Production WSGI Server**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Database Connection Pooling**:
   ```python
   # Add to app.py
   from mysql.connector import pooling
   
   config = {
       'user': os.getenv('DB_USER'),
       'password': os.getenv('DB_PASSWORD'),
       'host': os.getenv('DB_HOST'),
       'database': os.getenv('DB_NAME'),
       'pool_name': 'mypool',
       'pool_size': 10
   }
   
   pool = pooling.MySQLConnectionPool(**config)
   ```

3. **Caching**: Implement Redis for session storage and caching

4. **CDN**: Use CDN for static files

### Monitoring and Logging

1. **Application Monitoring**: Use tools like New Relic or DataDog
2. **Error Tracking**: Implement Sentry for error tracking
3. **Logging**: Configure proper logging levels
4. **Health Checks**: Implement comprehensive health checks

### Backup Strategy

1. **Database Backups**: Regular automated backups
2. **File Backups**: Backup uploaded files and configurations
3. **Code Backups**: Use Git for version control

## 🔍 Troubleshooting

### Common Issues

1. **Database Connection**: Check credentials and network access
2. **API Keys**: Verify Gemini API key is valid
3. **File Permissions**: Ensure proper file permissions
4. **Dependencies**: Check all system dependencies are installed

### Health Check Endpoint

The application includes a health check endpoint at `/api/health` that verifies:
- Database connectivity
- API availability
- System status

### Logs Location

- Application logs: Check console output or configure file logging
- System logs: `/var/log/` on Linux systems
- Database logs: MySQL error logs

## 📞 Support

For deployment issues:
1. Check the troubleshooting section
2. Review application logs
3. Create an issue on GitHub
4. Contact support team

---

**Happy Deploying! 🚀**