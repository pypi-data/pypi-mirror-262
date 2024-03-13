from os import environ
from .async_core import GeminiClient
from .core import Gemini
from .src.model.image import GeminiImage
from .src.model.output import GeminiCandidate, GeminiModelOutput
from .src.misc import *
from .src.parser import *
from .src.tools import *
from .src.tools.google import *

gemini_api_key = environ.get("GEMINI_COOKIES")

__version__ = "2.1.0"
__author__ = (
    "daniel park <parkminwoo1991@gmail.com>, antonio cheang <teapotv8@proton.me>"
)
