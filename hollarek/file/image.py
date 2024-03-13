from __future__ import annotations
from PIL.Image import Image
import PIL.Image as ImgHandler
import base64
from .file import File
from enum import Enum
import io
from typing import Optional
# ---------------------------------------------------------

class ImageFormat(Enum):
    PNG = 'PNG'
    JPG = 'JPG'
    JPEG = 'JPEG'
    # GIF = 'gif'
    # BMP = 'bmp'
    # TIFF = 'tiff'
    # WEBP = 'webp'

    @classmethod
    def as_list(cls) -> list[ImageFormat]:
        return [member for member in cls]


    def __eq__(self, other):
        if isinstance(other,str):
            return self.value.upper() == other.upper()
        elif isinstance(other, ImageFormat):
            return self.value == other.value
        return False

    def __str__(self):
        return self.value

class ImageConverter:  # Assuming these methods are part of a class named ImageConverter

    @classmethod
    def as_bytes(cls, image: Image, img_format : Optional[ImageFormat] = None) -> bytes:
        if not img_format:
            img_format = image.format
        if not img_format:
            raise ValueError(f'No img_format provided and failed to extract format from image as fallback')

        buffer = io.BytesIO()
        image.save(buffer, format=str(img_format))
        img_bytes = buffer.getvalue()
        return img_bytes

    @classmethod
    def as_base64_str(cls, image: Image, img_format : Optional[ImageFormat] = None) -> str:
        byte_content = cls.as_bytes(image=image, img_format=img_format)
        base64_content = base64.b64encode(byte_content).decode('utf-8')
        return base64_content

    @classmethod
    def convert(cls, image: Image, target_format : ImageFormat) -> Image:
        if not image.format:
            raise TypeError(f'Given image {image} has no format')
        if not image.format.lower() in cls.get_supported_formats():
            raise TypeError(f'Given image {image} has unsupported format: {image.format}')
        if not target_format in cls.get_supported_formats():
            raise TypeError(f'Conversion to format {target_format} is not supported')
        if not cls.is_valid_mode(image=image):
            raise TypeError(f'Image mode {image.mode} is invalid for format {image.format}')

        new_format = target_format.value.upper()
        if image.mode in ('LA', 'RGBA') and new_format in ['JPG', 'JPEG']:
            image = cls.to_rgb(image)
        elif image.mode != 'RGBA' and new_format == 'PNG':
            image = cls.to_rgba(image)
        else:
            image = image

        return cls.reload_as_fmt(image=image,target_format=target_format)

    @classmethod
    def reload_as_fmt(cls, image : Image, target_format : ImageFormat):
        buffer = io.BytesIO()
        image.save(buffer, format=target_format.value)
        buffer.seek(0)
        return ImgHandler.open(buffer)


    @classmethod
    def to_rgb(cls, image: Image) -> Image:
        new_img = ImgHandler.new('RGB', image.size, (255, 255, 255))
        rgb_content = image.convert('RGB')
        new_img.paste(rgb_content, mask=image.split()[-1])
        return new_img

    @classmethod
    def to_rgba(cls, image: Image) -> Image:
        return image.convert('RGBA')

    # ---------------------------------------------------------
    # check formats

    @classmethod
    def is_valid_mode(cls, image: Image) -> bool:
        if not cls.is_supported(image=image):
            raise TypeError(f'Image format {image.format} is not supported')

        if image.format.upper() == 'PNG':
            return image.mode in ['L', 'LA', 'RGB', 'RGBA', 'P']
        elif image.format.upper() in ['JPEG', 'JPG']:
            return image.mode in ['L', 'RGB', 'CMYK']
        return False


    @classmethod
    def is_supported(cls, image : Image) -> bool:
        return image.format.lower() in cls.get_supported_formats()

    @classmethod
    def get_supported_formats(cls) -> list[ImageFormat]:
        return ImageFormat.as_list()


class ImageFile(File):
    def check_format_ok(self) -> bool:
        if not self.get_suffix() in ImageFormat.as_list():
            if self.get_suffix():
                raise TypeError(f'Path \"{self.fpath}\" indicates unsupported image format: \"{self.get_suffix()}\"')
            else:
                raise TypeError(f'Path \"{self.fpath}\" must end in image suffix: {ImageFormat.as_list()}')
        return True

    def read(self) -> Image:
        return ImgHandler.open(self.fpath)

    def write(self, image: Image):
        image.save(self.fpath)

    def view(self):
        with self.read() as image:
            image.show()
