# coding=utf-8
import re
import traceback
import requests
import time
import multiprocessing


class FckScanner:

    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
        'Accept-Language': 'en-us',
        'Accept-Encoding': 'identity',
        'Keep-Alive': '300',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        }

    fckdir = [
        "FCKeditor2.3/",
        "/server/fckeditor/editor/fckdebug.html",
        "mambots/editors/fckeditor",
        "FCKeditor2/",
        "admin/fckeditor/editor/filemanager/upload/php/upload.php",
        "/FCKeditor/editor/dialog/",
        "admin/fckeditor/editor/filemanager/upload/asp/upload.asp",
        "includes/fckeditor/editor/filemanager/upload/asp/upload.asp",
        "includes/fckeditor/editor/filemanager/upload/php/upload.php",
        "FCKeditor21/",
        "includes/fckeditor/editor/filemanager/connectors/aspx/connector.aspx",
        "manage/fckeditor",
        "FCKeditor2.2/",
        "fckeditor/editor/filemanager/browser/default/connectors/php/connector.php",
        "/manage/fckeditor",
        "admin/fckeditor/editor/filemanager/connectors/aspx/upload.aspx",
        "admin/fckeditor/editor/filemanager/connectors/asp/connector.asp",
        "/html/editor/fckeditor/editor/filemanager",
        "fckeditor/editor/filemanager/connectors/asp/connector.asp",
        "fckeditor/editor/filemanager/browser/default/connectors/asp/connector.asp",
        "includes/fckeditor/editor/filemanager/connectors/asp/upload.asp",
        "assets/fckeditor",
        "fckeditor/editor/filemanager/upload/aspx/upload.aspx",
        "/web/FCKeditor/editor/filemanage",
        "inc/fckeditor/",
        "fckeditor/editor/filemanager/connectors/asp/upload.asp",
        "/admin/FCKeditor/editor/filemanage",
        "/browser/trunk/fckeditor/editor/filemanager/",
        "FCKeditor22/",
        "/scripts/fckeditor/editor/filemanager/",
        "admin/fckeditor/editor/filemanager/connectors/asp/upload.asp",
        "inc/fckeditor",
        "includes/fckeditor/editor/filemanager/connectors/php/connector.php",
        "/system/Fckeditor",
        "admin/FCKeditor",
        "editors/FCKeditor",
        "fckeditor",
        "javascript/editors/fckeditor",
        "include/fckeditor",
        "FCKeditor/editor/filemanager/browser/default/connectors/php/connector.php",
        "/boke/Edit_Plus/FCKeditor/editor/",
        "/js/editor/fckeditor/editor/filemanager",
        "FCKeditor23/",
        "plugins/fckeditor",
        "includes/fckeditor/editor/filemanager/browser/default/connectors/aspx/connector.aspx",
        "resources/fckeditor",
        "/tools/fckeditor/editor/filemanager",
        "FCKeditor20/",
        "/includes/fckeditor/editor/filemanager",
        "/html/js/editor/fckeditor/editor/filemanager",
        "fckeditor/editor/filemanager/connectors/aspx/upload.aspx",
        "FCKeditor2.4/",
        "/admin/fckeditor",
        "/machblog/browser/trunk/fckeditor/editor/filemanager/",
        "fckeditor/editor/filemanager/connectors/aspx/connector.aspx",
        "FCKeditor",
        "admin/fckeditor/editor/filemanager/upload/aspx/upload.aspx",
        "admin/fckeditor/editor/filemanager/browser/default/connectors/asp/connector.asp",
        "/results/fckeditor/editor/filemanage",
        "/editor/FCKeditor/editor/filemanager",
        "/fckEditor/editor/",
        "editor/FCKeditor",
        "/ocomon/includes/fckeditor/editor/filemanager",
        "sites/all/modules/fckeditor",
        "FCKeditor24/",
        "fckeditor/editor/filemanager/upload/asp/upload.asp",
        "/demo/fckeditor/editor/filemanager",
        "/web_Fckeditor",
        "sites/all/libraries/fckeditor",
        "includes/fckeditor/editor/filemanager/connectors/php/upload.php",
        "/FCKeditor/editor/filemanage",
        "/apps/trac/pragyan/browser/trunk/cms/modules/article/fckEditor/editor/filemanage",
        "gs/plugins/editors/fckeditor",
        "include/fckeditor/",
        "adm/fckeditor",
        "thirdparty/fckeditor",
        "includes/fckeditor/editor/filemanager/connectors/aspx/upload.aspx",
        "admin/fckeditor/editor/filemanager/connectors/aspx/connector.aspx",
        "/common/FckEditor/editor/filemanager",
        "includes/fckeditor/editor/filemanager/connectors/asp/connector.asp",
        "fckeditor/editor/filemanager/connectors/php/connector.php",
        "lib/fckeditor",
        "blog/fckeditor",
        "CFIDE/scripts/ajax/FCKeditor",
        "/ispcp/browser/trunk/gui/tools/filemanager/plugins/fckeditor/editor/filemanager",
        "/demo/admin/fckeditor/editor/filemanager",
        "admin/fckeditor/editor/filemanager/connectors/php/upload.php",
        "fckeditor/editor/filemanager/browser/default/connectors/aspx/connector.aspx",
        "includes/fckeditor/editor/filemanager/upload/aspx/upload.aspx",
        "assets/js/fckeditor",
        "fckeditor/editor/filemanager/upload/php/upload.php",
        "FCKeditor2.1/",
        "js/FCKeditor",
        "admin/scripts/fckeditor",
        "admin/fckeditor/editor/filemanager/browser/default/connectors/php/connector.php",
        "FCKeditor/",
        "fckeditor/editor/filemanager/connectors/php/upload.php",
        "/INC/FckEditor/editor/filemanager",
        "fck",
        "includes/fckeditor/editor/filemanager/browser/default/connectors/php/connector.php",
        "lib/fckeditor/",
        "/common/INC/FckEditor/editor/filemanager",
        "plugins/editors/fckeditor",
        "/includes/fckeditor",
        "admin/fckeditor/editor/filemanager/browser/default/connectors/aspx/connector.aspx",
        "includes/fckeditor/editor/filemanager/browser/default/connectors/asp/connector.asp",
        "admin/fckeditor/editor/filemanager/connectors/php/connector.php",
        "FCKeditor2.0/",
        "/ThirdPartyControl/fckeditor/editor/filemanage"
    ]

    def __init__(self,domain):
        self.domain =domain
        self.header_server = None
        self.timeout = 15
        self.useragent = [] #   几十个 随机
        self.result = []
        #   启动扫描程序
        self.run()

    def geturl(self,fckurl):
        try:
            url = self.domain+fckurl
            response = requests.get(url=url, timeout=self.timeout,allow_redirects=True)
            status_code = response.status_code
            htmldoc = response.text
            self.header_server = response.headers['Server']

            if status_code in [200,300,202]:
                if "404" not in htmldoc:
                    self.result.append(url)
                    print url
        except requests.ConnectionError:
            pass

        except requests.exceptions.ReadTimeout:
            pass
            print "[-]\tRead Timeout in {}".format(url)

        except KeyError:
            pass

        except:
            print traceback.print_exc()
            pass

    def run(self):
        print "[+]  Now Scan {}".format(self.domain)
        for fckurl in self.fckdir:
            self.geturl(fckurl)
        if len(self.result) != 0 and len(self.result) <20:
            with open("result.txt",'a') as f:
                f.write("{0}\t{1}\n".format(self.domain,self.header_server))
                for r in self.result:
                    f.write("\t\t|----{}\n".format(r))
                f.write("\n\n")


def ScanThread():
    """
    使用多进程跑，每次开100条进程，同时扫描100个网站
    :return:
    """
    processnum = 50
    domains = []
    with open('domain.txt','r') as f:
            for line in f.readlines():
                domains.append(line.strip())

    try:
        pool = multiprocessing.Pool(processes=processnum)
        pool.map_async(FckScanner,domains)
        pool.close()
        pool.join()

    except:
        print traceback.print_exc()


if __name__ == '__main__':
    # FckScanner("http://daintyhome.com.tr/")
    FckScanner("http://longtuyen.vn/")
    # ScanThread()
