from re import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db.models import Q
from numpy import number
from report import models
from .forms import UploadFileForm
from report import jmd, zqd, amr, crr, ms, Carry_over, Matrix_effect, Sample_Stability,Sample_ReferenceInterval,QC,others
from .models import *
import time
import re

# 认证模块
from django.contrib import auth

# 对应数据库
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# 登陆界面
def get_login_page(request):

    # post接受用户提交的数据
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("pwd")
        user_obj = auth.authenticate(username=username, password=password)

        # 判断用户是否存在,不存在仍然返回登陆界面
        if not user_obj:  
            message = "用户名或密码错误！"
            return render(request, 'report/login.html', locals())
        
        # 登陆成功跳转至报告生成界面
        else:
            auth.login(request, user_obj)
            return redirect("/generation")

    else:
        # 判断是否为未登录用户,不是返回登陆界面
        if isinstance(request.user, auth.models.AnonymousUser):  
            return render(request, 'report/login.html', locals())
         # 否则跳转至报告生成界面
        else:
            return redirect("/generation")

# 用户注销界面
def get_logout_page(request):
    logout(request)
    return render(request, 'report/logout.html', locals())

# 验证界面
def get_verification_page(request):

    # 判断是否用户是否登录，以在最上方导航栏显示“登录”或“未登录”状态，与layout.html关联
    try:
        name = User.objects.get(username=request.user).first_name
    except:
        pass
    if isinstance(request.user, auth.models.AnonymousUser):  # 判断是否为未登录用户
        User_class = 0
    else:
        User_class = 1

    # 用户在验证界面点击确定按钮后，走post请求
    if request.method == 'POST':
        # 激素11项专用
        if request.POST["quota"] == "激素11项专用":
            files = request.FILES.getlist('fileuploads')
            dicQC = QC.QCfileread(files)
            return render(request, 'report/project/QC.html', locals())

        else:
            # 一 接收验证界面传过来的数据
            instrument_num = request.POST["instrument_num"].strip() # 仪器编号,strip()的作用是去除前后空格
            Detectionplatform = request.POST["Detectionplatform"]  # 检测平台
            project = request.POST["project"]  # 检测项目
            platform = request.POST["platform"]  # 仪器平台(液质,液相,ICP-MS...)       
            manufacturers = request.POST["manufacturers"] # 仪器厂家(AB,Agilent...)
            verifyoccasion = request.POST["verifyoccasion"]  # 验证时机
            # verifyoccasiontexts = request.POST["verifyoccasiontexts"] #自定义验证时机
            # verifytime = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 初始验证时间

            # 二 后台管理系统查找单位,有效位数和化合物个数,此处由于单位,有效位数和化合物个数都为必填项,因此使用get()方法时不需要try
            Unit = Special.objects.get(Detectionplatform=Detectionplatform, project=project).unit  # 单位
            digits = Special.objects.get(project=project).Effective_digits  # 有效位数
            Number_of_compounds = Special.objects.get(project=project).Number_of_compounds  # 化合物个数

            # 三 判断此份报告是否已被创建
            if ReportInfo.objects.filter(number=instrument_num, project=project):
                reportinfo = ReportInfo.objects.get(number=instrument_num,Detectionplatform=Detectionplatform,project=project,
                platform=platform,manufacturers=manufacturers,verifyoccasion=verifyoccasion)
            else:
                reportinfo = ReportInfo.objects.create(number=instrument_num,Detectionplatform=Detectionplatform,project=project,
                platform=platform,manufacturers=manufacturers,verifyoccasion=verifyoccasion)

            # 四 验证原因关联
            if verifyoccasion == "新项目开发":
                if Validation_Reason.objects.filter(reportinfo_id=reportinfo):
                    pass
                else:
                    Validation_Reason.objects.create(reportinfo=reportinfo, reason="新项目首次开展")
            elif verifyoccasion == "期间核查":
                if Validation_Reason.objects.filter(reportinfo_id=reportinfo):
                    pass
                else:
                    Validation_Reason.objects.create(reportinfo=reportinfo, reason="项目已到期间核查时期")
            else:
                pass

            # 五 AB厂家需根据离子对名称和离子对数值进行表格读取
            normAB = []
            ZP_Method_precursor_ion = []  # 母离子列表
            ZP_Method_product_ion = []  # 子离子列表
            try:
                id_AB = Testmethod.objects.get(factory=manufacturers, project=project).id
                ZP_Method_table = ZP_Method.objects.filter(testmethod_id=id_AB, norm__contains='定量')
                       
                for i in ZP_Method_table:
                    ZP_Method_precursor_ion.append(i.precursor_ion)
                    ZP_Method_product_ion.append(i.product_ion)
                    normAB.append(i.norm.split("定量")[0])

            except:
                pass
            
            print("normAB:%s" % (normAB))
            
            # 六 9个验证指标数据提取
            # 1 精密度
            if request.POST["quota"] == "精密度":

                # 1.1 重复性精密度
                if request.POST["jmd"] == "重复性精密度":
                    namejmd = "重复性精密度"
                    files = request.FILES.getlist('fileuploads')
                    Result = jmd.IntraP_fileread(files, reportinfo, namejmd, project, platform, manufacturers,Unit, digits, ZP_Method_precursor_ion, ZP_Method_product_ion, normAB,Number_of_compounds)

                # 1.2 中间精密度
                elif request.POST["jmd"] == "中间精密度":
                    namejmd = "中间精密度"
                    files = request.FILES.getlist('fileuploads')
                    Result = jmd.InterP_fileread(files, reportinfo, namejmd, project, platform, manufacturers,Unit, digits, ZP_Method_precursor_ion, ZP_Method_product_ion, normAB,Number_of_compounds)
                return render(request, 'report/project/Jmd.html', locals())

            # 2 正确度
            elif request.POST["quota"] == "正确度":

                # 2.1 PT
                if request.POST["zqd"] == "PT":
                    files = request.FILES.getlist('fileuploads')

                    # 判断是否为25OHD项目
                    if "25OHD" not in project:
                        Result = zqd.PTfileread(files, Detectionplatform, project, platform, manufacturers,digits, ZP_Method_precursor_ion, ZP_Method_product_ion, normAB,Number_of_compounds)
                    else:
                        Result = zqd.PT_25OHD_fileread(files, Detectionplatform, project, platform, manufacturers,digits, ZP_Method_precursor_ion, ZP_Method_product_ion, normAB,Number_of_compounds)
                    
                    return render(request, 'report/project/PT.html', locals())

                # 2.2 加标回收率
                elif request.POST["zqd"] == "加标回收":
                    files = request.FILES.getlist('fileuploads')
                    Result = zqd.Recyclefileread(files, project, platform, manufacturers, Unit, digits, ZP_Method_precursor_ion, ZP_Method_product_ion, normAB,Number_of_compounds)
                    return render(request, 'report/project/Recycle.html', locals())

                # 2.3 仪器比对
                elif request.POST["zqd"] == "仪器比对":
                    return render(request, 'report/project/InstrumentCompare.html', locals())
            
            # 3 分析灵敏度与分析测量范围(Analytical Sensitivity and Analytical Measurement Range)
            
            elif request.POST["quota"] == "分析灵敏度与分析测量范围":

                # 3.1 方法定量限与线性范围(Limit of Quantitation and Linearity,LOQ)
                if request.POST["amr"] == "方法定量限与线性范围":
                    files = request.FILES.getlist('fileuploads')

                    # 判断上传的数据文件(不是图片文件)是1个还是多个
                    data_uploadfile_num = 0 
                    for file in files:
                        if '.png' not in file.name and ".JPG" not in file.name and ".PNG" not in file.name:
                            data_uploadfile_num +=1
                    
                    if data_uploadfile_num == 1:
                        Result = amr.LOQfileread(files, reportinfo, project, platform, manufacturers, Unit,digits, ZP_Method_precursor_ion, ZP_Method_product_ion, normAB, Number_of_compounds)  
                    else:
                        Result = amr.LOQgeneral_multiplefileread(files, reportinfo, project, platform, manufacturers, Unit,digits, ZP_Method_precursor_ion, ZP_Method_product_ion, normAB, Number_of_compounds)       
                    return render(request, 'report/project/LOQ.html', locals())

                # 3.2 方法检出限(Limit of Detection,LOD)
                elif request.POST["amr"] == "方法检出限":
                    files = request.FILES.getlist('fileuploads')
                    dicLOD = amr.LODfileread(files, reportinfo, project, platform, manufacturers,
                                            Unit, digits, ZP_Method_precursor_ion, ZP_Method_product_ion, normAB, Number_of_compounds)
                    return render(request, 'report/project/LOD.html', locals())
                elif request.POST["amr"] == "结论":
                    AMRid = ReportInfo.objects.get(number=instrument_num, project=project).id
                    return render(request, 'report/project/AMR_conclusion.html', locals())

            elif request.POST["quota"] == "临床可报告范围":
                if request.POST["crr"] == "不做验证":
                    CRRid = ReportInfo.objects.get(number=instrument_num, project=project).id
                    return render(request, 'report/project/CRRspecial.html', locals())
                else:
                    files = request.FILES.getlist('fileuploads')
                    Result = crr.CRRfileread(files, reportinfo, project, platform, manufacturers,
                                            Unit, digits, ZP_Method_precursor_ion, ZP_Method_product_ion, normAB, Number_of_compounds)
                    return render(request, 'report/project/CRRgeneral.html', locals())

            elif request.POST["quota"] == "基质特异性":
                files = request.FILES.getlist('fileuploads')
                MS = ms.MSfileread(files, reportinfo)
                return render(request, 'report/project/MS.html', locals())

            elif request.POST["quota"] == "基质效应":
                files = request.FILES.getlist('fileuploads')
                Result = Matrix_effect.Matrix_effect_fileread(files, reportinfo, project, platform, manufacturers, digits, ZP_Method_precursor_ion, ZP_Method_product_ion, normAB, Number_of_compounds)
                return render(request, 'report/project/Matrix_effect.html', locals())

            elif request.POST["quota"] == "携带效应":        
                if request.POST["carryover"] == "9个样本":
                    files = request.FILES.getlist('fileuploads')
                    Result = Carry_over.Carryover_9sample_fileread(files, Detectionplatform, reportinfo, project, platform,
                    manufacturers, Unit, digits, ZP_Method_precursor_ion, ZP_Method_product_ion, normAB, Number_of_compounds)
                    return render(request, 'report/project/Carryovergeneral.html', locals())

            elif request.POST["quota"] == "样品稳定性":
                if request.POST["stability"] == "样品储存稳定性":     
                    files = request.FILES.getlist('fileuploads')
                    Result = Sample_Stability.store_fileread(files, Detectionplatform, reportinfo, project, platform,manufacturers, Unit, digits, ZP_Method_precursor_ion, ZP_Method_product_ion, normAB, Number_of_compounds)
                elif request.POST["stability"] == "样品处理后稳定性":     
                    files = request.FILES.getlist('fileuploads')
                    Result = Sample_Stability.handle_fileread(files, Detectionplatform, reportinfo, project, platform,manufacturers, Unit, digits, ZP_Method_precursor_ion, ZP_Method_product_ion, normAB, Number_of_compounds) 
                return render(request, 'report/project/Sample_Stability.html', locals())

            elif request.POST["quota"] == "参考区间":
                if request.POST["referenceinterval"] == "参考区间建立":     
                    files = request.FILES.getlist('fileuploads')
                    Result = Sample_ReferenceInterval.create_fileread(files, Detectionplatform, reportinfo, project, platform,manufacturers, Unit, digits, ZP_Method_precursor_ion, ZP_Method_product_ion, normAB, Number_of_compounds)
                    return render(request, 'report/project/RI_Create.html', locals())
                elif request.POST["referenceinterval"] == "参考区间验证":        
                    files = request.FILES.getlist('fileuploads')
                    Result = Sample_ReferenceInterval.quote_fileread(files, Detectionplatform, reportinfo, project, platform,manufacturers, Unit, digits, ZP_Method_precursor_ion, ZP_Method_product_ion, normAB, Number_of_compounds)
                    return render(request, 'report/project/RI_quote.html', locals())

    else:
        Detectionplatform = []  # 检测平台列表，需传到verification.html
        project = []  # 项目列表，需传到verification.html
        Detectionplatformdata = Special.objects.all()

        for i in Detectionplatformdata:
            if i.Detectionplatform not in Detectionplatform:
                Detectionplatform.append(i.Detectionplatform)
        Detectionplatform.sort()

        for i in range(len(Detectionplatform)):
            project.append([])
            projectdata = Special.objects.filter(
                Detectionplatform=Detectionplatform[i])
            for j in projectdata:
                project[i].append(j.project)

    return render(request, 'report/verification.html', locals())

# 报告生成界面
def get_generation_page(request):
    # 判断是否用户是否登录，以在最上方导航栏显示“登录”或“未登录”状态，与layout.html关联
    name = User.objects.get(username=request.user).first_name
    if isinstance(request.user, auth.models.AnonymousUser):  # 判断是否为未登录用户
        User_class = 0  # 页面右上方显示"未登录"(layout.html)
    else:
        User_class = 1  # 页面右上方显示当前登录用户名(layout.html)

    # 项目平台主管只能看到自己平台下的项目
    if name == "余木俊" or name == "陈文彬":
        data = ReportInfo.objects.filter(Detectionplatform="微量营养素检测平台")
    elif name == "李冰玲":
        data = ReportInfo.objects.filter(Q(Detectionplatform="治疗药物检测平台") | Q(Detectionplatform="内分泌检测平台"))
    elif name == "陈秀茹":
        data = ReportInfo.objects.filter(Detectionplatform="遗传代谢病检测平台")
    else:
        data = ReportInfo.objects.all()
        # data = ReportInfo.objects.filter().exclude(number="test").all()
    return render(request, 'report/generation.html', locals())

