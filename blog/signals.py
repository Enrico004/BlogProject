from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from blog.models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Methode, die aufgerufen wird, sobald ein User-Profil erstellt wird
    :param sender: Modell, welches die Methode benachrichtigt
    :param instance: Erstellte Profil-Instanz
    :param created: Gibt an, ob das Profil neu erstellt wurde
    :param kwargs:
    :return:
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    Methode, die jedes Mal aufgerufen wird, sobald ein User-Profil gespeichert wird.
    Speichert das dazugehörige Profil (Avatar)
    :param sender: Modell, welches die Methode benachrichtigt
    :param instance: Zu speichernde Profil-Instanz
    :param kwargs:
    :return:
    """
    instance.profile.save()