from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AddressModel, CurrentAddressModel
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(post_save, sender=AddressModel)
def create_or_update_current_address(sender, instance, created, **kwargs):
    if created:
        # Check if a current address already exists for the user
        CurrentAddressModel.objects.update_or_create(user=instance.user, defaults={'address': instance})


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.email,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            # instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            'https://healfit.ae/reset-password/',
            reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('email/password_reset_email.html', context)
    email_plaintext_message = render_to_string('email/password_reset_email.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Healfit.ae"),
        # message:
        email_plaintext_message,
        # from:
        "no-reply@healfit.ae",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
