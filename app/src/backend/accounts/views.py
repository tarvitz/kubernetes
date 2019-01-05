from django.contrib import auth

from django.urls import reverse_lazy
from django.views.generic import View
from django.http import HttpResponseRedirect


class LogoutView(View):
    """
    Log-outs user on methods:

    - GET
    - POST

    Returns redirect to index page
    """
    def logout(self):
        if self.request.user.is_authenticated:
            auth.logout(self.request)

    def _method(self, request):
        self.logout()
        return HttpResponseRedirect(redirect_to=reverse_lazy('static:index'))

    def get(self, request):
        return self._method(request)

    def post(self, request):
        return self._method(request)
