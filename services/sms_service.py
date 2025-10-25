def send_sms(phone, message):
    print(f"SMS to {phone}: {message}")
    # For real SMS, use Twilio (sign up at twilio.com, get account SID, auth token, phone number):
    # from twilio.rest import Client
    # client = Client('your_sid', 'your_token')
    # client.messages.create(to=phone, from_='your_twilio_number', body=message)