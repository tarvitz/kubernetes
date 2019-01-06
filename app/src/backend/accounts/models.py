from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    """
    standard django user
    """
    is_verified = models.BooleanField(
        _('is verified'),
        default=False,
        help_text=_("flag that shows if user is verified and can "
                    "obtain main functionality")
    )


class Secret(models.Model):
    content = models.TextField(
        _("content"),
        help_text=_("secret content, i.e. password or something you should "
                    "not tell without using secure channels")
    )
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = _("Secret")
        verbose_name_plural = _("Secrets")
        ordering = ['-created_at']
