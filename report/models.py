from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


# 一 各验证指标数据存储表
# 1 主表
class ReportInfo(models.Model):
    number = models.CharField(max_length=32)  # 仪器编号
    Detectionplatform = models.CharField(max_length=32)  # 检测平台
    project = models.CharField(max_length=32)  # 检测项目
    platform = models.CharField(max_length=32)  # 仪器平台
    manufacturers = models.CharField(max_length=32)  # 仪器厂家
    verifyoccasion = models.CharField(max_length=32)  # 验证时机
    verifytime = models.DateField(auto_now_add=True)  # 验证时间

# 2 验证原因表
class Validation_Reason(models.Model):
    reportinfo = models.ForeignKey(ReportInfo, on_delete=models.CASCADE)  # 外键
    reason = models.CharField(max_length=500)  # 验证原因

# 3 各验证指标表
# 3.1 精密度(重复性精密度，中间精密度)
class JMD(models.Model):
    reportinfo = models.ForeignKey(ReportInfo, on_delete=models.CASCADE)  # 外键
    Experimentnum = models.CharField(max_length=32)  # 实验号
    norm = models.CharField(max_length=32)  # 化合物：D2,D3
    namejmd = models.CharField(max_length=32)  # 精密度名称：批内,批间
    low = models.CharField(max_length=32)  # 低浓度
    median = models.CharField(max_length=32)  # 中浓度
    high = models.CharField(max_length=32)  # 高浓度

# 3.2 PT
class PT(models.Model):
    reportinfo = models.ForeignKey(ReportInfo, on_delete=models.CASCADE)  # 外键
    Experimentnum = models.CharField(max_length=32)  # 实验号
    norm = models.CharField(max_length=32)  # 指标：MN,NMN,3-MT
    value = models.CharField(max_length=32)  # 结果

    templates = models.CharField(max_length=32)  # 模板

    # 模板1:可接受区间 需要用到的字段
    accept1 = models.CharField(max_length=32)  # 可接受区间下限
    accept2 = models.CharField(max_length=32)  # 可接收区间上限

    # 模板2:可接受标准 需要用到的字段
    target = models.CharField(max_length=32)  # 靶值(需手动输入)
    received = models.CharField(max_length=32)  # 可接受标准
    bias = models.CharField(max_length=32)  # 偏倚

    # 通用字段
    PT_pass = models.CharField(max_length=32)  # 是否通过

# 3.3 仪器比对
class InstrumentCompare(models.Model):
    reportinfo = models.ForeignKey(ReportInfo, on_delete=models.CASCADE)  # 外键
    textarea = models.CharField(max_length=32)  # 文字输入框

# 3.3 加标回收率
class RECYCLE(models.Model):
    reportinfo = models.ForeignKey(ReportInfo, on_delete=models.CASCADE)  # 外键
    Experimentnum = models.CharField(max_length=32)  # 本底：sam1,sam2,sam3
    norm = models.CharField(max_length=32)  # 指标：MN,NMN,3-MT
    level = models.CharField(max_length=32)  # 低中高
    sam_conc = models.CharField(max_length=32)  # 本底结果
    theory_conc = models.CharField(max_length=32)  # 本底加标理论值
    end_conc1 = models.CharField(max_length=32)  # 本底浓度最终值1
    end_conc2 = models.CharField(max_length=32)  # 本底浓度最终值2
    end_conc3 = models.CharField(max_length=32)  # 本底浓度最终值3
    end_recycle1 = models.CharField(max_length=32)  # 回收率1
    end_recycle2 = models.CharField(max_length=32)  # 回收率2
    end_recycle3 = models.CharField(max_length=32)  # 回收率3

# 3.4 线性测量范围-AMR
# 3.4.1 数据
class AMR(models.Model):
    reportinfo = models.ForeignKey(ReportInfo, on_delete=models.CASCADE)  # 外键
    Experimentnum = models.CharField(max_length=32)  # 曲线：S1,S2,S3...
    norm = models.CharField(max_length=32)  # 指标：MN,NMN,3-MT
    therory_conc = models.CharField(max_length=32)  # 理论浓度
    test_conc1 = models.CharField(max_length=32)  # 检测值1
    test_conc2 = models.CharField(max_length=32)  # 检测值2
    test_conc3 = models.CharField(max_length=32)  # 检测值3
    test_conc4 = models.CharField(max_length=32)  # 检测值4
    test_conc5 = models.CharField(max_length=32)  # 检测值5
    test_conc6 = models.CharField(max_length=32)  # 检测值6
    recycle1 = models.CharField(max_length=32)  # 回收率1
    recycle2 = models.CharField(max_length=32)  # 回收率2
    recycle3 = models.CharField(max_length=32)  # 回收率3
    recycle4 = models.CharField(max_length=32)  # 回收率4
    recycle5 = models.CharField(max_length=32)  # 回收率5
    recycle6 = models.CharField(max_length=32)  # 回收率6
    meanrecycle = models.CharField(max_length=32)  # 平均回收率
    cvtest_conc = models.CharField(max_length=32)  # 检测值CV

# 3.4.2 图片
class AMRpicture(models.Model):
    reportinfo = models.ForeignKey(ReportInfo, on_delete=models.CASCADE)  # 外键
    # 由于settings.py中MEDIA_ROOT的设置，upload_to会将图片默认保存在test1下的media文件夹下的img文件夹中
    img = models.ImageField(upload_to='img', null=True)
    name = models.CharField(max_length=32)  # 图片名称

# 删除报告时，相应文件夹中的图片文件也相应删除
@receiver(pre_delete, sender=AMRpicture)
def mymodel_delete(sender, instance, **kwargs):
    instance.img.delete(False)


# 3.5 方法检出限-LOD
# 3.5.1 数据
class LOD(models.Model):
    reportinfo = models.ForeignKey(ReportInfo, on_delete=models.CASCADE)  # 外键
    Experimentnum = models.CharField(max_length=32)  # 实验号
    norm = models.CharField(max_length=32)  # 化合物：D2,D3
    result = models.CharField(max_length=32)  # 结果数据

