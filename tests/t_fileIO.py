from hollarek.fileIO import BinaryIO, TextIO, ImageIO
from hollarek.devtools import Spoofer, Unittest
from hollarek.fsys import FsysNode
from PIL.Image import Image as PILImage
from unittest.mock import patch
import io


class TestIO(Unittest):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        # Set up for all tests; get files from spoofer
        spoofer = Spoofer()
        self.text_file = spoofer.lend_txt()
        self.jpg_file = spoofer.lend_jpg()
        self.png_file = spoofer.lend_png()

    def test_binary_read_write(self):
        bio = BinaryIO(self.text_file)
        bytes_count_mb = len(bio.read())/10**6
        fsize= FsysNode(path=self.png_file).get_size_in_MB()
        lower = int(fsize)
        upper = int(fsize+1)
        self.assertTrue(lower <= bytes_count_mb <= upper)

    def test_binary_view(self):
        bio = BinaryIO(self.text_file)
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            bio.view()
            self.assertIn("4f 6e", fake_out.getvalue())

    def test_image_view(self):
        image_io = ImageIO(fpath=self.png_file)
        image_io.view()

    def test_valid_image_read(self):
        image_io = ImageIO(fpath=self.png_file)
        result = image_io.read()
        self.assertIsInstance(obj=result, cls=PILImage)

    def test_invalid_image_read(self):
        image_io = ImageIO(fpath=self.text_file)
        with self.assertRaises(ValueError):
            image_io.read()

    def test_text_read(self):
        tio = TextIO(fpath=self.text_file)
        content = tio.read()
        self.assertIn(member=f'mankind', container=content)

    def test_text_view(self):
        tio = TextIO(fpath=self.text_file)
        tio.view()


if __name__ == '__main__':
    TestIO.execute_all()
