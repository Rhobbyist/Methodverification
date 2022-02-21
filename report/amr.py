from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from report import models
from report.models import *
import xlrd
import numpy as np
import math
from report.effectnum import *
import csv
from docx import Document
from datetime import datetime
import re

def AMRfileread(files,reportinfo,project,platform,manufacturers,Unit,digits,ZP_Method_precursor_ion,ZP_Method_product_ion,normAB,Number_of_compounds):

    # 第一步:后台数据抓取（回收率上下限，最大允许CV）
    id1 = Special.objects.get(project=project).id  
    id2 = AMRspecial.objects.get(special_id=id1).id

    # 优先查找特殊参数设置里是否有数据，如有就调用，没有则调用通用性参数设置里的数据
    if AMRspecialmethod.objects.filter(aMRspecial=id2): 
        lowvalue=AMRspecialmethod.objects.get(aMRspecial=id2).lowvalue #回收率下限
        upvalue=AMRspecialmethod.objects.get(aMRspecial=id2).upvalue #回收率上限
        cv=AMRspecialmethod.objects.get(aMRspecial=id2).cv #最大允许CV
        
    else:
        general = General.objects.get(name="通用性项目")
        amrgeneral = AMRgeneral.objects.get(general=general)
        lowvalue=AMRgeneralmethod.objects.get(aMRgeneral=amrgeneral).lowvalue #回收率下限
        upvalue=AMRgeneralmethod.objects.get(aMRgeneral=amrgeneral).upvalue #回收率上限
        cv=AMRgeneralmethod.objects.get(aMRgeneral=amrgeneral).cv #最大允许CV

    #  第二步:开始文件读取
    '''
    注释1:csv,txt,xlsx,docx 4种格式数据读取完毕后,需要生成一个字典AMR_dict,数据格式如下：
    print(AMR_dict):
    {"化合物1":{'S1':['S1理论浓度','S1检测值1','S1检测值2',...'S1回收率1','S1回收率2',...,]},
    {'S2':['S2理论浓度','S2检测值1','S2检测值2',...'S2回收率1','S2回收率2',...,]},
    "化合物2":{'S1':['S1理论浓度','S1检测值1','S1检测值2',...'S1回收率1','S1回收率2',...,]},
    {'S2':['S2理论浓度','S2检测值1','S2检测值2',...'S2回收率1','S2回收率2',...,]}
    '''

    #  1 定义最终需要的列表和字典
    AMR_dict={} #最终需要生成的字典
    Accuracyjudge=[] #每个化合物超过回收率范围的个数列表
    CVjudge=[] #每个化合物超过CV范围的个数列表
    S=["S1","S2","S3","S4","S5","S6","S7","S8","S9","S10","S11","S12","S13","S14","S15"] # 预定义浓度序号列表
    objfile=[] #图片文件列表
    picturenum=0

    error="" #收集错误信息

    #  2 开始文件读取
    for file in files:
        if '.png' in file.name or ".JPG" in file.name:    
            picturenum+=1
        if platform=="液质":
            if manufacturers =="Agilent": 
                if '.png' not in file.name and ".JPG" not in file.name:            
                    # 1 读取csv文件（Agilent）
                    csv_file = file.seek(0)  # https://www.jianshu.com/p/0d15ed85df2b
                    file_data = file.read().decode('utf-8')
                    lines = file_data.split('\r\n')
                    for i in range(len(lines)): 
                        if len(lines[i])!=0:
                            lines[i]=re.split(r',\s*(?![^"]*\"\,)', lines[i])  # 以逗号分隔字符串,但忽略双引号内的逗号
                            # lines[i]=lines[i].split(',') # 按逗号分隔后把每一行都变成一个列表
                        else:
                            lines[i]=re.split(r',\s*(?![^"]*\"\,)', lines[i])
                            del lines[i] #最后一行如为空行，则删除该元素

                    # 从第一行确定化合物名称(含有"-Q Results"),并添加进入化合物列表
                    norm=[] #化合物列表
                    for j in range(len(lines[0])):  #从第一行开始
                        if "-Q Results" in lines[0][j]:
                            if lines[0][j].split("-Q")[0][0]!='"':  # 若原始字符串中含有','，切割完后首位会多出一个'"',需去除  
                                norm.append(lines[0][j].split("-Q")[0])
                            else:
                                norm.append(lines[0][j].split("-Q")[0][1:])
                   
                    # 从第二行确定实验号（Sample Name）,理论浓度（Exp. Conc.）,实际浓度（Calc. Conc.）和回收率（Accuracy）的索引
                    nameindex=0  #实验号索引
                    theoryconindex=[]   #理论浓度索引列表（可能不止一个化合物，因此需要把索引放在一个列表里，下同）
                    calconindex=[]  #实际浓度索引列表
                    accuracyindex=[]    #回收率索引列表
                    for j in range(len(lines[1])):  #从第二行开始      
                        if lines[1][j] == "Sample Name" :
                            nameindex=j
                        elif lines[1][j]  == "Exp. Conc." :
                            theoryconindex.append(j)
                        elif lines[1][j]  == "Final Conc." :
                            calconindex.append(j)
                        elif lines[1][j]  == "Accuracy" :
                            accuracyindex.append(j)
                
                    # 确认原始数据中与AMR相关(实验号前含有"AMR-")的sample name名，即曲线点个数，放进一个列表(目前只能用于个各化合物曲线点个数一致的情况)
                    AMR_STD=[] 
                    for j in range(len(lines)):
                        if "AMR-" in lines[j][nameindex] and lines[j][nameindex] not in AMR_STD:
                            AMR_STD.append(lines[j][nameindex])
                
                    # AMR_STD_distict=[] 
                    # for i in AMR_STD:
                    #     if i not in AMR_STD_distict: # AMR_STD列表去重
                    #         AMR_STD_distict.append(i)
                    
                    # print(AMR_STD_distict) : ['AMR-STD-1', 'AMR-STD-2', 'AMR-STD-3', 'AMR-STD-4', 'AMR-STD-5',...]

                    #  从原始数据表格中抓取数据
                    for k in range(len(norm)): # 循环化合物列表
                        group_AMR={} #每个化合物数据字典
                        for j in range(len(AMR_STD)): 
                            calconc=[]  # 每个化合物内各曲线点（S1,S2,S3...）的数据列表列表：['S1检测值1','S1检测值2',...] 
                            theoryconc=[] # 每个化合物内各曲线点的理论值列表,会有重复                    
                            Accuracy=[] # 回收率列表
                                        
                            for i in range(len(lines)): # 循环原始数据中的每一行
                                if lines[i][nameindex] == AMR_STD[j]: # 如果实验号命名方式匹配上，则在相应列表中添加相应数据  
                                    calconc.append(effectnum(lines[i][calconindex[k]],digits)) #添加实际浓度              
                                    theoryconc.append(effectnum(lines[i][theoryconindex[k]],digits)) # 添加理论浓度
                                    Accuracy.append(new_round(lines[i][accuracyindex[k]],1)) #添加回收率

                            # # 第一个化合物的第一个曲线点列表calconc循环完成，放入group_AMR中，开始循环该化合物的下一个曲线点
                            group_AMR[AMR_STD[j]]=[]
                            group_AMR[AMR_STD[j]].append(theoryconc[0]) #理论浓度列表有重复，只添加第一个值
                            for i in calconc:
                                group_AMR[AMR_STD[j]].append(i)
                            for i in Accuracy:
                                group_AMR[AMR_STD[j]].append(i)

                        AMR_dict[norm[k]]=group_AMR # 第一个化合物的数据列表group_AMR循环完成，放入最终字典AMR_dict中，开始循环下一个化合物        
                    print(AMR_dict)
                
                else:
                    objfile.append(file)
                    if AMRpicture.objects.filter(reportinfo = reportinfo,img = "img/"+file.name):
                        pass
                    else:
                        AMRpicture.objects.create(reportinfo = reportinfo,img = file,name="")

                    objs_verify = AMRpicture.objects.filter(reportinfo = reportinfo)
                    id=[]
                    for item in objs_verify:
                        id.append(item.reportinfo_id)

            elif manufacturers =="Waters":
                if '.png' not in file.name and ".JPG" not in file.name:           
                    data = xlrd.open_workbook(filename=None, file_contents=file.read())  # 读取表格
                    file_data = data.sheets()[0]
                    nrows=file_data.nrows
                    ncols=file_data.ncols

                    norm=[] #化合物列表
                    norm_row=[] #化合物所在行
                    for j in range(nrows):
                        for i in PTnorm:
                            if i in str(file_data.row_values(j)[0]):
                                norm.append(i)
                                norm_row.append(j)

                    nameindex=0  #实验号索引
                    conindex=0  #实际浓度索引
                    theoryconindex=0   #理论浓度索引
                    accuracyindex=0   #回收率索引
                    for i in range(len(file_data.row_values(norm_row[0]+2))):  #第一个化合物表格确定samplename和浓度所在列，norm_row[0]为第一个化合物所在行，+2是该化合物表格位于该化合物所在行的下两行
                        if file_data.row_values(norm_row[0]+2)[i]=="Name":
                            nameindex=i
                        elif "实际浓度" in file_data.row_values(norm_row[0]+2)[i]:
                            conindex=i
                        elif "理论浓度" in file_data.row_values(norm_row[0]+2)[i]:
                            theoryconindex=i
                        elif "回收率" in file_data.row_values(norm_row[0]+2)[i]:
                            accuracyindex=i

                    for k in range(len(norm)):
                        AMR_STD=[]
                        AMR_STD_distict=[] 
                        if k<len(norm)-1: #如果不是最后一个化合物，索引为该化合物所在行到后一个化合物所在行
                            for i in range(norm_row[k],norm_row[k+1]): 
                                if "AMR-" in file_data.row_values(i)[nameindex]:
                                    AMR_STD.append(file_data.row_values(i)[nameindex])
                                            
                            for i in AMR_STD:
                                if i not in AMR_STD_distict: # AMR_STD列表去重
                                    AMR_STD_distict.append(i)

                            group_AMR={} #每个化合物数据字典
                            for j in range(len(AMR_STD_distict)): 
                                calconc=[]  # 每个化合物内各曲线点（S1,S2,S3...）的数据列表列表：['S1检测值1','S1检测值2',...] 
                                theoryconc=[]                 
                                Accuracy=[] 
                                            
                                for i in range(norm_row[k],norm_row[k+1]): 
                                    if file_data.row_values(i)[nameindex] == AMR_STD_distict[j]: # 如果实验号命名方式匹配上，则在相应列表中添加相应数据  
                                        calconc.append(effectnum(file_data.row_values(i)[conindex],digits)) #添加实际浓度              
                                        theoryconc.append(effectnum(file_data.row_values(i)[theoryconindex],digits)) # 添加理论浓度
                                        Accuracy.append(new_round(file_data.row_values(i)[accuracyindex],1)) #添加回收率

                                # # 第一个化合物的第一个曲线点列表calconc循环完成，放入group_AMR中，开始循环该化合物的下一个曲线点
                                group_AMR[AMR_STD_distict[j]]=[]
                                group_AMR[AMR_STD_distict[j]].append(theoryconc[0]) #理论浓度列表有重复，只添加第一个值
                                for i in calconc:
                                    group_AMR[AMR_STD_distict[j]].append(i)
                                for i in Accuracy:
                                    group_AMR[AMR_STD_distict[j]].append(i)

                            AMR_dict[norm[k]]=group_AMR # 第一个化合物的数据列表group_AMR循环完成，放入最终字典AMR_dict中，开始循环下一个化合物        
                        
                        else:
                            for i in range(norm_row[k],nrows):  
                                if "AMR-" in file_data.row_values(i)[nameindex]:
                                    AMR_STD.append(file_data.row_values(i)[nameindex])
                                            
                            for i in AMR_STD:
                                if i not in AMR_STD_distict: # AMR_STD列表去重
                                    AMR_STD_distict.append(i)

                            group_AMR={} #每个化合物数据字典
                            for j in range(len(AMR_STD_distict)): 
                                calconc=[]  # 每个化合物内各曲线点（S1,S2,S3...）的数据列表列表：['S1检测值1','S1检测值2',...] 
                                theoryconc=[]                 
                                Accuracy=[] 
                                            
                                for i in range(norm_row[k],nrows): 
                                    if file_data.row_values(i)[nameindex] == AMR_STD_distict[j]: # 如果实验号命名方式匹配上，则在相应列表中添加相应数据  
                                        calconc.append(effectnum(file_data.row_values(i)[conindex],digits)) #添加实际浓度              
                                        theoryconc.append(effectnum(file_data.row_values(i)[theoryconindex],digits)) # 添加理论浓度
                                        Accuracy.append(new_round(file_data.row_values(i)[accuracyindex],1)) #添加回收率

                                # # 第一个化合物的第一个曲线点列表calconc循环完成，放入group_AMR中，开始循环该化合物的下一个曲线点
                                group_AMR[AMR_STD_distict[j]]=[]
                                group_AMR[AMR_STD_distict[j]].append(theoryconc[0]) #理论浓度列表有重复，只添加第一个值
                                for i in calconc:
                                    group_AMR[AMR_STD_distict[j]].append(i)
                                for i in Accuracy:
                                    group_AMR[AMR_STD_distict[j]].append(i)

                            AMR_dict[norm[k]]=group_AMR # 第一个化合物的数据列表group_AMR循环完成，放入最终字典AMR_dict中，开始循环下一个化合物

                else:
                    if AMRpicture.objects.filter(reportinfo = reportinfo,img = "img/"+file.name):
                        pass
                    else:
                        AMRpicture.objects.create(reportinfo = reportinfo,img = file,name="")

                    objs_verify = AMRpicture.objects.filter(reportinfo = reportinfo)
                    id=[]
                    for item in objs_verify:
                        id.append(item.reportinfo_id)

            elif manufacturers =="Thermo":
                if '.png' not in file.name and ".JPG" not in file.name: 
                    Thermo = Special.objects.get(project=project) 
                    pt_special = PTspecial.objects.get(special=Thermo)
                    pt_accept = PTspecialaccept.objects.filter(pTspecial=pt_special)
                    PTnorm=[] # 待测物质列表
                    for i in pt_accept:
                        PTnorm.append(i.norm)

                    data = xlrd.open_workbook(filename=None, file_contents=file.read())  # 读取表格
                    norm=[] #Thermo的原始数据格式为一个化合物一个sheet,获取每个sheet的名字,与PTnorm相等的即为需要的sheet
                    sheetindex=[] #需要的化合物所在sheet索引列表
                    for index in range(len(data.sheet_names())):
                        if data.sheet_names()[index] in PTnorm:
                            norm.append(data.sheet_names()[index])
                            sheetindex.append(index)

                    # 循环读取每个sheet工作表,即为每个化合物的表
                    for index in range(len(sheetindex)):
                        file_data = data.sheets()[sheetindex[index]]
                        nrows=file_data.nrows
                        ncols=file_data.ncols

                        nameindex=0  #实验号索引
                        conindex=0  #实际浓度索引
                        theoryconindex=0   #理论浓度索引
                        accuracyindex=0   #回收率索引
                        for i in range(len(file_data.row_values(0))):  
                            if file_data.row_values(0)[i]=="Compound":
                                nameindex=i
                            elif file_data.row_values(0)[i]=="Calculated Amt":
                                conindex=i
                            elif file_data.row_values(0)[i]=="Theoretical Amt":
                                theoryconindex=i
                            elif file_data.row_values(0)[i]=="回收率换算":
                                accuracyindex=i

                        AMR_STD=[]
                        AMR_STD_distict=[] 
                        for i in range(nrows): 
                            if "AMR-" in file_data.row_values(i)[nameindex]:
                                AMR_STD.append(file_data.row_values(i)[nameindex])
                                        
                        for i in AMR_STD:
                            if i not in AMR_STD_distict: # AMR_STD列表去重
                                AMR_STD_distict.append(i)

                        group_AMR={} #每个化合物数据字典
                        for j in range(len(AMR_STD_distict)): 
                            calconc=[]  # 每个化合物内各曲线点（S1,S2,S3...）的数据列表列表：['S1检测值1','S1检测值2',...] 
                            theoryconc=[]                 
                            Accuracy=[] 
                                        
                            for i in range(nrows): 
                                if file_data.row_values(i)[nameindex] == AMR_STD_distict[j]: # 如果实验号命名方式匹配上，则在相应列表中添加相应数据  
                                    calconc.append(effectnum(file_data.row_values(i)[conindex],digits)) #添加实际浓度              
                                    theoryconc.append(effectnum(file_data.row_values(i)[theoryconindex],digits)) # 添加理论浓度

                                    accuracyconvert = float(file_data.row_values(i)[accuracyindex])+100 # Thermo数据需对回收率进行换算
                                    Accuracy.append(new_round(accuracyconvert,1)) #添加回收率

                            # # 第一个化合物的第一个曲线点列表calconc循环完成，放入group_AMR中，开始循环该化合物的下一个曲线点
                            group_AMR[AMR_STD_distict[j]]=[]
                            group_AMR[AMR_STD_distict[j]].append(theoryconc[0]) #理论浓度列表有重复，只添加第一个值
                            for i in calconc:
                                group_AMR[AMR_STD_distict[j]].append(i)
                            for i in Accuracy:
                                group_AMR[AMR_STD_distict[j]].append(i)

                        AMR_dict[norm[index]]=group_AMR # 第一个化合物的数据列表group_AMR循环完成，放入最终字典AMR_dict中，开始循环下一个化合物

                else:
                    if AMRpicture.objects.filter(reportinfo = reportinfo,img = "img/"+file.name):
                        pass
                    else:
                        AMRpicture.objects.create(reportinfo = reportinfo,img = file,name="")

                    objs_verify = AMRpicture.objects.filter(reportinfo = reportinfo)
                    id=[]
                    for item in objs_verify:
                        id.append(item.reportinfo_id)

            elif manufacturers =="岛津":
                if '.png' not in file.name and ".JPG" not in file.name: 
                    content= []
                    for line in file:
                        content.append(line.decode("GB2312").replace("\r\n", "").split("\t"))

                    nameindex=0
                    norm=[] #化合物列表
                    norm_row=[] #化合物所在行
                    theoryconindex=0  #理论浓度索引，岛津的数据格式决定每个化合物的浓度所在列一定是同一列，下同
                    calconindex=0 #实际浓度索引
                    accuracyindex=0    #回收率索引
                    
                    for i in range(len(content[2])):  #第二行确定samplename和浓度所在列
                        if content[2][i]=="数据文件名":
                            nameindex=i 
                        elif content[2][i]=="浓度":
                            calconindex=i 
                        elif content[2][i]=="理论浓度":
                            theoryconindex=i 
                        elif content[2][i]=="回收率":
                            accuracyindex=i 

                    for i in range(len(content)): 
                        if content[i][0]=="Name": #如果某一行第一列为"Name"，则该行第二列为化合物名称
                            norm.append(content[i][1])
                            norm_row.append(i)

                    # 确定曲线点数，实验号前含有"AMR-"(以第一个化合物为准确定曲线点数)
                    AMR_STD=[] 
                    if len(norm)==1: #如果只有一个化合物      
                        for i in range(norm_row[0],len(content)):                    
                            if "AMR-" in content[i][nameindex]: 
                                AMR_STD.append(content[i][nameindex])
                    else:
                        for i in range(norm_row[0],norm_row[1]):                    
                            if "AMR-" in content[i][nameindex]: 
                                AMR_STD.append(content[i][nameindex])
                
                    AMR_STD_distict=[] 
                    for i in AMR_STD:
                        if i not in AMR_STD_distict: # AMR_STD列表去重
                            AMR_STD_distict.append(i)
            
                    # print(AMR_STD_distict) : ['AMR-STD-1', 'AMR-STD-2', 'AMR-STD-3', 'AMR-STD-4', 'AMR-STD-5',...]

                    for k in range(len(norm)): # 循环化合物列表
                        group_AMR={} # 每个化合物数据字典
                        for j in range(len(AMR_STD_distict)): 
                            calconc=[]  # 每个化合物内各曲线点（S1,S2,S3...）的数据列表列表：['S1检测值1','S1检测值2',...] 
                            theoryconc=[] # 每个化合物内各曲线点的理论值列表,会有重复                    
                            Accuracy=[] # 回收率列表

                            if k<len(norm)-1: #如果不是最后一个化合物，索引为该化合物所在行到后一个化合物所在行              
                                for i in range(norm_row[k],norm_row[k+1]):
                                    if content[i][nameindex] == AMR_STD_distict[j]: # 如果实验号命名方式匹配上，则在相应列表中添加相应数据 
                                        calconc.append(effectnum(content[i][calconindex],digits)) #添加检测值                        
                                        theoryconc.append(effectnum(content[i][theoryconindex],digits)) # 添加理论值
                                        Accuracy.append(new_round(content[i][accuracyindex],1)) #添加回收率
                            else:
                                for i in range(norm_row[k],len(content)): 
                                    if content[i][nameindex] == AMR_STD_distict[j]: # 如果实验号命名方式匹配上，则在相应列表中添加相应数据 
                                        calconc.append(effectnum(content[i][calconindex],digits)) #添加检测值                        
                                        theoryconc.append(effectnum(content[i][theoryconindex],digits)) # 添加理论值
                                        Accuracy.append(new_round(content[i][accuracyindex],1)) #添加回收率

                            group_AMR[AMR_STD_distict[j]]=[]
                            group_AMR[AMR_STD_distict[j]].append(theoryconc[0]) #理论浓度列表有重复，只添加第一个值
                            for i in calconc:
                                group_AMR[AMR_STD_distict[j]].append(i)
                            for i in Accuracy:
                                group_AMR[AMR_STD_distict[j]].append(i)

                        AMR_dict[norm[k]]=group_AMR # 第一个化合物的数据列表group_AMR循环完成，放入最终字典AMR_dict中，开始循环下一个化合物        

                else:
                    if AMRpicture.objects.filter(reportinfo = reportinfo,img = "img/"+file.name):
                        pass
                    else:
                        AMRpicture.objects.create(reportinfo = reportinfo,img = file,name="")

                    objs_verify = AMRpicture.objects.filter(reportinfo = reportinfo)
                    id=[]
                    for item in objs_verify:
                        id.append(item.reportinfo_id)

            elif manufacturers =="AB":           
                # 错误1：未在后台管理系统里准确设置离子对数值!
                if len(normAB)!=Number_of_compounds:
                    error="未在后台管理系统里准确设置离子对数值!"  
                    return {"error":error}

                if '.png' not in file.name and ".JPG" not in file.name: 
                    norm=normAB
                    file_data = Document(file)
                    paragraphs=[] #段落列表，需依此及母离子和子离子列表判断table索引

                    # 将待测物质添加进入norm列表中
                    for p in file_data.paragraphs: 
                        if len(p.text)!=0 and p.text!="\n" and len(p.text.strip())!=0:
                            paragraphs.append(p.text.strip())

                    # 确定table索引
                    tableindex=[]
                    for i in range(len(paragraphs)):
                        for j in range(len(ZP_Method_precursor_ion)):
                            if ZP_Method_precursor_ion[j] in paragraphs[i] and ZP_Method_product_ion[j] in paragraphs[i]:
                                tableindex.append(2*i+1)

                    tables = file_data.tables #获取文件中的表格集
                    
                    for k in range(len(tableindex)): 
                        tableAMR = tables[tableindex[k]] #获取文件中的相关表格
                        nameindex=0  #实验号索引
                        theoryconindex=0   #理论浓度索引列表（可能不止一个化合物，因此需要把索引放在一个列表里，下同）
                        calconindex=0  #实际浓度索引列表
                        accuracyindex=0    #回收率索引列表

                        # 先把表格里的所有数据取出来放进一个列表中，读取速度会比直接读表格快很多
                        cells=tableAMR._cells
                        ROWS=len(tableAMR.rows)
                        COLUMNS=len(tableAMR.columns)
                        data=[] #每一行的数据
                        datas=[] #大列表，包含每一行的数据
                        for i in range(ROWS*COLUMNS):
                            text=cells[i].text.replace("\n","")
                            text=text.strip() #去除空白符
                            if i % 12 != 0 or i == 0:  #docx文件固定为12列
                                data.append(text)
                            else:
                                datas.append(data)
                                data=[]
                                data.append(text)
                        datas.append(data)

                        # 读取表格的第一行的单元格,判断实验号和浓度索引
                        for i in range(len(datas[0])):
                            if datas[0][i] == "Sample Name" :
                                nameindex=i
                            elif "Target" in datas[0][i]:
                                theoryconindex=i
                            elif "Calculated Conc" in datas[0][i]:
                                calconindex=i
                            elif "Accuracy" in datas[0][i]:
                                accuracyindex=i
            
                        # 错误2：未准确设置表头列名!
                        if theoryconindex==0 or calconindex==0 or accuracyindex==0:
                            error="未准确设置表头列名!"
                            return {"error":error}

                        # 确认原始数据中与AMR相关(实验号前含有"AMR-")的sample name名，放进一个列表
                        AMR_STD=[] 
                        for i in range(len(datas)): 
                            if "AMR-" in datas[i][nameindex] and datas[i][nameindex] not in AMR_STD and "0" not in datas[i][nameindex]:
                                AMR_STD.append(datas[i][nameindex])

                        # #  从原始数据表格中抓取数据(耗时较久,需优化)
                        # for k in range(len(norm)): # 循环化合物列表
                        group_AMR={} # 每个化合物数据字典
                        for j in range(len(AMR_STD)): 
                            calconc=[]  # 实际浓度列表
                            theoryconc=[] # 理论浓度列表
                            Accuracy=[] # 回收率列表

                            for i in range(len(datas)): # 循环原始数据中的每一行       
                                if datas[i][nameindex] == AMR_STD[j]: # 如果实验号命名方式匹配上，则在相应列表中添加相应数据  
                                    calconc.append(effectnum(datas[i][calconindex],digits)) #添加检测值           
                                    theoryconc.append(effectnum(datas[i][theoryconindex],digits)) # 添加理论值
                                    Accuracy.append(new_round(datas[i][accuracyindex],1)) #添加回收率

                            group_AMR[AMR_STD[j]]=[]
                            group_AMR[AMR_STD[j]].append(theoryconc[0]) #理论浓度列表有重复，只添加第一个值
                            for i in calconc:
                                group_AMR[AMR_STD[j]].append(i)
                            for i in Accuracy:
                                group_AMR[AMR_STD[j]].append(i)

                        AMR_dict[norm[k]]=group_AMR # 第一个化合物的数据列表group_AMR循环完成，放入最终字典AMR_dict中，开始循环下一个化合物

                else:
                    if AMRpicture.objects.filter(reportinfo = reportinfo,img = "img/"+file.name):
                        pass
                    else:
                        AMRpicture.objects.create(reportinfo = reportinfo,img = file,name="")

                    objs_verify = AMRpicture.objects.filter(reportinfo = reportinfo)
                    id=[]
                    for item in objs_verify:
                        id.append(item.reportinfo_id)
        
        elif platform=="液相":
            if manufacturers =="Agilent": 
                if '.png' not in file.name and ".JPG" not in file.name:            
                    data = xlrd.open_workbook(filename=None, file_contents=file.read())  # 读取表格
                    file_data = data.sheets()[0]
                    nrows=file_data.nrows
                    ncols=file_data.ncols

                    norm=[] #化合物列表
                    norm_row=[] #化合物所在行
                    for j in range(nrows):
                        if file_data.row_values(j)[0] == "化合物:" :  #如果某一行的第一个元素为“化合物”，则添加第三个元素进入化合物列表
                            norm.append(file_data.row_values(j)[2])
                            norm_row.append(j)

                    nameindex=0
                    conindex=0
                    for i in range(len(file_data.row_values(norm_row[0]+2))):  #第一个化合物表格确定samplename和浓度所在列，norm_row[0]为第一个化合物所在行，+2是该化合物表格位于该化合物所在行的下两行
                        if file_data.row_values(norm_row[0]+2)[i]=="样品名称":
                            nameindex=i
                        elif "含量" in file_data.row_values(norm_row[0]+2)[i]:
                            conindex=i

                    for k in range(len(norm)):
                        AMR_STD=[]
                        AMR_STD_distict=[] 
                        if k<len(norm)-1: #如果不是最后一个化合物，索引为该化合物所在行到后一个化合物所在行
                            for i in range(norm_row[k],norm_row[k+1]): 
                                if "AMR-" in file_data.row_values(i)[nameindex]:
                                    AMR_STD.append(file_data.row_values(i)[nameindex])
                                            
                            for i in AMR_STD:
                                if i not in AMR_STD_distict: # AMR_STD列表去重
                                    AMR_STD_distict.append(i)

                            group_AMR={} #每个化合物数据字典
                            for j in range(len(AMR_STD_distict)): 
                                calconc=[]  # 每个化合物内各曲线点（S1,S2,S3...）的数据列表列表：['S1检测值1','S1检测值2',...] 
                                # theoryconc=[] # 液相平台没有理论浓度                    
                                # Accuracy=[] # 液相平台没有回收率
                                            
                                for i in range(norm_row[k],norm_row[k+1]): 
                                    if file_data.row_values(i)[nameindex] == AMR_STD_distict[j]: # 如果实验号命名方式匹配上，则在相应列表中添加相应数据  
                                        calconc.append(effectnum(file_data.row_values(i)[conindex],digits)) #添加实际浓度              

                                group_AMR[AMR_STD_distict[j]]=[]
                                for i in calconc:
                                    group_AMR[AMR_STD_distict[j]].append(i)

                            AMR_dict[norm[k]]=group_AMR # 第一个化合物的数据列表group_AMR循环完成，放入最终字典AMR_dict中，开始循环下一个化合物        
                        
                        else:
                            for i in range(norm_row[k],nrows):  
                                if "AMR-" in file_data.row_values(i)[nameindex]:
                                    AMR_STD.append(file_data.row_values(i)[nameindex])
                                            
                            for i in AMR_STD:
                                if i not in AMR_STD_distict: # AMR_STD列表去重
                                    AMR_STD_distict.append(i)

                            group_AMR={} #每个化合物数据字典
                            for j in range(len(AMR_STD_distict)): 
                                calconc=[]  # 每个化合物内各曲线点（S1,S2,S3...）的数据列表列表：['S1检测值1','S1检测值2',...] 
                                  
                                for i in range(norm_row[k],nrows):  
                                    if file_data.row_values(i)[nameindex] == AMR_STD_distict[j]: # 如果实验号命名方式匹配上，则在相应列表中添加相应数据  
                                        calconc.append(effectnum(file_data.row_values(i)[conindex],digits)) #添加实际浓度              

                                group_AMR[AMR_STD_distict[j]]=[]
                                for i in calconc:
                                    group_AMR[AMR_STD_distict[j]].append(i)

                            AMR_dict[norm[k]]=group_AMR # 第一个化合物的数据列表group_AMR循环完成，放入最终字典AMR_dict中，开始循环下一个化合物

                    print(AMR_dict)

                else:
                    objfile.append(file)
                    if AMRpicture.objects.filter(reportinfo = reportinfo,img = "img/"+file.name):
                        pass
                    else:
                        AMRpicture.objects.create(reportinfo = reportinfo,img = file,name="")

                    objs_verify = AMRpicture.objects.filter(reportinfo = reportinfo)
                    id=[]
                    for item in objs_verify:
                        id.append(item.reportinfo_id)
                        
                    # for index,i in enumerate(objs_verify):
                    #     AMRpicture.objects.filter(img=i.img).delete() #删除对应对应报告的图片

    if platform=="液质":
        print(AMR_dict)
        ########文件读取完毕#######
        #  第三步:文件读取完毕后的操作(添加平均回收率和检测值CV)

        '''
        注释2:最终需要生成一个字典AMR_dict,数据格式如下：
        print(AMR_dict):
        {"化合物1":{'S1':['S1理论浓度','S1检测值1','S1检测值2',...'S1回收率1','S1回收率2',...,'平均回收率','检测值CV']},
        {'S2':['S2理论浓度','S2检测值1','S2检测值2',...'S2回收率1','S2回收率2',...,'平均回收率','检测值CV']},
        "化合物2":{'S1':['S1理论浓度','S1检测值1','S1检测值2',...'S1回收率1','S1回收率2',...,'平均回收率','检测值CV']},
        {'S2':['S2理论浓度','S2检测值1','S2检测值2',...'S2回收率1','S2回收率2',...,'平均回收率','检测值CV']}
        ''' 
        for key,value in AMR_dict.items():
            for r in value.keys():   
                sumcalconc=[] ##检测值列表，方便计算检测值CV(固定六个点)
                sumcalconc.append(float(value[r][1]))
                sumcalconc.append(float(value[r][2]))
                sumcalconc.append(float(value[r][3]))
                sumcalconc.append(float(value[r][4]))
                sumcalconc.append(float(value[r][5]))
                sumcalconc.append(float(value[r][6])) 
                cvcalconc=new_round(np.std(sumcalconc,ddof=1)/np.mean(sumcalconc)*100,1) #检测值CV

                sumrecycle=float(value[r][7])+float(value[r][8])+float(value[r][9])+float(value[r][10])+float(value[r][11])+float(value[r][12])   #回收率总和，方便计算平均回收率
                meanrecycle=new_round(sumrecycle/6,1) #平均回收率

                value[r].append(meanrecycle) #添加平均回收率
                value[r].append(cvcalconc) #添加检测值CV

        #  第四步:数据存入数据库

        # judgenum(回收率及检测值CV超过范围的个数,此数字为0才将数据存入数据库)
        judgenum=0 #每个化合物超过CV范围的个数
        print(lowvalue)
        for key,value in AMR_dict.items():     
            for i in value.values():
                for j in range(7,15): #7-13为回收率及平均回收率,14为检测值CV
                    if j>=7 and j<14:
                        if float(i[j])<lowvalue or float(i[j])>upvalue: # 如回收率不通过，添加不通过提示
                            i[j]=str(i[j])+" (不通过!)"
                            judgenum+=1
                    else:
                        if float(i[j])>cv: 
                            i[j]=str(i[j])+" (不通过!)"
                            judgenum+=1

        # 判断judgenum是否为0，为0才能将数据存入数据库              
        if judgenum==0:
            insert_list =[]
            for key,value in AMR_dict.items():
                for r,c in value.items():
                    insert_list.append(AMR(reportinfo=reportinfo,Experimentnum=r,norm=key,therory_conc=c[0],test_conc1=c[1],test_conc2=c[2],
                    test_conc3=c[3],test_conc4=c[4],test_conc5=c[5],test_conc6=c[6],recycle1=c[7],recycle2=c[8],recycle3=c[9],recycle4=c[10],
                    recycle5=c[11],recycle6=c[12],meanrecycle=c[13],cvtest_conc=c[14]))

            AMR.objects.bulk_create(insert_list)

        else: 
            insert_list =[]
            for key,value in AMR_dict.items():
                for r,c in value.items():
                    insert_list.append(AMR(reportinfo=reportinfo,Experimentnum=r,norm=key,therory_conc=c[0],test_conc1=c[1],test_conc2=c[2],
                    test_conc3=c[3],test_conc4=c[4],test_conc5=c[5],test_conc6=c[6],recycle1=c[7],recycle2=c[8],recycle3=c[9],recycle4=c[10],
                    recycle5=c[11],recycle6=c[12],meanrecycle=c[13],cvtest_conc=c[14]))

            AMR.objects.bulk_create(insert_list)

        if picturenum==0:
            return {"AMR_dict":AMR_dict,"Unit":Unit,"judgenum":judgenum,"picturenum":picturenum}      
        else:  
            return {"AMR_dict":AMR_dict,"objs_verify":objs_verify,"id":id[0],"Unit":Unit,"judgenum":judgenum,"picturenum":picturenum}

    elif platform=="液相":
        print(objfile)
        # for index,i in enumerate(objs_verify):
        #     AMRpicture.objects.filter(img=i.img).delete() #删除对应对应报告的图片
        if picturenum==0:
            return {"AMR_dict":AMR_dict,"Unit":Unit,"picturenum":picturenum,"lowvalue":lowvalue,"upvalue":upvalue,"cv":cv}
        else:
            return {"AMR_dict":AMR_dict,"objs_verify":objs_verify,"id":id[0],"Unit":Unit,"objfile":objfile,"picturenum":picturenum,"lowvalue":lowvalue,"upvalue":upvalue,"cv":cv}

