import datetime
import pdfplumber
import re
import itertools

# 读入PDF文件，并存储text和tables的extracted信息
def read_in_pdf(self):
    pdf_read_in=pdfplumber.open(self.pdf_full_path)
    self.total_pages=len(pdf_read_in.pages)
    self.all_pages={}
    self.all_tables=[]
    table_count=0
    for page_number in range(self.total_pages):
        this_page=pdf_read_in.pages[page_number]
        page_text_raw=this_page.extract_text()
        page_text_clean=page_text_raw.replace("√", "checkme")
        page_text_clean=''.join(x for x in page_text_clean if x.isalnum())
        n_tables_in_page=len(this_page.find_tables())
        self.all_pages[page_number]={
            "page_text_raw": page_text_raw,
            "page_text": page_text_clean,
            "page_text_len": len(page_text_clean),
            "n_tables_in_page": n_tables_in_page,
            "tables_index_in_page": list(range(table_count, table_count+n_tables_in_page)),
            "if_found_header": False,
        }
        table_count+=n_tables_in_page
        tables_in_this_page=this_page.extract_tables()
        for nth_table_in_page in range(len(this_page.find_tables())):
            this_table=tables_in_this_page[nth_table_in_page]
            n_rows=len(this_table)
            n_columns=len(this_table[0])
            nonempty_cells_coordinates_list=[]
            for r in range(n_rows):
                for c in range(n_columns):
                    if ((this_table[r][c] != None) & (this_table[r][c] != '')):
                        nonempty_cells_coordinates_list.append((r,c))
            self.all_tables.append({
                "page_number": page_number,
                "nth_table_in_page": nth_table_in_page,
                "n_rows": n_rows,
                "n_columns": n_columns,
                "n_cells": n_rows * n_columns,
                "n_nonempty_cells": len(nonempty_cells_coordinates_list),
                "table_start_position": None,
                "table_end_position": None,
                "previous_table_end": None,
                # "tentative_starts": None,
                # "tentative_starts_refined": None,
                "chars_total_length": None,
                "tentative_positions": None,
                "positions_checked": None,
                "if_unique_position": None,
                "nonempty_cells_coordinates_list": nonempty_cells_coordinates_list[:],
                "table_content": this_table[:],
            })
    self.total_tables=len(self.all_tables)
    self.deleted_tables=[]
    self.total_deleted_tables=len(self.deleted_tables)


    print(f"Read in PDF Succeeds at {datetime.datetime.now()}")
