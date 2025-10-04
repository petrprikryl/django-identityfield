from django.conf import settings
from django.db import DEFAULT_DB_ALIAS
from testcontainers.postgres import PostgresContainer

postgres = PostgresContainer("postgres:18-alpine")


def pytest_configure():
    postgres.start()

    settings.configure(
        INSTALLED_APPS=["identityfield"],
        DATABASES={
            DEFAULT_DB_ALIAS: {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": postgres.dbname,
                "USER": postgres.username,
                "PASSWORD": postgres.password,
                "HOST": postgres.get_container_host_ip(),
                "PORT": postgres.get_exposed_port(5432),
            }
        },
    )


def pytest_sessionfinish(session, exitstatus):
    postgres.stop()
