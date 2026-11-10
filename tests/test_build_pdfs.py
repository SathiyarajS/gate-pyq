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
    def test_generated_date_does_not_change_the_key(self):
        imgdir = Path('/nonexistent')
        a = build_pdfs.cache_key('<p>Generated 2026-11-10</p>', 'f', imgdir, lambda n: '', 'chrome')
        b = build_pdfs.cache_key('<p>Generated 2026-12-01</p>', 'f', imgdir, lambda n: '', 'chrome')
        c = build_pdfs.cache_key('<p>Generated 2026-12-01 changed</p>', 'f', imgdir, lambda n: '', 'chrome')
        self.assertEqual(a, b)
        self.assertNotEqual(b, c)


if __name__ == '__main__':
    unittest.main()
