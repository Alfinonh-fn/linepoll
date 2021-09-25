import line

from datetime import datetime, timedelta

from random import choice, randint, shuffle

import asyncio, ast, axolotl_curve25519, base64, json, os, re, sys, traceback, time, urllib, urllib.parse, subprocess, youtube_dl, uvloop

file_name = os.path.splitext(os.path.basename(__file__))[0]

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

ttt = "F76CZnUH4FqhENV6GkA3.5j5UGRPFsf8kw3NU2s1reW.Dng/7U/FH21YV1cr50380opWJrUN6KQ5ACsjsMmMOkI="

Line = line.Linepoll(

    authToken = ttt,

    device = "DESKTOPWIN",

    lhost = 'gxx.line.naver.jp' ,

    mod_name='binary',

    file_name = file_name

)

data = Line.data
owner = ["u8e6d34247f5f0adc92bf10a399f94fbc"]
admin = ["u8e6d34247f5f0adc92bf10a399f94fbc"]

def restartBot():

    os.system('clear')

    linepollv3 = sys.executable

    os.execl(linepollv3, linepollv3,*sys.argv)

def update_file():

    pass

def receiverPreview(message, users=None):

    if message.toType == 0:

        if message._from != users:

            receiver = message._from

        else:

            receiver = message.to

    if message.toType == 1:

        receiver = message.to

    if message.toType == 2:

        receiver = message.to

    return receiver