# 3.5.2 图片
class LODpicture(models.Model):
    reportinfo = models.ForeignKey(ReportInfo, on_delete=models.CASCADE)  # 外键
    img = models.ImageField(upload_to='img2', null=True)
    name = models.CharField(max_length=32)  # 图片名称
    conclusion = models.CharField(max_length=500)  # 结论

# 3.6 结论
class AMRconsluion(models.Model):
    reportinfo = models.ForeignKey(ReportInfo, on_delete=models.CASCADE)  # 外键
    name = models.CharField(max_length=32)  # 化合物
    lodconclusion = models.CharField(max_length=500)
    loqconclusion = models.CharField(max_length=500)
    amrconclusion = models.CharField(max_length=500)

# 3.7 临床可报告范围1(需上传文件)
class CRR(models.Model):
    reportinfo = models.ForeignKey(ReportInfo, on_delete=models.CASCADE)  # 外键
    Dilution = models.CharField(max_length=32)  # 稀释倍数
    norm = models.CharField(max_length=32)  # 指标：MN,NMN,3-MT
    test_conc1 = models.CharField(max_length=32)  # 检测值1
    test_conc2 = models.CharField(max_length=32)  # 检测值2
    test_conc3 = models.CharField(max_length=32)  # 检测值3
    test_conc4 = models.CharField(max_length=32)  # 检测值4
    test_conc5 = models.CharField(max_length=32)  # 检测值5
    mean_conc = models.CharField(max_length=32)  # 检测值均值
    cv_conc = models.CharField(max_length=32)  # 检测值cv
    calresults = models.CharField(max_length=32)  # 计算结果(检测均值或回收率)

# 3.8 临床可报告范围2(无需上传文件)
class CRR2(models.Model):
    reportinfo = models.ForeignKey(ReportInfo, on_delete=models.CASCADE)  # 外键
    norm = models.CharField(max_length=32)  # 指标：MN,NMN,3-MT
    crr = models.CharField(max_length=32)  # 临床可报告范围

# 3.9 基质特异性
class MS(models.Model):
    reportinfo = models.ForeignKey(ReportInfo, on_delete=models.CASCADE)  # 外键
    img = models.ImageField(upload_to='img', null=True)
    name = models.CharField(max_length=32)  # 图片名称
    conclusion = models.CharField(max_length=200)  # 结论

# 3.10 携带效应1(通用性表格:适用于VD,药物浓度等)
class Carryover(models.Model):
    reportinfo = models.ForeignKey(ReportInfo, on_delete=models.CASCADE)  # 外键
    norm = models.CharField(max_length=32)  # 指标：D2,D3
    systermnum = models.CharField(max_length=32)  # 针对多系统情况：系统编号
    C1_1 = models.CharField(max_length=32)
    C2_1 = models.CharField(max_length=32)
    C3_1 = models.CharField(max_length=32)
    C1_2 = models.CharField(max_length=32)
    C2_2 = models.CharField(max_length=32)
    C3_2 = models.CharField(max_length=32)
    C1_3 = models.CharField(max_length=32)
    C2_3 = models.CharField(max_length=32)
    C3_3 = models.CharField(max_length=32)
    C1mean = models.CharField(max_length=32)
    C3mean = models.CharField(max_length=32)
    bias = models.FloatField()

# 3.11 携带效应2(特殊表格:适用于元素等)
class Carryover2(models.Model):
    reportinfo = models.ForeignKey(ReportInfo, on_delete=models.CASCADE)  # 外键
    norm = models.CharField(max_length=32)  # 指标：D2,D3
    L01 = models.CharField(max_length=32)
    L02 = models.CharField(max_length=32)
    L03 = models.CharField(max_length=32)
    H04 = models.CharField(max_length=32)
    H05 = models.CharField(max_length=32)
    L06 = models.CharField(max_length=32)
    H07 = models.CharField(max_length=32)
    H08 = models.CharField(max_length=32)
    L09 = models.CharField(max_length=32)
    L10 = models.CharField(max_length=32)
    L11 = models.CharField(max_length=32)
    L12 = models.CharField(max_length=32)
    H13 = models.CharField(max_length=32)
    H14 = models.CharField(max_length=32)
    L15 = models.CharField(max_length=32)
    H16 = models.CharField(max_length=32)
    H17 = models.CharField(max_length=32)
    L18 = models.CharField(max_length=32)
    H19 = models.CharField(max_length=32)
    H20 = models.CharField(max_length=32)
    L21 = models.CharField(max_length=32)
    X1 = models.CharField(max_length=32)
    X2 = models.CharField(max_length=32)
    SD1 = models.CharField(max_length=32)

# 3.12 基质效应
class Matrixeffect(models.Model):
    reportinfo = models.ForeignKey(ReportInfo, on_delete=models.CASCADE)  # 外键
    samplename = models.CharField(max_length=32)  # 样本编号:A,B,C,D...
    norm = models.CharField(max_length=32)  # 指标：D2,D3
    Area_1 = models.CharField(max_length=32)
    IS_Area_1 = models.CharField(max_length=32)
    Area_IS_Area_1 = models.CharField(max_length=32)
    Area_2 = models.CharField(max_length=32)
    IS_Area_2 = models.CharField(max_length=32)
    Area_IS_Area_2 = models.CharField(max_length=32)
    Area_3 = models.CharField(max_length=32)
    IS_Area_3 = models.CharField(max_length=32)
    Area_IS_Area_3 = models.CharField(max_length=32)
    singlemean = models.CharField(max_length=32)  # 单一样本均值
    complexmean = models.CharField(max_length=32)  # 混合样本均值
    bias1 = models.CharField(max_length=32)
    bias2 = models.CharField(max_length=32)
    bias3 = models.CharField(max_length=32)

