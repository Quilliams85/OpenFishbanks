from django.core.mail import send_mail

def send_invitation_email(invitation):
    subject = f"Invitation to join {invitation.group.name}"
    message = f"Hi {invitation.recipient.username},\n\nYou have been invited to join {invitation.group.name} by {invitation.sender.username}.\n\nPlease visit the site to accept or decline the invitation."
    send_mail(subject, message, 'noreply@example.com', [invitation.recipient.email])