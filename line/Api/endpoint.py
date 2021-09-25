
class Line_Endpoint:

    DEFAULT_HOST = "gws.naver.line.jp"
    LONG_POLLING = "/P4" #TCBinaryProtocol = P3
    NORMAL_POLLING = "/NP4"
    NORMAL = "/S4" #TCBinaryProtocol = S3
    COMPACT_MESSAGE = "/C5"
    COMPACT_PLAIN_MESSAGE = "/CA5"
    COMPACT_E2EE_MESSAGE ="/ECA5"
    REGISTRATION = "/api/v4/TalkService.do"
    NOTIFY_SLEEP = "/F4"
    NOTIFY_BACKGROUND = "/B"
    BUDDY = "/BUDDY4"
    SHOP = "/SHOP4"
    SHOP_AUTH = "/SHOP4A"
    UNIFIED_SHOP = "/TSHOP4"
    STICON = "/SC4"
    CHANNEL = "/CH4" #TCBinaryProtocol CH3
    CHANNEL_LONGPOLLING = "/CP4"
    SNS_ADAPTER = "/SA4"
    SNS_ADAPTER_REGISTRATION = "/api/v4p/sa"
    AUTH_EAP = "/ACCT/authfactor/eap/v1"
    USER_INPUT = ""
    USER_BEHAVOIR_LOG = "/L1"
    AGE_CHECK = "/ACS4"
    SPOT = "/SP4"
    CALL = "/V4"
    EXTERNAL_INTERLOCK = "/EIS4"
    TYPING = "/TS"
    COIN = "/COIN4"
    COIN_INFO = "/R2"
    PAY = "/PY4"
    WALLET = "/WALLET4"
    AUTH = "/RS4"
    AUTH_REGISTRATION = "/api/v4p/rs"
    AUTH_QUERY_PATH = "/Q"
    SEARCH_V2 = "/serach/v2"
    SERACH_V3 = "/search/v3"
    BEACON = "/BEACON4"
    PERSONA = "/PS4"
    SQUARE = "/SQS1"
    SQUARE_BOT = "/BP1"
    POINT = "/POINT4"
    LIFF = "/LIFF1"
    CHAT_APP = "/CAPP1"
    IOT = "/IOT1"
    USER_PROVIDED_DATA = "/UPD4"
    NEW_REGISTRATION = "/acct/pais/v1"
    SECONDARY_QR_LOGIN = "/acct/lgn/sq/v1"
    SECONDARY_QR_LOGIN_VERIFIER = '/acct/lp/lgn/sq/v1'
    USER_SETTING = "/US4"
    LINE_SPOT = "/ex/spot"
    BOT_OA_ID = "u0be3650c6619cc078452ce5ec11a86db"

    UA = {
       "ANDROID":"Line/10.18.0",
       "ANDROID_BETA":"LLA/2.11.1 Nexus 5X 10",
       "ANDROID_ALPHA":"androidapp.line/10.18.0 (Linux; U; Android 4.4.4; en-US; 2014817 Build/KTU84P)",
       "BOT":"androidapp.line/7.5.0 (Linux; U; Android 4.4.4; en-US; 2014817 Build/KTU84P)",
       "CHROMEOS":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
       "DESKTOPWIN":"Line/6.7.0",
       "DESKTOPMAC":"DESKTOP:MAC:6.5.9-MAVERICKS-x64(5.1.2)",
       "IOS":"Line/11.3.0 iPhone8,1 13.3",
       "IOSIPAD":"Line/11.3.0 iPad4,1 8.0",
       "IPHONE": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Safari Line/11.3.0",
       "VIRTUAL":"Virtual.line/7.5.0 (Linux; U; Android 4.4.4; en-US; 2014817 Build/KTU84P)",
       "WAP":"WAPapp.line/7.5.0 (Linux; U; Android 4.4.4; en-US; 2014817 Build/KTU84P)",
       "WEB":"Line/2017.0731.2132 CFNetwork/758.6 Darwin/15.0.0"
    }

    LA = {
        'ANDROID': "ANDROID  10.18.0  Android  OS  6.0",
        'ANDROID_BETA': "ANDROIDLITE  2.11.1  Android  OS  6.0",
        'ANDROID_ALPHA': "ANDROID  10.18.0  Android  OS  6.0",
        'BOT': 'BOT  1.7.2  Linux Kernel  3.14.7',
        'CHROMEOS': "CHROMEOS\t2.3.8\tChrome\tOS\t83.0.4103.97",
        'DESKTOPWIN': 'DESKTOPWIN\t6.7.0\tDESKTOP-ALFINONH\t10.0.0-NT-x64',
        'DESKTOPMAC': "DESKTOPMAC\t6.5.9-MAVERICKS-x64\tMAC\t5.1.2",
        'MAC': 'MAC\t3.4.1\tMacOS\t8',
        'IOS': "IOS\t11.3.0\tiOS\t13.3",
        'IOSIPAD': "IOSIPAD\t11.3.0\tiPad4\t8.0.1",
        "IPHONE": "IOS\t11.3.0\tiPhone_OS\t13.3",
        'VIRTUAL': 'VIRTUAL  10.3.0  LINE_VIRTUAL  7.5.0',
        'WAP': 'WAP  10.3.0  iPhone  OS  1',
        'WEB': 'WEB  10.3.0  iPhone  OS  1'
    }

    CHANNEL_ID = {
        'TIMELINE': '1341209850',
        'WEBTOON': '1401600689',
        'TODAY': '1518712866',
        'STORE': '1376922440',
        'MUSIC': '1381425814',
        'SERVICES': '1459630796',
        'LIFF': '1654055086',
        'LIFF_V1': '1654260419',
        'LIFF_V2': '1654578478',
        'LIFF_SERVICE': '1654055086-BoD0ExEX',
        'DEFAULT': '1604066537-dl9GVZzo'
    }

    CHANNEL_SCREET = {
        'LIFF': 'CHANNEL_SCREET',
        'LIFF_V1': 'CHANNEL_SCREET',
        'LIFF_V2': 'CHANNEL_SCREET'
    }

    DEFAULT_HEADERS = {
       "User-Agent": "",
       "X-Line-Application": "",
       "x-lal" : "ja-JP_JP",
       "x-lhm": "POST"
    }
    
    DEFAULT_DATA = {
        "protectcancel": [],
        "protectinvite": [],
        "protectjoin": [],
        "protectkick": [],
        "protectname": [],
        "protectpicture": [],
        "protectqr": [],
        "gname": {},
        'image': {},
        'cover': {},
        'postId': {},
        'prefix': {
            'status': False,
            'key': ''
        },
        "autoLike": {
            "comment": "Manual like by:\nLinepoll-Client\n\n\ud83d\udc49 https://tinyurl.com/a-nhofficial\n\n\ud83d\udc49 https://tinyurl.com/finbot-creator",
                "commentWithSticker": {
                    "download": False,
                    "status": False,
                    "sticker": {
                        "STKID": 51626504,
                        "STKPKGID": 11538,
                        "STKVER": 1
                }
            },
            "status": True
        },
        'autoadd':{
            'status': False,
            "reply":{
                'status': False,
                'msg': 'Thanks for add me...'
            }
        },
        'autojoin': {
            'status': True,
            'ticket': True,
            'reply':{
                'status': True,
                'msg': 'Thanks for invited me.. @! '
            }
        },
        'unsendmessage': {},
        "owner": [
            "u8e6d34247f5f0adc92bf10a399f94fbc"
        ],
        "admin": [
            "u8e6d34247f5f0adc92bf10a399f94fbc"
        ],
        'lurking': {},
        'rname': '',
        'template': {},
        "mute": {},
        "token": False,
        "blacklist": {}
        }