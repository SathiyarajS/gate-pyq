"""Run with: python -m unittest discover -s tests -v."""
import hashlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import fitz
from PIL import Image

spec = importlib.util.spec_from_file_location('render_crops', Path(__file__).resolve().parents[1] / 'scripts/render_crops.py')
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)

class RenderCropTests(unittest.TestCase):
    def setUp(self):
        self.doc = fitz.open()
        self.page = self.doc.new_page(width=200, height=300)
        self.page.insert_text((35, 75), 'Source content 123')
        self.crop = {'bbox': [25.25, 50.5, 170.75, 95.25]}

    def tearDown(self):
        self.doc.close()

    def test_legacy_pixels_and_webp_unchanged(self):
        pix = self.page.get_pixmap(matrix=fitz.Matrix(3, 3), clip=fitz.Rect(self.crop['bbox']), alpha=False)
        old = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
        new = renderer.render_crop(self.page, self.crop)
        self.assertEqual(old.size, new.size)
        self.assertEqual(old.tobytes(), new.tobytes())
        a, b = io.BytesIO(), io.BytesIO()
        old.save(a, 'WEBP', quality=80)
        new.save(b, 'WEBP', quality=80)
        self.assertEqual(a.getvalue(), b.getvalue())

    def test_rotation_is_full_source_then_rectangle(self):
        crop = {**self.crop, 'transform': {'rotation_degrees': -2, 'coordinate_space': 'rotated_page'}}
        # Independently derive normalized full-page transform, then extract pixels.
        rotate = fitz.Matrix(-2)
        extent = self.page.rect * rotate
        rotate.e, rotate.f = -extent.x0, -extent.y0
        pix = self.page.get_pixmap(matrix=rotate * fitz.Matrix(3, 3), alpha=False)
        full = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
        box = (fitz.Rect(crop['bbox']) * fitz.Matrix(3, 3)).irect
        expected = full.crop((box.x0-pix.x, box.y0-pix.y, box.x1-pix.x, box.y1-pix.y))
        self.assertEqual(expected.tobytes(), renderer.render_crop(self.page, crop).tobytes())

    def test_source_polygon_round_trip(self):
        for angle in (-2, 0, 2):
            crop = {**self.crop, 'transform': {'rotation_degrees': angle, 'coordinate_space': 'rotated_page'}}
            box, matrix = renderer.crop_geometry(self.page, crop)
            polygon = renderer.crop_source_polygon(self.page, crop)
            for point, expected in zip(polygon, (box.tl, box.tr, box.br, box.bl)):
                actual = fitz.Point(point) * matrix
                self.assertAlmostEqual(actual.x, expected.x, places=4)
                self.assertAlmostEqual(actual.y, expected.y, places=4)

    def test_invalid_transform_rejected(self):
        for transform in ({}, {'rotation_degrees': -2, 'coordinate_space': 'source'},
                          {'rotation_degrees': float('nan'), 'coordinate_space': 'rotated_page'},
                          {'rotation_degrees': 11, 'coordinate_space': 'rotated_page'},
                          {'rotation_degrees': True, 'coordinate_space': 'rotated_page'}):
            with self.subTest(transform=transform), self.assertRaises(ValueError):
                renderer.render_crop(self.page, {**self.crop, 'transform': transform})

    def test_invalid_bounds_and_scale_rejected(self):
        for bbox in ([0, 0, float('inf'), 20], [20, 20, 10, 30], [-1, 0, 10, 10]):
            with self.subTest(bbox=bbox), self.assertRaises(ValueError):
                renderer.render_crop(self.page, {'bbox': bbox})
            with self.subTest(transformed_bbox=bbox), self.assertRaises(ValueError):
                renderer.render_crop(self.page, {'bbox': bbox, 'transform': {'rotation_degrees': -2, 'coordinate_space': 'rotated_page'}})
        for scale in (0, -1, float('nan'), float('inf')):
            with self.assertRaises(ValueError): renderer.render_crop(self.page, self.crop, scale)

    def test_hash_preflight_still_rejects_changed_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'data').mkdir(); (root/'audits').mkdir()
            pdf = root/'source.pdf'; pdf.write_bytes(self.doc.tobytes())
            crop = {**self.crop, 'file': 'source.pdf', 'page': 1, 'status': 'draft',
                    'transform': {'rotation_degrees': -2, 'coordinate_space': 'rotated_page'}}
            (root/'data/crops.json').write_text(json.dumps({'Q1': [crop]}))
            (root/'audits/crop-source-map.json').write_text(json.dumps({'sources': {'source.pdf': {'sha256': '0'*64}}}))
            with patch.object(renderer, 'ROOT', root), patch('sys.argv', ['render_crops', '--allow-draft']):
                with self.assertRaisesRegex(SystemExit, 'missing or changed source'): renderer.main()
            self.assertFalse((root/'site-assets/q').exists())

if __name__ == '__main__': unittest.main()
