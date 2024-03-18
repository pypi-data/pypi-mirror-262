import fitz
import os

from fitz import Document, Page
from pydantic import BaseModel, Field
from typing import Literal

from mediqbox.loadpdf.rect import *

class Image(BaseModel):
  number: int
  bbox: tuple[float, float, float, float]
  width: int
  height: int
  cs_name: str = Field(alias="cs-name")
  colorspace: int
  xres: int           # resolution in x-direction
  yres: int           # resolution in y-direction
  bpc: int            # bits per component
  size: int           # storage occupied by image
  digest: bytes       # MD5 hashcode
  xref: int           # image xref or 0

class Drawing(BaseModel):
  type_: Literal["f", "s", "fs"] = Field(alias="type")
  bbox: tuple[float, float, float, float] = Field(alias="rect")

def get_images(
    page: Page
) -> list[Image]:
  return [Image.model_validate(img)
          for img in page.get_image_info(xrefs=True) if img.get('xref', 0)]

def get_drawings(
    page: Page
) -> list[Drawing]:
  return [Drawing.model_validate(drw)
          for drw in page.get_cdrawings()]

"""
def get_raw_image_rects(
    page: Page
) -> list[Rect]:
  image_rects: list[Rect] = []

  for image in page.get_images(full=True):
    image_rects += page.get_image_rects(image)

  return image_rects

def get_raw_drawing_rects(
    page: Page
) -> list[Rect]:
  drawing_rects: list[Rect] = []

  for path in page.get_cdrawings(extended=True):
    if 'rect' in path:
      drawing_rects.append(Rect(path['rect']))
          
  return drawing_rects
"""
'''
def get_images_on_rect(
    page: Page,
    rect: Rect
) -> list[tuple]:
  """
  Get images that intersect a given rect
  """
  images_on_rect: list[tuple] = []

  images = page.get_images()
  for img in images:
    rects = page.get_image_rects(img)
    for r in rects:
      if intersect(r, rect):
        images_on_rect.append(img)
        break

  return images_on_rect

def get_images_outside_rect(
    page: Page,
    rect: Rect
) -> list[tuple]:
  images_outside_rect: list[tuple] = []

  images = page.get_images()
  for img in images:
    rects = page.get_image_rects(img)
    outside = True
    for r in rects:
      if intersect(r, rect):
        outside = False
        break
    if outside:
      images_outside_rect.append(img)
  
  return images_outside_rect

def remove_images(
    page: Page,
    images: list[tuple]
) -> None:
  """
  Remove images.

  The images aren't actually deleted, but replaced by transparent "dummy" images. See https://pymupdf.readthedocs.io/en/latest/page.html#Page.delete_image
  """
  for img in images:
    page.delete_image(img[0])
'''

def recoverpix(
    doc: Document,
    xref: int,
    smask: int
) -> dict:
  """
  Extract an image of a document.

  https://github.com/pymupdf/PyMuPDF-Utilities/blob/master/examples/extract-images/extract-from-pages.py

  :param xref: xref of PDF image
  :param smask: xref the its /SMask
  :return: dictionary of the image data
  """
  # special case: /SMask or /Mast exists
  if smask > 0:
    pix0 = fitz.Pixmap(doc.extract_image(xref)["image"])
    if pix0.alpha: # catch irregular situation
      pix0 = fitz.Pixmap(pix0, 0) # remove alpha channel
    mask = fitz.Pixmap(doc.extract_image(smask)["image"])

    try:
      pix = fitz.Pixmap(pix0, mask)
    except: # fallback to original base image in case of problems
      pix = fitz.Pixmap(doc.extract_image(xref)["image"])

    if pix0.n > 3:
      ext = "pam"
    else:
      ext = "png"

    return { # create dictionary expected by caller
      "ext": ext,
      "colorspace": pix.colorspace.n,
      "image": pix.tobytes(ext)}
  
  # special case: /Colorspace definition exists
  # to be sure, we convert these cases to RGB PNG images
  if "/Colorspace" in doc.xref_object(xref, compressed=True):
    pix = fitz.Pixmap(doc, xref)
    pix = fitz.Pixmap(fitz.csRGB, pix)
    return { # create dictionary expected by caller
      "ext": "png",
      "colorspace": 3,
      "image": pix.tobytes("png")}
  
  return doc.extract_image(xref)

'''
def extract_images(
    page: Page,
    imgdir: str,
    dimlimit: int = 0, # 100 in pixels
    relsize: float = 0.0, # 0.05 (5%)
    abssize: int = 0 # 2048 in bytes
) -> int:
  """
  Extract images on a page into the output folder.

  https://github.com/pymupdf/PyMuPDF-Utilities/blob/master/examples/extract-images/extract-from-pages.py

  :param page: The page of a document
  :param imgdir: The output folder
  :param dimlimit: The minimum size of the image's each dimension/side
  :param relsize: The minimum size ratio of the image
  :param abssize: The minimum absolution image size
  :return: Number of extracted images
  """
  doc = page.parent
  xreflist = []
  imglist = []

  for img in page.get_images():
    xref, smask = img[0], img[1]
    if xref in xreflist:
      # explored already
      continue

    xreflist.append(xref)

    width = img[2]
    height = img[3]
    if min(width, height) <= dimlimit:
      # smaller than the minimum side size
      continue

    image = recoverpix(doc, xref, smask)
    n = image['colorspace']
    imgdata = image['image']

    if len(imgdata) <= abssize:
      # less than the minimum absolute size
      continue
    if len(imgdata) / (width * height * n) <= relsize:
      # less than the minimum size ratio
      continue

    imgfile = os.path.join(imgdir, "img%05i.%s" % (xref, image['ext']))
    with open(imgfile, "wb") as fp:
      fp.write(imgdata)

    imglist.append(xref)

  return len(imglist)
'''