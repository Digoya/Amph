from journal.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist


def menu(request):
    try:
        user = UserProfile.objects.get(user__username=request.user)
    except ObjectDoesNotExist:
        return {'user': None, 'user_auth': False}
    if request.user.is_authenticated:

        return {'user': user, 'user_auth': True}
    else:
        return {'user': None, 'user_auth': False}
