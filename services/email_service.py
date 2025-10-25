import streamlit as st


def send_email(to_email, subject, body, is_html=False):
    """
    Simulate email sending - shows email in Streamlit
    In production, replace with real email service
    """
    st.info(f"""
    **📧 Email Notification**

    **To:** {to_email}
    **Subject:** {subject}

    {body}

    *In production, this would be sent via SMTP*
    """)
    return True


def send_verification_email(email, donor_name):
    """Send email verification"""
    subject = "Welcome to Husma Foundation - Verify Your Email"
    body = f"""
    Dear {donor_name},

    Thank you for registering with Husma Foundation!

    Your account has been successfully created and verified.

    You can now login and start making donations to support children fighting cancer.

    Best regards,
    Husma Foundation Team
    """

    return send_email(email, subject, body)


def send_password_reset_email(email, donor_name):
    """Send password reset instructions"""
    subject = "Password Reset Instructions - Husma Foundation"
    body = f"""
    Dear {donor_name},

    We received a request to reset your password.

    Please contact our support team at 0777348822 for assistance with password reset.

    Best regards,
    Husma Foundation Team
    """

    return send_email(email, subject, body)


def send_donation_receipt_email(email, donor_name, donation_data):
    """Send donation receipt via email"""
    subject = "Donation Receipt - Husma Foundation"

    body = f"""
    Dear {donor_name},

    Thank you for your generous donation of LKR {donation_data['amount']:,.2f}!

    **Donation Details:**
    - Amount: LKR {donation_data['amount']:,.2f}
    - Date: {donation_data['date']}
    - Receipt Number: {donation_data['receipt_number']}

    Your support helps provide nutritional supplements to children fighting cancer at Apeksha Hospital.

    **Bank Details for Future Donations:**
    Account: Husma Foundation
    Number: 106914030823
    Bank: Sampath Bank, Homagama

    Best regards,
    Husma Foundation Team
    """

    return send_email(email, subject, body)