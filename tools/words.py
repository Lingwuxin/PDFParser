from typing import Dict, List


def rerange_words(words: List[Dict[str, str]], position: str = 'top'):#根据坐标信息重新排列字词块
    index_dict:Dict[float,int]={}
    rerange_words_list: List[List[Dict[str, str]]] = []
    if position not in {'x0', 'x1', 'top', 'doctop', 'bottom'}:
        return rerange_words_list
    if len(words) == 0:
        return rerange_words_list
    pre_word_position = None
    for index in range(1, len(words)):
        word = words[index]
        if word[position] != pre_word_position:
            rerange_words_list.append([word])
            pre_word_position = word[position]
            
        else:
            rerange_words_list[-1].append(word)
    return rerange_words_list

def judge_position(word_bbox: List[float], page_width: float) -> bool:
    right, left = True, False
    x0 = word_bbox[0]
    x1 = word_bbox[2]
    if x0+x1 > page_width:
        return left
    else:
        return right