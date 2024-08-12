from django.db import models

from sequencefield.constraints import BigIntSequenceConstraint, IntSequenceConstraint
from sequencefield.fields import (
    BigIntegerWithDateSequenceField,
    IntegerSequenceField,
)


class IntSequenceModelA(models.Model):
    seqid = IntegerSequenceField(primary_key=True)

    class Meta:
        constraints = [
            IntSequenceConstraint(
                name="%(app_label)s_%(class)s_custseq",
                sequence="int_custseq",
                fields=["seqid"],
                start=100,
            )
        ]

    def __str__(self) -> str:
        return f"seqid:{self.seqid}"


class IntSequenceModelB(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    seqid = IntegerSequenceField()

    class Meta:
        constraints = [
            IntSequenceConstraint(
                name="%(app_label)s_%(class)s_custseq",
                sequence="int_custseq",
                fields=["seqid"],
                start=100,
            )
        ]

    def __str__(self) -> str:
        return f"seqid:{self.seqid}"


class BigIntSequenceModel(models.Model):
    id = models.BigIntegerField(primary_key=True, auto_created=False)
    seqid = BigIntegerWithDateSequenceField(datetime_field="created")  # type: ignore
    created = models.DateTimeField(editable=False)

    class Meta:
        constraints = [
            BigIntSequenceConstraint(
                name="%(app_label)s_%(class)s_custseq",
                sequence="gdw_post_custseq",
                fields=["seqid"],
                start=1,
            )
        ]

    def __str__(self) -> str:
        return f"id:{self.id}-created:{self.created}"
