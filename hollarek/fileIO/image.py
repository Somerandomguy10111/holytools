from PIL import Image
from PIL.Image import Image as PilImage
from .file_io import IO


class ImageIO(IO):
    @staticmethod
    def read(fpath: str) -> PilImage:
        image = Image.open(fpath)
        return image

    @staticmethod
    def write(fpath: str, image: PilImage) -> None:
        image.save(fpath)