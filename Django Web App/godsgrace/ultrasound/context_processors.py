from .models import Notification

def notifications_processor(request):  # <-- rename this
    if request.user.is_authenticated:
        notifications = request.user.notifications.all().order_by('-created_at')[:5]
        unread_notifications_count = request.user.notifications.filter(is_read=False).count()
    else:
        notifications = []
        unread_notifications_count = 0

    return {
        'notifications': notifications,
        'unread_notifications_count': unread_notifications_count,
    }
