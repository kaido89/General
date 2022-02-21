import requests

urls = ['http://test.com/']


# Ensure that the application accepts only a defined set of HTTP request methods, such as GET and POST are accepted,
# and unused methods (e.g. TRACE, PUT, DELETE) are explicitly blocked.
def HS1(name):
    method_list = ['POST', 'GET', 'PUT', 'DELETE', 'OPTIONS', 'TRACE', 'TEST']
    for url in urls:
        for method in method_list:
            req = requests.request(method, url)
            print(url, method, req.status_code, req.reason)


if __name__ == '__main__':
    HS1('PyCharm')