# 最终报告预览界面(点击报告预览后跳转界面)
def get_reportpreview_page(request, id):
    # 从数据库中抓取当前用户名传递到layout.html
    try:
        name = User.objects.get(username=request.user).first_name
    except:
        name = "未注册用户"

    # 判断是否为未登录用户
    if isinstance(request.user, auth.models.AnonymousUser):  
        User_class = 0
    else:
        User_class = 1

    # 基本参数，此处由于在验证界面提交数据时已经进行了判断，因此在使用get()方法时不需要try
    Instrument_number = ReportInfo.objects.get(id=id).number  # 仪器编号
    Detectionplatform = ReportInfo.objects.get(id=id).Detectionplatform  # 检测平台
    project = ReportInfo.objects.get(id=id).project  # 检测项目
    platform = ReportInfo.objects.get(id=id).platform  # 仪器项目
    manufacturers = ReportInfo.objects.get(id=id).manufacturers # 仪器厂家

    # project为必设置项,因此此部分不需要try
    special_id = Special.objects.get(project=project).id  # 找到特殊参数设置里对应的项目
    chinese_title = Special.objects.get(project=project).chinese_titie  # 中文标题
    english_title = Special.objects.get(project=project).english_titie  # 英文标题
    unit = Special.objects.get(project=project).unit  # 单位
    digits = Special.objects.get(project=project).Effective_digits  # 有效位数
    Number_of_compounds = int(Special.objects.get(project=project).Number_of_compounds)  # 化合物个数

    # 检测方法里找到仪器型号和色谱柱。可能存在用户忘记设置的情况，因此需要try
    try:
        Instrument_model = Testmethod.objects.get(platform=platform, factory=manufacturers, project=project).Instrument_model  # 仪器型号
    except:
        Instrument_model = "未设置仪器型号"
    
    try:
        Column = Testmethod.objects.get(platform=platform, factory=manufacturers, project=project).column  # 色谱柱
    except:
        Column = "未设置色谱柱"

    # Protocol_ID可由英文标题和验证时间推算出来
    if "by" in english_title and str(ReportInfo.objects.get(id=id).verifytime) != "":
        Protocol_ID = english_title.split("by")[1] + str(ReportInfo.objects.get(id=id).verifytime)[0:4] + str(ReportInfo.objects.get(id=id).verifytime)[5:7]   # Protocol ID
    else:
        Protocol_ID = "英文标题格式不对,需含有'by'关键词!!!"

    # 判断是否单独为某个化合物设置了单位 unit = {"化合物1":"单位1","化合物2":"单位6"}、
    UNIT_TABLE = Special.objects.get(project=project)
    pt_special = PTspecial.objects.get(special=UNIT_TABLE)
    pt_accept = PTspecialaccept.objects.filter(pTspecial=pt_special)
    Unitlist = []  # 每个化合物单位列表
    Unitdict = {}  # 每个化合物单位字典

    for i in pt_accept:
        Unitlist.append(i.unit)

    if Unitlist == [] or Unitlist[0] == "":  # 如果全部没设置或者只是单位没设置
        pass
    else:
        for i in pt_accept:
            Unitdict[i.norm] = i.unit

    if Number_of_compounds == 1:  # 单个化合物
        # 验证原因
        data_Validation_Reason = Validation_Reason.objects.filter(reportinfo_id=id) 
        text_Validation_Reason = []
        for i in data_Validation_Reason:
            text_Validation_Reason.append(i.reason)

        titleindex = 6  # 总标题索引从6开始  -- 6
        tableindex = 3  # 总表格索引从3开始。表1质谱参数，表2液相梯度条件

        # ---------------------------------------精密度（每个化合物一个表格）---------------------------------------
        JMDindex = titleindex  # 精密度主标题索引 6

        # 1 重复性精密度数据
        PNjmdindex = 0  # 重复性精密度副标题索引   6.1

        tablePNindex = tableindex # 重复性精密度表格索引  表3

        PNjmd_data = jmd.related_PNjmd(id)
        if PNjmd_data:
            if PNjmd_data["JMD_dict"]: 
                PNjmdindex += 1  # 重复性精密度副标题索引+1  6.2
                tableindex += Number_of_compounds  # 总表格索引+n，以两个化合物为例，开始是表3，现在是表5   表5

        # 2 中间精密度数据
        PJjmdindex = PNjmdindex  # 重复性精密度副标题索引赋值给中间精密度副标题索引

        tablePJindex = tableindex

        PJjmd_data = jmd.related_PJjmd(id)  
        if PJjmd_data: 
            if PJjmd_data["JMD_dict"]:
                PJjmdindex += 1  # 中间精密度副标题索引+1
                tableindex += Number_of_compounds 

        # 3 精密度结论
        JMDconclusionindex = PJjmdindex
        tableJMDconclusionindex = tableindex

        if PNjmd_data["JMD_dict"] and PJjmd_data["JMD_dict"]:
            jmdconclusion_data = jmd.related_jmdendconclusion(id)
        
            if jmdconclusion_data:
                JMDconclusionindex += 1  # 精密度结论副标题索引+1 -- 6.3
                tableindex += 1

        # 4 判断总标题索引是否需要自增
        if PNjmd_data["JMD_dict"] or PJjmd_data["JMD_dict"]:   # 如果有重复性精密度和中间精密度,总标题索引+1
            titleindex += 1 # -- 7

        # --------------------------------------- 正确度（每个化合物一个表格）---------------------------------------

        ZQDindex = titleindex # 正确度主标题索引 

        # 1  PT
        PTindex = 0  # PT副标题索引  7.1

        tablePTindex = tableindex

        PT_data = zqd.related_PT(id)
        if PT_data["PT_dict"]:
            PTindex += 1 # # 正确度副标题索引+1  7.2
            tableindex += Number_of_compounds

        # 2 加标回收率
        Recycleindex = PTindex # --7.1

        tableRecycleindex_start = tableindex
        tableRecycleindex_end = tableindex+Number_of_compounds-1

        Recycle_data = zqd.related_recycle(id)
        if Recycle_data:
            Recycleindex += 1 # --7.2
            tableindex += Number_of_compounds

        # 3 仪器比对
        InstrumentCompareindex = Recycleindex

        # 仪器比对描述性文字
        InstrumentCompare_data = InstrumentCompare.objects.filter(reportinfo_id=id)
        InstrumentCompare_text = []
        for i in InstrumentCompare_data:
            InstrumentCompare_text.append(i.textarea)
        
        if InstrumentCompare_data:
            InstrumentCompareindex += 1

        # 4 判断总标题索引是否需要自增
        if PT_data["PT_dict"] or Recycle_data:
            titleindex += 1  # 8

        # --------------------------------------- AMR（每个化合物一个表格）---------------------------------------
        
        AMRindex = titleindex  # AMR主标题索引

        # 1 LOQ
        LOQindex = 0
        pictureindex = 1  # 总图片索引
        tableLOQindex = tableindex
        pictureLOQindex_start = pictureindex
        pictureLOQindex_end = pictureindex+Number_of_compounds-1

        LOQ_data = amr.related_AMR(id, unit)
        if LOQ_data["AMR_dict"]:
            LOQindex += 1
            pictureindex += Number_of_compounds*2  # 总图片索引
            tableindex += Number_of_compounds

        # 2 LOD
        LODindex = LOQindex
        tableLODindex = tableindex
        pictureLODindex_start = pictureindex
        pictureLODindex_end = pictureindex+Number_of_compounds-1

        LOD_data = amr.related_LOD(id)
        if LOD_data:
            LODindex += 1
            pictureindex += Number_of_compounds

        # 3 AMRconclusion
        AMRconclusionindex = LODindex
        tableAMRconclusionindex = tableindex

        AMRconclusion_data = amr.related_AMRconclusion(id)
        if AMRconclusion_data:
            AMRconclusionindex += 1
            tableindex += 1

        if LOQ_data["AMR_dict"] or LOD_data:
            titleindex += 1

        # --------------------------------------- 稀释倍数（每个化合物一个表格）---------------------------------------
        CRRindex = titleindex # CRR主标题索引

        # 1 进行稀释倍数验证      
        CRR2_True = 1
        Dilutionindex = 0

        tableDilutionindex = tableindex

        Dilution_data = crr.related_CRR(id,unit)
        if Dilution_data:
            if Dilution_data["CRR_dict"]:
                Dilutionindex += 1
                titleindex += 1
                tableindex += 1

        # ---------------------------------------------- 基质特异性 --------------------------------------------------
        MSindex = titleindex
        pictureMSindex_start = pictureindex
        pictureMSindex_end = pictureindex+2  # 固定三种图(标准品，血清样本，空白基质)
        resultMS = ms.related_MS(id)
        if resultMS:
            titleindex += 1

        # --------------------------------------- 基质效应（每个化合物一个表格）---------------------------------------
        Matrix_effectindex = titleindex # 基质效应主标题索引

        tableMatrix_effectindex = tableindex

        Matrix_effect_data = Matrix_effect.related_Matrix_effect(id)
        if Matrix_effect_data["Matrixeffect_dict"]:
            titleindex += 1
            tableindex += 1

        # --------------------------------------- 携带效应 ---------------------------------------
        Carryoverindex = titleindex # 携带效应主标题索引

        tableCarryoverindex = tableindex

        Carryover_data = Carry_over.related_Carryover(id)
        if Carryover_data["Carryover_dict"]:
            titleindex += 1
            tableindex += 1

        # --------------------------------------- 样品稳定性 ---------------------------------------
        # 1 数据抓取与参数设置
        Stability_data = Sample_Stability.data_scrap(id)  # 抓取数据库中的数据
        Stabilityindex = titleindex  # 设置标题索引
        tableStabilityindex_start = tableindex  # 设置第一个表格索引
        tableStabilityindex_end = tableindex+Number_of_compounds*3-1

        # 2 如果存在数据，自增标题索引和表格索引
        if Stability_data["Room_conclevel_list"]:
            titleindex += 1
            tableindex += Number_of_compounds*2-1

        # --------------------------------------- 参考区间 ---------------------------------------
        # 1 数据抓取与参数设置
        Reference_Interval_data = Sample_ReferenceInterval.data_scrap(id)  # 抓取数据库中的数据
        Reference_Interval_index = titleindex  # 设置标题索引
        table_Reference_Interval_index_start = tableindex+1  # 设置第一个表格索引,参考区间在一个表格中显示
        # table_Reference_Interval_index_end = tableindex+Number_of_compounds*2-1 # 设置最后一个表格索引索引

        # 2 如果存在数据，自增标题索引和表格索引
        if Reference_Interval_data["Referenceinterval_dict"]:
            titleindex += 1
            tableindex += 1

        # --------------------------------------- 检测方法，设备，试剂耗材，样品处理，最终结论 ---------------------------------------
        Test_method_data = others.related_testmethod(id)
        Equipment_data = others.related_equipment(id)
        Reagents_Consumables_data = others.related_Reagents_Consumables(id)
        Sample_Preparation_data = others.related_Sample_Preparation(id)
        
        Endconclusion = "由以上各参数验证可知，本方法的分析灵敏度、分析测量范围、基质特异性、基质效应、临床可报告范围（稀释倍数）、精密度（重复性精密度和中间精密度）、正确度（PT，加标回收率）、携带效应、样品稳定性（样本储存稳定性和样本处理后稳定性）、参考区间均满足临床开展要求，本方法可以在FXS-YZ26（Thermo TSQ Altis LC-MS/MS）仪器上进行血清雌二醇、雌酮项目临床样本的日常检测。"

        Endconclusion = Endconclusion.replace('FXS-YZ26', Instrument_number)
        Endconclusion = Endconclusion.replace('Thermo TSQ Altis LC-MS/MS', Instrument_model)
        Endconclusion = Endconclusion.replace('血清雌二醇、雌酮', project)

        if not LOQ_data["AMR_dict"]:      
            Endconclusion = Endconclusion.replace('分析灵敏度、分析测量范围、', '')

        if not resultMS:
            Endconclusion = Endconclusion.replace('基质特异性、', '')

        if not Matrix_effect_data["Matrixeffect_dict"]:
            Endconclusion = Endconclusion.replace('基质效应、', '')

        if not Dilution_data["CRR_dict"]:
            Endconclusion = Endconclusion.replace('临床可报告范围（稀释倍数）、', '')

        # 精密度
        if not PNjmd_data["JMD_dict"] and not PJjmd_data["JMD_dict"]:
            Endconclusion = Endconclusion.replace('精密度（重复性精密度和中间精密度）、', '')

        if not PNjmd_data["JMD_dict"]:
            Endconclusion = Endconclusion.replace('重复性精密度和', '')

        if not PJjmd_data["JMD_dict"]:
            Endconclusion = Endconclusion.replace('和中间精密度', '')

        # 正确度
        if not PT_data["PT_dict"] and not Recycle_data:
            Endconclusion = Endconclusion.replace('正确度（PT，加标回收率）、', '')

        if not PT_data["PT_dict"]:
            Endconclusion = Endconclusion.replace('PT，', '')

        if not Recycle_data:
            Endconclusion = Endconclusion.replace('，加标回收率', '')

        if not Carryover_data["Carryover_dict"]:
            Endconclusion = Endconclusion.replace('携带效应、', '')

        if not Stability_data["Room_conclevel_list"]:
            Endconclusion = Endconclusion.replace('样品稳定性（样本储存稳定性和样本处理后稳定性）、', '')

        if not Reference_Interval_data["Referenceinterval_dict"]:
            Endconclusion = Endconclusion.replace('、参考区间', '')

        return render(request, 'report/reportpreview-single.html', locals())

    else:  # 多个化合物
        # 验证原因
        data_Validation_Reason = Validation_Reason.objects.filter(reportinfo_id=id) 
        text_Validation_Reason = []
        for i in data_Validation_Reason:
            text_Validation_Reason.append(i.reason)

        titleindex = 6  # 总标题索引从6开始  -- 6
        tableindex = 3  # 总表格索引从3开始。表1质谱参数，表2液相梯度条件

        # ---------------------------------------精密度（每个化合物一个表格）---------------------------------------
        JMDindex = titleindex  # 精密度主标题索引 6

        # 1  重复性精密度数据
        PNjmdindex = 0  # 重复性精密度副标题索引   6.1

        tablePNindex_start = tableindex # 第一个化合物的表格索引  表3
        tablePNindex_end = tableindex+Number_of_compounds-1 # 最后一个化合物的表格索引  以3个化合物为例，表3+3-1=5

        PNjmd_data = jmd.related_PNjmd(id)
        if PNjmd_data["JMD_dict"]:
            PNjmdindex += 1  # 重复性精密度副标题索引+1  6.2
            tableindex += Number_of_compounds  # 总表格索引+n，以两个化合物为例，开始是表3，现在是表5   表5

        # 2 中间精密度数据
        PJjmdindex = PNjmdindex  # 中间精密度副标题索引

        tablePJindex_start = tableindex
        tablePJindex_end = tableindex+Number_of_compounds-1

        PJjmd_data = jmd.related_PJjmd(id)
        if PJjmd_data["JMD_dict"]:
            PJjmdindex += 1  # 中间精密度副标题索引+1  -- 6.2
            tableindex += Number_of_compounds  # 总表格索引+n

        # 3 精密度结论数据
        JMDconclusionindex = PJjmdindex
        tableJMDconclusionindex = tableindex  # 精密度结论表格索引,不管几个化合物，最终结论都只有一个表格

        if PNjmd_data["JMD_dict"] and PJjmd_data["JMD_dict"]:
            jmdconclusion_data = jmd.related_jmdendconclusion(id)
           
            if jmdconclusion_data:
                JMDconclusionindex += 1  # 精密度结论副标题索引+1 -- 6.3
                tableindex += 1

        if PNjmd_data["JMD_dict"] or PJjmd_data["JMD_dict"]:  # 如果有重复性精密度和中间精密度,总标题索引+1
            titleindex += 1 # -- 7

        print("精密度 tableindex:%s" % (tableindex))
        print("精密度 titleindex:%s" % (titleindex))

        # --------------------------------------- 正确度（每个化合物一个表格）---------------------------------------

        ZQDindex = titleindex # 正确度主标题索引 

        # 1  PT
        PTindex = 0  # PT副标题索引  7.1

        tablePTindex_start = tableindex # 第一个化合物表格索引
        tablePTindex_end = tableindex+Number_of_compounds-1 # 最后一个化合物的表格索引

        PT_data = zqd.related_PT(id)
        if PT_data["PT_dict"]:
            PTindex += 1 # # 正确度副标题索引+1  7.2
            tableindex += Number_of_compounds # 总表格索引+n

        # 2 加标回收率
        Recycleindex = PTindex # --7.1

        tableRecycleindex_start = tableindex
        tableRecycleindex_end = tableindex+Number_of_compounds-1

        Recycle_data = zqd.related_recycle(id)
        if Recycle_data:
            Recycleindex += 1 # --7.2
            tableindex += Number_of_compounds

        # 3 仪器比对
        InstrumentCompareindex = Recycleindex

        # 仪器比对描述性文字
        InstrumentCompare_data = InstrumentCompare.objects.filter(reportinfo_id=id)
        InstrumentCompare_text = []
        for i in InstrumentCompare_data:
            InstrumentCompare_text.append(i.textarea)
        
        if InstrumentCompare_data:
            InstrumentCompareindex += 1

        if PT_data["PT_dict"] or Recycle_data:
            titleindex += 1  # 8

        print("正确度 tableindex:%s" % (tableindex))
        print("正确度 titleindex:%s" % (titleindex))

        # --------------------------------------- AMR（每个化合物一个表格）---------------------------------------
        
        AMRindex = titleindex  # AMR主标题索引

        # 1 LOQ
        LOQindex = 0
        pictureindex = 1  # 总图片索引
        tableLOQindex_start = tableindex
        tableLOQindex_end = tableindex+Number_of_compounds-1
        pictureLOQindex_start = pictureindex
        pictureLOQindex_end = pictureindex+Number_of_compounds-1

        LOQ_data = amr.related_AMR(id, unit)
        # 有数据和图片,同时增加表格和图片索引
        if LOQ_data["AMR_dict"] and LOQ_data["objs"]:
            LOQindex += 1
            pictureindex += Number_of_compounds  # 总图片索引
            tableindex += Number_of_compounds

        # 没有图片,不增加图片索引
        elif LOQ_data["AMR_dict"]:
            LOQindex += 1
            tableindex += Number_of_compounds
        
        else:
            pass

        # 2 LOD
        LODindex = AMRindex
        tableLODindex = tableindex
        pictureLODindex_start = pictureindex
        pictureLODindex_end = pictureindex+Number_of_compounds-1

        LOD_data = amr.related_LOD(id)
        if LOD_data:
            LODindex += 1
            pictureindex += Number_of_compounds

        # 3 AMRconclusion
        AMRconclusionindex = LODindex
        tableAMRconclusionindex = tableindex

        AMRconclusion_data = amr.related_AMRconclusion(id)
        if AMRconclusion_data["AMRconclusion_dict"]:
            AMRconclusionindex += 1
            tableindex += 1

        if LOQ_data["AMR_dict"] or LOD_data:
            titleindex += 1

        print("AMR tableindex:%s" % (tableindex))
        print("AMR titleindex:%s" % (titleindex))
            
        # --------------------------------------- 稀释倍数（每个化合物一个表格）---------------------------------------
        CRRindex = titleindex # CRR主标题索引

        Dilution_data = crr.related_CRR(id, unit)
        # 1 进行稀释倍数验证  
        if not Dilution_data["CRR2_True"]:    
            Dilutionindex = 0

            tableDilutionindex_start = tableindex
            tableDilutionindex_end = tableindex+Number_of_compounds-1
       
            if Dilution_data["CRR_dict"]:
                Dilutionindex += 1
                titleindex += 1

                # 多指标项目，稀释倍数结论需要单独占一个表格
                tableindex += Number_of_compounds+1

            print("CRR tableindex:%s" % (tableindex))
            print("CRR titleindex:%s" % (titleindex))
        
        else:
            Dilutionindex = 0
            tableDilutionindex = tableindex
            if Dilution_data["CRR_dict"]:
                Dilutionindex += 1
                titleindex += 1

                # 多指标项目，稀释倍数结论需要单独占一个表格
                tableindex += 1

            print("CRR tableindex:%s" % (tableindex))
            print("CRR titleindex:%s" % (titleindex))


        # ---------------------------------------------- 基质特异性 --------------------------------------------------
        MSindex = titleindex
        pictureMSindex_start = pictureindex
        pictureMSindex_end = pictureindex+2  # 固定三种图(标准品，血清样本，空白基质)
        resultMS = ms.related_MS(id)
        if resultMS:
            titleindex += 1

        # --------------------------------------- 基质效应（每个化合物一个表格）---------------------------------------
        Matrix_effectindex = titleindex # 基质效应主标题索引

        tableMatrix_effectindex_start = tableindex
        tableMatrix_effectindex_end = tableindex+Number_of_compounds-1

        Matrix_effect_data = Matrix_effect.related_Matrix_effect(id)
        if Matrix_effect_data["Matrixeffect_dict"]:
            titleindex += 1
            tableindex += Number_of_compounds

        # --------------------------------------- 携带效应 ---------------------------------------
        Carryoverindex = titleindex # 携带效应主标题索引

        tableCarryoverindex = tableindex

        Carryover_data = Carry_over.related_Carryover(id)
        if Carryover_data["Carryover_dict"]:
            titleindex += 1
            tableindex += 1

        # --------------------------------------- 样品稳定性 ---------------------------------------
        # 1 数据抓取与参数设置
        Stability_data = Sample_Stability.data_scrap(id)  # 抓取数据库中的数据
        Stabilityindex = titleindex  # 设置标题索引
        tableStabilityindex_start = tableindex  # 设置第一个表格索引
        tableStabilityindex_end = tableindex+Number_of_compounds*3-1

        # 2 如果存在数据，自增标题索引和表格索引
        if Stability_data["Room_conclevel_list"]:
            titleindex += 1
            tableindex += Number_of_compounds*2-1

        # --------------------------------------- 参考区间 ---------------------------------------
        # 1 数据抓取与参数设置
        Reference_Interval_data = Sample_ReferenceInterval.data_scrap(id)  # 抓取数据库中的数据
        Reference_Interval_index = titleindex  # 设置标题索引
        table_Reference_Interval_index_start = tableindex+1  # 设置第一个表格索引,参考区间在一个表格中显示
        # table_Reference_Interval_index_end = tableindex+Number_of_compounds*2-1 # 设置最后一个表格索引索引

        # 2 如果存在数据，自增标题索引和表格索引
        if Reference_Interval_data["Referenceinterval_dict"]:
            titleindex += 1
            tableindex += 1

        # --------------------------------------- 检测方法，设备，试剂耗材，样品处理，最终结论 ---------------------------------------
        Test_method_data = others.related_testmethod(id)
        Equipment_data = others.related_equipment(id)
        Reagents_Consumables_data = others.related_Reagents_Consumables(id)
        Sample_Preparation_data = others.related_Sample_Preparation(id)
        
        Endconclusion = "由以上各参数验证可知，本方法的分析灵敏度、分析测量范围、基质特异性、基质效应、临床可报告范围（稀释倍数）、精密度（重复性精密度和中间精密度）、正确度（PT，加标回收率）、携带效应均满足临床开展要求，本方法可以在FXS-YZ26（Thermo TSQ Altis LC-MS/MS）仪器上进行血清雌二醇、雌酮项目临床样本的日常检测。"

        Endconclusion = Endconclusion.replace('FXS-YZ26', Instrument_number)
        Endconclusion = Endconclusion.replace('Thermo TSQ Altis LC-MS/MS', Instrument_model)
        Endconclusion = Endconclusion.replace('血清雌二醇、雌酮', project)

        if not LOQ_data["AMR_dict"]:      
            Endconclusion = Endconclusion.replace('分析灵敏度、分析测量范围、', '')

        if not resultMS:
            Endconclusion = Endconclusion.replace('基质特异性、', '')

        if not Matrix_effect_data["Matrixeffect_dict"]:
            Endconclusion = Endconclusion.replace('基质效应、', '')

        if not Dilution_data["CRR_dict"]:
            Endconclusion = Endconclusion.replace('临床可报告范围（稀释倍数）、', '')

        # 精密度
        if not PNjmd_data["JMD_dict"] and not PJjmd_data["JMD_dict"]:
            Endconclusion = Endconclusion.replace('精密度（重复性精密度和中间精密度）、', '')

        if not PNjmd_data["JMD_dict"]:
            Endconclusion = Endconclusion.replace('重复性精密度和', '')

        if not PJjmd_data["JMD_dict"]:
            Endconclusion = Endconclusion.replace('和中间精密度', '')

        # 正确度
        if not PT_data["PT_dict"] and not Recycle_data:
            Endconclusion = Endconclusion.replace('正确度（PT，加标回收率）、', '')

        if not PT_data["PT_dict"]:
            Endconclusion = Endconclusion.replace('PT，', '')

        if not Recycle_data:
            Endconclusion = Endconclusion.replace('，加标回收率', '')

        if not Carryover_data["Carryover_dict"]:
            Endconclusion = Endconclusion.replace('、携带效应', '')

        if not Stability_data["Room_conclevel_list"]:
            Endconclusion = Endconclusion.replace('样品稳定性（样本储存稳定性和样本处理后稳定性）、', '')

        if not Reference_Interval_data["Referenceinterval_dict"]:
            Endconclusion = Endconclusion.replace('、参考区间', '')


        return render(request, 'report/reportpreview-multiple.html', locals())

