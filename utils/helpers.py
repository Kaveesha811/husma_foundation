import os
import secrets
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont


def setup_directories():
    """Create necessary directories"""
    directories = [
        "instance/uploads",
        "temp/receipts",
        "static/images",
        "static/css",
        "templates/email_templates"
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)


def allowed_file(filename):
    """Check if file type is allowed"""
    allowed_extensions = {'png', 'jpg', 'jpeg', 'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def generate_receipt_number():
    """Generate unique receipt number"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_part = secrets.token_hex(3).upper()
    return f"HF{timestamp}{random_part}"


def format_currency(amount):
    """Format amount as currency"""
    return f"LKR {amount:,.2f}"


def get_stock_status(stock, min_stock):
    """Get stock status with color coding"""
    if stock == 0:
        return "Out of Stock", "red"
    elif stock <= min_stock * 0.3:
        return "Critical", "red"
    elif stock <= min_stock:
        return "Low", "orange"
    else:
        return "Good", "green"


def create_placeholder_images():
    """Create placeholder images if they don't exist"""
    images_info = {
        "husma_logo.png": "Husma Foundation\nLogo",
        "husma_fb_image.jpg": "Husma Foundation\nTeam Photo",
        "pediasure.jpg": "Pediasure\nNutritional Milk",
        "ensure.jpg": "Ensure\nNutrition Shake",
        "sustagen.jpg": "Sustagen\nMilk Powder",
        "pediasure_gold.jpg": "Pediasure Gold\nPremium Nutrition",
        "ensure_complete.jpg": "Ensure Complete\nBalanced Nutrition",
        "sustagen_junior.jpg": "Sustagen Junior\nChildren's Formula"
    }

    for filename, text in images_info.items():
        filepath = f"static/images/{filename}"
        if not os.path.exists(filepath):
            # Create a simple placeholder image
            img = Image.new('RGB', (300, 200), color=(73, 109, 137))
            d = ImageDraw.Draw(img)

            # Try to use a font, fallback to default
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except:
                font = ImageFont.load_default()

            # Add text to image
            lines = text.split('\n')
            y_offset = 70
            for line in lines:
                bbox = d.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                x = (300 - text_width) // 2
                d.text((x, y_offset), line, fill=(255, 255, 255), font=font)
                y_offset += text_height + 10

            img.save(filepath)
            print(f"Created placeholder image: {filepath}")

# Remove the display_image function for now as it requires streamlit