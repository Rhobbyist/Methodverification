from report.models import *

def related_testmethod(id): 
    # 后台管理系统数据提取

    # 根据id找到项目
    project=ReportInfo.objects.get(id=id).project
    platform=ReportInfo.objects.get(id=id).platform
    manufacturers=ReportInfo.objects.get(id=id).manufacturers

    # 定义相关列表
    zp_method_list=[] # 质谱方法表格
    zp_method_texts_list=[]
    yx_method_list=[]
    yx_method_texts_list=[]
    try:
        Testmethod_endreport = Testmethod.objects.get(platform=platform,factory=manufacturers,project=project)
        zp_method = ZP_Method.objects.filter(testmethod=Testmethod_endreport)
        zp_method_texts = ZP_Methodtexts.objects.filter(testmethod=Testmethod_endreport)
        yx_method = YX_Method.objects.filter(testmethod=Testmethod_endreport)
        yx_method_texts = YX_Methodtexts.objects.filter(testmethod=Testmethod_endreport)

        # 质谱方法   
        for i in zp_method:
            group=[]
            group.append(i.norm)
            group.append(i.precursor_ion)
            group.append(i.product_ion)
            if i.Col4!="":
                group.append(i.Col4)
            if i.Col5!="":
                group.append(i.Col5)
            if i.Col6!="":
                group.append(i.Col6)
            if i.Col7!="":
                group.append(i.Col7)
            if i.Col8!="":
                group.append(i.Col8)
            zp_method_list.append(group)
        
        print(zp_method_list)
      
        for i in zp_method_texts:
            zp_method_texts_list.append(i.text)
    
        for i in yx_method:
            group=[]
            group.append(i.step)
            group.append(i.time)
            group.append(i.Flowrate)
            group.append(i.Mobile_phaseB)
            group.append(i.Mobile_phaseA)
            yx_method_list.append(group)
   
        for i in yx_method_texts:
            yx_method_texts_list.append(i.text)

    except:
        pass

    return{"zp_method_list":zp_method_list,"zp_method_texts_list":zp_method_texts_list,"yx_method_list":yx_method_list,
    "yx_method_texts_list":yx_method_texts_list}

def related_equipment(id): 
    # 后台管理系统数据提取
    Detection_equipment_texts_list=[]
    Auxiliary_equipment_texts_list=[]

    try:
        # 根据id找到项目
        project = ReportInfo.objects.get(id=id).project

        Equipment_endreport = Equipment.objects.get(name=project)
        Detection_equipment_texts = Detection_equipment.objects.filter(equipment=Equipment_endreport)
        Auxiliary_equipment_texts = Auxiliary_equipment.objects.filter(equipment=Equipment_endreport)        
        for i in Detection_equipment_texts:
            Detection_equipment_texts_list.append(i.text)
      
        for i in Auxiliary_equipment_texts:
            Auxiliary_equipment_texts_list.append(i.text)
    
    except:
        pass

    return{"Detection_equipment_texts_list":Detection_equipment_texts_list,"Auxiliary_equipment_texts_list":Auxiliary_equipment_texts_list}

def related_Reagents_Consumables(id): 
    # 后台管理系统数据提取
    reagents_texts_list=[]
    consumables_texts_list=[]

    try:
        # 根据id找到项目
        project = ReportInfo.objects.get(id=id).project

        Reagents_Consumables_endreport = Reagents_Consumables.objects.get(name=project)
        Reagents_texts = Reagents.objects.filter(reagents_Consumables=Reagents_Consumables_endreport)
        Consumables_texts = Consumables.objects.filter(reagents_Consumables=Reagents_Consumables_endreport)
        for i in Reagents_texts:
            reagents_texts_list.append(i.text)
 
        for i in Consumables_texts:
            consumables_texts_list.append(i.text)

    except:
        pass

    return{"reagents_texts_list":reagents_texts_list,"consumables_texts_list":consumables_texts_list}

def related_Sample_Preparation(id): 
    # 后台管理系统数据提取
    Sample_Preparation_texts_list=[]

    try:
        # 根据id找到项目
        project = ReportInfo.objects.get(id=id).project

        Sample_Preparation_endreport = Sample_Preparation.objects.get(name=project)
        Sample_Preparation_texts = texts.objects.filter(sample_Preparation=Sample_Preparation_endreport) 
        for i in Sample_Preparation_texts:
            Sample_Preparation_texts_list.append(i.text)

    except:
        pass

    return{"Sample_Preparation_texts_list":Sample_Preparation_texts_list}
