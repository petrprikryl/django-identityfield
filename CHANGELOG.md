# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.3.0 - 2026-09-08

### Changed

* Identity fields are real `GeneratedField` subclasses instead of a mixin that
  only claimed `generated = True`. Django reaches for `expression`,
  `output_field`, `db_persist`, `referenced_fields` and `generated_sql()` on
  every generated field, and each had to be hand-rolled and kept in sync with
  new Django releases. `IdentityField()` still takes the same arguments and
  serializes into migrations unchanged.
* `IdentityMixin` is now `IdentityFieldBase`, and it is a base class rather
  than a mixin. A `GeneratedField` takes its column from `output_field`, not
  from the MRO, so `class Foo(IdentityMixin, models.SmallIntegerField)` no
  longer picks the column type -- subclass and set `output_field_class`.
* `identity` is keyword-only. `IdentityField("Sequence")` used to bind the
  verbose name to `identity` and emit `GENERATED Sequence AS IDENTITY`.
* Identity fields are no longer `editable`, which `GeneratedField` enforces.
  They stop appearing in ModelForms and the admin. Assigning to them never
  affected `save()` anyway, the column is excluded from INSERT and UPDATE.
* The test matrix covers Django 5.2, 6.0 and 6.1 on Python 3.14.

### Added

* `output_field_class` picks the column type on a subclass.

### Removed

* `PositiveIdentityField` and `PositiveBigIdentityField`. A `CHECK (>= 0)` was
  all that set them apart, and nothing could trip it: the sequence is built
  `MINVALUE 1, INCREMENT BY 1, NO CYCLE`, so the database never returns a value
  below 1, and `generated = True` keeps the column out of every INSERT and
  UPDATE, so `create()`, `bulk_create()` and `QuerySet.update()` all discard an
  assigned value. Only raw SQL against a `BY DEFAULT` column could reach it.
  Use `IdentityField` or `BigIdentityField`.

### Fixed

* `makemigrations` no longer crashes on a model with an identity field, whether
  the field itself or a sibling column is added or removed --
  `AttributeError: 'IdentityField' object has no attribute 'expression'`.
  Adding one no longer asks for a default either, which an identity column
  cannot have.
* Changing the identity clause reports that the field has to be removed and
  re-added, instead of crashing with `AttributeError: 'IdentityField' object
  has no attribute 'db_persist'`.
* `default=` and `editable=True` are rejected instead of silently ignored.
* `null=True` is reported as having no effect (`fields.W225`, Django 6.1+).

## 0.2.0 - 2026-03-17

### Added

* Django 6 compatibility.
* `ty` type checking.

## 0.1.2 - 2025-10-05

### Added

* `tox` and a cleaned-up test structure.
* Package description metadata.

## 0.1.1 - 2025-10-04

### Fixed

* Packaging.

## 0.1.0 - 2025-10-03

Initial release.
