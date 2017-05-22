from django.conf import settings


def settings_variables(request):
    return {
        'SHOW_SPEAKERS_LIST_NAVBAR_LINK': getattr(settings, 'SHOW_SPEAKERS_LIST_NAVBAR_LINK', False)
    }
