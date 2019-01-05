from . import models


def secret(request):
    return {
        'secret': models.Secret.objects.first()
    }
