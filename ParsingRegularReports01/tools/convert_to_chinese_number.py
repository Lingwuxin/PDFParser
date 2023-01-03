
def convert_to_chinese_number(self, num):
    num_str=str(num)
    num_len=len(num_str)
    num_dict={'0': '零', '1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六', '7': '七', '8': '八', '9': '九'}
    position_dict={1: '', 2: '十', 3: '百', 4: '千'}

    if num_len>3:
        print("Error from conver_to_chinese_number: 数字超过3位了！")
        return None

    out_str=[]
    for position in range(num_len):
        position_str=position_dict[num_len-position]
        digit=num_str[position]
        digit_str=num_dict[digit]
        if digit=='0':
            if position+1<num_len:
                out_str.append(f"{digit_str}")
            else:
                pass
        elif ((digit=='1') & (position==0) & (num_len==2)):
            out_str.append('十')
        else:
            out_str.append(f"{digit_str}{position_str}")
    return ''.join(out_str)


# num=13
# num_cn=convert_to_chinese_number(num=num)
# print(num_cn)
