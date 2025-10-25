import streamlit as st
from datetime import datetime


def generate_donation_receipt(donation_data, donor_data):
    """Generate donation receipt (simulated)"""
    receipt_content = f"""
    HUSMA FOUNDATION - DONATION RECEIPT
    ====================================

    Receipt Number: {donation_data['receipt_number']}
    Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

    Donor Information:
    - Name: {donor_data['name']}
    - Donor ID: {donor_data['donor_id']}
    - NIC: {donor_data['nic']}
    - Phone: {donor_data['phone']}

    Donation Details:
    - Amount: LKR {donation_data['amount']:,.2f}
    - Date: {donation_data['date']}
    - Payment Method: Bank Transfer

    Thank you for your generous donation!

    Contact Information:
    Husma Foundation
    278/1, Katuwana Road, Homagama
    0777348822 / 0777138822
    """

    st.info(f"""
    **📄 Receipt Generated: {donation_data['receipt_number']}**

    ```
    {receipt_content}
    ```

    *In production, this would generate a PDF file*
    """)

    return receipt_content