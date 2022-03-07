from re import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from numpy import number
from report import models
from .forms import UploadFileForm
from report import jmd, zqd, amr, crr, ms, Carry_over, Matrix_effect, testmethod, equipment, reagents_consumables, sample_preparation, QC, Sample_Stability,Sample_ReferenceInterval
from .models import *
import time

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
            End_conclusion = request.POST["End_conclusion"]  # 报告最终结论
            # verifytime = time.strftime('%Y-%m-%d', time.localtime(time.time()))  # 初始验证时间

            # 二 后台管理系统查找单位,有效位数和化合物个数,此处由于单位,有效位数和化合物个数都为必填项,因此使用get()方法时不需要try
            Unit = Special.objects.get(Detectionplatform=Detectionplatform, project=project).unit  # 单位
            digits = Special.objects.get(project=project).Effective_digits  # 有效位数
            Number_of_compounds = Special.objects.get(project=project).Number_of_compounds  # 化合物个数

            # 三 判断此份报告是否已被创建
            if ReportInfo.objects.filter(number=instrument_num, project=project):
                reportinfo = ReportInfo.objects.get(number=instrument_num,Detectionplatform=Detectionplatform,project=project,platform=platform,manufacturers=manufacturers)
            else:
                reportinfo = ReportInfo.objects.create(number=instrument_num,Detectionplatform=Detectionplatform,project=project,platform=platform,manufacturers=manufacturers)

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
            
            # 六 9个验证指标数据提取
            # 1 精密度
            if request.POST["quota"] == "精密度":
                if request.POST["jmd"] == "重复性精密度":
                    namejmd = "重复性精密度"
                    files = request.FILES.getlist('fileuploads')
                    Result = jmd.IntraP_fileread(files, reportinfo, namejmd, project, platform, manufacturers,Unit, digits, ZP_Method_precursor_ion, ZP_Method_product_ion, normAB)
                elif request.POST["jmd"] == "中间精密度":
                    namejmd = "中间精密度"
                    files = request.FILES.getlist('fileuploads')
                    Result = jmd.InterP_fileread(files, reportinfo, namejmd, project, platform, manufacturers,Unit, digits, ZP_Method_precursor_ion, ZP_Method_product_ion, normAB)
                return render(request, 'report/project/Jmd.html', locals())

            elif request.POST["quota"] == "正确度":
                if request.POST["zqd"] == "PT":
                    files = request.FILES.getlist('fileuploads')
                    Result = zqd.PTfileread(files, Detectionplatform, project, platform, manufacturers,digits, ZP_Method_precursor_ion, ZP_Method_product_ion, normAB)
                    return render(request, 'report/project/PT.html', locals())
                elif request.POST["zqd"] == "加标回收":
                    files = request.FILES.getlist('fileuploads')
                    Result = zqd.recyclefileread(files, project, platform, manufacturers, Unit, digits, ZP_Method_precursor_ion, ZP_Method_product_ion, normAB)
                    return render(request, 'report/project/Recycle.html', locals())
                elif request.POST["zqd"] == "仪器比对":
                    pass

            # ICP-MS平台AMR可能需要上传多个数据文件
            elif request.POST["quota"] == "分析灵敏度与分析测量范围":
                if request.POST["amr"] == "方法定量限与线性范围":
                    files = request.FILES.getlist('fileuploads')
                    if platform != "ICP-MS":  # 不是ICP-MS，上传单个文件
                        dicAMR = amr.AMRfileread(files, reportinfo, project, platform, manufacturers, Unit,
                                                 digits, ZP_Method_precursor_ion, ZP_Method_product_ion, normAB, Number_of_compounds)
                        if platform == "液质":
                            # if dicAMR["error"]:
                            #     error=dicAMR["error"]
                            #     return render(request,'report/error.html',locals())
                            pass

                            return render(request, 'report/project/AMR.html', locals())
                        else:
                            return render(request, 'report/project/AMR2.html', locals())
                    else:
                        dicAMR = amr.AMRmutiplefileread(
                            files, reportinfo, project, platform, manufacturers, Unit, digits, ZP_Method_precursor_ion, ZP_Method_product_ion)
                        return render(request, 'report/project/AMR2.html', locals())

                elif request.POST["amr"] == "方法检出限":
                    files = request.FILES.getlist('fileuploads')
                    dicLOD = amr.LODfileread(files, reportinfo, project, platform, manufacturers,
                                             Unit, digits, ZP_Method_precursor_ion, ZP_Method_product_ion)
                    return render(request, 'report/project/LOD.html', locals())
                elif request.POST["amr"] == "结论":
                    AMRid = ReportInfo.objects.get(
                        number=instrument_num, project=project).id
                    return render(request, 'report/project/AMR_conclusion.html', locals())

            elif request.POST["quota"] == "临床可报告范围":
                if request.POST["crr"] == "不做验证":
                    CRRid = ReportInfo.objects.get(
                        number=instrument_num, project=project).id
                    return render(request, 'report/project/CRR2.html', locals())
                else:
                    files = request.FILES.getlist('fileuploads')
                    dicCRR = crr.CRRfileread(files, reportinfo, project, platform, manufacturers,
                                             Unit, digits, ZP_Method_precursor_ion, ZP_Method_product_ion, normAB)
                    return render(request, 'report/project/CRR.html', locals())

            elif request.POST["quota"] == "基质特异性":
                files = request.FILES.getlist('fileuploads')
                MS = ms.MSfileread(files, reportinfo)
                return render(request, 'report/project/MS.html', locals())

            elif request.POST["quota"] == "基质效应":
                if request.POST["Me"] == "2个浓度水平":
                    files = request.FILES.getlist('fileuploads')
                    dicMatrix_effect = Matrix_effect.Matrix_effectfileread2(files, reportinfo, project, platform, manufacturers, digits, ZP_Method_precursor_ion, ZP_Method_product_ion, normAB)
                elif request.POST["Me"] == "3个浓度水平":
                    files = request.FILES.getlist('fileuploads')
                    dicMatrix_effect = Matrix_effect.Matrix_effectfileread3(files, reportinfo, project, platform, manufacturers, digits, ZP_Method_precursor_ion, ZP_Method_product_ion, normAB)
                return render(request, 'report/project/Matrix_effect.html', locals())

            elif request.POST["quota"] == "携带效应":
                files = request.FILES.getlist('fileuploads')
                Carryover2_True = 0  # 判断验证界面是用通用性模板还是特殊模板(元素组)
                if request.POST["carryover"] == "携带效应2":
                    Carryover2_True += 1
                dicCarryover = Carry_over.Carryoverfileread(files, Detectionplatform, reportinfo, project, platform,
                                                            manufacturers, Carryover2_True, Unit, digits, ZP_Method_precursor_ion, ZP_Method_product_ion, normAB)
                return render(request, 'report/project/Carryover.html', locals())

            elif request.POST["quota"] == "样品稳定性":
                if request.POST["stability"] == "样品储存稳定性":     
                    files = request.FILES.getlist('fileuploads')
                    Result = Sample_Stability.store_fileread(files, Detectionplatform, reportinfo, project, platform,manufacturers, Unit, digits, ZP_Method_precursor_ion, ZP_Method_product_ion, normAB)
                elif request.POST["stability"] == "样品处理后稳定性":     
                    files = request.FILES.getlist('fileuploads')
                    Result = Sample_Stability.handle_fileread(files, Detectionplatform, reportinfo, project, platform,manufacturers, Unit, digits, ZP_Method_precursor_ion, ZP_Method_product_ion, normAB) 
                return render(request, 'report/project/Sample_Stability.html', locals())

            elif request.POST["quota"] == "参考区间":
                if request.POST["referenceinterval"] == "参考区间建立":     
                    files = request.FILES.getlist('fileuploads')
                    Result = Sample_ReferenceInterval.create_fileread(files, Detectionplatform, reportinfo, project, platform,manufacturers, Unit, digits, ZP_Method_precursor_ion, ZP_Method_product_ion, normAB)
                    return render(request, 'report/project/RI_Create.html', locals())
                elif request.POST["referenceinterval"] == "参考区间验证":        
                    files = request.FILES.getlist('fileuploads')
                    Result = Sample_ReferenceInterval.quote_fileread(files, Detectionplatform, reportinfo, project, platform,manufacturers, Unit, digits, ZP_Method_precursor_ion, ZP_Method_product_ion, normAB)
                    return render(request, 'report/project/RI_quote.html', locals())


            elif request.POST["quota"] == "最终结论":
                endconclusion.objects.create(reportinfo=reportinfo, text=End_conclusion)
                HttpResponse = "最终结论保存成功！"
                return render(request, 'report/Datasave.html', locals())

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

    if name == "余木俊" or name == "陈文彬":
        data = ReportInfo.objects.filter(Detectionplatform="微量营养素检测平台")
    elif name == "李冰玲":
        data = ReportInfo.objects.filter(Detectionplatform="治疗药物检测平台")
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
        PNjmdindex = 0  # 重复性精密度副标题索引   6.1

        tablePNindex = tableindex # 重复性精密度表格索引  表3

        # 重复性精密度数据
        PNjmd_data = jmd.related_PNjmd(id)
        if PNjmd_data:
            PNjmdindex += 1  # 重复性精密度副标题索引+1  6.2
            tableindex += Number_of_compounds  # 总表格索引+n，以两个化合物为例，开始是表3，现在是表5   表5

        # 中间精密度
        resultPJ = jmd.related_PJjmd(id)
        PJjmdindex = PNjmdindex  # 重复性精密度副标题索引赋值给中间精密度副标题索引
        tablePJindex = tableindex

        if resultPJ:
            PJjmdindex += 1  # 中间精密度副标题索引+1
            tableindex += 1  # 总表格索引+n

        # 精密度结论
        if PNjmd_data and resultPJ:
            resultjmdendconclusion = jmd.related_jmdendconclusion(id)
            JMDendconclusionindex = PJjmdindex
            tablejmdendconclusionindex = tableindex  # 精密度结论表格索引,不管几个化合物，最终结论都只有一个表格
            if resultjmdendconclusion:
                JMDendconclusionindex += 1  # 精密度结论副标题索引+1
                tableindex += 1

        if PNjmd_data or resultPJ:  # 如果有重复性精密度和中间精密度,总标题索引+1
            titleindex += 1

        # 正确度
        ZQDindex = titleindex
        PTindex = 0  # PT副标题索引
        tablePTindex = tableindex

        resultPT = zqd.related_PT(id)
        if resultPT:
            PTindex += 1
            tableindex += 1

        # 加标回收
        RECYCLEindex = PTindex
        tableRECYCLEindex = tableindex

        resultrecycle = zqd.related_recycle(id)
        if resultrecycle:
            RECYCLEindex += 1
            tableindex += 1

        if resultPT or resultrecycle:
            titleindex += 1  # 7

        # AMR
        AMRindex = titleindex  # 7
        amrindex = 0
        pictureindex = 1  # 总图片索引
        tableAMRindex = tableindex
        pictureAMRindex_start = pictureindex
        pictureAMRindex_end = pictureindex+Number_of_compounds*2-1

        resultAMR = amr.related_AMR(id, unit)
        if resultAMR:
            amrindex += 1
            pictureindex += Number_of_compounds*2  # 总图片索引
            tableindex += 1

        # LOD
        LODindex = amrindex
        tableLODindex = tableindex
        pictureLODindex_start = pictureindex
        pictureLODindex_end = pictureindex+Number_of_compounds-1

        resultLOD = amr.related_LOD(id)
        if resultLOD:
            if group != "元素":
                LODindex += 1
                pictureindex += Number_of_compounds
            else:
                LODindex += 1
                tableindex += 1

        # AMRconclusion
        AMRconclusionindex = LODindex
        tableAMRconclusionindex = tableindex
        resultAMRconclusion = amr.related_AMRconclusion(id)
        if resultAMRconclusion:
            AMRconclusionindex += 1
            tableindex += 1

        if resultAMR or resultLOD:
            titleindex += 1

        # CRR(稀释倍数)
        CRRindex = titleindex
        crrindex = 0
        tableCRRindex = tableindex

        resultCRR = crr.related_CRR(id)
        if resultCRR:
            crrindex += 1
            titleindex += 1
            tableindex += 1

        # 基质特异性
        MSindex = titleindex
        pictureMSindex_start = pictureindex
        pictureMSindex_end = pictureindex+2  # 固定三种图(标准品，血清样本，空白基质)
        resultMS = ms.related_MS(id)
        if resultMS:
            titleindex += 1

        # 基质效应
        Matrix_effectindex = titleindex
        tableMatrix_effectindex = tableindex
        resultMatrix_effect = Matrix_effect.related_Matrix_effect(id)
        if resultMatrix_effect:
            titleindex += 1
            tableindex += 1

        # 携带效应
        Carryoverindex = titleindex
        tableCarryoverindex_start = tableindex
        tableCarryoverindex_end = tableindex+1

        resultCarryover = Carry_over.related_Carryover(id)
        if resultCarryover:
            titleindex += 1

        # 检测方法
        resulttest_method = testmethod.related_testmethod(id)

        resultequipment = equipment.related_equipment(id)
        resultReagents_Consumables = reagents_consumables.related_Reagents_Consumables(id)
        resultSample_Preparation = sample_preparation.related_Sample_Preparation(id)

        End_conclusion_table = endconclusion.objects.filter(reportinfo_id=id)
        if End_conclusion_table:
            resultEnd_conclusion = []
            for i in End_conclusion_table:
                resultEnd_conclusion.append(i.text)
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

        if PNjmd_data or PJjmd_data:  # 如果有重复性精密度和中间精密度,总标题索引+1
            titleindex += 1 # -- 7

        # --------------------------------------- 正确度（每个化合物一个表格）---------------------------------------

        ZQDindex = titleindex # 正确度度主标题索引 

        # 1  PT
        PTindex = 0  # PT副标题索引  7.1

        tablePTindex_start = tableindex # 第一个化合物表格索引
        tablePTindex_end = tableindex+Number_of_compounds-1 # 最后一个化合物的表格索引

        PT_data = zqd.related_PT(id)
        if PT_data["PT_dict"]:
            PTindex += 1 # # 正确度副标题索引+1  7.2
            tableindex += Number_of_compounds # 总表格索引+n

        # 加标回收
        RECYCLEindex = PTindex # --7.1

        tableRECYCLEindex_start = tableindex
        tableRECYCLEindex_end = tableindex+Number_of_compounds-1

        resultrecycle = zqd.related_recycle(id)
        if resultrecycle:
            RECYCLEindex += 1 # --7.2
            tableindex += Number_of_compounds

        if PT_data or resultrecycle:
            titleindex += 1  # 8

        # AMR
        AS_AMRindex = titleindex  # 8 (分析灵敏度和分析测量范围大标题索引)

        AMRindex = 0
        pictureindex = 1  # 总图片索引
        tableAMRindex_start = tableindex
        tableAMRindex_end = tableindex+Number_of_compounds-1
        pictureAMRindex_start = pictureindex
        pictureAMRindex_end = pictureindex+Number_of_compounds*2-1

        resultAMR = amr.related_AMR(id, unit)
        if resultAMR:
            AMRindex += 1
            pictureindex += Number_of_compounds*2  # 总图片索引
            tableindex += Number_of_compounds

        # LOD
        LODindex = AMRindex
        tableLODindex = tableindex
        pictureLODindex_start = pictureindex
        pictureLODindex_end = pictureindex+Number_of_compounds-1

        resultLOD = amr.related_LOD(id)
        if resultLOD:
            if group != "元素":
                LODindex += 1
                pictureindex += Number_of_compounds
            else:
                LODindex += 1
                tableindex += 1

        # AMRconclusion
        AMRconclusionindex = LODindex
        tableAMRconclusionindex = tableindex
        resultAMRconclusion = amr.related_AMRconclusion(id)
        if resultAMRconclusion:
            AMRconclusionindex += 1
            tableindex += 1

        if resultAMR or resultLOD:
            titleindex += 1

        # CRR(稀释倍数)
        CRR2_True = 1  # 判断是用通用性模板还是特殊模板(元素组)
        if Detectionplatform == "元素":
            CRR2_True -= 1

            CRRindex = titleindex
            crrindex = 0
            tableCRRindex = tableindex

            resultCRR = crr.related_CRR(id)
            if resultCRR:
                crrindex += 1
                titleindex += 1
                tableindex += 1

        else:
            CRRindex = titleindex
            crrindex = 0
            tableCRRindex_start = tableindex
            tableCRRindex_end = tableindex+Number_of_compounds-1

            resultCRR = crr.related_CRR(id)
            if resultCRR:
                crrindex += 1
                titleindex += 1
                tableindex += Number_of_compounds

        # 基质特异性
        MSindex = titleindex
        pictureMSindex_start = pictureindex
        pictureMSindex_end = pictureindex+2  # 固定三种图(标准品，血清样本，空白基质)
        resultMS = ms.related_MS(id)
        if resultMS:
            titleindex += 1

        # 基质效应
        Matrix_effectindex = titleindex
        tableMatrix_effectindex_start = tableindex
        tableMatrix_effectindex_end = tableindex+Number_of_compounds-1
        resultMatrix_effect = Matrix_effect.related_Matrix_effect(id)
        if resultMatrix_effect:
            titleindex += 1
            tableindex += Number_of_compounds

        # 携带效应
        Carryover2_True = 0  # 判断是用通用性模板还是特殊模板(元素组)
        if Detectionplatform == "元素":
            Carryover2_True += 1

        Carryoverindex = titleindex
        tableCarryoverindex_start = tableindex
        tableCarryoverindex_end = tableindex+Number_of_compounds//7

        resultCarryover = Carry_over.related_Carryover(id)
        if resultCarryover:
            titleindex += 1
            tableindex += 1

        ## ----稳定性----
        # 1 数据抓取与参数设置
        Stability_data = Sample_Stability.data_scrap(id)  # 抓取数据库中的数据
        Stabilityindex = titleindex  # 设置标题索引
        tableStabilityindex_start = tableindex  # 设置第一个表格索引
        tableStabilityindex_end = tableindex+Number_of_compounds*3-1

        # 2 如果存在数据，自增标题索引和表格索引
        if Stability_data:
            titleindex += 1
            tableindex += Number_of_compounds*2-1

        ## ----参考区间----
        # 1 数据抓取与参数设置
        Reference_Interval_data = Sample_ReferenceInterval.data_scrap(id)  # 抓取数据库中的数据
        Reference_Interval_index = titleindex  # 设置标题索引
        table_Reference_Interval_index_start = tableindex+1  # 设置第一个表格索引,参考区间在一个表格中显示
        # table_Reference_Interval_index_end = tableindex+Number_of_compounds*2-1 # 设置最后一个表格索引索引

        # 2 如果存在数据，自增标题索引和表格索引
        if Reference_Interval_data:
            titleindex += 1
            tableindex += 1

        # 仪器条件
        Test_method_data = testmethod.related_testmethod(id)

        # 设备
        Equipment_data = equipment.related_equipment(id)

        # 试剂耗材
        Reagents_Consumables_data = reagents_consumables.related_Reagents_Consumables(id)

        # 样品处理
        Sample_Preparation_data= sample_preparation.related_Sample_Preparation(id)

        End_conclusion_table = endconclusion.objects.filter(reportinfo_id=id)
        if End_conclusion_table:
            resultEnd_conclusion = []
            for i in End_conclusion_table:
                resultEnd_conclusion.append(i.text)
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
        PNjmdindex = 0  # 重复性精密度副标题索引   6.1

        tablePNindex = tableindex # 重复性精密度表格索引  表3

        # 重复性精密度数据
        PNjmd_data = jmd.related_PNjmd(id)
        if PNjmd_data:
            PNjmdindex += 1  # 重复性精密度副标题索引+1  6.2
            tableindex += Number_of_compounds 
        return render(request, 'report/reportdelete_single.html', locals())

    else:  # 多个化合物
        # 验证原因
        data_Validation_Reason = Validation_Reason.objects.filter(reportinfo_id=id) 
        text_Validation_Reason = []
        for i in data_Validation_Reason:
            text_Validation_Reason.append(i.reason)

        titleindex = 6  # 总标题索引从6开始  -- 6
        tableindex = 3  # 总表格索引从3开始。表1质谱参数，表2液相梯度条件

        # ---------------------------------------1 精密度（每个化合物一个表格）---------------------------------------
        JMDindex = titleindex  # 精密度主标题索引 6
        PNjmdindex = 0  # 重复性精密度副标题索引   6.1

        tablePNindex_start = tableindex # 第一个化合物的表格索引  表3
        tablePNindex_end = tableindex+Number_of_compounds-1 # 最后一个化合物的表格索引  以3个化合物为例，表3+3-1=5

        # 重复性精密度数据
        PNjmd_data = jmd.related_PNjmd(id)
        if PNjmd_data:
            PNjmdindex += 1  # 重复性精密度副标题索引+1  6.2
            tableindex += Number_of_compounds  # 总表格索引+n，以两个化合物为例，开始是表3，现在是表5   表5

        # 中间精密度
        PJjmd_data = jmd.related_PJjmd(id)
        PJjmdindex = PNjmdindex  # 中间精密度副标题索引

        tablePJindex_start = tableindex
        tablePJindex_end = tableindex+Number_of_compounds-1

        # 中间精密度数据
        if PJjmd_data:
            PJjmdindex += 1  # 中间精密度副标题索引+1  -- 6.2
            tableindex += Number_of_compounds  # 总表格索引+n

        # 精密度结论
        if PNjmd_data and PJjmd_data:
            jmdconclusion_data = jmd.related_jmdendconclusion(id)
            JMDconclusionindex = PJjmdindex
            tableJMDconclusionindex = tableindex  # 精密度结论表格索引,不管几个化合物，最终结论都只有一个表格
            if jmdconclusion_data:
                JMDconclusionindex += 1  # 精密度结论副标题索引+1 -- 6.3
                tableindex += 1

        if PNjmd_data or PJjmd_data:  # 如果有重复性精密度和中间精密度,总标题索引+1
            titleindex += 1 # -- 7

        # --------------------------------------- 2 正确度（每个化合物一个表格）---------------------------------------

        ZQDindex = titleindex # 正确度度主标题索引 

        # 1  PT
        PTindex = 0  # PT副标题索引  7.1

        tablePTindex_start = tableindex # 第一个化合物表格索引
        tablePTindex_end = tableindex+Number_of_compounds-1 # 最后一个化合物的表格索引

        PT_data = zqd.related_PT(id)
        if PT_data["PT_dict"]:
            PTindex += 1 # # 正确度副标题索引+1  7.2
            tableindex += Number_of_compounds # 总表格索引+n

        
        # 仪器条件
        Test_method_data = testmethod.related_testmethod(id)

        # 设备
        Equipment_data = equipment.related_equipment(id)

        # 试剂耗材
        Reagents_Consumables_data = reagents_consumables.related_Reagents_Consumables(id)

        # 样品处理
        Sample_Preparation_data= sample_preparation.related_Sample_Preparation(id)

        End_conclusion_table = endconclusion.objects.filter(reportinfo_id=id)
        if End_conclusion_table:
            resultEnd_conclusion = []
            for i in End_conclusion_table:
                resultEnd_conclusion.append(i.text)
    
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
    verifyoccasion_verifyagain = "新项目开发"
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

        # 2 提取html中的字典
        PT_dict = eval(str(request.POST.getlist("Result")[0]))

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

        if PT_judgenum == 0:
            insert_list = []
            for i in PT_norm:
                for j in range(len(PT_dict[i])):
                    insert_list.append(PT(reportinfo=reportinfo, norm=i, Experimentnum=PT_dict[i][j][0], value=PT_dict[i][j][1],
                                          target=PT_dict[i][j][3], received=PT_dict[i][j][2], bias=PT_dict[i][j][4], PT_pass=PT_dict[i][j][5]))

            PT.objects.bulk_create(insert_list)
            HttpResponse = "PT数据保存成功!"
            return render(request, 'report/Datasave.html', locals())

        else:
            HttpResponse = "PT验证结果中含有不通过数据,请核对后重新提交!"
            return render(request, 'report/Warning.html', locals())


