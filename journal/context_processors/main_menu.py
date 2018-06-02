from django.template.context_processors import request
from journal.models import UserProfile


def menu(request):
    if request.user.is_authenticated:
        user = UserProfile.objects.get(user__username=request.user)
        return {'user': user, 'user_auth': True}
    else:
        return {'user_auth': False}