# 在报告生成界面点击删除时跳转的界面
def get_reportdelete_page(request, id):
    # 从数据库中抓取当前用户名传递到layout.html
    try:
        name = User.objects.get(username=request.user).first_name
    except:
        name = "未注册用户"

    # 判断是否为未登录用户
    if isinstance(request.user, auth.models.AnonymousUser):  
        User_class = 0
    else:
        User_class = 1

    # 基本参数，此处由于在验证界面提交数据时已经进行了判断，因此在使用get()方法时不需要try
    Instrument_number = ReportInfo.objects.get(id=id).number  # 仪器编号
    Detectionplatform = ReportInfo.objects.get(id=id).Detectionplatform  # 检测平台
    project = ReportInfo.objects.get(id=id).project  # 检测项目
    platform = ReportInfo.objects.get(id=id).platform  # 仪器项目
    manufacturers = ReportInfo.objects.get(id=id).manufacturers # 仪器厂家

    # project为必设置项,因此此部分不需要try
    special_id = Special.objects.get(project=project).id  # 找到特殊参数设置里对应的项目
    chinese_title = Special.objects.get(project=project).chinese_titie  # 中文标题
    english_title = Special.objects.get(project=project).english_titie  # 英文标题
    unit = Special.objects.get(project=project).unit  # 单位
    digits = Special.objects.get(project=project).Effective_digits  # 有效位数
    Number_of_compounds = int(Special.objects.get(project=project).Number_of_compounds)  # 化合物个数

    # 检测方法里找到仪器型号和色谱柱。可能存在用户忘记设置的情况，因此需要try
    try:
        Instrument_model = Testmethod.objects.get(platform=platform, factory=manufacturers, project=project).Instrument_model  # 仪器型号
    except:
        Instrument_model = "未设置仪器型号"
    
    try:
        Column = Testmethod.objects.get(platform=platform, factory=manufacturers, project=project).column  # 色谱柱
    except:
        Column = "未设置色谱柱"

    # Protocol_ID可由英文标题和验证时间推算出来
    if "by" in english_title and str(ReportInfo.objects.get(id=id).verifytime) != "":
        Protocol_ID = english_title.split("by")[1] + str(ReportInfo.objects.get(id=id).verifytime)[0:4] + str(ReportInfo.objects.get(id=id).verifytime)[5:7]   # Protocol ID
    else:
        Protocol_ID = "英文标题格式不对,需含有'by'关键词!!!"

    # 判断是否单独为某个化合物设置了单位 unit = {"化合物1":"单位1","化合物2":"单位6"}、
    UNIT_TABLE = Special.objects.get(project=project)
    pt_special = PTspecial.objects.get(special=UNIT_TABLE)
    pt_accept = PTspecialaccept.objects.filter(pTspecial=pt_special)
    Unitlist = []  # 每个化合物单位列表
    Unitdict = {}  # 每个化合物单位字典

    for i in pt_accept:
        Unitlist.append(i.unit)

    if Unitlist == [] or Unitlist[0] == "":  # 如果全部没设置或者只是单位没设置
        pass
    else:
        for i in pt_accept:
            Unitdict[i.norm] = i.unit


    if Number_of_compounds == 1:  # 单个化合物
        # 验证原因
        data_Validation_Reason = Validation_Reason.objects.filter(reportinfo_id=id) 
        text_Validation_Reason = []
        for i in data_Validation_Reason:
            text_Validation_Reason.append(i.reason)

        titleindex = 6  # 总标题索引从6开始  -- 6
        tableindex = 3  # 总表格索引从3开始。表1质谱参数，表2液相梯度条件

        # ---------------------------------------精密度（每个化合物一个表格）---------------------------------------
        JMDindex = titleindex  # 精密度主标题索引 6

        # 1 重复性精密度数据
        PNjmdindex = 0  # 重复性精密度副标题索引   6.1

        tablePNindex = tableindex # 重复性精密度表格索引  表3

        PNjmd_data = jmd.related_PNjmd(id)
        if PNjmd_data:
            if PNjmd_data["JMD_dict"]:
                PNjmdindex += 1  # 重复性精密度副标题索引+1  6.2
                tableindex += Number_of_compounds  # 总表格索引+n，以两个化合物为例，开始是表3，现在是表5   表5

        # 2 中间精密度数据
        PJjmdindex = PNjmdindex  # 重复性精密度副标题索引赋值给中间精密度副标题索引

        tablePJindex = tableindex

        PJjmd_data = jmd.related_PJjmd(id)   
        if PJjmd_data:
            if PJjmd_data["JMD_dict"]:
                PJjmdindex += 1  # 中间精密度副标题索引+1
                tableindex += Number_of_compounds 

        # 3 精密度结论
        JMDconclusionindex = PJjmdindex
        tableJMDconclusionindex = tableindex

        if PNjmd_data and PJjmd_data:
            if PNjmd_data["JMD_dict"] and PJjmd_data["JMD_dict"]:
                jmdconclusion_data = jmd.related_jmdendconclusion(id)
            
                if jmdconclusion_data:
                    JMDconclusionindex += 1  # 精密度结论副标题索引+1 -- 6.3
                    tableindex += 1

        if PNjmd_data["JMD_dict"] or PJjmd_data["JMD_dict"]:  # 如果有重复性精密度和中间精密度,总标题索引+1
            titleindex += 1 # -- 7

        # --------------------------------------- 正确度（每个化合物一个表格）---------------------------------------

        ZQDindex = titleindex # 正确度主标题索引 

        # 1  PT
        PTindex = 0  # PT副标题索引  7.1

        tablePTindex = tableindex

        PT_data = zqd.related_PT(id)
        if PT_data["PT_dict"]:
            PTindex += 1 # # 正确度副标题索引+1  7.2
            tableindex += Number_of_compounds

        # 2 加标回收率
        Recycleindex = PTindex # --7.1

        tableRecycleindex_start = tableindex
        tableRecycleindex_end = tableindex+Number_of_compounds-1

        Recycle_data = zqd.related_recycle(id)
        if Recycle_data:
            Recycleindex += 1 # --7.2
            tableindex += Number_of_compounds

        if PT_data["PT_dict"] or Recycle_data:
            titleindex += 1  # 8

        # --------------------------------------- AMR（每个化合物一个表格）---------------------------------------
        
        AMRindex = titleindex  # AMR主标题索引

        # 1 LOQ
        LOQindex = 0
        pictureindex = 1  # 总图片索引
        tableLOQindex = tableindex
        pictureLOQindex_start = pictureindex
        pictureLOQindex_end = pictureindex+Number_of_compounds-1

        LOQ_data = amr.related_AMR(id, unit)
        # 有数据和图片,同时增加表格和图片索引
        if LOQ_data["AMR_dict"] and LOQ_data["objs"]:
            LOQindex += 1
            pictureindex += Number_of_compounds  # 总图片索引
            tableindex += Number_of_compounds

        # 没有图片,不增加图片索引
        elif LOQ_data["AMR_dict"]:
            LOQindex += 1
            tableindex += Number_of_compounds
        
        else:
            pass

        # 2 LOD
        LODindex = AMRindex
        tableLODindex = tableindex
        pictureLODindex_start = pictureindex
        pictureLODindex_end = pictureindex+Number_of_compounds-1

        LOD_data = amr.related_LOD(id)
        if LOD_data:
            LODindex += 1
            pictureindex += Number_of_compounds

        # 3 AMRconclusion
        AMRconclusionindex = LODindex
        tableAMRconclusionindex = tableindex

        AMRconclusion_data = amr.related_AMRconclusion(id)
        if AMRconclusion_data:
            AMRconclusionindex += 1
            tableindex += 1

        if LOQ_data["AMR_dict"] or LOD_data:
            titleindex += 1

        # --------------------------------------- 稀释倍数（每个化合物一个表格）---------------------------------------
        CRRindex = titleindex # CRR主标题索引

        # 1 进行稀释倍数验证      
        CRR2_True = 1
        Dilutionindex = 0

        tableDilutionindex = tableindex

        Dilution_data = crr.related_CRR(id,unit)
        if Dilution_data["CRR_dict"]:
            Dilutionindex += 1
            titleindex += 1
            tableindex += 1

        # ---------------------------------------------- 基质特异性 --------------------------------------------------
        MSindex = titleindex
        pictureMSindex_start = pictureindex
        pictureMSindex_end = pictureindex+2  # 固定三种图(标准品，血清样本，空白基质)
        resultMS = ms.related_MS(id)
        if resultMS:
            titleindex += 1

        # --------------------------------------- 基质效应（每个化合物一个表格）---------------------------------------
        Matrix_effectindex = titleindex # 基质效应主标题索引

        tableMatrix_effectindex = tableindex

        Matrix_effect_data = Matrix_effect.related_Matrix_effect(id)
        if Matrix_effect_data["Matrixeffect_dict"]:
            titleindex += 1
            tableindex += 1

        # --------------------------------------- 携带效应 ---------------------------------------
        Carryoverindex = titleindex # 携带效应主标题索引

        tableCarryoverindex = tableindex

        Carryover_data = Carry_over.related_Carryover(id)
        if Carryover_data:
            titleindex += 1
            tableindex += 1

        # --------------------------------------- 检测方法，设备，试剂耗材，样品处理，最终结论 ---------------------------------------
        Test_method_data = others.related_testmethod(id)
        Equipment_data = others.related_equipment(id)
        Reagents_Consumables_data = others.related_Reagents_Consumables(id)
        Sample_Preparation_data = others.related_Sample_Preparation(id)
        
        Endconclusion = "由以上各参数验证可知，本方法的分析灵敏度、分析测量范围、基质特异性、基质效应、临床可报告范围（稀释倍数）、精密度（重复性精密度和中间精密度）、正确度（PT，加标回收率）、携带效应、样品稳定性（样本储存稳定性和样本处理后稳定性）、参考区间均满足临床开展要求，本方法可以在FXS-YZ26（Thermo TSQ Altis LC-MS/MS）仪器上进行血清雌二醇、雌酮项目临床样本的日常检测。"

        Endconclusion = Endconclusion.replace('FXS-YZ26', Instrument_number)
        Endconclusion = Endconclusion.replace('Thermo TSQ Altis LC-MS/MS', Instrument_model)
        Endconclusion = Endconclusion.replace('血清雌二醇、雌酮', project)

        if not LOQ_data["AMR_dict"]:      
            Endconclusion = Endconclusion.replace('分析灵敏度、分析测量范围、', '')

        if not resultMS:
            Endconclusion = Endconclusion.replace('基质特异性、', '')

        if not Matrix_effect_data["Matrixeffect_dict"]:
            Endconclusion = Endconclusion.replace('基质效应、', '')

        if not Dilution_data["CRR_dict"]:
            Endconclusion = Endconclusion.replace('临床可报告范围（稀释倍数）、', '')

        # 精密度
        if not PNjmd_data["JMD_dict"] and not PJjmd_data["JMD_dict"]:
            Endconclusion = Endconclusion.replace('精密度（重复性精密度和中间精密度）、', '')

        if not PNjmd_data["JMD_dict"]:
            Endconclusion = Endconclusion.replace('重复性精密度和', '')

        if not PJjmd_data["JMD_dict"]:
            Endconclusion = Endconclusion.replace('和中间精密度', '')

        # 正确度
        if not PT_data["PT_dict"] and not Recycle_data:
            Endconclusion = Endconclusion.replace('正确度（PT，加标回收率）、', '')

        if not Carryover_data["Carryover_dict"]:
            Endconclusion = Endconclusion.replace('携带效应、', '')

        # if not Stability_data["Room_conclevel_list"]:
        #     Endconclusion = Endconclusion.replace('样品稳定性（样本储存稳定性和样本处理后稳定性）、', '')

        # if not Reference_Interval_data["Referenceinterval_dict"]:
        #     Endconclusion = Endconclusion.replace('、参考区间', '')

        return render(request, 'report/reportdelete_single.html', locals())

    else:  # 多个化合物
        # 验证原因
        data_Validation_Reason = Validation_Reason.objects.filter(reportinfo_id=id) 
        text_Validation_Reason = []
        for i in data_Validation_Reason:
            text_Validation_Reason.append(i.reason)

        titleindex = 6  # 总标题索引从6开始  -- 6
        tableindex = 3  # 总表格索引从3开始。表1质谱参数，表2液相梯度条件

        # ---------------------------------------精密度（每个化合物一个表格）---------------------------------------
        JMDindex = titleindex  # 精密度主标题索引 6

        # 1  重复性精密度数据
        PNjmdindex = 0  # 重复性精密度副标题索引   6.1

        tablePNindex_start = tableindex # 第一个化合物的表格索引  表3
        tablePNindex_end = tableindex+Number_of_compounds-1 # 最后一个化合物的表格索引  以3个化合物为例，表3+3-1=5

        PNjmd_data = jmd.related_PNjmd(id)
        if PNjmd_data["JMD_dict"]:
            print("重复性精密度存在")
            PNjmdindex += 1  # 重复性精密度副标题索引+1  6.2
            tableindex += Number_of_compounds  # 总表格索引+n，以两个化合物为例，开始是表3，现在是表5   表5

        # 2 中间精密度数据
        PJjmdindex = PNjmdindex  # 中间精密度副标题索引

        tablePJindex_start = tableindex
        tablePJindex_end = tableindex+Number_of_compounds-1

        PJjmd_data = jmd.related_PJjmd(id)
        if PJjmd_data["JMD_dict"]:
            print("中间精密度存在")
            PJjmdindex += 1  # 中间精密度副标题索引+1  -- 6.2
            tableindex += Number_of_compounds  # 总表格索引+n

        # 3 精密度结论数据
        JMDconclusionindex = PJjmdindex
        tableJMDconclusionindex = tableindex  # 精密度结论表格索引,不管几个化合物，最终结论都只有一个表格

        if PNjmd_data["JMD_dict"] and PJjmd_data["JMD_dict"]:
            jmdconclusion_data = jmd.related_jmdendconclusion(id)
           
            if jmdconclusion_data:
                JMDconclusionindex += 1  # 精密度结论副标题索引+1 -- 6.3
                tableindex += 1

        if PNjmd_data["JMD_dict"] or PJjmd_data["JMD_dict"]:  # 如果有重复性精密度和中间精密度,总标题索引+1
            titleindex += 1 # -- 7

        # --------------------------------------- 正确度（每个化合物一个表格）---------------------------------------

        ZQDindex = titleindex # 正确度主标题索引 

        # 1  PT
        PTindex = 0  # PT副标题索引  7.1

        tablePTindex_start = tableindex # 第一个化合物表格索引
        tablePTindex_end = tableindex+Number_of_compounds-1 # 最后一个化合物的表格索引

        PT_data = zqd.related_PT(id)
        if PT_data["PT_dict"]:
            PTindex += 1 # # 正确度副标题索引+1  7.2
            tableindex += Number_of_compounds # 总表格索引+n

        # 2 加标回收率
        Recycleindex = PTindex # --7.1

        tableRecycleindex_start = tableindex
        tableRecycleindex_end = tableindex+Number_of_compounds-1

        Recycle_data = zqd.related_recycle(id)
        if Recycle_data:
            Recycleindex += 1 # --7.2
            tableindex += Number_of_compounds

        if PT_data["PT_dict"] or Recycle_data:
            titleindex += 1  # 8

        # --------------------------------------- 3 AMR（每个化合物一个表格）---------------------------------------
        
        AMRindex = titleindex  # AMR主标题索引

        print("titleindex:%s" % (titleindex))

        # 1 LOQ
        LOQindex = 0
        pictureindex = 1  # 总图片索引
        tableLOQindex_start = tableindex
        tableLOQindex_end = tableindex+Number_of_compounds-1
        pictureLOQindex_start = pictureindex
        pictureLOQindex_end = pictureindex+Number_of_compounds*2-1

        LOQ_data = amr.related_AMR(id, unit)
        if LOQ_data["AMR_dict"]:
            LOQindex += 1
            pictureindex += Number_of_compounds*2  # 总图片索引
            tableindex += Number_of_compounds

        # 2 LOD
        LODindex = AMRindex
        tableLODindex = tableindex
        pictureLODindex_start = pictureindex
        pictureLODindex_end = pictureindex+Number_of_compounds-1

        LOD_data = amr.related_LOD(id)
        if LOD_data:
            LODindex += 1
            pictureindex += Number_of_compounds

        # 3 AMRconclusion
        AMRconclusionindex = LODindex
        tableAMRconclusionindex = tableindex

        AMRconclusion_data = amr.related_AMRconclusion(id)
        if AMRconclusion_data:
            AMRconclusionindex += 1
            tableindex += 1

        if LOQ_data["AMR_dict"] or LOD_data:
            titleindex += 1


        # --------------------------------------- 稀释倍数（每个化合物一个表格）---------------------------------------
        CRRindex = titleindex # CRR主标题索引
    
        # 1 进行稀释倍数验证      
        CRR2_True = 1
        Dilutionindex = 0

        tableDilutionindex_start = tableindex
        tableDilutionindex_end = tableindex+Number_of_compounds-1

        Dilution_data = crr.related_CRR(id,unit)
        if Dilution_data:
            Dilutionindex += 1
            titleindex += 1
            tableindex += Number_of_compounds

         # ---------------------------------------------- 基质特异性 --------------------------------------------------
        MSindex = titleindex
        pictureMSindex_start = pictureindex
        pictureMSindex_end = pictureindex+2  # 固定三种图(标准品，血清样本，空白基质)
        resultMS = ms.related_MS(id)
        if resultMS:
            titleindex += 1

        # --------------------------------------- 基质效应（每个化合物一个表格）---------------------------------------
        Matrix_effectindex = titleindex # 基质效应主标题索引

        tableMatrix_effectindex_start = tableindex
        tableMatrix_effectindex_end = tableindex+Number_of_compounds-1

        Matrix_effect_data = Matrix_effect.related_Matrix_effect(id)
        if Matrix_effect_data["Matrixeffect_dict"]:
            titleindex += 1
            tableindex += Number_of_compounds

        # ---------------------------------------------携带效应---------------------------------------------------------
        Carryoverindex = titleindex # 基质效应主标题索引

        tableCarryoverindex_start = tableindex
        tableCarryoverindex_end = tableindex+Number_of_compounds//7

        Carryover_data = Carry_over.related_Carryover(id)
        if Carryover_data:
            titleindex += 1
            tableindex += 1

        # --------------------------------------- 检测方法，设备，试剂耗材，样品处理，最终结论 ---------------------------------------
        Test_method_data = others.related_testmethod(id)
        Equipment_data = others.related_equipment(id)
        Reagents_Consumables_data = others.related_Reagents_Consumables(id)
        Sample_Preparation_data = others.related_Sample_Preparation(id)
        
        Endconclusion = "由以上各参数验证可知，本方法的分析灵敏度、分析测量范围、基质特异性、基质效应、临床可报告范围（稀释倍数）、精密度（重复性精密度和中间精密度）、正确度（PT，加标回收率）、携带效应、样品稳定性（样本储存稳定性和样本处理后稳定性）、参考区间均满足临床开展要求，本方法可以在FXS-YZ26（Thermo TSQ Altis LC-MS/MS）仪器上进行血清雌二醇、雌酮项目临床样本的日常检测。"

        Endconclusion = Endconclusion.replace('FXS-YZ26', Instrument_number)
        Endconclusion = Endconclusion.replace('Thermo TSQ Altis LC-MS/MS', Instrument_model)
        Endconclusion = Endconclusion.replace('血清雌二醇、雌酮', project)

        if not LOQ_data["AMR_dict"]:      
            Endconclusion = Endconclusion.replace('分析灵敏度、分析测量范围、', '')

        if not resultMS:
            Endconclusion = Endconclusion.replace('基质特异性、', '')

        if not Matrix_effect_data["Matrixeffect_dict"]:
            Endconclusion = Endconclusion.replace('基质效应、', '')

        if not Dilution_data["CRR_dict"]:
            Endconclusion = Endconclusion.replace('临床可报告范围（稀释倍数）、', '')

        # 精密度
        if not PNjmd_data["JMD_dict"] and not PJjmd_data["JMD_dict"]:
            Endconclusion = Endconclusion.replace('精密度（重复性精密度和中间精密度）、', '')

        if not PNjmd_data["JMD_dict"]:
            Endconclusion = Endconclusion.replace('重复性精密度和', '')

        if not PJjmd_data["JMD_dict"]:
            Endconclusion = Endconclusion.replace('和中间精密度', '')

        # 正确度
        if not PT_data["PT_dict"] and not Recycle_data:
            Endconclusion = Endconclusion.replace('正确度（PT，加标回收率）、', '')

        if not Carryover_data["Carryover_dict"]:
            Endconclusion = Endconclusion.replace('携带效应、', '')

        # if not Stability_data["Room_conclevel_list"]:
        #     Endconclusion = Endconclusion.replace('样品稳定性（样本储存稳定性和样本处理后稳定性）、', '')

        # if not Reference_Interval_data["Referenceinterval_dict"]:
        #     Endconclusion = Endconclusion.replace('、参考区间', '')

    
        return render(request, 'report/reportdelete_mutiple.html', locals())

