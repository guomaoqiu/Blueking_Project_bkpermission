# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns('home_application.views',
	# app列表，默认为主页
    (r'^$', 'applist'),
    # 连接paas数据库配置页
    (r'^setting/$', 'setting'),
    # 配置用户app权限页
    (r'^app_permission/$', 'app_permission'),
    # 删除数据库配置
    (r'^del_db/$', 'del_db'),
    # 删除数据库配置
    (r'^return_result_b/$', 'return_result_b'),
    # 删除用户
    (r'^del_users/$', 'del_users'),
    # 添加用户
    (r'^add_users/$', 'add_users'),
    # 从paas同步数据
    (r'^test/$', 'test'),
    (r'^students/$','students'),
    (r'^return_data/$','return_data'),


    (r'^return_forbidden/$','return_forbidden')
)
