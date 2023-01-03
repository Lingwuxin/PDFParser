


# sys.path.append("/home/cuixin02/Coding/Python/Codes/cx_modules/")
# from HbSqlJobs008 import SqlJobs

from ParsingRegularReports01 import Parser

self=Parser(
    comp_info="南新制药2021年报",
    pdf_full_path="8180733.PDF"
)
self.read_in_pdf()

self.find_header()


self.find_toc()
# self.possible_tocs

self.find_sections_pages()
# self.section_titles

self.compare_standard_toc()






self.find_fin_report_structure()
# self.fin_subsections_compared_std[3][5]



self.find_positions_of_all_tables()
#   self.all_pages[61]["page_text"]
# self.all_tables[139]
self.remove_one_table(139)
self.find_positions_of_all_tables()

self.remove_one_table(160)
self.find_positions_of_all_tables()


# self.table_keywords放在init中，是个dict。key是我给出的表名，value是个tuple，其元素依次为：报告中的关键词（list），上级章节（字符串，一级标题为无）,所属章节（字符串）,是否有适用（字符串）
self.table_keywords={
    "公司基本情况": (["公司基本情况"], "无", "公司简介和主要财务指标", "否", ),
    "公司股票简况": (["公司股票简况"], "无", "公司简介和主要财务指标", "是", ),
    "公司存托凭证简况": (["公司存托凭证简况"], "无", "公司简介和主要财务指标", "是", ),
    "会计师事务所、持续督导券商": (["其他相关资料"], "无", "公司简介和主要财务指标", "否", ),
    "主要会计数据": (["主要会计数据"], "无", "公司简介和主要财务指标", "否", ),
    "主要财务指标": (["主要财务指标"], "无", "公司简介和主要财务指标", "否", ),
    "母公司现金流量表": (["母公司现金流量表"], "财务报告", "财务报表", "否", ),
    "附注-货币资金": (["货币资金"], "财务报告", "合并财务报表项目注释", "是", ),
    "附注-交易性金融资产": (["交易性金融资产"], "财务报告", "合并财务报表项目注释", "是", ),
    "附注-衍生金融资产": (["衍生金融资产"], "财务报告", "合并财务报表项目注释", "是", ),
}



import re
import itertools

# self.parsed_tables是个dict。key是我给出的表名，value是个list，其元素依次为：所属的section或subsection的起止page（自己、前一个、后一个），找到了几个possible_positions_refined1，找到的具体的possible_positions_refined1
self.parsed_tables={}
for table_name in self.table_keywords:
    table_to_find=self.table_keywords[table_name]
    # 找所属的section或subsection的起止page
    section_subsection_page_range=None
    if table_to_find[1]=="无":
        in_this_section=table_to_find[2]
        for section_info in self.sections_compared_std:
            if in_this_section==section_info[2]:
                section_subsection_page_range=(section_info[3], section_info[4], section_info[5])
                break
    elif table_to_find[1]=="财务报告":
            in_this_fin_subsection=table_to_find[2]
            for section_info in self.fin_subsections_compared_std:
                if in_this_fin_subsection==section_info[5]:
                    section_subsection_page_range=(section_info[2],section_info[3],section_info[4],)
                    break
    if section_subsection_page_range==None:
        print(f"Error from find_parsed_tables: This table fails to find the section or subsection page range.")
        print(table_to_find)
        break

    #搜索文本
    possible_positions=[]
    for keyword in table_to_find[0]:
        for page_number in range(self.total_pages):
            if (page_number<section_subsection_page_range[0][0][0]) | (page_number>section_subsection_page_range[2][0][0]):
                continue
            this_page=self.all_pages[page_number]
            for match in re.finditer(keyword, this_page["page_text"]):
                position=(page_number, match.span()[0], match.span()[1])
                # 如果这个位置在所属章节之前，就不要这个位置
                if page_number==section_subsection_page_range[0][0][0]:
                    if match.span()[0]<=section_subsection_page_range[0][0][2]:
                        continue
                # 如果这个位置在所属章节之后，就不要这个位置
                if page_number==section_subsection_page_range[2][0][0]:
                    if match.span()[0]>section_subsection_page_range[2][0][1]:
                        continue
                # 如果这个位置是在表里，就不要这个位置
                for nth_table in this_page["tables_index_in_page"]:
                    this_table=self.all_tables[nth_table]
                possible_positions.append(position)

    #对possible_positions进一步检验
    possible_positions_refined1=possible_positions[:]
    possible_positions_refined2=[]

    for position in possible_positions:
        page_number=position[0]
        this_page=self.all_pages[page_number]
        # 如果这个表是有适用的
        if table_to_find[3]=='是':
            text_to_check=self.all_pages[page_number]["page_text"][position[2]:position[2]+12]
            if text_to_check=='checkme适用不适用':
                there_is_a_table=0
                for nth_table in this_page["tables_index_in_page"]:
                    this_table=self.all_tables[nth_table]
                    for table_position in this_table["positions_checked"]:
                        if ((table_position[0]==page_number) & (table_position[1]>=position[2]+12)):
                            possible_positions_refined2.append((position, nth_table, table_position))
                            there_is_a_table=1
                            break
                    if there_is_a_table==1:
                        break
            elif text_to_check=='适用checkme不适用':
                possible_positions_refined2.append((position, "不适用", None))
                break
            else:
                possible_positions_refined1.remove(position)
        # 如果这个表是没有适用的
        else:
            there_is_a_table=0
            for nth_table in this_page["tables_index_in_page"]:
                this_table=self.all_tables[nth_table]
                for table_position in this_table["positions_checked"]:
                    if ((table_position[0]==page_number) & (table_position[1]>=position[2]) & (table_position[1]<=position[2]+30)):
                        possible_positions_refined2.append((position, nth_table, table_position))
                        there_is_a_table=1
                        break
                if there_is_a_table==1:
                    break

    # 如果possible_positions_refined2有多个元素，进行如下筛选
    if len(possible_positions_refined2)>1:
        possible_table_indxes=list(set(x[1] for x in possible_positions_refined2))
        if len(possible_table_indxes)==1:
            possible_positions_refined3=possible_positions_refined2[0:1]
        else:
            possible_positions_refined3=[]
            for nth_table in possible_table_indxes:
                temp_list_for_possible_positions_refined3=list(x for x in possible_positions_refined2 if x[1]==nth_table)
                possible_positions_refined3.append(temp_list_for_possible_positions_refined3[0])

    else:
        possible_positions_refined3=possible_positions_refined2[:]

    # 把信息填入self.parsed_tables
    self.parsed_tables.update({table_name: [section_subsection_page_range, len(possible_positions_refined3), possible_positions_refined3]})
    # self.parsed_tables.update({table_name: [section_subsection_page_range, len(possible_positions), possible_positions]})

self.parsed_tables["主要会计数据"][2]

# self.all_pages[127]

self.parsed_tables

# 这些章节是否都找到了



sections_used=[]
fin_subsections_used=[]
for table_name in self.table_keywords:
    table_to_find=self.table_keywords[table_name]
    if table_to_find[1]=="无":
        sections_used.append(table_to_find[2])
    else:
        sections_used.append(table_to_find[1])
        fin_subsections_used.append(table_to_find[2])
sections_used=list(set(sections_used))
fin_subsections_used=list(set(fin_subsections_used))
