"""Test percentage and base percentage fee strategies."""

import unittest
from decimal import Decimal

from fee.fee_strategy import FeeStrategy
from fee.percentage_fee_strategy import PercentageFeeStrategy
from fee.base_percentage_fee_strategy import BasePercentageFeeStrategy


class TestFeeStrategy(unittest.TestCase):
    """Verify the fee strategy interface is abstract."""

    def test_cannot_instantiate_abstract_strategy(self):
        with self.assertRaises(TypeError):
            FeeStrategy()


class TestPercentageFeeStrategy(unittest.TestCase):
    """Test percentage validation and fee calculations."""

    def test_invalid_percentages(self):
        for percentage in (Decimal("-0.01"), Decimal("1.01")):
            with self.subTest(percentage=percentage):
                with self.assertRaises(ValueError) as context:
                    PercentageFeeStrategy(percentage)

                self.assertEqual(
                    "percentage must be a value between 0 and 1 (inclusive).",
                    str(context.exception)
                )

    def test_boundary_percentages(self):
        for percentage, expected in (
            (Decimal("0"), Decimal("0.00")),
            (Decimal("1"), Decimal("100.00")),
        ):
            with self.subTest(percentage=percentage):
                strategy = PercentageFeeStrategy(percentage)
                self.assertEqual(
                    expected, strategy.get_fee(Decimal("100.00"))
                )

    def test_percentage_fee(self):
        strategy = PercentageFeeStrategy(Decimal("0.0035"))
        self.assertEqual(
            Decimal("0.35"), strategy.get_fee(Decimal("100.00"))
        )

    def test_fee_rounded_to_two_places(self):
        strategy = PercentageFeeStrategy(Decimal("0.007"))
        self.assertEqual(
            Decimal("0.86"), strategy.get_fee(Decimal("123.45"))
        )


class TestBasePercentageFeeStrategy(unittest.TestCase):
    """Test minimum fees, validation, and rounding."""

    def test_negative_base_fee(self):
        with self.assertRaises(ValueError) as context:
            BasePercentageFeeStrategy(
                Decimal("-0.01"), Decimal("0.007")
            )

        self.assertEqual(
            "base_fee must be greater than or equal to zero.",
            str(context.exception)
        )

    def test_invalid_percentages(self):
        for percentage in (Decimal("-0.01"), Decimal("1.01")):
            with self.subTest(percentage=percentage):
                with self.assertRaises(ValueError) as context:
                    BasePercentageFeeStrategy(
                        Decimal("1.25"), percentage
                    )

                self.assertEqual(
                    "percentage must be a value between 0 and 1 (inclusive).",
                    str(context.exception)
                )

    def test_base_fee_when_percentage_is_lower(self):
        strategy = BasePercentageFeeStrategy(
            Decimal("1.25"), Decimal("0.007")
        )
        self.assertEqual(
            Decimal("1.25"), strategy.get_fee(Decimal("100.00"))
        )

    def test_percentage_when_greater_than_base(self):
        strategy = BasePercentageFeeStrategy(
            Decimal("1.25"), Decimal("0.007")
        )
        self.assertEqual(
            Decimal("3.50"), strategy.get_fee(Decimal("500.00"))
        )

    def test_equal_base_and_percentage_fee(self):
        strategy = BasePercentageFeeStrategy(
            Decimal("1.25"), Decimal("0.01")
        )
        self.assertEqual(
            Decimal("1.25"), strategy.get_fee(Decimal("125.00"))
        )

    def test_zero_base_and_boundary_percentages(self):
        for percentage, expected in (
            (Decimal("0"), Decimal("0.00")),
            (Decimal("1"), Decimal("100.00")),
        ):
            with self.subTest(percentage=percentage):
                strategy = BasePercentageFeeStrategy(
                    Decimal("0"), percentage
                )
                self.assertEqual(
                    expected, strategy.get_fee(Decimal("100.00"))
                )

    def test_fee_rounded_to_two_places(self):
        strategy = BasePercentageFeeStrategy(
            Decimal("1.25"), Decimal("0.007")
        )
        self.assertEqual(
            Decimal("2.16"), strategy.get_fee(Decimal("308.45"))
        )