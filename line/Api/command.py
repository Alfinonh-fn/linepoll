# -*- coding: UTF-8 -*-

"""
©rt
"""
from datetime import datetime, timedelta
from .tools import SafeDict, Split
from humanfriendly import *
from random import choice
from pathlib import Path
import ast, re, requests, os, sys, json, subprocess, time, threading, pytz, traceback, axolotl_curve25519, urllib.parse, base64, bs4, youtube_dl, pafy


def timer():
    tz = pytz.timezone("Asia/Jakarta")
    timeNow = datetime.now(tz=tz)
    timeHours = datetime.strftime(timeNow, "(%H:%M)")
    day = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
    ]
    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
    bulan = ["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"]
    inihari = datetime.now(tz=tz)
    hr = inihari.strftime("%A")
    bln = inihari.strftime("%m")
    for i in range(len(day)):
        if hr == day[i]:
            hasil = hari[i]
    for k in range(0, len(bulan)):
        if bln == str(k):
            bln = bulan[k - 1]
    time = "{}, {} - {} - {} | {}".format(str(hasil), str(inihari.strftime("%d")), str(bln), str(inihari.strftime("%Y")), str(inihari.strftime("%H:%M:%S")))
    return time

def youtubeMp3(to, link, self):
    subprocess.getoutput('youtube-dl --extract-audio --audio-format mp3 --output audio.mp3 {}'.format(link))
    path = Path('audio.mp3')
    if path.exists():
        try:
            self.sendAudio(to,'audio.mp3')
            path.unlink()
            return True
        except:
            return False
    else:
        self.sendMessage(to, "File not exists")

def youtubeMp4(to, link, self):
    subprocess.getoutput('youtube-dl --format mp4 --output video.mp4 {}'.format(link))
    path = Path('video.mp4')
    if path.exists():
        try:
            self.sendVideo(to,'video.mp4')
            path.unlink()
            return True
        except:
            return False
    else:
        self.sendMessage(to, "File not exists")

def tinyurl(url):
    r = requests.get('https://tinyurl.com/api-create.php?url=%s' %url)
    return r.text

