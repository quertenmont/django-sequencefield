import math
from datetime import datetime, timezone

from django.test import TestCase

from sequencefield.functions import DateFromId, RightShift
from tests.models import (
    BigIntSequenceModel,
    IntSequenceModelA,
    IntSequenceModelB,
)


class ColorFieldTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_model_id(self):
        """
        Checking that id is taken from sequence field
        id should start at 100 as defined by SequenceConstraint.
        and should be incremented (and used by multiple models)
        """
        a = IntSequenceModelA()
        a.save()
        self.assertEqual(a.seqid, 100)

        b = IntSequenceModelB(id=1)
        b.save()
        self.assertEqual(b.seqid, 101)

        a2 = IntSequenceModelA()
        a2.save()
        self.assertEqual(a2.seqid, 102)

    def test_model_idWithDate(self):
        """
        Checking that id we can generate an id containing a data value inside
        """
        dt = datetime(2020, 1, 1, tzinfo=timezone.utc)
        x = BigIntSequenceModel(id=1, created=dt)
        x.save()
        self.assertEqual(x.seqid, 5140296024689999873)

        # verify that we can extract the number of days since epoch from id
        data = BigIntSequenceModel.objects.values(
            epochdays=RightShift("seqid", bits=48)
        ).first()
        print("epochdays", data)
        self.assertEqual(data["epochdays"], math.floor(dt.timestamp() / 86400))

        # verify that we can extract the date from the id itself
        data = BigIntSequenceModel.objects.values(date=DateFromId("seqid")).first()
        self.assertEqual(data["date"], dt.date())
