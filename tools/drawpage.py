import pdfplumber
from pdfplumber.page import Page
from typing import List


class DrawTool:
    def __init__(self) -> None:
        self.img_lit: List[Page] = []

    def append_page(self, page: Page) -> None:
        self.img_lit.append(page)

    def show_page(page: Page, bbox_or_obj=None) -> None:
        im = page.to_image()
        if bbox_or_obj is not None:
            try:
                im.draw_rect(bbox_or_obj)
            except:
                print('from show_page:图形绘制失败')
        im.show()