## 适用于ICP-MS平台，AMR可能需要上传多个文件的情况
def AMRmutiplefileread(files, reportinfo,project,platform,manufacturers,Unit,digits,ZP_Method_precursor_ion,ZP_Method_product_ion):
    # 第一步:后台数据抓取（最小样本数，最大允许CV,化合物个数）
    norm_num = Special.objects.get(project=project).Number_of_compounds

    #  第二步:开始文件读取

    '''
    注释1:csv,txt,xlsx,docx 4种格式数据读取完毕后,需要生成一个字典AMR_dict,数据格式如下：
    print(AMR_dict):
    {"化合物1":{'S1':['S1理论浓度','S1检测值1','S1检测值2',...'S1回收率1','S1回收率2',...,]},
    {'S2':['S2理论浓度','S2检测值1','S2检测值2',...'S2回收率1','S2回收率2',...,]},
    "化合物2":{'S1':['S1理论浓度','S1检测值1','S1检测值2',...'S1回收率1','S1回收率2',...,]},
    {'S2':['S2理论浓度','S2检测值1','S2检测值2',...'S2回收率1','S2回收率2',...,]}
    '''

    #  1 定义最终需要的列表和字典
    AMR_dict={} #最终需要生成的字典
    Accuracyjudge=[] #每个化合物超过回收率范围的个数列表
    CVjudge=[] #每个化合物超过CV范围的个数列表
    norm=[] #指标列表
    S=["S1","S2","S3","S4","S5","S6","S7","S8","S9","S10","S11","S12","S13","S14","S15"] # 预定义浓度序号列表

    # 后台管理系统-各项目参数设置-PT指标设置里找到化合物名称(适用于ICP-MS平台)
    zqd = Special.objects.get(project=project) 
    pt_special = PTspecial.objects.get(special=zqd)
    pt_accept = PTspecialaccept.objects.filter(pTspecial=pt_special)
    PTnorm=[] # 待测物质列表
    for i in pt_accept:
        PTnorm.append(i.norm)

    for k in range(norm_num):  #中间精密度需先循环化合物个数，在循环文件
        group_AMR={} #每个化合物数据字典
        for fileindex in range(len(files)):
            file=files[fileindex]
            if manufacturers =="Agilent": 
                if '.png' not in file.name and ".JPG" not in file.name:  
                    data = xlrd.open_workbook(filename=None, file_contents=file.read())  # 读取表格
                    file.seek(0,0)  #循环读取同一个文件两遍，需加此句代码移动文件读取指针到开头，否则会报错
                    file_data = data.sheets()[0]
                    nrows=file_data.nrows
                    ncols=file_data.ncols

                    # 从第一行确定化合物名称
                    for j in range(ncols):
                        for i in PTnorm:             
                            if i in file_data.row_values(0)[j] and i not in norm:
                                norm.append(i) 

                    # 从第二行确定实验号和化合物浓度索引
                    nameindex=0  #实验号索引
                    conindex=[] #浓度索引
                    for j in range(ncols):       
                        if file_data.row_values(1)[j] == "样品名称":
                            nameindex = j
                        elif file_data.row_values(1)[j] == "浓度 [ ppm ]" or file_data.row_values(1)[j] == "浓度 [ ppb ]":
                            conindex.append(j)

                    # 确认原始数据中与AMR相关(实验号前含有"AMR-")的sample name名，放进一个列表
                    AMR_STD=[] 
                    for i in range(nrows):
                        if "AMR-" in file_data.row_values(i)[nameindex]:
                            AMR_STD.append(file_data.row_values(i)[nameindex])
                
                    # AMR_STD_distict=[] 
                    # for i in AMR_STD:
                    #     if i not in AMR_STD_distict: # AMR_STD列表去重
                    #         AMR_STD_distict.append(i)
                    
                    # print(AMR_STD_distict) : ['AMR-STD-1', 'AMR-STD-2', 'AMR-STD-3', 'AMR-STD-4', 'AMR-STD-5',...]

                    for j in range(len(AMR_STD)): 
                        calconc=[]  # 每个化合物内各曲线点（S1,S2,S3...）的数据列表列表：['S1检测值1','S1检测值2',...] 
                         
                        for i in range(nrows): # 循环原始数据中的每一行
                            if file_data.row_values(i)[nameindex] == AMR_STD[j]: # 如果实验号命名方式匹配上，则在相应列表中添加相应数据  
                                calconc.append(effectnum(file_data.row_values(i)[conindex[k]],digits)) #添加实际浓度       

                        # # 第一个化合物的第一个曲线点列表calconc循环完成，放入group_AMR中，开始循环该化合物的下一个曲线点
                        # group_AMR.append(calconc)

                        # 第一个文件才将group_AMR[AMR_STD[j]]设为空，否则只能显示最后一个文件的数据
                        if fileindex==0:
                            group_AMR[AMR_STD[j]]=[]
                        for i in calconc:
                            group_AMR[AMR_STD[j]].append(i)

                else:
                    if k==0:
                        if AMRpicture.objects.filter(reportinfo = reportinfo,img = "img/"+file.name):
                            pass
                        else:
                            AMRpicture.objects.create(reportinfo = reportinfo,img = file,name="")

                        objs_verify = AMRpicture.objects.filter(reportinfo = reportinfo)
                        id=[]
                        for item in objs_verify:
                            id.append(item.reportinfo_id)
        AMR_dict[norm[k]]=group_AMR # 第一个化合物的数据列表group_AMR循环完成，放入最终字典AMR_dict中，开始循环下一个化合物
    print(AMR_dict)
    
    return {"AMR_dict":AMR_dict,"objs_verify":objs_verify,"id":id[0],"Unit":Unit}

