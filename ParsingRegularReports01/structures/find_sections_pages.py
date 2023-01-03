import re
import itertools

def find_sections_pages(self, compare_nth_toc=0):
    self.sections_pages_checked=[]
    self.sections_without_page_number=[]
    self.sections_with_abnormal_pages=[]
    # 最终建立self.section_titles，是个list，每个元素是个tuple，其元素依次是：本文第几节，本文中含节号的名称，本文中不含节号的名称，所在的位置（位置又是个tuple），前一个所在的位置，后一个所在的位置
    self.section_titles=[]


    sections=self.possible_tocs[compare_nth_toc][1]

    # 取出每一个section，然后在全文中查找位置，并把这些结果放在sections_pages_list用于下一步顺序比对
    self.sections_pages={}
    for nth_section in range(len(sections)):
        self.sections_pages[nth_section]=[]
    for page_number in range(self.possible_tocs[compare_nth_toc][0][0], self.total_pages):
        this_page_text=self.all_pages[page_number]['page_text']
        for nth_section in range(len(sections)):
            this_section=sections[nth_section]
            for match in re.finditer(this_section, this_page_text):
                self.sections_pages[nth_section].append((page_number, match.span()[0], match.span()[1]))
    sections_pages_list=[]
    for nth_section in range(len(sections)):
        this_item=self.sections_pages[nth_section]
        # 如果没有找到这个section，把它放入self.sections_without_page_number中
        if len(this_item)==0:
            self.need_intervention=1
            self.sections_without_page_number.append(sections[nth_section])
        else:
            sections_pages_list.append(this_item)

    if len(self.sections_without_page_number)>0:
        print("Error from find_sections_pages: Fail to find any position for the following sections")
        print(self.sections_without_page_number)


    # 进行顺序的比对
    ret_compare_positions_order=self.compare_positions_order(objects_list=sections_pages_list, first_position=self.possible_tocs[compare_nth_toc][0], last_position=None)


    # 如果比对的结果与原来的结果 行数一致，进一步判断
    if len(sections)==len(ret_compare_positions_order):
        self.sections_pages_checked=ret_compare_positions_order[:]

        for nth_section in range(len(sections)):
            if len(self.sections_pages_checked[nth_section])!=1:
                # 如果找到多个，保留哪个？规则：首先是找与目录页显示的页码一致的，然后在这里面保留第一个。
                multi_pages=self.sections_pages_checked[nth_section][:]
                multi_pages_refined=[]
                for position in multi_pages:
                    if position[0]+1 == self.possible_tocs[compare_nth_toc][2][nth_section][1]:
                        multi_pages_refined.append(position)
                if len(multi_pages_refined)==1:
                    self.sections_pages_checked[nth_section]=multi_pages_refined[0:1]
                else:
                    self.sections_with_abnormal_pages.append((sections[nth_section], self.sections_pages_checked[nth_section]))
        if len(self.sections_with_abnormal_pages)==0:
            print("Success from find_sections_pages: Find and Compare Sections Pages Succeeds.")
            # 建立self.section_titles，是个list，每个元素是个tuple，其元素依次是：本文第几节，本文中含节号的名称，本文中不含节号的名称，所在的位置（位置又是个tuple），前一个所在的位置，后一个所在的位置
            for nth_toc in range(len(self.possible_tocs[compare_nth_toc][1])):
                toc=self.possible_tocs[compare_nth_toc][1][nth_toc]
                if toc.startswith('第'):
                    cn_nums=[]
                    section_title=[]
                    for nth_char in range(1,len(toc)):
                        char=toc[nth_char]
                        if char.isnumeric():
                            cn_nums.append(char)
                        else:
                            break
                    this_position=self.sections_pages_checked[nth_toc]
                    if nth_toc==0:
                        previous_position=None
                    else:
                        previous_position=self.sections_pages_checked[nth_toc-1]
                    if nth_toc==len(self.possible_tocs[compare_nth_toc][1])-1:
                        next_position=[(self.total_pages-1, self.all_pages[self.total_pages-1]["page_text_len"]+1, self.all_pages[self.total_pages-1]["page_text_len"]+1)]
                    else:
                        next_position=self.sections_pages_checked[nth_toc+1]
                    self.section_titles.append((nth_toc, toc, toc[nth_char+1:], this_position, previous_position, next_position))
                    arabic_num=self.tools_num_cn2arabic[''.join(cn_nums)]
                    if arabic_num != 1+ nth_toc:
                        print(f"Error from find_sections_pages: the {nth_toc}-th toc has different Chinese and Arabic Numbers.")
                else:
                    print(f"Waring from find_sections_pages: the {nth_toc}-th toc does not start with 第.")
        else:
            self.need_intervention=1
            print(f"Warning from find_sections_pages: There are {len(self.sections_with_abnormal_pages)} sections that have abnormal pages.")
            print("self.sections_with_abnormal_pages is as follows:")
            print(self.sections_with_abnormal_pages)
    else:
        self.need_intervention=1
        print(f"Warning from find_sections_pages: The compared positions is fewer than self.sections_pages")
