# 🛍️E-Commerce Platform

## 🌟Overview
A full featured E-Commerce platform built with Django that enables customers to browse products, make purchases, and allows shopkeepers to manage their inventory and orders. This project aims to provide a seamless shopping experience while giving shopkeepers powerful tools to manage their business.

## 🚀Features

### 👤For Customers
- User registration and authentication
- Browse products with search and filtering
- Shopping cart functionality
- Secure checkout process
- Order tracking and history
- User profile management

### 👨‍💼For Shopkeepers
- Product management (add/edit/delete)
- Order management and tracking
- Sales summary and analytics
- Inventory management
- User management

## ⚙️Technology Stack
- **Backend**: Django 5.x
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite

## 📁Project Structure
```
shopingcart/
├── final_shop/          # Main project directory
├── myapp/              # Main application directory
├── templates/          # HTML templates
├── static/            # Static files (CSS, JS, images)
├── media/             # User-uploaded files
├── manage.py          # Django management script
└── db.sqlite3         # Database file
```

## 🖥️Installation and Setup

1. **Clone the repository**
```bash
git clone https://github.com/tejasvini2006/Ecommerce-Website.git
cd Ecommerce-Website
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
# For Windows:
venv\Scripts\activate
# For Linux/Mac:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create a superuser**
```bash
python manage.py createsuperuser
```

6. **Start the development server**
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## 🔐Login
### Admin Login
The admin can log in using superuser credentials. If you have not created one yet, run:
```bash
python manage.py createsuperuser
```

### User Login
Users can log in through the Login Page using their credentials. New users can sign up via the Signup Page.

## 🔍Explore Features

### 👤For Customers
- Register a new account or login
- Browse products
- Add items to cart
- Proceed to checkout
- Track orders

### 👨‍💼For Shopkeepers
- Login with shopkeeper credentials
- Access admin dashboard
- Manage products and orders
- View sales analytics

## 📌Closing Remarks
This project demonstrates practical implementation of Django web development and aims to solve real-world problems in e-commerce. We hope this platform continues to evolve with more advanced features in the future, helping create smarter and more efficient ways to manage online shopping.

Feel free to fork this repository and make improvements. Your contributions are welcome!

Thank you for your interest in our E-Commerce Platform!