# 在删除界面勾选删除选项(删除整份报告或删除一个或多个验证指标)后返回的界面，也是报告生成界面
def get_reportdeleteselect_page(request):
    name = User.objects.get(username=request.user).first_name
    if isinstance(request.user, auth.models.AnonymousUser):  # 判断是否为未登录用户
        User_class = 0
    else:
        User_class = 1
    if request.method == 'POST':
        id = int(request.POST.getlist("id")[0])
        quotalist = request.POST.getlist("quota")
        print(quotalist)

        if 'all' not in quotalist:
            if '重复性精密度' in quotalist:
                JMD.objects.filter(reportinfo_id=id, namejmd='重复性精密度').delete()

            if '中间精密度' in quotalist:
                JMD.objects.filter(reportinfo_id=id, namejmd='中间精密度').delete()

            if 'PT' in quotalist:
                PT.objects.filter(reportinfo_id=id).delete()

            if '加标回收率' in quotalist:
                RECYCLE.objects.filter(reportinfo_id=id).delete()

            if '仪器比对' in quotalist:
                InstrumentCompare.objects.filter(reportinfo_id=id).delete()

            if '方法定量限与线性范围' in quotalist:
                AMR.objects.filter(reportinfo_id=id).delete()
                AMRpicture.objects.filter(reportinfo_id=id).delete()

            if '方法检出限' in quotalist:
                LOD.objects.filter(reportinfo_id=id).delete()
                LODpicture.objects.filter(reportinfo_id=id).delete()

            if 'AMR最终结论' in quotalist:
                AMRconsluion.objects.filter(reportinfo_id=id).delete()

            if '稀释倍数' in quotalist:
                CRR.objects.filter(reportinfo_id=id).delete()
                CRR2.objects.filter(reportinfo_id=id).delete()

            if '基质特异性' in quotalist:
                MS.objects.filter(reportinfo_id=id).delete()

            if '基质效应' in quotalist:
                Matrixeffect.objects.filter(reportinfo_id=id).delete()

            if '携带效应' in quotalist:
                Carryover.objects.filter(reportinfo_id=id).delete()
                Carryover2.objects.filter(reportinfo_id=id).delete()

        else:
            report = ReportInfo.objects.filter(id=id)
            report.delete()

        data = ReportInfo.objects.all()
        return render(request, 'report/generation.html', {"data": data})

