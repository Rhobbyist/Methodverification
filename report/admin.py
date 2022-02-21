from django.contrib import admin
from .models import *
from django.shortcuts import redirect

admin.site.site_title = "方法学验证报告后台数据管理系统"
# admin.site.site_header = "方法学验证报告后台数据管理系统"
admin.site.index_title = ""

# 一  方法学参数
class GeneralInline(admin.StackedInline):
    model = General
    show_change_link = True
    can_delete = True
    extra = 0

# class SpecialInline(admin.StackedInline):
#     model = Special
#     show_change_link = True
#     can_delete = True
#     extra = 0

# 一 通用性参数设置
# 1 重复性精密度
class RepeatprecisiongeneralInline(admin.StackedInline):
    model = Repeatprecisiongeneral
    show_change_link = True
    can_delete = True
    extra = 0

class RepeatprecisiongeneralmethodInline(admin.TabularInline):
    model = Repeatprecisiongeneralmethod
    show_change_link = True
    can_delete = True
    extra = 1

class RepeatprecisiongeneraltextsInline(admin.TabularInline):
    model = Repeatprecisiongeneraltexts
    show_change_link = True
    can_delete = True
    extra = 1

# 2 中间精密度
class InterprecisiongeneralInline(admin.StackedInline):
    model = Interprecisiongeneral
    show_change_link = True
    can_delete = True
    extra = 0

class InterprecisiongeneralmethodInline(admin.TabularInline):
    model = Interprecisiongeneralmethod
    show_change_link = True
    can_delete = True
    extra = 1

class InterprecisiongeneraltextsInline(admin.TabularInline):
    model = Interprecisiongeneraltexts
    show_change_link = True
    can_delete = True
    extra = 1

# 3 PT
class PTgeneralInline(admin.StackedInline):
    model = PTgeneral
    show_change_link = True
    can_delete = True
    extra = 0

class PTgeneralmethodInline(admin.TabularInline):
    model = PTgeneralmethod
    show_change_link = True
    can_delete = True
    extra = 1

class PTgeneraltextsInline(admin.TabularInline):
    model = PTgeneraltexts
    show_change_link = True
    can_delete = True
    extra = 1

# 4 加标回收率
class RecyclegeneralInline(admin.StackedInline):
    model = Recyclegeneral
    show_change_link = True
    can_delete = True
    extra = 0

class RecyclegeneralmethodInline(admin.TabularInline):
    model = Recyclegeneralmethod
    show_change_link = True
    can_delete = True
    extra = 1

class RecyclegeneraltextsInline(admin.TabularInline):
    model = Recyclegeneraltexts
    show_change_link = True
    can_delete = True
    extra = 1

# 5 AMR(线性范围)
class AMRgeneralInline(admin.StackedInline):
    model = AMRgeneral
    show_change_link = True
    can_delete = True
    extra = 0

class AMRgeneralmethodInline(admin.TabularInline):
    model = AMRgeneralmethod
    show_change_link = True
    can_delete = True
    extra = 1

class AMRgeneraltextsInline(admin.TabularInline):
    model = AMRgeneraltexts
    show_change_link = True
    can_delete = True
    extra = 1

# 6 JCX(检出限)
class JCXgeneralInline(admin.StackedInline):
    model = JCXgeneral
    show_change_link = True
    can_delete = True
    extra = 0

class JCXgeneraltextsInline(admin.TabularInline):
    model = JCXgeneraltexts
    show_change_link = True
    can_delete = True
    extra = 1

# 7 CRR(稀释倍数)
class CRRgeneralInline(admin.StackedInline):
    model = CRRgeneral
    show_change_link = True
    can_delete = True
    extra = 0

class CRRgeneralmethodInline(admin.TabularInline):
    model = CRRgeneralmethod
    show_change_link = True
    can_delete = True
    extra = 1

class CRRgeneraltextsInline(admin.TabularInline):
    model = CRRgeneraltexts
    show_change_link = True
    can_delete = True
    extra = 1

# 8 MS(基质特异性)
class MSgeneralInline(admin.StackedInline):
    model = MSgeneral
    show_change_link = True
    can_delete = True
    extra = 0

