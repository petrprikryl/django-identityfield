# identityfield

Auto-incrementing fields like Django `AutoField` but without restrictions!

This reusable app provides fields that are using PostgreSQL `GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY`.
Same as Django `AutoField`. But without `primary_key=true` limitation.

## Installation
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

## Running test suite

```bash
uv run pytest
```
