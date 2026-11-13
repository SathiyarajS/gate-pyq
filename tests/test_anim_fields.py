import sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from animations import fields

class AddressFieldsTest(unittest.TestCase):
    def test_set_associative_split(self):
        # CS-2014-S2-Q19: 4 GB, 16 KB 4-way, 32-byte blocks -> tag 20.
        _, out, _ = fields.address_fields(dict(mode='cache', memory=4 << 30, cache=16 << 10, ways=4, block=32))
        self.assertEqual((out['offset'], out['index'], out['tag']), (5, 7, 20))

    def test_block_size_cancels_when_not_given(self):
        _, out, _ = fields.address_fields(dict(mode='cache', address_bits=40, cache=512 << 10, ways=8))
        self.assertEqual(out['tag'], 24)  # CS-2016-S2-Q42

    def test_hex_split_and_paging(self):
        _, out, _ = fields.address_fields(dict(mode='cache', memory=1 << 20, cache=(1 << 12) * 16, block=16, split='E201F'))
        self.assertEqual(out['split'], {'Tag': 'E', 'Index': '201', 'Offset': 'F'})
        _, out, _ = fields.address_fields(dict(mode='page', address_bits=57, page=4096, pte=8, levels=True))
        self.assertEqual(out['levels'], 5)
        with self.assertRaises(SystemExit):
            fields.address_fields(dict(mode='cache', address_bits=32, cache=3000, block=32))
