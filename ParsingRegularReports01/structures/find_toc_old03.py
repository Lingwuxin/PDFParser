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
                last_char_position=toc_end
                for nth_char in range(toc_end, len(this_page_text)):
                    char=this_page_text[nth_char]
                    if (nth_char==toc_end):
                        this_section=[char]
                        keep_appending=True
                    else:
                        if char.isdigit()==False:
                            if keep_appending==True:
                                this_section.append(char)
                            else:
                                if char=='第':
                                    sections.append(''.join(this_section))
                                    if nth_char>last_char_position:
                                        last_char_position=nth_char
                                    this_section=[char]
                                    keep_appending=True
                                else:
                                    pass
                        else:
                            keep_appending=False
                self.possible_tocs.append(((page_number, toc_start, last_char_position), sections))
            else:
                print(f"Messages from find_toc: 发现“目录”，但不以第字开头。position:({page_number}, {toc_start}, {toc_end})")

    # 如果目录具体内容取出来了，进一步检查页码
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
        print(f"Success from find_toc：找到一个目录页，page_number={page_number}")
        print(self.possible_tocs[0][1])
        print("Need to continue to run find_section_pages")

    # self.toc_pages={}
    # if len(toc_possible_positions)==1:
    #     toc_at_page_number=toc_possible_positions[0][0]
    # else:
    #     toc_at_page_number=0
    # for nth_section in range(len(toc_extracted_from_one_possible)):
    #     section_name=toc_extracted_from_one_possible[nth_section][0]
    #     section_toc_page=toc_extracted_from_one_possible[nth_section][1]
    #     if nth_section==0:
    #         check_from_this_page=toc_at_page_number+1
    #     else:
    #         if len(self.toc_pages[nth_section-1]["section_pdf_page"])==1:
    #             check_from_this_page=self.toc_pages[nth_section-1]["section_pdf_page"][0]["section_at_page_number"]+1
    #         else:
    #             check_from_this_page=toc_at_page_number+1
    #     pages=[]
    #     for page_number in range(check_from_this_page, self.total_pages):
    #         this_page=self.all_pages[page_number]
    #         this_page_text=this_page["page_text"]
    #         for match in re.finditer(section_name, this_page_text):
    #             pages.append({
    #                 "section_at_page_number": page_number,
    #                 "section_title_start": match.span()[0],
    #                 "section_title_end": match.span()[1],
    #             })
    #     self.toc_pages[nth_section]={
    #         "section_name": section_name,
    #         "section_toc_page": section_toc_page,
    #         "section_pdf_page": pages[:]
    #     }
    # #如果有多个页码，取第一个，并取出下一个section的位置
    # self.toc_pages_refined={}
    # for nth_section in range(len(toc_extracted_from_one_possible)):
    #     this_section_info=self.toc_pages[nth_section]["section_pdf_page"][0]
    #     self.toc_pages_refined[nth_section]=this_section_info
    #     if nth_section==len(toc_extracted_from_one_possible)-1:
    #         self.toc_pages_refined[nth_section]["next_section_at_page_number"]=self.total_pages-1
    #         self.toc_pages_refined[nth_section]["next_section_title_start"]=len(self.all_pages[self.total_pages-1]["page_text"])-1
    #     else:
    #         self.toc_pages_refined[nth_section]["next_section_at_page_number"]=self.toc_pages[nth_section+1]["section_pdf_page"][0]["section_at_page_number"]
    #         self.toc_pages_refined[nth_section]["next_section_title_start"]=self.toc_pages[nth_section+1]["section_pdf_page"][0]["section_title_start"]
