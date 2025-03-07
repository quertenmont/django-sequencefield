[![](https://img.shields.io/pypi/pyversions/django-sequencefield.svg?color=3776AB&logo=python&logoColor=white)](https://www.python.org/)
[![](https://img.shields.io/pypi/djversions/django-sequencefield?color=0C4B33&logo=django&logoColor=white&label=django)](https://www.djangoproject.com/)
[![Published on Django Packages](https://img.shields.io/badge/Published%20on-Django%20Packages-0c3c26)](https://djangopackages.org/packages/p/django-sequencefield/)

[![](https://img.shields.io/pypi/v/django-sequencefield.svg?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/django-sequencefield/)
[![](https://static.pepy.tech/badge/django-sequencefield/month)](https://pepy.tech/project/django-sequencefield)
[![](https://img.shields.io/github/stars/quertenmont/django-sequencefield?logo=github&style=flat)](https://github.com/quertenmont/django-sequencefield/stargazers)
[![](https://img.shields.io/pypi/l/django-sequencefield.svg?color=blue)](https://github.com/quertenmont/django-sequencefield/blob/main/LICENSE.txt)

[![](https://results.pre-commit.ci/badge/github/quertenmont/django-sequencefield/main.svg)](https://results.pre-commit.ci/latest/github/quertenmont/django-sequencefield/main)
[![](https://img.shields.io/github/actions/workflow/status/quertenmont/django-sequencefield/test-package.yml?branch=main&label=build&logo=github)](https://github.com/quertenmont/django-sequencefield)
[![](https://img.shields.io/codecov/c/gh/quertenmont/django-sequencefield?logo=codecov)](https://codecov.io/gh/quertenmont/django-sequencefield)
[![](https://img.shields.io/codacy/grade/194566618f424a819ce43450ea0af081?logo=codacy)](https://www.codacy.com/app/quertenmont/django-sequencefield)
[![](https://img.shields.io/badge/code%20style-black-000000.svg?logo=python&logoColor=black)](https://github.com/psf/black)
[![](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)



# sequencefield
simple model field taking it's value from a postgres sequence.  This is an easy replacement for django autofield offering the following advantages:
-  Sequence could be shared among multiple models (db tables), so you can now have unique id among multiple django models
-  Possibility to generate alphanumeric id of the form "{PREFIX}_{ID}"
-  Unique Id could also be combined with data from other field to build complex id.  One example is given that combine unique id with date information to offer an efficient table indexing/clustering for faster data retrieval when filtering on date.  (Particularly useful with BRIN index)


---

## Installation
-   Run `pip install django-sequencefield`
-   Use a (Small/Big)IntegerSequenceField in one of your model
-   Add a SequenceConstraint into the same model to name the sequence field to use and which id should take values from this sequence constraint

---

## Usage

### Settings
This package doesn't need any setting.

### Simple Example
Just add a sequence field(s) to your models like this:

```python
from django.db import models
from sequencefield.constraints import IntSequenceConstraint
from sequencefield.fields import IntegerSequenceField


class IntSequenceModel(models.Model):
    id = IntegerSequenceField(primary_key=True) #primary_key=False works too

    class Meta:
        constraints = [
            IntSequenceConstraint(
                name="%(app_label)s_%(class)s_custseq",
                sequence="int_custseq", #name of sequence to use
                drop=False, #avoid deleting the sequence if shared among multiple tables
                fields=["id"], #name of the field that should be populated by this sequence
                start=100, #first value of the sequence
                maxvalue=200 #max value allowed for the sequence, will raise error if we go above, use None for the maximum allowed value of the db
            )
        ]

```

### Simple AlphaNumeric Example
Just add an AlphaNumericSequenceField field(s) to your models like this.
You can provide a "format" argument to define how to convert the number to char.  The syntax is the one used in postgres to_char function ([see here](https://www.postgresql.org/docs/current/functions-formatting.html)).  In the example bellow, we will get sequence values: INV_000001, INV_000002, INV_000003, ...

```python
from django.db import models
from sequencefield.constraints import IntSequenceConstraint
from sequencefield.fields import AlphaNumericSequenceField

class AlphaNumericSequenceModel(models.Model):
    seqid = AlphaNumericSequenceField(
        primary_key=False, prefix="INV", format="FM000000"
    )

    class Meta:
        constraints = [
            IntSequenceConstraint(
                name="%(app_label)s_%(class)s_custseq",
                sequence="alphanum_custseq", , #name of sequence to use
                drop=False, #avoid deleting the sequence if shared among multiple tables
                fields=["seqid"], #name of the field that should be populated by this sequence
                start=1,
            )
        ]
```

### Advance Example
Just add a sequence field(s) to your models like this:

```python
from django.db import models
from sequencefield.constraints import BigIntSequenceConstraint
from sequencefield.fields import BigIntegerWithDateSequenceField


class BigIntSequenceModel(models.Model):
    id = models.BigIntegerField(primary_key=True, auto_created=False)
    created = models.DateTimeField(editable=False)
    seqid = BigIntegerWithDateSequenceField(datetime_field="created") #this field with combine values from the sequence with date timestamp
    # the 2 first bytes of the bigint will contains the number of days since 1/1/1970
    # the 6 following bytes will contains a unique id coming from the sequence

    class Meta:
        constraints = [
            BigIntSequenceConstraint(
                name="%(app_label)s_%(class)s_custseq",
                sequence="gdw_post_custseq", #name of the quence
                drop=False, #avoid deleting the sequence if shared among multiple tables
                fields=["seqid"], #field to be populated from this sequence
                start=1, #first value of the sequence
            )
        ]
```

---

## Remarks

Until we find a good solution to properly handle supression of a sequence shared among multiple tables,
It's better to pass the flag drop=False in the SequenceConstraint.  Otherwise a sequence that is still being used by another table might be deleted.

---

## Testing
```bash
# clone repository
git clone https://github.com/quertenmont/django-sequencefield.git && cd sequencefield

# create virtualenv and activate it
python -m venv venv && . venv/bin/activate

# upgrade pip
python -m pip install --upgrade pip

# install requirements
pip install -r requirements.txt -r requirements-test.txt

# install pre-commit to run formatters and linters
pre-commit install --install-hooks

# run tests
tox
# or
python runtests.py
# or
python -m django test --settings "tests.settings"
```
---

## License
Released under [MIT License](LICENSE.txt).

---

## Supporting

- :star: Star this project on [GitHub](https://github.com/quertenmont/django-sequencefield)
- :octocat: Follow me on [GitHub](https://github.com/quertenmont)
- :blue_heart: Follow me on [Twitter](https://twitter.com/LoicQuertenmont)
- :moneybag: Sponsor me on [Github](https://github.com/sponsors/quertenmont)
