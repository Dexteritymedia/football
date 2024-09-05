from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.contrib.auth import get_user_model

@receiver(user_signed_up)
def add_initial_credits(sender, request, user):
    user.user_credits = 10
    user.save()

    print(f"{user.username} was given 10 credits upon signup.")
