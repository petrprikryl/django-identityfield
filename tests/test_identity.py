import pytest
from django.db import connection

from tests.app.models import IdentityModel


@pytest.fixture
def last_sequence():
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT last_value, is_called FROM app_identitymodel_sequence_seq"
        )
        val, is_called = cursor.fetchone()
        return val if is_called else val - 1


@pytest.mark.django_db
def test_insert(last_sequence):
    assert IdentityModel.objects.create().sequence == last_sequence + 1
    assert IdentityModel.objects.create().sequence == last_sequence + 2


@pytest.mark.django_db
def test_update(last_sequence):
    im = IdentityModel.objects.create()
    assert im.sequence == last_sequence + 1

    im.save()
    assert im.sequence == last_sequence + 1

    im.sequence = 0
    im.save()
    assert im.sequence == 0

    assert IdentityModel.objects.create().sequence == last_sequence + 2


@pytest.mark.django_db
def test_delete(last_sequence):
    im = IdentityModel.objects.create()
    assert im.sequence == last_sequence + 1
    im.delete()

    assert IdentityModel.objects.create().sequence == last_sequence + 2
