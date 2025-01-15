from django.core.mail import EmailMessage


def send_inactivity_notification(user):
    subject = f"Inactivity Notification - user ID: {user.id}"
    body = "You haven't logged into your account for 30 days."
    from_email = "your-email@gmail.com"
    to_email = [user.email]

    email = EmailMessage(subject, body, from_email, to_email)

    try:
        email.send(fail_silently=False)
        print("Notification sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")