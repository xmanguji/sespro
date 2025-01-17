import io
from typing import BinaryIO, Tuple

from PIL import Image

# size = (128, 128)
size = (512, 512)

def make_thumbnails(image: str, thumbnails_dim: Tuple[int, int]) -> BinaryIO:
    max_width, max_height = thumbnails_dim
    try:
        buf = io.BytesIO(image)
        img = Image.open(buf)
        img_copy = img.copy()
        old_width, old_height = img_copy.size
        aspect_ratio = old_width / old_height
        new_width = int(max_height * (aspect_ratio))
        if new_width > max_width:
            img_copy = img.copy()
            img_copy.thumbnail(thumbnails_dim, Image.Resampling.LANCZOS)
        else:
            img_copy = img_copy.resize((new_width, max_height), Image.Resampling.LANCZOS)

        buffer = io.BytesIO()
        img_copy.save(buffer, "JPEG")
        buffer.seek(0)
        return buffer

    except IOError as e:
        print(e)
        return False


if __name__ == "__main__":
    make_thumbnails("image.jpg", size)
