from django.db import models
from django.db.models import Value


class Identity:
    ALWAYS = "ALWAYS"
    BY_DEFAULT = "BY DEFAULT"


class IdentityFieldBase(models.GeneratedField):
    """A PostgreSQL identity column.

    `GeneratedField` is the only field Django keeps out of both the INSERT and
    the UPDATE value list, which `GENERATED ALWAYS AS IDENTITY` requires. The
    clause itself comes from the schema editor patch in `apps.py`.
    """

    # On the class, not a kwarg: `deconstruct()` drops `output_field`, so
    # migrations rebuild the field from the class.
    output_field_class: type[models.Field] = models.IntegerField

    def __init__(self, *, identity=Identity.BY_DEFAULT, **kwargs):
        self.identity = identity
        for reserved in ("expression", "output_field", "db_persist"):
            if reserved in kwargs:
                raise TypeError(
                    f"{type(self).__name__} does not accept {reserved!r}; "
                    "set output_field_class on a subclass instead."
                )
        kwargs["db_persist"] = True
        kwargs["output_field"] = self.output_field_class()
        # References nothing: Django walks every generated field's expression
        # when a sibling column is dropped.
        kwargs["expression"] = Value(None)
        super().__init__(**kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        for key in ("expression", "output_field", "db_persist"):
            del kwargs[key]
        if self.identity != Identity.BY_DEFAULT:
            kwargs["identity"] = self.identity
        return name, path, args, kwargs

    def identity_sql(self) -> tuple[str, tuple]:
        return f"GENERATED {self.identity} AS IDENTITY", ()

    def generated_sql(self, connection):
        # Only `alter_field()`'s precheck reads this; the DDL comes from
        # `identity_sql()`.
        return self.identity_sql()


class IdentityField(IdentityFieldBase):
    output_field_class = models.IntegerField


class BigIdentityField(IdentityFieldBase):
    output_field_class = models.BigIntegerField
