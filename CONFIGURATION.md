# Configuration Guide

## Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# Security
SECRET_KEY=your-secret-key-here
ADMIN_PASSWORD=your-secure-admin-password

# Application
BASE_URL=http://localhost:8501

# Database (optional - defaults to SQLite)
# DATABASE_URL=sqlite:///husma_foundation.db

# Email Configuration (for production)
# SMTP_SERVER=smtp.gmail.com
# SMTP_PORT=587
# SMTP_USERNAME=your-email@gmail.com
# SMTP_PASSWORD=your-app-password
```

## Security Notes

1. **Change the admin password** in production
2. **Use a strong SECRET_KEY** for session management
3. **Set up proper email service** for production
4. **Use environment variables** for sensitive data

## Running the Application

1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variables (optional)
3. Run: `streamlit run app.py`
4. Access at: http://localhost:8501

## Default Admin Access

- Username: Check admin checkbox
- Password: admin123 (change this!)
