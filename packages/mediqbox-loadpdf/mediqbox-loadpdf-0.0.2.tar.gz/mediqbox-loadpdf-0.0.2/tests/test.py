import os
import shutil

from mediqbox.loadpdf import LoadPdfConfig

from mediqbox.loadpdf import *
from tests.data import *

def test():
  # Clean up output directory
  for root, dirs, files in os.walk(output_dir):
    for f in files:
      os.unlink(os.path.join(root, f))
    for d in dirs:
      shutil.rmtree(os.path.join(root, d))

  # Test LoadPdf with all PDF files
  for _, fname in pdf_filenames.items():
    print(f"Processing file {fname} ...")
    LoadPdf(LoadPdfConfig(
      figure_scale=4.0
    )).process(LoadPdfInputData(
      input_file=os.path.join(data_dir, fname),
      output_dir=output_dir))

if __name__ == "__main__":
  test()