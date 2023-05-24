from django.core.mail import send_mail

# send information about a new order to the operator
def send_email_info(subject, message,recipient):
    send_mail(subject, message, 'kyzlos@gmail.com', recipient)