# 在报告生成界面点击继续验证时跳转的界面
def get_verifyagain_page(request, id):
    name = User.objects.get(username=request.user).first_name
    if isinstance(request.user, auth.models.AnonymousUser):  # 判断是否为未登录用户
        User_class = 0
    else:
        User_class = 1

    instrument_num_verifyagain = ReportInfo.objects.get(id=id).number
    Detectionplatform_verifyagain = ReportInfo.objects.get(id=id).Detectionplatform  # 找到项目组
    project_verifyagain = ReportInfo.objects.get(id=id).project  # 找到项目
    platform_verifyagain = ReportInfo.objects.get(id=id).platform
    manufacturers_verifyagain = ReportInfo.objects.get(id=id).manufacturers
    verifyoccasion_verifyagain = ReportInfo.objects.get(id=id).verifyoccasion
    return render(request, 'report/verification.html', locals())

# PT数据保存
def PTsave(request):

    # 从数据库中抓取当前用户名传递到layout.html
    try:
        name = User.objects.get(username=request.user).first_name
    except:
        pass
    if isinstance(request.user, auth.models.AnonymousUser):  # 判断是否为未登录用户
        User_class = 0
    else:
        User_class = 1
    
    # 提取PT.html中的数据，并存入数据库
    if request.method == 'POST':
        print(request.POST)
        '''
        <QueryDict: {'Result': ["{'25OHD2': [['PT561', 3.06, '± 25.0 %'], ['PT562', 1.13, '± 25.0 %'], ['PT563', 1.58, '± 25.0 %'], 
        ['PT564', 1.15, '± 25.0 %'], ['PT565', 22.96, '± 25.0 %']], '25OHD3': [['PT561', 68.45, '± 25.0 %'], ['PT562', 46.59, '± 25.0 %'],
        ['PT563', 91.69, '± 25.0 %'], ['PT564', 43.03, '± 25.0 %'], ['PT565', 59.44, '± 25.0 %']]}"], 'instrument': ['123'], 
        'project': ['25OHD'], 'PT_num': ['5'], 'PTtarget1': ['3', '68'], 'bias1': ['2.00%', '0.66%'], 'pass1': ['通过', '通过'], 
        'PTtarget2': ['1.1', '47'], 'bias2': ['2.73%', '0.87%'], 'pass2': ['通过', '通过'], 'PTtarget3': ['1.6', '92'], 
        'bias3': ['1.25%', '0.34%'], 'pass3': ['通过', '通过'], 'PTtarget4': ['1.2', '43'], 'bias4': ['4.17%', '0.07%'], 
        'pass4': ['通过', '通过'], 'PTtarget5': ['23', '60'], 'bias5': ['0.17%', '0.93%'], 'pass5': ['通过', '通过']}>
        '''

        # 1 基本信息提取
        instrument_num = request.POST["instrument_num"]
        Detectionplatform = request.POST["Detectionplatform"]  # 项目组
        project = request.POST["project"]  # 项目
        platform = request.POST["platform"]  # 仪器平台(液质,液相,ICP-MS...)
        manufacturers = request.POST["manufacturers"]  # 仪器厂家(AB,Agilent...)
        verifyoccasion = request.POST["verifyoccasion"]  # 验证时机

        # 2 模板信息提取
        templates = request.POST["templates"]  # 模板

        # 3 数据抓取
        if templates=="1":
            PT_dict = eval(str(request.POST.getlist("PT_dict")[0]))
            lowaccept = []  # 可接受区间下限列表
            upaccept = []  # 可接受区间上限列表
            PTpass = []  # 是否通过列表
            PT_num = int(request.POST.getlist("PT_num")[0])  # PT样本数

            for i in range(1, PT_num+1):
                string_lowaccept = "lowaccept"+str(i)
                string_upaccept = "upaccept"+str(i)
                string_pass = "pass"+str(i)
                lowaccept.append(request.POST.getlist(string_lowaccept))
                upaccept.append(request.POST.getlist(string_upaccept))
                PTpass.append(request.POST.getlist(string_pass))

            PT_norm = []  # 待测物质列表
            for i in PT_dict.keys():
                PT_norm.append(i)

            PT_judgenum = 0
            for i in range(PT_num):
                for j in range(len(PT_norm)):
                    PT_dict[PT_norm[j]][i].append(lowaccept[i][j])
                    PT_dict[PT_norm[j]][i].append(upaccept[i][j])
                    PT_dict[PT_norm[j]][i].append(PTpass[i][j])
                    if PTpass[i][j] == "不通过":
                        PT_judgenum += 1

            reportinfo = ReportInfo.objects.get(number=request.POST["instrument_num"], project=request.POST["project"])

            if PT_judgenum == 0:
                insert_list = []
                for i in PT_norm:
                    for j in range(len(PT_dict[i])):
                        insert_list.append(PT(reportinfo=reportinfo, norm=i, templates="1",Experimentnum=PT_dict[i][j][0], value=PT_dict[i][j][1],
                                            accept1=PT_dict[i][j][2], accept2=PT_dict[i][j][3], PT_pass=PT_dict[i][j][4], target="",received="",bias=""))

                PT.objects.bulk_create(insert_list)
                HttpResponse = "PT数据保存成功!"
                return render(request, 'report/Datasave.html', locals())

            else:
                HttpResponse = "PT验证结果中含有不通过数据,请核对后重新提交!"
                return render(request, 'report/Warning.html', locals())

        else:       
            PT_dict = eval(str(request.POST.getlist("PT_dict")[0]))

            PTtarget = []  # 靶值列表
            PTbias = []  # 偏移或绝对差值列表
            PTpass = []  # 是否通过列表
            PT_num = int(request.POST.getlist("PT_num")[0])  # PT样本数

            for i in range(1, PT_num+1):
                string_target = "PTtarget"+str(i)
                string_bias = "bias"+str(i)
                string_pass = "pass"+str(i)
                PTtarget.append(request.POST.getlist(string_target))
                PTbias.append(request.POST.getlist(string_bias))
                PTpass.append(request.POST.getlist(string_pass))

            PT_norm = []  # 待测物质列表
            for i in PT_dict.keys():
                PT_norm.append(i)

            PT_judgenum = 0
            for i in range(PT_num):
                for j in range(len(PT_norm)):
                    PT_dict[PT_norm[j]][i].append(PTtarget[i][j])
                    PT_dict[PT_norm[j]][i].append(PTbias[i][j])
                    PT_dict[PT_norm[j]][i].append(PTpass[i][j])
                    if PTpass[i][j] == "不通过":
                        PT_judgenum += 1

            reportinfo = ReportInfo.objects.get(number=request.POST["instrument_num"], project=request.POST["project"])

            print(PT_dict)

            if PT_judgenum == 0:
                # 判断是否为25-OH-D项目

                # 1 不是25-OH-D项目
                if project!="25OHD":
                    insert_list = []
                    for i in PT_norm:
                        for j in range(len(PT_dict[i])):
                            insert_list.append(PT(reportinfo=reportinfo, norm=i, templates="2",Experimentnum=PT_dict[i][j][0], value=PT_dict[i][j][1],
                                                target=PT_dict[i][j][3], received=PT_dict[i][j][2], bias=PT_dict[i][j][4], PT_pass=PT_dict[i][j][5],
                                                accept1="",accept2=""))

                    PT.objects.bulk_create(insert_list)

                # # 2 是25-OH-D项目
                else:
                    insert_list = []
                    for i in PT_norm:
                        for j in range(len(PT_dict[i])):
                        
                            # 2 只显示总D结果,D2和D3结果不显示
                            insert_list.append(PT(reportinfo=reportinfo, norm=i, templates="2",Experimentnum=PT_dict[i][j][0], 
                                                    value=PT_dict[i][j][1]+"-"+PT_dict[i][j][2]+"-"+PT_dict[i][j][3],target=PT_dict[i][j][5], received=PT_dict[i][j][4], bias=PT_dict[i][j][6], PT_pass=PT_dict[i][j][7],
                                                    accept1="",accept2=""))

                    PT.objects.bulk_create(insert_list)
                HttpResponse = "PT数据保存成功!"
                return render(request, 'report/Datasave.html', locals())

            else:
                HttpResponse = "PT验证结果中含有不通过数据,请核对后重新提交!"
                return render(request, 'report/Warning.html', locals())