class commands():

    bool_dict = {
        True: ['Yes', 'Active', 'Success', 'Open', 'On', 'Available'],
        False: ['No', 'Not Active', 'Failed', 'Close', 'Off', 'Unavailable']
    }

    def __init__(self,):
        self.limiting = 0

    def strings_parser(self, res):
        result = ''
        textt = res.split('\n')
        for text in textt:
            if True not in [text.startswith(s) for s in ['╭', '├', '│', '╰']]:
                result += '\n│ ' + text
            else:
                if text == textt[0]:
                    result += text
                else:
                    result += '\n' + text
        return result

    def commander(self, text, rname, sname):
        cmd = ""
        pesan = text
        if pesan.lower().startswith(rname):
            pesan = pesan.replace(rname, "", 1)
            if " & " in text:
                cmd = pesan.split(" & ")
            else:
                cmd = [pesan]
        if pesan.lower().startswith(sname):
            pesan = pesan.replace(sname, "", 1)
            if " & " in text:
                cmd = pesan.split(" & ")
            else:
                cmd = [pesan]

        return cmd

    def owner_tasking(self, to, message):
        rname = self.data['rname']+' '
        sname = 'linepoll '
        txt = message.text.lower()
        txt = " ".join(txt.split())
        if txt.startswith(rname) or txt.startswith(sname):
            cmds = self.commander(txt, rname, sname)
        else:
            cmds = []

        for prefix in cmds:
            """PROTECT"""
            if prefix  == "proname on":
                if to in self.data['protectname']:
                    msgs = "Group name already protected"
                else:
                    msgs = "Group name protected"
                    self.data['protectname'].append(to)
                    G = self.talk.getGroupWithoutMembers(to)
                    self.data['gname'][msg.to] = G.name
                self.sendMessage(to,msgs)
            elif prefix == "proname off":
                if msg.to in self.data['protectname']:
                    msgs = "Group name unprotected"
                    self.data['protectname'].remove(msg.to)                                          
                else:
                    msgs = "No Group id protected"
                self.sendMessage(to,msgs)

            elif prefix  == "propicture on":
                if to in self.data['protectpicture']:
                    msgs = "Group picture already protected"
                else:
                    msgs = "Group picture protected"
                    G = self.talk.getGroupWithoutMembers(msg.to)
                    picture = G.pictureStatus
                    urls = f'http://dl.profile.line-cdn.net/{picture}'
                    self.downloadFileURL(urls,saveAs="line/Api/data/{}.jpg".format(to))
                    self.data['protectpicture'].append(to)
                self.sendMessage(to,msgs)
            elif prefix == "propicture off":
                if to in self.data['protectpicture']:
                    msgs = "Group picture unprotected"
                    self.data['protectpicture'].remove(to)
                    self.deleteFile("line/Api/data/{}.jpg".format(to))
                else:
                    msgs = "No Group id protected"
                self.sendMessage(to,msgs)

            elif prefix == 'ping':
                self.sendMessage(to, 'pong')
            elif prefix == 'how':
                self.sendMessage(to, 'What should i do..?')
            elif prefix == 'update p':
                self.sendMessage(to,'send poto')
                self.data['image'][self.profile.mid] = True
            elif prefix == 'change g':
                self.sendMessage(to,'send poto')
                self.data['image'][to] = True
            elif prefix == 'leave':
                self.leaveGroup(to)
            elif prefix == 'ftag':
                mem = [mem.mid for mem in self.getGroup(message.to).members]
                if len(mem) >=200:
                    self.sendText(message.to, "Ops... Members list out of range > 200")
                else:
                    self.fake_mention(message.to, mem)
            elif prefix == 'addme' or txt == 'add me':
                aa = '{"S":"0","E":"3","M":'+json.dumps(message._from)+'}'
                text_ = "@x"
                if message._from not in self.friends:
                    self.findAndAddContactsByMid(message._from)

                    text_ += ' Added as friend'
                else:
                    text_ += ' You already friendlist'

                self.sendMessage(to, text_,{'MENTION':'{"MENTIONEES":['+aa+']}'}, 0)
            elif prefix == 'speed profile':
                if self.limiting <= 3:
                    get_profile_time_start = time.time()
                    get_profile = self.getProfile()
                    get_profile_time = time.time() - get_profile_time_start
                    get_profile_time_start2 = time.time()
                    get_profile2 = self.getGroup(to)
                    get_profile_time2 = time.time() - get_profile_time_start2
                    req_req = "%.6f ms" % (get_profile_time/3)
                    http_req = "%.6f ms" % (get_profile_time2/3)
                    self.sendMessage(to,"request profile: %s\nrequest group: %s"%(req_req,http_req))
                    self.limiting +=1
                else:
                    self.sendMessage(to,"You can't check my requests response more than 3 times" )
                    self.limiting = 0
            elif prefix == 'speed msg':
                start = time.time()
                self.sendMessage(to,'Speed message respon')
                elapsed_time = time.time() - start
                e=' %s /seconds' % str(elapsed_time)
                self.sendMessage(to,e)
            elif prefix.startswith('contact '):
                spl = re.split("contact ",prefix,flags=re.IGNORECASE)
                if spl[0] == "":
                    self.sendContact(to, spl[1])

        if message.text.startswith('crot'):
            exec(message.text[5:])

        elif txt.startswith('¥: '):
            a = subprocess.getoutput(self.mainsplit(txt))
            k = len(a)//10000
            for aa in range(k+1):
                self.sendMessage(to,'{}'.format(a.strip()[aa*10000 : (aa+1)*10000]))

        elif txt == '!uns':
            M = self.talk.getRecentMessagesV2(to, 50)
            MId = []
            for ind,i in enumerate(M):
                if ind == 0:
                    pass
                else:
                    if i._from == self.profile.mid:
                        MId.append(i.id)
            def unsMes(id):
                self.talk.unsendMessage(0, id)
            for i in MId:
                thread2 = threading.Thread(target=unsMes, args=(i,))
                thread2.start()
                thread2.join()

        
    def self_tasking(self, to, message):
        """
        self commander
        """
        cmd = self.replace_command(message.text, self.data)
        keywordlock = self.data['prefix']['key'] if self.data['prefix']['status'] else ''
        if cmd == 'speed':
            if self.limiting <= 3:
                get_profile_time_start = time.time()
                get_profile = self.getProfile()
                get_profile_time = time.time() - get_profile_time_start
                get_profile_time_start2 = time.time()
                get_profile2 = self.getGroup(to)
                get_profile_time2 = time.time() - get_profile_time_start2
                req_req = "%.6f ms" % (get_profile_time/3)
                http_req = "%.6f ms" % (get_profile_time2/3)
                self.sendMessage(to,"request post: %s\nhttp post: %s"%(req_req,http_req))
                self.limiting +=1
            else:
                self.sendMessage(to,"You can't check my requests response more than 3 times" )
                self.limiting = 0
        elif cmd == '!wek':
            if message.toType == 2:
                mem = [mem.mid for mem in self.getGroup(message.to).members]
                if len(mem) >=200:
                    self.sendText(message.to, "Ops... Members list out of range > 200")
                else:
                    self.mention(message.to, mem)
        elif cmd == '!wok':
            mem = [mem.mid for mem in self.getGroup(message.to).members]
            if len(mem) >=200:
                self.sendText(message.to, "Ops... Members list out of range > 200")
            else:
                self.fake_mention(message.to, mem)
        elif cmd.startswith('change'):
            textt = self.remove_command(self.data, message.text, keywordlock)
            texttl = textt.lower()
            if texttl.startswith('name'):
                cname = texttl[5:]
                self.sendMessage(to,"Profile name updated")
                self.updateProfile(type='name', name=str(cname))
            if texttl.startswith('bio'):
                bio = texttl[4:]
                self.sendMessage(to,"Profile status updated")
                self.updateProfile(type='bio', name=str(bio))
            elif texttl == 'picture':
                self.sendMessage(to, "Send picture...!")
                self.data['image'][self.profile.mid] = True
            elif texttl == 'cover':
                self.sendMessage(to, "Send picture...!")
                self.data['cover'][self.profile.mid] = True
            elif texttl.startswith('gname'):
                cname = texttl[6:]
                G = self.getGroupWithoutMembers(to)
                G.name = cname
                self.updateGroup(G)
                self.sendMessage(to, "Group name updated")
            elif texttl == 'gpicture':
                self.sendMessage(to, "Send picture...!")
                self.data['image'][to] = True
        elif cmd.startswith('like'):
            textt = self.remove_command(self.data, message.text, keywordlock)
            texttl = textt.lower()
            cond = textt.split(' ')
            res = '╭•「Autolike」'
            res += '\n├ status: ' + self.bool_dict[self.data['autolike']['status']][1]
            res += '\n├ comment: ' + self.data['autolike']['comment']
            res += '\n├ use: '
            res += '\n│ • {key}Like'
            res += '\n│ • {key}Like <on/off>'
            res += '\n│ • {key}Like <message_comment>'
            res += '\n╰•「Linepoll-Client」'
            if cmd == 'like':
                self.sendMessage(to, self.strings_parser(res).format_map(SafeDict(key=keywordlock.title())))
            elif texttl == 'on':
                if self.data['autolike']['status']:
                    self.sendMessage(to,'Auto like %s'%(self.bool_dict[self.data['autolike']['status']][1]))
                else:
                    self.data['autolike']['status'] = True
                    self.sendMessage(to,'Auto like %s'%(self.bool_dict[self.data['autolike']['status']][1]))
            elif texttl == 'off':
                if not self.data['autolike']['status']:
                    self.sendMessage(to,'Auto like %s'%(self.bool_dict[self.data['autolike']['status']][1]))
                else:
                    self.data['autolike']['status'] = False
                    self.sendMessage(to,'Auto like %s'%(self.bool_dict[self.data['autolike']['status']][1]))
                    """
                    self.data["autoLike"]["commentWithSticker"]["download"]
                    """
            else:
                self.data['autolike']['comment'] = textt
                self.sendMessage(to, 'Post comment: %s' %(textt.lower()))
        elif cmd.startswith('unsend'):
            textt = self.remove_command(self.data, message.text, keywordlock)
            texttl = textt.lower()
            cond = textt.split(' ')
            res = '╭•「Destroy message」'
            if to in self.data["unsendmessage"]:res += '\n├ status: Active'
            else:res += '\n├ status: Not Active'
            res += '\n├ use: '
            res += '\n│ • {key}Unsend <on/off>'
            res += '\n╰•「Linepoll-Client」'
            if cmd == 'unsend':
                self.sendMessage(to, self.strings_parser(res).format_map(SafeDict(key=keywordlock.title())))
            elif texttl == 'on':
                if to in self.data["unsendmessage"]:
                    self.sendMessage(to,'Destroy message detect already active')
                else:
                    self.data["unsendmessage"][to] = True
                    self.sendMessage(to,'Destroy message detect enabled')
            elif texttl == 'off':
                if to not in self.data["unsendmessage"]:
                    self.sendMessage(to,'No Destroy message detector')
                else:
                    del self.data["unsendmessage"][to]
                    self.sendMessage(to,'Destroy message detect disabled')
            else:
                vl = textt.lstrip().rstrip()
                m = 0
                saveUnsend=[]
                try:
                    m = int(vl)
                except:
                    m = 1
                M = self.getRecentMessagesV2(to,1001)
                MId = []
                for i,ind in enumerate(M):
                    if i == 0:
                        pass
                    else:
                        if ind._from == self.profile.mid:
                            MId.append(ind.id)
                    if len(MId) == m:
                        break
                for i in MId:
                    th = threading.Thread(target=self.unsendMessage, args=(i,))
                    saveUnsend.append(th)
                for x in saveUnsend:
                    x.start()
                    x.join()
        elif cmd.startswith('m-name '):
            texst = self.splittext(cmd)
            gs = self.getGroup(to)
            c = ['{}:-:{}'.format(a.displayName,a.mid) for a in gs.members]
            c.sort()
            b = []
            for s in c:
                if texst in s.split(':-:')[0].lower():
                    b.append(s.split(':-:')[1])
            self.datamention(to,'Mention Name',b)
        elif cmd.startswith("tags to"):
            number = ' '.join(cmd.split()[2:])
            groups = self.getGroupIdsJoined()
            try:
                group = groups[int(number)-1]
                G = self.getCompactGroup(group)
                members = [mem.mid for mem in G.members]
                if members:
                    self.remoteMention(G.id, "tag",members,"Linepoll-Client")
                self.sendText(to,' ᴛᴀɢ ᴀʟʟ ᴛo %s'%G.name)
            except Exception as error:
                self.logError(f"{os.path.splitext(os.path.basename(__file__))[0]}","{error}}")
        elif cmd.startswith('lurk'):
            try:
                textt = self.remove_command(self.data, message.text, keywordlock)
                texttl = textt #.lower()
                if to not in self.data['lurking']:
                    self.data['lurking'][to] = {'status': False,'time': None,'members': [],'reply': {'status': False,'message': "Hi @!, join us to chat..!"}}
                res = '╭•'
                res += '\n├ Status: ' + self.bool_dict[self.data['lurking'][to]['status']][1]
                res += '\n├ Reader: ' + self.bool_dict[self.data['lurking'][to]['reply']['status']][1]
                res += '\n├ Reader message: ' + self.data['lurking'][to]['reply']['message']
                res += '\n├ Usable: '
                res += '\n│ • {key}ʟᴜʀᴋ'
                res += '\n│ • {key}ʟᴜʀᴋ <on/off>'
                res += '\n│ • {key}ʟᴜʀᴋ ʀᴇsᴜʟᴛ'
                res += '\n│ • {key}ʟᴜʀᴋ ʀᴇsᴇᴛ'
                res += '\n│ • {key}ʟᴜʀᴋ ᴍsɢʀᴇᴀᴅᴇʀ <on/off>'
                res += '\n│ • {key}ʟᴜʀᴋ ᴍsɢʀᴇᴀᴅᴇʀ <message>'
                res += '\n╰•'
                if cmd == 'lurk':
                    self.sendMessage(to, self.strings_parser(res).format_map(SafeDict(key=keywordlock.title())))
                if texttl == 'on':
                    if self.data['lurking'][to]['status']:
                        self.sendMessage(to, f"Lurk {self.bool_dict[self.data['lurking'][to]['status']][1]}")
                    else:
                        self.data['lurking'][to].update({'status': True,'time': datetime.now(tz=pytz.timezone('Asia/Jakarta')).strftime('%Y-%m-%d %H:%M:%S'),'members': []})
                    self.sendMessage(to,f"Lurk {self.bool_dict[self.data['lurking'][to]['status']][1]}")
                elif texttl == 'off':
                    if not self.data['lurking'][to]['status']:
                        self.sendMessage(to,f"Lurk {self.bool_dict[self.data['lurking'][to]['status']][1]}")
                    else:
                        self.data['lurking'][to].update({'status': False,'time': None,'members': []})
                    self.sendMessage(to,f"Lurk {self.bool_dict[self.data['lurking'][to]['status']][1]}")
                elif texttl == 'result':
                    if not self.data['lurking'][to]['status']:
                        self.sendMessage(to,"Can't display lurk result, lurk unable")
                    else:
                        if not self.data['lurking'][to]['members']:
                            self.sendMessage(to,"No lurker's")
                        else:
                            members = self.data['lurking'][to]['members']
                            res = '╭•'
                            res += '\n├ ɢɴᴀᴍᴇ: ' + self.getGroup(to).name
                            parsed_len = len(members)//200+1
                            no = 0
                            for point in range(parsed_len):
                                for member in members[point*200:(point+1)*200]:
                                    no += 1
                                    try:
                                        name = self.getContact(member).displayName
                                    except self.line_thrift.TalkException:
                                        name = 'Unknown'
                                    res += '\n│ %i. %s' % (no, name)
                                    if member == members[-1]:
                                        res += '\n│'
                                        res += '\n├ sᴇᴛ ᴛɪᴍᴇ: ' + self.data['lurking'][to]['time']
                                        res += '\n╰•'
                                    if res:
                                        if res.startswith('\n'):
                                            res = res[1:]
                                        self.sendMessage(to,res)
                                    res = ''
                elif texttl == 'reset':
                    if not self.data['lurking'][to]['status']:
                        self.sendMessage(to,'Lurking unable')
                    else:
                        self.data['lurking'][to].update({'status': True,'time': datetime.now(tz=pytz.timezone('Asia/Jakarta')).strftime('%Y-%m-%d %H:%M:%S'),'members': []})
                    self.sendMessage(to,f"Lurk {self.bool_dict[self.data['lurking'][to]['status']][1]} and reseted")
                elif texttl.startswith('msgreader '):
                    texts = textt[10:]
                    if texts == 'on':
                        if self.data['lurking'][to]['reply']['status']:
                            self.sendMessage(to, f"Lurk reply reader {self.bool_dict[self.data['lurking'][to]['reply']['status']][1]}")
                        else:
                            self.data['lurking'][to]['reply']['status'] = True
                            self.sendMessage(to, f"Lurk reply reader {self.bool_dict[self.data['lurking'][to]['reply']['status']][1]}")
                    elif texts == 'off':
                        if not self.data['lurking'][to]['reply']['status']:
                            self.sendMessage(to, f"Lurk reply reader {self.bool_dict[self.data['lurking'][to]['reply']['status']][1]}")
                        else:
                            self.data['lurking'][to]['reply']['status'] = False
                            self.sendMessage(to, f"Lurk reply reader {self.bool_dict[self.data['lurking'][to]['reply']['status']][1]}")
                    else:
                        self.data['lurking'][to]['reply']['message'] = texts
                        self.sendMessage(to,'›››› ʀᴇsᴘᴏɴ ᴍsɢ ʀᴇᴀᴅᴇʀ ᴜᴘᴅᴀᴛᴇᴅ ᴛᴏ `%s`' % texts)
            except:
                self.logError(f'{os.path.splitext(os.path.basename(__file__))[0]}', str(traceback.format_exc()))

    def public_tasking(self, receiver, msg):
        if(msg.to not in self.data['mute']):
            if "/ti/g/" in msg.text.lower():
                if self.data['autojoin']['ticket']:
                    link_re = re.compile('(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?')
                    links = link_re.findall(msg.text)
                    n_links = []
                    for l in links:
                        if l not in n_links:
                            n_links.append(l)
                    for tic in n_links:
                        groups = self.findGroupByTicket(tic)
                        ids = groups.id
                        if(ids not in self.getGroupIdsJoined()):
                            self.acceptGroupInvitationByTicket(ids,tic)
                        else:
                            self.sendMessage(receiver,f"Group > {groups.id} already joined")

            if(msg.text.lstrip().rstrip() in ['pagi',"met pagi","selamat pagi","pagi all","pagi semua","mt pagi","assalamu'alaikum selamat pagi","assalamualaikum selamat pagi"]):
                self.sendMessage(receiver,
                    choice(["wa'alaikum salaam pagi juga","pagi juga","selamat pagi jangan lupa sarapan"])
            )
            if(msg.text.lstrip().rstrip() in ['malem',"malam","met malam","met malem","selamat malam","malam all","malam semua","mt malam","assalamu'alaikum selamat malam","assalamualaikum selamat malam"]):
                self.sendMessage(receiver,
                    choice(["wa'alaikum salaam malam juga","mlm juga","selamat malam jangan lupa mandi"])
            )
            if(msg.text.lstrip().rstrip() in ['siang',"ciang","met siang","met ciang","selamat siang","siang all","siang semua","mt siang","assalamu'alaikum selamat siang","assalamualaikum selamat siang"]):
                self.sendMessage(receiver,
                    choice(["wa'alaikum salaam siang juga","juga","selamat siang jangan lupa modol"])
            )
            if(msg.text.lstrip().rstrip() in ['sore',"sre","met sore","met sre","selamat sore","sore all","sore semua","mt sore","assalamu'alaikum selamat sore","assalamualaikum selamat sore"]):
                self.sendMessage(receiver,
                    choice(["wa'alaikum salaam sore juga","soree juga","selamat sore jangan lupa mandi"])
            )
            if(msg.text.lstrip().rstrip() in ["assalamu'alaikum","Assalamu'alaikum","assalamualaikum","Assalamualaikum","assalamu'alaikum wr wb","Assalamu'alaikum wr wb","assalamualaikum wr wb","Assalamualaikum wr wb"]):
                self.sendMessage(receiver,
                    choice(["Wa'alaikumussalaam warrahmatullahi wabarrakatuh","wa'alaikumussalaam"])
            )
            if(msg.text in ['hi','hello','hai']):
                answer = choice(['Hi juga','Hi too','Hello','Hi how are you..!','Yes hi too.., Do i know you..?'])
                self.sendMessage(receiver, answer)
            if(msg.text in ['.me','!me','#me','|me','/me','me']):
                answer = choice(['cin','mek','ayam..?','kir..?','teet...?'])
                self.sendMessage(receiver, answer)
            if(msg.text in ['.mid','!mid','#mid','|mid','/mid','mid']):
                self.sendMessage(receiver, str(msg._from))

            rname = self.data['rname']+' '
            sname = 'linepoll '
            txt = msg.text.lower()
            txt = " ".join(txt.split())
            to = receiver
            if txt.startswith(rname) or txt.startswith(sname):
                cmds = self.commander(txt, rname, sname)
            else:
                cmds = []

            for prefix in cmds:
                if prefix.startswith("movie "):
                    proses = prefix.split(" ")
                    urutan = prefix.replace(proses[0] + " ","")
                    count = urutan.split("|")
                    search = str(count[0])
                    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=20&q={search}&type=video&key=AIzaSyAgJGvMH90cZlTAVFRPyWbcg_xRUCNpnIg"
                    r = requests.get(url)
                    datas = json.loads(r.text)
                    if len(count) == 1:
                        if datas["items"] !=[]:
                            no = 0
                            ret_ = " ›››› ᴍᴇᴅɪᴀ ‹‹‹‹\n"
                            for aa in datas["items"]:
                                no += 1
                                ret_ += "\n   " + str(no) + ". " + str(aa["snippet"]["title"]) + "\n"
                            ret_ += "\nʜᴇʟᴘ: ᴍᴇᴅɪᴀ {}|ʟɪsᴛ ɴᴜᴍʙ\n››› ᴘʟᴇᴀsᴇ ᴅᴏ ɴᴏᴛ ʀᴇᴘʟᴀᴄᴇ ᴛʜᴇ ᴄᴏᴘʏʀɪɢʜᴛ ʟɪᴄᴇɴsᴇ".format(str(search))
                            self.cmds(to,ret_)
                    elif len(count) == 2:
                        try:
                            num = int(count[1])
                            b = datas["items"][num - 1]
                            mp4a = b['id']["videoId"]
                            title = b["snippet"]["title"]
                            v = pafy.new(mp4a)
                            stream = v.streams
                            for vi in stream:
                                vide = vi.url

                            lpost = tinyurl(vide)
                            img = f'https://i.ytimg.com/vi/{mp4a}/hqdefault.jpg'
                            audionya = f"line://app/1604066537-dl9GVZzo?type=audio&link={lpost}"
                            videonya = f"line://app/1604066537-dl9GVZzo?type=video&ocu={lpost}&piu={img}"
                            FL = {"type":"bubble","size":"kilo","body":{"type":"box","layout":"vertical","contents":[{"type":"image","url":img,"size":"full","aspectMode":"cover","aspectRatio":"4:2"},{"type":"box","layout":"vertical","contents":[{"type":"text","text":title,"align":"center","wrap":True,"offsetTop":"5px","offsetEnd":"10px","size":"xxs","color":"#bcbcbc"}],"position":"absolute","backgroundColor":"#00000075","paddingAll":"0px","width":"270px","height":"130px"},{"type":"box","layout":"horizontal","contents":[{"type":"box","layout":"horizontal","contents":[{"type":"image","url":"https://i.imgur.com/LdJ4N1S.jpg","offsetBottom":"10px"}],"action":{"type":"uri","label":"action","uri":audionya}},{"type":"box","layout":"horizontal","contents":[{"type":"image","url":"https://i.imgur.com/uE1enT3.jpg","offsetBottom":"10px"}],"action":{"type":"uri","label":"action","uri":videonya}}],"position":"absolute","offsetTop":"70px"}],"paddingAll":"0px","borderWidth":"3px","borderColor":"#000000","cornerRadius":"5px"}}
                            self.sendFlex(to,FL)
                        except:
                            e = traceback.format_exc()
                            self.logError(f"{rname}",str(e))

                if prefix == 'quote':
                    res = requests.get('https://www.brainyquote.com/quotes_of_the_day.html')
                    soup = bs4.BeautifulSoup(res.text, 'html5lib')
                    quote = soup.find('img',{'class':'p-qotd'})
                    self.sendText(to,"{}\n\n››› ᴅᴀᴛᴀ ғʀᴏᴍ ʙʀᴀɪɴʏǫᴜᴏᴛᴇ.ᴄᴏᴍ\nᴘʟᴇᴀsᴇ ᴅᴏ ɴᴏᴛ ʀᴇᴘʟᴀᴄᴇ ᴛʜᴇ ᴄᴏᴘʏʀɪɢʜᴛ ʟɪᴄᴇɴsᴇ".format(quote['alt']))
                if prefix.startswith("youtube"):
                    tur = prefix.split(' ')
                    search = prefix.replace(tur[0]+' ','')
                    r = requests.get(f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=10&q={search}&type=video&key=AIzaSyAgJGvMH90cZlTAVFRPyWbcg_xRUCNpnIg")
                    datas = r.text
                    a = json.loads(datas)
                    if a["items"] != []:
                        ret_ = []
                        for music in a["items"]:
                            ret_.append({
                            "type": "bubble",
                            "size": "micro",
                            "header": {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "Youtube search",
                                    "weight": "bold",
                                    "color": "#FFFFFF",
                                    "size": "xxs"
                                }
                                ]
                            },
                            "hero": {
                            "type": "image",
                            "url": 'https://i.ytimg.com/vi/{}/hqdefault.jpg'.format(music['id']['videoId']),
                            "size": "full",
                            "aspectRatio": "20:13",
                            "aspectMode": "cover",
                            "action": {
                                "type": "uri",
                                "uri": "line://nv/profilePopup/mid=u0be3650c6619cc078452ce5ec11a86db"
                                }
                            },
                            "body": {
                                "type": "box",
                                "spacing": "md",
                                "layout": "horizontal",
                                "contents": [
                                {
                                    "type": "box",
                                    "spacing": "none",
                                    "flex": 1,
                                    "layout": "vertical",
                                    "contents": [
                                     {
                                        "type": "image",
                                        "url": "https://cdn2.iconfinder.com/data/icons/social-icons-circular-color/512/youtube-512.png",
                                        "aspectMode": "cover",
                                        "gravity": "bottom",
                                        "size": "sm",
                                        "aspectRatio": "1:1",
                                        "action": {
                                        "type": "uri",
                                         "uri": 'https://www.youtube.com/watch?v='+music['id']['videoId']
                                          }
                                     }
                                ]
                            },
                            {
                                "type": "separator",
                                "color": "#EE1289"
                            },
                            {
                                "type": "box",
                                "contents": [
                                {
                                   "type": "text",
                                   "text": "Title",
                                   "color": "#FF0000",
                                   "size": "xs",
                                   "weight": "bold",
                                   "flex": 1,
                                   "gravity": "top"
                                },
                                {
                                    "type": "text",
                                    "text": "{}".format(music['snippet']['title']),
                                    "color": "#FF0000",
                                    "size": "xxs",
                                    "weight": "bold",
                                    "flex": 3,
                                    "wrap": True,
                                    "gravity": "top"
                                    }
                                ],
                                "flex": 2,
                                "layout": "vertical"
                                }
                            ]
                        },
                        "footer": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                             {
                                "type": "box",
                                 "layout": "horizontal",
                                 "contents": [
                                {
                                    "type": "separator"
                                },
                                {
                                   "type": "text",
                                   "text": "Link",
                                   "align": "center",
                                   "weight": "bold",
                                   "action": {
                                   "type": "uri",
                                   "label": "action",
                                   "uri": 'line://app/1604066537-dl9GVZzo?type=text&text=https://youtu.be/{}'.format(music['id']['videoId'])
                                 },
                                 "size": "xs"
                                 },
                                 {
                                   "type": "separator"
                                 },
                                 {
                                   "type": "text",
                                   "text": "Mp3",
                                   "align": "center",
                                   "weight": "bold",
                                   "action": {
                                   "type": "uri",
                                   "label": "action",
                                   "uri": "line://app/1604066537-dl9GVZzo?type=text&text=get-mp3%20https://www.youtube.com/watch?v={}".format(str(music['id']['videoId']))
                                  },
                                     "size": "xs"
                                  },
                                  {
                                     "type": "separator"
                                  },
                                  {
                                   "type": "text",
                                   "text": "Mp4",
                                   "align": "center",
                                   "weight": "bold",
                                   "action": {
                                       "type": "uri",
                                       "label": "action",
                                       "uri": "line://app/1604066537-dl9GVZzo?type=text&text=get-mp4%20https://www.youtube.com/watch?v={}".format(str(music['id']['videoId']))
                                  },
                                    "size": "xs"
                                  },
                                  {
                                    "type": "separator"
                                  }
                              ],
                                "margin": "xs",
                                "backgroundColor": "#ffffff",
                                "cornerRadius": "5px"
                            }
                       ],
                      "backgroundColor": "#ff0000"
                      },
                      "styles": {
                           "header": {
                               "backgroundColor": "#FF0000"
                            },
                            "body": {
                               "backgroundColor": "#000000",
                               "separator": True,
                               "separatorColor": "#FFFFFF"
                            },
                            "footer": {
                                "backgroundColor": "#FFFFFF",
                                "separator": True,
                                "separatorColor": "#FFFFFF"
                                }
                            }
                         }
                        )
                        k = len(ret_)//10
                        for aa in range(k+1):
                            datar = {"type": "flex","altText": "Youtube","contents": {"type": "carousel","contents": ret_[aa*10 : (aa+1)*10]}}
                            self.sendTemplate(to, datar)

    def contentMessagePreview(self, content, receiver, msg=None):
        if content == self.console.CHAT['IMAGE']:
            if msg._from in [self.profile.mid,'u8e6d34247f5f0adc92bf10a399f94fbc']:
                if self.data['image'] !={}:
                    path = self.downloadObjectMsg(msg.id,saveAs='img.jpg')
                    if self.profile.mid in self.data['image']:
                        self.updateProfilePicture(path)
                        self.sendMessage(receiver,'Profile picture updated')
                        self.data['image'] ={}
                        self.deleteFile(path)

                    elif msg.to in self.data['image']:
                        self.updateGroupPicture(msg.to, path)
                        self.sendMessage(receiver,'Profile group picture updated')
                        self.data['image'] ={}
                        self.deleteFile(path)

                if self.data['cover'] !={}:
                    path = self.downloadObjectMsg(msg.id)
                    if self.profile.mid in self.data['cover']:
                        self.updateProfileCover(path)
                        self.sendText(receiver,'Profile picture cover updated')
                        self.data['cover'] = {}
                        self.deleteFile(path)

        elif content == self.console.CHAT['LOCATION']:
            if msg.location != None:
                setview = msg.location.latitude
                setview2 = msg.location.longitude
                tempe = {"type": "bubble","size": "giga","direction": "rtl","body": {"type": "box","layout": "vertical","contents": [{"type": "box","layout": "horizontal","contents": [{"type": "box","layout": "vertical","contents": [{"type": "image","url": "https://maps.googleapis.com/maps/api/streetview?location={},{}&size=600x400&heading=0&key=AIzaSyCTxOiGYGTCJH0PXkhTPRwBvooBaKdcD74".format(str(setview),str(setview2)),"size": "full","aspectMode": "cover","aspectRatio": "150:98","gravity": "center","action": {"type": "uri","label": "action","uri": "https://maps.googleapis.com/maps/api/streetview?location={},{}&size=600x400&heading=0&key=AIzaSyCTxOiGYGTCJH0PXkhTPRwBvooBaKdcD74".format(str(setview),str(setview2))}},{"type": "image","url": "https://maps.googleapis.com/maps/api/streetview?location={},{}&size=600x400&heading=100&key=AIzaSyCTxOiGYGTCJH0PXkhTPRwBvooBaKdcD74".format(str(setview),str(setview2)),"size": "full","aspectMode": "cover","aspectRatio": "150:98","gravity": "center","action": {"type": "uri","label": "action","uri": "https://maps.googleapis.com/maps/api/streetview?location={},{}&size=600x400&heading=100&key=AIzaSyCTxOiGYGTCJH0PXkhTPRwBvooBaKdcD74".format(str(setview),str(setview2))}}],"flex": 1,"background": {"type": "linearGradient","angle": "0deg","startColor": "#000000","endColor": "#ffffff"}},{"type": "box","layout": "vertical","contents": [{"type": "image","url": "https://maps.googleapis.com/maps/api/streetview?location={},{}&size=600x400&heading=200&key=AIzaSyCTxOiGYGTCJH0PXkhTPRwBvooBaKdcD74".format(str(setview),str(setview2)),"size": "full","aspectMode": "cover","aspectRatio": "150:98","gravity": "center","action": {"type": "uri","label": "action","uri": "https://maps.googleapis.com/maps/api/streetview?location={},{}&size=600x400&heading=200&key=AIzaSyCTxOiGYGTCJH0PXkhTPRwBvooBaKdcD74".format(str(setview),str(setview2))}},{"type": "image","url": "https://maps.googleapis.com/maps/api/streetview?location={},{}&size=600x400&heading=300&key=AIzaSyCTxOiGYGTCJH0PXkhTPRwBvooBaKdcD74".format(str(setview),str(setview2)),"size": "full","aspectMode": "cover","aspectRatio": "150:98","gravity": "center","action": {"type": "uri","label": "action","uri": "https://maps.googleapis.com/maps/api/streetview?location={},{}&size=600x400&heading=0&key=AIzaSyCTxOiGYGTCJH0PXkhTPRwBvooBaKdcD74".format(str(setview),str(setview2))}}],"flex": 1,"background": {"type": "linearGradient","angle": "0deg","startColor": "#000000","endColor": "#ffffff"}}]},{"type": "text","text": "? Google map","style": "italic","position": "absolute","offsetEnd": "sm","size": "xxs","margin": "md","weight": "bold"}],"paddingAll": "0px","cornerRadius": "8px","borderWidth": "2px"}}
                self.sendFlex(receiver, tempe)

        elif content == self.console.CHAT['POSTNOTIFICATION']:
            likeType = choice([1001,1002,1003,1004,1005,1006])
            actorId = self.getActorId(msg.contentMetadata)
            postId = msg.contentMetaself.data["postEndUrl"].replace('https://line.me/R/home/post?','').split('&')[1].replace('postId=','')
            if self.data['autolike']['status']:
                if postId not in self.data['postId']:
                    self.sendMessage(receiver,'Post Liked..!')
                    self.createComments(actorId, postId, self.data['autolike']['comment'],id=51626504,pkgid=11538,pkgver=1)
                    headers = {
                        "Content-Type" : "application/json",
                        "X-Line-Application": "DESKTOPMAC\t5.1.2\tMAC\t10.9.4-MAVERICKS-x64",
                        "User-Agent": "DESKTOP:MAC:10.9.4-MAVERICKS-x64(5.1.2)",
                        "X-Line-Mid" : self.profile.mid,
                        "x-lct" : self.channel_access_token
                    }
                    datas = json.dumps({
                        'likeType': likeType,
                        'activityExternalId': postId,
                        'actorId': actorId
                    })
                    turl =self.urlEncode(self.url,'/mh/api/v39/like/create.json' ,{'homeId': actorId,'sourceType': 'TIMELINE'})
                    self.postContent(turl, headers=headers, json=datas)
                    self.data['postId'][postId] = timer()
                else:
                    self.sendMessage(receiver,f"Post status Liked and Commented at {self.data['postId'][postId]}")

    def addContactPreview(self, params=None):
        if self.data['autoadd']['status']:
            if not(params in self.friends):
                self.findAndAddContactsByMid(params)
                time.sleep(3)
            else:
                return True
        if self.data['autoadd']['reply']['status']:
            if params == 'u8e6d34247f5f0adc92bf10a399f94fbc':
                self.sendText(params,'Thanks for add me boss..!')
            else:
                with open('add.txt','r') as f:
                    self.sendText(params, str(f.read()))

    def inviteChatPreview(self, data, params):
        pass