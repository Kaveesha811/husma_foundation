import streamlit as st
import os
import sys
from datetime import datetime, date

# Add the current directory to Python path
sys.path.append(os.path.dirname(__file__))

# Import custom modules
try:
    from config import config
    from database.operations import init_database, get_next_donor_id
    from database.operations import create_donor, get_donor_by_username, get_donor_by_email
    from database.operations import get_inventory, get_low_stock_items, update_inventory_stock, update_inventory
    from database.operations import create_donation, get_donations_by_donor, get_donation_analytics
    from database.operations import create_child, get_children, get_child_by_id, create_issue, get_issues_by_child, \
        update_child_last_issue
    from database.operations import get_all_donations
    from auth.authentication import hash_password, check_password, authenticate_user, validate_password_strength
    from auth.validation import validate_nic, validate_phone, validate_email, validate_password
    from services.email_service import send_verification_email, send_donation_receipt_email
    from services.sms_service import send_donation_confirmation_sms
    from services.report_service import display_analytics_dashboard
    from utils.helpers import setup_directories, generate_receipt_number, get_stock_status, allowed_file, \
        create_placeholder_images
except ImportError as e:
    st.error(f"Import error: {e}")
    st.info("Please make sure all required files are in the correct directories")

# Page configuration
st.set_page_config(
    page_title="Husma Foundation - Donation System",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)


def initialize_app():
    """Initialize the application"""
    try:
        setup_directories()
        create_placeholder_images()
        init_database()
        return True
    except Exception as e:
        st.error(f"Initialization error: {e}")
        return False


# Initialize application
if not initialize_app():
    st.stop()


# Apply custom CSS
def load_css():
    css_file = "static/css/style.css"
    if os.path.exists(css_file):
        with open(css_file, encoding='utf-8') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        # Fallback basic CSS
        st.markdown("""
        <style>
        .main { font-family: Arial, sans-serif; }
        .header { background-color: #2E86AB; color: white; padding: 2rem; border-radius: 10px; margin-bottom: 2rem; }
        .header h1 { margin: 0; font-size: 2.5rem; }
        .header p { margin: 0.5rem 0 0 0; opacity: 0.9; }
        .card { background: white; border-radius: 10px; padding: 1.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 1rem; }
        .stButton>button { border-radius: 8px; font-weight: 600; }
        .stButton>button:first-child { background-color: #2E86AB; color: white; }
        .product-card { border: 1px solid #ddd; border-radius: 10px; padding: 1rem; margin: 0.5rem 0; }
        .admin-section { background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 10px; padding: 1rem; margin: 1rem 0; }
        .login-form { background: #f8f9fa; padding: 2rem; border-radius: 10px; border: 1px solid #dee2e6; }
        </style>
        """, unsafe_allow_html=True)


load_css()


# Session state initialization
def initialize_session_state():
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    if 'admin_logged_in' not in st.session_state:
        st.session_state.admin_logged_in = False
    if 'checkout_active' not in st.session_state:
        st.session_state.checkout_active = False
    if 'selected_child_history' not in st.session_state:
        st.session_state.selected_child_history = None
    if 'show_login' not in st.session_state:
        st.session_state.show_login = False


initialize_session_state()


# Navigation function
def navigate_to(page):
    st.session_state.current_page = page
    st.session_state.show_login = False
    st.rerun()


# Header Section
def show_header():
    st.markdown("""
    <div class="header">
        <h1>❤️ Husma Foundation</h1>
        <p>Nourishing Little Warriors Fighting Cancer at Apeksha Hospital</p>
    </div>
    """, unsafe_allow_html=True)


