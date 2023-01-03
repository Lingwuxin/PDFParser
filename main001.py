


# sys.path.append("/home/cuixin02/Coding/Python/Codes/cx_modules/")
# from HbSqlJobs008 import SqlJobs

from ParsingRegularReports01 import Parser

self=Parser(
    comp_info="南新制药2021年报",
    pdf_full_path="/Users/cuixin/CX/Coding/Python/Codes/识别/原始数据/南新制药688189（2020年报）.pdf"
)
self.read_in_pdf()

self.find_positions_of_all_tables()
self.remove_one_table(111)
self.find_positions_of_all_tables()

self.show_results(show_type="multi_position_tables")
self.update_tables_positions_checked()


self.find_header()
self.show_results(show_type="pages_without_header")

self.find_toc()

self.find_sections_pages()













self.find_fin_report_structure(fin_report_subsections="一审计报告,二财务报表,三公司基本情况,四财务报表的编制基础,五重要会计政策及会计估计,六税项,七合并财务报表项目注释,八合并范围的变更,九在其他主体中的权益,十与金融工具相关的风险,十一公允价值的披露,十二关联方及关联交易,十三股份支付,十四承诺及或有事项,十五资产负债表日后事项,十六其他重要事项,十七母公司财务报表主要项目注释,十八补充资料")

self.sections_pages
self.possible_tocs[0][1]
self.sections_pages_checked




for x in sections:
    print(x)
self.fin_report_subsections
self.fin_report_subsections_positions_dict


# 如果有self.unfound_subsections，应当停下来，看一下什么原因。这又需要写一些程序，比如单独修正某一个问题，或者重新再跑一遍（比如subsection的名字有其他的）。总之，最后应当确保subsection是全部找到的
# 目录应当最后一个必须是 财务报告 或者 备查文件目录
# 这些条件都满足后，应当最终生成一个唯一的表。
def finalize_structure_detail(section_number_type="第一节"):
    self.structure_details={}
    sections=self.possible_tocs[0][1]
    for nth_section in range(len(sections)):
        section=sections[nth_section]
        if section_number_type=="第一节":
            section_number_end=re.search('节',section).span()[1]
            section_number=section[:section_number_end]
            section_name=section[section_number_end:]

section='第一节释义'

sections

self.unfound_subsections
self.found_subsections
self.subsections_pages_found_checked
self.fin_subsections_with_abnormal_pages


    temp_strings=fin_report_subsections
    if temp_strings != None:
        temp_strings=re.sub("[ 、.\n]", "", temp_strings)
        temp_strings=re.sub("[;；，]", ",", temp_strings)
        self.fin_report_subsections=temp_strings.split(',')
    else:
        print("Error from find_fin_report_structure: parameter fin_report_subsections is not valid")
        return

import re
        for nth_section in range(len(self.possible_tocs[0][1])):
            section=self.possible_tocs[0][1][nth_section]
            if ((re.search("财务报告", section)!=None) | (re.search("财务报表", section)!=None)):
                fin_report_position=self.sections_pages_checked[nth_section][0]
                if nth_section+1<len(self.possible_tocs[0][1]):
                    fin_report_next_subsection_position=self.sections_pages_checked[nth_section+1][-1]
                break

nth_section=10

self.possible_tocs[0][1][1]
self.sections_pages[3]
self.sections_pages_checked[2][0]

import re
import itertools
sections=self.possible_tocs[0][1]
    self.sections_pages_checked=[]

    sections=self.possible_tocs[0][1]
    self.sections_pages={}
    for nth_section in range(len(sections)):
        self.sections_pages[nth_section]=[]
    for page_number in range(self.possible_tocs[0][0][0], self.total_pages):
        this_page_text=self.all_pages[page_number]['page_text']
        for nth_section in range(len(sections)):
            this_section=sections[nth_section]
            for match in re.finditer(this_section, this_page_text):
                self.sections_pages[nth_section].append((page_number, match.span()[0], match.span()[1]))
    sections_pages_list=[]
    for nth_section in range(len(sections)):
        this_item=self.sections_pages[nth_section]
        if len(this_item)==0:
            print(f"Error from find_sections_pages: Fail to find any position for nth_section={nth_section} {sections[nth_section]}")
            break
        else:
            sections_pages_list.append(this_item)

