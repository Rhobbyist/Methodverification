from django.urls import path, include

import report.views

from django.conf.urls import url, include
from django.contrib import admin

from django.conf.urls.static import static
from django.conf import settings


urlpatterns=[
    # 初始界面，即验证界面
    path('', report.views.get_verification_page,name="verification"),

    # 登陆界面
    path('login', report.views.get_login_page, name="login"),

    # 登出界面
    path('logout', report.views.get_logout_page, name="logout"),

    # 报告生成界面
    path('generation', report.views.get_generation_page, name="generation"),

    # 最终报告预览界面(点击报告预览后跳转界面)
    path('reportpreview/<int:id>', report.views.get_reportpreview_page, name="reportpreview"),

    # 最终报告删除界面(点击删除后跳转界面)
    path('reportdelete/<int:id>', report.views.get_reportdelete_page, name="reportdelete"),

    # 在删除界面勾选删除选项(删除整份报告或删除一个或多个验证指标)后返回的界面，也是报告生成界面
    path('reportdeleteselect', report.views.get_reportdeleteselect_page, name="reportdeleteselect"),

    # 在报告生成界面点击继续验证时跳转的界面
    path('verifyagain/<int:id>', report.views.get_verifyagain_page, name="verifyagain"),

    # PT数据保存
    path('PTsave', report.views.PTsave, name="PTsave"),

    # 加标回收率数据保存
    path('Recyclesave', report.views.Recyclesave, name="Recyclesave"),

    # 仪器比对数据保存
    path('InstrumentComparesave', report.views.InstrumentComparesave, name="InstrumentComparesave"),

    # 方法定量限与线性范围(LOQ)数据保存
    path('LOQsave', report.views.LOQsave, name="LOQsave"),
    
    path('mssave', report.views.MSsave, name="MSsave"),
    path('lodsave', report.views.LODsave, name="LODsave"),
    
    path('amr2save', report.views.AMR2save, name="AMR2save"),
    path('amr_conclusionsave', report.views.AMR_conclusionsave, name="AMR_conclusionsave"),
    path('crrsave', report.views.CRRsave, name="CRRsave"),
    path('SampleStabilitySave', report.views.Sample_Stability_Save, name="Sample_Stability_Save"),
    
    path('verifyagain', report.views.verifyagain, name="verifyagain"),
    path('returnback', report.views.returnback, name="returnback"),
    # path('upload', report.views.picture_upload, name="upload"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

