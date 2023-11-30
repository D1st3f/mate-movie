from django.core.mail import send_mail


def send_activation_email(email: str):
    send_mail(
        subject="Account activation",
        message="Your account is pending activation",
        from_email="noreply@example.com",
        recipient_list=[email]
    )