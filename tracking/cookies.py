# encoding=utf-8
import json
import base64
import requests

myWeiBo = [
  # -------------------------------------- These accounts have been frozen
  #    R I P
  #    {'no': '15065033488', 'psw': 'a12345'},  # F
  #    {'no': '18039066824', 'psw': 'a12345'},  # F
  #    {'no': '18240493241', 'psw': 'a12345'},  # F
  #    {'no': '13731141938', 'psw': 'a12345'},  # F
  #    {'no': '14792351794', 'psw': 'a12345'},  # F
  #    {'no': '13155964852', 'psw': 'a12345'},  # F

  #    {'no': '18753085435', 'psw': 'a123456'},  # F
  #    {'no': '15130149020', 'psw': 'a123456'},  # F
  #    {'no': '13240572932', 'psw': 'a123456'},  # F
  #    {'no': '13731141695', 'psw': 'a123456'},  # F
  #    {'no': '13197944945', 'psw': 'a123456'},  # F
  #    {'no': '18002628575', 'psw': 'a123456'},  # F

  #    {'no': '13415281914', 'psw': 'a123456'},  # F
  #    {'no': '13425209920', 'psw': 'a123456'},  # F
  #    {'no': '13425221294', 'psw': 'a123456'},  # F
  #    {'no': '15915101221', 'psw': 'a123456'},  # F
  #    {'no': '15917507411', 'psw': 'a123456'},  # F
  #    {'no': '13062578486', 'psw': 'a123456'},  # F
  # ----------------------------------------------------------------------------

  #    {'no': '15876355221', 'psw': 'a123456'},
  #    {'no': '13633185498', 'psw': 'a123456'},
  #    {'no': '13784857442', 'psw': 'a123456'},
  #    {'no': '13582485493', 'psw': 'a123456'},  # F
  #    {'no': '13610533533', 'psw': 'a123456'},
  #{'no': '15236647604', 'psw': 'a123456'},

]


def getCookies(weibo):
  """ 获取Cookies """
  cookies = []
  loginURL = r'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'
  for elem in weibo:
    account = elem['no']
    password = elem['psw']
    username = base64.b64encode(account.encode('utf-8')).decode('utf-8')
    postData = {
      "entry": "sso",
      "gateway": "1",
      "from": "null",
      "savestate": "30",
      "useticket": "0",
      "pagerefer": "",
      "vsnf": "1",
      "su": username,
      "service": "sso",
      "sp": password,
      "sr": "1440*900",
      "encoding": "UTF-8",
      "cdult": "3",
      "domain": "sina.com.cn",
      "prelt": "0",
      "returntype": "TEXT",
    }
    session = requests.Session()
    r = session.post(loginURL, data=postData)
    jsonStr = r.content.decode('gbk')
    info = json.loads(jsonStr)
    if info["retcode"] == "0":
      print "Get Cookie Success!( Account:%s )" % account
      cookie = session.cookies.get_dict()
      cookies.append(cookie)
    else:
      print "Failed!( Reason:%s )" % info['reason']
  return cookies


cookies = getCookies(myWeiBo)
print "Get Cookies Finish!( Num:%d)" % len(cookies)

neteaseCookie = {
    "mail_psc_fingerprint": "fd710b4a1b2eaa49b73820e579d73779",
    "_ntes_nnid": "7a647246abb0849782a6ca83088405cb,1492647008535",
    "_ntes_nuid": "7a647246abb0849782a6ca83088405cb",
    "NTES_SESS": "egDXAqt_F5VtQQWObWIpTKiHW_ec5zgb0R30llZvi7Di4eB3c4CByOazTlHDmIYR6BhV2OKIDEjfQR0PbWzmrQRPADPCgvEuf4dyXyrLcyz3IYx5SzQergyVa2sGIFGdmJVtztDekUi_dFGfdAifuInG4",
    "S_INFO": "1492736894|0|3&20##|hhc_digitop",
    "P_INFO": "hhc_digitop@163.com|1492736894|0|other|00&99|bej&1492687805&other#bej&null#10#0#0|&0||hhc_digitop@163.com",
    "ANTICSRF": "910848bf3a86f461a6b10907d1df6c4b",
    "vjuids": "-17d2b2ab7.15b8e103532.0.9424c0a0f9ecb",
    "vjlast": "1492737079.1492737079.30",
    "ne_analysis_trace_id": "1492737078584",
    "NTES_CMT_USER_INFO": "104578209%%7Chhc_digitop%%7C%%7Cfalse%%7CaGhjX2RpZ2l0b3BAMTYzLmNvbQ%%3D%%3D",
    "vinfo_n_f_l_n3": "439826a284be8d23.1.0.1492737078586.0.1492737277660",
    "s_n_f_l_n3": "439826a284be8d231492737078587",
    "NTESsubscribeSI": "41B4D9968615F517726920D5D58D2C57.bjyz-subscribe-tomcat5.server.163.org-8010"
}

