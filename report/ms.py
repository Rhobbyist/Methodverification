from django.http import HttpResponse
from django.http import HttpResponseRedirect
from report import models
from report.models import *

def MSfileread(files,reportinfo):
    for file in files:
        if '.png' in file.name or ".JPG" in file.name:
            MS.objects.create(reportinfo = reportinfo,img = file,name="")

            objs_verify = MS.objects.filter(reportinfo = reportinfo)
            id=[]
            for item in objs_verify:
                id.append(item.reportinfo_id)
            
    return {"objs_verify":objs_verify,"id":id[0]}

# 基质特异性数据关联进入最终报告
def related_MS(id): 
    # 后台数据关联进入报告
    # 优先查找特殊参数设置里是否有数据，如有就调用，没有则调用通用性参数设置里的数据

    # 从数据库中抓取描述性内容
    MS_general = General.objects.get(name="通用性项目")
    ms_general = MSgeneral.objects.get(general=MS_general)
    MS_text_general = MSgeneraltexts.objects.filter(mSgeneral=ms_general)   
    MS_textlist_general = []
    for i in MS_text_general:
        MS_textlist_general.append(i.text)

    dataMS = MS.objects.filter(reportinfo_id = id)
    conclusion=[]
    for item in dataMS:
        conclusion.append(item.conclusion)

    if dataMS:   
        return {"dataMS":dataMS,"MS_textlist_general":MS_textlist_general,"conclusion":conclusion[0],"serial":len(MS_textlist_general)+1,
        "obj_serial":len(conclusion)}