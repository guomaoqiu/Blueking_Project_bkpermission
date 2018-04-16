# -*- coding: utf-8 -*-
from ..base import ComponentAPI


class CollectionsCMSI(object):
    """Collections of CMSI APIS"""

    def __init__(self, client):
        self.client = client

        self.noc_notice = ComponentAPI(
            client=self.client, method='POST', path='/api/c/compapi/cmsi/noc_notice/',
            description=u'公共语音通知',
        )
        self.send_mail = ComponentAPI(
            client=self.client, method='POST', path='/api/c/compapi/cmsi/send_mail/',
            description=u'发送邮件',
        )
        self.send_qy_weixin = ComponentAPI(
            client=self.client, method='POST', path='/api/c/compapi/cmsi/send_qy_weixin/',
            description=u'发送企业微信',
        )
        self.send_sms = ComponentAPI(
            client=self.client, method='POST', path='/api/c/compapi/cmsi/send_sms/',
            description=u'发送短信',
        )
