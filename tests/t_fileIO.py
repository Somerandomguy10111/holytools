import unittest
from hollarek.fileIO import TextIO, BinaryIO, ImageIO
from PIL import Image
from hollarek.devtools import Spoofer
from hollarek.devtools import Unittest

class TestFileIO(Unittest):

    @classmethod
    def setUpClass(cls):
        pass

    def test_text_io(self):
        # Test reading and writing text files
        txt_path = Spoofer.get_txt()
        original_content = TextIO.read(txt_path)
        new_content = "This is a new content for testing."
        TextIO.write(txt_path, new_content)
        self.assertEqual(TextIO.read(txt_path), new_content)
        TextIO.write(txt_path, original_content)

    def test_binary_io(self):
        # Test reading and writing binary files
        pdf_path = Spoofer.get_pdf()
        original_content = BinaryIO.read(pdf_path)
        new_content = b"This is new binary content for testing."
        BinaryIO.write(pdf_path, new_content)
        self.assertEqual(BinaryIO.read(pdf_path), new_content)
        BinaryIO.write(pdf_path, original_content)

    def test_image_io(self):
        # Test reading and writing image files
        png_path = Spoofer.get_png()
        original_image = ImageIO.read(png_path)
        new_image = Image.new('RGB', (100, 100), color = 'red')
        ImageIO.write(png_path, new_image)
        # Reopen the image to verify changes
        modified_image = ImageIO.read(png_path)
        self.assertEqual(modified_image.size, new_image.size)
        original_image.save(png_path)

if __name__ == '__main__':
    unittest.main()