# 3.13 样品稳定性
class Stability(models.Model):
    reportinfo = models.ForeignKey(ReportInfo, on_delete=models.CASCADE)  # 外键
    norm = models.CharField(max_length=32)  # 化合物名称
    temperature = models.CharField(max_length=32)  # 验证温度：室温，冷藏，冷冻
    time = models.FloatField()  # 验证时间：0h,5h,24h,48h...
    L01 = models.CharField(max_length=32)  # 低浓度水平1
    L02 = models.CharField(max_length=32)  # 低浓度水平2
    L03 = models.CharField(max_length=32)  # 低浓度水平3
    M01 = models.CharField(max_length=32)  # 中浓度水平1
    M02 = models.CharField(max_length=32)  # 中浓度水平2
    M03 = models.CharField(max_length=32)  # 中浓度水平3
    H01 = models.CharField(max_length=32)  # 高浓度水平1
    H02 = models.CharField(max_length=32)  # 高浓度水平2
    H03 = models.CharField(max_length=32)  # 高浓度水平3

# 3.14 参考区间
class Reference_Interval(models.Model):
    reportinfo = models.ForeignKey(ReportInfo, on_delete=models.CASCADE)  # 外键
    norm = models.CharField(max_length=32)  # 化合物
    Experimentnum = models.CharField(max_length=32)  # 实验号
    Result = models.CharField(max_length=32)  # 结果


##########################分界线###############################


# 二 后台admin管理后台相关数据表

# 1 通用性参数设置

# 1.1 主表
class General(models.Model):
    name = models.CharField(max_length=32, verbose_name="项目名称")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "general table"
        verbose_name = "通用性参数设置"
        verbose_name_plural = "1 通用性参数设置"


# 重复性精密度
class Repeatprecisiongeneral(models.Model):
    general = models.OneToOneField(General, verbose_name="方法学报告性能验证指标", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=32, verbose_name="验证指标", blank=True, editable=False)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "重复性精密度"
        verbose_name_plural = "重复性精密度"


class Repeatprecisiongeneralmethod(models.Model):
    repeatprecisiongeneral = models.OneToOneField(Repeatprecisiongeneral, verbose_name="重复性精密度", on_delete=models.CASCADE)
    minSample = models.IntegerField("所需最小样本数")
    maxCV = models.FloatField("最大允许CV(%)")

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "基本参数"
        verbose_name_plural = "基本参数"


class Repeatprecisiongeneraltexts(models.Model):
    repeatprecisiongeneral = models.ForeignKey(Repeatprecisiongeneral, verbose_name="重复性精密度", on_delete=models.CASCADE)
    text = models.TextField("描述性内容", max_length=500, blank=True)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "描述性内容"
        verbose_name_plural = "描述性内容"

# 中间精密度
class Interprecisiongeneral(models.Model):
    general = models.OneToOneField(General, verbose_name="方法学报告性能验证指标", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=32, verbose_name="验证指标", blank=True, editable=False)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "中间精密度"
        verbose_name_plural = "中间精密度"


class Interprecisiongeneralmethod(models.Model):
    interprecisiongeneral = models.OneToOneField(Interprecisiongeneral, verbose_name="中间精密度", on_delete=models.CASCADE)
    minSample = models.IntegerField("所需最小样本数")
    maxCV = models.FloatField("最大允许CV(%)")

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "基本参数"
        verbose_name_plural = "基本参数"


class Interprecisiongeneraltexts(models.Model):
    interprecisiongeneral = models.ForeignKey(Interprecisiongeneral, verbose_name="中间精密度", on_delete=models.CASCADE)
    text = models.TextField("描述性内容", max_length=500, blank=True)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "描述性内容"
        verbose_name_plural = "描述性内容"

# PT
class PTgeneral(models.Model):
    general = models.OneToOneField(General, verbose_name="方法学报告性能验证指标", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=32, verbose_name="验证指标", blank=True, editable=False)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "PT"
        verbose_name_plural = "PT"


class PTgeneralmethod(models.Model):
    pTgeneral = models.OneToOneField(PTgeneral, verbose_name="PT", on_delete=models.CASCADE)
    minSample = models.IntegerField("所需最小样本数", blank=True)
    minPass = models.FloatField("最低通过率CV(%)", blank=True)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "基本参数"
        verbose_name_plural = "基本参数"


class PTgeneraltexts(models.Model):
    pTgeneral = models.ForeignKey(PTgeneral, verbose_name="PT", on_delete=models.CASCADE)
    text = models.TextField("描述性内容", max_length=500)

    class Meta:
        verbose_name = "描述性内容"
        verbose_name_plural = "描述性内容"

# 加标回收


class Recyclegeneral(models.Model):
    general = models.OneToOneField(General, verbose_name="方法学报告性能验证指标", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=32, verbose_name="验证指标", blank=True, editable=False)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "加标回收率"
        verbose_name_plural = "加标回收率"


class Recyclegeneralmethod(models.Model):
    recyclegeneral = models.OneToOneField(Recyclegeneral, verbose_name="加标回收率", on_delete=models.CASCADE)
    lowvalue = models.FloatField("回收率下限(%)")
    upvalue = models.FloatField("回收率上限(%)")

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "基本参数"
        verbose_name_plural = "基本参数"


class Recyclegeneraltexts(models.Model):
    recyclegeneral = models.ForeignKey(Recyclegeneral, verbose_name="加标回收率", on_delete=models.CASCADE)
    text = models.TextField("描述性内容", max_length=500)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "描述性内容"
        verbose_name_plural = "描述性内容"

# AMR(分析灵敏度与分析测量范围)
class AMRgeneral(models.Model):
    general = models.OneToOneField(General, verbose_name="方法学报告性能验证指标", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=32, verbose_name="验证指标", blank=True, editable=False)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "分析灵敏度与分析测量范围"
        verbose_name_plural = "分析灵敏度与分析测量范围"


