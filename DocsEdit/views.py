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
from utils.security import DesSecret
from utils.send import *
from utils.token import create_token
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
#查看文档列表
@csrf_exempt
def viewDocList(request):
    if request.method == 'POST':
        DS=DesSecret()
        projectid=request.POST.get('projectID')
        projectid = DS.des_de(projectid)
        if projectid:
            project=ProjectInfo.objects.filter(projectID=projectid).first()
            doc_list = Document.objects.filter( project=project, recycled=False).order_by('-modified_time')
            data = []
            for c in doc_list:
                ret = {
                    'docID': c.docId,
                    'title': c.title,
                    'creatorID': c.creator.userID,
                    'perm': c.docRight,
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
        type = request.POST.get('type')
        DS = DesSecret()
        userID = request.POST.get('userID')
        userid = DS.des_de(userID)
        # print(type)
        # print(type(type))
        if type == '0':
            # print(000)
            projectid = request.POST.get('projectID')
            projectid = DS.des_de(projectid)

            try:
                project = ProjectInfo.objects.get(projectID=projectid)
            except:
                return JsonResponse({'error': 1004, 'msg': "项目不存在"})
            groupid = project.projectTeam.groupId
        else:
            # print(111)
            project = None
            groupid = request.POST.get('groupID')
            groupid = DS.des_de(groupid)
        title = request.POST.get('title')
        group=Group.objects.filter(groupId=groupid).first()
        if userid:
            user = UserInfo.objects.filter(userID=userid).first()
            doc = Document.objects.filter(title=title, project=project).first()
            if doc:
                return JsonResponse({'errno': 1003, 'msg': "文件名已存在"})
            document = Document()
            document.creator = user
            document.title = title
            document.content = request.POST.get('content')
            document.created_time = timezone.now()
            document.modified_time = timezone.now()
            document.project=project
            document.group=group
            if project:
                document.type = False
            else:
                document.type = True
            document.save()
            if project:
                project.docNum += 1
                project.save()
            ret={
                'docID': document.docId,
                'title': document.title,
            }
            return JsonResponse({'errno': 0, 'data': ret})
        else:
            return JsonResponse({'errno': 1002, 'msg': "用户未登录"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

@csrf_exempt
def viewDoc(request):
    if request.method == 'GET':
        DS = DesSecret()
        doc_id = request.POST.get("docID")
        doc_id = DS.des_de(doc_id)
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
            DS = DesSecret()
            doc_id = request.POST.get("docID")
            doc_id = DS.des_de(doc_id)
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
            DS = DesSecret()
            doc_id = request.POST.get("docID")
            doc_id = DS.des_de(doc_id)
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
            DS = DesSecret()
            doc_id = request.POST.get("docID")
            doc_id = DS.des_de(doc_id)
            doc = Document.objects.get(docID=doc_id)
            doc.recycled = True
            doc.save()
            doc.project.docNum -= 1
            doc.project.save()
            return JsonResponse({'errno': 0, 'msg': "回收成功"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})


# 删除回收站文档/彻底删除文档
@csrf_exempt
def delRecycleDoc(request):
    if request.method == 'POST':
            DS = DesSecret()
            doc_id = request.POST.get("docId")
            doc_id = DS.des_de(doc_id)
            Document.objects.filter(docID=doc_id).first().delete()
            return JsonResponse({'errno': 0, 'msg': "删除成功"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

# 回收站恢复文档（个人中心）
@csrf_exempt
def recover(request):
    if request.method == 'POST':
            DS = DesSecret()
            doc_id = request.POST.get("docId")
            doc_id = DS.des_de(doc_id)
            doc = Document.objects.filter(docID=doc_id).first()
            doc.recycled = False
            doc.save()
            return JsonResponse({'errno': 0, 'msg': "恢复成功"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

@csrf_exempt
def viewProjectDocList(request):
    if request.method == 'POST':
        DS = DesSecret()
        project_id = request.POST.get('projectID')
        project_id = DS.des_de(project_id)
        print(DS.des_en(str(8)))
        project = ProjectInfo.objects.filter(projectID=project_id).first()
        childdoc=[]
        if project:
            return JsonResponse({'errno': 0, 'documentList':get_prodocs(project)})
        else:
            return JsonResponse({'errno': 1004, 'msg': "项目不存在"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

def get_prodocs(project):
    childdoc = []
    documentList = []
    docs = Document.objects.filter(project=project).all()
    for doc in docs:
        ret = {
                'docid': doc.docId,
                'isSub': "false",
                'title': doc.title,
                'content': doc.content,
                'docRight': doc.docRight,
                'created_time': doc.created_time,
                'modified_time': doc.modified_time,
                'creator': doc.creator.username,
                'group': doc.group.groupName,
                'childdoc': childdoc,
        }
        documentList.append(ret)
    return documentList

@csrf_exempt
def viewTeamDocList(request):
    global pro
    if request.method == 'POST':
        DS = DesSecret()
        team_id = request.POST.get('teamID')
        team_id = DS.des_de(team_id)
        team = Group.objects.filter(groupId=team_id).first()
        if team:
            documentList = []
            docs= Document.objects.filter(group=team)
            for doc in docs:
                if not doc.type:
                    sub = 'false'
                    childdoc = []
                    ret = {
                        'docid': doc.docId,
                        'isSub': sub,
                        'title': doc.title,
                        'content': doc.content,
                        'docRight': doc.docRight,
                        'created_time': doc.created_time,
                        'modified_time': doc.modified_time,
                        'creator': doc.creator.username,
                        'group': doc.group.groupName,
                        'childdoc': childdoc,
                    }
                    documentList.append(ret)
                else:
                    sub = 'true'
                    pros=docs.values('project').distinct()
                    for pro in pros:
                        childdoc = []
                        if pro['project']==None:
                            continue
                        for c in docs.filter(project=pro['project']).all():
                            childdoc.append({
                                'docid': c.docId,
                                'title': c.title,
                                'content': c.content,
                                'docRight': c.docRight,
                                'created_time': c.created_time,
                                'modified_time': c.modified_time,
                                'creator': c.creator.username,
                                'group': c.group.groupName,
                            })
                        ret = {
                            'docid': -1,
                            'isSub': sub,
                            'title': pro['project'],
                            'content': None,
                            'childdoc': childdoc,
                        }
                        documentList.append(ret)
            return JsonResponse({'errno': 0, 'documentList': documentList})
        else:
            return JsonResponse({'errno': 1004, 'msg': "团队不存在"})
    else:
        return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})
