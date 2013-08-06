from emaillist.models import EmailAddress
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist

def remove_email(request, email):
    if email[-1] == '/':
        email = email[:-1]

    try:
        addr = EmailAddress.objects.filter(address=email).get()
    except EmailAddress.DoesNotExist:
        return render_to_response('emaillist/email_removed.html')

    if addr.excluded:
        return render_to_response('emaillist/email_removed.html')

    #Exclude the email
    addr.excluded = True
    addr.save()

    #Find the user who pressed the exclude button
    user = addr.user

    return render_to_response('emaillist/email_removed.html')
