import streamlit as st
import pandas as pd
from datetime import datetime
from decimal import Decimal
import os
import calendar

from database.operations import get_conn, create_tables, add_donor, find_donor_by_id, get_donors, add_donation, update_inventory, get_donations_by_donor, add_child, get_children, update_child, delete_child, get_child_by_id, add_issue, get_issues_by_child, update_child_last_issue
from auth.validation import validate_nic, validate_phone, validate_password
from auth.authentication import hash_password, check_login
from utils.helpers import get_next_donor_id, allowed_file
from services.email_service import send_email
from services.sms_service import send_sms

# Initialize DB
conn = get_conn()
create_tables(conn)

# Inventory initialization if empty
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM inventory")
if cursor.fetchone()[0] == 0:
    products = [
        (1, "Pediasure", 3900.00, 100, "static/images/pediasure.jpg"),
        (2, "Ensure", 3500.00, 80, "static/images/ensure.jpg"),
        (3, "Sustagen", 3200.00, 120, "static/images/sustagen.jpg"),
        (4, "Pediasure Gold", 4100.00, 90, "static/images/pediasure_gold.jpg"),
        (5, "Ensure Complete", 3800.00, 70, "static/images/ensure_complete.jpg"),
        (6, "Sustagen Junior", 3000.00, 110, "static/images/sustagen_junior.jpg"),
    ]
    cursor.executemany("INSERT INTO inventory VALUES (?, ?, ?, ?, ?)", products)
    conn.commit()

# Sidebar Navigation
pages = ["Home", "Donor Registration", "Donate", "Donor Dashboard", "Contact Us", "Admin - Children Registration", "Admin - Issue Milk Powder", "Admin - Reports"]
st.sidebar.title("Husma Foundation")
page = st.sidebar.selectbox("Go to", pages)

if page == "Home":
    st.title("Nourishing Little Warriors, One Meal at a Time")
    if os.path.exists("static/images/husma_logo.png"):
        st.image("static/images/husma_logo.png", width=200)
    st.write("At the Husma Foundation, our hearts are dedicated to a single, powerful mission: ensuring that no child fighting cancer has to fight malnutrition as well.")
    st.write("We have witnessed the brave little souls undergoing intensive treatments, often left with painful mouth sores that make the simple act of eating an impossible challenge. Seeing them struggle to eat is what moved us to act. That's why we provide essential nutritional supplements free of charge to these incredible little warriors, giving their tiny bodies the strength to endure and heal.")
    st.subheader("How You Can Help Make a Difference")
    st.write("The need is constant, and your support, in any form, is what keeps this mission alive.")
    st.write("1. Donate Nutritional Supplements: A single tin of specialized nutritional milk formula (like Pediasure) costs LKR 3,900. You can donate any number of tins to directly impact a child's life. We require 1,500 tins every month to meet the growing need.")
    st.write("2. Make a Monetary Donation: If you find it difficult to visit us, you can easily contribute through a bank transfer. Our account details are available on our page. Every rupee brings us closer to our goal.")
    st.write("3. Join Us in Person: We invite you to be a part of our distribution days. Come, hand a tin to a child, share a smile, and feel the profound joy of giving firsthand. Your personal connection means the world to them.")
    st.subheader("Our Distribution Schedule")
    st.write("We are committed to consistency. You can find us distributing supplements every:")
    st.write("- Tuesday, Wednesday, and Thursday")
    st.write("- From 9:00 AM to 12:00 PM")
    st.write("- Near the Apeksha Hospital (Cancer Hospital), Maharagama.")
    st.write("Our distributions are timed to conclude after the children's morning clinics, ensuring they receive this vital support when they need it most.")
    if os.path.exists("static/images/husma_fb_image.jpg"):
        st.image("static/images/husma_fb_image.jpg", caption="Husma Team")

