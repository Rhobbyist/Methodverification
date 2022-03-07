import numpy as np

# 小数点后两位
def new_round(num,n=2):
    # 1 判断num是否为整数(1 是整数，直接用'{:.2f}'.format(num);2 是小数，进入第2步)
    # 2 查找小数点后第2位是原始数字的第几位(如果小数点后没有两位，则直接用'{:.2f}'.format(num))
    # 3 判断小数点后第3位开始是否有字符(1 没有，返回原字符串；2 有，进入第4步)
    # 4 判断小数点后第3位是哪个数字(1 <=4或>=6，直接用'{:.2f}'.format(num);2 是5，进入第5步)
    # 5 判断小数点后第4位开始是否有字符(1 没有;2 有且全是0；3 有且不全为0)
        # 1和2，判断小数点第2位是奇数还是偶数
        # 3 
    num=str(num)
    if n==2:
        if "." not in num:
            return '{:.2f}'.format(float(num))
        else:     
            index1=num.find(".") #小数点所处索引
            # 判断小数点后是否有两位，没有则直接调用'{:.2f}'.format(num))
            if len(num)<=index1+2:
                return '{:.2f}'.format(float(num))
            else:
                index2=index1+2 #小数点后第2位所处索引
                if (index2+1)==len(num):
                    return num
                else:
                    if int(num[index2+1])<=4 or int(num[index2+1])>=6:
                        return '{:.2f}'.format(float(num))
                    else:
                        if (index2+2)==len(num): #小数点后第4位开始没有字符
                            if (int(num[index2])%2)==0: #偶数，不进位，把小数点后第三位的5变成4，再调用'{:.2f}'.format(num)
                                num2=num[:-1]+"4"
                                return '{:.2f}'.format(float(num2))
                            else: #奇数，进一位，，把小数点后第三位的5变成6，再调用'{:.2f}'.format(num)
                                num2=num[:-1]+"6"
                                return '{:.2f}'.format(float(num2)) 
                        else:
                            return '{:.2f}'.format(float(num))
    
    elif n==3:
        if "." not in num:
            return '{:.3f}'.format(float(num))
        else:     
            index1=num.find(".") #小数点所处索引
            
            if len(num)<=index1+3:
                return '{:.3f}'.format(float(num))
            else:
                index2=index1+3 
                if (index2+1)==len(num):
                    return num
                else: 
                    if int(num[index2+1])<=4 or int(num[index2+1])>=6:
                        return '{:.3f}'.format(float(num))
                    else:
                        if (index2+2)==len(num): 
                            if (int(num[index2])%2)==0: #偶数，不进位，把小数点后第三位的5变成4，再调用'{:.3f}'.format(num)
                                num2=num[:-1]+"4"
                                return '{:.3f}'.format(float(num2))
                            else: #奇数，进一位，，把小数点后第三位的5变成6，再调用'{:.3f}'.format(num)
                                num2=num[:-1]+"6"
                                return '{:.3f}'.format(float(num2)) 
                        else:  #小数点后第4位开始有字符，直接进位
                            return '{:.3f}'.format(float(num))

    elif n==1:
        if "." not in num:
            return '{:.1f}'.format(float(num))
        else:     
            index1=num.find(".") #小数点所处索引
            
            # 判断小数点后是否有一位，没有则直接调用'{:.1f}'.format(num))
            if len(num)<=index1+1:
                return '{:.1f}'.format(float(num))
            else:
                index2=index1+1 #小数点后第3位所处索引
                if (index2+1)==len(num):  #如果小数点后恰好有3位，则返回原始数据
                    return num
                else: 
                    if int(num[index2+1])<=4 or int(num[index2+1])>=6:
                        return '{:.1f}'.format(float(num))
                    else:
                        if (index2+2)==len(num):
                            if (int(num[index2])%2)==0: #偶数，不进位，把小数点后第三位的5变成4，再调用'{:.3f}'.format(num)
                                num2=num[:-1]+"4"
                                return '{:.1f}'.format(float(num2))
                            else: #奇数，进一位，，把小数点后第三位的5变成6，再调用'{:.3f}'.format(num)
                                num2=num[:-1]+"6"
                                return '{:.1f}'.format(float(num2)) 
                        else:  #小数点后第4位开始有字符，直接进位
                            return '{:.1f}'.format(float(num))

