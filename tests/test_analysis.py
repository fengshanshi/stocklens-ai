from datetime import UTC, datetime, timedelta
import unittest

from stocklens.analysis import analyze
from stocklens.models import PriceBar


class AnalysisTests(unittest.TestCase):
    def test_uptrend_is_bullish(self):
        start = datetime(2026, 1, 1, tzinfo=UTC)
        bars = [PriceBar(start + timedelta(days=i), 100 + i) for i in range(30)]
        signal = analyze("demo", bars)
        self.assertEqual(signal.trend, "上行")
        self.assertGreaterEqual(signal.score, 65)

    def test_requires_history(self):
        with self.assertRaises(ValueError):
            analyze("demo", [PriceBar(datetime.now(UTC), 1)] * 20)


if __name__ == "__main__":
    unittest.main()

