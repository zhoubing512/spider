# encoding=utf-8
import random
import string
import urllib2
import json
import logging
from user_agents import agents
from proxies import ProxyScanner
from cookies import cookies, neteaseCookie, ucCokkie, toutiaoCookie

ps = ProxyScanner()

def BID():
  return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(11))

class UserAgentMiddleware(object):
  def process_request(self, request, spider):
    agent = random.choice(agents)
    request.headers["User-Agent"] = agent

class UserAgentSpiderMiddleware(object):
  def process_request(self, request, spider):
    request.headers["User-Agent"] = "Googlebot"

class CookiesMiddleware(object):
  def process_request(self, request, spider):
    cookie = {
      "qv_swfrfu":"http://www.buuoo.com/wp-content/plugins/ck-video/includes/direct.php",
      "tvfe_boss_uuid":"202da144f307abc1",
      "mobileUV":"1_1582320062e_174ea",
      "pgv_info":"ssid",
      "pgv_pvid":"2760462218",
      "o_cookie":"10185841"
    }
    request.cookies = cookie


class WeiboCookiesMiddleware(object):
  """ 测试阶段用的Cookie """

  def process_request(self, request, spider):
    cookie = random.choice(cookies)
    request.cookies = cookie

class NeteaseTrackingCookieMiddleware(object):
    """ 换Cookie """
    def process_request(self, request, spider):
      request.cookies = neteaseCookie

class UcFansCookieMiddleware(object):
    """ 换Cookie """
    def process_request(self, request, spider):
      request.cookies = ucCokkie

class ToutiaoTrackingCookieMiddleware(object):
    """ 换Cookie """
    def process_request(self, request, spider):
      request.cookies = toutiaoCookie

class WeiboCookiesDemoMiddleware(object):
    """ 换Cookie """
    def process_request(self, request, spider):
      cookie = {
        "YF-V5-G0": "55fccf7be1706b6814a78384fa94e30c",
        "login_sid_t": "4b4f8be18101907fbaf475e1b7ee5a62",
        "YF-Ugrow-G0": "5b31332af1361e117ff29bb32e4d8439",
        "_s_tentry": "-",
        "Apache": "4347483695861.9824.1491456463962",
        "SINAGLOBAL": "4347483695861.9824.1491456463962",
        "ULV": "1491456464971:1:1:1:4347483695861.9824.1491456463962:",
        "YF-Page-G0": "0acee381afd48776ab7a56bd67c2e7ac",
        "TC-V5-G0": "5fc1edb622413480f88ccd36a41ee587",
        "TC-Page-G0": "e2379342ceb6c9c8726a496a5565689e",
        "TC-Ugrow-G0": "968b70b7bcdc28ac97c8130dd353b55e",
        "wb_publish_fist100_5976703500": "1",
        "WBtopGlobal_register_version": "a05309c5d15974a8",
        "WBStorage": "02e13baf68409715|undefined",
        "UOR": ",,login.sina.com.cn",
        "SCF": "Al_DLgDhuLvxXIQEN55aoxZUbALSL363McMveA_5chk1eKHPREyt0FLY270Ja4wd5qJ_PlwDyPNNb_bw2nsfocM.",
        "SUB": "_2A250FVdKDeRhGeNH7FQW8C3JyzyIHXVXY8-CrDV8PUNbmtANLWvNkW9yuxHeSxYxNF3ZmLplrYs_Pn00Cg..",
        "SUBP": "0033WrSXqPxfM725Ws9jqgMF55529P9D9WFvUIVCE_xq0wc1-g_VPoKM5JpX5K2hUgL.Fo-4S0qNehefeh52dJLoIEBLxK.L1-BLBoeLxK-L12qLBo5LxKML1h2L12eLxK.L1-BLBoet",
        "SUHB": "0TPlr_6xMl8wDX",
        "ALF": "1525832346",
        "SSOLoginState": "1494296346",
        "un": "13633185498",
        "wvr": "6"
      }
      request.cookies = cookie


