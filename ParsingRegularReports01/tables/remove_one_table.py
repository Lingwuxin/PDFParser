import datetime

def remove_one_table(self, nth_of_total_tables):
    page_number=self.all_tables[nth_of_total_tables]["page_number"]
    self.all_pages[page_number]["n_tables_in_page"]-=1
    self.total_tables-=1
    self.deleted_tables.append(self.all_tables[nth_of_total_tables])
    self.total_deleted_tables=len(self.deleted_tables)
    del self.all_tables[nth_of_total_tables]

    for nth_page in range(self.total_pages):
        self.all_pages[nth_page]["tables_index_in_page"]=[]
    for nth_table in range(self.total_tables):
        page_number=self.all_tables[nth_table]["page_number"]
        self.all_pages[page_number]["tables_index_in_page"].append(nth_table)




    print(f"Removing the {nth_of_total_tables}th Table Succeeds at {datetime.datetime.now()}")
