from report.models import *

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


