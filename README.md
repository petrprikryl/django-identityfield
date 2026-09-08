# identityfield

Auto-incrementing fields like Django `AutoField` but without restrictions!

This reusable app provides fields that are using PostgreSQL `GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY`.
Same as Django `AutoField`. But without `primary_key=true` limitation.

## Installation
https://pypi.org/project/django-identityfield/
* `uv add django-identityfield`
* add `"identityfield"` to your `settings.INSTALLED_APPS`

## Usage

```python
from django.db import models
from identityfield import IdentityField, Identity


class HappyModel(models.Model):
    sequence = IdentityField()
    # ALWAYS rejects any value other than DEFAULT in UPDATE
    always_sequence = IdentityField(identity=Identity.ALWAYS)
```

DB sequences are automatically created by PostgreSQL.
And are automatically incremented on DB side.

https://www.postgresql.org/docs/current/ddl-identity-columns.html

## Available fields

| Field              | Column    |
|--------------------|-----------|
| `IdentityField`    | `integer` |
| `BigIdentityField` | `bigint`  |

Need a different column type? Subclass and set `output_field_class`:

```python
from django.db import models
from identityfield import IdentityFieldBase


class SmallIdentityField(IdentityFieldBase):
    output_field_class = models.SmallIntegerField
```

## Limitations

* PostgreSQL only. The app patches the PostgreSQL schema editor on startup,
  because Django has no hook for a generated column whose clause is not an
  expression.
* The database owns the value, so the field is not `editable`. It never shows
  up in ModelForms or the admin, and assigning to it has no effect on `save()`.
* `default` and `db_default` are rejected, an identity column cannot have one.
* `identity` is keyword-only. Pass other options by keyword as well, including
  `verbose_name`.
* Changing the identity clause, or switching between an identity field and a
  plain one, cannot be done in place. Django tells you to remove and re-add the
  field. Widening the column (`IdentityField` to `BigIdentityField`) does work.
  Changing `null` slips past that check and fails in the database instead.
* `primary_key=True` produces valid DDL but breaks on the first `create()`.
  Use Django's `AutoField` or `BigAutoField` for the primary key.

## Running test suite

```bash
uv run --frozen pytest
uvx tox
```

`--frozen` keeps `uv run` from re-resolving. Without it, a `UV_DEFAULT_INDEX`
pointing at a private registry silently rewrites every `source` in `uv.lock`.
