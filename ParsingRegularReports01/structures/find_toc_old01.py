import re
import itertools

def find_toc(self):
    # 先查找目录页
    toc_possible_positions=[]
    for page_number in range(self.total_pages):
        for match in re.finditer("目录", self.all_pages[page_number]["page_text"]):
            toc_start=match.span()[0]
            toc_end=match.span()[1]
            if_best_guess=False
            if this_page["if_found_header"]==True:
                if toc_start-self.header_len<=5:
                    if_best_guess=True
            if this_page_text[toc_end]=='第':
                if_best_guess=True
            if if_best_guess==True:
                toc_possible_positions.append((page_number, toc_start, toc_end))
    # 把目录具体内容取出来
    toc_extracted=[]
    for i in rang(len(toc_possible_positions)):
        toc_extracted_from_one_possible=[]
        page_number=toc_possible_positions[i][0]
        toc_end=toc_possible_positions[i][2]
        this_page_text=self.all_pages[page_number]["page_text"]

        this_section_list=[]
        this_section_page=[]
        for nth_char in range(toc_end, len(this_page_text)):
            char=this_page_text[nth_char]
            if nth_char==toc_end:
                this_section_list.append(char)
            else:
                if char.isdigit()==True:
                    this_section_page.append(char)
                else:
                    if this_page_text[nth_char-1].isdigit()==True:
                        if this_section_list[0]=='第':
                            toc_extracted_from_one_possible.append((''.join(this_section_list), int(''.join(this_section_page))))
                        this_section_list=[]
                        this_section_page=[]
                    this_section_list.append(char)
            if nth_char==len(this_page_text)-1:
                if this_section_list[0]=='第':
                    tentative_append=(''.join(this_section_list), int(''.join(this_section_page)))
                    if tentative_append != toc_extracted_from_one_possible[-1]:
                        toc_extracted_from_one_possible.append(tentative_append)
        possbile_toc_text=''.join(toc_extracted_from_one_possible)
a='一'
a.isnumeric()
        toc_extracted.append(toc_extracted_from_one_possible)

    # 如果目录具体内容取出来了，进一步检查页码
    self.toc_pages={}
    if len(toc_possible_positions)==1:
        toc_at_page_number=toc_possible_positions[0][0]
    else:
        toc_at_page_number=0
    for nth_section in range(len(toc_extracted_from_one_possible)):
        section_name=toc_extracted_from_one_possible[nth_section][0]
        section_toc_page=toc_extracted_from_one_possible[nth_section][1]
        if nth_section==0:
            check_from_this_page=toc_at_page_number+1
        else:
            if len(self.toc_pages[nth_section-1]["section_pdf_page"])==1:
                check_from_this_page=self.toc_pages[nth_section-1]["section_pdf_page"][0]["section_at_page_number"]+1
            else:
                check_from_this_page=toc_at_page_number+1
        pages=[]
        for page_number in range(check_from_this_page, self.total_pages):
            this_page=self.all_pages[page_number]
            this_page_text=this_page["page_text"]
            for match in re.finditer(section_name, this_page_text):
                pages.append({
                    "section_at_page_number": page_number,
                    "section_title_start": match.span()[0],
                    "section_title_end": match.span()[1],
                })
        self.toc_pages[nth_section]={
            "section_name": section_name,
            "section_toc_page": section_toc_page,
            "section_pdf_page": pages[:]
        }
    #如果有多个页码，取第一个，并取出下一个section的位置
    self.toc_pages_refined={}
    for nth_section in range(len(toc_extracted_from_one_possible)):
        this_section_info=self.toc_pages[nth_section]["section_pdf_page"][0]
        self.toc_pages_refined[nth_section]=this_section_info
        if nth_section==len(toc_extracted_from_one_possible)-1:
            self.toc_pages_refined[nth_section]["next_section_at_page_number"]=self.total_pages-1
            self.toc_pages_refined[nth_section]["next_section_title_start"]=len(self.all_pages[self.total_pages-1]["page_text"])-1
        else:
            self.toc_pages_refined[nth_section]["next_section_at_page_number"]=self.toc_pages[nth_section+1]["section_pdf_page"][0]["section_at_page_number"]
            self.toc_pages_refined[nth_section]["next_section_title_start"]=self.toc_pages[nth_section+1]["section_pdf_page"][0]["section_title_start"]
