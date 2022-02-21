from report.models import *

def related_testmethod(id): 
    # 后台管理系统数据提取

    # 根据id找到项目
    project=ReportInfo.objects.get(id=id).project
    platform=ReportInfo.objects.get(id=id).platform
    manufacturers=ReportInfo.objects.get(id=id).manufacturers

    # 定义相关列表
    zp_method_list=[]
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
            group.append(i.Times)
            group.append(i.ConeV)
            group.append(i.CollisionV)
            zp_method_list.append(group)
      
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

        # ####下面为判断相关数据是否需要在报告中显示
        # zp_method_listTrue=0 #判断质谱参数表格里是否有数据，如有则在报告中显示，没有则不显示
        # if zp_method_list!=[]:
        #     zp_method_listTrue+=1

        # yx_method_listTrue=0 #判断液相参数表格里是否有数据，如有则在报告中显示，没有则不显示
        # if yx_method_list!=[]:
        #     yx_method_listTrue+=1

        # zpTrue=0 #判断质谱大标题是否需要在报告中显示
        # if zp_method_list!=[] or zp_method_texts_list!=[]:
        #     zpTrue+=1

        # yxTrue=0 #判断液相大标题是否需要在报告中显示
        # if yx_method_list!=[] or yx_method_texts_list!=[]:
        #     yxTrue+=1

    except:
        pass

    return{"zp_method_list":zp_method_list,"zp_method_texts_list":zp_method_texts_list,"yx_method_list":yx_method_list,
    "yx_method_texts_list":yx_method_texts_list}

    

