"""
contact/views.py
Handles the public contact form: save to DB and email the team.
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .forms import ContactForm


def contact_view(request):
    """Render and process the contact form."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_msg = form.save()

            # Send notification email to the TalentHeart team
            _send_notification_email(contact_msg)

            messages.success(
                request,
                'Thank you for reaching out! We will get back to you within 24 hours.'
            )
            return redirect('contact:contact')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form})


# ---------------------------------------------------------------------------
# Internal helper
# ---------------------------------------------------------------------------
def _send_notification_email(msg):
    """Send a notification to the CONTACT_EMAIL address when a form is submitted."""
    subject = f'[TalentHeart] New Contact: {msg.subject}'
    body = (
        f'You have a new contact message from the website.\n\n'
        f'Name:    {msg.name}\n'
        f'Email:   {msg.email}\n'
        f'Phone:   {msg.phone or "—"}\n'
        f'Subject: {msg.subject}\n\n'
        f'Message:\n{msg.message}\n'
    )
    try:
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [settings.CONTACT_EMAIL],
            fail_silently=True,       # don't blow up the page if mail is misconfigured
        )
    except Exception:
        pass  # Log in production via Sentry / logging framework
