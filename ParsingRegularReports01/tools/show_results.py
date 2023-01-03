def show_results(self, show_type="help"):
    if show_type in ["help", "H", "h", "HELP", "Help"]:
        print("show_type 取值：")
        # print("  unmatched tables: 没有找到起始位置的table")
        print("  multi_position_tables: 有多个position的table")
        print("  pages_without_header: 没有页眉，或者页眉不正常的页面")
    # elif show_type in ["unmatched tables"]:
    #     n_wrong=0
    #     for page_number in self.pages_and_tables_extracted.keys():
    #         this_page=self.pages_and_tables_extracted[page_number]
    #         if this_page["n_tables"]>0:
    #             for nth_table in range(this_page["n_tables"]):
    #                 this_table_details=this_page["table_details"][nth_table]
    #                 table_start_position=this_table_details["table_start_position"]
    #                 table_end_position=this_table_details["table_end_position"]
    #                 previous_table_end=this_table_details["previous_table_end"]
    #                 if ((table_start_position!=None) & (table_end_position!=None)):
    #                     if previous_table_end != None:
    #                         if previous_table_end>table_start_position:
    #                             n_wrong+=1
    #                             print(f"\n{n_wrong} (previous_end>start): \npage_number={page_number}\nnth_table={nth_table}\nprevious,start,end={previous_table_end},{table_start_position},{table_end_position}")
    #                 else:
    #                     n_wrong+=1
    #                     print(f"\n{n_wrong} (nones):\npage_number={page_number}\nnth_table={nth_table}\nprevious,start,end={previous_table_end},{table_start_position},{table_end_position}")
    #
    #     print(f"***Total number of unmatched tables: {n_wrong}.***")

    elif show_type in ["multi_position_tables"]:
        multi_position_tables=[]
        for nth_table in range(self.total_tables):
            positions=self.all_tables_positions_checked[nth_table]
            if len(positions)>1:
                multi_position_tables.append(nth_table)
        if len(multi_position_tables)==0:
            print("Success: There are no tables with multiple positions.")
        else:
            print(f"Warning: The following {len(multi_position_tables)} tables have multiple positions:")
            for i in range(len(multi_position_tables)):
                nth_table=multi_position_tables[i]
                positions=self.all_tables_positions_checked[nth_table]
                print(f"\nnth_table={nth_table}:")
                print(positions)

    elif show_type in ["pages_without_header"]:
        print(f"页眉：{self.document_header}，长度：{self.header_len}")
        if len(self.page_numbers_with_abnormal_header)>0:
            print(f"The following {len(self.page_numbers_with_abnormal_header)} pages have abnormal header:")
            print(self.page_numbers_with_abnormal_header)
        else:
            print(f"All pages have the header.")
