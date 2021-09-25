# -*- coding: UTF-8 -*-
"""
©
"""
from copy import deepcopy
from datetime import datetime

from pathlib import Path
from typing import Union, List, Dict, Any, Optional

from .curve.livejson import File, MergeJSON
from .curve.console import Console, make_client

from .Api.api import Api
from .Api.command import commands
from .Api.endpoint import Line_Endpoint
from .Api.liff import Liff
from .Api.poll import Poll
from .Api.talk import Talk
from .Api.call import Call
from .Api.shop import Shop
from .Api.timeline import Timeline
from time import sleep

__all__ =['File', 'MergeJSON', 'Path', 'Line_Endpoint']

class Linepoll(Api, Liff, Poll, Talk, Call, Shop, Timeline, commands):

    groups = None
    friends = None
    inviteed = None
    isLoggin = False
    isCrt = "line/Api/data/cert/"
    isToken = "line/Api/data/tokens/"
    certificate = None

    def __init__(self, 
        authToken=None, 
        authKey =None, 
        email=None, 
        password=None, 
        lhost = 'gxx.line.naver.jp', 
        device="IOS", 
        version= None, 
        system_name="Linepoll-Client",
        os_version= "6.7.0",
        mod_name="binary", file_name=None):
        assert device in Line_Endpoint.LA, 'Invalid Application types for %s \nCheck at app configuration types'%device

        self.console = Console
        self._func = Console.line_thrift
        self._connect = make_client
        self.endpoint = Line_Endpoint
        self.os_version = os_version
        self.host = f"https://{lhost}:443"
        self.url = f'https://{lhost}'

        self.APP_TYPE = device
        self.systemName = system_name
        self.file_name = file_name
        self.mod = mod_name
        Api.__init__(self)

        if not (authToken or authKey or email and password):
            self.secondaryQr(appType=device, systemName=system_name, version=os_version)

        if authToken:
            self.headers.update({'X-Line-Access': authToken})
            self.authToken = authToken
            self.login()

        if authKey:
            self.generateAccessToken(authKey)
            
        if(email and password):
            try:
                with open(self.isToken + email + '.session','r') as f:
                    ttkn = f.read()
                if ttkn:
                    print('\n: Validating token...\n\n')
                    sleep(3)
                    self.headers.update({'X-Line-Access': ttkn})
                    self.login()
                    print('\n: Login with authtoken success..!\n')
                    self.authToken = ttkn
            except Exception:
                print('\n(-) Opss...! token expired\n')
                sleep(5)
                print('\n(-) Please wait while regenerating new authToken')
                sleep(7)
                self.loginWithCredentialsForCrt(email,password)

        self.limit = False
        if(self.authToken and self.revision):
            self.initAll()

    def initAll(self):
        Liff.__init__(self)
        Poll.__init__(self)
        Talk.__init__(self)
        Call.__init__(self)
        Shop.__init__(self)
        Timeline.__init__(self)
        commands.__init__(self)

        self._loginLineTimeline()

        str_to_encode = self.dir_name(self.profile.mid)
        if Path(f"{str_to_encode}.json").exists():
            self._datttta = File(f"{str_to_encode}.json", True, True, 4)
            self.data = self._datttta['group']
        else:
            db = File(f"{str_to_encode}.json", True, True, 4)
            self.data = self.endpoint.DEFAULT_DATA
            if not "group" in db:db['group'] = self.data;self.data=db['group']
            else:self.data=db['group']

        if self.file_name:
            self.data['rname'] = self.file_name
        else:self.data['rname'] = "line"

        print(f"Name: {self.profile.displayName}\nMid: {self.profile.mid}\nAuthToken: {self.authToken}")
