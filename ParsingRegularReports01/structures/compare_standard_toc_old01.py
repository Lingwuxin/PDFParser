

def compare_standard_toc(self):
    # 建立self.sections_compared_std，在self.section_titles的基础上，每个tuple增加两个元素，增加的第1个元素是该section是标准section的第几节，如果没找到，这个元素是None；增加的第2个元素是这个section在标准section中的名称，即self.standard_sections中的对应行的第1个元素
    # 最终self.sections_compared_std每一行的元素依次是：本文第几节，本文中含节号的名称，本文中不含节号的名称，该section所在的位置（位置又是个list of tuples，但这个list在多数情况下只有一个元素），前一个section所在的位置，后一个section所在的位置，该section是标准目录self.standard_sections的第几节，这个section在标准目录self.standard_sections中的名称
    self.sections_compared_std=[]
    self.sections_not_on_std_list=[]
    self.unfound_std_sections=[]

    # 检查每个section对应标准section的第几节
    # 建立self.sections_compared_std，在self.section_titles的基础上，每个tuple增加两个元素，增加的第1个元素是该section是标准section的第几节，如果没找到，这个元素是None；增加的第2个元素是这个section在标准section中的名称，即self.standard_sections中的对应行的第1个元素
    for section in self.section_titles:
        section_checked=list(section)
        std_number=None
        for std_section in self.standard_sections:
            if section[2] in std_section[2]:
                std_number=std_section[0]
                std_name=std_section[1]
                break
        section_checked.append(std_number)
        section_checked.append(std_name)
        self.sections_compared_std.append(tuple(section_checked))

    # 检查section的顺序是否有错乱，如果有会停止？
    # 还检查sectionv是否有新的，即不在标准section列表的，如果有，把这个self.sections_compared_std中的元素放到self.sections_not_on_std_list这个列表中
    for nth_section in range(1, len(self.sections_compared_std)):
        this_std_num=self.sections_compared_std[nth_section][3]
        previous_std_num=self.sections_compared_std[nth_section-1][3]
        if (previous_std_num != None) & (this_std_num != None):
            if previous_std_num>=this_std_num:
                self.need_intervention=1
                print(f"Error from compare_standard_toc: the {nth_section}-th section has an order number that is wrong.")
                break
        else:
            if this_std_num == None:
                self.sections_not_on_std_list.append(self.sections_compared_std[nth_section])

    if len(self.sections_not_on_std_list)>0:
        self.need_intervention=1
        print(f"Error from compare_standard_toc: the following sections are not on the list of standard sections.")
        print(self.sections_not_on_std_list)
    else:
        print("Success from compare_standard_toc: All sections are on the list of standard sections.")

    # 注意：并不强求与标准section的顺序是一致的。
    # 检查标准section列表中的section是否不在本文中，如果有，把self.standard_sections中的这个元素放到self.unfound_std_sections中
    for std_section in self.standard_sections:
        if_unfound=1
        for this_item in  self.sections_compared_std:
            section=this_item[2]
            if section in std_section[2]:
                if_unfound=0
        if if_unfound==1:
            self.unfound_std_sections.append(std_section)
    if len(self.unfound_std_sections)>0:
        print(f"Warning from compare_standard_toc: the following standard sections are not found in this PDF file:")
        print(f"{self.unfound_std_sections}")
    else:
        print("Success from compare_standard_toc: All standard sections are found in this file")
