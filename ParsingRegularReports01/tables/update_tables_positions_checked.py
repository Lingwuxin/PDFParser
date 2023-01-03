import datetime

def update_tables_positions_checked(self):
    for nth_table in range(self.total_tables):
        positions_checked=self.all_tables_positions_checked[nth_table]
        self.all_tables[nth_table]["positions_checked"]=positions_checked
        if len(self.all_tables_positions_checked[nth_table])==1:
            self.all_tables[nth_table]["if_unique_position"]=True
        elif len(self.all_tables_positions_checked[nth_table])>1:
            self.all_tables[nth_table]["if_unique_position"]=False

    print(f"Updating Table positions_checked Success at {datetime.datetime.now()}")
