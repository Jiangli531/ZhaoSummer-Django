import re

import pytz
from django.core.mail import send_mail
from django.http import JsonResponse
from django.utils import timezone

from DocsEdit.models import *
from Login.form import RegisterForm, LoginForm, ForgetPwdForm
from Login.models import UserInfo
from ZhaoSummer_Django.settings import EMAIL_FROM
from utils.hash import *
from utils.send import *
from utils.token import create_token
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
#查看文档列表
@csrf_exempt
def viewDocList(request):
    if request.method == 'POST':
        projectid=request.POST.get('projectID')
        if projectid:
            project=ProjectInfo.objects.filter(projectID=projectid).first()
            doc_list = Document.objects.filter( project=project, recycled=False).order_by('-modified_time')
            data = []
            for c in doc_list:
                ret = {
                    'docID': c.id,
                    'title': c.title,
                    'creatorID': c.creator.userID,
                    'perm': c.doc_right,
                    'modified_date': c.modified_time.strftime('%Y-%m-%d %H:%M:%S')
                }
                data.append(ret)
            return JsonResponse({'errno': 0, 'data': data})
        else:
            return JsonResponse({'errno': 1002, 'msg': "用户未登录"})

    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def createDocument(request):
    if request.method == 'POST':
        userid = request.POST.get('userID')
        projectid = request.POST.get('projectID')
        title = request.POST.get('title')
        if userid:
            user = UserInfo.objects.filter(userID=userid).first()
            project = ProjectInfo.objects.filter(projectID=projectid).first()
            doc = Document.objects.filter(title=title, creator=user, project=project).first()
            if doc:
                return JsonResponse({'errno': 1003, 'msg': "文件名已存在"})
            document = Document()
            document.creator = user
            document.title = title
            document.content = request.POST.get('content')
            document.created_time = timezone.now()
            document.modified_time = timezone.now()
            document.save()
            return JsonResponse({'errno': 0, 'msg': "创建成功"})
        else:
            return JsonResponse({'errno': 1002, 'msg': "用户未登录"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

@csrf_exempt
def viewDoc(request):
    if request.method == 'GET':
        doc_id = request.POST.get("docID")
        doc = Document.objects.filter(docID=doc_id).first()
        if doc:
            ret = {
                    'title': doc.title,
                    'content': doc.content,
                    'docRight': doc.docRight
            }
            return JsonResponse({'errno': 0, 'data': ret})
        else:
                return JsonResponse({'errno': 1003, 'msg': "未找到该文件}"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

@csrf_exempt
def modifyDocName(request):
    if request.method == 'POST':
            doc_id = request.POST.get("docID")
            title = request.POST.get("title")
            doc = Document.objects.get(docID=doc_id)
            doc.title = title
            doc.save()
            return JsonResponse({'errno': 0, 'msg': "修改成功"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


@csrf_exempt
def modifyDocContent(request):
    if request.method == 'POST':
            doc_id = request.POST.get("docID")
            content = request.POST.get("content")
            doc = Document.objects.get(docID=doc_id)
            doc.content = content
            doc.modified_time = timezone.now()
            doc.save()
            return JsonResponse({'errno': 0, 'msg': "修改成功"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

@csrf_exempt
def recycleDoc(request):
    if request.method == 'POST':
            doc_id = request.POST.get("docID")
            doc = Document.objects.get(docID=doc_id)
            doc.recycled = True
            doc.save()
            return JsonResponse({'errno': 0, 'msg': "回收成功"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


# 删除回收站文档/彻底删除文档
@csrf_exempt
def delRecycleDoc(request):
    if request.method == 'POST':
            doc_id = request.POST.get("docId")
            Document.objects.filter(docID=doc_id).first().delete()
            return JsonResponse({'errno': 0, 'msg': "删除成功"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

# 回收站恢复文档（个人中心）
@csrf_exempt
def recover(request):
    if request.method == 'POST':
            doc_id = request.POST.get("docId")
            doc = Document.objects.filter(docID=doc_id).first()
            doc.recycled = False
            doc.save()
            return JsonResponse({'errno': 0, 'msg': "恢复成功"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})