def Recyclesave(request):
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
        instrument_num = request.POST["instrument_num"]  # 仪器编号,strip()的作用是去除前后空格
        Detectionplatform = request.POST["Detectionplatform"]  # 项目组
        project = request.POST["project"]  # 项目
        platform = request.POST["platform"]  # 仪器平台(液质,液相,ICP-MS...)
        manufacturers = request.POST["manufacturers"]  # 仪器厂家(AB,Agilent...)
        verifyoccasion = request.POST["verifyoccasion"]  # 验证时机

        dic_recyclesave = eval(str(request.POST.getlist("Recycle_enddict")[0]))
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
        endmedianrecycle = [endmedianrecycle1,
                            endmedianrecycle2, endmedianrecycle3]

        endhighrecycle1 = request.POST.getlist("endhighrecycle1")
        endhighrecycle2 = request.POST.getlist("endhighrecycle2")
        endhighrecycle3 = request.POST.getlist("endhighrecycle3")
        endhighrecycle = [endhighrecycle1, endhighrecycle2, endhighrecycle3]

        # Recycle_enddict的格式为一个列表，列表里只有一个字符串，字符串里又是一个字典，见上述注释，需要先把该字符串里的字典提取出来

        norm = []  # 化合物列表
        for key in dic_recyclesave.keys():
            norm.append(key)

        samnum = []  # 本底个数列表
        for key, value in dic_recyclesave.items():
            samnum.append(len(value))

        samname = ["one", "two", "three", "four", "five",
                   "six", "seven", "eight", "nine", "ten"]  # 本底后缀
        for i in range(len(norm)):
            norm_dict = dic_recyclesave[norm[i]]
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

        print(dic_recyclesave)

        reportinfo = ReportInfo.objects.get(
            number=request.POST["instrument_num"], project=request.POST["project"])

        recycle_judgenum = 0
        for i in endlowrecycle:
            for j in i:
                if "不通过" in j:
                    recycle_judgenum += 1

        for i in endmedianrecycle:
            for j in i:
                if "不通过" in j:
                    recycle_judgenum += 1

        for i in endhighrecycle:
            for j in i:
                if "不通过" in j:
                    recycle_judgenum += 1

        level = ["L", "M", "H"]
        if recycle_judgenum == 0:
            insert_list = []
            for key, value in dic_recyclesave.items():  # 循环本底
                for r, c in value.items():
                    for j in range(len(level)):
                        insert_list.append(RECYCLE(reportinfo=reportinfo, norm=key, Experimentnum=r, level=level[j],
                                                   sam_conc=c[j], theory_conc=c[j+12], end_conc1=c[3 *
                                                                                                   j+3], end_conc2=c[3*j+4], end_conc3=c[3*j+5],
                                                   end_recycle1=c[3*j+15], end_recycle2=c[3*j+16], end_recycle3=c[3*j+17]))

            RECYCLE.objects.bulk_create(insert_list)  # 这种保存数据方法较省时间
            HttpResponse = "加标回收率数据保存成功!"
            return render(request, 'report/Datasave.html', locals())

        else:
            # 展示数据需要，后续需把这段代码删除
            insert_list = []
            for key, value in dic_recyclesave.items():  # 循环本底
                for r, c in value.items():
                    for j in range(len(level)):
                        insert_list.append(RECYCLE(reportinfo=reportinfo, norm=key, Experimentnum=r, level=level[j],
                                                   sam_conc=c[j], theory_conc=c[j+12], end_conc1=c[3 *
                                                                                                   j+3], end_conc2=c[3*j+4], end_conc3=c[3*j+5],
                                                   end_recycle1=c[3*j+15], end_recycle2=c[3*j+16], end_recycle3=c[3*j+17]))

            RECYCLE.objects.bulk_create(insert_list)  # 这种保存数据方法较省时间
            HttpResponse = "加标回收率验证结果中含有不通过数据,请核对后重新提交!"
            return render(request, 'report/HttpResponse-danger.html', locals())


