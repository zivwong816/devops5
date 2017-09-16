#!/usr/bin/python
# coding=utf8

from django.views.generic import View, TemplateView, ListView
from django.shortcuts import redirect, reverse, render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, Group
from resources.models import Idc
from django.core import serializers
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
import json
from accounts.mixins import PermissionRequiredMixin
from resources.forms import CreateIdcForm

# class CreateIdcView(TemplateView):

#     template_name = "add_idc.html"

#     def post(self, request):
#         print(request.POST)
#         print(reverse("success", kwargs={"next": "user_lsit"}))
#         # return redirect("suceess", next="user_list")
#         return redirect("error", next="idc_add", msg="人为失败")
        # return HttpResponse("")

class IdcListView(LoginRequiredMixin, ListView):
    """IDC 信息展示逻辑"""
    permission_required = "resources.add_idc"       # 覆盖父类 PermissionRequiredMixin 类属性
    template_name = "idclist.html"
    model = Idc
    permission_redirect_field_name = "dashboard"        # 覆盖父类 PermissionRequiredMixin 类属性

    # @method_decorator(permission_required("resources.add_idc", login_url=reverse("dashboard")))
    # def get(self, request, *args, **kwargs):
    #     return super(IdcListView, self).get(request, *args, **kwargs)


class CreateIdcView(LoginRequiredMixin ,TemplateView):
    """增加 IDC 逻辑"""
    template_name = "add_idc.html"

    def post(self, request):
        idcform = CreateIdcForm(request.POST)
        if idcform.is_valid():
            idc = Idc(**idcform.cleaned_data)
            try:
                idc.save()
                return redirect("success", next="idc_list")
            except Exception as e:
                return redirect("error", next="idc_list", msg=e.args)

        else:
            return redirect("error", next="idc_list",
                            msg=json.dumps(json.loads(idcform.errors.as_json()), ensure_ascii=False))

        # print(forms)      # 取表单数据，是一个dict


class DeleteIdcView(LoginRequiredMixin ,View):
    """删除 Idc 的逻辑，响应前端 ajax 请求"""
    def post(self, request):
        ret = {'status': 0}
        idc_id = request.POST.get('idc_id', '')     # 获取前端 ajax 传递过来的 idc_id
        # 获取 idc_id 后进行对应的删除，异常给予报错提示
        try:
            idc = Idc.objects.get(id=idc_id)
            idc.delete()
        except Idc.DoesNotExist:
            ret['stauts'] = 1
            ret['errmsg'] = "Idc不存在"
        return JsonResponse(ret)


class IdcMoreView(LoginRequiredMixin ,View):
    """IDC 详情按钮的逻辑，响应后端的 ajax 请求"""
    def get(self, request):
        idc_id = request.GET.get('idc_id', '')
        # print(idc_id)
        try:
            idc = Idc.objects.get(id=idc_id)
        except Idc.DoesNotExist:
            return JsonResponse([], safe=False)

        # print(idc.__dict__)
        # 为了排除上述 dict 的非可用 "_state" key
        new_idc_obj = {}
        for i in idc.__dict__:
            if i != "_state":
                new_idc_obj[i] = idc.__dict__[i]
        # print(new_idc_obj)
        return JsonResponse(new_idc_obj)
        # return HttpResponse(serializers.serialize("json", idc_obj.__dict__), content_type="application/json")
        # return render(request, {"idc_obj": idc_obj})
        # return HttpResponse("")