class MSgeneraltextsInline(admin.TabularInline):
    model = MSgeneraltexts
    show_change_link = True
    can_delete = True
    extra = 1

# 9 携带效应
class CarryovergeneralInline(admin.StackedInline):
    model = Carryovergeneral
    show_change_link = True
    can_delete = True
    extra = 0

class CarryovergeneralmethodInline(admin.TabularInline):
    model = Carryovergeneralmethod
    show_change_link = True
    can_delete = True
    extra = 1

class CarryovergeneraltextsInline(admin.TabularInline):
    model = Carryovergeneraltexts
    show_change_link = True
    can_delete = True
    extra = 1

# 10 基质效应
class MatrixeffectgeneralInline(admin.StackedInline):
    model = Matrixeffectgeneral
    show_change_link = True
    can_delete = True
    extra = 0

class MatrixeffectgeneralmethodInline(admin.TabularInline):
    model = Matrixeffectgeneralmethod
    show_change_link = True
    can_delete = True
    extra = 1

class MatrixeffectgeneraltextsInline(admin.TabularInline):
    model = Matrixeffectgeneraltexts
    show_change_link = True
    can_delete = True
    extra = 1

# 11 样品稳定性
class StabilitygeneralInline(admin.StackedInline):
    model = Stabilitygeneral
    show_change_link = True
    can_delete = True
    extra = 0

class StabilitygeneralmethodInline(admin.TabularInline):
    model = Stabilitygeneralmethod
    show_change_link = True
    can_delete = True
    extra = 1

class StabilitygeneraltextsInline(admin.TabularInline):
    model = Stabilitygeneraltexts
    show_change_link = True
    can_delete = True
    extra = 1

# 12 参考区间
class ReferenceintervalgeneralInline(admin.StackedInline):
    model = Referenceintervalgeneral
    show_change_link = True
    can_delete = True
    extra = 0

class ReferenceintervalgeneraltextsInline(admin.TabularInline):
    model = Referenceintervalgeneraltexts
    show_change_link = True
    can_delete = True
    extra = 1


# 二 通用性内联
class GeneralAdmin(admin.ModelAdmin):
    inlines = [RepeatprecisiongeneralInline, InterprecisiongeneralInline, PTgeneralInline, RecyclegeneralInline, AMRgeneralInline,
               JCXgeneralInline, CRRgeneralInline, MSgeneralInline, CarryovergeneralInline, MatrixeffectgeneralInline, StabilitygeneralInline,
               ReferenceintervalgeneralInline]
    list_display = ('name',)

    def has_add_permission(self, request):
        return False

