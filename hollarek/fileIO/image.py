from PIL import Image
from PIL.Image import Image as PilImage
from .file_io import IO


class ImageIO(IO):
    def read(self) -> PilImage:
        supported_formats = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp']
        suffix = self.get_suffix()
        if not suffix in supported_formats:
            raise ValueError(f'Unsupported image format: {suffix}')

        image = Image.open(self.fpath)
        return image

    def write(self, image: PilImage) -> None:
        image.save(self.fpath)


    def view(self):
        image = self.read()
        image.show()
