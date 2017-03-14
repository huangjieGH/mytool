'''Converter: 1)from roman 2 arabic
              2)from arabic 2 roman

   usage:transroman.py 123|CXXIII
   note:arabic number should in the 1~3999.
'''
import sys
import re

arabic_dict = {'kil':0, 'hun':0, 'ten':0, 'uni':0}
roman_dict  = {'kil':'N', 'hun':'N', 'ten':'N', 'uni':'N'}

ten_map = {'kil':'M', 'hun':'C', 'ten':'X', 'uni':'I'}
five_map = {'kil':'N', 'hun':'D', 'ten':'L', 'uni':'V'}
next_map = {'kil':'N', 'hun':'M', 'ten':'C', 'uni':'X'}
all_map = {'M':1000, 'D':500, 'C':100, 'L':50, 'X':10, 'V':5, 'I':1}

def transsingle(value, key):
    '''trans single arabic number to roman number.
    '''
    if value >= 4:
        if abs(5-value) <= 3:
            if 5-value >= 0:
                return ten_map[key] * (5 - value) + five_map[key]
            else:
                return five_map[key] + ten_map[key] * abs(5 - value)
        else:
            return ten_map[key] * (10 - value) + next_map[key]
    else:
        return ten_map[key] * value

def isarabic(inputvalue):
    '''match the valid arabic number.
    '''
    arabicpattern = re.compile(r'^([1-9]+\d*)$')
    return arabicpattern.search(inputvalue)

def isroman(inputvalue):
    '''match the vaalid roman number.
    '''
    romanpattern = re.compile(r'^(M{0,3})(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$')
    return romanpattern.search(inputvalue).groups() if romanpattern.search(inputvalue) else False

def arabic2roman(inputvalue):
    inputvalue = int(inputvalue)

    if inputvalue/1000 >= 1:
        arabic_dict['kil'] = inputvalue//1000
        arabic_dict['hun'] = (inputvalue%1000)//100
        arabic_dict['ten'] = ((inputvalue%1000)%100)//10
        arabic_dict['uni'] = ((inputvalue%1000)%100)%10
    else:
        if inputvalue/100 >= 1:
            arabic_dict['kil'] = 0
            arabic_dict['hun'] = inputvalue//100
            arabic_dict['ten'] = (inputvalue%100)//10
            arabic_dict['uni'] = (inputvalue%100)%10
        else:
            if inputvalue/10 >= 1:
                arabic_dict['kil'] = 0
                arabic_dict['hun'] = 0
                arabic_dict['ten'] = inputvalue//10
                arabic_dict['uni'] = inputvalue%10
            else:
                arabic_dict['kil'] = 0
                arabic_dict['hun'] = 0
                arabic_dict['ten'] = 0
                arabic_dict['uni'] = inputvalue

    if arabic_dict['kil'] == 0:
        if arabic_dict['hun'] == 0:
            if arabic_dict['ten'] == 0:
                roman_dict['uni'] = transsingle(arabic_dict['uni'], 'uni')
            else:
                roman_dict['ten'] = transsingle(arabic_dict['ten'], 'ten')
                roman_dict['uni'] = transsingle(arabic_dict['uni'], 'uni')
        else:
            roman_dict['hun'] = transsingle(arabic_dict['hun'], 'hun')
            roman_dict['ten'] = transsingle(arabic_dict['ten'], 'ten')
            roman_dict['uni'] = transsingle(arabic_dict['uni'], 'uni')
    else:
        roman_dict['kil'] = transsingle(arabic_dict['kil'], 'kil')
        roman_dict['hun'] = transsingle(arabic_dict['hun'], 'hun')
        roman_dict['ten'] = transsingle(arabic_dict['ten'], 'ten')
        roman_dict['uni'] = transsingle(arabic_dict['uni'], 'uni')
    
def roman2arabic(inputvalue):
    roman_dict['kil'] = inputvalue[0]
    roman_dict['hun'] = inputvalue[1]
    roman_dict['ten'] = inputvalue[2]
    roman_dict['uni'] = inputvalue[3]
    
    for i in roman_dict.keys():
        if roman_dict[i] == '':
            arabic_dict[i] = 0
        else:
            tmp_list = roman_dict[i]
            pos = 0
            a = tmp_list[0]
        
            for j in range(len(tmp_list)):
                if a != tmp_list[j]:
                    pos = j
        
            if pos == 0:
                arabic_dict[i] = tmp_list.count(tmp_list[0]) * all_map[tmp_list[0]]
            else:
                leftsum = 0
                rightsum = 0

                #left
                for k in range(pos):
                    leftsum += all_map[tmp_list[k]]
                #right
                for l in range(pos, len(tmp_list)):
                    rightsum += all_map[tmp_list[l]]
            
                if leftsum > rightsum:
                    arabic_dict[i] = leftsum + rightsum
                else:
                    arabic_dict[i] = rightsum - leftsum
    
def main(inputvalue):
    if isarabic(inputvalue):
        if int(inputvalue) > 3999:
            raise ValueError('The input number is too large,it should in 1~3999.')
        arabic2roman(inputvalue)
        print((roman_dict['kil'] + roman_dict['hun'] + roman_dict['ten'] + roman_dict['uni']).replace('N', ''))
    elif isroman(inputvalue):
        roman2arabic(isroman(inputvalue))
        print(arabic_dict['kil'] + arabic_dict['hun'] + arabic_dict['ten'] + arabic_dict['uni'])
    else:
        print("The input is neither arabic number nor roman number !")

if __name__ == '__main__':
    #批量转换，从文件读取，写入到文件中
    ####file_object = open('arabicnumber_list.txt')
    ###file_object = open('romannumber_list.txt')
    ###try:
    ###    lines = file_object.readlines()
    ###finally:
    ###    file_object.close()

    ###saveout = sys.stdout
    ####fsock = open('romannumber_list.txt', 'w')
    ###fsock = open('arabicnumber_list.txt', 'w')
    ###sys.stdout = fsock

    ###for i in lines:
    ###    main(i)
    ###
    ###sys.stdout = saveout
    ###fsock.close()

    inputvalue = sys.argv[1]
    main(inputvalue)
