from __future__ import annotations

import PIL.Image as ImgHandler
from PIL.Image import Image

from .file import File


# ---------------------------------------------------------


class ImageFile(File):
    def check_content_ok(self) -> bool:
        pass

    def read(self) -> Image:
        return ImgHandler.open(self.fpath)

    def write(self, image: Image):
        image.save(self.fpath)

    def view(self):
        with self.read() as image:
            image.show()
