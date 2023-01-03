import re
import itertools

# objects_list这个参数，应当是一个list，而且是已经按照业务逻辑排好序的list。这个list中的每一个元素，也应该是一个list，这一层的每一个元素应该是一个位置的tuple，这个tuple的三个元素依次是: page_number, span()[0], span()[1]
def compare_positions_order(self, objects_list, first_position=None, last_position=None):
    if first_position==None:
        first_position=[[(0,0,0)]]
    else:
        first_position=[[first_position]]
    if last_position==None:
        last_page_number=self.total_pages-1
        last_char_position=self.all_pages[last_page_number]["page_text_len"]
        last_position=[[(last_page_number,last_char_position-1,last_char_position)]]
    else:
        last_position=[[last_position]]
    list_to_check= first_position + objects_list + last_position

    list_products=[]
    list_checked_dict={}
    list_checked=[]
    for iter in itertools.product(*list_to_check):
        keepme=1
        for i in range(1, len(list_to_check)):
            this_item=iter[i]
            previous_item=iter[i-1]
            if ((previous_item[0]>this_item[0]) | ((previous_item[0]==this_item[0]) & (previous_item[2]>this_item[1]))):
                keepme=0
                break
        if keepme==1:
            list_products.append(iter)
    if len(list_products)>0:
        for i in range(len(list_products)):
            iter=list_products[i]
            for j in range(len(list_to_check)):
                if j not in list_checked_dict.keys():
                    list_checked_dict[j]=[iter[j]]
                else:
                    if iter[j] not in list_checked_dict[j]:
                        list_checked_dict[j].append(iter[j])
        for j in range(len(list_to_check)):
            list_checked.append(list_checked_dict[j])


# 返回的是什么？是个list，每一个元素又是一个list，这一层list的每一个元素是潜在正确的位置。
# 返回的list是一个与objects_list同样结构的list，只不过把objects_list中那些肯定不正确的元素删除了。
    return list_checked[1:-1]