# Home Page
def show_home():
    show_header()

    st.markdown("""
    ## Welcome to Husma Foundation

    We provide essential nutritional supplements to children battling cancer at Apeksha Hospital, 
    Maharagama. Your donations help ensure these brave children receive the nutrition they need 
    during their treatment journey.
    """)

    # Mission and Vision
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 🎯 Our Mission
        To provide continuous nutritional support to pediatric cancer patients, 
        ensuring they have access to essential supplements during their treatment.
        """)

    with col2:
        st.markdown("""
        ### 🌟 Our Vision
        A Sri Lanka where no child fighting cancer lacks access to proper nutrition, 
        enabling better treatment outcomes and improved quality of life.
        """)

    # Distribution Schedule
    st.markdown("### 📅 Our Distribution Schedule")
    st.markdown("""
    We are committed to consistency. You can find us distributing supplements every:
    - **Tuesday, Wednesday, and Thursday**
    - **From 9:00 AM to 12:00 PM**  
    - **Near the Apeksha Hospital (Cancer Hospital), Maharagama**
    """)

    # Quick Stats
    st.markdown("### 📈 Quick Statistics")

    try:
        analytics = get_donation_analytics()
        children = get_children()
        inventory = get_inventory()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Donations", f"LKR {analytics.get('total_amount', 0):,.2f}")

        with col2:
            st.metric("Children Supported", len(children))

        with col3:
            st.metric("Active Donors", analytics.get('unique_donors', 0))

        with col4:
            total_stock = sum(item['stock'] for item in inventory)
            st.metric("Total Stock", total_stock)
    except Exception as e:
        st.warning("Statistics temporarily unavailable")

    # Call to Action
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("👤 Register Now", use_container_width=True):
            navigate_to("Register")
    with col2:
        if st.button("💝 Donate Now", use_container_width=True):
            navigate_to("Donate")
    with col3:
        if st.button("📊 View Dashboard", use_container_width=True):
            navigate_to("Dashboard")


# Login Form
def show_login_form():
    st.markdown("### 🔐 Login to Your Account")

    with st.form("login_form"):
        username = st.text_input("Username or Email")
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button("Login", type="primary", use_container_width=True)

        if submitted:
            if not username or not password:
                st.error("Please enter both username and password")
                return

            donor = authenticate_user(username, password)
            if donor:
                st.session_state.user = {
                    'donor_id': donor['donor_id'],
                    'name': donor['name'],
                    'username': donor['username'],
                    'email': donor['email'],
                    'phone': donor['phone']
                }
                st.success(f"Welcome back, {donor['name']}!")
                st.session_state.show_login = False
                st.rerun()
            else:
                st.error("Invalid username or password")


# Registration Page - ONLY FOR REGISTRATION
def show_register():
    show_header()
    st.markdown("## 👤 Create Your Donor Account")

    # Show login option if user wants to login instead
    if not st.session_state.user:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔐 Already have an account? Login here", use_container_width=True):
                st.session_state.show_login = True
                st.rerun()

    if st.session_state.show_login:
        show_login_form()
        return

    with st.form("registration_form"):
        st.markdown("### Personal Information")

        col1, col2 = st.columns(2)

        with col1:
            full_name = st.text_input("Full Name *", placeholder="Enter your full name")
            nic = st.text_input("NIC Number *", placeholder="Enter your NIC number")
            phone = st.text_input("Phone Number *", placeholder="07XXXXXXXX")

        with col2:
            email = st.text_input("Email Address", placeholder="your.email@example.com")
            username = st.text_input("Username *", placeholder="Choose a username")
            password = st.text_input("Password *", type="password", placeholder="Create a strong password")

        # Password strength indicator
        if password:
            is_valid, message = validate_password_strength(password)
            if is_valid:
                st.success("✅ " + message)
            else:
                st.error("❌ " + message)

        st.markdown("---")
        st.markdown("**Terms & Conditions**")
        st.markdown("""
        - I agree to provide accurate information
        - I understand that my donations will be used to support children with cancer
        - I consent to receive communication regarding my donations
        """)

        agree_terms = st.checkbox("I agree to the terms and conditions *")

        submitted = st.form_submit_button("Create Account", type="primary", use_container_width=True)

        if submitted:
            # Validate required fields
            if not all([full_name, nic, phone, username, password]):
                st.error("Please fill in all required fields (*)")
                return

            if not validate_nic(nic):
                st.error("Please enter a valid NIC number (10 or 12 digits)")
                return

            if not validate_phone(phone):
                st.error("Please enter a valid 10-digit phone number")
                return

            if email and not validate_email(email):
                st.error("Please enter a valid email address")
                return

            if not agree_terms:
                st.error("Please agree to the terms and conditions")
                return

            try:
                # Check if username or email already exists
                if get_donor_by_username(username):
                    st.error("Username already exists. Please choose a different one.")
                    return

                if email and get_donor_by_email(email):
                    st.error("Email already registered. Please use a different email or login.")
                    return

                # Create new donor
                donor_id = get_next_donor_id()
                hashed_password = hash_password(password)

                create_donor((
                    donor_id, full_name, nic, phone, email,
                    username, hashed_password
                ))

                # Send welcome email
                if email:
                    send_verification_email(email, full_name)

                st.success(f"🎉 Account created successfully! Your Donor ID is: **{donor_id}**")
                st.info("You can now login and start making donations.")

                # Auto-login
                st.session_state.user = {
                    'donor_id': donor_id,
                    'name': full_name,
                    'username': username,
                    'email': email,
                    'phone': phone
                }

                st.balloons()

            except Exception as e:
                st.error(f"Registration failed: {str(e)}")


# Milk Powder Catalog Section
def show_milk_catalog():
    st.markdown("## 🥛 Nutritional Supplements Catalog")
    st.markdown("""
    A single tin of specialized nutritional milk formula costs LKR 3,900. 
    You can donate any number of tins to directly impact a child's life. 
    **We require 1,500 tins every month** to meet the growing need.
    """)

    inventory = get_inventory()

    # Display products in a grid
    cols = st.columns(3)
    for idx, product in enumerate(inventory):
        with cols[idx % 3]:
            with st.container():
                st.markdown(f"""
                <div class="product-card">
                    <h4>{product['name']}</h4>
                    <p><strong>Price:</strong> LKR {product['price']:,.2f}</p>
                    <p><strong>Stock:</strong> {product['stock']} units</p>
                </div>
                """, unsafe_allow_html=True)

                # Display product image
                image_path = product.get('image_path', f"static/images/{product['name'].lower().replace(' ', '_')}.jpg")
                if os.path.exists(image_path):
                    st.image(image_path, width=200, caption=product['name'])
                else:
                    st.info(f"🖼️ {product['name']} Image")

                # Add to cart functionality
                if product['stock'] > 0:
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        quantity = st.number_input(
                            f"Quantity",
                            min_value=0,
                            max_value=min(product['stock'], 20),
                            value=0,
                            key=f"qty_{product['product_id']}",
                            label_visibility="collapsed"
                        )
                    with col2:
                        if quantity > 0:
                            if st.button("🛒 Add", key=f"add_{product['product_id']}"):
                                # Add to cart
                                cart_item = {
                                    'product_id': product['product_id'],
                                    'name': product['name'],
                                    'price': product['price'],
                                    'quantity': quantity,
                                    'subtotal': product['price'] * quantity
                                }

                                # Check if item already in cart
                                existing_index = next((i for i, item in enumerate(st.session_state.cart)
                                                       if item['product_id'] == product['product_id']), None)

                                if existing_index is not None:
                                    st.session_state.cart[existing_index] = cart_item
                                else:
                                    st.session_state.cart.append(cart_item)

                                st.success(f"Added {quantity} {product['name']} to cart!")
                                st.rerun()
                else:
                    st.warning("Out of Stock")


# Shopping Cart Section
def show_shopping_cart():
    if not st.session_state.cart:
        st.info("🛒 Your cart is empty. Add some products from the catalog above!")
        return

    st.markdown("## 🛒 Your Shopping Cart")

    total_amount = 0
    tax_rate = 0.01  # 1% tax

    for item in st.session_state.cart:
        if item['quantity'] > 0:
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1:
                st.write(f"**{item['name']}**")
            with col2:
                st.write(f"Qty: {item['quantity']}")
            with col3:
                st.write(f"LKR {item['subtotal']:,.2f}")
            with col4:
                if st.button("❌ Remove", key=f"remove_{item['product_id']}"):
                    st.session_state.cart = [i for i in st.session_state.cart if i['product_id'] != item['product_id']]
                    st.rerun()

            total_amount += item['subtotal']

    if total_amount > 0:
        tax_amount = total_amount * tax_rate
        final_total = total_amount + tax_amount

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Subtotal:** LKR {total_amount:,.2f}")
            st.write(f"**Tax (1%):** LKR {tax_amount:,.2f}")
            st.write(f"**Total:** LKR {final_total:,.2f}")

        with col2:
            if st.button("💳 Proceed to Checkout", type="primary", use_container_width=True):
                st.session_state.checkout_active = True
                st.rerun()


# Checkout Section
def show_checkout():
    st.markdown("## 💳 Checkout")

    st.info(f"Donor: **{st.session_state.user['name']}** (ID: {st.session_state.user['donor_id']})")

    # Display cart summary
    total_amount = sum(item['subtotal'] for item in st.session_state.cart)
    tax_amount = total_amount * 0.01
    final_total = total_amount + tax_amount

    st.markdown(f"""
    **Order Summary:**
    - Subtotal: LKR {total_amount:,.2f}
    - Tax (1%): LKR {tax_amount:,.2f}
    - **Total: LKR {final_total:,.2f}**
    """)

    # Bank transfer details
    st.markdown("### 🏦 Bank Transfer Details")
    st.markdown(f"""
    <div style="background: #f0f8ff; padding: 20px; border-radius: 10px; border-left: 4px solid #2E86AB;">
        <h4 style="color: #2E86AB; margin-top: 0;">Please transfer to:</h4>
        <p><strong>Account Name:</strong> Husma Foundation</p>
        <p><strong>Account Number:</strong> 106914030823</p>
        <p><strong>Bank:</strong> Sampath Bank, Homagama</p>
        <p><strong>Branch:</strong> Homagama</p>
        <p><strong>Amount:</strong> LKR {final_total:,.2f}</p>
    </div>
    """, unsafe_allow_html=True)

    # Payment slip upload
    st.markdown("### 📎 Upload Payment Slip")
    uploaded_file = st.file_uploader(
        "Upload your bank transfer confirmation slip",
        type=['png', 'jpg', 'jpeg', 'pdf'],
        help="Supported formats: PNG, JPG, JPEG, PDF (Max 5MB)"
    )

    remarks = st.text_area("Remarks (Optional)", placeholder="Any additional comments about your donation...")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Cart", use_container_width=True):
            st.session_state.checkout_active = False
            st.rerun()

    with col2:
        if st.button("✅ Confirm Donation", type="primary", use_container_width=True):
            if final_total == 0:
                st.error("Please add items to your cart first")
                return

            try:
                # Process donation
                payment_slip_path = None
                if uploaded_file:
                    # Save uploaded file
                    upload_dir = "instance/uploads"
                    os.makedirs(upload_dir, exist_ok=True)
                    filename = f"payment_{st.session_state.user['donor_id']}_{datetime.now().timestamp()}.{uploaded_file.type.split('/')[-1]}"
                    payment_slip_path = os.path.join(upload_dir, filename)

                    with open(payment_slip_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                # Record donation
                create_donation(
                    st.session_state.user['donor_id'],
                    final_total,
                    payment_slip_path
                )

                # Update inventory
                for item in st.session_state.cart:
                    if item['quantity'] > 0:
                        update_inventory_stock(item['product_id'], item['quantity'])

                # Generate receipt
                receipt_number = generate_receipt_number()

                # Send notifications
                if st.session_state.user.get('email'):
                    send_donation_receipt_email(
                        st.session_state.user['email'],
                        st.session_state.user['name'],
                        {
                            'amount': final_total,
                            'date': datetime.now().strftime('%Y-%m-%d'),
                            'receipt_number': receipt_number
                        }
                    )

                if st.session_state.user.get('phone'):
                    send_donation_confirmation_sms(
                        st.session_state.user['phone'],
                        st.session_state.user['name'],
                        final_total
                    )

                st.success(f"🎉 Thank you for your donation of LKR {final_total:,.2f}!")
                st.info(f"**Receipt Number:** {receipt_number}")

                # Clear cart
                st.session_state.cart = []
                st.session_state.checkout_active = False

                # Show receipt
                from utils.pdf_generator import generate_donation_receipt
                generate_donation_receipt(
                    {
                        'amount': final_total,
                        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'receipt_number': receipt_number
                    },
                    st.session_state.user
                )

            except Exception as e:
                st.error(f"Donation failed: {str(e)}")


# Donate Page - ONLY FOR DONATIONS
def show_donate():
    show_header()

    if not st.session_state.user:
        st.warning("🔒 Please login or register to make a donation")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("👤 Register New Account", use_container_width=True):
                navigate_to("Register")
        with col2:
            if st.button("🔐 Login to Existing Account", use_container_width=True):
                st.session_state.show_login = True
                st.rerun()

        if st.session_state.show_login:
            show_login_form()
        return

    st.markdown(f"## 💝 Make a Donation")
    st.info(f"Welcome back, **{st.session_state.user['name']}**! (Donor ID: {st.session_state.user['donor_id']})")

    # Check if checkout is active
    if st.session_state.get('checkout_active'):
        show_checkout()
    else:
        # Show catalog and cart
        show_milk_catalog()
        st.markdown("---")
        show_shopping_cart()


# Admin Login Section
def admin_login():
    st.markdown("### 🔒 Admin Login")

    with st.form("admin_login_form"):
        username = st.text_input("Admin Username")
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button("Login", type="primary")

        if submitted:
            if username == "admin" and password == "admin123":
                st.session_state.admin_logged_in = True
                st.success("Admin access granted!")
                st.rerun()
            else:
                st.error("Invalid admin credentials")


# Children Management (Admin Only)
def show_children_management():
    if not st.session_state.admin_logged_in:
        admin_login()
        return

    st.markdown("## 👶 Children Management")

    # Add new child form
    with st.expander("➕ Add New Child", expanded=True):
        with st.form("add_child_form"):
            col1, col2 = st.columns(2)

            with col1:
                child_name = st.text_input("Child's Name *")
                birthday = st.date_input("Birthday *", max_value=date.today())
                milk_type = st.selectbox("Milk Type *",
                                         ["Pediasure", "Ensure", "Sustagen",
                                          "Pediasure Gold", "Ensure Complete", "Sustagen Junior"])

            with col2:
                guardian = st.text_input("Guardian's Name *")
                phone = st.text_input("Guardian's Phone *")
                issue_today = st.checkbox("Issue milk today")

            if st.form_submit_button("Add Child"):
                if all([child_name, guardian, phone, milk_type]):
                    try:
                        create_child((child_name, birthday.isoformat(), guardian, phone, milk_type))

                        # Issue milk if requested
                        if issue_today:
                            children = get_children()
                            if children:
                                child_id = children[-1]['id']  # Get the latest child ID
                                today = date.today().isoformat()
                                create_issue(child_id, today, milk_type)
                                update_child_last_issue(child_id, today)
                                # Find the product ID for the milk type
                                inventory = get_inventory()
                                product_id = next((p['product_id'] for p in inventory if p['name'] == milk_type), None)
                                if product_id:
                                    update_inventory_stock(product_id, 1)
                                st.success(f"Child {child_name} added and milk issued for today!")
                            else:
                                st.success(f"Child {child_name} added successfully!")
                        else:
                            st.success(f"Child {child_name} added successfully!")

                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to add child: {str(e)}")
                else:
                    st.error("Please fill all required fields (*)")

    # Search and display children
    st.markdown("### 📋 Registered Children")

    search_name = st.text_input("🔍 Search by child name")
    children = get_children(search_name)

    if children:
        for child in children:
            with st.expander(f"👶 {child['name']} - {child['milk_type']}"):
                col1, col2, col3 = st.columns([2, 1, 1])

                with col1:
                    st.write(f"**Guardian:** {child['guardian']}")
                    st.write(f"**Phone:** {child['phone']}")
                    st.write(f"**Birthday:** {child['birthday']}")
                    st.write(f"**Milk Type:** {child['milk_type']}")
                    if child['last_issue']:
                        st.write(f"**Last Issue:** {child['last_issue']}")

                with col2:
                    # Issue milk button
                    if st.button("🥛 Issue Milk", key=f"issue_{child['id']}"):
                        try:
                            today = date.today().isoformat()
                            create_issue(child['id'], today, child['milk_type'])
                            update_child_last_issue(child['id'], today)
                            # Update inventory
                            inventory = get_inventory()
                            product_id = next((p['product_id'] for p in inventory if p['name'] == child['milk_type']),
                                              None)
                            if product_id:
                                update_inventory_stock(product_id, 1)
                            st.success(f"Milk issued to {child['name']} for today!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to issue milk: {str(e)}")

                with col3:
                    # View history button
                    if st.button("📊 History", key=f"history_{child['id']}"):
                        st.session_state.selected_child_history = child['id']
                        st.rerun()

                # Show history if selected
                if st.session_state.get('selected_child_history') == child['id']:
                    st.markdown("#### Issue History")
                    issues = get_issues_by_child(child['id'])
                    if issues:
                        for issue in issues:
                            st.write(f"- {issue['date']}: {issue['milk_type']}")
                    else:
                        st.info("No issue history found")
    else:
        st.info("No children registered yet")


def show_inventory_management():
    st.markdown("### 📦 Inventory Management")
    inventory = get_inventory()

    for product in inventory:
        with st.expander(f"{product['name']} - Stock: {product['stock']}"):
            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**Current Stock:** {product['stock']}")
                st.write(f"**Price:** LKR {product['price']:,.2f}")
                st.write(f"**Min Stock Level:** {product['min_stock_level']}")

                status, color = get_stock_status(product['stock'], product['min_stock_level'])
                st.write(f"**Status:** {status}")

            with col2:
                adjustment = st.number_input(
                    f"Stock Adjustment",
                    value=0,
                    key=f"adj_{product['product_id']}",
                    help="Positive to add stock, negative to remove"
                )

                if st.button(f"Update Stock", key=f"btn_{product['product_id']}"):
                    try:
                        update_inventory(product['product_id'], adjustment)
                        st.success(f"Stock updated for {product['name']}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Update failed: {str(e)}")

    # Low stock alert
    low_stock = get_low_stock_items()
    if low_stock:
        st.warning("🚨 Low Stock Alert!")
        for item in low_stock:
            st.error(f"{item['name']}: Only {item['stock']} units left!")


def show_donation_management():
    st.markdown("### 💰 All Donations")

    try:
        donations = get_all_donations()

        if donations:
            total = sum(d['amount'] for d in donations)
            st.metric("Total Donations Received", f"LKR {total:,.2f}")

            for donation in donations:
                with st.container():
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                    with col1:
                        donor_name = donation.get('donor_name', 'Anonymous')
                        st.write(f"**{donor_name}** ({donation['donor_id']})")
                    with col2:
                        st.write(f"LKR {donation['amount']:,.2f}")
                    with col3:
                        st.write(f"{donation['timestamp'][:10]}")
                    with col4:
                        if donation.get('payment_slip'):
                            st.write("📎 Slip")
        else:
            st.info("No donations recorded yet")

    except Exception as e:
        st.error(f"Error loading donations: {str(e)}")
        st.info("This feature is being updated. Please check back later.")


# Admin Dashboard
def show_admin_dashboard():
    if not st.session_state.admin_logged_in:
        admin_login()
        return

    st.markdown("## 🔧 Admin Dashboard")

    # Admin tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📦 Inventory", "👶 Children", "💰 Donations", "📊 Analytics"])

    with tab1:
        show_inventory_management()

    with tab2:
        show_children_management()

    with tab3:
        show_donation_management()

    with tab4:
        try:
            display_analytics_dashboard()
        except Exception as e:
            st.error(f"Error loading analytics: {e}")


# Dashboard Page
def show_dashboard():
    show_header()
    st.markdown("## 📊 Donation Dashboard")

    if not st.session_state.user:
        st.warning("Please login to view your dashboard")
        show_login_form()
        return

    # Analytics Overview
    try:
        display_analytics_dashboard()
    except Exception as e:
        st.warning("Analytics temporarily unavailable")

    # Recent Donations
    st.markdown("---")
    st.markdown("### 📋 Your Donation History")

    if st.session_state.user:
        try:
            donations = get_donations_by_donor(st.session_state.user['donor_id'])
            if donations:
                for donation in donations:
                    with st.container():
                        col1, col2, col3 = st.columns([2, 1, 1])
                        with col1:
                            st.write(f"**Date:** {donation['timestamp'][:10]}")
                        with col2:
                            st.write(f"**Amount:** LKR {donation['amount']:,.2f}")
                        with col3:
                            if donation['payment_slip']:
                                st.write("📎 Slip Attached")
                st.markdown(f"**Total Donated:** LKR {sum(d['amount'] for d in donations):,.2f}")
            else:
                st.info("No donations yet. Make your first donation today!")
        except Exception as e:
            st.warning("Unable to load donation history")


# Contact Page
def show_contact():
    show_header()
    st.markdown("## 📞 Contact Us")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### Get in Touch

        **Husma Foundation**  
        278/1, Katuwana Road,  
        Homagama, Sri Lanka

        **Phone Numbers:**  
        📞 0777348822  
        📞 0777138822

        **Email:**  
        📧 husmafoundation@gmail.com

        **Bank Details:**  
        🏦 Sampath Bank, Homagama  
        💳 Account: 106914030823
        """)

    with col2:
        st.markdown("""
        ### Our Mission

        Husma Foundation is dedicated to providing nutritional 
        support to children battling cancer at Apeksha Hospital, 
        Maharagama.

        We believe that proper nutrition plays a vital role in 
        helping these little warriors fight cancer and recover 
        successfully.

        Your donations help us provide essential nutritional 
        supplements to children in need.
        """)


