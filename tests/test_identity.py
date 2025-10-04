from __future__ import annotations

import pytest
from django.db import models, connection

from identityfield import IdentityField


class IdentityModel(models.Model):
    class Meta:
        app_label = "testapp"

    objects: models.Manager[IdentityModel] = models.Manager()

    sequence = IdentityField()


@pytest.fixture(scope="module", autouse=True)
def create_schema(django_db_blocker):
    with django_db_blocker.unblock():
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(IdentityModel)

        yield


@pytest.fixture
def last_sequence():
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT last_value, is_called FROM {IdentityModel._meta.db_table}_sequence_seq"  # ty: ignore[unresolved-attribute]
        )
        val, is_called = cursor.fetchone()
        return val if is_called else val - 1


@pytest.mark.db
def test_insert(last_sequence):
    assert IdentityModel.objects.create().sequence == last_sequence + 1
    assert IdentityModel.objects.create().sequence == last_sequence + 2


@pytest.mark.db
def test_update(last_sequence):
    im = IdentityModel.objects.create()
    assert im.sequence == last_sequence + 1

    im.save()
    assert im.sequence == last_sequence + 1

    im.sequence = 0
    im.save()
    assert im.sequence == 0

    assert IdentityModel.objects.create().sequence == last_sequence + 2


@pytest.mark.db
def test_delete(last_sequence):
    im = IdentityModel.objects.create()
    assert im.sequence == last_sequence + 1
    im.delete()

    assert IdentityModel.objects.create().sequence == last_sequence + 2
