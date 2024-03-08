from PIL.Image import open as load_img
from PIL.Image import new as create_img
from PIL.Image import Image as PilImage
import base64
from .file_io import IO
from enum import Enum
import io
# ---------------------------------------------------------

class ImageFormat(Enum):
    PNG = 'png'
    JPG = 'jpg'
    JPEG = 'jpeg'
    # GIF = 'gif'
    # BMP = 'bmp'
    # TIFF = 'tiff'
    # WEBP = 'webp'

    @classmethod
    def as_list(cls) -> list[str]:
        return [member.value for member in cls]



class Image:
    def __init__(self, path : str):
        self.content : PilImage = load_img(path)

    def save(self, *args, **kwargs):
        self.content.save(*args, **kwargs)

    def show(self):
        self.content.show()

    def as_bytes(self) -> bytes:
        buffer = io.BytesIO()
        self.content.save(buffer, format=self.get_format())
        img_bytes = buffer.getvalue()
        return img_bytes


    def get_format(self) -> str:
        return self.content.format


    def as_base64_str(self) -> str:
        byte_content = self.as_bytes()
        base64_content = base64.b64encode(byte_content).decode('utf-8')
        return base64_content


    def convert(self, target_format: ImageFormat):
        new_format = target_format.value.upper()
        if new_format == 'JPG':
            new_format = 'JPEG'
        if self.content.format.upper() == new_format:
            return

        content = self.content
        if self.content.mode in ('LA', 'RGBA') and new_format in ['JPG', 'JPEG']:
            new = create_img('RGB', content.size, (255, 255, 255))
            rgb_content = content.convert('RGB') if content.mode == 'RGBA' else content.convert('L').convert('RGB')
            new.paste(rgb_content, mask=content.split()[-1])
        elif self.content.mode != 'RGBA' and new_format == 'PNG':
            new = content.convert('RGBA')
        else:
            new = self.content

        buffer = io.BytesIO()
        new.save(buffer, format=new_format)
        buffer.seek(0)
        self.content = load_img(buffer)
        return self


class ImageIO(IO):
    def read(self) -> Image:
        supported_formats = ImageFormat.as_list()
        suffix = self.get_suffix()
        if not suffix in supported_formats:
            raise ValueError(f'Unsupported image format: {suffix}')
        return Image(path=self.fpath)

    def write(self, image: Image) -> None:
        image.save(self.fpath)

    def view(self):
        image = self.read()
        image.show()
