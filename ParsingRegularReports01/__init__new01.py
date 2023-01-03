import datetime

dict0={'释义':1, '公司简介和主要财务指标':2, '公司业务概要':3, '经营情况讨论与分析':4, '重要事项':5, '股份变动及股东情况':6, '优先股相关情况':7, '董事监事高级管理人员和员工情况':8, '公司治理':9, '公司债券相关情况':10, '财务报告':11, '备查文件目录':12}
for key in dict0.keys():
    print(dict0[key])

dict0["新1"]=13
dict0.values()
dict0.update({"新2": 14})
del dict0["新2"]

class Parser(object):
    def __init__(self, comp_info, pdf_full_path, report_type):
        self.comp_info=comp_info
        self.pdf_full_path=pdf_full_path

        if report_type=="年报1型":
            self.file_meta={
                "sections": ('释义', '公司简介和主要财务指标', '公司业务概要', '经营情况讨论与分析', '重要事项', '股份变动及股东情况', '优先股相关情况', '董事监事高级管理人员和员工情况', '公司治理', '公司债券相关情况', '财务报告', '备查文件目录'),
                "section_number_format": {"第": True, "节": True, "ChineseNumber": True},
            }

        self.sections_details=None
        self.fin_subsections_details=None

def generate_sections_details(self, ):
sections_numbered_names=[]
for nth_section in range(len(self.file_meta["sections"])):
    section_numbered_name=[]
    if self.file_meta["section_number_format"]["第"]==True:
        section_numbered_name.append('第')
    if self.file_meta["section_number_format"]["ChineseNumber"]==True:
        cn_num=self.convert_to_chinese_number(num=nth_section)
        section_numbered_name.append(cn_num)
    if self.file_meta["section_number_format"]["节"]==True:
        section_numbered_name.append('节')
    section_numbered_name.append(self.file_meta["sections"][nth_section])
    sections_numbered_names.append(''.join(section_numbered_name))




第一节释义	0	释义
第二节公司简介和主要财务指标	1	公司简介和主要财务指标

for i in range(-3,0):
    print(f"{-i}")


a=23
int(23/10)
str(a)
        print(f"Parser Object Creation Succeeds at {datetime.datetime.now()}")

    from .read_in_pdf import read_in_pdf

    from .tables.find_position_of_one_table import find_position_of_one_table
    from .tables.find_positions_of_all_tables import find_positions_of_all_tables
    from .tables.remove_one_table import remove_one_table
    from .tables.update_tables_positions_checked import update_tables_positions_checked

    from .structures.find_header import find_header
    from .structures.find_toc import find_toc
    from .structures.find_sections_pages import find_sections_pages
    from .structures.find_fin_report_structure import find_fin_report_structure

    from .tools.compare_positions_order import compare_positions_order
    from .tools.convert_to_chinese_number import convert_to_chinese_number
    # from .tools.show_results import show_results
