import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

from django.conf import settings
from Login.models import *
from ZhaoSummer_Django.settings import EMAIL_FROM, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

from utils.hash import *

import datetime
import random


def make_confirm_string(user):  # generate confirm_code for user (username+c_time)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.username, now)
    ConfirmString.objects.create(code=code, user=user)
    return code


def send_email_note(to, email_body, email_title):
    print(to)
    # print(email_body)
    print(email_title)
    try:
        msg = MIMEText(email_body, _subtype='html', _charset='utf-8')  # 发送html格式
        # msg=MIMEText(data, _charset='utf-8') # data 发送文本
        msg['From'] = formataddr(["发送者名称", EMAIL_FROM])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["接收者名称", to])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = email_title  # 邮件的主题，也可以说是标题
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(EMAIL_HOST_USER, [to, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()
        return True
    except Exception as e:
        print(e)
        return False




def send_email_confirm(email, code):
    from django.core.mail import EmailMultiAlternatives

    subject = '来自《墨书》-软工团队协作与管理平台的注册确认邮件！！'

    text_content = '''感谢注册墨书，\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>这里是墨书，一个专注于软工团队协作与管理的平台！欢迎年轻可爱又有活力的你加入我们！请点击<a href="{}/confirm/?code={}" target=blank>链接</a>，\
                    完成注册！</p>
                    <p>在这里与伙伴一起高效开发！应对甲方！芜湖！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format(settings.WEB_FRONT, code, settings.CONFIRM_DAYS)  # url must be corrected

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def random_str():
    # 用randint()
    code = ''
    for i in range(6):
        n = random.randint(0, 9)
        b = chr(random.randint(65, 90))
        s = chr(random.randint(97, 122))
        code += str(random.choice([n, b, s]))
    return code
