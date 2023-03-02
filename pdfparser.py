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
bbox记录四个位置信息(x0, top, x1, bottom)用来标记一个矩形区域,
下面是项目地址(https://github.com/jsvine/pdfplumber)中的部分文档说明
x0	Distance of left-side extremity from left side of page.
x1	Distance of right-side extremity from left side of page.
y0	Distance of bottom extremity from bottom of page.
y1	Distance of top extremity bottom of page.
top	Distance of top of line from top of page.
bottom	Distance of bottom of the line from top of page.
doctop	Distance of top of line from top of document.
'''


def show_page(page: Page, bbox_or_obj=None):
    im = page.to_image()
    if bbox_or_obj is not None:
        try:
            im.draw_rect(bbox_or_obj)
        except:
            print('from show_page:图形绘制失败')
    im.show()


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
        self.find_header()

        self.cropped_pages: List[Page] = []
        self.crop_pages()  # 剪切掉所有页面的页眉页脚
        self.new_page_words: List[List[Dict[str, str]]] = []
        self.load_new_pages()

        self.possible_tocs: List[Dict[str, str]] = []
        self.find_toc()

    def open(self, path: str):
        self.pdf_file = open(path, 'rb')

    def read_pdf(self):
        self.pdf = pdfplumber.open(path_or_fp=self.pdf_file)
        self.pages_num = len(self.pdf.pages)
        for page in self.pdf.pages:
            self.all_page_words.append(page.extract_words())
            self.all_page_tables.append(page.find_tables())
    def load_new_pages(self):
        for page in self.cropped_pages:
            self.new_page_words.append(page.extract_words())
    # 确定页眉的内容
    def _find_header(self) -> bool:
        if self.header_is_find:
            return True
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

    def find_header(self):  # 深嵌套多耦合，完全没有可读性,如无必要，不要尝试读懂它
        if self._find_header():
            msg = ' '
            msg_list = self.headers.get_header_text_list()
            print(f'Msg from find_header: 页眉为\'{msg.join(msg_list)}\'')
        else:
            print('Error from find_header: 无法确认页眉')

    def crop_pages(self):
        header_num = self.headers.total_header
        header_text_list = self.headers.get_header_text_list()
        header_exist = True
        for page_index, page in enumerate(self.pdf.pages):
            words = page.extract_words()
            bottom: int = words[-3]['top']-1
            for i in range(header_num):
                if self.all_page_words[page_index][i]['text'] != header_text_list[i]:
                    header_exist = False
                    break
            if header_exist:
                top: int = self.all_page_words[page_index][header_num-1]['bottom']
                top += 10  # 冗余
                self.cropped_pages.append(
                    page.crop(bbox=[0, top, page.width, bottom]))
            header_exist = True

    # own_header 表示该页是否有页眉
    def consolidate_tables(self, pagination: int, table_num: int, own_header: bool = True) -> dict[str, list[int]]:
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

        self.table_statue: Dict[str, list] = {
            'pagination': [pagination],
            'list': [table_num]
        }
        header_msg = self.headers.get_header()
        while True:
            if not pagination+1 < self.pages_num:
                break
            page = self.pdf.pages[pagination+1]
            tables = page.find_tables()
            table_top = tables[0].bbox[1]
            page_words = page.extract_words()
            if table_is_consecutive(header_msg=header_msg, page_words=page_words, table_top=table_top):
                self.table_statue['pagination'].append(pagination+1)
                self.table_statue['list'].append(1)
            if not len(tables) == 1:
                break
            pagination += 1
        return self.table_statue

    def find_toc(self):
        page_numbers: List[int] = []
        for page in self.pdf.pages:
            if len(page.annots):
                print(f'Msg from find_toc: 在第{page.page_number}页找到目录')
                page_numbers.append(page.page_number)
        toc_crop_list: List[Page] = []
        for page_number in page_numbers:
            page = self.pdf.pages[page_number-1]
            for annot in page.annots:
                bbox = [annot['x0'], annot['top'],
                        annot['x1'], annot['bottom']]
                toc_crop_list.append(page.crop(bbox=bbox))
        for toc in toc_crop_list:
            words = toc.extract_words()
            tmp_dict = {}
            tmp_dict['section_num'] = words[0]['text']
            tmp_dict['section_name'] = words[1]['text']
            tmp_dict['section_page'] = words[3]['text']
            self.possible_tocs.append(tmp_dict)

    def rerange_words(self,words: List[Dict[str, str]], position: str = 'top'):#根据坐标信息重新排列字词块
        index_dict:Dict[float,int]={}
        rerange_words_list: List[List[Dict[str, str]]] = []
        if position not in {'x0', 'x1', 'top', 'doctop', 'bottom'} or len(words) == 0:
            return rerange_words_list,index_dict
        pre_word_position = None
        index=0
        for i in range(1, len(words)):
            word = words[i]
            if word[position] != pre_word_position:
                index_dict[word[position]]=index
                index+=1
                rerange_words_list.append([word])
                pre_word_position = word[position]
            else:
                rerange_words_list[-1].append(word)
        return rerange_words_list,index_dict

    def find_words_in_pdf(self,target_str_or_list=None):#words_str_or_list="√不适用,√适用"
        def match_words(match_words,target_words):
            tmp_page_words = []
            for match in match_words:
                for word in target_words:
                    if word == match['text']:
                        tmp_page_words.append(match)
            return tmp_page_words
        words_msg: List[List[Dict[str]]] = []  # 列表中的每一个元素存储一个页的目标字词块信息
        target_words = target_str_or_list
        if isinstance(target_str_or_list, str):
            target_words = target_str_or_list.split(',')
        for matchs in self.all_page_words:
            tmp_page_words=match_words(match_words=matchs,target_words=target_words)
            words_msg.append(tmp_page_words)
        return words_msg


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
        print('Debug')
