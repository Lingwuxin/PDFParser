import datetime
import re
import itertools

from .find_position_of_one_table import find_position_of_one_table
from ..tools.compare_positions_order import compare_positions_order

def find_positions_of_all_tables(self):
    self.all_tables_positions=[]
    self.all_tables_positions_checked=[]
    if_continue=1
    for nth_table in range(self.total_tables):
        self.find_position_of_one_table(nth_of_total_tables=nth_table)
        tentative_positions=self.all_tables[nth_table]["tentative_positions"]
        if tentative_positions==None:
            print(f"Finding Positions of All Tables Error: table {nth_table} of all_tables FAILS to get tentative_positions")
            if_continue=0
        if len(tentative_positions)==0:
            print(f"Finding Positions of All Tables Error: table {nth_table} of all_tables FAILS to get tentative_positions")
            if_continue=0
        if if_continue==0:
            break
        self.all_tables_positions.append(self.all_tables[nth_table]["tentative_positions"])

    if if_continue==1:
        ret_compare_positions_order=self.compare_positions_order(objects_list=self.all_tables_positions, first_position=None, last_position=None)
        if self.total_tables==len(ret_compare_positions_order):
            self.all_tables_positions_checked=ret_compare_positions_order[:]
        else:
            if_continue=0
            print(f"Error from find_positions_of_all_tables: After running compare_positions_order, the returned all_tables_positions_checked has {len(ret_compare_positions_order)} elements, whereas total_tables={self.total_tables}")



    if if_continue==1:
        print(f"Finding Positions of All Tables Succeeds at {datetime.datetime.now()}")
