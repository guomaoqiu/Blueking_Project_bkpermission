# -*- coding: utf-8 -*-
from django.http  import HttpResponse
from common.mymako import render_mako_context, render_json
from settings import PRPCRYPTO_KEY
from django.views.decorators.csrf import csrf_exempt
from account.decorators import login_exempt
from .models import PaasCon,AppPer,Students
from crypto import prpcrypt
import json, MySQLdb, requests
from django.conf import settings
# from utils import access_check
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

@csrf_exempt
def setting(request):
    '''
    @note: 如果是GET方法直接从数据库获取内容;获取paas平台的数据库连接信息
    '''
    if request.method == "POST":
        try:
            if len(request.GET.get('port')) == 0:
                p_port = 3306
                print '端口为空'
            else:
                print '端口不为空'
                p_port = request.GET.get('port')

            cli = PaasCon(p_host = request.GET.get('host'),
                          p_user = request.GET.get('user'),
                          p_pass = request.GET.get('password'),
                          p_port = p_port
                          )
            # 在数据录入时 将密码加密
            prpcrypt_key = prpcrypt(PRPCRYPTO_KEY) # 调用crypto 加密

            cli.p_pass = prpcrypt_key.encrypt(request.GET.get('password', ''),)
            cli.save()
            result = {"result": True,"message":u"添加信息成功"}
            return render_json(result)

        except Exception,e:
            result = {"result": False,"message":u"添加信息失败{0}".format(e)}
            return render_json(result)

    data = []
    for each_data in PaasCon.objects.all():
        data.append(each_data.to_json())

    if len(data) == 0:
        return render_mako_context(request,'/home_application/app_perm/setting.html',{"result":False,})
    else:
        return render_mako_context(request,'/home_application/app_perm/setting.html',{"result":True,"data":data})

@csrf_exempt
def del_db(request):
    '''
    @note: 删除paas平台的数据库连接信息
    '''
    print request.method
    if request.method == "POST":
        info_id = request.GET.get('info_id')
        try:
            PaasCon.objects.filter(id=info_id).delete()
            result = {"result":True,"message":u"删除成功..."}
            return render_json(result)
        except Exception,e:
            result = {"result":False,"message":u"删除失败...\n{}".format(e)}
            print e
            return render_json(result)

def applist(request):
    '''
    @note: 连接paas平台数据库；连接信息从数据库中获取
    '''
    data = []
    try:
        for each_data in PaasCon.objects.all():
            data.append(each_data.to_json())

        prpcrypt_key = prpcrypt(PRPCRYPTO_KEY)  # 调用crypto 解密
        password =  prpcrypt_key.decrypt(data[0]['p_pass'])

        db = MySQLdb.connect(data[0]['p_host'],data[0]['p_user'],password,'open_paas',charset="utf8") # 一定要加连接时的字符
        cursor = db.cursor()
        cursor.execute("select * from paas_app where code != 'bk_agent_setup' and code != 'bk_monitor'") # 过滤掉自带saas应用(除了管理员身份都不能访问)
        data = cursor.fetchall()

        # 查询paas的app跟本地对比；若没有添加进数据库则添加
        exists_appcode = []

        for each_appcode in AppPer.objects.all():
            exists_appcode.append(each_appcode.to_json()['app_code'])


        for each_data in data:
            if  each_data[2] not in exists_appcode:
                client = AppPer(app_code=each_data[2],app_name=each_data[1],app_userlist='["admin"]')
                client.save()

        return render_mako_context(request,'/home_application/app_perm/app_list.html',{"data":data,"result":True})

    except Exception,e:
        if len(data) == 0:
            data = u'数据库连接信息为空'
        else:
            data = e
        return render_mako_context(request,'/home_application/app_perm/app_list.html',{"data":data,"result":False})


def app_permission(request):
    '''
    @note: 查询数据库后返回该APP所包含的用户
    '''
    app_code = request.GET.get('app_code')
    app_name = request.GET.get('app_name')
    try:
        users = ''

        for each_data in AppPer.objects.filter(app_code=app_code):
            users = each_data.to_json()['app_userlist']
        return render_mako_context(request,'/home_application/app_perm/app_permission.html',{'app_code':app_code,'app_name':app_name,'app_users':json.loads(users)})
    except Exception,e:
        return HttpResponse(e)

@csrf_exempt
def del_users(request):
    '''
    @note: 删除某个用户对某个APP的访问权限
    '''
    if request.method == 'POST':
        app_user = request.GET.get('app_user')
        app_code = request.GET.get('app_code')
        try:
            users = ''
            for each_data in AppPer.objects.filter(app_code=app_code):
                users = each_data.to_json()['app_userlist']

            app_userlist = json.loads(users)
            app_userlist.remove(app_user)
            AppPer.objects.filter(app_code=app_code).update(app_userlist=json.dumps(app_userlist))

            result = {"result":True,"messages":u'删除成功...'}
            return render_json(result)
        except Exception,e:
            result = {"result":True,"messages":u'删除失败{}'.format(e)}
            return render_json(result)

