# -*- coding: utf-8 -*-

from django.db import models

class PaasCon(models.Model):
    p_host = models.CharField(u"主机",max_length=30,unique=True)
    p_pass = models.CharField(u"密码",max_length=120)
    p_user = models.CharField(u"用户",max_length=30)
    p_port = models.CharField(u"端口",max_length=30)

    def to_json(self):
        return {
        		'id':self.id,
                'p_host' : self.p_host,
                'p_pass' : self.p_pass,
                'p_user' : self.p_user,
                'p_port' : self.p_port,
        }


class AppPer(models.Model):
    '''
    @note: app对应的用户列表，即这个用户能访问哪些app
    '''
    app_code = models.CharField(u"app_code",max_length=30,unique=True)
    app_name = models.CharField(u"app名称",max_length=30)
    app_userlist = models.TextField(u"用户列表",null=True)


    def to_json(self):
        return {
                'id':self.id,
                'app_code' : self.app_code,
                'app_name' : self.app_name,
                'app_userlist' : self.app_userlist,

        }



class Students(models.Model):
    '''
    @note: 数据表格测试数据
    '''
    s_name = models.CharField(u"学生姓名",max_length=30,unique=True)
    s_age = models.CharField(u"学生年龄",max_length=30)
    s_country = models.TextField(u"学生国籍",null=True)


    def to_json(self):
        return {
                'id':self.id,
                's_name' : self.s_name,
                's_age' : self.s_age,
                's_country' : self.s_country,

        }
