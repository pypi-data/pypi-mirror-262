from PIL import Image, ImageDraw
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import ImageFormatter
from typing import Union
from pathlib import Path
import io


class CodeSnap:
    """
    A class for creating images from code snippets using Pygments and PIL.

    Args:
        language (str): The programming language of the code snippet.
        code (str): The code snippet to convert into an image.

    Attributes:
        lexer: The Pygments lexer for the specified programming language.
        code (str): The code snippet to convert into an image.
        image: The resulting image after creating it from the code snippet.
    """

    def __init__(self, language: str, code: str) -> None:
        """
        Initialize the CodeSnap object.

        Args:
            language (str): The programming language of the code snippet.
            code (str): The code snippet to convert into an image.
        """
        self.lexer = get_lexer_by_name(language, stripall=True)
        self.code = code.strip()

    def create(self, width: int = 800, height: int = 600, font_size: int = 14, line_numbers: bool = True) -> None:
        """
        Create the image from the code snippet.

        Args:
            width (int): The width of the resulting image.
            height (int): The height of the resulting image.
            font_size (int): The font size to use for the code text.
            line_numbers (bool): Whether to include line numbers in the image.
        """
        # Make a photo by using Pillow
        self.image = Image.new("RGB", (width, height), "white")
        ImageDraw.Draw(self.image)
        # Show text as a Photo
        code_bytes = highlight(self.code, self.lexer, ImageFormatter(font_size=font_size, line_numbers=line_numbers))
        code_img = Image.open(io.BytesIO(code_bytes))
        # Add text to picture
        self.image.paste(code_img, (50, 50))
    
    def show(self) -> None:
        """Show the resulting image."""
        self.image.show()
    
    def save(self,
             fp: Union[str, bytes, Path],
             format: str = 'PNG',
             bitmap_format: str = 'PNG',
             optimize: bool = False,
    ) -> None:
        """
        Save the resulting image to a file.

        Args:
            fp (Union[str, bytes, Path]): The file path or file object to save the image to.
            format (str): The format of image.
            bitmap_format (str): The format to save the image in (e.g., 'PNG', 'JPEG', 'GIF').
            optimize (bool): Whether to optimize the image.
        """
        self.image.save(fp, format=format, bitmap_format=bitmap_format, optimize=optimize)

    def to_bytes(self,
                 format: str = 'PNG',
                 bitmap_format: str = 'PNG',
                 optimize: bool = False,) -> bytes:
        """
        Convert the resulting image to bytes.

        Args:
            - format (str): The format of image.

        Returns:
            - bytes: The bytes representation of the resulting image.
        """
        output = io.BytesIO()
        self.image.save(output, format=format, bitmap_format=bitmap_format, optimize=optimize)
        return output.getbuffer()