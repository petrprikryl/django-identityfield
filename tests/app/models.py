from django.db import models

from identityfield import IdentityField


class IdentityModel(models.Model):
    sequence = IdentityField()
