from django.urls import path, include

import report.views

from django.conf.urls import url, include
from django.contrib import admin

from django.conf.urls.static import static
from django.conf import settings


urlpatterns=[
    path('', report.views.get_verification_page,name="verification"),
    path('login', report.views.get_login_page, name="login"),
    path('logout', report.views.get_logout_page, name="logout"),
    path('generation', report.views.get_generation_page, name="generation"),
    path('endreport/<int:id>', report.views.get_endreport_page, name="endreport"),
    path('delete/<int:id>', report.views.delete, name="delete"),
    path('ptsave', report.views.PTsave, name="PTsave"),
    path('recyclesave', report.views.recyclesave, name="recyclesave"),
    path('mssave', report.views.MSsave, name="MSsave"),
    path('lodsave', report.views.LODsave, name="LODsave"),
    path('amrsave', report.views.AMRsave, name="AMRsave"),
    path('amr2save', report.views.AMR2save, name="AMR2save"),
    path('amr_conclusionsave', report.views.AMR_conclusionsave, name="AMR_conclusionsave"),
    path('crrsave', report.views.CRRsave, name="CRRsave"),
    path('SampleStabilitySave', report.views.Sample_Stability_Save, name="Sample_Stability_Save"),
    path('reportdelete', report.views.REPORTdelete, name="REPORTdelete"),
    path('verifyagain', report.views.verifyagain, name="verifyagain"),
    path('returnback', report.views.returnback, name="returnback"),
    # path('upload', report.views.picture_upload, name="upload"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

