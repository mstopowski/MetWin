from urllib.request import urlopen
import ssl


class Request:

    @staticmethod
    def get_context_without_ssl():
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx

    @staticmethod
    def urlopen(url):
        raise NotImplementedError

    @staticmethod
    def urlopen_without_ssl(url):
        return urlopen(url, context=Request.get_context_without_ssl())


if __name__ == "__main__":
    req = Request('https://www.github.com/')
    print(req.read_without_ssl())