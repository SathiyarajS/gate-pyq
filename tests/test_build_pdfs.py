import io, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_pdfs


class RepackGrayImagesTest(unittest.TestCase):
    def _pdf_with(self, image, path):
        import pymupdf
        buf = io.BytesIO(); image.save(buf, 'PNG')
        doc = pymupdf.open(); page = doc.new_page()
        page.insert_image(pymupdf.Rect(20, 20, 20 + image.width, 20 + image.height), stream=buf.getvalue())
        doc.save(path)

    def _pixels(self, path):
        import pymupdf
        doc = pymupdf.open(path)
        xref = doc[0].get_images()[0][0]
        pix = pymupdf.Pixmap(doc, xref)
        if pix.n != 1 or pix.colorspace is None or pix.colorspace.n != 1:
            pix = pymupdf.Pixmap(pymupdf.csGRAY, pix)
        return pix.width, pix.height, pix.samples

    def test_sixteen_grey_levels_are_packed_losslessly(self):
        from PIL import Image
        levels = [0, 17, 40, 90, 120, 150, 170, 190, 200, 210, 220, 230, 240, 248, 252, 255]
        for width in (33, 34):  # odd widths need a padded nibble per row
            img = Image.new('RGB', (width, 21))
            img.putdata([(v, v, v) for v in (levels[(x * 7 + y * 3) % 16] for y in range(21) for x in range(width))])
            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / 'a.pdf'
                self._pdf_with(img, path)
                before = self._pixels(path)
                self.assertEqual(build_pdfs.repack_gray_images(path), 1)
                self.assertEqual(self._pixels(path), before)

    def test_colour_images_are_left_alone(self):
        from PIL import Image
        img = Image.new('RGB', (10, 10), (200, 30, 30))
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'a.pdf'
            self._pdf_with(img, path)
            self.assertEqual(build_pdfs.repack_gray_images(path), 0)


class CacheKeyTest(unittest.TestCase):
    """The key follows what the PDF prints (its print fingerprint), not every byte of the site."""
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.imgdir = Path(tmp.name)
        (self.imgdir / 'a.png').write_bytes(b'one')
        self.doc = f'<img src="{self.imgdir.as_uri()}/a.png">'

    def key(self, printed, footer='f'):
        image_hash = lambda name: (self.imgdir / name).read_bytes().hex()
        return build_pdfs.cache_key(printed, self.doc, footer, self.imgdir, image_hash, '158.0')

    def test_generated_date_does_not_change_the_key(self):
        self.assertEqual(self.key('1 #Generated 2026-11-10'), self.key('1 #Generated 2026-12-01'))
        self.assertNotEqual(self.key('1 #Generated 2026-12-01'), self.key('1 #Generated 2026-12-01 changed'))

    def test_printed_text_footer_and_images_change_the_key(self):
        base = self.key('1 #Q1')
        self.assertNotEqual(base, self.key('1 #Q2'))
        self.assertNotEqual(base, self.key('1 #Q1', footer='g'))
        (self.imgdir / 'a.png').write_bytes(b'two')
        self.assertNotEqual(base, self.key('1 #Q1'))

    def test_fingerprint_skips_elements_hidden_in_print(self):
        self.assertIn("cs.display==='none'", build_pdfs.PRINT_FINGERPRINT)
        self.assertIn("return out.join('\\n')", build_pdfs.PRINT_FINGERPRINT)


if __name__ == '__main__':
    unittest.main()
