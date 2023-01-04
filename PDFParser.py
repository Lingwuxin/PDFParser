import pdfplumber
SIT_DEVATION = 10e-6


class PDFParser:
    def __init__(self, path: str = None) -> None:
        self.pdf = None
        self.read_pdf(path=path)

    def read_pdf(self, path: str):
        self.pdf = pdfplumber.open(path_or_fp=path)

    def find_header(self):
        pass
    def find_toc(self):
        pass
    def close(self):
        self.pdf.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.close()
            return True
        except:
            return False


if __name__ == '__main__':
    with PDFParser('8180733.PDF') as parser:
        pass