elif page == "Donor Registration":
    st.title("Donor Registration")
    donor_nic = st.text_input("NIC Number")
    donor_name = st.text_input("Donor Name")
    donor_phone = st.text_input("Telephone Number")
    donor_email = st.text_input("Email (Optional)")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if not validate_nic(donor_nic):
            st.error("Enter a valid NIC number with 10 or 12 characters.")
        elif not validate_phone(donor_phone):
            st.error("Enter a valid telephone number with 10 digits.")
        elif not validate_password(password):
            st.error("Password must be at least 8 characters, with uppercase, lowercase, digit, and special character.")
        else:
            cursor.execute("SELECT * FROM donors WHERE nic = ?", (donor_nic,))
            if cursor.fetchone():
                st.error("Donor with this NIC already registered.")
            else:
                donor_id = get_next_donor_id(conn)
                hashed_password = hash_password(password)
                add_donor(conn, donor_id, donor_name, donor_nic, donor_phone, donor_email, username, hashed_password)
                st.success(f"Donor registered! ID: {donor_id}")
    # Search Donor
    search_id = st.text_input("Search Donor by ID (e.g., D001)")
    if st.button("Search"):
        donor = find_donor_by_id(conn, search_id)
        if donor:
            st.write("Found Donor:")
            st.json(donor)
        else:
            st.error("Donor not found.")

elif page == "Donate":
    st.title("Donate")
    # Optional Donor Login
    st.subheader("Login as Donor (Optional - To Track Donations and Send Confirmation)")
    donor_username = st.text_input("Username")
    donor_password = st.text_input("Password", type="password")
    donor_id = None
    donor_phone = None
    donor_email = None
    if st.button("Login"):
        result = check_login(conn, donor_username, donor_password)
        if result:
            donor_id, donor_phone, donor_email = result
            st.success("Logged in!")
        else:
            st.error("Invalid credentials.")
    # For anonymous, optional contact for confirmation
    if not donor_id:
        st.subheader("Anonymous Donation? Provide Contact for Confirmation (Optional)")
        donor_phone = st.text_input("Phone for SMS")
        donor_email = st.text_input("Email for Confirmation")

    if 'cart' not in st.session_state:
        st.session_state.cart = []
    st.subheader("Product Catalog")
    cursor.execute("SELECT * FROM inventory")
    products = [{"id": row[0], "name": row[1], "price": Decimal(str(row[2])), "stock": row[3], "image": row[4]} for row in cursor.fetchall()]
    for product in products:
        col1, col2 = st.columns(2)
        with col1:
            if os.path.exists(product['image']):
                st.image(product['image'], width=100)
            else:
                st.write("(Image not found)")
        with col2:
            st.write(f"{product['name']} - LKR {product['price']}")
            st.write(f"Stock: {product['stock']}")
            qty = st.number_input(f"Quantity for {product['name']}", min_value=0, max_value=product['stock'], key=f"qty_{product['id']}")
            if st.button(f"Add to Cart", key=f"add_{product['id']}"):
                if qty > 0:
                    st.session_state.cart.append({"product": product, "qty": qty})
                    st.success(f"Added {qty} of {product['name']} to cart.")
    # Cart
    if st.session_state.cart:
        st.subheader("Shopping Cart")
        total = Decimal("0")
        for i, item in enumerate(st.session_state.cart):
            subtotal = item['product']['price'] * Decimal(item['qty'])
            st.write(f"{item['product']['name']} x {item['qty']} = LKR {subtotal}")
            if st.button(f"Remove {item['product']['name']}", key=f"remove_{i}"):
                st.session_state.cart.pop(i)
                st.success("Item removed.")
            total += subtotal
        tax = total * Decimal("0.01")
        grand_total = total + tax
        st.write(f"Subtotal: LKR {total}")
        st.write(f"Tax (1%): LKR {tax}")
        st.write(f"Grand Total: LKR {grand_total}")
        if st.button("Clear Cart"):
            st.session_state.cart = []
            st.success("Cart cleared.")
    else:
        grand_total = Decimal("0")
    # Direct Monetary Donation
    st.subheader("Or Make a Direct Monetary Donation")
    monetary_amount = st.number_input("Amount (LKR)", min_value=0.0)
    if monetary_amount > 0:
        grand_total += Decimal(monetary_amount)
        st.write(f"Added Monetary Donation: LKR {monetary_amount}")
    # Checkout
    st.subheader("Checkout")
    uploaded_file = st.file_uploader("Upload Payment Slip (Proof of Bank Transfer)", type=['png', 'jpg', 'jpeg', 'pdf'])
    if uploaded_file and st.button("Submit Donation"):
        if allowed_file(uploaded_file.name):
            if uploaded_file.size > 5 * 1024 * 1024:
                st.error("File too large. Max 5MB.")
            else:
                filename = uploaded_file.name  # Use secure_filename if using Werkzeug, but simplified
                os.makedirs("instance/uploads", exist_ok=True)
                save_path = os.path.join("instance/uploads", filename)
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                donor_id_to_save = donor_id if donor_id else "anonymous"
                add_donation(conn, donor_id_to_save, float(grand_total), save_path, datetime.now().isoformat())
                # Update Stock if cart
                for item in st.session_state.cart:
                    update_inventory(conn, item['product']['id'], item['qty'])
                # Send Confirmation if contact provided
                message = f"Thank you for your donation of LKR {grand_total}! Your support helps children in need."
                if donor_phone:
                    send_sms(donor_phone, message)
                if donor_email:
                    send_email(donor_email, message)
                st.session_state.cart = []
                st.success("Thank you! Donation submitted.")
        else:
            st.error("Invalid file type.")
    st.subheader("Bank Details")
    st.write("Account Name: Husma Foundation")
    st.write("Account Number: 106914030823")
    st.write("Bank: Sampath Bank")
    st.write("Branch: Homagama")

