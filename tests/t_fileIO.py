from hollarek.fileIO import BinaryIO, TextIO, ImageIO, ImageConverter, ImageFormat
from hollarek.devtools import Spoofer, Unittest
from hollarek.fsys import FsysNode
from PIL.Image import Image
import PIL.Image as ImgHandler
from unittest.mock import patch
import io
# ---------------------------------------------------------


class TestIO(Unittest):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.text_fpath = Spoofer.lend_txt().fpath
        self.jpg_fpath = Spoofer.lend_jpg().fpath
        self.png_fpath = Spoofer.lend_png().fpath


    def test_binary_read_write(self):
        bio = BinaryIO(self.text_fpath)
        bytes_count_mb = len(bio.read())/10**6
        fsize= FsysNode(path=self.png_fpath).get_size_in_MB()
        lower = int(fsize)
        upper = int(fsize+1)
        self.assertTrue(lower <= bytes_count_mb <= upper)

    def test_binary_view(self):
        bio = BinaryIO(self.text_fpath)
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            bio.view()
            self.assertIn("4f 6e", fake_out.getvalue())

    def test_image_view(self):
        image_io = ImageIO(fpath=self.png_fpath)
        image_io.view()

    def test_valid_image_read(self):
        image_io = ImageIO(fpath=self.png_fpath)
        result = image_io.read()
        self.assertIsInstance(obj=result, cls=Image)

    def test_invalid_image_read(self):
        image_io = ImageIO(fpath=self.text_fpath)
        with self.assertRaises(ValueError):
            image_io.read()

    def test_invalid_image_write(self):
        image_io = ImageIO(fpath=f'test')
        with self.assertRaises(TypeError):
            image_io.write(image=ImgHandler.open(self.text_fpath))

    def test_text_read(self):
        tio = TextIO(fpath=self.text_fpath)
        content = tio.read()
        self.assertIn(member=f'mankind', container=content)

    def test_text_view(self):
        tio = TextIO(fpath=self.text_fpath)
        tio.view()



class TestImage(Unittest):
    def setUp(self):
        spoofer = Spoofer()
        self.jpg_file = spoofer.lend_jpg().fpath
        self.png_file = spoofer.lend_png().fpath

    def test_png_to_jpeg(self):
        image_io = ImageIO(fpath=self.png_file)
        image = image_io.read()
        new = ImageConverter.convert(image=image, target_format=ImageFormat.JPEG)
        self.assertTrue(new.format == 'JPEG')


    def test_jpg_to_png(self):
        image_io = ImageIO(fpath=self.jpg_file)
        image = image_io.read()
        new = ImageConverter.convert(image=image, target_format=ImageFormat.PNG)
        self.assertTrue(new.format == 'PNG')


if __name__ == '__main__':
    # TestIO.execute_all()
    TestImage.execute_all()
