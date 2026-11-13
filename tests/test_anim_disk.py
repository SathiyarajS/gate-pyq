import sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from animations import disk

class DiskSchedulingTest(unittest.TestCase):
    QUEUE = [98, 183, 37, 122, 14, 124, 65, 67]  # the standard textbook queue, head at 53

    def path(self, policy, direction='up'):
        d = disk.disk_schedule(53, self.QUEUE, policy, direction, 0, 199)
        return d['total'], [m[1] for m in d['moves']]

    def test_policies(self):
        self.assertEqual(self.path('fcfs')[0], 640)
        self.assertEqual(self.path('sstf'), (236, [65, 67, 37, 14, 98, 122, 124, 183]))
        self.assertEqual(self.path('scan', 'down'), (236, [37, 14, 0, 65, 67, 98, 122, 124, 183]))
        self.assertEqual(self.path('look', 'down')[0], 208)
        self.assertEqual(self.path('cscan'), (382, [65, 67, 98, 122, 124, 183, 199, 0, 14, 37]))
        self.assertEqual(self.path('clook'), (322, [65, 67, 98, 122, 124, 183, 14, 37]))

    def test_sstf_tie_stops_the_build(self):
        with self.assertRaises(SystemExit):
            disk.disk_schedule(50, [40, 60], 'sstf')

    def test_reversal_cost(self):
        # CS-2018-Q63: 200 cylinders at 20 per 100, three reversals at 15.
        spec = dict(kind='disk-schedule', start=80, requests=[72, 134, 20, 86, 116, 16], lo=0, hi=199, metric='cost',
                    cost=dict(per=20, cylinders=100, reversal=15), policies=[dict(policy='sstf', expect=85)])
        self.assertIn('changes direction 3 times', disk.disk_animation('Q', spec)['schedules'][0]['steps'][-1]['note'])
