import streamlit as st


def send_sms(phone_number, message):
    """
    Simulate SMS sending
    In production, replace with real SMS service like Twilio
    """
    st.info(f"""
    **📱 SMS Notification**

    **To:** {phone_number}
    **Message:** {message}

    *In production, this would be sent via SMS gateway*
    """)
    return True


def send_donation_confirmation_sms(phone_number, donor_name, amount):
    """Send donation confirmation SMS"""
    message = f"Thank you {donor_name}! Your donation of LKR {amount:,.2f} to Husma Foundation has been received. Your support helps children fighting cancer."
    return send_sms(phone_number, message)


def send_password_reset_sms(phone_number, donor_name):
    """Send password reset SMS"""
    message = f"Hi {donor_name}, for password reset assistance, please contact Husma Foundation at 0777348822."
    return send_sms(phone_number, message)