## 检出限数据上传读取
def LODfileread(files,reportinfo,project,platform,manufacturers,Unit,digits,ZP_Method_precursor_ion,ZP_Method_product_ion):
    LOD_dict={}

    if platform=="ICP-MS":
        if manufacturers =="Agilent":
            for file in files:
                data = xlrd.open_workbook(filename=None, file_contents=file.read())  # 读取表格
                file_data = data.sheets()[0]
                nrows=file_data.nrows
                ncols=file_data.ncols

                # 后台管理系统-各项目参数设置-PT指标设置里找到化合物名称
                zqd = Special.objects.get(project=project) 
                pt_special = PTspecial.objects.get(special=zqd)
                pt_accept = PTspecialaccept.objects.filter(pTspecial=pt_special)
                PTnorm=[] # 待测物质列表

                for i in pt_accept:
                    PTnorm.append(i.norm)

                # 从第一行确定化合物名称
                norm=[]
                for j in range(ncols):
                    for i in PTnorm:             
                        if i in file_data.row_values(0)[j]:
                            norm.append(i) 

                # 从第二行确定实验号（Sample Name）的索引和化合物浓度索引
                nameindex=0  #实验号索引
                conindex=[] #浓度索引
                for j in range(ncols):       
                    if file_data.row_values(1)[j] == "样品名称":
                        nameindex = j
                    elif file_data.row_values(1)[j] == "浓度 [ ppm ]" or file_data.row_values(1)[j] == "浓度 [ ppb ]":
                        conindex.append(j)

                # 匹配原始数据中与精密度相关(实验号前含有"L-"或"M-"或"H-")的行  
                for j in range(len(conindex)):
                    LOD_dict[norm[j]]=[]
                    for i in range(2,nrows): 
                        if "JCX-" in file_data.row_values(i)[nameindex]:
                            LOD_dict[norm[j]].append(float(effectnum(file_data.row_values(i)[conindex[j]],digits)))

            ### 数据文件读取完毕后的操作          
            for key in LOD_dict.keys():
                mean=new_round(np.mean(LOD_dict[key]),5)
                sd=new_round(np.std(LOD_dict[key],ddof=1),5)
                lod_3sd=new_round(3*sd,5)
                lod_10sd=new_round(10*sd,5)
                LOD_dict[key].append(str(mean))
                LOD_dict[key].append(str(sd))
                LOD_dict[key].append(str(lod_3sd))
                LOD_dict[key].append(str(lod_10sd))

            for key,value in LOD_dict.items():
                for i in range(len(LOD_dict[key])):
                    if isinstance(LOD_dict[key][i], str)!=True:
                        LOD_dict[key][i]=effectnum(LOD_dict[key][i],digits)

            print(LOD_dict)

            Experimentnum=["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","X","SD","LOD(3 SD)","LOD(10 SD)"]

            insert_list =[]
            for key,value in LOD_dict.items():
                for i in range(len(value)):
                    insert_list.append(LOD(reportinfo=reportinfo,Experimentnum=Experimentnum[i],norm=key,result=value[i]))

            LOD.objects.bulk_create(insert_list)

        return {"LOD_dict":LOD_dict,"Unit":Unit}

    else:
        for file in files:
            if '.png' in file.name:
                if LODpicture.objects.filter(reportinfo = reportinfo,img = "img2/"+file.name):
                    pass
                else:
                    LODpicture.objects.create(reportinfo = reportinfo,img = file,name="")

                objs_verify = LODpicture.objects.filter(reportinfo = reportinfo)
                id=[]
                for item in objs_verify:
                    id.append(item.reportinfo_id)

        return {"objs_verify":objs_verify,"id":id[0]}

                    
