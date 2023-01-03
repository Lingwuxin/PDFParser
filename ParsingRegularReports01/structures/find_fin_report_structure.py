import re
import itertools


def find_fin_report_structure(self):
    self.fin_subsections_dict={}
    self.fin_subsections_dict_found={}
    self.fin_subsections_dict_found_refined={}
    self.fin_subsections_dict_found_refined2=[]
    self.fin_subsections_dict_found_multiple=[]


    self.fin_subsections_with_abnormal_pages=[] #它的结构与self.fin_subsections_compared_std相同
    # 最终self.fin_subsections_compared_std是一个list of tuples。每一个tuple的元素依次是：该fin_subsection是标准目录self.standard_fin_subsections的第几节，在本文财务报告中第几个小节，该fin_subsection所在的位置（位置又是个list of tuples，但这个list在多数情况下只有一个元素），前一个fin_subsection所在的位置，后一个fin_subsection所在的位置，该fin_subsection在标准目录self.standard_fin_subsections中的名字
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

    # 找出标准的fin_subsection的文本。主要问题是，也许正常的就会出现某些小节没有。但是同时也可能出现新增的小节
    # 现在先考虑把标准fin_subsection都找出来。如果本文中有新增小节（标准fin_subsection中没有），这种情况还没有考虑
    # 结果是：self.fin_subsections_dict。它是一个dict，每一个key是标准fin_subsection的key，每一个value又是一个dict，这一层dict有很多keys-values，每一对key-value分别是，key是本文中可能是第几小节，value是一个list，这个list有两个元素，第1个元素是一个list(其元素是：把这个小节char和标准fin_subsection可能的title文本合起来的文本)，第2个元素也是一个list(其元素是找到的位置，不过在这一步里它是空的)。
    possible_fin_subsection_nums=list(self.tools_num_arabic2cn.values())
    for nth_std_fin_subsec in self.standard_fin_subsections.keys():
        dict_for_this_std_fin_subsec={}
        for possible_nth in self.tools_num_arabic2cn.keys():
            dict_for_this_std_fin_subsec.update({possible_nth: [[],[]]})
            cn_num=self.tools_num_arabic2cn[possible_nth]
            for item in self.standard_fin_subsections[nth_std_fin_subsec][1]:
                dict_for_this_std_fin_subsec[possible_nth][0].append(f"{cn_num}{item}")
        self.fin_subsections_dict.update({nth_std_fin_subsec: dict_for_this_std_fin_subsec})

    # 开始按照上面列出的标准fin_subsection文本进行查找：
    #结果仍然是self.fin_subsections_dict，只不过把上一步留空的找到的位置填进去了
    for page_number in range(fin_report_start[0], fin_report_end[0]+1):
        this_page_text=self.all_pages[page_number]["page_text"]
        if page_number==fin_report_end[0]:
            this_page_text=this_page_text[:fin_report_end[1]]

        for nth_std_fin_subsec in self.fin_subsections_dict.keys():
            dict_for_this_std_fin_subsec=self.fin_subsections_dict[nth_std_fin_subsec]
            for possible_nth in dict_for_this_std_fin_subsec.keys():
                subsec_titles=dict_for_this_std_fin_subsec[possible_nth][0]
                for subsec_title in subsec_titles:
                    for match in re.finditer(subsec_title, this_page_text):
                        position=(page_number, match.span()[0], match.span()[1])
                        dict_for_this_std_fin_subsec[possible_nth][1].append(position)
            self.fin_subsections_dict.update({nth_std_fin_subsec: dict_for_this_std_fin_subsec})

    # self.fin_subsections_dict与标准fin_subsection的行数是一样的，即查找每一个标准fin_subsection。但是可能会有某些小节是没有找到的。
    # 把没找到的标准fin_subsection删掉。只是删，不考虑找的是否正确。
    #结果：self.fin_subsections_dict_found，它的结构与self.fin_subsections_dict类似，不同之处是，第二层dict虽然也有很多keys-values，但是每一个key-value的value都只是一个list，这个list是找到的位置。
    for nth_std_fin_subsec in self.fin_subsections_dict.keys():
        dict_for_this_std_fin_subsec_refined={}
        dict_for_this_std_fin_subsec=self.fin_subsections_dict[nth_std_fin_subsec]
        for possible_nth in dict_for_this_std_fin_subsec.keys():
            if dict_for_this_std_fin_subsec[possible_nth][1] != []:
                dict_for_this_std_fin_subsec_refined.update({possible_nth: dict_for_this_std_fin_subsec[possible_nth][1]})
        if dict_for_this_std_fin_subsec_refined != {}:
            self.fin_subsections_dict_found.update({nth_std_fin_subsec: dict_for_this_std_fin_subsec_refined})


    # 试着从self.fin_subsections_dict_found找一下正确的内容。逻辑是：如果一个标准subsection有多个序号，那么前后颠倒的序号应当被删掉
    # 结果：found_keys_checked。它是一个list，每一个元素是一个tuple，这个tuple依次列出了每一个找到的标准fin_subsection在文中的小节编号
    found_keys=[]
    for nth_std_fin_subsec in self.fin_subsections_dict_found.keys():
        found_keys.append(list(self.fin_subsections_dict_found[nth_std_fin_subsec].keys()))
    found_keys_checked=[]
    for iter in itertools.product(*found_keys):
        keepme=1
        for nth_item in range(1,len(iter)):
            if iter[nth_item-1]>=iter[nth_item]:
                keepme=0
                break
        if keepme==1:
            found_keys_checked.append(iter)
    # 把上一步找出的found_keys_checked做出一个self.fin_subsections_dict_found_refined。后者与self.fin_subsections_dict_found的结构一致，只不过是把上一步能够剔除的序号剔除了
    for nth_found_fin_subsec in range(len(self.fin_subsections_dict_found.keys())):
        nth_std_fin_subsec=list(self.fin_subsections_dict_found.keys())[nth_found_fin_subsec]
        positions_for_this_found_fin_subsec={}
        for nth_product in range(len(found_keys_checked)):
            possible_nth=found_keys_checked[nth_product][nth_found_fin_subsec]
            positions_for_this_found_fin_subsec.update({possible_nth: self.fin_subsections_dict_found[nth_std_fin_subsec][possible_nth]})
        self.fin_subsections_dict_found_refined.update({nth_std_fin_subsec: positions_for_this_found_fin_subsec})

    # self.fin_subsections_dict_found_refined中每个key(即nth_std_fin_subsec)是不是只有唯一的序号。把那些唯一的单列出来即self.fin_subsections_dict_found_refined2
    # self.fin_subsections_dict_found_refined2是一个list，它的结构是：每一个找到的标准fin_subsec是一行，每一行是一个tuple，其元素依次是：标准fin_subsec的序号，本文中是第几小节，找到的位置。这个list用于下一步position的比对
    # 注意这一步有可能会出现self.need_intervention=1
    positions_to_compare=[]
    for nth_std_fin_subsec in self.fin_subsections_dict_found_refined.keys():
        if len(self.fin_subsections_dict_found_refined[nth_std_fin_subsec].keys())>1:
            self.fin_subsections_dict_found_multiple.append(self.fin_subsections_dict_found_refined[nth_std_fin_subsec])
        else:
            found_subsec_number= list(self.fin_subsections_dict_found_refined[nth_std_fin_subsec].keys())[0]
            found_subsec_positions=self.fin_subsections_dict_found_refined[nth_std_fin_subsec][found_subsec_number]
            self.fin_subsections_dict_found_refined2.append((nth_std_fin_subsec, found_subsec_number, found_subsec_positions))
            positions_to_compare.append(found_subsec_positions)
    # 如果有不唯一的，列出来
    if self.fin_subsections_dict_found_multiple!=[]:
        self.need_intervention=1
        print(f"Error from find_fin_report_structure: The following {len(self.fin_subsections_dict_found_multiple)} Financial Report Subsections have Multiple Subsection Numbers.")
        for item in self.fin_subsections_dict_found_multiple:
            print(f"{item}")


    # 比对顺序，删掉那些不合理的位置
    ret_compare_positions_order=self.compare_positions_order(objects_list=positions_to_compare, first_position=fin_report_start, last_position=fin_report_end)
    # 如果都正确，输出结果self.fin_subsections_compared_std
    if len(positions_to_compare)==len(ret_compare_positions_order):
        for nth_std_fin_subsec in range(len(self.fin_subsections_dict_found_refined2)):
            this_std_subsec=self.fin_subsections_dict_found_refined2[nth_std_fin_subsec]
            this_position=ret_compare_positions_order[nth_std_fin_subsec]
            if nth_std_fin_subsec==0:
                previous_position=None
            else:
                previous_position=ret_compare_positions_order[nth_std_fin_subsec-1]
            if nth_std_fin_subsec==len(self.fin_subsections_dict_found_refined2)-1:
                next_position=[fin_report_end]
            else:
                next_position=ret_compare_positions_order[nth_std_fin_subsec+1]
            tuple_to_append=(this_std_subsec[0], this_std_subsec[1], this_position, previous_position, next_position, self.standard_fin_subsections[this_std_subsec[0]][0])
            self.fin_subsections_compared_std.append(tuple_to_append)
            if len(ret_compare_positions_order[nth_std_fin_subsec])!=1:
                self.fin_subsections_with_abnormal_pages.append(tuple_to_append)
        if len(self.fin_subsections_with_abnormal_pages)==0:
            print("Success from find_fin_report_structure: Find and Compare Fin SubSections Pages Succeeds, without multiple pages.")
        else:
            print(f"Warning from find_fin_report_structure: There are {len(self.fin_subsections_with_abnormal_pages)} sections that have abnormal pages.")
            print("self.fin_subsections_with_abnormal_pages is as follows:")
            print(self.fin_subsections_with_abnormal_pages)
    else:
        print(f"Warning from find_fin_report_structure: The compared positions is fewer than self.fin_subsections_dict_found_refined2")
