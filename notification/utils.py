from django.conf import settings

from pyfcm import FCMNotification

from ..models import UserDevice


def send_fcm_notification(title="", body="", data=None, users=None):
    """
    sends fcm notification to a single or multiple user device
    :param title: title of the notification message
    :param body: body of the notification
    :param data: any data to be sent
    :param users: list of user ids
    :return: True/False
    """
    if users:
        push_service = FCMNotification(api_key=settings.FCM_API_KEY)
        try:
            if data:
                if isinstance(users, list):
                    registration_ids = [
                        devices.registration_id for devices in UserDevice.objects.filter(used_id__in=users)]
                    push_service.multiple_devices_data_message(
                        registration_ids=registration_ids,
                        data_message=data
                    )
                else:
                    registration_id = UserDevice.objects.get(user_id=users).registration_id
                    push_service.single_device_data_message(
                        registration_id=registration_id,
                        data_message=data
                    )
            else:
                if isinstance(users, list):
                    registration_ids = [
                        devices.registration_id for devices in UserDevice.objects.filter(user_id__in=users)]
                    push_service.notify_multiple_devices(
                        registration_ids=registration_ids,
                        message_title=title,
                        message_body=body
                    )
                else:
                    registration_id = UserDevice.objects.get(user_id=users).registration_id
                    push_service.notify_single_device(
                        registration_id=registration_id,
                        message_title=title,
                        message_body=body
                    )
            return True
        except:
            return False
    else:
        return False
