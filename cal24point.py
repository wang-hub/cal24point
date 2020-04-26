# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 14:14:05 2020

@author: wangwei
"""
import random

def twoto24(a,b,*p,tem=[],to=24):
    '''
    用于一个括号或无括号计算的最后一步
    两个数计算能得到24输出计算过程并返回1
    因为扑克范围在1-13，均小于24
    不会出现a-b-c*d的情况（这种情况无法用递归树存储）
    *这种情况输出表达式若无括号，则从左往右计算，不按四则运算优先级
    '''
    if(a+b==to):
        tem.append('+')
        for i in range(3):
            print(p[i],tem[i],end=' ')
        print(b,'=24')
        return 1
    if(a*b==to):
        tem.append('*')
        for i in range(3):
            print(p[i],tem[i],end=' ')
        print(b,'=24')
        return 1
    if(a>b):
        if(a-b==to):
            tem.append('-')
            for i in range(3):
                print(p[i],tem[i],end=' ')
            print(b,'=24')
            return 1
        if(a==to*b):
            tem.append('/')
            for i in range(3):
                print(p[i],tem[i],end=' ')
            print(b,'=24')
            return 1
        return 0
    else:
        if(b-a==to):
            print(b,'-(',end=' ')
            for i in range(2):
                print(p[i],tem[i],end=' ')
            print(p[2],')=24')
            return 1
        if(b==a*to):
            print(b,'/(',end=' ')
            for i in range(2):
                print(p[i],tem[i],end=' ')
            print(p[2],')=24')
            return 1
        return 0
        
def fourto24(*a,now=0,deep=0,tem=[]):
    '''
    4个数分为1-3组合，即最多一个括号，可通过调换顺序解决
    例如：4*3+6+6
    a为传入的四个数
    deep为当前计算到的层数
    now为当前层初始计算数值
    这种情况第二个操作数必为输入中的，不存在为0情况，不用考虑除0
    新增tem保存计算符号
    '''
    if(deep==3):
        #最后一个数加入计算，出口层
        if(twoto24(now,a[deep],*a,tem=tem)):
            return 1;
        else:
            return 0;
    elif(deep==0):
        #第一个数为初始值
        #因为默认参数中列表传入的为地址，所以重新赋空值，以防万一
        return fourto24(*a,now=now+a[deep],deep=deep+1,tem=[])
    else:
        #1,2层计算
        #加
        _tem=list(tem);
        _tem.append('+')
        if(fourto24(*a,now=now+a[deep],deep=deep+1,tem=_tem)==1):
            return 1;
        #减
        _tem=list(tem)
        _tem.append('-')
        if(fourto24(*a,now=now-a[deep],deep=deep+1,tem=_tem)==1):
            return 1;
        #乘
        _tem=list(tem)
        _tem.append('*')
        if(fourto24(*a,now=now*a[deep],deep=deep+1,tem=_tem)==1):
            return 1;
        #除
        _tem=list(tem)
        _tem.append('/')
        if(now % a[deep]==0):   #不是分数
            if(fourto24(*a,now=now/a[deep],deep=deep+1,tem=_tem)==1):
                return 1;
        return 0;

def two_two(*a):
    '''
    4个数分为2-2组合，有两个括号
    例如：（4-1）*（2+6）
    因为外层全排列遍历所有情况，这里可以分为ab-cd组合，就概括所有
    这部分可以调用twoto24函数，因为想打印出过程，就不调用了
    注意：这里需要考虑除0操作
    '''
    if((a[0]+a[1])*(a[2]+a[3])==24):
        print('(',a[0],'+',a[1],')*(',a[2],'+',a[3],')=24')
        return 1
    if((a[0]+a[1])*(a[2]-a[3])==24):    #前+后减和前-后加是一样的
        print('(',a[0],'+',a[1],')*(',a[2],'-',a[3],')=24')
        return 1
    if((a[0]-a[1])*(a[2]-a[3])==24):
        print('(',a[0],'-',a[1],')*(',a[2],'-',a[3],')=24')
        return 1
    if((a[0]+a[1])%(a[2]+a[3])==0 and (a[0]+a[1])/(a[2]+a[3])==24):
        print('(',a[0],'+',a[1],')/(',a[2],'+',a[3],')=24')
        return 1
    if(a[2]!=a[3] and (a[0]+a[1])%(a[2]-a[3])==0 and (a[0]+a[1])/(a[2]-a[3])==24):
        print('(',a[0],'+',a[1],')/(',a[2],'-',a[3],')=24')
        return 1
    if(a[0]!=a[1] and a[2]!=a[3] and (a[0]-a[1])%(a[2]-a[3])==0 and (a[0]-a[1])/(a[2]-a[3])==24):
        print('(',a[0],'-',a[1],')/(',a[2],'-',a[3],')=24')
        return 1
    return 0

def spe_point(*a):
    '''
    处理特殊情况
    特指最后一步为整数/分数=24的情况
    例如：3 3 8 8和1 3 4 6
    经分析，分数不可能是两数相除所得，否则可通过先乘后除避免
    分数来自三个数有a*(b+-c/d)和a/(b+-c/d)两种情况
    其中a*(b+-c/d)=a*b+-a*c/d,此时成立a*c/d一定为整数
    而a/（b+-c/d)=24化简为24*b*d-a*d+-24*c=0
    这种情况经过化简也不会出现除0情况
    '''
    if((a[0]*a[2])%a[3]==0):
        if(a[0]*a[1]+a[0]*a[2]/a[3]==24):
            print(a[0],'*(',a[1],'+',a[2],'/',a[3],')=24')
            return 1
        elif(a[0]*a[1]-a[0]*a[2]/a[3]==24):
            print(a[0],'*(',a[1],'-',a[2],'/',a[3],')=24')
            return 1
    if(24*a[1]*a[3]-a[0]*a[3]+24*a[2]==0):
        print(a[0],'/(',a[1],'+',a[2],'/',a[3],')=24')
        return 1
    if(24*a[1]*a[3]-a[0]*a[3]-24*a[2]==0):
        print(a[0],'/(',a[1],'-',a[2],'/',a[3],')=24')
        return 1
    return 0
        
def is_24(*a):
    '''
    4个数全排列计算能否得到24点
    for i in range(4):
        j=(i+1)%4
        while(j!=i):
            k=(j+1)%4
            while(k!=i and k!=j):
    '''
    for i in range(4):
        for j in range(4):
            for k in range(4):
                if(i!=j and i!=k and j!=k):
                    b=(a[i],a[j],a[k],a[6-i-j-k])
                    if(fourto24(*b)==1 or two_two(*b)==1 or spe_point(*b)==1 ):
                        print(b,'can get 24 point')
                        print('you win!')
                        print()
                        print()
                        return
                #k=(k+1)%4
            #j=(j+1)%4
    print(a,'can\'t get 24 points')
    print('you lose!')
    print()
    print()
    
    '''
    每次输入四张牌，牌与牌间用空格隔开，范围为1-k，可用A代替1
    输入0自发结束游戏
    输入范围不对时结束游戏
    输入数量不对时结束游戏
    '''

while(1):  
    flag=0
    temp=[]
    print('********************************************')
    print('1:input,Better do it than wsih it done')
    print('2:random,Destiny is sometimes more reliable')
    print('0:exit,See you later')
    print('********************************************')
    game=input('Do your choose please:')
    if(game=='0'):
        print('Thanks for your playing')
        break;
    elif(game=='1'):
        a=input('please input four numbers:')
        a=list(a.split(' '))
        if(len(a)!=4):
            print('input number is wrong,over!')
            break
        for i in a:
            if(i<='9' and i>='0'):
                temp.append(int(i))
            elif(i=='10'):
                temp.append(10)
            elif(i=='J' or i=='j'):
                temp.append(11)
            elif(i=='Q' or i=='q'):
                temp.append(12)
            elif(i=='K' or i=='k'):
                temp.append(13)
            elif(i=='A' or i=='a'):
                temp.append(1)
            else:
                print('input is wrong!')
                flag=1
                break
            if(flag):
                break
    elif(game=='2'):
        a=''
        for i in range(4):
            t=random.randint(1,13)
            temp.append(t)
            if(t<11 and t>1):
                a=a+str(t)+' '
            elif(t==11):
                a=a+'J '
            elif(t==12):
                a+='Q '
            elif(t==13):
                a+='K '
            elif(t==1):
                a+='A '
    else:
        print('please choose from range')
        continue
    print('your cards are',a)
    is_24(*temp)
    


        
        