def Recyclesave(request):

    # 从数据库中抓取当前用户名传递到layout.html
    try:
        name = User.objects.get(username=request.user).first_name
    except:
        pass
    if isinstance(request.user, auth.models.AnonymousUser):  # 判断是否为未登录用户
        User_class = 0
    else:
        User_class = 1

    # 提取Recycle.html中的数据，并存入数据库   
    if request.method == 'POST':
        print(request.POST)
        '''
        print(request.POST)
        <QueryDict: {'Recycle_enddict': ["{'EVE': {'Recycle-sam1': [0.48, 0.44, 0.46, 4.09, 3.83, 4.11, 17.48, 17.82, 18.54, 33.25, 34.69, 34.98], 
        'Recycle-sam2': [0.48, 0.46, 0.44, 3.97, 3.96, 4.32, 18.48, 18.5, 18.94, 35.56, 36.96, 36.02], 
        'Recycle-sam3': [0.47, 0.43, 0.47, 4.19, 4.05, 4.28, 19.21, 18.46, 18.42, 36.05, 37.34, 36.32]}}"], 
        'instrument': ['123'], 'project': ['EVE'], 'verifyoccasion': ['新项目开发'], 'theoryconc1': ['25.00', '50.00', '100.00'], 
        'endlowrecycle1': ['14.52', '7.02', '3.73'], 'endlowrecycle2': ['13.48', '7.00', '3.59'], 'endlowrecycle3': ['14.60', '7.72', '3.82'], 
        'theoryconc2': ['37.50', '75.00', '166.67'], 'endmedianrecycle1': ['45.39', '24.03', '11.25'], 
        'endmedianrecycle2': ['46.29', '24.05', '10.80'], 'endmedianrecycle3': ['48.21', '24.64', '10.78'], 
        'theoryconc3': ['62.50', '125.00', '166.67'], 'endhighrecycle1': ['52.46', '28.08', '21.35'], 
        'endhighrecycle2': ['54.77', '29.20', '22.13'], 'endhighrecycle3': ['55.23', '28.45', '21.52']}>
        '''

        # 1 基本信息提取
        instrument_num = request.POST["instrument_num"]  # 仪器编号,strip()的作用是去除前后空格
        Detectionplatform = request.POST["Detectionplatform"]  # 项目组
        project = request.POST["project"]  # 项目
        platform = request.POST["platform"]  # 仪器平台(液质,液相,ICP-MS...)
        manufacturers = request.POST["manufacturers"]  # 仪器厂家(AB,Agilent...)
        verifyoccasion = request.POST["verifyoccasion"]  # 验证时机

        # 2 提取html中的数据
        Recycle_dict = eval(str(request.POST.getlist("Recycle_enddict_savedata")[0])) # 需要提取数据保存字典，而不是数据展示字典
        theoryconc1 = request.POST.getlist("theoryconc1")
        theoryconc2 = request.POST.getlist("theoryconc2")
        theoryconc3 = request.POST.getlist("theoryconc3")
        endlowrecycle1 = request.POST.getlist("endlowrecycle1")
        endlowrecycle2 = request.POST.getlist("endlowrecycle2")
        endlowrecycle3 = request.POST.getlist("endlowrecycle3")
        endlowrecycle = [endlowrecycle1, endlowrecycle2, endlowrecycle3]

        endmedianrecycle1 = request.POST.getlist("endmedianrecycle1")
        endmedianrecycle2 = request.POST.getlist("endmedianrecycle2")
        endmedianrecycle3 = request.POST.getlist("endmedianrecycle3")
        endmedianrecycle = [endmedianrecycle1,endmedianrecycle2, endmedianrecycle3]

        endhighrecycle1 = request.POST.getlist("endhighrecycle1")
        endhighrecycle2 = request.POST.getlist("endhighrecycle2")
        endhighrecycle3 = request.POST.getlist("endhighrecycle3")
        endhighrecycle = [endhighrecycle1, endhighrecycle2, endhighrecycle3]

        falsecounter = request.POST.getlist("falsecounter")[0]
        
        norm = []  # 化合物列表
        for key in Recycle_dict.keys():
            norm.append(key)

        samnum = []  # 本底个数列表
        for key, value in Recycle_dict.items():
            samnum.append(len(value))

        samname = ["RecB-1", "RecB-2", "RecB-3"]  # 本底后缀

        for i in range(len(norm)):
            norm_dict = Recycle_dict[norm[i]]
            for j in range(samnum[i]):  # 循环每个化合物下的本底个数
                norm_dict[samname[j]].append(theoryconc1[j+3*i])
                norm_dict[samname[j]].append(theoryconc2[j+3*i])
                norm_dict[samname[j]].append(theoryconc3[j+3*i])
                norm_dict[samname[j]].append(endlowrecycle1[j+3*i])
                norm_dict[samname[j]].append(endlowrecycle2[j+3*i])
                norm_dict[samname[j]].append(endlowrecycle3[j+3*i])
                norm_dict[samname[j]].append(endmedianrecycle1[j+3*i])
                norm_dict[samname[j]].append(endmedianrecycle2[j+3*i])
                norm_dict[samname[j]].append(endmedianrecycle3[j+3*i])
                norm_dict[samname[j]].append(endhighrecycle1[j+3*i])
                norm_dict[samname[j]].append(endhighrecycle2[j+3*i])
                norm_dict[samname[j]].append(endhighrecycle3[j+3*i])

        print(Recycle_dict)

        reportinfo = ReportInfo.objects.get(number=request.POST["instrument_num"], project=request.POST["project"])

        level = ["L", "M", "H"]
        if int(falsecounter) == 0:
            insert_list = []
            for key, value in Recycle_dict.items():  # 循环本底
                for r, c in value.items():
                    for j in range(len(level)):
                        insert_list.append(RECYCLE(reportinfo=reportinfo, norm=key, Experimentnum=r, level=level[j],
                                                   sam_conc=c[j], theory_conc=c[j+12], end_conc1=c[3*j+3], end_conc2=c[3*j+4], 
                                                   end_conc3=c[3*j+5],end_recycle1=c[3*j+15], end_recycle2=c[3*j+16], end_recycle3=c[3*j+17]))

            RECYCLE.objects.bulk_create(insert_list)  # 这种保存数据方法较省时间
            HttpResponse = "加标回收率数据保存成功!"
            return render(request, 'report/Datasave.html', locals())

        else:
            # 展示数据需要，后续需把这段代码删除
            insert_list = []
            for key, value in Recycle_dict.items():  # 循环本底
                for r, c in value.items():
                    for j in range(len(level)):
                        insert_list.append(RECYCLE(reportinfo=reportinfo, norm=key, Experimentnum=r, level=level[j],
                                                   sam_conc=c[j], theory_conc=c[j+12], end_conc1=c[3*j+3], end_conc2=c[3*j+4], 
                                                   end_conc3=c[3*j+5],end_recycle1=c[3*j+15], end_recycle2=c[3*j+16], end_recycle3=c[3*j+17]))

            RECYCLE.objects.bulk_create(insert_list)  # 这种保存数据方法较省时间
            HttpResponse = "加标回收率验证结果中含有不通过数据,请核对后重新提交!"
            return render(request, 'report/HttpResponse-danger.html', locals())

def InstrumentComparesave(request):
    try:
        name = User.objects.get(username=request.user).first_name
    except:
        pass
    if isinstance(request.user, auth.models.AnonymousUser):  # 判断是否为未登录用户
        User_class = 0
    else:
        User_class = 1
    if request.method == 'POST':
        # 接收验证基本信息，点击继续验证按钮时需用到
        instrument_num = request.POST["instrument_num"]
        Detectionplatform = request.POST["Detectionplatform"]  # 项目组
        project = request.POST["project"]  # 项目
        platform = request.POST["platform"]  # 仪器平台(液质,液相,ICP-MS...)
        manufacturers = request.POST["manufacturers"]  # 仪器厂家(AB,Agilent...)
        verifyoccasion = request.POST["verifyoccasion"]  # 验证时机
        
        textarea = request.POST["textarea"]

        reportinfo = ReportInfo.objects.get(number=instrument_num, project=project)
        InstrumentCompare.objects.create(reportinfo=reportinfo, textarea=textarea)

        HttpResponse = "仪器比对数据保存成功!"
        return render(request, 'report/Datasave.html', locals())

