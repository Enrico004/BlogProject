from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from blog.models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    method which gets called every time a user creates a profile
    :param sender: model that notifies this method
    :param instance: profile instance that is created
    :param created: true if profile is newly created
    :param kwargs:
    :return:
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    method that gets called every time a user saves a profile
    :param sender: model that notifies the receiver -> method when an event occurs
    :param instance: profile instance that is saved
    :param kwargs:
    :return:
    """
    instance.profile.save()