import math
from datetime import datetime

from django.core import checks
from django.db import models
from django.db.models import BigIntegerField, Field, IntegerField, SmallIntegerField
from django.db.models.expressions import Expression
from django.utils.functional import cached_property

from .constraints import SequenceConstraint
from .functions import LeftShift, NextSeqVal


class SequenceFieldMixin(Field):
    @property
    def db_returning(self):
        return True

    def get_sequence_name(self) -> str | None:
        for c in self.model._meta.constraints:
            if isinstance(c, SequenceConstraint) and self.attname in c.fields:
                return c.sequence
        return None

    @cached_property
    def sequence_name(self) -> str:
        seq_name = self.get_sequence_name()
        if not seq_name:
            raise ValueError(
                "Not found any SequenceConstraint providing values"
                f" for this field ({self.attname}) "
            )
        return seq_name

    def _check_has_sequence_constraint(self):
        seq_name = self.get_sequence_name()
        if not seq_name:
            return [
                checks.Error(
                    "No SequenceConstraint providing values",
                    obj=self,
                    id="fields.E006",
                )
            ]
        return []

    def check(self, **kwargs):
        return [*super().check(**kwargs), *self._check_has_sequence_constraint()]

    def pre_save(self, model_instance, add):
        if add:
            return self.get_db_expression(model_instance)
        else:
            return super().pre_save(model_instance, add)

    def get_db_expression(self, model_instance) -> Expression:
        return NextSeqVal(self.sequence_name)


class SequenceField(SequenceFieldMixin, IntegerField):
    pass


class SmallIntegerSequenceField(SequenceFieldMixin, SmallIntegerField):
    pass


class IntegerSequenceField(SequenceFieldMixin, IntegerField):
    pass


class BigIntegerSequenceField(SequenceFieldMixin, BigIntegerField):
    pass


class BigIntegerWithDateSequenceField(SequenceFieldMixin, BigIntegerField):
    def __init__(self, *args, datetime_field, **kwargs):
        super().__init__(*args, **kwargs)
        self.datetime_field = datetime_field

    def check(self, **kwargs):
        return [
            *super().check(**kwargs),
            *self._check_datetime_field(),
        ]

    def _check_datetime_field(self):
        if self.datetime_field is None or not isinstance(self.datetime_field, str):
            return [
                checks.Error(
                    "datetime_field argument is not provided or is not a string for %s."
                    % self.__class__.__name__,
                    hint=(
                        "add valid datetime_field argument giving"
                        "the name of a field within the same model"
                    ),
                    obj=self,
                )
            ]

        model_field = next(
            (f for f in self.model._meta.fields if f.name == self.datetime_field), None
        )
        if model_field is None or not isinstance(model_field, models.DateTimeField):
            return [
                checks.Error(
                    (
                        "datetime_field argument is not pointing"
                        " to a DatetimeField instance for %s."
                    )
                    % self.__class__.__name__,
                    hint=(
                        "verify that the datetime_field argument"
                        "is pointing to a DateTimeField field within the same model"
                    ),
                    obj=self,
                )
            ]

        return []

    # needed to store the additional parameter
    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.datetime_field:
            kwargs["datetime_field"] = self.datetime_field
        return name, path, args, kwargs

    def get_db_expression(self, model_instance) -> Expression:
        date = getattr(model_instance, self.datetime_field)
        assert isinstance(date, datetime)
        epoch_days = math.floor(date.timestamp() / 86400)
        return LeftShift(epoch_days, bits=48) + super().get_db_expression(
            model_instance
        )