# 接收验证界面LOQ指标传递过来的参数(图片名称)
def AMRsave(request):
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
        Detectionplatform = request.POST["Detectionplatform"]  # 项目组
        project = request.POST["project"]  # 项目
        platform = request.POST["platform"]  # 仪器平台(液质,液相,ICP-MS...)
        manufacturers = request.POST["manufacturers"]  # 仪器厂家(AB,Agilent...)
        verifyoccasion = request.POST["verifyoccasion"]  # 验证时机

        judgenum = int(request.POST.getlist("judgenum")[0])  # 判断验证结果是否通过
        picturename = request.POST.getlist("picturename")
        AMR_id = int(request.POST.getlist("id")[0])
        objs = AMRpicture.objects.filter(reportinfo_id=AMR_id)

        if judgenum == 0:
            for index, i in enumerate(objs):
                AMRpicture.objects.filter(img=i.img).update(
                    name=picturename[index])  # 更新数据库中的图片名称
            HttpResponse = "方法定量限与线性范围数据保存成功!"
            return render(request, 'report/Datasave.html', locals())
        else:
            # for index,i in enumerate(objs):
            #     AMRpicture.objects.filter(img=i.img).update(name=picturename[index]) #更新数据库中的图片名称
            # HttpResponse="方法定量限与线性范围数据保存成功!"
            # for index,i in enumerate(objs):
            #     AMRpicture.objects.filter(img=i.img).delete() #删除对应对应报告的图片
            for index, i in enumerate(objs):
                AMRpicture.objects.filter(img=i.img).update(
                    name=picturename[index])  # 更新数据库中的图片名称
            HttpResponse = "方法定量限与线性范围验证结果中含有不通过数据,请核对后重新提交!"
            return render(request, 'report/HttpResponse-danger.html', locals())


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

        # print("111111")
        # print(objfile_list)
        # print(type(objfile_list))

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
        print(request.POST)
        # 仪器编号,strip()的作用是去除前后空格
        instrument_num = request.POST["instrument_num"]
        group = request.POST["group"]  # 项目组
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
            AMRconsluion.objects.create(
                reportinfo_id=id, name=compound[i], lodconclusion=lod[i], loqconclusion=loq[i], amrconclusion=amr[i])

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
        # print(request.POST)
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
