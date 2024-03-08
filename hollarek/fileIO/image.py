from PIL.Image import Image
import PIL.Image as ImgHandler
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


class ImageConverter:
    @staticmethod
    def as_bytes(image : Image) -> bytes:
        buffer = io.BytesIO()
        image.save(buffer, format=image.format)
        img_bytes = buffer.getvalue()
        return img_bytes


    @staticmethod
    def as_base64_str(image : Image):
        byte_content = ImageConverter.as_bytes(image=image)
        base64_content = base64.b64encode(byte_content).decode('utf-8')
        return base64_content


    @staticmethod
    def convert(image: Image, target_format: ImageFormat):
        new_format = target_format.value.upper()
        if new_format == 'JPG':
            new_format = 'JPEG'
        if image.format.upper() == new_format:
            return image

        content = image
        if image.mode in ('LA', 'RGBA') and new_format in ['JPG', 'JPEG']:
            new = ImgHandler.new('RGB', content.size, (255, 255, 255))
            rgb_content = content.convert('RGB') if content.mode == 'RGBA' else content.convert('L').convert('RGB')
            new.paste(rgb_content, mask=content.split()[-1])
        elif image.mode != 'RGBA' and new_format == 'PNG':
            new = content.convert('RGBA')
        else:
            new = image

        buffer = io.BytesIO()
        new.save(buffer, format=new_format)
        buffer.seek(0)
        new_image = ImgHandler.open(buffer)
        return new_image



class ImageIO(IO):
    def read(self) -> Image:
        supported_formats = ImageFormat.as_list()
        suffix = self.get_suffix()
        if not suffix in supported_formats:
            raise ValueError(f'Unsupported image format: {suffix}')
        return ImgHandler.open(self.fpath)

    def write(self, image: Image):
        image.save(self.fpath)

    def view(self):
        image = self.read()
        image.show()
