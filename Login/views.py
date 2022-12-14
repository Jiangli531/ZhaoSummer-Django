import re

import pytz
from django.core.mail import send_mail
from django.http import JsonResponse

from Login.form import RegisterForm, LoginForm, ForgetPwdForm, DetailInfoForm
from Login.models import UserInfo
from ZhaoSummer_Django.settings import EMAIL_FROM
from utils.hash import *
from utils.security import DesSecret
from utils.send import *
from utils.token import create_token
from django.views.decorators.csrf import csrf_exempt
from utils.security import DesSecret

# Create your views here.
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from Login.models import UserInfo
from TeamManager.models import *
from ProjectManager.models import *
from DocsEdit.models import *
from utils.security import DesSecret

@csrf_exempt
def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            realName = register_form.cleaned_data.get('realName')

            repeated_name = UserInfo.objects.filter(username=username)
            if repeated_name.exists():
                return JsonResponse({'error': 4001, 'msg': '用户名已存在'})

            repeated_email = UserInfo.objects.filter(useremail=email)
            if repeated_email.exists():
                return JsonResponse({'error': 4002, 'msg': '邮箱已存在'})

            # 检测两次密码是否一致
            if password1 != password2:
                return JsonResponse({'error': 4004, 'msg': '两次输入的密码不一致'})
            # 检测密码不符合规范：8-18，英文字母+数字
            if not re.match('^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,18}$', password1):
                return JsonResponse({'error': 4003, 'msg': '密码不符合规范'})

            # 成功
            new_user = UserInfo()
            new_user.username = username
            new_user.userpassword = hash_code(password1)  # 密码不要存明文
            new_user.useremail = email
            new_user.realName = realName
            new_user.save()
            # new_user.userAvatar = rootUrl.IMAGE_URL
            code = make_confirm_string(new_user)

            try:
                send_email_confirm(email, code)
            except:
                new_user.delete()
                return JsonResponse({'error': 4005, 'msg': '邮件发送失败，请重新注册'})

            # request.session['is_login'] = True
            # request.session['useremail'] = email
            return JsonResponse({'error': 0, 'msg': '注册成功。请去邮箱验证'})

        else:
            return JsonResponse({'error': 3001, 'msg': '表单信息验证失败'})

    return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


@csrf_exempt
def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            # print(username)
            try:
                user = UserInfo.objects.get(username=username)
            except:
                return JsonResponse({'error': 4002, 'msg': '用户名不存在'})
            if hash_code(password) == user.userpassword:
                # 如果该用户未在邮箱中验证，则不允许登录
                if not user.has_confirmed:
                    return JsonResponse({'error': 4004, 'msg': '用户未验证，请先进行邮箱验证'})

                token = create_token(username)
                # ID加密
                DS = DesSecret()
                return JsonResponse({
                    'error': 0,
                    'msg': "登录成功",
                    'username': user.username,
                    'authorization': token,
                    'userID': DS.des_en(str(user.userID).encode()),
                    'email': user.useremail,
                    'realName': user.realName,
                })
            else:
                return JsonResponse({'error': 4003, 'msg': '密码错误'})
        else:
            return JsonResponse({'error': 3001, 'msg': '表单信息验证失败'})
    return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


@csrf_exempt
def user_confirm(request):
    if request.method == 'POST':
        code = request.POST.get('code')  # get code from url (?code=..)
        try:
            confirm = ConfirmString.objects.get(code=code)
        except:
            return JsonResponse({'error': 4001, 'msg': '校验码不存在,验证失败'})

        c_time = confirm.c_time.replace(tzinfo=pytz.UTC)
        now = datetime.datetime.now().replace(tzinfo=pytz.UTC)
        if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
            confirm.user.delete()
            return JsonResponse({'error': 4002, 'msg': '验证链接已过期'})
        else:
            confirm.user.has_confirmed = True
            confirm.user.save()
            confirm.delete()
            return JsonResponse({'error': 0, 'msg': '认证成功'})

    return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


