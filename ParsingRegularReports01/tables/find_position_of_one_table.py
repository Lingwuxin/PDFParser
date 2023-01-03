import re
import itertools

# 分析表的起止位置。思路是每个字的重复次数是正确的
def find_position_of_one_table(self, nth_of_total_tables):
    table=self.all_tables[nth_of_total_tables]
    page_number=table["page_number"]
    this_page_text=self.all_pages[page_number]["page_text"]
    # 找出表中所有的字
    chars_total_length=0
    all_chars={}
    for coordinates in table["nonempty_cells_coordinates_list"]:
        cell_text_raw_clean=table["table_content"][coordinates[0]][coordinates[1]].replace("√", "checkme")
        cell_text=''.join(x for x in cell_text_raw_clean if x.isalnum())
        chars_total_length+=len(cell_text)
        for char in cell_text:
            if char not in all_chars.keys():
                all_chars[char]=1
            else:
                all_chars[char]+=1
    table["chars_total_length"]=chars_total_length
    # 找出表中每个字的出现次数
    chars_occurrences={}
    for key, value in all_chars.items():
        if value not in chars_occurrences.keys():
            chars_occurrences[value]=[key]
        else:
            chars_occurrences[value].append(key)
    # 对每个字，在全文中不同的block中查找看出现的次数。
    chars_occurrences_keys=list(chars_occurrences.keys())
    chars_occurrences_keys.sort(reverse=True)
    tentative_positions=[]
    for nth_start in range(len(this_page_text)-(chars_total_length-1)): # 全文中每个block由这个i定义，i也是表的起始位置
        this_try_text=this_page_text[nth_start : nth_start+chars_total_length]
        all_matched=1
        for occurrence in chars_occurrences_keys: # j是一个字出现了几次
            chars_this_occurrences=chars_occurrences[occurrence]
            if_continue=1
            for char in chars_this_occurrences: # 出现若干次的字又有若干个，依次检查。每次就是char
                n_matches=0
                for match in re.finditer(char, this_try_text):
                    n_matches+=1
                if n_matches!=occurrence:
                    if_continue=0
                    all_matched=0
                    break
            if if_continue==0:
                break
        # 中止检查字频。条件：前一个block是正确的，本block是错误的才中止。如果本表只有2行，则一直检查到文末
        if all_matched==1:
            tentative_positions.append((page_number, nth_start, nth_start+chars_total_length))
        elif len(tentative_positions)>0:
            if tentative_positions[-1][1] + 1 == nth_start:
                if table["n_rows"]>2:
                    break

    # 对一些特殊情况做处理
    # 特殊情况1：相邻的位置。如果首尾文字相同，则在先的位置是正确的
    # if len(tentative_positions)>1:
    #     adjacent_positions=[]
    #     for nth_position in range(1, len(tentative_positions)):
    #         this=tentative_positions[nth_position]
    #         previous=tentative_positions[nth_position-1]
    #         if ((this[0]==previous[0]) & (this[1]==previous[1]+1)):
    #             if_adjacent=True
    #         else:
    #             if_adjacent=False
    #         if if_adjacent==True:
    #             if adjacent_positions==[]:
    #                 adjacent_positions.append([nth_position-1,nth_position])
    #             else:
    #                 if adjacent_positions[-1][-1]==nth_position-1:
    #                     adjacent_positions[-1].append(nth_position)
    #                 else:
    #                     adjacent_positions.append([nth_position-1,nth_position])
    #     if len(adjacent_positions)>0:
    #         positions_to_be_removed=[]
    #         for nth_adjacent in range(len(adjacent_positions)):
    #             original_positions=adjacent_positions[nth_adjacent][:]
    #             page_number=self.all_tables[nth_of_total_tables]["page_number"]
    #             chars_total_length=self.all_tables[nth_of_total_tables]["chars_total_length"]
    #             table_text=self.all_pages[page_number]["page_text"][tentative_positions[original_positions[0]][1]:tentative_positions[original_positions[-1]][2]]
    #             for n_same_chars in range(chars_total_length):
    #                 if table_text[n_same_chars] != table_text[-n_same_chars]:
    #                     break
    #             if n_same_chars>0:
    #                 positions_to_be_removed=positions_to_be_removed + original_positions[1:]
    #         if len(positions_to_be_removed)>0:
    #             tentative_positions_refined=[]
    #             for idx in range(len(tentative_positions)):
    #                 if idx not in positions_to_be_removed:
    #                     tentative_positions_refined.append(tentative_positions[idx])
    #             if tentative_positions_refined!=[]:
    #                 tentative_positions=tentative_positions_refined[:]





    # 最终导出数据
    table["tentative_positions"]=tentative_positions[:]
