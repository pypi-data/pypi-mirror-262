from fitz import Page
from pydantic import BaseModel, ConfigDict, Field, root_validator
from typing import Any

class FontItem(BaseModel):
  # Make it immutable to make it hashable
  model_config = ConfigDict(frozen=True)

  font: str
  size: float = Field(gt=0.0)
  color: int

  @root_validator(pre=True)
  def make_hashable(cls, values: Any) -> Any:
    # This method ensures all values are processed before the model is initialized
    return values
  
  def __hash__(self):
    # This method computes a hash value for the model
    return hash((type(self), ) + tuple(self.__dict__.values()))

class FontStat(BaseModel):
  total_chars: int = 0
  fonts: dict[FontItem, int] = {}

class TextSpan(BaseModel):
  font: str
  size: float
  color: int
  flags: int
  ascender: float
  descender: float
  origin: tuple[float, float]
  bbox: tuple[float, float, float, float]
  text: str

class TextLine(BaseModel):
  wmode: int = 0
  dir_: tuple[float, float] = Field(alias="dir")
  bbox: tuple[float, float, float, float]
  spans: list[TextSpan]

  @property
  def text(self) -> str:
    return ''.join(span.text for span in self.spans)

class TextBlock(BaseModel):
  number: int
  type_: int = Field(alias="type", default=0, ge=0, le=0) # can only be 0
  bbox: tuple[float, float, float, float]
  lines: list[TextLine]
  
  @property
  def text(self) -> str:
    return '\n'.join([line.text for line in self.lines])

def get_text_blocks(
    page: Page
) -> list[TextBlock]:
  blocks = [block for block in page.get_text("dict")['blocks']
            if block['type'] == 0]
  
  return [TextBlock.model_validate(block)
          for block in blocks if block['type'] == 0]

def do_font_stat(
    text_blocks: list[TextBlock]
) -> FontStat:
  font_stat = FontStat()

  for block in text_blocks:
    for line in block.lines:
      for span in line.spans:
        font_item = FontItem(
          font=span.font, size=span.size, color=span.color)
        font_stat.fonts[font_item] = font_stat.fonts.get(font_item, 0) + len(span.text)
        font_stat.total_chars += len(span.text)

  return font_stat

def sort_font_stat(
    font_stat: FontStat,
    reverse: bool = True
) -> list[tuple[FontItem, int, float]]:
  sorted_stat = sorted(font_stat.fonts.items(), key=lambda item: item[1], reverse=reverse)

  result = []
  for item in sorted_stat:
    result.append(item + (item[1]/font_stat.total_chars,))

  return result

def get_major_fonts(
    blocks: list[TextBlock],
    plimit: float = 0.05,
    nlimit: int|None = None
) -> list[tuple[FontItem, int, float]]:
  sorted_fonts = sort_font_stat(do_font_stat(blocks))
  major_fonts = [font[0] for font in sorted_fonts if font[2] >= plimit]

  if nlimit:
    return major_fonts[:nlimit]

  return major_fonts

def find_major_font_text_blocks(
    text_blocks: list[TextBlock],
    major_fonts: list[FontItem],
    charlimit: int = 30,
    plimit: float = 0.3
) -> list[TextBlock]:
  return [block for block in text_blocks
          if len([font for font in get_major_fonts([block], plimit=plimit)
                  if font in major_fonts])
          and len(block.text) >= charlimit]