import re
import itertools


def find_fin_report_structure(self):
    self.fin_subsections_positions_dict={}
    self.unfound_fin_subsections=[]
    self.found_fin_subsections=[]
    self.found_fin_subsections_positions=[]
    self.fin_subsections_with_abnormal_pages=[]

    # 是个list of lists。每一个元素是个list，第二层元素依次是：在本文中是财务报告中的第几小节，本文中含小节号的名称，本文中不含小节号的名称，该小节所在的位置（位置又是个tuple），前一个小节所在的位置，后一个小节所在的位置，该小节是标准财务报告二级目录self.standard_fin_subsections的第几小节，这个小节在标准标准财务报告二级目录self.standard_fin_subsections中的名称
    self.fin_subsections_compared_std=[]

    # 找到财务报告这个section的位置
    fin_report_start=None
    fin_report_end=None
    for item in self.sections_compared_std:
        if item[7]=='财务报告':
            fin_report_start=item[3][0]
            fin_report_end=item[5][0]
            break
    if ((fin_report_start==None) | (fin_report_end==None)):
        self.need_intervention=1
        print(f"Error from find_fin_report_structure: fin_report_start or fin_report_end is None")

    # 找出标准的fin_subsection的文本：fin_report_subsection_titles。它是个list，每个元素是个tuple，tuple第0个元素是标准的小节编号，第2个元素是个list，是每一种可能的小节文本
    fin_report_subsection_titles=[]
    for key in self.standard_fin_subsections.keys():
        cn_num=self.tools_num_arabic2cn[key+1]
        titles=[]
        for item in self.standard_fin_subsections[key][1]:
            titles.append(f"{cn_num}{item}")
        fin_report_subsection_titles.append((key, titles))

    # 开始按照上面列出的标准fin_subsection文本进行查找：
    for page_number in range(fin_report_start[0], fin_report_end[0]+1):
        this_page_text=self.all_pages[page_number]["page_text"]
        if page_number==fin_report_end[0]:
            this_page_text=this_page_text[:fin_report_end[1]]

        for subsec in fin_report_subsection_titles:
            nth_subsection=subsec[0]
            subsec_titles=subsec[1]
            for subsec_title in subsec_titles:
                for match in re.finditer(subsec_title, this_page_text):
                    position=(page_number, match.span()[0], match.span()[1])
                    if (nth_subsection==0) & (position[0]==fin_report_start[0]) & (position[1]<fin_report_start[1]):
                        pass
                    else:
                        if nth_subsection not in self.fin_subsections_positions_dict.keys():
                            self.fin_subsections_positions_dict[nth_subsection]=[position]
                        else:
                            self.fin_subsections_positions_dict[nth_subsection].append(position)
    # 根据上面查找的结果，仅把未找到的列出来。
    for nth_subsection in range(len(self.fin_subsections_positions_dict)):
        if len(self.fin_subsections_positions_dict[nth_subsection])>0:
            self.found_fin_subsections.append(self.standard_fin_subsections[nth_subsection])
            self.found_fin_subsections_positions.append(self.fin_subsections_positions_dict[nth_subsection])
        else:
            self.unfound_fin_subsections.append(self.standard_fin_subsections[nth_subsection])
    # for nth_subsection in range(len(self.fin_subsections_positions_dict)):
    #     if len(self.fin_subsections_positions_dict[nth_subsection])==0:
    #         self.unfound_fin_subsections.append(self.standard_fin_subsections[nth_subsection])

    # 如果有未找到的，也许是真的没有。但是就会因为小节序号的问题，导致此后的小节都找不到，处理一下这个问题。


    # 展示一下是否有没有找到的fin_subsection
    if len(self.unfound_fin_subsections)==0:
        print(f"Success from find_fin_report_structure: All Financial Report SubSections have been found.")
    else:
        print(f"Warning from find_fin_report_structure: The following Financial Report SubSections have NOT been found.")
        print(self.unfound_fin_subsections)

    # 比对顺序，删掉那些不合理的位置
    ret_compare_positions_order=self.compare_positions_order(objects_list=self.found_fin_subsections_positions, first_position=fin_report_start, last_position=fin_report_end)


    # 是个list of lists。每一个元素是个list，第二层元素依次是：在本文中是财务报告中的第几小节，本文中含小节号的名称，本文中不含小节号的名称，该小节所在的位置（位置又是个tuple），前一个小节所在的位置，后一个小节所在的位置，该小节是标准财务报告二级目录self.standard_fin_subsections的第几小节，这个小节在标准标准财务报告二级目录self.standard_fin_subsections中的名称


    # 如果都正确，输出结果self.fin_subsections_compared_std
    if len(self.found_fin_subsections_positions)==len(ret_compare_positions_order):
        for nth_subsection in range(len(self.found_fin_subsections_positions)):
            fin_subsection_std=self.found_fin_subsections[nth_subsection]
            self.fin_subsections_compared_std.append([nth_subsection, ])
            if len(ret_compare_positions_order[nth_subsection])!=1:
                self.fin_subsections_with_abnormal_pages.append((self.found_fin_subsections[nth_subsection], ret_compare_positions_order[nth_subsection]))
        if len(self.fin_subsections_with_abnormal_pages)==0:
            print("Success from find_fin_report_structure: Find and Compare Fin SubSections Pages Succeeds, without multiple pages.")
        else:
            print(f"Warning from find_fin_report_structure: There are {len(self.fin_subsections_with_abnormal_pages)} sections that have abnormal pages.")
            print("self.fin_subsections_with_abnormal_pages is as follows:")
            print(self.fin_subsections_with_abnormal_pages)
    else:
        print(f"Warning from find_fin_report_structure: The compared positions is fewer than self.found_fin_subsections_positions")
