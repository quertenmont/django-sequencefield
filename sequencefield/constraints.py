from django.db.models.constraints import BaseConstraint
from django.db.models.fields import BigIntegerField
from django.db.utils import DEFAULT_DB_ALIAS


class SequenceConstraint(BaseConstraint):
    maxvalue: int | None = None

    def __init__(
        self, name=None, sequence="", drop=True, maxvalue=None, fields=(), start=1
    ):
        if not sequence:
            raise TypeError(
                f"{self.__class__.__name__}.__init__() missing 1 required keyword-only "
                f"argument: 'sequence'"
            )

        self.fields = tuple(fields)
        self.drop = drop
        self.start = start
        self.sequence = sequence
        self.maxvalue = maxvalue if maxvalue else self.maxvalue

        super().__init__(name=name)

    def __eq__(self, other):
        if isinstance(other, SequenceConstraint):
            return (
                self.name == other.name
                and self.fields == other.fields
                and self.drop == other.drop
                and self.sequence == other.sequence
                and self.maxvalue == other.maxvalue
            )
        return super().__eq__(other)

    def deconstruct(self):
        path, args, kwargs = super().deconstruct()
        kwargs["sequence"] = self.sequence
        kwargs["drop"] = self.drop
        kwargs["fields"] = self.fields
        kwargs["start"] = self.start
        kwargs["maxvalue"] = self.maxvalue
        return path, args, kwargs

    @property
    def field_name(self):
        if len(self.fields) != 1:
            raise ValueError("A SequenceConstraint must contains exactly one field")
        return self.fields[0]

    def constraint_sql(self, model, schema_editor):
        assert schema_editor
        assert model

        return self.create_sql(model, schema_editor)

    def create_sql(self, model, schema_editor):
        assert schema_editor
        assert model
        sql = f"CREATE SEQUENCE IF NOT EXISTS {self.sequence}"
        if self.maxvalue:
            sql += f" MAXVALUE {self.maxvalue}"
        sql += f" START {self.start}"
        sql += ";"

        return schema_editor.execute(
            sql=sql,
            params=(),
        )

    def remove_sql(self, model, schema_editor):
        assert schema_editor
        assert model

        if self.drop:
            return schema_editor.execute(
                sql=f"""DROP SEQUENCE IF EXISTS {self.sequence}""",
                params=(),
            )

        return

    def validate(self, model, instance, exclude=None, using=DEFAULT_DB_ALIAS):
        print("CALL VALIDATE")
        pass


class SmallIntSequenceConstraint(SequenceConstraint):
    maxvalue = 32767


class IntSequenceConstraint(SequenceConstraint):
    maxvalue = 2147483647


class BigIntSequenceConstraint(SequenceConstraint):
    maxvalue = BigIntegerField.MAX_BIGINT
