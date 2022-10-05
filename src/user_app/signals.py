from django.db.models.signals import post_save, post_delete, m2m_changed

from user_app.models import UserAccount, UserOTP
from user_app import logger


class UserAccountSignalReciever:
    """
    Class to store all signals used in the storyapp.
    """
    model = UserAccount

    @classmethod
    def user_created(cls, sender, instance: UserAccount, created, **kwargs):
        """
        Signal to send when a story is created.
        """
        if created:
            pass

    @classmethod
    def user_updated(cls, sender, instance: UserAccount, created, **kwargs):
        """
        Signal to send when a story is updated.
        """
        if not created:
            pass

    @classmethod
    def user_deleted(cls, sender, instance: UserAccount, **kwargs):
        """
        Signal to send when a story is deleted.
        """
        pass


## Signal to send when a user is created.
post_save.connect(receiver=UserAccountSignalReciever.user_created,
                  sender=UserAccountSignalReciever.model)
## Signal to send when a user is updated.
post_save.connect(receiver=UserAccountSignalReciever.user_updated,
                  sender=UserAccountSignalReciever.model)
## Signal to send when a user is deleted.
post_delete.connect(receiver=UserAccountSignalReciever.user_deleted,
                    sender=UserAccountSignalReciever.model)


class UserOTPSignalReciever:

    model = UserOTP

    @classmethod
    def instance_created(cls, sender, instance: UserOTP, created, *args, **kwargs):
        if created:
            logger.info(
                f"New OTP for User '{instance.user.email}' created with Transaction ID '{instance.id}.'")

    @classmethod
    def instance_verified(cls, sender, instance: UserOTP, created, *args, **kwargs):
        if instance.verified and not created:
            logger.info(f"OTP '{instance.id}.' for User '{instance.user.email}' verified.")

    @classmethod
    def instance_deleted(cls, sender, instance: UserOTP, created, *args, **kwargs):
        logger.info(
            f"OTP <{instance.id}> for User '{instance.user.email}' deleted.'")


post_save.connect(receiver=UserOTPSignalReciever.instance_created, sender=UserOTPSignalReciever.model)
post_save.connect(receiver=UserOTPSignalReciever.instance_verified, sender=UserOTPSignalReciever.model)
post_delete.connect(receiver=UserOTPSignalReciever.instance_deleted, sender=UserOTPSignalReciever.model)
