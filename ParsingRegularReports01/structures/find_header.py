


def find_header(self):
    self.header_len=None
    self.document_header=None
    self.page_numbers_with_abnormal_header=[]

    tentative_document_header=self.all_pages[0]["page_text"][:300]
    page_text_1=self.all_pages[1]["page_text"]
    for header_len in range(300):
        if page_text_1[header_len] != tentative_document_header[header_len]:
            break
    if header_len>0:
        self.header_len=header_len
        self.document_header=tentative_document_header[:self.header_len]
        # 看一下是否有些页里没有title
        for page_number in range(self.total_pages):
            if self.all_pages[page_number]["page_text"][:self.header_len]==self.document_header:
                self.all_pages[page_number]["if_found_header"]=True
            else:
                self.all_pages[page_number]["if_found_header"]=False
                self.page_numbers_with_abnormal_header.append(page_number)

        print(f"Message from find_header: 页眉：{self.document_header}，长度：{self.header_len}")
        if len(self.page_numbers_with_abnormal_header)>0:
            self.need_intervention=1
            print(f"The following {len(self.page_numbers_with_abnormal_header)} pages have abnormal header:")
            print(self.page_numbers_with_abnormal_header)
        else:
            print(f"Success from find_header: All pages have the header.")
    else:
        self.need_intervention=1
        print("Warning from find_header: No header is found.")
