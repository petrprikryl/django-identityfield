from django.db import models


class Identity:
    ALWAYS = "ALWAYS"
    BY_DEFAULT = "BY DEFAULT"


class IdentityMixin:
    generated = True

    def __init__(self, identity=Identity.BY_DEFAULT, *args, **kwargs):
        self.identity = identity
        kwargs["blank"] = True
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["blank"]
        if self.identity != Identity.BY_DEFAULT:
            kwargs["identity"] = self.identity
        return name, path, args, kwargs

    @property
    def db_returning(self):
        return True

    def identity_sql(self) -> tuple[str, tuple]:
        return f"GENERATED {self.identity} AS IDENTITY", ()


class IdentityField(IdentityMixin, models.IntegerField):
    pass


class BigIdentityField(IdentityMixin, models.BigIntegerField):
    pass


class PositiveIdentityField(IdentityMixin, models.PositiveIntegerField):
    pass


class PositiveBigIdentityField(IdentityMixin, models.PositiveBigIntegerField):
    pass