# AMR数据关联进入最终报告
def related_AMR(id,unit): 
    print(unit)
    # 第一步：后台描述性内容数据提取

    # 根据id找到项目
    project=ReportInfo.objects.get(id=id).project

    # 优先查找特殊参数设置里是否有数据，如有就调用，没有则调用通用性参数设置里的数据
    # 特殊数据抓取
    AMR_special = Special.objects.get(project=project)   
    amr_special = AMRspecial.objects.get(special=AMR_special) 
    textlist_special = [] #特殊参数设置描述性内容
    if AMRspecialtexts.objects.filter(aMRspecial=amr_special).count()>0: 
        text_special = AMRspecialtexts.objects.filter(aMRspecial=amr_special)   
        for i in text_special:
            textlist_special.append(i.text)

    # 通用数据抓取
    AMR_general = General.objects.get(name="通用性项目") #通用参数设置描述性内容
    amr_general = AMRgeneral.objects.get(general=AMR_general)
    text_general = AMRgeneraltexts.objects.filter(aMRgeneral=amr_general)   
    textlist_general = [] 
    for i in text_general:
        textlist_general.append(i.text) #AMR通用参数设置描述性内容添加完毕

    # 查找是否单独设置了每个化合物的有效位数
    DIGITS_TABLE = Special.objects.get(project=project) 
    pt_special = PTspecial.objects.get(special=DIGITS_TABLE)
    pt_accept = PTspecialaccept.objects.filter(pTspecial=pt_special)
    Digitslist=[] # 每个化合物有效位数列表
    Digitsdict={} # 每个化合物有效位数字典

    for i in pt_accept:
        Digitslist.append(i.digits)

    if Digitslist==[] or Digitslist[0]=="": #如果全部没设置或者只是单位没设置
        pass
    else:
        for i in pt_accept:
            Digitsdict[i.norm]=i.digits

    # 第二步：报告数据提取
    dataAMR = AMR.objects.filter(reportinfo_id=id) # 根据id找到相应报告

    '''
    此数据关联步骤需要生成一个字典AMR_dict_report，数据格式如下：
    print(AMR_dict_report):
    {"化合物1":[['S1','S1理论浓度','S1检测值1','S1回收率1','S1检测值2','S1回收率2'...,'平均回收率','检测值CV'],
    ['S2','S2理论浓度','S2检测值1','S2回收率1','S2检测值2','S2回收率2'...,'平均回收率','检测值CV'],...],
    "化合物2":[['S1','S1理论浓度','S1检测值1','S1回收率1','S1检测值2','S1回收率2'...,'平均回收率','检测值CV'],
    ['S2','S2理论浓度','S2检测值1','S2回收率1','S2检测值2','S2回收率2'...,'平均回收率','检测值CV'],...]]}
    '''

    if dataAMR: # 只有找到了才能继续进行下面这些步骤 
        AMR_dict_report={} #最终需要的字典
        range_AMR_dict={} # 每个化合物的线性范围数据字典

        AMR_endreport_norm=[] #化合物列表
        for i in dataAMR:
            AMR_endreport_norm.append(i.norm)
        
        AMR_endreport_norm_distinct=[] #化合物列表去重
        for i in AMR_endreport_norm:
            if i not in AMR_endreport_norm_distinct:
                AMR_endreport_norm_distinct.append(i)
                           
        for i in AMR_endreport_norm_distinct:
            dataAMR_group = AMR.objects.filter(reportinfo_id=id,norm=i) #每个化合物的数据表
            AMR_dict_report[i]=[]
            rangeAMR=[] # 每个化合物的线性范围数据列表
            for item in dataAMR_group: # 依次按顺序从数据库中抓取数据
                #没有为每个化合物单独设置有效位数，则调用通用性设置
                if Digitsdict=={} or list(Digitsdict.values())[0]==None:     
                    group=[]
                    group.append(item.Experimentnum)
                    group.append(item.therory_conc)
                    group.append(item.test_conc1)
                    group.append(item.recycle1)
                    group.append(item.test_conc2)
                    group.append(item.recycle2)
                    group.append(item.test_conc3)
                    group.append(item.recycle3)
                    group.append(item.test_conc4)
                    group.append(item.recycle4)
                    group.append(item.test_conc5)
                    group.append(item.recycle5)
                    group.append(item.test_conc6)
                    group.append(item.recycle6)
                    group.append(item.meanrecycle)
                    group.append(item.cvtest_conc)
                    AMR_dict_report[i].append(group)
                    rangeAMR.append(float(item.therory_conc)) #要计算线性范围最大最小值，得把理论浓度添加进来

                #为每个化合物单独设置了有效位数，则调用每个化合物的设置
                else:
                    group=[]
                    group.append(item.Experimentnum)
                    group.append(effectnum(item.therory_conc,Digitsdict[i]))
                    group.append(effectnum(item.test_conc1,Digitsdict[i]))
                    group.append(item.recycle1)
                    group.append(effectnum(item.test_conc2,Digitsdict[i]))
                    group.append(item.recycle2)
                    group.append(effectnum(item.test_conc3,Digitsdict[i]))
                    group.append(item.recycle3)
                    group.append(effectnum(item.test_conc4,Digitsdict[i]))
                    group.append(item.recycle4)
                    group.append(effectnum(item.test_conc5,Digitsdict[i]))
                    group.append(item.recycle5)
                    group.append(effectnum(item.test_conc6,Digitsdict[i]))
                    group.append(item.recycle6)
                    group.append(item.meanrecycle)
                    group.append(item.cvtest_conc)
                    AMR_dict_report[i].append(group)
                    rangeAMR.append(float(item.therory_conc)) #要计算线性范围最大最小值，得把理论浓度添加进来
            range_AMR_dict[i]=rangeAMR

        # print(range_AMR_dict) {'25OHD3': [8.66, 15.3, 29.2, 60.2, 148.0], '25OHD2': [8.58, 14.4, 27.9, 57.7, 143.0]}

        # 描述性内容最后一句结论格式：结果数据如表10和图1~2，18-OHF线性范围为{{resultAMR.min}}~{{resultAMR.max}}pmol/L, 定量限为{{resultAMR.min}}pmol/L。
        AMR_textlist_end='' # 预先定义一个空字符串，用来存放AMR描述性内容的最后一句话
        for key,value in range_AMR_dict.items():
            AMR_textlist_end+=key
            AMR_textlist_end+="线性范围为"
            AMR_textlist_end+=str(min(value))+'~'+str(max(value))+unit+','
            AMR_textlist_end+='定量限为'+str(min(value))+unit+';'

        # print(AMR_textlist_end) 25OHD3线性范围为8.66~148.0pmol/L,定量限为8.66pmol/L;25OHD2线性范围为8.58~143.0pmol/L,定量限为8.58pmol/L;
        AMR_textlist_end=AMR_textlist_end[:-1] #去除最后一个分号
        
        objs = AMRpicture.objects.filter(reportinfo_id=id) #图片数据表

        if len(textlist_special)!=0:
            return {"AMR_dict_report":AMR_dict_report,"AMR_textlist_end":AMR_textlist_end,"textlist":textlist_special,"serial":len(textlist_special)+1,"id":id,"objs":objs}

        else:
            return {"AMR_dict_report":AMR_dict_report,"AMR_textlist_end":AMR_textlist_end,"textlist":textlist_general,"serial":len(textlist_general)+1,"id":id,"objs":objs}


