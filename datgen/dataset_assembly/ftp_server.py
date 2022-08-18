from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


def start_fpt_server(Username, Password):
    authorizer = DummyAuthorizer()
    authorizer.add_user(Username, Password, '/Users/xuxia/projects/data', perm='lr')

    handler = FTPHandler

    handler.permit_foreign_addresses = True
    handler.permit_privileged_ports = True
    handler.authorizer = authorizer
    handler.banner = "DatGen FTP server"

    address = ('0.0.0.0', 2121)
    server = FTPServer(address, handler)

    server.max_cons = 10
    server.max_cons_per_ip = 3

    server.serve_forever()


if __name__ == '__main__':
    start_fpt_server('xiaxu', '12345')