# Sidebar Navigation
def show_sidebar():
    with st.sidebar:
        # Logo and header
        st.markdown("""
        <div style="text-align: center;">
            <h2>❤️ Husma Foundation</h2>
            <p><i>Nourishing Little Warriors</i></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Navigation menu
        menu_items = [
            ("🏠", "Home", "Home"),
            ("👤", "Register", "Register"),
            ("💰", "Donate", "Donate"),
            ("📊", "Dashboard", "Dashboard"),
            ("📞", "Contact", "Contact"),
        ]

        for icon, label, page in menu_items:
            if st.button(f"{icon} {label}", key=f"nav_{page}", use_container_width=True):
                navigate_to(page)

        # Admin section
        st.markdown("---")
        st.markdown("**Admin Access**")
        if st.button("🔧 Admin Panel", key="nav_Admin", use_container_width=True):
            navigate_to("Admin")

        st.markdown("---")

        # User info
        if st.session_state.user:
            st.success(f"**Welcome, {st.session_state.user['name']}!**")
            st.info(f"Donor ID: `{st.session_state.user['donor_id']}`")

            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.user = None
                st.session_state.cart = []
                st.session_state.admin_logged_in = False
                st.session_state.checkout_active = False
                st.session_state.show_login = False
                st.rerun()


# Main application router
def main():
    show_sidebar()

    # Page routing
    if st.session_state.current_page == "Home":
        show_home()
    elif st.session_state.current_page == "Register":
        show_register()
    elif st.session_state.current_page == "Donate":
        show_donate()
    elif st.session_state.current_page == "Dashboard":
        show_dashboard()
    elif st.session_state.current_page == "Contact":
        show_contact()
    elif st.session_state.current_page == "Admin":
        show_admin_dashboard()


if __name__ == "__main__":
    main()