ucCokkie = {
  "_uab_collina": "149369546177268526950894",
  "_umdata": "BA335E4DD2FD504F613A74E4D288D1CB0A211F19EE8B400B10288780BE443CC819473358249CECE1CD43AD3E795C914C5CBF1AC6D3D42A48AAF7C3523FA40547",
  "_UP_A4A_11_": "wb6a913e22a347929e8d944a57c953a0",
  "_UP_L_": "zh",
  "_UP_F7E_8D_": "4K7SM3le0hDugCm2n2QRGxzy6ZfcuPaCcCX5PS4jd7ZM7G5rLtmiOSwgG3mCnckgEUez5D%2BmyE8HjaM3L9JAQJQdokMYch13ywfi%2FNw59JSA4d%2BoZ0XH5Vv0CWFeDTU7nwophJ50y3ImBd9PCi%2BgRy2z3qDnYStBfuAlccHfgOZMnJVud4XLkzptKiV3q7grvvIk%2BqxjztacjvzgM6Em62cn6E41EnNxiFOhXbv3dSSCJwsZdYNQtLNWMS8ybOdpVnaCJNfZ71n8rT%2FNXCSsX79Rn8AU60dG0vwRrfdXxoWTMMmbzim1P%2FGZG4Kxr5sMas4r5bs16kB65h1MGsfX1ZXMxBnUatpyhAF3Rgn4OBc%3D",
  "_UP_D_": "pc",
  "USER_TMP": '''yVutR4nouHmm04suzTAG5g.pSvzEDN2b0zq95OnxNJdoH5OuZMWQ3VSkaLxj-zLyQCffNfCgGzqQfWLug1ZCxBFBFd2onca48bOsHyjmXcsgDPQjrkjUhbTjewH37ZnxTq7zZ0tWerCpY0PMJODUd96qFSTZA_bwuar_02yWFqd2Hur3FoKNFObo4eKKRak-dMUsDKv4iTZTKGflMvAiB_gm1z94H4TyLM3yuyShSkEEItJfkHkEgH5pZcynYwnTsmiM-nljGzEgO_PHqSIRaOVCXSrPKWR68vkyyZ6TOq2J9ELKIfoe9maMflUlHCNr5L6Onvi2GzOfcC40BKJR7ZbONih9kmaym6fqGckyoKSPaKi-rxhDkU1i_O5ibAxB_jlkEvd2Pg_wZyY_WVWIN3mt-mg41wlieQuzR3q2AhWGsy5GZUKjksTka6fl_9tZfWiPN8BM6Cr5ttkg8t98uPqn81uYFRcr2-S-UwytxC4ImfX7xTjsHQSc5sZQZrxNlSivkI1d13iPrhfxmSRRe-oUKrTLZeP2zEWmj1W9zwWKhxG-MJW-lk_SqykMTmi2nDUzo9JdekPFiNyurf_EOUas-Il1lYxSa6iPaH3d3hJmooNohxllwwQN78aM4mZVXEKYP9XdacArdm3fVCnZFzETKODhXg3s5-oswIzGXSTjwBjQVoE3sUw1xARf8OeJ0Io0MRqcr0UauTb9tE0B2VjE5QPOmM-2et-7dVVjbM3_K2rq8P9rJQH8PIYVSBtH3C2porQJLOZVwyy9bclnBbeQG5hbJEy2l3jWCAhFeDcU2MrbA1Xrt5ui7KYVZxiBj7W6Mbk0ViZdMdWIeA9HZsrLRgGduaA6QUse1aqIXUy1kDR6TMj6q00EKxgA-rW5i6acGLj--b9itdjz_lug2fS8Al9bEqaQtVfCx_oX2xqxivL7juZiDew6bEzV4hbehsz4bK11DTjM5NydWec0bfW-xArnKC-esb3lFmy03PyZbqPEKQ_NGFsZJDVbsjqxRzKObq1v6eIy1uT-lEqGnKoOYefb04ardaxKol_bjzJvwj5MPjLa3DtXXhYrROO0wouBvBJOJzOxvp-LTi8OsqdW8pp-AGx_90Afg61CKwIWLtokfKPk4b2-_mkOKyCaqpiUfr4-xPu-EwUpILj16iEmsnadPQ36F40_CEwuu4S0_w0P6QhCshsbTY_49AWSZu7Eagt6xS6NN1ELmITSa5z4X1-kaq9KeP2SJmlhyRKFtxd-DPIL9S7ITSkAlk_dU_w393Cl7pfpaO2Dc2w42kosDN2amF0ob1r7JkxK43W9bMwk352CA2-E9b0EcaLhwCBVCP1v_GB-79uJor-y5Ad.1493876584051.86400000.QMx360PR8Mj8WFA941rt9F84vvVSxK6rFdW0-5WbVhw'''
}

toutiaoCookie = {
  "uuid": "w:02e1ddba97ab4e128afe21149639286f",
  "UM_distinctid": "15b40e627a0141-0b34984dc49205-317f0158-100200-15b40e627a12fa",
  "_ba": "BA0.2-20170419-5110e-mMqBkjCsuhauGAZ5QDr2",
  "sso_login_status":"1",
  "login_flag": "1c909e9112eb4c2dd9d375c7331797ad",
  "sid_tt": "5608ec1446b4a66165c34913a35234f0",
  "sid_guard": "5608ec1446b4a66165c34913a35234f0|1492587134|2591999|Fri\054 19-May-2017 07:32:13 GMT",
  "__utma": "24953151.284395669.1481011893.1488958540.1492593396.2",
  "__utmz": "24953151.1488958540.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
  "sessionid": "5608ec1446b4a66165c34913a35234f0",
  "TT_WEB_ID": "972990860071525",
  "tt_im_token": "1493988835061496814929163287459015998573922799956747200932708949",
  "_ga": "GA1.2.284395669.1481011893",
  "_gid": "GA1.2.1285755496.1493988898",
  "currentMediaId": "6009321998",
  "tt_webid": "39546414783",
  "_ga": "GA1.3.284395669.1481011893",
  "_gid": "GA1.3.1768581131.1493990184"
}
