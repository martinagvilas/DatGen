from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


def start_fpt_server(Username, Password):
    authorizer = DummyAuthorizer()
    authorizer.add_user(Username, Password, 'datasets', perm='lr')

    handler = FTPHandler

    handler.authorizer = authorizer
    handler.banner = "DatGen FTP server"

    handler.masquerade_address = '141.2.248.135'
    handler.passive_ports = range(60000, 65535)

    address = ('', 60333)
    server = FTPServer(address, handler)

    server.max_cons = 10
    server.max_cons_per_ip = 3

    server.serve_forever()


if __name__ == '__main__':
    start_fpt_server('xiaxu', '12345')