@csrf_exempt
def forget_pwd(request):
    """ 找回密码 """
    if request.method == 'POST':
        form = ForgetPwdForm(request.POST)
        if form.is_valid():
            register_email = form.cleaned_data.get('email')
            exists = UserInfo.objects.filter(useremail=register_email).exists()
            if exists:
                # 发送邮件
                email_title = "找回密码"
                code = random_str()  # 随机生成的验证码
                request.session["code"] = code  # 将验证码保存到session
                email_body = "Hello!这里是《墨书》，你收到这封邮件是因为你正在请求更改密码！如果你没有，请忽视这封邮件！\n你的验证码为：{0}".format(code)
                send_status = send_mail(email_title, email_body, EMAIL_FROM, [register_email])
                if send_status:
                    msg = "验证码已发送，请查收邮件"
                    return JsonResponse({'error': 0, 'msg': msg})
                else:
                    return JsonResponse({'error': 4001, 'msg': '邮件发送失败'})
            else:
                return JsonResponse({'error': 4002, 'msg': '邮箱还未注册，请前往注册！'})
        else:
            return JsonResponse({'error': 3001, 'msg': '表单验证失败'})
    else:
        return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


@csrf_exempt
def update_pwd(request):
    if request.method == 'POST':
        register_email = request.POST.get("useremail")
        password = request.POST.get("password")
        try:
            user = UserInfo.objects.get(useremail=register_email)
        except:
            return JsonResponse({'error': 4003, 'msg': '邮箱不存在'})
        code = request.POST.get("code")  # 获取传递过来的验证码
        if code == request.session["code"]:
            if not re.match('^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,18}$', password):
                return JsonResponse({'error': 4001, 'msg': '密码不符合规范'})
            user.userpassword = hash_code(password)
            user.save()
            del request.session["code"]  # 删除session
            msg = "密码已重置"
            return JsonResponse({'error': 0, 'msg': msg})
        return JsonResponse({'error': 4002, 'msg': '验证码错误'})
    return JsonResponse({'error': 2001, 'msg': '请求方式错误'})


@csrf_exempt
def userinfo_edit(request):
    if request.method == 'POST':

        detail_form = DetailInfoForm(request.POST)

        if detail_form.is_valid():
            userID = detail_form.cleaned_data.get('userID')
            # realName = detail_form.cleaned_data.get('realName')
            email = detail_form.cleaned_data.get('email')
            # username = detail_form.cleaned_data.get('username')
            try:
                user = UserInfo.objects.get(userID=userID)
            except:
                return JsonResponse({'error': 4001, 'msg': '用户不存在'})
            if user.useremail != email:  # 要更改新的用户名，需要判断用户名是否重复
                repeated = UserInfo.objects.filter(useremail=email)
                if repeated.exists():
                    return JsonResponse({'error': 4003, 'msg': '邮箱已注册'})
            if email == '':
                user.email = None
            else:
                user.email = email
            user.save()
            return JsonResponse({'error': 0, 'msg': '修改成功'})

        else:
            return JsonResponse({'error': 3001, 'msg': '表单验证错误'})

    return JsonResponse({'error': 2001, 'msg': '请求方式错误！'})


#  查看个人信息
@csrf_exempt
def userinfo_view(request):
    if request.method == 'POST':
        DS = DesSecret()
        user_id = request.POST.get('userID')
        try:
            user_id = DS.des_de(user_id)
        except:
            return JsonResponse({'error': 3001, 'msg': '你的userID不对啊！'})
        try:
            user = UserInfo.objects.get(userID=user_id)
        except:
            return JsonResponse({'error': 4001, 'msg': '用户不存在'})
        return JsonResponse({'error': 0, 'msg': '查询成功', 'data': {'userID': DS.des_en(str(user.userID).encode()), 'userName': user.username,'userPassword':user.userpassword, 'userEmail': user.useremail,'realName':user.realName}})
    return JsonResponse({'error': 2001, 'msg': '请求方式错误！'})