first_position=self.possible_tocs[0][0]
first_position=[[first_position]]
last_page_number=self.total_pages-1
last_char_position=self.all_pages[last_page_number]["page_text_len"]
last_position=[[(last_page_number,last_char_position-1,last_char_position)]]
list_to_check= first_position + sections_pages_list + last_position
list_to_check[0]
list_to_check[-1]


    list_products=[]
    list_checked_dict={}
    list_checked=[]
    for iter in itertools.product(*list_to_check):
        keepme=1
        for i in range(1, len(list_to_check)):
            this_item=iter[i]
            previous_item=iter[i-1]
            if ((previous_item[0]>this_item[0]) | ((previous_item[0]==this_item[0]) & (previous_item[2]>this_item[1]))):
                keepme=0
                break
        if keepme==1:
            list_products.append(iter)
    if len(list_products)>0:
        for i in range(len(list_products)):
            iter=list_products[i]
            for j in range(len(list_to_check)):
                if j not in list_checked_dict.keys():
                    list_checked_dict[j]=[iter[j]]
                else:
                    if iter[j] not in list_checked_dict[j]:
                        list_checked_dict[j].append(iter[j])
        for j in range(len(list_to_check)):
            list_checked.append(list_checked_dict[j])






self.possible_tocs[0][0]






self.all_tables_positions_checked
self.all_tables_positions

self.find_position_of_one_table(nth_of_total_tables=nth_table)
self.all_tables[nth_table]["tentative_positions"]


nth_table=253
page_number=self.all_tables[nth_table]["page_number"]
nth_table_in_page=self.all_tables[nth_table]["nth_table_in_page"]
page_text=self.all_pages[page_number]["page_text"]
page_text[9:62]

nth_of_total_tables=245
self.all_tables[nth_of_total_tables]["page_number"]
chars_total_length=self.all_tables[nth_of_total_tables]["chars_total_length"]

table_text=self.all_pages[174]["page_text"][259:361]
for n_same_chars in range(chars_total_length):
    if table_text[n_same_chars] != table_text[-n_same_chars]:
        break
if n_same_chars>0:


len(self.all_tables_positions_checked)



self.total_tables
self.all_tables[253]


first_position=[[(0,0,0)]]
last_page_number=self.total_pages-1
last_char_position=self.pages_and_tables_extracted[last_page_number]["page_text_len"]
last_position=[[(last_page_number,last_char_position-1,last_char_position)]]
list_to_check= first_position + self.all_tables_positions + last_position

type(list_to_check[0][0])

import itertools
list_products_raw=[]
len(list_products_raw)
list_products=[]
list_checked_dict={}
list_checked=[]
for iter in itertools.product(*list_to_check):
    # list_products_raw.append(iter)

    keepme=1
    for i in range(1, len(list_to_check)):
        try:
            this_item=iter[i]
            previous_item=iter[i-1]
            if ((previous_item[0]>this_item[0]) | ((previous_item[0]==this_item[0]) & (previous_item[2]>this_item[1]))):
                keepme=0
                break
        except:
            print(iter)
            print(i)
            break
    if keepme==1:
        list_products.append(iter)
len(list_products)

list_products_raw[0]

len(self.all_tables_positions_checked)
nth_of_total_tables=111
page_number=self.all_tables[nth_of_total_tables]["page_number"]
page_number=95
self.pages_and_tables_extracted[page_number]["n_tables_in_page"]
self.pages_and_tables_extracted[page_number]["n_tables_in_page"]
self.total_tables
self.all_tables[111]
