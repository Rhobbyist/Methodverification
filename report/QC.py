def QCfileread(files):
    # 读取txt文件

    enddict={} #最终字典  
    QCnum=[]
    for index,file in enumerate(files):
        content= []
        for line in file:
            content.append(line.decode("GB2312").replace("\r\n", "").split("\t"))

        nameindex=0
        conindex=0 #浓度索引，岛津的数据格式决定每个化合物的浓度所在列一定是同一列
        norm=[] #化合物列表
        norm_row=[] #化合物所在行
        

        for i in range(len(content[2])):  #第二行确定samplename和浓度所在列
            if content[2][i]=="数据文件名":
                nameindex=i 
            elif content[2][i]=="浓度":
                conindex=i 

        for i in range(len(content)): 
            if content[i][0]=="Name": #如果某一行第一列为"Name"，则该行第二列为化合物名称
                norm.append(content[i][1])
                norm_row.append(i)
        
        print(norm)

        # 每个文件的第一个化合物判断有几个QC
        num=0
        for k in range(norm_row[0],norm_row[1]): 
            if len(content[k])>nameindex:
                if "QC1" in content[k][nameindex]:
                    num+=1
        QCnum.append(num)

        for j in range(len(norm)):
            if index<1:
                enddict[norm[j]]=[]
            group=[]
            if j<len(norm)-1: #如果不是最后一个化合物，索引为该化合物所在行到后一个化合物所在行
                for i in range(norm_row[j],norm_row[j+1]): 
                    if len(content[i])>nameindex:
                        if "QC" in content[i][nameindex]:
                            if j<1:                             
                                if "NEW" in content[i][nameindex]:
                                    date=content[i][nameindex].split("-NEW")[0]
                                elif "new" in content[i][nameindex]:
                                    date=content[i][nameindex].split("-new")[0]
                                else:
                                    date=content[i][nameindex].split("-QC")[0]

                            group.append(content[i][conindex])
                            
            
            else: #如果是最后一个化合物，索引为该化合物所在行到总行数
                for i in range(norm_row[j],len(content)):
                    if len(content[i])>nameindex: 
                        if "QC" in content[i][nameindex]:
                            if j<1:
                                if "NEW" in content[i][nameindex]:
                                    date=content[i][nameindex].split("-NEW")[0]
                                elif "new" in content[i][nameindex]:
                                    date=content[i][nameindex].split("-new")[0]
                                else:
                                    date=content[i][nameindex].split("-QC")[0]

                            group.append(content[i][conindex])
            
            group.insert(0, date)
            enddict[norm[j]].append(group)
            # enddict[norm[j]].insert(0, date)

        
    print(enddict)
    # print(date)

    # list1=[1,2,3]
    # list2=[[4,5,6],[40,50,60],[400,500,600]]
    print(QCnum)
    # fileindex=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    return {'enddict':enddict,"files":files,"QCnum":QCnum}
    
    