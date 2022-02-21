from report.models import *

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