# 🏥 Husma Foundation - Donation Management System

A comprehensive web application built with Streamlit for managing donations, donors, children, and inventory for the Husma Foundation.

## 🚀 Quick Start

### Option 1: Using the startup script (Recommended)
```bash
python start_app.py
```

### Option 2: Direct Streamlit command
```bash
streamlit run app.py
```

### Option 3: Using the batch file (Windows)
```bash
run_simple.bat
```

## 📋 Features

### 👥 Donor Management
- **Registration**: Complete donor registration with validation
- **Authentication**: Secure login system with password hashing
- **Email Verification**: Automated email verification system
- **Password Reset**: Secure password reset functionality
- **Dashboard**: Personal donation history and statistics

### 💰 Donation System
- **Product Catalog**: Browse available nutritional supplements
- **Shopping Cart**: Add multiple items to cart
- **Payment Processing**: Upload payment slips for verification
- **Receipt Generation**: Automatic receipt generation and email
- **Inventory Management**: Real-time stock updates

### 👶 Children Management (Admin)
- **Child Registration**: Register children with guardian details
- **Milk Powder Issuance**: Track milk powder distribution
- **Issue History**: Complete history of distributions
- **Child Search**: Search and filter children

### 📊 Analytics Dashboard (Admin)
- **Donation Analytics**: Total donations, trends, and statistics
- **Donor Rankings**: Top donors and their contributions
- **Inventory Alerts**: Low stock and critical alerts
- **Monthly Reports**: Monthly donation trends

### 📦 Inventory Management (Admin)
- **Stock Tracking**: Real-time inventory levels
- **Low Stock Alerts**: Automatic alerts for low stock
- **Stock Updates**: Add or adjust inventory levels
- **Product Management**: Manage product details and pricing

## 🔧 Installation

1. **Clone or download the project**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## ⚙️ Configuration

### Environment Variables (Optional)
Create a `.env` file in the project root:

```bash
# Security
SECRET_KEY=your-secret-key-here
ADMIN_PASSWORD=your-secure-admin-password

# Application
BASE_URL=http://localhost:8501
```

### Default Admin Access
- **Username**: Check "Admin Access" checkbox
- **Password**: `admin123` (change this in production!)

## 🗂️ Project Structure

```
husma_foundation/
├── app.py                 # Main Streamlit application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── start_app.py          # Startup script
├── run_app.bat           # Windows batch file
├── README.md             # This file
├── CONFIGURATION.md      # Detailed configuration guide
├── auth/                 # Authentication modules
│   ├── authentication.py # Password hashing and validation
│   └── validation.py     # Input validation functions
├── database/             # Database operations
│   ├── models.py         # Database models
│   └── operations.py     # Database CRUD operations
├── services/             # External services
│   └── email_service.py  # Email functionality
├── utils/                # Utility functions
│   └── helpers.py        # Helper functions
├── static/               # Static assets
│   ├── css/             # CSS styles
│   └── images/          # Images and logos
├── templates/            # Email templates
└── instance/            # File uploads
    └── uploads/         # Payment slips
```

## 🔐 Security Features

- **Password Hashing**: Bcrypt encryption for passwords
- **Input Validation**: Comprehensive validation for all inputs
- **File Upload Security**: Secure file handling with unique naming
- **Session Management**: Secure session state management
- **Admin Protection**: Password-protected admin sections

## 📱 Usage Guide

### For Donors
1. **Register**: Create an account with your details
2. **Verify Email**: Check your email for verification link
3. **Login**: Access your personal dashboard
4. **Donate**: Browse products, add to cart, and make donations
5. **Track**: View your donation history and receipts

### For Administrators
1. **Admin Login**: Check "Admin Access" and enter password
2. **Manage Children**: Register and track children
3. **Issue Milk Powder**: Record distributions
4. **View Analytics**: Monitor donations and trends
5. **Manage Inventory**: Update stock levels and products

## 🛠️ Troubleshooting

### Common Issues

1. **"File does not exist: app.py"**
   - Make sure you're in the correct directory
   - Run: `cd "C:\Users\HP Probook 640 G4\PycharmProjects\husma_foundation"`

2. **"Session state has no key"**
   - Always use `streamlit run app.py` instead of `python app.py`

3. **Import errors**
   - Install dependencies: `pip install -r requirements.txt`

4. **Database errors**
   - The database will be created automatically on first run

### Getting Help
- Check the terminal output for error messages
- Ensure all dependencies are installed
- Verify you're using the correct Python environment

## 🌟 Features Highlights

- **Responsive Design**: Works on desktop and mobile
- **Real-time Updates**: Live inventory and donation tracking
- **Email Integration**: Automated receipts and notifications
- **Data Validation**: Comprehensive input validation
- **Security**: Secure password handling and file uploads
- **Analytics**: Detailed reporting and statistics
- **User-Friendly**: Intuitive interface for all users

## 📞 Support

For technical support or questions about the Husma Foundation system, please contact the development team.

---

**Husma Foundation** - Nourishing Little Warriors, One Meal at a Time ❤️