# LOQ数据保存
def LOQsave(request):
    try:
        name = User.objects.get(username=request.user).first_name
    except:
        pass
    if isinstance(request.user, auth.models.AnonymousUser):  # 判断是否为未登录用户
        User_class = 0
    else:
        User_class = 1
    if request.method == 'POST':
        # 接收验证基本信息，点击继续验证按钮时需用到
        instrument_num = request.POST["instrument_num"]
        Detectionplatform = request.POST["Detectionplatform"]  # 项目组
        project = request.POST["project"]  # 项目
        platform = request.POST["platform"]  # 仪器平台(液质,液相,ICP-MS...)
        manufacturers = request.POST["manufacturers"]  # 仪器厂家(AB,Agilent...)
        verifyoccasion = request.POST["verifyoccasion"]  # 验证时机

        if platform == "液质":
            judgenum = int(request.POST.getlist("judgenum")[0])  # 判断验证结果是否通过
            picturename = request.POST.getlist("picturename")
            AMR_id = int(request.POST.getlist("id")[0])
            objs = AMRpicture.objects.filter(reportinfo_id=AMR_id)

            if judgenum == 0:
                for index, i in enumerate(objs):
                    AMRpicture.objects.filter(img=i.img).update(name=picturename[index])  # 更新数据库中的图片名称
                HttpResponse = "方法定量限与线性范围数据保存成功!"
                return render(request, 'report/Datasave.html', locals())
            else:
                for index, i in enumerate(objs):
                    AMRpicture.objects.filter(img=i.img).delete()  # 删除数据库中的图片
                HttpResponse = "方法定量限与线性范围验证结果中含有不通过数据,请核对后重新提交!"
                return render(request, 'report/Warning.html', locals())
        
        else:
            print(request.POST)
            AMR_dict = eval(str(request.POST.getlist("AMR_dict")[0]))
            LOQ_num = int(request.POST.getlist("LOQ_num")[0])  # PT样本数
            LOQ_judge = request.POST["LOQ_judge"]  # 是否通过判断
            picturenum = request.POST["picturenum"]  # 图片个数

            # 预定义曲线点标识列表
            S=["AMR-S1","AMR-S2","AMR-S3","AMR-S4","AMR-S5","AMR-S6","AMR-S7","AMR-S8",
            "AMR-S9","AMR-S10","AMR-S11","AMR-S12","AMR-S13","AMR-S14","AMR-S15"] 

            # 获取AMR_dict中的key
            LOQ_norm = []
            for key in AMR_dict.keys():
                LOQ_norm.append(key)

            # 添加理论浓度
            theoryconclist = []
            for i in range(1, LOQ_num+1):
                theoryconc_string = "theoryconc"+str(i)
                theoryconclist.append(request.POST.getlist(theoryconc_string))

            for i in range(LOQ_num):
                for j in range(len(LOQ_norm)):
                    # 理论浓度添加到首位
                    AMR_dict[LOQ_norm[j]][S[i]].insert(0, theoryconclist[i][j])

            # 添加回收率
            recycle_one = []
            recycle_two = []
            recycle_three = []
            recycle_four = []
            recycle_five = []
            recycle_six = []

            for i in range(1, LOQ_num+1):
                recycle_one_string = "recycle_one"+str(i)
                recycle_two_string = "recycle_two"+str(i)
                recycle_three_string = "recycle_three"+str(i)
                recycle_four_string = "recycle_four"+str(i)
                recycle_five_string = "recycle_five"+str(i)
                recycle_six_string = "recycle_six"+str(i)
                recycle_one.append(request.POST.getlist(recycle_one_string))
                recycle_two.append(request.POST.getlist(recycle_two_string))
                recycle_three.append(request.POST.getlist(recycle_three_string))
                recycle_four.append(request.POST.getlist(recycle_four_string))
                recycle_five.append(request.POST.getlist(recycle_five_string))
                recycle_six.append(request.POST.getlist(recycle_six_string))

            for i in range(LOQ_num):
                for j in range(len(LOQ_norm)):
                    AMR_dict[LOQ_norm[j]][S[i]].append(recycle_one[i][j])
                    AMR_dict[LOQ_norm[j]][S[i]].append(recycle_two[i][j])
                    AMR_dict[LOQ_norm[j]][S[i]].append(recycle_three[i][j])
                    AMR_dict[LOQ_norm[j]][S[i]].append(recycle_four[i][j])
                    AMR_dict[LOQ_norm[j]][S[i]].append(recycle_five[i][j])
                    AMR_dict[LOQ_norm[j]][S[i]].append(recycle_six[i][j])

            # 添加平均回收率,检测值CV
            meanrecycle = []
            CV = []
            for i in range(1, LOQ_num+1):
                meanrecycle_string = "meanrecycle"+str(i)
                CV_string = "CV"+str(i)
                meanrecycle.append(request.POST.getlist(meanrecycle_string))
                CV.append(request.POST.getlist(CV_string))

            for i in range(LOQ_num):
                for j in range(len(LOQ_norm)):
                    AMR_dict[LOQ_norm[j]][S[i]].append(meanrecycle[i][j])
                    AMR_dict[LOQ_norm[j]][S[i]].append(CV[i][j])

            # 数据保存
            reportinfo = ReportInfo.objects.get(number=request.POST["instrument_num"], project=request.POST["project"])

            print(LOQ_judge)
            if LOQ_judge == "通过!":
                insert_list =[]
                for key,value in AMR_dict.items():
                    for r,c in value.items():
                        insert_list.append(AMR(reportinfo=reportinfo,Experimentnum=r,norm=key,therory_conc=c[0],test_conc1=c[1],test_conc2=c[2],
                        test_conc3=c[3],test_conc4=c[4],test_conc5=c[5],test_conc6=c[6],recycle1=c[7],recycle2=c[8],recycle3=c[9],recycle4=c[10],
                        recycle5=c[11],recycle6=c[12],meanrecycle=c[13],cvtest_conc=c[14]))

                AMR.objects.bulk_create(insert_list)

                # 图片保存
                if picturenum!=0:
                    picturename = request.POST.getlist("picturename")
                    AMR_id = int(request.POST.getlist("id")[0])
                    objs = AMRpicture.objects.filter(reportinfo_id=AMR_id)

                    for index, i in enumerate(objs):
                        AMRpicture.objects.filter(img=i.img).update(name=picturename[index])  # 更新数据库中的图片名称

                HttpResponse = "方法定量限与线性范围数据保存成功!"
                return render(request, 'report/Datasave.html', locals())

            else:
                HttpResponse = "方法定量限与线性范围验证结果中含有不通过数据,请核对后重新提交!"
                return render(request, 'report/Warning.html', locals())


def AMR2save(request):
    '''
    注释:最终需要生成一个字典dic_AMRsave,数据格式如下：
    print(dic_AMRsave):
    {"化合物1":{'S1':['S1理论浓度','S1检测值1','S1检测值2',...'S1回收率1','S1回收率2',...,'平均回收率','检测值CV']},
    {'S2':['S2理论浓度','S2检测值1','S2检测值2',...'S2回收率1','S2回收率2',...,'平均回收率','检测值CV']},
    "化合物2":{'S1':['S1理论浓度','S1检测值1','S1检测值2',...'S1回收率1','S1回收率2',...,'平均回收率','检测值CV']},
    {'S2':['S2理论浓度','S2检测值1','S2检测值2',...'S2回收率1','S2回收率2',...,'平均回收率','检测值CV']}
    '''
    try:
        name = User.objects.get(username=request.user).first_name
    except:
        pass
    if isinstance(request.user, auth.models.AnonymousUser):  # 判断是否为未登录用户
        User_class = 0
    else:
        User_class = 1
    if request.method == 'POST':
        print(request.POST)

        # 仪器编号,strip()的作用是去除前后空格
        instrument_num = request.POST["instrument_num"]
        group = request.POST["group"]  # 项目组
        project = request.POST["project"]  # 项目
        platform = request.POST["platform"]  # 仪器平台(液质,液相,ICP-MS...)
        manufacturers = request.POST["manufacturers"]  # 仪器厂家(AB,Agilent...)
        verifyoccasion = request.POST["verifyoccasion"]  # 验证时机

        dic_AMRsave = eval(str(request.POST.getlist("dicAMR")[0]))
        # dicPT的格式为一个列表，列表里只有一个字符串，字符串里又是一个字典，需要先把该字符串里的字典提取出来
        AMR_judgenum = int(request.POST.getlist('AMRjudgenum')[0])
        picturenum = int(request.POST.getlist('picturenum')[0])
        # objfile_list=request.POST.getlist('objfile')[0].split(',')

        AMR2save_norm = []  # 化合物列表
        for key in dic_AMRsave.keys():
            AMR2save_norm.append(key)

        AMR_STD = ['AMR-STD-1', 'AMR-STD-2', 'AMR-STD-3', 'AMR-STD-4', 'AMR-STD-5',
                   'AMR-STD-6', 'AMR-STD-7', 'AMR-STD-8', 'AMR-STD-9', 'AMR-STD-10']  # 预先定义列表
        for i in range(len(AMR2save_norm)):
            for j in range(len(dic_AMRsave[AMR2save_norm[i]])):
                string_theoryconc = 'theoryconc'+str(j+1)
                dic_AMRsave[AMR2save_norm[i]][AMR_STD[j]].insert(
                    0, request.POST.getlist(string_theoryconc)[i])  # 首位添加理论浓度

                # 依次添加六个回收率、平均回收率和CV
                string_recycle1 = 'recycle_one'+str(j+1)
                dic_AMRsave[AMR2save_norm[i]][AMR_STD[j]].append(
                    request.POST.getlist(string_recycle1)[i])

                string_recycle2 = 'recycle_two'+str(j+1)
                dic_AMRsave[AMR2save_norm[i]][AMR_STD[j]].append(
                    request.POST.getlist(string_recycle2)[i])

                string_recycle3 = 'recycle_three'+str(j+1)
                dic_AMRsave[AMR2save_norm[i]][AMR_STD[j]].append(
                    request.POST.getlist(string_recycle3)[i])

                string_recycle4 = 'recycle_four'+str(j+1)
                dic_AMRsave[AMR2save_norm[i]][AMR_STD[j]].append(
                    request.POST.getlist(string_recycle4)[i])

                string_recycle5 = 'recycle_five'+str(j+1)
                dic_AMRsave[AMR2save_norm[i]][AMR_STD[j]].append(
                    request.POST.getlist(string_recycle5)[i])

                string_recycle6 = 'recycle_six'+str(j+1)
                dic_AMRsave[AMR2save_norm[i]][AMR_STD[j]].append(
                    request.POST.getlist(string_recycle6)[i])

                string_meanrecycle = 'meanrecycle'+str(j+1)
                dic_AMRsave[AMR2save_norm[i]][AMR_STD[j]].append(
                    request.POST.getlist(string_meanrecycle)[i])

                string_CV = 'CV'+str(j+1)
                dic_AMRsave[AMR2save_norm[i]][AMR_STD[j]].append(
                    request.POST.getlist(string_CV)[i])

        reportinfo = ReportInfo.objects.get(
            number=request.POST["instrument_num"], project=request.POST["project"])

        if AMR_judgenum == 0:
            insert_list = []
            for key, value in dic_AMRsave.items():
                for r, c in value.items():
                    insert_list.append(AMR(reportinfo=reportinfo, Experimentnum=r, norm=key, therory_conc=c[0], test_conc1=c[1], test_conc2=c[2],
                                           test_conc3=c[3], test_conc4=c[4], test_conc5=c[5], test_conc6=c[
                                               6], recycle1=c[7], recycle2=c[8], recycle3=c[9], recycle4=c[10],
                                           recycle5=c[11], recycle6=c[12], meanrecycle=c[13], cvtest_conc=c[14]))

            AMR.objects.bulk_create(insert_list)

            if picturenum != 0:
                picturename = request.POST.getlist("picturename")
                AMR2_id = int(request.POST.getlist("id")[0])
                objs = AMRpicture.objects.filter(reportinfo_id=AMR2_id)
                for index, i in enumerate(objs):
                    AMRpicture.objects.filter(img=i.img).update(
                        name=picturename[index])  # 更新数据库中的图片名称

            HttpResponse = "方法定量限与线性范围数据保存成功!"
            return render(request, 'report/Datasave.html', locals())

        else:
            insert_list = []
            for key, value in dic_AMRsave.items():
                for r, c in value.items():
                    insert_list.append(AMR(reportinfo=reportinfo, Experimentnum=r, norm=key, therory_conc=c[0], test_conc1=c[1], test_conc2=c[2],
                                           test_conc3=c[3], test_conc4=c[4], test_conc5=c[5], test_conc6=c[
                                               6], recycle1=c[7], recycle2=c[8], recycle3=c[9], recycle4=c[10],
                                           recycle5=c[11], recycle6=c[12], meanrecycle=c[13], cvtest_conc=c[14]))

            AMR.objects.bulk_create(insert_list)

            if picturenum != 0:
                picturename = request.POST.getlist("picturename")
                AMR2_id = int(request.POST.getlist("id")[0])

                # for file in objfile:
                #     AMRpicture.objects.create(reportinfo = reportinfo,img = file,name="")

                objs = AMRpicture.objects.filter(reportinfo_id=AMR2_id)
                for index, i in enumerate(objs):
                    AMRpicture.objects.filter(img=i.img).update(
                        name=picturename[index])  # 更新数据库中的图片名称

            HttpResponse = "方法定量限与线性范围验证结果中含有不通过数据,请核对后重新提交!"
            return render(request, 'report/HttpResponse-danger.html', locals())


def LODsave(request):
    try:
        name = User.objects.get(username=request.user).first_name
    except:
        pass
    if isinstance(request.user, auth.models.AnonymousUser):  # 判断是否为未登录用户
        User_class = 0
    else:
        User_class = 1
    if request.method == 'POST':
        print(request.POST)
        # 仪器编号,strip()的作用是去除前后空格
        instrument_num = request.POST["instrument_num"]
        group = request.POST["group"]  # 项目组
        project = request.POST["project"]  # 项目
        platform = request.POST["platform"]  # 仪器平台(液质,液相,ICP-MS...)
        manufacturers = request.POST["manufacturers"]  # 仪器厂家(AB,Agilent...)
        verifyoccasion = request.POST["verifyoccasion"]  # 验证时机

        picturename = request.POST.getlist("picturename")
        conclusion = request.POST.getlist("conclusion")[0]
        LOD_id = int(request.POST.getlist("id")[0])
        objs = LODpicture.objects.filter(reportinfo_id=LOD_id)
        for index, i in enumerate(objs):
            LODpicture.objects.filter(img=i.img).update(
                name=picturename[index])
            LODpicture.objects.filter(img=i.img).update(conclusion=conclusion)

        objs = LODpicture.objects.filter(reportinfo_id=LOD_id)

    HttpResponse = "方法检出限数据保存成功!"
    return render(request, 'report/Datasave.html', locals())


def AMR_conclusionsave(request):
    try:
        name = User.objects.get(username=request.user).first_name
    except:
        pass
    if isinstance(request.user, auth.models.AnonymousUser):  # 判断是否为未登录用户
        User_class = 0
    else:
        User_class = 1
    if request.method == 'POST':
        # 接收验证基本信息，点击继续验证按钮时需用到
        instrument_num = request.POST["instrument_num"]
        Detectionplatform = request.POST["Detectionplatform"]  # 项目组
        project = request.POST["project"]  # 项目
        platform = request.POST["platform"]  # 仪器平台(液质,液相,ICP-MS...)
        manufacturers = request.POST["manufacturers"]  # 仪器厂家(AB,Agilent...)
        verifyoccasion = request.POST["verifyoccasion"]  # 验证时机

        id = int(request.POST.getlist("id")[0])
        compound = request.POST.getlist("compound")
        lod = request.POST.getlist("lod")
        loq = request.POST.getlist("loq")
        amr = request.POST.getlist("amr")

        for i in range(len(compound)):
            AMRconsluion.objects.create(reportinfo_id=id, name=compound[i], lodconclusion=lod[i], loqconclusion=loq[i], amrconclusion=amr[i])

    HttpResponse = "AMR最终结论数据保存成功!"
    return render(request, 'report/Datasave.html', locals())


