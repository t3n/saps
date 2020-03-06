from time import localtime, strftime
from django.db import models
from django.contrib.auth.models import User


class OAuth2Token(models.Model):
    name = models.CharField(max_length=40)
    token_type = models.CharField(max_length=40)
    access_token = models.CharField(max_length=5000)
    refresh_token = models.CharField(max_length=5000)
    expires_at = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'OAuth2Token'
        verbose_name_plural = 'OAuth2Tokens'

    def __str__(self):
        return self.user.email + '-' + strftime('%Y-%m-%d %H:%M:%S', localtime(self.expires_at))

    def to_token(self):
        return dict(
            access_token=self.access_token,
            token_type=self.token_type,
            refresh_token=self.refresh_token,
            expires_at=self.expires_at,
        )