class AMRgeneralmethod(models.Model):
    aMRgeneral = models.OneToOneField(AMRgeneral, verbose_name="AMR", on_delete=models.CASCADE)
    lowvalue = models.FloatField("回收率下限(%)")
    upvalue = models.FloatField("回收率上限(%)")
    cv = models.FloatField("最大允许CV(%)")

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "基本参数"
        verbose_name_plural = "基本参数"


class AMRgeneraltexts(models.Model):
    aMRgeneral = models.ForeignKey(AMRgeneral, verbose_name="AMR", on_delete=models.CASCADE)
    text = models.TextField("描述性内容", max_length=500)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "描述性内容"
        verbose_name_plural = "描述性内容"

# JCX(检出限)
class JCXgeneral(models.Model):
    general = models.OneToOneField(General, verbose_name="方法学报告性能验证指标", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=32, verbose_name="验证指标", blank=True, editable=False)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "检出限"
        verbose_name_plural = "检出限"

class JCXgeneraltexts(models.Model):
    jCXgeneral = models.ForeignKey(JCXgeneral, verbose_name="JCX", on_delete=models.CASCADE)
    text = models.TextField("描述性内容", max_length=500)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "描述性内容"
        verbose_name_plural = "描述性内容"

# CRR(临床可报告范围)
class CRRgeneral(models.Model):
    general = models.OneToOneField(General, verbose_name="方法学报告性能验证指标", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=32, verbose_name="验证指标", blank=True, editable=False)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "临床可报告范围"
        verbose_name_plural = "临床可报告范围"


class CRRgeneralmethod(models.Model):
    cRRgeneral = models.OneToOneField(CRRgeneral, verbose_name="CRR", on_delete=models.CASCADE)
    lowvalue = models.FloatField("回收率下限(%)")
    upvalue = models.FloatField("回收率上限(%)")

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "基本参数"
        verbose_name_plural = "基本参数"


class CRRgeneraltexts(models.Model):
    cRRgeneral = models.ForeignKey(CRRgeneral, verbose_name="CRR", on_delete=models.CASCADE)
    text = models.TextField("描述性内容", max_length=500)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "描述性内容"
        verbose_name_plural = "描述性内容"


# MS(基质特异性)
class MSgeneral(models.Model):
    general = models.OneToOneField(General, verbose_name="方法学报告性能验证指标", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=32, verbose_name="验证指标", blank=True, editable=False)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "基质特异性"
        verbose_name_plural = "基质特异性"


class MSgeneraltexts(models.Model):
    mSgeneral = models.ForeignKey(MSgeneral, verbose_name="基质特异性", on_delete=models.CASCADE)
    text = models.TextField("描述性内容", max_length=500)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "描述性内容"
        verbose_name_plural = "描述性内容"

# Carryover(携带效应)
class Carryovergeneral(models.Model):
    general = models.OneToOneField(General, verbose_name="方法学报告性能验证指标", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=32, verbose_name="验证指标", blank=True, editable=False)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "携带效应"
        verbose_name_plural = "携带效应"


class Carryovergeneralmethod(models.Model):
    carryovergeneral = models.OneToOneField(Carryovergeneral, verbose_name="携带效应", on_delete=models.CASCADE)
    acceptable = models.FloatField("可接受标准(%)")

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "基本参数"
        verbose_name_plural = "基本参数"


class Carryovergeneraltexts(models.Model):
    carryovergeneral = models.ForeignKey(Carryovergeneral, verbose_name="携带效应", on_delete=models.CASCADE)
    text = models.TextField("描述性内容", max_length=500)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "描述性内容"
        verbose_name_plural = "描述性内容"

# 基质效应
class Matrixeffectgeneral(models.Model):
    general = models.OneToOneField(General, verbose_name="方法学报告性能验证指标", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=32, verbose_name="验证指标", blank=True, editable=False)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "基质效应"
        verbose_name_plural = "基质效应"


class Matrixeffectgeneralmethod(models.Model):
    matrixeffectgeneral = models.OneToOneField(Matrixeffectgeneral, verbose_name="基质效应", on_delete=models.CASCADE)
    bias = models.FloatField("最大允许偏差(%)")

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "基本参数"
        verbose_name_plural = "基本参数"


class Matrixeffectgeneraltexts(models.Model):
    matrixeffectgeneral = models.ForeignKey(Matrixeffectgeneral, verbose_name="基质效应", on_delete=models.CASCADE)
    text = models.TextField("描述性内容", max_length=500)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "描述性内容"
        verbose_name_plural = "描述性内容"

# 稳定性
# 1  样品处理后稳定性
class Stabilitygeneral(models.Model):
    general = models.OneToOneField(General, verbose_name="方法学报告性能验证指标", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=32, verbose_name="验证指标", blank=True, editable=False)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "样品稳定性"
        verbose_name_plural = "样品稳定性"


class Stabilitygeneralmethod(models.Model):
    stabilitygeneral = models.OneToOneField(Stabilitygeneral, verbose_name="回收率", on_delete=models.CASCADE)
    lowvalue = models.FloatField("回收率下限(%)")
    upvalue = models.FloatField("回收率上限(%)")

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "基本参数"
        verbose_name_plural = "基本参数"


class Stabilitygeneraltexts(models.Model):
    stabilitygeneral = models.ForeignKey(Stabilitygeneral, verbose_name="", on_delete=models.CASCADE)
    text = models.TextField("描述性内容", max_length=500)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "描述性内容"
        verbose_name_plural = "描述性内容"

# 参考区间
class Referenceintervalgeneral(models.Model):
    general = models.OneToOneField(General, verbose_name="方法学报告性能验证指标", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=32, verbose_name="验证指标", blank=True, editable=False)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "参考区间"
        verbose_name_plural = "参考区间"

class Referenceintervalgeneraltexts(models.Model):
    referenceintervalgeneral = models.ForeignKey(Referenceintervalgeneral, verbose_name="", on_delete=models.CASCADE)
    text = models.TextField("描述性内容", max_length=500)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "描述性内容"
        verbose_name_plural = "描述性内容"
        
