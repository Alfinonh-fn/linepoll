from .session import Server
from random import choice
from copy import deepcopy
import axolotl_curve25519, base64, hmac, time, hashlib, json, os, rsa, re, requests, socket, sys, traceback, urllib.parse

class Api(Server):

    def __init__(self,):
        Server.__init__(self)
        self.headers.update({
           "User-Agent": self.endpoint.UA[self.APP_TYPE],
           "X-Line-Application": self.endpoint.LA[self.APP_TYPE]
        })

        self.fake_headers = deepcopy(self.headers)
        self.fake_headers.update({
           "x-le": "18",
           "x-lap": "4",
           "x-lpv": "1",
           "content-type": "application/x-thrift; protocol=TBINARY",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        })

        self._talk_service_do = self._connect(host=self.host, 
                       path= self.endpoint.REGISTRATION,
                       Headers= self.headers,
                       service=self.console.TalkService, isOpen=False)

        self._auth = self._connect(host=self.host,
                     path= self.endpoint.AUTH_REGISTRATION,
                     Headers=self.headers, 
                     service=self.console.AuthService, isOpen=False)

    def login(self) -> bool:
        if self.mod == "binary":
            path = "/P3"
        else:
            path = self.endpoint.LONG_POLLING

        self.poll = self._connect(host=self.host, 
                                                 path= path,
                                                 Headers=self.headers,
                                                 service=self.console.PollService, proto=True, method=self.mod)

        self.revision = self.poll.getLastOpRevision()
        self.isLoggin = True
        return True

    def normalizePhoneNumber(self, countryCode, phoneNumber, countryCodeHint):
        return self._auth.normalizePhoneNumber(countryCode, phoneNumber, countryCodeHint)

    def respondE2EELoginRequest(self, verifier, publicKey, encryptedKeyChain, hashKeyChain, errorCode):
        return self._auth.respondE2EELoginRequest(verifier, publicKey, encryptedKeyChain, hashKeyChain, errorCode)

    def confirmE2EELogin(self, verifier, deviceSecret):
        return self._auth.confirmE2EELogin(verifier, deviceSecret)

    def logoutZ(self):
        return self._auth.logoutZ()

    def loginZ(self, loginRequest):
        return self._auth.loginZ(loginRequest)

    def issueTokenForAccountMigrationSettings(self, enforce):
        return self._auth.issueTokenForAccountMigrationSettings(enforce)

    def issueTokenForAccountMigration(self, migrationSessionId):
        return self._auth.issueTokenForAccountMigration(migrationSessionId)

    def verifyQrcodeWithE2EE(self, verifier, pinCode, errorCode, publicKey, encryptedKeyChain, hashKeyChain):
        return self._auth.verifyQrcodeWithE2EE(verifier, pinCode, errorCode, publicKey, encryptedKeyChain, hashKeyChain)

    def __write_val(self, data):
        return (chr(len(data)) + data)
		
    def __gen_message(self, tuple_msg):
        return (''.join(tuple_msg)).encode('utf-8')

    def __rsa_crypt(self, message, RSA):
        pub_key = rsa.PublicKey(int(RSA.nvalue, 16), int(RSA.evalue, 16))
        crypto  = rsa.encrypt(message, pub_key)
        return crypto

    def _encryptedEmailAndPassword(self, mail, passwd, RSA):
        message_ = (
            self.__write_val(RSA.sessionKey),
            self.__write_val(mail),
            self.__write_val(passwd),
        )
        message = self.__gen_message(message_)
        crypto  = self.__rsa_crypt(message, RSA).hex()
        return crypto

    def _encryptedPhoneAndPassword(self, phone, password, RSA):
        message_ = (
            self.__write_val(RSA.sessionKey),
            self.__write_val(phone),
            self.__write_val(password),
        )
        message = self.__gen_message(message_)
        crypto  = self.__rsa_crypt(message, RSA).hex()
        return crypto

    def get_issued_at(self) -> bytes:
        return base64.b64encode(
            f"iat: {int(time.time()) * 60}\n".encode("utf-8")) + b"."

    def get_digest(self, key: bytes, iat: bytes) -> bytes:
        return base64.b64encode(hmac.new(key, iat, hashlib.sha1).digest())

    def dir_name(self, str_to_encode: str):
        hasher = hashlib.md5()
        hasher.update(str_to_encode.encode('utf-8'))
        directory_name = hasher.hexdigest()
        return f"{directory_name}"

    def sign_with_requests_session(self, type, data):
        lReq = self._func.LoginRequest()
        if type == '0':
            lReq.type = 0
            lReq.identityProvider = data['identityProvider']
            lReq.identifier = data['identifier']
            lReq.password = data['password']
            lReq.keepLoggedIn = data['keepLoggedIn']
            lReq.accessLocation = data['accessLocation']
            lReq.systemName = data['systemName']
            lReq.certificate = data['certificate']
            lReq.e2eeVersion = data['e2eeVersion']
        elif type == '1':
            lReq.type = 1
            lReq.keepLoggedIn = data['keepLoggedIn']
            if 'identityProvider' in data:
                lReq.identityProvider = data['identityProvider']
            if 'accessLocation' in data:
                lReq.accessLocation = data['accessLocation']
            if 'systemName' in data:
                lReq.systemName = data['systemName']
            lReq.verifier = data['verifier']
            lReq.e2eeVersion = data['e2eeVersion']
        else:
            lReq=False
        return lReq

    def loginWithCredentialsForCrt(self, email, passwd, certificate= None, systemName = None, appName=None):
        if systemName is None:
            systemName=self.systemName

        if re.compile(r"[^@]+@[^@]+\.[^@]+").match(email):
            self.provider = 1
        else:
            self.provider = 2

        if appName is None:
            appName = self.APP_TYPE

        rsaKey      = self._talk_service_do.getRSAKeyInfo(self.provider)
        crypto     = self._encryptedEmailAndPassword(email, passwd, rsaKey)
        try:
            with open(self.isCrt + email + '.crt', 'r') as f:
                self.certificate = f.read()
        except:
            if certificate is not None:
                self.certificate = certificate
                if os.path.exists(certificate):
                    with open(certificate, 'r') as f:
                        self.certificate = f.read()

        accessLocation = socket.gethostbyname(socket.gethostname())
        lReq = self.sign_with_requests_session('0', {
            'identityProvider': self.provider,
            'identifier': rsaKey.keynm,
            'password': crypto,
            'keepLoggedIn': True,
            'accessLocation': accessLocation,
            'systemName': systemName,
            'certificate': self.certificate,
            'e2eeVersion': 0
        })
        result = self.loginZ(lReq)
        if result.type == 1:
            self.headers.update({
                'X-Line-Access': result.authToken
            })
            self.certificate = result.certificate
            self.authToken = result.authToken
            self.login()
            self.__defaultCallback("loginWithCredentialsForCertificate: success")
            with open(self.isToken + email +'.session','w') as f:
                f.write(result.authToken)

        elif result.type == 3:
            self.__defaultCallback("›››› Input your pin code on your LINE apps: %s ‹‹‹‹"%result.pinCode)
            self.headers['X-Line-Access'] = result.verifier
            content = requests.get(self.url+self.endpoint.AUTH_QUERY_PATH,headers=self.headers).text
            getAccessKey = json.loads(content)
            try:
                _lreq = self.sign_with_requests_session('1', {
                    'identityProvider': self.provider,
                    'keepLoggedIn': True,
                    'accessLocation': accessLocation,
                    'systemName': systemName,
                    'verifier': getAccessKey['result']['verifier'],
                    'e2eeVersion': 0
                })
                result2 = self.loginZ(_lreq)
            except:
                raise Exception('Login failed <%s>'%email)

            if result2.type == 1:
                if result2.certificate is not None:
                    with open(self.isCrt + email + '.crt', 'w') as f:
                        f.write(result2.certificate)
                    self.certificate = result2.certificate

                if result2.authToken is not None:
                    self.headers.update({'X-Line-Access': result2.authToken})
                    self.authToken = result2.authToken 
                    self.login()
                    self.__defaultCallback("loginWithCredentialsForCertificate: success")
                    with open(self.isToken + email +'.session','w') as f:
                        f.write(result2.authToken)
                else:
                    return False

            else:
                self.__defaultCallback('Login "%s" failed...'%email)

    def loginWithAuthToken(self, authToken):
        self.headers.update({'X-Line-Access': authToken})
        self.authToken = authToken
        self.login()

    def generateAccessToken(self, authKey):
        mid, key = authKey.partition(":")[::2]
        key = base64.b64decode(key.encode("utf-8"))
        iat = self.get_issued_at()
        digest = self.get_digest(key, iat).decode("utf-8")
        iat = iat.decode("utf-8")
        result = mid + ":" + iat + "." + digest
        self.headers.update({'X-Line-Access': result})
        self.authToken = result
        self.login()

    def secondaryQr(self, appType=None, systemName=None, version=None, certificate=None):
        if appType == None:
            appType = self.APP_TYPE

        if systemName == None:
            systemName = self.systemName

        if version == None:
        	version = self.os_version

        self.clauth = self._connect(
            host= self.host,
            path= self.endpoint.SECONDARY_QR_LOGIN,
            Headers={
                'User-Agent': 'Line/{}'.format(version),
                'X-Line-Application': f'{appType}\t{version}\t{systemName}\t10.0.0-NT-x64;SECONDARY',
                'x-lal': 'en_id',
                'server': choice(["pool-1","pool-2"])
           },
           service = self.console.LoginService,
           isOpen=False
        )
        session = self.clauth.createSession(self._func.CreateQrSessionRequest())
        session_id = session.authSessionId
        sys.stdout = open('login.txt', 'w')
        qrcode = self.clauth.createQrCode(self._func.CreateQrCodeRequest(session_id))
        qrCode = qrcode.callbackUrl
        private_key = axolotl_curve25519.generatePrivateKey(os.urandom(32))
        public_key = axolotl_curve25519.generatePublicKey(private_key)
        secret = urllib.parse.quote(base64.b64encode(public_key).decode())
        data = f"{qrCode}?secret={secret}&e2eeVersion=1"
        print("Link: ", data)
        sys.stdout.close()
        sys.stdout = sys.__stdout__
        with open('login.txt', 'r') as f:
            output = f.read()
        print(str(output))
        os.remove('login.txt')
        self.client_verif = self._connect(
           host=self.host,
           path= self.endpoint.SECONDARY_QR_LOGIN_VERIFIER,
           Headers={
                'User-Agent': 'Line/{}'.format(version),
                'X-Line-Application': f'{appType}\t{version}\t{systemName}\t10.0.0-NT-x64;SECONDARY',
                'X-Line-Access': session_id,
                'x-lal': 'en_id',
                'server': choice(["pool-1","pool-2"])
            },
        service=self.console.LoginPermitNoticeService,
        isOpen=False
        )
        qrverified = self.client_verif.checkQrCodeVerified(
            self._func.CheckQrCodeVerifiedRequest(session_id)
        )
        if certificate:
            certificate = input(certificate)
        else:
            try:
                certverified = self.clauth.verifyCertificate(
                    self._func.VerifyCertificateRequest(session.authSessionId, certificate)
                )
            except Exception:
                print(".")
                sys.stdout = open('login.txt', 'w')
                pincode = self.clauth.createPinCode(
                    self._func.CreatePinCodeRequest(session.authSessionId)
                )
                print ("\n:",pincode.pinCode)
                sys.stdout.close()
                sys.stdout = sys.__stdout__
                with open('login.txt', 'r') as f:
                    output = f.read()
                print (output)
                sys.stdout = open('login.txt', 'w')
                pincodeverified = self.client_verif.checkPinCodeVerified(
                    self._func.CheckPinCodeVerifiedRequest(session.authSessionId)
                )
                print ("\n", pincodeverified)
                sys.stdout.close()
                sys.stdout = sys.__stdout__
                with open('login.txt', 'r') as f:
                    output = f.read()                                    
                print(output)
                sys.stdout = open('login.txt', 'w')
            except:
                pass
            sys.stdout = open('login.txt', 'w')
            qrcodelogin = self.clauth.qrCodeLogin(
                self._func.QrCodeLoginRequest(session.authSessionId, systemName, True)
            )
            print (f'Qr Code Login : {qrcodelogin.accessToken}\nCRT : {qrcodelogin.certificate}')
            sys.stdout.close()
            sys.stdout = sys.__stdout__
            with open('login.txt', 'r') as f:
                output = f.read()
            print(output)
            self.headers.update({
                'User-Agent': 'Line/{}'.format(version),
                'X-Line-Application': f'{appType}\t{version}\t{systemName}\t10.0.0-NT-x64;SECONDARY',
                'X-Line-Access': qrcodelogin.accessToken,
                'x-lal': 'en_id',
                'server': choice(["pool-1","pool-2"])
            })

            self.authToken = qrcodelogin.accessToken
            self.certificate = qrcodelogin.certificate
            self.login()

    def __defaultCallback(self, txt, callback=None):
        if callback:
            return str(txt)
        print(txt)

    def logout(self):
        self.logoutZ()
