from django.core.mail import EmailMessage
from emaillist.models import EmailExclusion

def send_mail(subject, body, from_email, recipient_list, fail_silently=False):
    to = [addr for addr in recipient_list if not EmailExclusion.excluded(addr)]

    for addr in to:

        #For now use default email body with an unsubscribe link
        html_content = '%s <br><a href="http://rcos.rpi.edu/email/remove/%s"> Unsubscribe From RCOS Emails</a>' % (body, addr)

        msg = EmailMessage(subject, html_content, from_email, [addr])
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send(fail_silently = fail_silently)
