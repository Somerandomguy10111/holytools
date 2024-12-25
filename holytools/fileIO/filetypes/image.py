from __future__ import annotations

import PIL.Image as ImgHandler
from PIL.Image import Image

from .file import File


# ---------------------------------------------------------


class ImageFile(File):
    def check_is_ok(self) -> bool:
        if not self._get_suffix() in ['png', 'jpg', 'jpeg']:
            if self._get_suffix():
                raise TypeError(f'Path \"{self.fpath}\" indicates unsupported image format: \"{self._get_suffix()}\"')
            else:
                raise TypeError(f'Path \"{self.fpath}\" does not indicate file type through suffix')
        return True

    def read(self) -> Image:
        return ImgHandler.open(self.fpath)

    def write(self, image: Image):
        image.save(self.fpath)

    def view(self):
        with self.read() as image:
            image.show()
