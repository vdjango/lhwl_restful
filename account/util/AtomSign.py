from urllib.parse import quote
from lhwill.settings import HTTP_HOST, SECRET_KEY
from  account.util.MD5_SALE import MD5

import base64

URL = HTTP_HOST

def httpUrl(request, url, stype='lock'):
    username = request.user.username
    httpurls = ''
    print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
    if stype == 'lock':
        if username:
            httpurls += '?'
            httpurls += 'username'
            httpurls += '='
            httpurls += username

        return url, False
    if stype == 'unlock':
        dic = {}
        AtomS = {}
        auth = str(url).split('?')
        if len(auth) > 1:
            for i in str(auth[1]).split('&'):
                kv = str(i).split('=')
                if len(kv) > 1:
                    k = kv[0]
                    v = kv[1]
                    if v:
                        if k == 'atom' or k == 'sign':
                            AtomS[k] = v
                        else:
                            dic[k] = v

        httpurls += '?'
        for d in dic:
            httpurls += d
            httpurls += '='
            httpurls += dic[d]
            httpurls += '&'

        return httpurls, AtomS

def sortedDictKey(dict):
    return sorted(dict.items(), key=lambda e:e[1])

def sign(sign, salt=None):
    sign = quote(sign)
    md = MD5(sign.encode("utf-8"), salt=salt)
    salts = md.get_salt()
    print('MOD',salts)
    return md.md5, salts

def Autom(sig, salt=None):
    httpurls = sig
    sig_key = "{}{}".format(
        SECRET_KEY,
        URL
    )
    bytesString = sig_key.encode(encoding="utf-8")
    encodestr = base64.b64encode(bytesString)
    # 解码
    # decodestr = base64.b64decode(encodestr)
    print('encodestr', encodestr)

    sig, salt = sign(encodestr, salt=salt)
    atom = str(encodestr.decode())
    http = httpurls
    http += 'atom='
    http += atom
    http += '&'
    http += "sign="
    http += sig
    return http, {
        'atom': atom,
        'sign': sig,
        'salt': salt,
    }

def AtomSig(request, url, stype='lock', salt=None):
    dic = {}

    httpurls, Atomsign = httpUrl(request, url, stype)
    httpurls = str(httpurls).split('?')

    urlhttp = httpurls[1]

    if urlhttp:
        for list in urlhttp.split('&'):
            print('url', list.split('='))
            kv = list.split('=')
            if len(kv) > 1:
                key = kv[0]
                value = kv[1]
                if value and key != 'sign' and key != 'atom':
                    dic[key] = value

    dic = dict(sortedDictKey(dic))
    print('Url', dic)
    sig = ''

    for key, value in dic.items():
        sig +=  key
        sig += '='
        sig += dic[key]
        sig += '&'

    sig = httpurls[0] + '?' + sig
    auto, dicAtomSign = Autom(sig, salt=salt)
    salt = dicAtomSign['salt']
    if Atomsign and dicAtomSign:
        print('验证Sign地址[未加密]', Atomsign['sign'])
        print('验证Atom地址[未加密]', Atomsign['atom'])

        print('验证Sign地址[以加密]', dicAtomSign['sign'])
        print('验证Atom地址[以加密]', dicAtomSign['atom'])

        if Atomsign['atom'] == dicAtomSign['atom'] and Atomsign['sign'] == dicAtomSign['sign']:
            print('Atom AtomSign True')
            return True, salt

        return False, salt

    else:

        print('Url', sig)
        print('Atom', auto)
        return auto, salt

if __name__ == '__main__':
    AtomSig('http://api.lhwill.com/?user=job&date=20180312114600')



'''
http://api.lhwill.com/?date=20180312114600&user=job&atom=aHR0cDovL2FwaS5saHdpbGwuY29tLz9kYXRlPTIwMTgwMzEyMTE0NjAwJnVzZXI9am9iJg==&sign=36468d9e9717fdf0f504f74c985e345f
'''