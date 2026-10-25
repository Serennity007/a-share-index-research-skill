from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import compare_index_styles as tool

HEADER='index,observation_date,available_at,close,return_type\n'
def panel():
    rows=[]
    for day,values in [('2024-01-08',[100,100,100,100]),('2024-01-09',[110,105,120,125])]:
        for name,value in zip(['HS300','SSE50','CSI500','CSI1000'],values):
            rows.append(f'{name},{day},{day}T07:00:00Z,{value},price')
    return (HEADER+'\n'.join(rows)+'\n').encode()

class AdvancedTests(unittest.TestCase):
    def check(self,raw):
        return tool.analyze(raw,'2024-01-09T08:00:00Z','synthetic')

    def test_relative_ratio_and_percentage_point_spread_are_distinct(self):
        result=self.check(panel())
        pair=result['relative_strength'][0]
        self.assertEqual(result['ranked_by_price_return'][0],'CSI1000')
        self.assertAlmostEqual(pair['return_difference_pp'],15)
        self.assertAlmostEqual(pair['relative_ratio_change'],1.25/1.1-1)
        self.assertNotIn('futures_return',result)

    def test_incomplete_dates_are_not_forward_filled(self):
        raw=panel().replace(b'CSI1000,2024-01-09,2024-01-09T07:00:00Z,125,price\n',b'')
        with self.assertRaises(ValueError):
            self.check(raw)

    def test_future_publications_cannot_change_style_ranking(self):
        reports=[self.check(panel()+f'HS300,2024-01-09,2024-01-10T07:00:00Z,{v},price\n'.encode()) for v in (1,9999)]
        self.assertEqual(reports[0]['ranked_by_price_return'],reports[1]['ranked_by_price_return'])
        self.assertEqual(reports[0]['excluded_unavailable_rows'],1)

    def test_duplicates_total_return_and_zero_levels_are_rejected(self):
        for raw in [panel()+panel().splitlines()[1]+b'\n',panel().replace(b',price',b',total_return'),panel().replace(b',110,',b',0,')]:
            with self.subTest(raw=raw),self.assertRaises(ValueError):
                self.check(raw)