async def LineUnofficial(op):

    try:

        if op.type == 0:

            return

        if op.type == 5:

            Line.addContactPreview(params=op.param1)

        if(op.type == 11 or op.type == 122):

            if op.param3 == '1':

                if op.param1 in data['protectname'] and op.param2 not in(owner or admin):

                    group = Line.getGroupWithoutMembers(op.param1)

                    group.name = data["gname"][op.param1]

                    Line.updateGroup(group)

                    Line.sendMention(op.param1, "Group Name protected\n\n@! You have been warned..!",'',[op.param2])

                    data["blacklist"][op.param2] = True

            if op.param3 == '2':

                if op.param1 in data['protectpicture'] and op.param2 not in(owner or admin):

                    group = Line.getGroupWithoutMembers(op.param1)

                    path = 'line/Api/data/%s.jpg'%(op.param1)

                    Line.updateGroupPicture(op.param1,path)

                    Line.sendMention(op.param1, "Group picture protected\n\n@! You have been warned..!",'',[op.param2])

                    data["blacklist"][op.param2] = True

            if op.param3 == '4':

                if op.param1 in data['protectqr']:

                    G=Line.getGroupWithoutMembers(op.param1)

                    if G.preventedJoinByTicket == False:

                        if op.param2 not in(owner or admin):

                            Line.joinByTicket(op.param1)

                            Line.sendMention(op.param1,"@! Please don't open group link anymore",'',[op.param2])

                            data["blacklist"][op.param2] = True

            if(op.param2 in data['blacklist'] and op.param2 not in(owner or admin)):

                Line.kickoutFromGroup(op.param1, [op.param2])

        if op.type == 13 or op.type == 124:

            if op.param3 == Line.profile.mid:

                try:

                    Line.acceptGroupInvitation(op.param1)

                except:pass

                if op.param2 not in(owner or admin):

                    Line.leaveGroup(op.param1)

        if op.type == 19 or op.type == 133:

            if op.param3 in(owner or admin):

                if not op.param3 in Line.friends:

                    Line.findAndAddContactsByMid(op.param3)

                try:

                    Line.inviteIntoGroup(op.param1,[op.param3])

                except:

                    G = Line.getGroup(op.param1)

                    if G.preventedJoinByTicket == False:

                        tckt = Line.reissueGroupTicket(op.param1)

                    else:

                        G.preventedJoinByTicket = False

                        Line.updateGroup(G)

                        tckt = Line.reissueGroupTicket(op.param1)

                    Line.sendText(op.param3, f"https://line.me/R/ti/g/{tckt}")

                    Line.sendMessage(op.param1, 'Creator gue jangan di ciak nyet..!')

        if op.type == 26:

            msg = op.message

            if(msg.toType == 0 or msg.toType == 1 or msg.toType == 2):

                receiver = receiverPreview(op.message,users=Line.profile.mid)

                if msg.contentType == 0:

                    if msg.text is None:

                        return

                    else:

                        try:

                            Line.public_tasking(

                                    receiver,

                                    msg

                            )

                        except:

                            error = traceback.format_exc()

                            Line.logError(f'{file_name} \n', str(error))

                        if msg._from in(owner or admin):

                            try:

                                Line.owner_tasking(

                                    receiver,

                                    msg

                                )

                            except:

                                error = traceback.format_exc()

                                Line.logError(f'{file_name} \n', str(error))

                            if(msg.text == 'restart'):

                                try:

                                    Line.sendMessage(receiver,'restart....')

                                    restartBot()

                                except:pass

                            if msg.text == '!tkn':

                                if data['token']==True:

                                    certificate = ""

                                    cl = Line._connect(host = Line.host,

                                        path="/acct/lgn/sq/v1",

                                        http_header_factory={

                                          'User-Agent': 'Line/6.7.0',

                                          'X-Line-Application': 'DESKTOPWIN\t6.7.0\tDESKTOP-ALFINONH\t10.0.0-NT-x64;SECONDARY',

                                          'x-lal': 'en_id',

                                          'server': choice(["pool-1","pool-2"])

                                        },

                                        service=Line.console.LoginService,

                                        isOpen=False

                                    )

                                    session = cl.createSession(Line._func.CreateQrSessionRequest())

                                    session_id = session.authSessionId

                                    sys.stdout = open('login.txt', 'w')

                                    qrcode = cl.createQrCode(Line._func.CreateQrCodeRequest(session_id))

                                    qrCode = qrcode.callbackUrl

                                    private_key = axolotl_curve25519.generatePrivateKey(os.urandom(32))

                                    public_key = axolotl_curve25519.generatePublicKey(private_key)

                                    secret = urllib.parse.quote(base64.b64encode(public_key).decode())

                                    datang = f"{qrCode}?secret={secret}&e2eeVersion=1"

                                    print(datang)

                                    sys.stdout.close()

                                    sys.stdout = sys.__stdout__

                                    with open('login.txt', 'r') as f:

                                        output = f.read()

                                    Line.sendMessage(receiver, str(output))

                                    os.remove('login.txt')

                                    client_verif = Line._connect(host = Line.host,

                                        path="/acct/lp/lgn/sq/v1",

                                        http_header_factory={

                                          'User-Agent': 'Line/6.7.0',

                                          'X-Line-Application': 'DESKTOPWIN\t6.7.0\tDESKTOP-ALFINONH\t10.0.0-NT-x64;SECONDARY',

                                          'X-Line-Access': session_id,

                                          'x-lal': 'en_id',

                                          'server': choice(["pool-1","pool-2"])

                                        },

                                        service=Line.console.LoginPermitNoticeService,

                                        isOpen=False

                                    )

                                    qrverified = client_verif.checkQrCodeVerified(

                                            Line._func.CheckQrCodeVerifiedRequest(session_id)

                                    )

                                    if certificate == "oke":

                                        certificate = input(certificate)

                                    else:

                                        try:

                                            certverified = cl.verifyCertificate(

                                                Line._func.VerifyCertificateRequest(session.authSessionId, certificate)

                                            )

                                        except Exception as error:

                                            print ('Error Verify Certificate :', error)                                

                                            sys.stdout = open('login.txt', 'w')

                                            pincode = cl.createPinCode(

                                                Line._func.CreatePinCodeRequest(session.authSessionId)

                                            )

                                            print (pincode.pinCode)

                                            sys.stdout.close()

                                            sys.stdout = sys.__stdout__

                                            with open('login.txt', 'r') as f:

                                                output = f.read()

                                                print (output)

                                            Line.sendMessage(receiver, output)

                                            sys.stdout = open('login.txt', 'w')

                                            pincodeverified = client_verif.checkPinCodeVerified(

                                                Line._func.CheckPinCodeVerifiedRequest(session.authSessionId)

                                            )

                                            print (pincodeverified)

                                            sys.stdout.close()

                                            sys.stdout = sys.__stdout__

                                            with open('login.txt', 'r') as f:

                                                output = f.read()                                    

                                            Line.sendMessage(receiver, output)

                                            sys.stdout = open('login.txt', 'w')

                                        except Exception:

                                            traceback.print_exc()

                                        sys.stdout = open('login.txt', 'w')

                                        qrcodelogin = cl.qrCodeLogin(

                                            Line._func.QrCodeLoginRequest(session.authSessionId, 'DESKTOP-ALFINONH', True)

                                        )

                                        print (f'Qr Code Login : {qrcodelogin.accessToken}\nCRT : {qrcodelogin.certificate}')

                                        sys.stdout.close()

                                        sys.stdout = sys.__stdout__

                                        with open('login.txt', 'r') as f:

                                            output = f.read()

                                        Line.sendMessage(receiver, output)

                                else:

                                    Line.sendMessage(receiver,"Failed")

        if op.type == 25:

            msg = op.message

            if(msg.toType == 0 or msg.toType == 1 or msg.toType == 2):

                receiver = receiverPreview(op.message, users=Line.profile.mid)

                if msg.contentType == 0:

                    if msg.text is None:

                        return

                    else:

                        if(msg.text == 'reboot'):

                            try:

                                Line.sendMessage(receiver,'rebooting....!')

                                restartBot()

                            except:pass

                        try:

                            Line.self_tasking(

                                receiver,

                                msg

                            )

                        except:

                            Line.logError(f'{file_name} \n', str(traceback.format_exc()))

                        if msg.text.startswith("profile-youtube"):

                            link = msg.text[16:]

                            pict = Line.downloadFileURL("http://dl.profile.line-cdn.net/{}".format(str(Line.getProfile().pictureStatus)))

                            Line.sendMessage(receiver,'Downloading image')

                            try:

                                subprocess.getoutput('youtube-dl --format mp4 --output video.mp4 {}'.format(link))

                                Line.sendMessage(receiver,'Rendering video')

                                time.sleep(8)

                                vprof = Line._session.post('https://obs-sg.line-apps.com/talk/vp/upload.nhn', headers=Line.headers, data = {'params': json.dumps({'name': 'media', 'oid': Line.profile.mid, 'size': len(open('video.mp4','rb').read()),'type': 'video','cat': 'vp.mp4','ver': '1.0'})}, files={'file': open("video.mp4", 'rb')})

                                Line.updateProfilePicture(pict, 'vp')

                                Line.sendMessage(receiver,'Profile video updated')

                                time.sleep(3)

                                Line.deleteFile(pict)

                                Line.deleteFile('video.mp4')

                            except:

                                e = traceback.format_exc()

                                Line.logError('> ', str(e))

        if op.type == 25 or op.type == 26:

            msg = op.message

            if(msg.toType == 0 or msg.toType == 1 or msg.toType == 2):

                receiver = receiverPreview(op.message,users=Line.profile.mid)

                Line.contentMessagePreview(msg.contentType, receiver, msg=msg)

    except:

        error = traceback.format_exc()

        Line.logError(f'{file_name} \n', str(error))

async def main():

    while True:

        try:

            Ops = Line.singleTrace()

            if Ops is not None:

                for op in Ops:

                    await LineUnofficial(op)

                    Line.setRevision(op.revision)

                    if op.type != 0:

                        print("OP->",Line.console.operations[op.type].replace("_","::"))

        except EOFError:

            return

loop = asyncio.get_event_loop()

if __name__== '__main__':

    try:

        loop.run_until_complete(main())

    finally:

        loop.close()

