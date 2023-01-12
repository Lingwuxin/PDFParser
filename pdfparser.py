import time
import pdfplumber
from pdfplumber.page import Page
from pdfplumber.table import Table
from typing import List, Dict
from tools.headers import Headers
# 一些全局参数
SIT_DEVATION = 10e-6  # 坐标中存在大量的浮点数，当两个坐标的差的绝对值小于10e-6时，认为两个坐标是相同的。
HEADER_MAX_ROW = 10  # 在确定页眉内容时最多只检查HEADER_MAX_ROW个字块
'''
关于坐标位置的说明
bbox记录四个位置信息(x0,y0,x1,y1)用来标记一个矩形区域,
其中x0、y0记录到左边界的距离,y0、y1记录到上边界的距离
下面是项目地址(https://github.com/jsvine/pdfplumber)中的部分文档说明
x0	Distance of left-side extremity from left side of page.
x1	Distance of right-side extremity from left side of page.
y0	Distance of bottom extremity from bottom of page.
y1	Distance of top extremity bottom of page.
top	Distance of top of line from top of page.
bottom	Distance of bottom of the line from top of page.
doctop	Distance of top of line from top of document.
'''


class Parser:
    def __init__(self, path: str = None) -> None:
        self.header_is_find = False
        self.pdf: pdfplumber.pdf.PDF = None
        self.pdf_file = None
        self.pdf_num = 0
        self.all_page_words: List[List[Dict[str, str]]] = []
        self.all_page_tables: List[List[Table]] = []
        self.open(path=path)
        self.read_pdf()
        self.headers = Headers(pages_num=self.pages_num)

    def open(self, path):
        self.pdf_file = open(path, 'rb')

    def read_pdf(self):
        self.pdf = pdfplumber.open(path_or_fp=self.pdf_file)
        self.pages_num = len(self.pdf.pages)
        for page in self.pdf.pages:
            self.all_page_words.append(page.extract_words())
            self.all_page_tables.append(page.find_tables())

    def get_header(self):
        if self.header_is_find == False:
            self.header_is_find = self.find_header_words()
        return self.headers.get_header()

    # 确定页眉的内容
    def find_header_words(self) -> bool:
        word_num = 0
        word = ''
        while True:
            for pagination in range(len(self.all_page_words)):
                if not pagination+1 < len(self.all_page_words):
                    break
                # 拿到当前页的所有字块
                now_page_words = self.all_page_words[pagination]
                # 拿到下一页的所有字块
                next_page_words = self.all_page_words[pagination+1]
                # 判断当前字块序号是否超出索引范围
                if not word_num < len(now_page_words) or not word_num < len(next_page_words):
                    continue
                # 判断前后两页相同序号的字块是否相同，如果相同则有可能是页眉
                if now_page_words[word_num]['text'] == next_page_words[word_num]['text']:
                    word = now_page_words[word_num]
                    if pagination == 0:
                        self.headers.append(
                            word=word, pagination=pagination)
                    self.headers.append(
                        word=word, pagination=pagination+1)
            if self.headers.header_is_find(word_num=word_num, word_text=word['text']):
                return True
            word_num += 1
            if word_num > HEADER_MAX_ROW:
                return False

    # own_header 表示该页是否有页眉
    def consolidate_tables(self, pagination: int, table_num: int, own_header: bool) -> dict[str, list[int]]:
        # 此函数用来判断下一页的第一张表格是否与上一页最后一张表格是同一张表格
        def table_is_consecutive(header_msg: list[Dict[str, str]], page_words: list[Dict[str, str]], table_top: str):
            try:
                for word_num, header_word in enumerate(page_words):
                    if word_num < len(header_msg):
                        if not header_msg[word_num]['text'] == header_word['text']:
                            return False
                    else:
                        if table_top <= header_word['top']:
                            return True
                        else:
                            return False

            except Exception as e:
                print(e)
                return False
        table_statue: Dict[str, list] = {
            'pagination': [pagination],
            'list': [table_num]
        }
        header_msg = self.get_header()
        while True:
            if not pagination+1 < self.pages_num:
                break
            page = self.pdf.pages[pagination+1]
            tables = page.find_tables()
            table_top = tables[0].bbox[1]
            page_words = page.extract_words()
            if table_is_consecutive(header_msg=header_msg, page_words=page_words, table_top=table_top):
                table_statue['pagination'].append(pagination+1)
                table_statue['list'].append(1)
            if not len(tables) == 1:
                break
            pagination += 1
        return table_statue
    

    def find_toc(self) -> List[int]:
        page_numbers: List[int] = []
        for page in self.pdf.pages:
            if len(page.annots):
                print(f'Msg from find_toc: 在第{page.page_number}页找到目录')
                page_numbers.append(page.page_number)
        return page_numbers

    def get_toc(self):
        pass

    def close(self):
        self.pdf_file.close()
        self.pdf.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


if __name__ == '__main__':
    with Parser('test.PDF') as parser:
        pass
