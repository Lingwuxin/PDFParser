import re
import itertools




def find_toc(self):
    self.possible_tocs=[]
    for page_number in range(self.total_pages):
        this_page_text=f"{self.all_pages[page_number]['page_text']}第"
        # 先查找目录页，并提取出所有的section
        for match in re.finditer("目录", this_page_text):
            toc_start=match.span()[0]
            toc_end=match.span()[1]
            if toc_end>=len(this_page_text):
                continue
            if this_page_text[toc_end] not in ['第', '1', '一']:
                continue
            if this_page_text[toc_end]=='第':
                sections=[]
                sections_toc_page=[]
                last_char_position=toc_end
                for nth_char in range(toc_end, len(this_page_text)):
                    char=this_page_text[nth_char]
                    if (nth_char==toc_end):
                        this_section=[char]
                        this_section_toc_page=[]
                        keep_appending=True
                    else:
                        if char.isdigit()==False:
                            if keep_appending==True:
                                this_section.append(char)
                            else:
                                if char=='第':
                                    this_section_title=''.join(this_section)
                                    this_section_toc_page=int(''.join(this_section_toc_page))
                                    sections.append(this_section_title)
                                    sections_toc_page.append((this_section_title, this_section_toc_page))
                                    if nth_char>last_char_position:
                                        last_char_position=nth_char
                                    this_section=[char]
                                    this_section_toc_page=[]
                                    keep_appending=True
                                else:
                                    pass
                        else:
                            keep_appending=False
                            this_section_toc_page.append(char)
                self.possible_tocs.append(((page_number, toc_start, last_char_position), sections, sections_toc_page))
            else:
                print(f"Messages from find_toc: 发现“目录”，但不以第字开头。position:({page_number}, {toc_start}, {toc_end})")

    # 总结本步的情况
    if len(self.possible_tocs)==0:
        self.need_intervention=1
        print("Warning from find_toc：没有找到目录页")
    elif len(self.possible_tocs)>1:
        self.need_intervention=1
        print("Warning from find_toc：找到多于1个目录页，需要手动确认")
        for nth_toc in range(len(self.possible_tocs)):
            toc=self.possible_tocs[nth_toc]
            print(f"\nnth_toc={nth_toc}")
            print(toc)
        print("Need to continue to run find_section_pages，注意这个函数的参数compare_nth_toc（取值应为为上面显示的nth_toc中的一个）就是选定的目录页")
    else:
        print(f"Success from find_toc：找到一个目录页，位置：{self.possible_tocs[0][0]}")
        # print(self.possible_tocs[0][1])
        # print("Need to continue to run find_section_pages")