# 2  各项目参数设置

# 2.1 主表
class Special(models.Model):
    # group = models.CharField(max_length=32,verbose_name = "项目组")
    内分泌检测平台 = '内分泌检测平台'
    遗传代谢病检测平台 = '遗传代谢病检测平台'
    微量营养素检测平台 = '微量营养素检测平台'
    治疗药物检测平台 = '治疗药物检测平台'
    研发与创新平台 = '研发与创新平台'
    Detectionplatform_CHOICES = (
        ('内分泌检测平台', '内分泌检测平台'),
        ('遗传代谢病检测平台', '遗传代谢病检测平台'),
        ('微量营养素检测平台', '微量营养素检测平台'),
        ('治疗药物检测平台', '治疗药物检测平台'),
        ('研发与创新平台', '研发与创新平台'),
    )
    Detectionplatform = models.CharField(max_length=16, choices=Detectionplatform_CHOICES, verbose_name="检测平台")
    project = models.CharField(max_length=32, verbose_name="项目名称", unique=True)  # unique=True设置项目不可重复
    chinese_titie = models.TextField(max_length=200, verbose_name="中文标题", blank=True)
    english_titie = models.TextField(max_length=200, verbose_name="英文标题", blank=True)
    unit = models.CharField(max_length=200, verbose_name="单位")
    Effective_digits = models.IntegerField("有效位数")
    Number_of_compounds = models.IntegerField("化合物个数")

    def __str__(self):
        return self.project

    class Meta:
        verbose_name = "各项目参数设置"
        verbose_name_plural = "2 各项目参数设置"


# 重复性精密度
class Repeatprecisionspecial(models.Model):
    special = models.OneToOneField(Special, verbose_name="特殊参数设置", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=32, verbose_name="验证指标",blank=True, default="重复性精密度", editable=False)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "重复性精密度"
        verbose_name_plural = "重复性精密度"


class Repeatprecisionspecialmethod(models.Model):
    repeatprecisionspecial = models.OneToOneField(Repeatprecisionspecial, verbose_name="重复性精密度", on_delete=models.CASCADE)
    minSample = models.IntegerField("所需最小样本数", blank=True)
    maxCV = models.FloatField("最大允许CV(%)", blank=True)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "基本参数"
        verbose_name_plural = "基本参数"


class Repeatprecisionspecialtexts(models.Model):
    repeatprecisionspecial = models.ForeignKey(Repeatprecisionspecial, verbose_name="重复性精密度", on_delete=models.CASCADE)
    text = models.TextField("描述性内容", max_length=500, blank=True)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "描述性内容"
        verbose_name_plural = "描述性内容"


# 中间精密度
class Interprecisionspecial(models.Model):
    special = models.OneToOneField(Special, verbose_name="特殊参数设置", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=32, verbose_name="验证指标",blank=True, default="中间精密度", editable=False)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "中间精密度"
        verbose_name_plural = "中间精密度"


class Interprecisionspecialmethod(models.Model):
    interprecisionspecial = models.OneToOneField(Interprecisionspecial, verbose_name="中间精密度", on_delete=models.CASCADE)
    minSample = models.IntegerField("所需最小样本数", blank=True)
    maxCV = models.FloatField("最大允许CV(%)", blank=True)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "基本参数"
        verbose_name_plural = "基本参数"


class Interprecisionspecialtexts(models.Model):
    interprecisionspecial = models.ForeignKey(Interprecisionspecial, verbose_name="中间精密度", on_delete=models.CASCADE)
    text = models.TextField("描述性内容", max_length=500, blank=True)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "描述性内容"
        verbose_name_plural = "描述性内容"


# PT
class PTspecial(models.Model):
    special = models.OneToOneField(Special, verbose_name="特殊参数设置", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=32, verbose_name="验证指标", blank=True, default="PT", editable=False)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "PT"
        verbose_name_plural = "PT"


class PTspecialmethod(models.Model):
    pTspecial = models.OneToOneField(PTspecial, verbose_name="PT", on_delete=models.CASCADE)
    minSample = models.IntegerField("所需最小样本数", blank=True)
    minPass = models.FloatField("最低通过率CV(%)", blank=True)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "基本参数"
        verbose_name_plural = "基本参数"


class PTspecialtexts(models.Model):
    pTspecial = models.ForeignKey(PTspecial, verbose_name="PT", on_delete=models.CASCADE)
    text = models.TextField("描述性内容", max_length=500)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "描述性内容"
        verbose_name_plural = "描述性内容"


class PTspecialaccept(models.Model):
    pTspecial = models.ForeignKey(PTspecial, verbose_name="PT", on_delete=models.CASCADE)
    norm = models.CharField(max_length=32, verbose_name="化合物名称", blank=True, null=True)
    unit = models.CharField(max_length=32, verbose_name="单位", blank=True, null=True)
    digits = models.IntegerField("有效位数", blank=True, null=True)
    range1 = models.FloatField("可接受标准一适用范围(<=)", blank=True, null=True)
    accept1 = models.FloatField("可接受标准一(差值)", blank=True, null=True)
    range2 = models.FloatField("可接受标准二适用范围(>)", blank=True, null=True)
    accept2 = models.FloatField("可接受标准二(比值%)", blank=True, null=True)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "可接受标准"
        verbose_name_plural = "可接受标准"

class PTspecialBoolean(models.Model):
    pTspecial = models.OneToOneField(PTspecial, verbose_name="PT", on_delete=models.CASCADE)
    Boolean = models.BooleanField(verbose_name="结果不通过时是否关联数据进入报告", blank=True, null=True)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "数据关联"
        verbose_name_plural = "数据关联"


# 加标回收
class Recyclespecial(models.Model):
    special = models.OneToOneField(Special, verbose_name="特殊参数设置", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=32, verbose_name="验证指标",blank=True, default="加标回收率", editable=False)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "加标回收率"
        verbose_name_plural = "加标回收率"


