import os
import tempfile
import zipfile

from pathlib import Path

from mediqbox.abc.abc_component import *
from mediqbox.loadpdf.doc import *

class LoadPdfConfig(ComponentConfig):
  min_figure_area_percentile: float = 0.1
  figure_scale: float = 1.0

class LoadPdfInputData(InputData):
  input_file: str
  output_dir: str
  
class LoadPdf(AbstractComponent):

  def process(self, input_data: LoadPdfInputData) -> str:
    input_file = input_data.input_file
    output_dir = input_data.output_dir

    doc = fitz.open(input_file)

    pdf_doc = PdfDoc(
      doc=doc,
      file_size=os.path.getsize(input_file),
      sha256sum=sha256sum(input_file)
    )
    pdf_doc.cleanse()

    with tempfile.TemporaryDirectory() as tmpdir:
      # Save cleansed PDF file
      cleansed_pdf_file = os.path.join(tmpdir, "cleansed.pdf")
      pdf_doc.save(cleansed_pdf_file)

      # Extract figures
      figure_dir = os.path.join(tmpdir, "figures")
      os.mkdir(figure_dir)
      pdf_doc.extract_figures(
        figure_dir,
        scale=self.config.figure_scale,
        min_figure_area_percentile=self.config.min_figure_area_percentile)
      
      # Zip files
      fstem = Path(input_file).stem
      zip_filename = os.path.join(output_dir, f"{fstem}.zip")
      with zipfile.ZipFile(zip_filename, "w") as zipf:
        zipf.write(
          cleansed_pdf_file,
          arcname=os.path.join(fstem, os.path.basename(cleansed_pdf_file)))
        
        for item in os.listdir(figure_dir):
          archive_name = os.path.join(fstem, "figures", item)
          zipf.write(os.path.join(figure_dir, item), arcname=archive_name)

    doc.close()

    return