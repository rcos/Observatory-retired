from django.core.mail import EmailMessage
from emaillist.models import EmailAddress
from django.core.urlresolvers import reverse
from settings import SITE_ADDRESS

def send_mail(subject, body, from_email, recipient_list, fail_silently=False):
    to = [addr for addr in recipient_list if not EmailAddress.is_excluded(addr)]

    #Doing a separate email for each person so we can allow unsubscription links
    for addr in to:

        print "Emailing: %s" % addr
        print "Subject: %s" % subject

        #For now use default email body with an unsubscribe link
        html_content = '%s <br><a href="%s"> Unsubscribe From RCOS Emails</a>' % (body, SITE_ADDRESS + reverse('emaillist.views.remove_email', args=[addr]))

        msg = EmailMessage(subject, html_content, from_email, [addr])
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send(fail_silently = fail_silently)