class Recyclespecialmethod(models.Model):
    recyclespecial = models.OneToOneField(Recyclespecial, verbose_name="加标回收率", on_delete=models.CASCADE)
    lowvalue = models.FloatField("回收率下限(%)", blank=True)
    upvalue = models.FloatField("回收率上限(%)", blank=True)

    class Meta:
        verbose_name = "基本参数"
        verbose_name_plural = "基本参数"


class Recyclespecialtexts(models.Model):
    recyclespecial = models.ForeignKey(Recyclespecial, verbose_name="加标回收率", on_delete=models.CASCADE)
    text = models.TextField("描述性内容", max_length=500)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "描述性内容"
        verbose_name_plural = "描述性内容"

# AMR
class AMRspecial(models.Model):
    special = models.OneToOneField(Special, verbose_name="特殊参数设置", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=32, verbose_name="验证指标",blank=True, default="线性灵敏度和线性范围", editable=False)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "线性灵敏度和线性测量范围"
        verbose_name_plural = "线性灵敏度和线性测量范围"


class AMRspecialmethod(models.Model):
    aMRspecial = models.OneToOneField(AMRspecial, verbose_name="AMR", on_delete=models.CASCADE)
    lowvalue = models.FloatField("回收率下限(%)", blank=True)
    upvalue = models.FloatField("回收率上限(%)", blank=True)
    cv = models.FloatField("最大允许CV(%)", blank=True)

    class Meta:
        verbose_name = "基本参数"
        verbose_name_plural = "基本参数"


class AMRspecialtexts(models.Model):
    aMRspecial = models.ForeignKey(AMRspecial, verbose_name="AMR", on_delete=models.CASCADE)
    text = models.TextField("描述性内容", max_length=500)

    class Meta:
        verbose_name = "描述性内容"
        verbose_name_plural = "描述性内容"

# 检出限
class JCXspecial(models.Model):
    special = models.OneToOneField(Special, verbose_name="特殊参数设置", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=32, verbose_name="验证指标", blank=True, default="检出限", editable=False)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "检出限"
        verbose_name_plural = "检出限"


class JCXspecialtexts(models.Model):
    jCXspecial = models.ForeignKey(JCXspecial, verbose_name="JCX", on_delete=models.CASCADE)
    text = models.TextField("描述性内容", max_length=500)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "描述性内容"
        verbose_name_plural = "描述性内容"

# 临床可报告范围
class CRRspecial(models.Model):
    special = models.OneToOneField(Special, verbose_name="特殊参数设置", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=32, verbose_name="验证指标",blank=True, default="临床可报告范围", editable=False)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "临床可报告范围"
        verbose_name_plural = "临床可报告范围"


class CRRspecialmethod(models.Model):
    cRRspecial = models.OneToOneField(CRRspecial, verbose_name="CRR", on_delete=models.CASCADE)
    lowvalue = models.FloatField("回收率下限(%)", blank=True)
    upvalue = models.FloatField("回收率上限(%)", blank=True)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "基本参数"
        verbose_name_plural = "基本参数"


class CRRspecialtexts(models.Model):
    cRRspecial = models.ForeignKey(CRRspecial, verbose_name="CRR", on_delete=models.CASCADE)
    text = models.TextField("描述性内容", max_length=500)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "描述性内容"
        verbose_name_plural = "描述性内容"

# 基质特异性
class MSspecial(models.Model):
    special = models.OneToOneField(Special, verbose_name="特殊参数设置", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=32, verbose_name="验证指标",blank=True, default="基质特异性", editable=False)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "基质特异性"
        verbose_name_plural = "基质特异性"


class MSspecialtexts(models.Model):
    mSspecial = models.ForeignKey(MSspecial, verbose_name="基质特异性", on_delete=models.CASCADE)
    text = models.TextField("描述性内容", max_length=500)

    class Meta:
        verbose_name = "描述性内容"
        verbose_name_plural = "描述性内容"

# 携带效应
class Carryoverspecial(models.Model):
    special = models.OneToOneField(Special, verbose_name="特殊参数设置", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=32, verbose_name="验证指标", blank=True, default="携带效应", editable=False)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "携带效应"
        verbose_name_plural = "携带效应"


class Carryoverspecialmethod(models.Model):
    carryoverspecial = models.OneToOneField(Carryoverspecial, verbose_name="携带效应", on_delete=models.CASCADE)
    accept = models.FloatField("可接受标准(%)", blank=True)

    class Meta:
        verbose_name = "基本参数"
        verbose_name_plural = "基本参数"


class Carryoverspecialtexts(models.Model):
    carryoverspecial = models.ForeignKey(Carryoverspecial, verbose_name="携带效应", on_delete=models.CASCADE)
    text = models.TextField("描述性内容", max_length=500)

    class Meta:
        verbose_name = "描述性内容"
        verbose_name_plural = "描述性内容"


# 基质效应
class Matrixeffectspecial(models.Model):
    special = models.OneToOneField(Special, verbose_name="特殊参数设置", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=32, verbose_name="验证指标", blank=True, default="基质效应", editable=False)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "基质效应"
        verbose_name_plural = "基质效应"


class Matrixeffectspecialmethod(models.Model):
    matrixeffectspecial = models.OneToOneField(Matrixeffectspecial, verbose_name="基质效应", on_delete=models.CASCADE)
    bias = models.FloatField("最大允许偏差(%)", blank=True)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "基本参数"
        verbose_name_plural = "基本参数"


class Matrixeffectspecialtexts(models.Model):
    matrixeffectspecial = models.ForeignKey(Matrixeffectspecial, verbose_name="基质效应", on_delete=models.CASCADE)
    text = models.TextField("描述性内容", max_length=500)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "描述性内容"
        verbose_name_plural = "描述性内容"