# 小数点后两位结果转浮点数
def float_newround(num):
    return float(new_round(num))

# 有效位数
def effectnum(num,n):
    if isinstance(num, str):
        num=float(num)
        if num>=1:
            if "." in f'%.{n}g' % num:
                if "e" not in f'%.{n}g' % num:
                    if len(f'%.{n}g' % num)==n+1:
                        return f'%.{n}g' % num
                    else:
                        a=f'%.{n}g' % num
                        for i in range(n+1-len(f'%.{n}g' % num)):
                            a=a+"0"
                        return a
                else:
                    x = str(f'%.{n}g' % num).split("e")
                    if len(x[0])==n+1:
                        return x[0]+"e"+x[1] 
                    else:
                        for i in range(n+1-len(x[0])):
                            x[0]=x[0]+"0"
                        return x[0]+"e"+x[1]     

            else:
                if "e" not in f'%.{n}g' % num:
                    if len(f'%.{n}g' % num)==n:
                        return f'%.{n}g' % num
                    else:
                        b=f'%.{n}g' % num
                        for i in range(n-len(f'%.{n}g' % num)):
                            if i == 0:
                                b=b+"."
                            b = b+"0"
                        return b

                else:
                    x = str(f'%.{n}g' % num).split("e")
                    if len(x[0])==n:
                        return x[0]+"e"+x[1] 
                    else:
                        for i in range(n-len(x[0])):
                            if i == 0:
                                x[0]=x[0]+"."
                            x[0] = x[0]+"0"
                        return x[0]+"e"+x[1]  
        elif num<=-1:
            if "." in f'%.{n}g' % num:
                if "e" not in f'%.{n}g' % num:
                    if len(f'%.{n}g' % num)==n+2:
                        return f'%.{n}g' % num
                    else:
                        a=f'%.{n}g' % num
                        for i in range(n+2-len(f'%.{n}g' % num)):
                            a=a+"0"
                        return a
                else:
                    x = str(f'%.{n}g' % num).split("e")
                    if len(x[0])==n+2:
                        return x[0]+"e"+x[1] 
                    else:
                        for i in range(n+2-len(x[0])):
                            x[0]=x[0]+"0"
                        return x[0]+"e"+x[1]     

            else:
                if "e" not in f'%.{n}g' % num:
                    if len(f'%.{n}g' % num)==n+1:
                        return f'%.{n}g' % num
                    else:
                        b=f'%.{n}g' % num
                        for i in range(n+1-len(f'%.{n}g' % num)):
                            if i == 0:
                                b=b+"."
                            b = b+"0"
                        return b

                else:
                    x = str(f'%.{n}g' % num).split("e")
                    if len(x[0])==n:
                        return x[0]+"e"+x[1] 
                    else:
                        for i in range(n+1-len(x[0])):
                            if i == 0:
                                x[0]=x[0]+"."
                            x[0] = x[0]+"0"
                        return x[0]+"e"+x[1]

        elif num>0 and num<1:          
            strs=f'%.{n}g' % num
            count_0=0
            for i in range(2,len(strs)):  #从2开始是因为"0."的长度为2
                if strs[i]=="0":
                    count_0+=1
                else:
                    break
            if len(strs)==n+2+count_0: 
                return f'%.{n}g' % num
            else:
                for i in range(n+2+count_0-len(f'%.{n}g' % num)):
                    strs=strs+"0"
                return strs  

        elif num>-1 and num<0:          
            strs=f'%.{n}g' % num
            count_0=0
            for i in range(3,len(strs)):  #从3开始是因为"-0."的长度为2
                if strs[i]=="0":
                    count_0+=1
                else:
                    break
            if len(strs)==n+3+count_0: 
                return f'%.{n}g' % num
            else:
                for i in range(n+3+count_0-len(f'%.{n}g' % num)):
                    strs=strs+"0"
                return strs        
        
        else:
            return "0"

    else:
        if num>=1:
            if "." in f'%.{n}g' % num:
                if "e" not in f'%.{n}g' % num:
                    if len(f'%.{n}g' % num)==n+1:
                        return f'%.{n}g' % num
                    else:
                        a=f'%.{n}g' % num
                        for i in range(n+1-len(f'%.{n}g' % num)):
                            a=a+"0"
                        return a
                else:
                    x = str(f'%.{n}g' % num).split("e")
                    if len(x[0])==n+1:
                        return x[0]+"e"+x[1] 
                    else:
                        for i in range(n+1-len(x[0])):
                            x[0]=x[0]+"0"
                        return x[0]+"e"+x[1]     

            else:
                if "e" not in f'%.{n}g' % num:
                    if len(f'%.{n}g' % num)==n:
                        return f'%.{n}g' % num
                    else:
                        b=f'%.{n}g' % num
                        for i in range(n-len(f'%.{n}g' % num)):
                            if i == 0:
                                b=b+"."
                            b = b+"0"
                        return b

                else:
                    x = str(f'%.{n}g' % num).split("e")
                    if len(x[0])==n:
                        return x[0]+"e"+x[1] 
                    else:
                        for i in range(n-len(x[0])):
                            if i == 0:
                                x[0]=x[0]+"."
                            x[0] = x[0]+"0"
                        return x[0]+"e"+x[1]  
        elif num<=-1:
            if "." in f'%.{n}g' % num:
                if "e" not in f'%.{n}g' % num:
                    if len(f'%.{n}g' % num)==n+2:
                        return f'%.{n}g' % num
                    else:
                        a=f'%.{n}g' % num
                        for i in range(n+2-len(f'%.{n}g' % num)):
                            a=a+"0"
                        return a
                else:
                    x = str(f'%.{n}g' % num).split("e")
                    if len(x[0])==n+2:
                        return x[0]+"e"+x[1] 
                    else:
                        for i in range(n+2-len(x[0])):
                            x[0]=x[0]+"0"
                        return x[0]+"e"+x[1]     

            else:
                if "e" not in f'%.{n}g' % num:
                    if len(f'%.{n}g' % num)==n+1:
                        return f'%.{n}g' % num
                    else:
                        b=f'%.{n}g' % num
                        for i in range(n+1-len(f'%.{n}g' % num)):
                            if i == 0:
                                b=b+"."
                            b = b+"0"
                        return b

                else:
                    x = str(f'%.{n}g' % num).split("e")
                    if len(x[0])==n:
                        return x[0]+"e"+x[1] 
                    else:
                        for i in range(n+1-len(x[0])):
                            if i == 0:
                                x[0]=x[0]+"."
                            x[0] = x[0]+"0"
                        return x[0]+"e"+x[1]

        elif num>0 and num<1:
            strs=f'%.{n}g' % num
            count_0=0
            for i in range(2,len(strs)):  #从2开始是因为"0."的长度为2
                if strs[i]=="0":
                    count_0+=1
                else:
                    break
            if len(strs)==n+2+count_0: 
                return f'%.{n}g' % num
            else:
                for i in range(n+2+count_0-len(f'%.{n}g' % num)):
                    strs=strs+"0"
                return strs    

        elif num>-1 and num<0:          
            strs=f'%.{n}g' % num
            count_0=0
            for i in range(3,len(strs)):  #从3开始是因为"-0."的长度为2
                if strs[i]=="0":
                    count_0+=1
                else:
                    break
            if len(strs)==n+3+count_0: 
                return f'%.{n}g' % num
            else:
                for i in range(n+3+count_0-len(f'%.{n}g' % num)):
                    strs=strs+"0"
                return strs     

        else:
            return "0"

# 有效位数结果转浮点数
def floateffectnum(num,n):
    if "." not in effectnum(num,n):
        return int(effectnum(num,n))
    else:
        return float(effectnum(num,n))


def Reverse(lst):
    return [ele for ele in reversed(lst)]

# 均值
def mean(lst):
    meanresult = np.mean(lst)

    return new_round(meanresult)

# sd
def sd(lst):
    sdresult = np.std(lst, ddof=1)

    return new_round(sdresult)

# cv
def cv(lst):
    meanresult = np.mean(lst)
    sdresult = np.std(lst,ddof=1)
    cvresult = sdresult/meanresult*100

    return new_round(cvresult)


data=[None]

if not any(data):
    print("not any data")