class WeiboCookiesHotSearchMiddleware(object):
  """ 换Cookie """

  def process_request(self, request, spider):
    cookie = {
      "login_sid_t": "4b4f8be18101907fbaf475e1b7ee5a62",
      "_s_tentry": "-",
      "Apache": "4347483695861.9824.1491456463962",
      "SINAGLOBAL": "4347483695861.9824.1491456463962",
      "ULV": "1491456464971:1:1:1:4347483695861.9824.1491456463962:",
      "SWB": "usrmdinst_20",
      "SSOLoginState": "1492067367",
      "NSC_wjq_txfjcp_mjotij": "ffffffff094113d545525d5f4f58455e445a4a423660",
      "UOR": ",,login.sina.com.cn",
      "SCF": "Al_DLgDhuLvxXIQEN55aoxZUbALSL363McMveA_5chk1lKH2OKEclKWkpULGbP_8fVUkZQa6eqXkp6ZXxX51coE.",
      "SUHB": "04We8SJgw4gAan",
      "ALF": "1523886429",
      "un": "13633185498"
    }
    request.cookies = cookie

class QqCookiesMiddleware(object):
  def process_request(self, request, spider):
    cookie = {
      "tvfe_boss_uuid": "c7582d8855744c96",
      "pgv_pvi": "5612879872",
      "pgv_si": "s9943817216",
      "ptui_loginuin": "10407622",
      "pt2gguin": "o0010407622",
      "uin": "o0010407622",
      "ptisp": "ctc",
      "RK": "lGvemK+7U6",
      "ptcz": "fa6e90cb44858c46a66dd1eb495683141da2f347796e659cefaeabe626bfd063",
      "o_cookie": "10407622",
      "pgv_info": "ssid=s1547281784",
      "pgv_pvid": "1894147597",
      "OM_EMAIL": "taste_well@qq.com",
      "fname": "%E5%A5%BD%E5%A5%BD%E5%90%83",
      "fimgurl": "http%3A%2F%2Finews.gtimg.com%2Fnewsapp_ls%2F0%2F1285328993_200200%2F0",
      "userid": "5436116",
      "TSID": "lg6dtpg57nl6d3j1g71ibodd46",
      "9e67236d07bdc7152e6e2b42b7f00f43": "7b3072674977ce18efd4f9361c6378e836be3f64a%253A4%253A%257Bi%253A0%253Bs%253A7%253A%25225436116%2522%253Bi%253A1%253Bs%253A17%253A%2522taste_well%2540qq.com%2522%253Bi%253A2%253Bi%253A43200%253Bi%253A3%253Ba%253A11%253A%257Bs%253A6%253A%2522status%2522%253Bs%253A1%253A%25222%2522%253Bs%253A5%253A%2522email%2522%253Bs%253A17%253A%2522taste_well%2540qq.com%2522%253Bs%253A6%253A%2522imgurl%2522%253Bs%253A55%253A%2522http%253A%252F%252Finews.gtimg.com%252Fnewsapp_ls%252F0%252F1285328993_200200%252F0%2522%253Bs%253A3%253A%2522uin%2522%253Bs%253A0%253A%2522%2522%253Bs%253A4%253A%2522name%2522%253Bs%253A9%253A%2522%25E5%25A5%25BD%25E5%25A5%25BD%25E5%2590%2583%2522%253Bs%253A10%253A%2522isVerified%2522%253Bb%253A1%253Bs%253A10%253A%2522isRejected%2522%253Bb%253A0%253Bs%253A26%253A%2522agreementAcceptingRequired%2522%253Bb%253A0%253Bs%253A29%253A%2522initialPasswordChangeRequired%2522%253Bb%253A0%253Bs%253A27%253A%2522initialAvatarChangeRequired%2522%253Bb%253A0%253Bs%253A2%253A%2522id%2522%253Bs%253A7%253A%25225436116%2522%253B%257D%257D",
      "omtoken": "3d1551670b",
      "omtoken_expire": "1493303259",
      "rmod": "1"
    }
    request.cookies = cookie

class ProxyMiddleware(object):
  def process_request(self, request, spider):
    ps.check_and_get_proxies_json(ps.xun_target_url,'xun_proxy')
    proxies = ps.proxies
    if len(proxies)<1:
        ps.check_and_get_proxies_json(ps.free_target_url)
        proxies = ps.proxies

    if len(proxies) > 0:
        proxy = random.choice(proxies)
        #request.headers["proxy"] = proxy
        request.meta["proxy"] = proxy