# 样品处理后稳定性
class Prepared_Sample_Stability_special(models.Model):
    special = models.OneToOneField(Special, verbose_name="特殊参数设置", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=32, verbose_name="验证指标", blank=True, default="样品处理后稳定性", editable=False)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "样品处理后稳定性"
        verbose_name_plural = "样品处理后稳定性"


class Prepared_Sample_Stability_special_method(models.Model):
    prepared_Sample_Stability_special = models.OneToOneField(Prepared_Sample_Stability_special, verbose_name="样品处理后稳定性", on_delete=models.CASCADE)
    lowvalue = models.FloatField("回收率下限(%)", blank=True)
    upvalue = models.FloatField("回收率上限(%)", blank=True)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "基本参数"
        verbose_name_plural = "基本参数"


class Prepared_Sample_Stability_special_texts(models.Model):
    prepared_Sample_Stability_special = models.ForeignKey(Prepared_Sample_Stability_special, verbose_name="样品处理后稳定性", on_delete=models.CASCADE)
    text = models.TextField("描述性内容", max_length=500)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "描述性内容"
        verbose_name_plural = "描述性内容"

# 新建各项目参数设置时，无需在每个验证指标下方输入name
@receiver(post_save, sender=Special)
def create_user(sender, instance, created, **kwargs):
    if created:
        Repeatprecisionspecial.objects.create(special=instance)
        Interprecisionspecial.objects.create(special=instance)
        PTspecial.objects.create(special=instance)
        Recyclespecial.objects.create(special=instance)
        AMRspecial.objects.create(special=instance)
        JCXspecial.objects.create(special=instance)
        CRRspecial.objects.create(special=instance)
        MSspecial.objects.create(special=instance)
        Carryoverspecial.objects.create(special=instance)
        Matrixeffectspecial.objects.create(special=instance)
        Prepared_Sample_Stability_special.objects.create(special=instance)

##########################分界线###############################

# 二 仪器条件
class Testmethod(models.Model):

    # 仪器平台
    液质 = '液质'
    液相 = '液相'
    气相 = '气相'
    电感耦合等离子体 = 'ICP-MS'
    platform_CHOICES = (
        ('液质', '液质'),
        ('液相', '液相'),
        ('气相', '气相'),
        ('ICP-MS', 'ICP-MS'),
    )
    platform = models.CharField(max_length=16, choices=platform_CHOICES, verbose_name="仪器平台")

    # 仪器平台
    AB = 'AB'
    Agilent = 'Agilent'
    岛津 = '岛津'
    Thermo = 'Thermo'
    Waters = 'Waters'
    factory_CHOICES = (
        ('AB', 'AB'),
        ('Agilent', 'Agilent'),
        ('岛津', '岛津'),
        ('Thermo', 'Thermo'),
        ('Waters', 'Waters'),
    )
    factory = models.CharField(max_length=16, choices=factory_CHOICES, verbose_name="仪器厂家")

    # 检测平台
    内分泌检测平台 = '内分泌检测平台'
    遗传代谢病检测平台 = '遗传代谢病检测平台'
    微量营养素检测平台 = '微量营养素检测平台'
    治疗药物检测平台 = '治疗药物检测平台'
    研发与创新平台 = '研发与创新平台'
    Detectionplatform_CHOICES = (
        ('内分泌检测平台', '内分泌检测平台'),
        ('遗传代谢病检测平台', '遗传代谢病检测平台'),
        ('微量营养素检测平台', '微量营养素检测平台'),
        ('治疗药物检测平台', '治疗药物检测平台'),
        ('研发与创新平台', '研发与创新平台'),
    )
    Detectionplatform = models.CharField(max_length=16, choices=Detectionplatform_CHOICES, verbose_name="检测平台")
    project = models.CharField(max_length=16, verbose_name="项目名称", unique=True) # 检测项目
    column = models.CharField(max_length=100, verbose_name="色谱柱", blank=True) # 色谱柱
    Instrument_model = models.CharField(max_length=100, verbose_name="仪器型号", blank=True) # 仪器型号
    
    def __str__(self):
        return f"{self.project}"

    class Meta:
        verbose_name = "仪器条件"
        verbose_name_plural = "3 仪器条件"


class ZP_Method(models.Model):
    testmethod = models.ForeignKey(Testmethod, on_delete=models.CASCADE)
    norm = models.CharField(max_length=200, verbose_name="分析物名称")
    precursor_ion = models.CharField(max_length=200, verbose_name="母离子(m/z)")
    product_ion = models.CharField(max_length=200, verbose_name="子离子(m/z)")
    Col4 = models.CharField(max_length=200, verbose_name="第4列", blank=True)
    Col5 = models.CharField(max_length=200, verbose_name="第5列", blank=True)
    Col6 = models.CharField(max_length=200, verbose_name="第6列", blank=True)
    Col7 = models.CharField(max_length=200, verbose_name="第7列", blank=True)
    Col8 = models.CharField(max_length=200, verbose_name="第8列", blank=True)

    # Times = models.CharField(max_length=200, verbose_name="Time(s)", blank=True)
    # ConeV = models.CharField(max_length=200, verbose_name="Cone(V)", blank=True)
    # CollisionV = models.CharField(max_length=200, verbose_name="Collision(V)", blank=True)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "质谱方法(首行输入列名)"
        verbose_name_plural = "质谱方法(首行输入列名)"


class ZP_Methodtexts(models.Model):
    testmethod = models.ForeignKey(Testmethod, on_delete=models.CASCADE)
    text = models.TextField("描述性内容", max_length=500)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "质谱方法描述性内容"
        verbose_name_plural = "质谱方法描述性内容"


class YX_Method(models.Model):
    testmethod = models.ForeignKey(Testmethod, on_delete=models.CASCADE)
    step = models.CharField(max_length=200, verbose_name="步骤", blank=True)
    time = models.CharField(max_length=200, verbose_name="分析时间(min)", blank=True)
    Flowrate = models.CharField(max_length=200, verbose_name="流速(mL/min)", blank=True)
    Mobile_phaseA = models.CharField(max_length=200, verbose_name="流动相A(水相)", blank=True)
    Mobile_phaseB = models.CharField(max_length=200, verbose_name="流动相B(有机相)", blank=True)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "液相方法"
        verbose_name_plural = "液相方法"