elif page == "Donor Dashboard":
    st.title("Donor Dashboard - View Past Donations")
    donor_username = st.text_input("Username")
    donor_password = st.text_input("Password", type="password")
    if st.button("Login to View"):
        result = check_login(conn, donor_username, donor_password)
        if result:
            donor_id, _, _ = result
            donations = get_donations_by_donor(conn, donor_id)
            if donations:
                df = pd.DataFrame(donations, columns=["Amount (LKR)", "Timestamp", "Payment Slip"])
                st.dataframe(df)
            else:
                st.write("No past donations found.")
        else:
            st.error("Invalid credentials.")

elif page == "Contact Us":
    st.title("Contact Us")
    st.subheader("Categories")
    st.write("Charity organization")
    st.subheader("Address")
    st.write("278/1, Katuwana Road, Homagama, Sri Lanka, 10200")
    st.subheader("Service Area")
    st.write("Colombo, Sri Lanka · Maharagama, Sri Lanka · Homagama, Sri Lanka")
    st.subheader("Mobile")
    st.write("0777348822 / 0777138822")
    st.subheader("Facebook")
    st.markdown("[Husma Foundation](https://www.facebook.com/husmafoundationlk)")
    st.subheader("Account Information")
    st.write("Account Name: Husma Foundation")
    st.write("Account Number: 106914030823")
    st.write("Bank: Sampath Bank")
    st.write("Branch: Homagama")
    st.write("Husma Foundation is a government-registered and audited account for the medicine and nutritional needs of children with cancer.")
    st.write("Please avoid depositing any financial donations made to the Husma Fund into any individual's account or any other account.")
    st.write("For more information, please contact: 0777348822 / 0777138822")

elif page == "Admin - Children Registration":
    st.title("Children Registration (Admin Only)")
    admin_pass = st.text_input("Admin Password", type="password")
    if admin_pass != "admin123":
        st.error("Access Denied")
        st.stop()
    # Left: Management, Right: List
    left, right = st.columns(2)
    with left:
        st.subheader("Add/Update Child")
        child_id = st.text_input("Child ID to Update (Leave blank for new)")
        name = st.text_input("Child's Name")
        birthday = st.date_input("Birthday")
        guardian = st.text_input("Guardian's Name")
        phone = st.text_input("Phone Number")
        milk_type = st.selectbox("Milk Powder Type", ["Pediasure", "Ensure", "Sustagen", "Pediasure Gold", "Ensure Complete", "Sustagen Junior"])
        if st.button("Save Child"):
            if not validate_phone(phone):
                st.error("Invalid phone number (10 digits).")
            else:
                if child_id:
                    update_child(conn, child_id, name, birthday.isoformat(), guardian, phone, milk_type)
                    st.success("Child updated!")
                else:
                    add_child(conn, name, birthday.isoformat(), guardian, phone, milk_type)
                    st.success("Child registered!")
    with right:
        st.subheader("Registered Children")
        search_name = st.text_input("Search by Name")
        children = get_children(conn, search_name)
        if children:
            df = pd.DataFrame(children, columns=["ID", "Name", "Birthday", "Guardian", "Phone", "Milk Type", "Last Issue"])
            st.dataframe(df)
            delete_id = st.text_input("Child ID to Delete")
            if st.button("Delete Child"):
                delete_child(conn, delete_id)
                st.success("Child deleted!")
        else:
            st.write("No children registered.")

