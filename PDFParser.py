import pdfplumber
from pdfplumber.page import Page
from typing import List, Dict

SIT_DEVATION = 10e-6
HEADER_MAX_ROW = 10
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


class HeaderMsg:
    def __init__(self):
        self.cout: int = 0  # 记录该字块出现的次数
        self.page_num_list: List[int] = []  # 记录该子块在那些页面出现
        self.word_msg_dict: Dict[str, str] = dict()

    def __str__(self) -> str:
        return str([self.cout, self.page_num_list])


class Headers:
    def __init__(self, pages_num: int):
        self.max = 0
        self.pages_num = pages_num
        self.header_words: Dict[str, HeaderMsg] = {}

    def append(self, word: Dict[str, str], page_num: int):
        word_text = word['text']
        if word_text not in self.header_words:
            tmp_header_msg = HeaderMsg()
            tmp_header_msg.cout = 1
            tmp_header_msg.page_num_list.append(page_num)
            tmp_header_msg.word_msg_dict = word
            self.header_words[word_text] = tmp_header_msg
        else:
            self.header_words[word_text].cout += 1
            self.header_words[word_text].page_num_list.append(page_num)
        if self.max < self.header_words[word_text].cout:
            self.max = self.header_words[word_text].cout

    # word_num是字块的序号 当word_num=0时，self.header_word
    def header_is_find(self, word_num: int, word_text: str):
        if word_num < 1:
            return False
        elif self.header_words[word_text].cout < self.max:
            return True

    def get_header(self):
        self.header_list: List[Dict[str, str]] = []
        for header_word, header_msg in self.header_words.items():
            if header_msg.cout > self.pages_num/2:
                self.header_list.append(header_msg.word_msg_dict)
        return self.header_list

    def __str__(self) -> str:
        res = ''
        for key, item in self.header_words.items():
            res += f'{key}:{str(item)}\n'

        return res


class PDFParser:
    def __init__(self, path: str = None) -> None:
        self.header_is_find = False
        self.pdf: pdfplumber.pdf.PDF = None
        self.all_page_words: List[List[Dict[str, str]]] = []
        self.read_pdf(path=path)

    def read_pdf(self, path: str):
        self.pdf = pdfplumber.open(path_or_fp=path)
        self.pages_num = len(self.pdf.pages)
        for page in self.pdf.pages:
            self.all_page_words.append(page.extract_words())

    def get_header(self):
        if self.header_is_find == False:
            self.find_header_words()
        return self.headers.get_header()
    # 确定页眉的内容

    def find_header_words(self) -> bool:
        self.headers = Headers(pages_num=len(self.pdf.pages))
        word_num = 0
        word = ''
        while True:

            for page_num in range(len(self.all_page_words)):
                if not page_num+1 < len(self.all_page_words):
                    break
                now_page_words = self.all_page_words[page_num]
                next_page_words = self.all_page_words[page_num+1]
                if not word_num < len(now_page_words) or not word_num < len(next_page_words):
                    continue
                if now_page_words[word_num]['text'] == next_page_words[word_num]['text']:
                    word = now_page_words[word_num]
                    if page_num == 0:
                        self.headers.append(
                            word=word, page_num=page_num)
                    self.headers.append(
                        word=word, page_num=page_num+1)
            if self.headers.header_is_find(word_num=word_num, word_text=word['text']):
                self.header_is_find = True
                return True
            word_num += 1
            if word_num > HEADER_MAX_ROW:
                return False

    def find_toc(self):
        pass

    def close(self):
        self.pdf.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


if __name__ == '__main__':
    with PDFParser('test.PDF') as parser:
        print(parser.get_header())
