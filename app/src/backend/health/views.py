from django.views.generic import View
from django.http import HttpResponse
from django.db.utils import OperationalError

from django.contrib.auth import get_user_model

from .. consts import HttpStatus


def _app_health_check():
    """
    Checks health of running application. This function should be as simple
    and as fastest as possible

    :raises django.db.utils.OperationalError:
        - if connection to database was lost
    :rtype: None
    :return: None
    """
    get_user_model().objects.exists()


class StatusView(View):
    def get(self, request):
        return HttpResponse('ok')


class HealthView(View):
    """
    Health View
    """
    def get(self, request):
        try:
            _app_health_check()
        except OperationalError:
            return HttpResponse("fail", status=HttpStatus.DOWN)
        except Exception:
            return HttpResponse("fail <unhandled exception>",
                                status=HttpStatus.DOWN)
        return HttpResponse("ok", status=HttpStatus.OK)
