from journal.models import UserProfile


def menu(request):
    if request.user.is_authenticated:
        user = UserProfile.objects.get(user__username=request.user)
        return {'user': user, 'user_auth': True}
    else:
        return {'user': None, 'user_auth': False}
