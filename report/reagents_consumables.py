from report.models import *

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

