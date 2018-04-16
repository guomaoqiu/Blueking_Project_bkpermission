#-*- coding:utf-8 -*-

def enum(**enums):
    return type('Enum', (), enums)

AppStateEnum = enum(OUTLINE=0, DEVELOPMENT=1, TEST=3, ONLINE=4, IN_TEST=8, IN_ONLINE=9, IN_OUTLINE=10)
STATE_CHOICES = [
 (
  AppStateEnum.OUTLINE, u'已下架'),
 (
  AppStateEnum.DEVELOPMENT, u'开发中'),
 (
  AppStateEnum.TEST, u'测试中'),
 (
  AppStateEnum.ONLINE, u'已上线'),
 (
  AppStateEnum.IN_TEST, u'正在提测'),
 (
  AppStateEnum.IN_ONLINE, u'正在上线'),
 (
  AppStateEnum.IN_OUTLINE, u'正在下架')
 ]

STATE_CHOICES_DISPALY_DICT = dict(STATE_CHOICES)
AppOpenEnum = enum(OPEN_IN_ALL=1, OPEN_IN_TEST=2, OPEN_IN_PRO=3, OPEN_NONE=4)