elif page == "Admin - Issue Milk Powder":
    st.title("Issue Milk Powder (Admin Only)")
    admin_pass = st.text_input("Admin Password", type="password")
    if admin_pass != "admin123":
        st.error("Access Denied")
        st.stop()
    # Two-panel layout
    left, right = st.columns(2)
    with left:
        st.subheader("Select Child")
        search_name = st.text_input("Search by Name")
        children = get_children(conn, search_name)
        if children:
            df = pd.DataFrame(children, columns=["ID", "Name", "Birthday", "Guardian", "Phone", "Milk Type", "Last Issue"])
            st.dataframe(df)
        selected_child_id = st.text_input("Enter Child ID to Issue")
    with right:
        if selected_child_id:
            child = get_child_by_id(conn, selected_child_id)
            if child:
                st.subheader(f"Selected Child: {child[1]}")
                st.write(f"Milk Type: {child[5]}")
                st.subheader("Calendar View")
                today = datetime.now()
                year = st.number_input("Year", value=today.year)
                month = st.number_input("Month", min_value=1, max_value=12, value=today.month)
                # Get issued dates for month
                issues = get_issues_by_child(conn, selected_child_id)
                issued_days = {datetime.fromisoformat(issue[0]).day for issue in issues if datetime.fromisoformat(issue[0]).year == year and datetime.fromisoformat(issue[0]).month == month}
                cal = calendar.monthcalendar(year, month)
                for week in cal:
                    cols = st.columns(7)
                    for i, day in enumerate(week):
                        if day == 0:
                            cols[i].write("")
                        else:
                            is_issued = day in issued_days
                            is_today = (day == today.day and month == today.month and year == today.year)
                            button_type = "primary" if is_today else "secondary"
                            if cols[i].button(str(day), key=f"issue_{year}_{month}_{day}_{selected_child_id}", type=button_type):
                                issue_date = datetime(year, month, day).isoformat()
                                add_issue(conn, selected_child_id, issue_date, child[5])
                                update_child_last_issue(conn, selected_child_id, issue_date)
                                st.success(f"Issued on {issue_date}")
                            if is_issued:
                                cols[i].markdown("<p style='color:red; font-size:12px;'>Issued</p>", unsafe_allow_html=True)
                if st.button("Issue Today"):
                    today_str = today.isoformat()
                    add_issue(conn, selected_child_id, today_str, child[5])
                    update_child_last_issue(conn, selected_child_id, today_str)
                    st.success("Issued today!")
                st.subheader("Issue History")
                issues = get_issues_by_child(conn, selected_child_id)
                if issues:
                    df = pd.DataFrame(issues, columns=["Date", "Milk Type"])
                    st.dataframe(df)
                    st.write(f"Total Issues: {len(df)}")
                else:
                    st.write("No issues yet.")
            else:
                st.error("Child not found.")

elif page == "Admin - Reports":
    st.title("Reports (Admin Only)")
    admin_pass = st.text_input("Admin Password", type="password")
    if admin_pass != "admin123":
        st.error("Access Denied")
        st.stop()
    st.subheader("Inventory Levels")
    cursor.execute("SELECT name, stock FROM inventory")
    inventory = pd.DataFrame(cursor.fetchall(), columns=["Product", "Stock"])
    st.dataframe(inventory)
    st.bar_chart(inventory.set_index("Product"))
    st.subheader("Donations Summary")
    cursor.execute("SELECT donor_id, amount, timestamp FROM donations")
    donations = pd.DataFrame(cursor.fetchall(), columns=["Donor ID", "Amount", "Timestamp"])
    if not donations.empty:
        donations["Timestamp"] = pd.to_datetime(donations["Timestamp"])
        total_donations = donations["Amount"].sum()
        st.write(f"Total Donations: LKR {total_donations}")
        monthly = donations.resample("M", on="Timestamp")["Amount"].sum()
        st.line_chart(monthly)
        st.dataframe(donations)
    else:
        st.write("No donations yet.")
    st.subheader("Distribution Summary")
    cursor.execute("SELECT child_id, date, milk_type FROM issues")
    issues = pd.DataFrame(cursor.fetchall(), columns=["Child ID", "Date", "Milk Type"])
    if not issues.empty:
        issues["Date"] = pd.to_datetime(issues["Date"])
        total_issues = len(issues)
        st.write(f"Total Distributions: {total_issues}")
        monthly_issues = issues.resample("M", on="Date").size()
        st.line_chart(monthly_issues)
        st.dataframe(issues)
    else:
        st.write("No distributions yet.")

# Close conn (good practice)
conn.close()