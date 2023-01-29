from typing import List, Dict


class HeaderMsg:
    def __init__(self):
        self.cout: int = 0  # 记录该字块出现的次数
        self.pagination_list: List[int] = []  # 记录该子块在那些页面出现
        self.word_msg_dict: Dict[str, str] = dict()

    def __str__(self) -> str:
        return str([self.cout, self.pagination_list])


class Headers:
    def __init__(self, pages_num: int):
        self.max = 0
        self.pages_num = pages_num
        self.header_words: Dict[str, HeaderMsg] = {}
        self.header_list: List[Dict[str, str]] = []
        self.is_find = False
        self.total_header = 0

    def append(self, word: Dict[str, str], pagination: int):
        word_text = word['text']
        if word_text not in self.header_words:
            tmp_header_msg = HeaderMsg()
            tmp_header_msg.cout = 1
            tmp_header_msg.pagination_list.append(pagination)
            tmp_header_msg.word_msg_dict = word
            self.header_words[word_text] = tmp_header_msg
        else:
            self.header_words[word_text].cout += 1
            self.header_words[word_text].pagination_list.append(pagination)
        if self.max < self.header_words[word_text].cout:
            self.max = self.header_words[word_text].cout

    # word_num是字块的序号
    def header_is_find(self, word_num: int, word_text: str):
        if word_num < 1:
            return False
        elif self.header_words[word_text].cout < self.max:
            return True

    def get_header(self):
        if self.is_find:
            return self.header_list
        for header_word, header_msg in self.header_words.items():
            if header_msg.cout > self.pages_num/2:
                self.header_list.append(header_msg.word_msg_dict)
        self.is_find = True
        self.total_header = len(self.header_list)
        return self.header_list

    def get_header_text(self):
        self.header_text_list: List[str] = []
        for header_msg in self.get_header():
            self.header_text_list.append(header_msg['text'])
        return self.header_text_list

    def __str__(self) -> str:
        res = ''
        for key, item in self.header_words.items():
            res += f'{key}:{str(item)}\n'

        return res