# 方法检出限数据关联进入最终报告
def related_LOD(id): 
    # 第一步：后台描述性内容数据提取

    # 根据id找到项目
    project=ReportInfo.objects.get(id=id).project

    # 优先查找特殊参数设置里是否有数据，如有就调用，没有则调用通用性参数设置里的数据
    # 特殊数据抓取
    JCX_special = Special.objects.get(project=project)   
    jcx_special = JCXspecial.objects.get(special=JCX_special) 
    textlist_special = [] #特殊参数设置描述性内容
    if JCXspecialtexts.objects.filter(jCXspecial=jcx_special).count()>0: 
        text_special = JCXspecialtexts.objects.filter(jCXspecial=jcx_special)   
        for i in text_special:
            textlist_special.append(i.text)
    
    # 通用数据抓取
    JCX_general = General.objects.get(name="通用性项目") #通用参数设置描述性内容
    jcx_general = JCXgeneral.objects.get(general=JCX_general)
    text_general = JCXgeneraltexts.objects.filter(jCXgeneral=jcx_general)   
    textlist_general = [] 
    for i in text_general:
        textlist_general.append(i.text) #AMR通用参数设置描述性内容添加完毕

    # 第二步：报告数据提取
    dataLOD = LOD.objects.filter(reportinfo_id=id)
    dataLOD_picture = LODpicture.objects.filter(reportinfo_id=id)

    if dataLOD:
        LOD_endreport_dict={}

        LOD_endreport_norm=[] #待测物质列表

        for i in dataLOD:
            if i not in LOD_endreport_norm:
                LOD_endreport_norm.append(i.norm)

        for i in LOD_endreport_norm:
            dataLOD_group = LOD.objects.filter(reportinfo_id=id,norm=i)
            group=[]
            for j in dataLOD_group:    
                group.append(j.result)
            LOD_endreport_dict[i]=group
        
        print(LOD_endreport_dict)
        
        if len(textlist_special)!=0:
            return {"LOD_endreport_dict":LOD_endreport_dict,"textlist":textlist_special,"serial":len(textlist_special)+1}
        else:
            return {"LOD_endreport_dict":LOD_endreport_dict,"textlist":textlist_general,"serial":len(textlist_general)+1}

    if dataLOD_picture:
        LOD_conclusion=[] 
        for i in dataLOD_picture:
            LOD_conclusion.append(i.conclusion)

        if len(textlist_special)!=0:
            return {"objs":dataLOD_picture,"LOD_conclusion":LOD_conclusion[0],"textlist":textlist_special,"serial":len(textlist_special)+1}
        else:
            return {"objs":dataLOD_picture,"LOD_conclusion":LOD_conclusion[0],"textlist":textlist_general,"serial":len(textlist_general)+1}

# AMR最终结论表格进入最终报告
def related_AMRconclusion(id): 
    data_AMRconclusiontable = AMRconsluion.objects.filter(reportinfo_id=id)
    AMRconclusiontabledict={}

    if data_AMRconclusiontable: 
        for i in data_AMRconclusiontable:
            AMRconclusiontabledict[i.name]=[]
            AMRconclusiontabledict[i.name].append(i.lodconclusion)
            AMRconclusiontabledict[i.name].append(i.loqconclusion)
            AMRconclusiontabledict[i.name].append(i.amrconclusion)
    
        return {"AMRconclusiontabledict":AMRconclusiontabledict}