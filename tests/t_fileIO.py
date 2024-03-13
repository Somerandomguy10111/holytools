from hollarek.file import BinaryFile, TextFile, ImageFile, ImageConverter, ImageFormat
from hollarek.devtools import FileSpoofer, Unittest
from hollarek.fsys import FsysNode
from PIL.Image import Image
from unittest.mock import patch
import io
# ---------------------------------------------------------


class TestFile(Unittest):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.text_fpath = FileSpoofer.lend_txt().fpath
        self.jpg_fpath = FileSpoofer.lend_jpg().fpath
        self.png_fpath = FileSpoofer.lend_png().fpath


    def test_binary_size(self):
        bio = BinaryFile(self.text_fpath)
        bytes_count_mb = len(bio.read())/10**6
        fsize= FsysNode(path=self.png_fpath).get_size_in_MB()
        lower = int(fsize)
        upper = int(fsize+1)
        self.assertTrue(lower <= bytes_count_mb <= upper)

    def test_valid_image_read(self):
        image_io = ImageFile(fpath=self.png_fpath)
        with image_io.read() as result:
            self.assertIsInstance(obj=result, cls=Image)

    def test_invalid_image_read(self):
        image_io = ImageFile(fpath=f'test.png')
        with self.assertRaises(FileNotFoundError):
            with image_io.read() as _:
                pass

    def test_invalid_image_write(self):
        with self.assertRaises(TypeError):
            ImageFile(fpath=f'/tmp/test')

    def test_text_read(self):
        tio = TextFile(fpath=self.text_fpath)
        content = tio.read()
        self.assertIn(member=f'mankind', container=content)

    def test_text_view(self, manual : bool = False):
        if not manual:
            self.skipTest(f'View can only be tested manually')
        tio = TextFile(fpath=self.text_fpath)
        tio.view()

    def test_binary_view(self, manual : bool= False):
        if not manual:
            self.skipTest(f'View can only be tested manually')
        bio = BinaryFile(self.text_fpath)
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            bio.view()
            self.assertIn("4f 6e", fake_out.getvalue())

    def test_image_view(self, manual : bool = False):
        if not manual:
            self.skipTest(f'View can only be tested manually')
        image_io = ImageFile(fpath=self.png_fpath)
        image_io.view()


class TestImageConverter(Unittest):
    def setUp(self):
        spoofer = FileSpoofer()
        self.jpg_file = spoofer.lend_jpg().fpath
        self.png_file = spoofer.lend_png().fpath

    def test_png_to_jpeg(self):
        image_io = ImageFile(fpath=self.png_file)
        image = image_io.read()
        new = ImageConverter.convert(image=image, target_format=ImageFormat.JPEG)
        self.assertTrue(new.format == 'JPEG')

    def test_jpg_to_png(self):
        image_io = ImageFile(fpath=self.jpg_file)
        image = image_io.read()
        new = ImageConverter.convert(image=image, target_format=ImageFormat.PNG)
        self.assertTrue(new.format == 'PNG')

    def test_no_format_attempt(self):
        image_io = ImageFile(fpath=self.jpg_file)
        image = image_io.read()
        no_format_img = ImageConverter.to_rgb(image=image)
        with self.assertRaises(TypeError):
            ImageConverter.convert(image=no_format_img, target_format=ImageFormat.JPEG)

    # noinspection PyClassVar
    def test_invalid_format_attempt(self):
        image_io = ImageFile(fpath=self.jpg_file)
        image = image_io.read()
        image.format = 'xyz'
        with self.assertRaises(TypeError):
            ImageConverter.convert(image=image, target_format=ImageFormat.PNG)


if __name__ == '__main__':
    # TestIO.execute_all()
    TestImageConverter.execute_all()
