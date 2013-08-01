from emaillist.models import EmailExclusion
from django.shortcuts import render_to_response

def remove_email(request, email):
    if email[-1] == '/':
        email = email[:-1]

    #Only exclude an email once
    if EmailExclusion.excluded(email):
        return render_to_response('emaillist/email_removed.html')

    #Exclude the email
    exclude = EmailExclusion(email=email)
    exclude.save()

    #Find the user who pressed the exclude button
    user = None

    return render_to_response('emaillist/email_removed.html')