# 1 重复性精密度内联
class RepeatprecisiongeneralAdmin(admin.ModelAdmin):
    inlines = [RepeatprecisiongeneralmethodInline,RepeatprecisiongeneraltextsInline]

    def has_module_permission(self, requset):
        return False

    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/general/')

    def response_change(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/general/')

# 2 中间精密度内联
class InterprecisiongeneralAdmin(admin.ModelAdmin):
    inlines = [InterprecisiongeneralmethodInline,InterprecisiongeneraltextsInline]

    def has_module_permission(self, requset):
        return False

    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/general/')

    def response_change(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/general/')

# 3 PT内联
class PTgeneralAdmin(admin.ModelAdmin):
    inlines = [PTgeneralmethodInline, PTgeneraltextsInline]

    def has_module_permission(self, requset):
        return False

    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/general/')

    def response_change(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/general/')

# 4 加标回收率内联
class RecyclegeneralAdmin(admin.ModelAdmin):
    inlines = [RecyclegeneralmethodInline, RecyclegeneraltextsInline]

    def has_module_permission(self, requset):
        return False

    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/general/')

    def response_change(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/general/')

# 5 AMR(线性范围)内联
class AMRgeneralAdmin(admin.ModelAdmin):
    inlines = [AMRgeneralmethodInline, AMRgeneraltextsInline]

    def has_module_permission(self, requset):
        return False

    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/general/')

    def response_change(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/general/')

# 6 JCX(检出限)内联
class JCXgeneralAdmin(admin.ModelAdmin):
    inlines = [JCXgeneraltextsInline]

    def has_module_permission(self, requset):
        return False

    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/general/')

    def response_change(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/general/')

# 7 稀释倍数内联
class CRRgeneralAdmin(admin.ModelAdmin):
    inlines = [CRRgeneralmethodInline, CRRgeneraltextsInline]

    def has_module_permission(self, requset):
        return False

    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/general/')

    def response_change(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/general/')

# 8 基质特异性内联
class MSgeneralAdmin(admin.ModelAdmin):
    inlines = [MSgeneraltextsInline]

    def has_module_permission(self, requset):
        return False

    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/general/')

    def response_change(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/general/')

# 9 携带效应内联
class CarryovergeneralAdmin(admin.ModelAdmin):
    inlines = [CarryovergeneralmethodInline, CarryovergeneraltextsInline]

    def has_module_permission(self, requset):
        return False

    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/general/')

    def response_change(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/general/')

# 10 基质效应内联
class MatrixeffectgeneralAdmin(admin.ModelAdmin):
    inlines = [MatrixeffectgeneralmethodInline, MatrixeffectgeneraltextsInline]

    def has_module_permission(self, requset):
        return False

    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/general/')

    def response_change(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/general/')

# 11 样品处理后稳定性内联
class StabilitygeneralAdmin(admin.ModelAdmin):
    inlines = [StabilitygeneralmethodInline, StabilitygeneraltextsInline]

    def has_module_permission(self, requset):
        return False

    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/general/')

    def response_change(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/general/')

# 12 参考区间内联
class ReferenceintervalgeneralAdmin(admin.ModelAdmin):
    inlines = [ReferenceintervalgeneraltextsInline]

    def has_module_permission(self, requset):
        return False

    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/general/')

    def response_change(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/general/')


# 三 各项目参数设置
# 1 重复性精密度
class RepeatprecisionspecialInline(admin.StackedInline):
    model = Repeatprecisionspecial
    show_change_link = True
    can_delete = True
    # extra = 0

class RepeatprecisionspecialmethodInline(admin.TabularInline):
    model = Repeatprecisionspecialmethod
    show_change_link = True
    can_delete = True
    extra = 1

class RepeatprecisionspecialtextsInline(admin.TabularInline):
    model = Repeatprecisionspecialtexts
    show_change_link = True
    can_delete = True
    extra = 1

# 2 中间精密度
class InterprecisionspecialInline(admin.StackedInline):
    model = Interprecisionspecial
    show_change_link = True
    can_delete = True
    # extra = 0

class InterprecisionspecialmethodInline(admin.TabularInline):
    model = Interprecisionspecialmethod
    show_change_link = True
    can_delete = True
    extra = 1

class InterprecisionspecialtextsInline(admin.TabularInline):
    model = Interprecisionspecialtexts
    show_change_link = True
    can_delete = True
    extra = 1

# 3 PT
class PTspecialInline(admin.StackedInline):
    model = PTspecial
    show_change_link = True
    can_delete = True
    # extra = 0

class PTspecialmethodInline(admin.TabularInline):
    model = PTspecialmethod
    show_change_link = True
    can_delete = True
    extra = 1

class PTspecialtextsInline(admin.TabularInline):
    model = PTspecialtexts
    show_change_link = True
    can_delete = True
    extra = 1

class PTspecialacceptInline(admin.TabularInline):
    model = PTspecialaccept
    show_change_link = True
    can_delete = True
    extra = 1

# 4 加标回收率
class RecyclespecialInline(admin.StackedInline):
    model = Recyclespecial
    show_change_link = True
    can_delete = True
    # extra = 0

class RecyclespecialmethodInline(admin.TabularInline):
    model = Recyclespecialmethod
    show_change_link = True
    can_delete = True
    extra = 1

class RecyclespecialtextsInline(admin.TabularInline):
    model = Recyclespecialtexts
    show_change_link = True
    can_delete = True
    extra = 1

# 5 AMR(线性范围)
class AMRspecialInline(admin.StackedInline):
    model = AMRspecial
    show_change_link = True
    can_delete = True
    # extra = 0

class AMRspecialmethodInline(admin.TabularInline):
    model = AMRspecialmethod
    show_change_link = True
    can_delete = True
    extra = 1

class AMRspecialtextsInline(admin.TabularInline):
    model = AMRspecialtexts
    show_change_link = True
    can_delete = True
    extra = 1

# 6 检出限
class JCXspecialInline(admin.StackedInline):
    model = JCXspecial
    show_change_link = True
    can_delete = True
    # extra = 0

class JCXspecialtextsInline(admin.TabularInline):
    model = JCXspecialtexts
    show_change_link = True
    can_delete = True
    extra = 1

# 7 CRR(稀释倍数)
class CRRspecialInline(admin.StackedInline):
    model = CRRspecial
    show_change_link = True
    can_delete = True
    # extra = 0

class CRRspecialmethodInline(admin.TabularInline):
    model = CRRspecialmethod
    show_change_link = True
    can_delete = True
    extra = 1

class CRRspecialtextsInline(admin.TabularInline):
    model = CRRspecialtexts
    show_change_link = True
    can_delete = True
    extra = 1

# 8 MS(基质特异性)
class MSspecialInline(admin.StackedInline):
    model = MSspecial
    show_change_link = True
    can_delete = True
    # extra = 0

class MSspecialtextsInline(admin.TabularInline):
    model = MSspecialtexts
    show_change_link = True
    can_delete = True
    extra = 1

# 9 携带效应
class CarryoverspecialInline(admin.StackedInline):
    model = Carryoverspecial
    show_change_link = True
    can_delete = True
    # extra = 0

class CarryoverspecialmethodInline(admin.TabularInline):
    model = Carryoverspecialmethod
    show_change_link = True
    can_delete = True
    extra = 1

class CarryoverspecialtextsInline(admin.TabularInline):
    model = Carryoverspecialtexts
    show_change_link = True
    can_delete = True
    extra = 1

# 10 基质效应
class MatrixeffectspecialInline(admin.StackedInline):
    model = Matrixeffectspecial
    show_change_link = True
    can_delete = True
    # extra = 0

class MatrixeffectspecialmethodInline(admin.TabularInline):
    model = Matrixeffectspecialmethod
    show_change_link = True
    can_delete = True
    extra = 1

class MatrixeffectspecialtextsInline(admin.TabularInline):
    model = Matrixeffectspecialtexts
    show_change_link = True
    can_delete = True
    extra = 1

# 11 样品处理后稳定性
class Prepared_Sample_Stability_specialInline(admin.StackedInline):
    model = Prepared_Sample_Stability_special
    show_change_link = True
    can_delete = True
    # extra = 0

class Prepared_Sample_Stability_special_methodInline(admin.TabularInline):
    model = Prepared_Sample_Stability_special_method
    show_change_link = True
    can_delete = True
    extra = 1

class Prepared_Sample_Stability_special_textsInline(admin.TabularInline):
    model = Prepared_Sample_Stability_special_texts
    show_change_link = True
    can_delete = True
    extra = 1


# 四 特殊内联
class SpecialAdmin(admin.ModelAdmin):
    inlines = [RepeatprecisionspecialInline, InterprecisionspecialInline, PTspecialInline, RecyclespecialInline, AMRspecialInline,
               JCXspecialInline, CRRspecialInline, MSspecialInline, CarryoverspecialInline, MatrixeffectspecialInline,Prepared_Sample_Stability_specialInline]
    list_display = ('Detectionplatform', 'project', 'unit',
                    'Effective_digits', 'Number_of_compounds')
    list_filter = ('Detectionplatform', 'project',
                   'unit', 'Number_of_compounds',)
    search_fields = ['Detectionplatform', 'project']
    list_per_page = 10  # 每页显示10条记录
    ordering = ('Number_of_compounds',)

#  1 重复性精密度
class RepeatprecisionspecialAdmin(admin.ModelAdmin):
    inlines = [RepeatprecisionspecialmethodInline,RepeatprecisionspecialtextsInline]

    def has_module_permission(self, requset):
        return False

    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/special/')

    def response_change(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/special/')

#  2 中间精密度
class InterprecisionspecialAdmin(admin.ModelAdmin):
    inlines = [InterprecisionspecialmethodInline,
               InterprecisionspecialtextsInline]

    def has_module_permission(self, requset):
        return False

    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/special/')

    def response_change(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/special/')

#  3 PT
class PTspecialAdmin(admin.ModelAdmin):
    inlines = [PTspecialmethodInline,
               PTspecialtextsInline, PTspecialacceptInline]

    def has_module_permission(self, requset):
        return False

    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/special/')

    def response_change(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/special/')

#  4 加标回收率
class RecyclespecialAdmin(admin.ModelAdmin):
    inlines = [RecyclespecialmethodInline, RecyclespecialtextsInline]

    def has_module_permission(self, requset):
        return False

    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/special/')

    def response_change(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/special/')

#  5 AMR(线性范围)
class AMRspecialAdmin(admin.ModelAdmin):
    inlines = [AMRspecialmethodInline, AMRspecialtextsInline]

    def has_module_permission(self, requset):
        return False

    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/special/')

    def response_change(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/special/')

#  6 检出限
class JCXspecialAdmin(admin.ModelAdmin):
    inlines = [JCXspecialtextsInline]

    def has_module_permission(self, requset):
        return False

    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/special/')

    def response_change(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/special/')

#  7 稀释倍数
class CRRspecialAdmin(admin.ModelAdmin):
    inlines = [CRRspecialmethodInline, CRRspecialtextsInline]

    def has_module_permission(self, requset):
        return False

    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/special/')

    def response_change(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/special/')

#  8 基质特异性
class MSspecialAdmin(admin.ModelAdmin):
    inlines = [MSspecialtextsInline]

    def has_module_permission(self, requset):
        return False

    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/special/')

    def response_change(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/special/')

#  9 携带效应
class CarryoverspecialAdmin(admin.ModelAdmin):
    inlines = [CarryoverspecialmethodInline, CarryoverspecialtextsInline]

    def has_module_permission(self, requset):
        return False

    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/special/')

    def response_change(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/special/')

#  10 基质效应
class MatrixeffectspecialAdmin(admin.ModelAdmin):
    inlines = [MatrixeffectspecialmethodInline, MatrixeffectspecialtextsInline]

    def has_module_permission(self, requset):
        return False

    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/special/')

    def response_change(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/special/')

#  11 样品处理后稳定性
class Prepared_Sample_Stability_specialAdmin(admin.ModelAdmin):
    inlines = [Prepared_Sample_Stability_special_methodInline, Prepared_Sample_Stability_special_textsInline]

    def has_module_permission(self, requset):
        return False

    def response_add(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/special/')

    def response_change(self, request, obj, post_url_continue=None):
        return redirect('/admin/report/special/')


# 五 通用性参数注册
admin.site.register(General, GeneralAdmin)
admin.site.register(Repeatprecisiongeneral, RepeatprecisiongeneralAdmin)
admin.site.register(Interprecisiongeneral, InterprecisiongeneralAdmin)
admin.site.register(PTgeneral, PTgeneralAdmin)
admin.site.register(Recyclegeneral, RecyclegeneralAdmin)
admin.site.register(AMRgeneral, AMRgeneralAdmin)
admin.site.register(JCXgeneral, JCXgeneralAdmin)
admin.site.register(CRRgeneral, CRRgeneralAdmin)
admin.site.register(MSgeneral, MSgeneralAdmin)
admin.site.register(Carryovergeneral, CarryovergeneralAdmin)
admin.site.register(Matrixeffectgeneral, MatrixeffectgeneralAdmin)
admin.site.register(Stabilitygeneral, StabilitygeneralAdmin)
admin.site.register(Referenceintervalgeneral, ReferenceintervalgeneralAdmin)

# 六 特殊参数注册
admin.site.register(Special, SpecialAdmin)
admin.site.register(Repeatprecisionspecial, RepeatprecisionspecialAdmin)
admin.site.register(Interprecisionspecial, InterprecisionspecialAdmin)
admin.site.register(PTspecial, PTspecialAdmin)
admin.site.register(Recyclespecial, RecyclespecialAdmin)
admin.site.register(AMRspecial, AMRspecialAdmin)
admin.site.register(JCXspecial, JCXspecialAdmin)
admin.site.register(CRRspecial, CRRspecialAdmin)
admin.site.register(MSspecial, MSspecialAdmin)
admin.site.register(Carryoverspecial, CarryoverspecialAdmin)
admin.site.register(Matrixeffectspecial, MatrixeffectspecialAdmin)
admin.site.register(Prepared_Sample_Stability_special, Prepared_Sample_Stability_specialAdmin)

##########################分界线###############################

# 二 检测方法

# 1 Inline
class ZP_MethodInline(admin.TabularInline):
    model = ZP_Method
    show_change_link = True
    can_delete = True
    extra = 0


class ZP_MethodtextsInline(admin.TabularInline):
    model = ZP_Methodtexts
    show_change_link = True
    can_delete = True
    extra = 0


class YX_MethodInline(admin.TabularInline):
    model = YX_Method
    show_change_link = True
    can_delete = True
    extra = 0


class YX_MethodtextsInline(admin.TabularInline):
    model = YX_Methodtexts
    show_change_link = True
    can_delete = True
    extra = 0


class TestmethodAdmin(admin.ModelAdmin):

    inlines = [ZP_MethodInline, ZP_MethodtextsInline,
               YX_MethodInline, YX_MethodtextsInline]

    '''设置列表可显示的字段'''
    list_display = ('platform', 'factory', 'Detectionplatform',
                    'project', 'column', 'Instrument_model')

    # '''设置过滤选项'''
    list_filter = ('platform', 'factory', 'Detectionplatform', 'project',)

    ordering = ('platform',)

    # '''每页显示条目数'''
    # list_per_page = 5

    # '''设置可编辑字段'''
    # list_editable = ('status',)

    # '''按日期月份筛选'''
    # date_hierarchy = 'pub_date'

    # '''按发布日期排序'''
    # ordering = ('-mod_date',)

    search_fields = ('platform', 'factory', 'project')


admin.site.register(Testmethod, TestmethodAdmin)

##########################分界线###############################

# 三 设备

# 1 Inline


class Detection_equipmentInline(admin.StackedInline):
    model = Detection_equipment
    show_change_link = True
    can_delete = True
    extra = 0


class Auxiliary_equipmentInline(admin.StackedInline):
    model = Auxiliary_equipment
    show_change_link = True
    can_delete = True
    extra = 0

#  2 内联


class EquipmentAdmin(admin.ModelAdmin):
    '''设置列表可显示的字段'''
    list_display = ('Detectionplatform', 'name',)
    list_filter = ('Detectionplatform', 'name',)
    search_fields = ('Detectionplatform', 'name',)
    ordering = ('Detectionplatform',)
    inlines = [Detection_equipmentInline, Auxiliary_equipmentInline]


# 3 注册
admin.site.register(Equipment, EquipmentAdmin)


# 四 试剂耗材
# 1 Inline
class ReagentsInline(admin.StackedInline):
    model = Reagents
    show_change_link = True
    can_delete = True
    extra = 0


class ConsumablesInline(admin.StackedInline):
    model = Consumables
    show_change_link = True
    can_delete = True
    extra = 0


#  2 内联
class Reagents_ConsumablesAdmin(admin.ModelAdmin):
    '''设置列表可显示的字段'''
    list_display = ('Detectionplatform', 'name',)
    list_filter = ('Detectionplatform', 'name',)
    search_fields = ('Detectionplatform', 'name',)
    ordering = ('Detectionplatform',)
    inlines = [ReagentsInline, ConsumablesInline]


# 3 注册
admin.site.register(Reagents_Consumables, Reagents_ConsumablesAdmin)


# 五 样品处理
# 1 Inline
class textsInline(admin.StackedInline):
    model = texts
    show_change_link = True
    can_delete = True
    extra = 0


#  2 内联
class Sample_PreparationAdmin(admin.ModelAdmin):
    '''设置列表可显示的字段'''
    list_display = ('Detectionplatform', 'name',)
    list_filter = ('Detectionplatform', 'name',)
    search_fields = ('Detectionplatform', 'name',)
    ordering = ('Detectionplatform',)
    inlines = [textsInline]


# 3 注册
admin.site.register(Sample_Preparation, Sample_PreparationAdmin)
