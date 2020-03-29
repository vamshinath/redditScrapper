import urllib.request
import ssl

def getFileSize(url):

    req = urllib.request.Request(
        url, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    gcontext = ssl.SSLContext()
    pre = urllib.request.urlopen(req,context=gcontext)
    sze = pre.info()["Content-Length"] 
    if sze == None:
        print("From sec")
        sz = pre.read().__len__()
    else:
        sz=int(sze)
    
    print(sz/1000)
    return sz



if __name__ == "__main__":
    getFileSize(input())
