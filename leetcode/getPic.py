getPageUrl = """https://view45.book118.com/PW/GetPage?f=dXAyNS0yLmJvb2sxMTguY29t
LjgwXDI0MTc4NDgtNWE0MGMzNDMyMDA2Mi5wZGY=&img={}&isMobile=false&readLimit=AzAQPtkxN27gR
DAC95u8sw==&sn={}&furl=o4j9ZG7fK97qcILiPIEolIOcrDfnjM6NDRXI@btfn9i3xWChDysRMtgw1J
Z69rFAlvyVLY4OUPZV3HHah5kst5GgUQ8QQBR7F4aJ8JmVzq3AWTDQwovzPw=="""

index = '7o@o7xcocmksMfXel0@FxPkQCEJgkk1OGWehMvivf6GnlihqLr65ifAB0wfnX0xoKzlRttzJdr4='
imgURL = 'https://view45.book118.com/img?img={}&tp='

import requests
import json

sn = 1
# i = 1
headers = {
    "Cookie": "CLIENT_SYS_UN_ID=wKh2GVxvVocTCB6EOTM9Ag==; Hm_lvt_5d91dc9c92e499ab00ba867fc2294136=1550800524,1550800630,1550800810,1550801441; Hm_lpvt_5d91dc9c92e499ab00ba867fc2294136=1550801441",
    "Host": "view45.book118.com",
    "If-Modified-Since": "Wed, 20 Feb 2019 05:06:26 GMT",
    "Upgrade-Insecure-Requests": '1',
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"}


def getPic():
    global index, sn
    resp = requests.get(getPageUrl.format(index, sn), headers=headers)
    print(getPageUrl.format(index, sn))
    resp = json.loads(resp.content)
    print(imgURL.format(index))
    fileName = './imgs/{}.png'.format(sn)
    img = requests.get(imgURL.format(index), headers=headers)

    with open(fileName, 'wb') as f:
        f.write(img.content)
        # i += 1
    sn += 1
    index = resp.get('NextPage')
    if not index:
        return
    getPic()


getPic()