def CRRsave(request):
    try:
        name = User.objects.get(username=request.user).first_name
    except:
        pass
    if isinstance(request.user, auth.models.AnonymousUser):  # 判断是否为未登录用户
        User_class = 0
    else:
        User_class = 1
    if request.method == 'POST':
        print(request.POST)
        id = int(request.POST.getlist("id")[0])
        compound = request.POST.getlist("compound")
        crr = request.POST.getlist("crr")

        for i in range(len(compound)):
            CRR2.objects.create(reportinfo_id=id, norm=compound[i], crr=crr[i])

    HttpResponse = "临床可报告范围数据保存成功!"
    return render(request, 'report/Datasave.html', locals())


def MSsave(request):
    try:
        name = User.objects.get(username=request.user).first_name
    except:
        pass
    if isinstance(request.user, auth.models.AnonymousUser):  # 判断是否为未登录用户
        User_class = 0
    else:
        User_class = 1
    if request.method == 'POST':
        # 仪器编号,strip()的作用是去除前后空格
        instrument_num = request.POST["instrument_num"]
        group = request.POST["group"]  # 项目组
        project = request.POST["project"]  # 项目
        platform = request.POST["platform"]  # 仪器平台(液质,液相,ICP-MS...)
        manufacturers = request.POST["manufacturers"]  # 仪器厂家(AB,Agilent...)
        verifyoccasion = request.POST["verifyoccasion"]  # 验证时机

        picturename = request.POST.getlist("picturename")
        conclusion = request.POST.getlist("conclusion")[0]
        MS_id = int(request.POST.getlist("id")[0])
        objs = MS.objects.filter(reportinfo_id=MS_id)
        for index, i in enumerate(objs):
            MS.objects.filter(img=i.img).update(name=picturename[index])
            MS.objects.filter(img=i.img).update(conclusion=conclusion)

        objs = MS.objects.filter(reportinfo_id=MS_id)

    HttpResponse = "基质特异性数据保存成功!"
    return render(request, 'report/Datasave.html', locals())


def Sample_Stability_Save(request):
    # print(request.POST)

    # 从数据库中抓取当前用户名传递到layout.html
    try:
        name = User.objects.get(username=request.user).first_name
    except:
        pass

    # 判断是否为未登录用户
    if isinstance(request.user, auth.models.AnonymousUser):  
        User_class = 0
    else:
        User_class = 1

    # 提取Sample_Stability.html中的数据，并存入数据库
    if request.method == 'POST':   
        # 一 基本信息提取，layout.html中需要用到
        instrument_num = request.POST["instrument_num"] # 仪器编号
        Detectionplatform = request.POST["Detectionplatform"]  # 检测平台（研发，微量营养素...）
        project = request.POST["project"]  # 检测项目
        platform = request.POST["platform"]  # 仪器平台(液质,液相,ICP-MS...)
        manufacturers = request.POST["manufacturers"]  # 仪器厂家(AB,Agilent...)
        verifyoccasion = request.POST["verifyoccasion"]  # 验证时机

        # 二 判断验证结论是否通过
        conclusion = int(request.POST["conclusion"])

        # 1 验证未通过，不抓取数据，直接返回提示界面
        if conclusion > 0:
            HttpResponse = "样品稳定性验证结果中含有不通过数据,请核对后重新提交!"
            return render(request, 'report/HttpResponse-danger.html', locals())

        # 2 验证通过，抓取验证结果界面中的数据
        else:  
            # 2.1 提取html中的字典和对应的浓度水平
            Room_tem_dict = eval(str(request.POST.getlist("Room_tem_dict")[0]))
            Refrigerate_tem_dict = eval(str(request.POST.getlist("Refrigerate_tem_dict")[0]))
            Freeze_tem_dict = eval(str(request.POST.getlist("Freeze_tem_dict")[0]))

            Room_conclevel_list = eval(str(request.POST.getlist("Room_conclevel_list")[0]))
            Refrigerate_conclevel_list = eval(str(request.POST.getlist("Refrigerate_conclevel_list")[0]))
            Freeze_conclevel_list = eval(str(request.POST.getlist("Freeze_conclevel_list")[0]))

            # 2.2 判断用户是否修改了验证时间，方法是分别比较Room_tem_dict和Refrigerate_tem_dict中的时间和input框中的时间
            # 2.2.1 比较Room_tem_dict中每个化合物的验证时间（即比较上传文件中的时间和用户点击保存后的时间）
            for key,value in Room_tem_dict.items():
                # 用户点击保存后的时间
                list1 = request.POST.getlist("Room_tem_time_"+key)
                # 上传文件中的时间
                list2 = []
                
                for i in value.keys():
                    list2.append(i)
                
                # 判断list1和list2是否相等，不相等需用用户输入的时间替换原来的时间
                if list1 !=list2:
                    # 字典替换key的方法
                    a = value.values()
                    b = list1
                    Room_tem_dict[key] = dict(zip(b,a))

            # 2.2.2 比较Refrigerate_tem_dict中每个化合物的验证时间（即比较上传文件中的时间和用户点击保存后的时间）
            for key,value in Refrigerate_tem_dict.items():
                # 用户点击保存后的时间
                list1 = request.POST.getlist("Refrigerate_tem_time_"+key)
                # 上传文件中的时间
                list2 = []
                
                for i in value.keys():
                    list2.append(i)
                
                # 判断list1和list2是否相等，不相等需用用户输入的时间替换原来的时间
                if list1 !=list2:

                    # 字典替换key的方法
                    a = value.values()
                    b = list1
                    Refrigerate_tem_dict[key] = dict(zip(b,a))

            # 2.2.3 比较Freeze_tem_dict中每个化合物的验证时间（即比较上传文件中的时间和用户点击保存后的时间）
            for key,value in Freeze_tem_dict.items():
                # 用户点击保存后的时间
                list1 = request.POST.getlist("Freeze_tem_time_"+key)
                # 上传文件中的时间
                list2 = []
                
                for i in value.keys():
                    list2.append(i)
                
                # 判断list1和list2是否相等，不相等需用用户输入的时间替换原来的时间
                if list1 !=list2:

                    # 字典替换key的方法
                    a = value.values()
                    b = list1
                    Freeze_tem_dict[key] = dict(zip(b,a))

            # 2.3 添加数据进入数据库
            # 2.3.1 关联主表
            reportinfo = ReportInfo.objects.get(number=request.POST["instrument_num"], Detectionplatform = request.POST["Detectionplatform"],project=request.POST["project"],
                                                platform = request.POST["platform"],manufacturers = request.POST["manufacturers"])

            # 2.3.2 添加室温
            insert_list_Room_tem = []
            
            # 3个浓度水平
            if len(Room_conclevel_list)==3:
                for key,value in Room_tem_dict.items():
                    for i,j in value.items(): 
                        insert_list_Room_tem.append(Stability(reportinfo=reportinfo, norm=key, temperature="Room_tem", time=i,L01=j[0],L02=j[1],L03=j[2],
                        M01=j[3],M02=j[4],M03=j[5],H01=j[6],H02=j[7],H03=j[8]))

            # 两个浓度水平
            else:
                if "低" not in Room_conclevel_list:
                    for key,value in Room_tem_dict.items():
                        for i,j in value.items(): 
                            insert_list_Room_tem.append(Stability(reportinfo=reportinfo, norm=key, temperature="Room_tem", time=i,L01="/",L02="/",L03="/",
                            M01=j[0],M02=j[1],M03=j[2],H01=j[3],H02=j[4],H03=j[5]))

                elif "中" not in Room_conclevel_list:
                    for key,value in Room_tem_dict.items():
                        for i,j in value.items(): 
                            insert_list_Room_tem.append(Stability(reportinfo=reportinfo, norm=key, temperature="Room_tem", time=i,M01="/",M02="/",M03="/",
                            L01=j[0],L02=j[1],L03=j[2],H01=j[3],H02=j[4],H03=j[5]))
                
                elif "高" not in Room_conclevel_list:
                    for key,value in Room_tem_dict.items():
                        for i,j in value.items(): 
                            insert_list_Room_tem.append(Stability(reportinfo=reportinfo, norm=key, temperature="Room_tem", time=i,H01="/",H02="/",H03="/",
                            L01=j[0],L02=j[1],L03=j[2],M01=j[3],M02=j[4],M03=j[5]))

            Stability.objects.bulk_create(insert_list_Room_tem)

            # 2.3.3 添加冷藏
            insert_list_Refrigerate_tem = []

            # 3个浓度水平
            if len(Refrigerate_conclevel_list)==3:
                for key,value in Refrigerate_tem_dict.items():
                    for i,j in value.items(): 
                        insert_list_Refrigerate_tem.append(Stability(reportinfo=reportinfo, norm=key, temperature="Refrigerate_tem", time=i,L01=j[0],L02=j[1],L03=j[2],
                        M01=j[3],M02=j[4],M03=j[5],H01=j[6],H02=j[7],H03=j[8]))

            # 两个浓度水平
            else:
                if "低" not in Refrigerate_conclevel_list:
                    for key,value in Refrigerate_tem_dict.items():
                        for i,j in value.items(): 
                            insert_list_Refrigerate_tem.append(Stability(reportinfo=reportinfo, norm=key, temperature="Refrigerate_tem", time=i,L01="/",L02="/",L03="/",
                            M01=j[0],M02=j[1],M03=j[2],H01=j[3],H02=j[4],H03=j[5]))

                elif "中" not in Refrigerate_conclevel_list:
                    for key,value in Refrigerate_tem_dict.items():
                        for i,j in value.items(): 
                            insert_list_Refrigerate_tem.append(Stability(reportinfo=reportinfo, norm=key, temperature="Refrigerate_tem", time=i,M01="/",M02="/",M03="/",
                            L01=j[0],L02=j[1],L03=j[2],H01=j[3],H02=j[4],H03=j[5]))
                
                elif "高" not in Refrigerate_conclevel_list:
                    for key,value in Refrigerate_tem_dict.items():
                        for i,j in value.items(): 
                            insert_list_Refrigerate_tem.append(Stability(reportinfo=reportinfo, norm=key, temperature="Refrigerate_tem", time=i,H01="/",H02="/",H03="/",
                            L01=j[0],L02=j[1],L03=j[2],M01=j[3],M02=j[4],M03=j[5]))

            Stability.objects.bulk_create(insert_list_Refrigerate_tem)

            # 2.3.4 添加冷冻
            insert_list_Freeze_tem = []

             # 3个浓度水平
            if len(Freeze_conclevel_list)==3:
                for key,value in Freeze_tem_dict.items():
                    for i,j in value.items(): 
                        insert_list_Freeze_tem.append(Stability(reportinfo=reportinfo, norm=key, temperature="Freeze_tem", time=i,L01=j[0],L02=j[1],L03=j[2],
                        M01=j[3],M02=j[4],M03=j[5],H01=j[6],H02=j[7],H03=j[8]))

            # 两个浓度水平
            else:
                if "低" not in Freeze_conclevel_list:
                    for key,value in Freeze_tem_dict.items():
                        for i,j in value.items(): 
                            insert_list_Freeze_tem.append(Stability(reportinfo=reportinfo, norm=key, temperature="Freeze_tem", time=i,L01="/",L02="/",L03="/",
                            M01=j[0],M02=j[1],M03=j[2],H01=j[3],H02=j[4],H03=j[5]))

                elif "中" not in Freeze_conclevel_list:
                    for key,value in Freeze_tem_dict.items():
                        for i,j in value.items(): 
                            insert_list_Freeze_tem.append(Stability(reportinfo=reportinfo, norm=key, temperature="Freeze_tem", time=i,M01="/",M02="/",M03="/",
                            L01=j[0],L02=j[1],L03=j[2],H01=j[3],H02=j[4],H03=j[5]))
                
                elif "高" not in Freeze_conclevel_list:
                    for key,value in Freeze_tem_dict.items():
                        for i,j in value.items(): 
                            insert_list_Freeze_tem.append(Stability(reportinfo=reportinfo, norm=key, temperature="Freeze_tem", time=i,H01="/",H02="/",H03="/",
                            L01=j[0],L02=j[1],L03=j[2],M01=j[3],M02=j[4],M03=j[5]))

            Stability.objects.bulk_create(insert_list_Freeze_tem)

            HttpResponse = "样品处理后稳定性数据保存成功!"
            return render(request, 'report/Datasave.html', locals())

def verifyagain(request):
    if request.method == 'POST':
        instrument_num_verifyagain = request.POST["instrument_num"]
        # 项目组
        Detectionplatform_verifyagain = request.POST["Detectionplatform"]
        project_verifyagain = request.POST["project"]  # 项目
        # 仪器平台(液质,液相,ICP-MS...)
        platform_verifyagain = request.POST["platform"]
        # 仪器厂家(AB,Agilent...)
        manufacturers_verifyagain = request.POST["manufacturers"]
        verifyoccasion_verifyagain = request.POST["verifyoccasion"]  # 验证时机
    return render(request, 'report/verification.html', locals())

def returnback(request):
    Detectionplatform = []  # 项目组列表，需传到前端
    project = []  # 项目列表，需传到前端
    Detectionplatformdata = Special.objects.all()
    for i in Detectionplatformdata:
        if i.Detectionplatform not in Detectionplatform:
            Detectionplatform.append(i.Detectionplatform)
    Detectionplatform.sort()

    for i in range(len(Detectionplatform)):
        project.append([])
        projectdata = Special.objects.filter(
            Detectionplatform=Detectionplatform[i])
        for j in projectdata:
            project[i].append(j.project)

    print(Detectionplatform)
    return render(request, 'report/verification.html', locals())