class YX_Methodtexts(models.Model):
    testmethod = models.ForeignKey(Testmethod, on_delete=models.CASCADE)
    text = models.TextField("描述性内容", max_length=500)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "液相方法描述性内容"
        verbose_name_plural = "液相方法描述性内容"

##########################分界线###############################

# 三  设备


class Equipment(models.Model):
    # group = models.CharField(max_length=16,verbose_name = "项目组")
    内分泌检测平台 = '内分泌检测平台'
    遗传代谢病检测平台 = '遗传代谢病检测平台'
    微量营养素检测平台 = '微量营养素检测平台'
    治疗药物检测平台 = '治疗药物检测平台'
    研发与创新平台 = '研发与创新平台'
    Detectionplatform_CHOICES = (
        ('内分泌检测平台', '内分泌检测平台'),
        ('遗传代谢病检测平台', '遗传代谢病检测平台'),
        ('微量营养素检测平台', '微量营养素检测平台'),
        ('治疗药物检测平台', '治疗药物检测平台'),
        ('研发与创新平台', '研发与创新平台'),
    )
    Detectionplatform = models.CharField(max_length=16, choices=Detectionplatform_CHOICES, verbose_name="检测平台")
    name = models.CharField(max_length=32, verbose_name="项目名称", unique=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "项目名称"
        verbose_name_plural = "4 设备"


class Detection_equipment(models.Model):
    equipment = models.ForeignKey(Equipment, verbose_name="检测设备", on_delete=models.CASCADE, null=True)
    text = models.TextField("描述性内容", max_length=500)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = ""
        verbose_name_plural = "检测设备描述性内容"


class Auxiliary_equipment(models.Model):
    equipment = models.ForeignKey(Equipment, verbose_name="辅助设备", on_delete=models.CASCADE, null=True)
    text = models.TextField("描述性内容", max_length=500)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = ""
        verbose_name_plural = "辅助设备描述性内容"

# 四  试剂耗材


class Reagents_Consumables(models.Model):
    # group = models.CharField(max_length=16,verbose_name = "项目组")
    内分泌检测平台 = '内分泌检测平台'
    遗传代谢病检测平台 = '遗传代谢病检测平台'
    微量营养素检测平台 = '微量营养素检测平台'
    治疗药物检测平台 = '治疗药物检测平台'
    研发与创新平台 = '研发与创新平台'
    Detectionplatform_CHOICES = (
        ('内分泌检测平台', '内分泌检测平台'),
        ('遗传代谢病检测平台', '遗传代谢病检测平台'),
        ('微量营养素检测平台', '微量营养素检测平台'),
        ('治疗药物检测平台', '治疗药物检测平台'),
        ('研发与创新平台', '研发与创新平台'),
    )
    Detectionplatform = models.CharField(max_length=16, choices=Detectionplatform_CHOICES, verbose_name="检测平台")
    name = models.CharField(max_length=32, verbose_name="项目名称", unique=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "项目名称"
        verbose_name_plural = "5 试剂耗材"


class Reagents(models.Model):
    reagents_Consumables = models.ForeignKey(Reagents_Consumables, verbose_name="主要试剂", on_delete=models.CASCADE, null=True)
    text = models.TextField("描述性内容", max_length=500)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = ""
        verbose_name_plural = "主要试剂描述性内容"


class Consumables(models.Model):
    reagents_Consumables = models.ForeignKey(Reagents_Consumables, verbose_name="主要耗材", on_delete=models.CASCADE, null=True)
    text = models.TextField("描述性内容", max_length=500)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = ""
        verbose_name_plural = "主要耗材描述性内容"


# 五  样品处理
class Sample_Preparation(models.Model):
    # group = models.CharField(max_length=16,verbose_name = "项目组")
    内分泌检测平台 = '内分泌检测平台'
    遗传代谢病检测平台 = '遗传代谢病检测平台'
    微量营养素检测平台 = '微量营养素检测平台'
    治疗药物检测平台 = '治疗药物检测平台'
    研发与创新平台 = '研发与创新平台'
    Detectionplatform_CHOICES = (
        ('内分泌检测平台', '内分泌检测平台'),
        ('遗传代谢病检测平台', '遗传代谢病检测平台'),
        ('微量营养素检测平台', '微量营养素检测平台'),
        ('治疗药物检测平台', '治疗药物检测平台'),
        ('研发与创新平台', '研发与创新平台'),
    )
    Detectionplatform = models.CharField(max_length=16, choices=Detectionplatform_CHOICES, verbose_name="检测平台")
    name = models.CharField(max_length=32, verbose_name="项目名称", unique=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "项目名称"
        verbose_name_plural = "6 样品处理"


class texts(models.Model):
    sample_Preparation = models.ForeignKey(Sample_Preparation, verbose_name="主要试剂", on_delete=models.CASCADE, null=True)
    text = models.TextField("描述性内容", max_length=500)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = ""
        verbose_name_plural = "样品处理描述性内容"


class BulkGetOrCreateManager(models.Manager):
    def bulk_get_or_create(self, objs, lookup_field=None):
        assert lookup_field, "Not set 'lookup_field' for 'bulk_get_or_create'"

        lookup = {f'{lookup_field}__in': [getattr(obj, lookup_field) for obj in objs]}
        existing_objects = [
            obj for obj in self.get_queryset().filter(**lookup)
        ]
        existing_object_lookup_fields = [getattr(obj, lookup_field) for obj in existing_objects]
        non_existing_objects = [
            obj for obj in objs if getattr(obj, lookup_field) not in existing_object_lookup_fields
        ]
        self.bulk_create(non_existing_objects, batch_size=999)

        return super().get_queryset().filter(**lookup)
