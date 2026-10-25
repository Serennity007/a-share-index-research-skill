from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT / 'scripts'))
import analyze_breadth as tool

HEADER = 'code,close,previous_close,turnover_cny,sector,observed_at\n'
ROWS = ['000001,11,10,100,A,2024-01-09T15:00:00+08:00', '000002,9,10,200,A,2024-01-09T15:00:00+08:00','000003,10,10,0,B,2024-01-09T15:00:00+08:00']
def data(rows=ROWS):
    return (HEADER+'\n'.join(rows)+'\n').encode()

class BreadthTests(unittest.TestCase):
    def run_breadth(self, raw=None, count=5):
        return tool.analyze(data() if raw is None else raw,'2024-01-09T15:00:00+08:00','DEMO',count,'synthetic')

    def test_partial_coverage_and_equal_weight_arithmetic(self):
        result=self.run_breadth()
        self.assertEqual((result['advancing'],result['declining'],result['unchanged']),(1,1,1))
        self.assertAlmostEqual(result['sample_equal_weight_return'],0)
        self.assertEqual(result['coverage'],.6)
        self.assertFalse(result['declared_sample_complete'])
        self.assertEqual(result['turnover_cny'],300)
        self.assertAlmostEqual(result['advance_fraction'],1/3)
        self.assertNotIn('official_index_return',result)

    def test_declared_completeness_is_only_count_equality(self):
        self.assertTrue(self.run_breadth(count=3)['declared_sample_complete'])
        with self.assertRaises(ValueError):
            self.run_breadth(count=2)

    def test_top_five_concentration_and_sectors(self):
        rows=[f'{i:06d},11,10,{i},A,2024-01-09T15:00:00+08:00' for i in range(1,7)]
        result=self.run_breadth(data(rows),count=6)
        self.assertAlmostEqual(result['top5_turnover_share'],20/21)
        self.assertEqual(result['sectors'][0]['count'],6)
        self.assertAlmostEqual(result['sectors'][0]['equal_weight_return'],.1)

    def test_zero_turnover_avoids_division_by_zero(self):
        rows=[r.replace(',100,',',0,').replace(',200,',',0,') for r in ROWS]
        self.assertIsNone(self.run_breadth(data(rows))['top5_turnover_share'])

    def test_future_counterfactual_does_not_change_observations(self):
        reports=[self.run_breadth(data(ROWS+[f'000004,{v},10,100,B,2024-01-10T15:00:00+08:00'])) for v in (1,999)]
        for report in reports:
            self.assertEqual(report['observed_count'],3)
            self.assertEqual(report['excluded_future_rows'],1)
        self.assertEqual(reports[0]['sample_equal_weight_return'],reports[1]['sample_equal_weight_return'])

    def test_duplicate_codes_and_mixed_market_dates_are_rejected(self):
        for rows in [ROWS+[ROWS[0]], [ROWS[0].replace('2024-01-09','2024-01-08'),*ROWS[1:]]]:
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                self.run_breadth(data(rows))

    def test_negative_turnover_nonfinite_price_and_zero_previous_are_rejected(self):
        for old,new in [(',100,',',-100,'),(',11,',',NaN,'),(',11,10,',',11,0,')]:
            with self.subTest(new=new), self.assertRaises(ValueError):
                self.run_breadth(data().replace(old.encode(),new.encode()))

    def test_timestamp_offsets_use_same_beijing_market_date(self):
        rows=[ROWS[0].replace('15:00:00+08:00','07:00:00Z'),*ROWS[1:]]
        self.assertEqual(self.run_breadth(data(rows))['observation_span_seconds'],0)
