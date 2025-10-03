from django.apps import AppConfig
from django.db.backends.postgresql.schema import DatabaseSchemaEditor

from identityfield import IdentityMixin


class IdentityFieldConfig(AppConfig):
    name = "identityfield"

    def ready(self):
        # Nasty monkey patch to override the generated clause
        def patched__column_generated_sql(self, field):
            if isinstance(field, IdentityMixin):
                return field.identity_sql()

            return super(DatabaseSchemaEditor, self)._column_generated_sql(field)

        DatabaseSchemaEditor._column_generated_sql = patched__column_generated_sql