@csrf_exempt
def add_users(request):
    '''
    @note: 添加某个用户对某个APP的访问权限
    '''
    if request.method == 'POST':

        app_user = request.GET.get('app_user')
        app_code = request.GET.get('app_code')

        print app_user,app_code
        try:
            users = ''
            for each_data in AppPer.objects.filter(app_code=app_code):
                users = each_data.to_json()['app_userlist']

            app_userlist = json.loads(users)
            app_userlist.append(app_user)
            AppPer.objects.filter(app_code=app_code).update(app_userlist=json.dumps(app_userlist))

            result = {"result":True,"messages":u'添加成功...'}
            return render_json(result)
        except Exception,e:
            result = {"result":True,"messages":u'添加失败{}'.format(e)}
            return render_json(result)

# 返回访问策略:
@login_exempt # 登录豁免(无需用户登录平台，直接可以访问该视图函数)
def return_result_b(request):
    '''
    @note: 查询某个用户对这个APP是否有访问权限

    @example:
    Request:
        pass平台域名 + /o/bkpermission/return_result_b/?app_code=xxxxx&username=xxxxx

    Return:
        {
            messages: "认证通过",
            result: true
        }

    '''
    try:
        res = AppPer.objects.filter(app_code=str(request.GET.get('app_code')))
        if len(res) == 0:
            result = {"result": False,"messages":u"您所访问该App不存在或没有访问权限，请联系管理员!"}
            return render_json(result)
        else:
            for each_appuserlist in res:

                app_userlist = each_appuserlist.to_json()
                if str(request.GET.get('username')) in app_userlist['app_userlist']:
                    result = {"result": True,"messages":u"认证通过"}
                    return render_json(result)
                else:
                    result = {"result": False,"messages":u"您没有权限访问该App!...请联系管理员!"}
                    return render_json(result)
    except Exception,e:
        return render_json({"result":True,"messages":u"访问出错啦!\n{}".format(e)})


@csrf_exempt
@login_exempt
def return_forbidden(request):
    '''
    @note: 返回所有平台统一的禁止页面
    '''
    PAAS_PLATURL = settings.BK_PAAS_HOST + "/platform" # 正式Domain
    REQUEST_USER = request.GET['username']  # 请求用户，用户名
    return render_mako_context(request,'/home_application/app_perm/403.html',{'PAAS_PLATURL':PAAS_PLATURL,'REQUEST_USER':REQUEST_USER})



@csrf_exempt
@login_exempt # 登录豁免(无需用户登录平台，直接可以访问该视图函数)
def test(request):

    if request.method == 'POST':
        print request.body

        result = {"reusult": True}
        return render_json(result)


    data = []
    try:
        for each_data in PaasCon.objects.all():
            data.append(each_data.to_json())

        prpcrypt_key = prpcrypt(PRPCRYPTO_KEY)  # 调用crypto 解密
        password =  prpcrypt_key.decrypt(data[0]['p_pass'])

        db = MySQLdb.connect(data[0]['p_host'],data[0]['p_user'],password,'open_paas',charset="utf8") # 一定要加连接时的字符
        cursor = db.cursor()
        cursor.execute("select * from paas_app where code != 'bk_agent_setup' and code != 'bk_monitor'") # 过滤掉自带saas应用(除了管理员身份都不能访问)
        data = cursor.fetchall()

        # 查询paas的app跟本地对比；若没有添加进数据库则添加
        exists_appcode = []

        for each_appcode in AppPer.objects.all():
            exists_appcode.append(each_appcode.to_json()['app_code'])


        for each_data in data:
            if  each_data[2] not in exists_appcode:
                client = AppPer(app_code=each_data[2],app_name=each_data[1],app_userlist='["admin"]')
                client.save()

        return render_mako_context(request,'/home_application/app_perm/test.html',{"data":data,"result":True})

    except Exception,e:
        if len(data) == 0:
            data = u'数据库连接信息为空'
        else:
            data = e
        return render_mako_context(request,'/home_application/app_perm/test.html',{"data":data,"result":False})

@login_exempt # 登录豁免(无需用户登录平台，直接可以访问该视图函数)
def return_data(request):
    data1 = {"app_name": 'test', "app_age": 10}
    try:
        for each_data in AppPer.objects.all():
            data.append(each_data.to_json())
            print each_data.to_json()
        data1 = {"app_name": 'test', "app_age": 10}
        return render_json(data1)

    except Exception,e:
        if len(data) == 0:
            data = u'数据库连接信息为空'
        else:
            data = e

        return render_json(data1)




@csrf_exempt
@login_exempt # 登录豁免(无需用户登录平台，直接可以访问该视图函数)
def students(request):

    if request.method == 'POST':
        action = request.POST['action']
        try:
            table_id = int(request.POST['aid'])
        except ValueError:
            pass


        if action == 'delete':
            try:
                Students.objects.get(id=table_id).delete()
                return render_json({'message':'删除成功','table_id':table_id})
            except Exception,e:

                return render_json({'message':'删除失败{0}'.format(e)})
        elif action == 'edit':
            # 编辑后更新保存数据库
            try:
                s_name = request.POST['s_name']
                s_age = request.POST['s_age']
                s_country = request.POST['s_country']

                item = Students.objects.get(id=table_id)
                item.s_name = s_name
                item.s_age = s_age
                item.s_country = s_country
                item.save()

                return render_json({'message':'修改成功','table_id':table_id})

            except Exception,e:
                return render_json({'message':'修改失败{0}'.format(e)})
        else:
            pass


    data = []
    try:
        for each_data in Students.objects.all():
            data.append(each_data.to_json())


        return render_mako_context(request,'/home_application/app_perm/students.html',{"data":data})
    except Exception,e:
        print e
