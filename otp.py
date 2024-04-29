import smtplib
import random
from twilio.rest import Client

def initialize_twilio_client():
    account_sid = " "
    auth_token = " "
    return Client(account_sid, auth_token)

def initialize_twilio_service(twilio_client):
    service_sid = " "
    return twilio_client.verify.v2.services(service_sid)

def send_sms(phone_number):
    try:
        twilio_client = initialize_twilio_client()
        twilio_service = initialize_twilio_service(twilio_client)

        otp_request = twilio_service.verifications.create(
            to = f'+91{phone_number}',
            channel = "sms"
        )
        return True

    except Exception as exc:
        print("Error Occurred:\n", exc)

def verify_sms(phone_number, otp_input):
    try:
        twilio_client = initialize_twilio_client()
        twilio_service = initialize_twilio_service(twilio_client)

        otp_verification = twilio_service.verification_checks.create(
            to = f'+91{phone_number}',
            code = otp_input
        )

        if otp_verification.status == "approved":
            return True
        else:
            return False

    except Exception as exc:
        print("Error Occurred:\n", exc)

def email(username, email, otp_input):
    otp = "".join([str(random.randint(0, 9)) for _ in range(6)])

    subject = "Archiva Security Team"
    body = f'Hey {username}, Welcome to Archiva!\n\nYour One-Time Password is: {otp}'
    message = f'{subject}\n\n{body}'

    try:
        server = smtplib.SMTP("smtp.google.com", 587)
        server.starttls()
        server.login("security@archiva.org", " ")
        server.sendmail("security@archiva.org", email, message)
        server.quit()

        if otp_input == otp:
            return True
        else:
            return False

    except Exception as exc:
        print("Error Occurred:\n", exc)