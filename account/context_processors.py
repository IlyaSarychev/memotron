from .models import Notification


def notifications(request):
    return {
        'new_notifications': Notification.objects.filter(is_viewed=False)
    }