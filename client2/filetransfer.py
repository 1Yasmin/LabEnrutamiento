import logging
from getpass import getpass
from argparse import ArgumentParser

import slixmpp
from slixmpp.exceptions import IqError, IqTimeout

#se ingresa el usuario y contrasena se determina a quien se le va a enviar y el archivo 
class S5BSender(slixmpp.ClientXMPP):
    def __init__(self, jid, password, receiver, filename):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.receiver = receiver
        #se abren archivos con rb
        self.file = open(filename, 'rb')
        self.add_event_handler("session_start", self.start)
        #self.send_message(mto=self.receiver ,mbody=filename,mtype='chat')
        #es necesario llamar al plugin xep_0065 y se realiza un handshake . luego de esto se lee el data y es enviado al usuario
    async def start(self, event):
        try:
            proxy = await self['xep_0065'].handshake(self.receiver)
            while True:
                data = self.file.read(1048576)
                if not data:
                    break
                await proxy.write(data)
                print("archivo enviado")
                self.send_message(mto=self.receiver,
                          mbody=self.filename,
                          mtype='chat')

            proxy.transport.write_eof()
        finally:
            self.file.close()
            self.disconnect()
        

if __name__ == '__main__':
 
    parser = ArgumentParser()

   
    parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                        action="store_const", dest="loglevel",
                        const=logging.ERROR, default=logging.INFO)
    parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                        action="store_const", dest="loglevel",
                        const=logging.DEBUG, default=logging.INFO)

 
    parser.add_argument("-j", "--jid", dest="jid",
                        help="JID to use")
    parser.add_argument("-p", "--password", dest="password",
                        help="password to use")
    parser.add_argument("-r", "--receiver", dest="receiver",
                        help="JID of the receiver")
    parser.add_argument("-f", "--file", dest="filename",
                        help="file to send")
    parser.add_argument("-m", "--use-messages", action="store_true",
                        help="use messages instead of iqs for file transfer")

    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel,
                        format='%(levelname)-8s %(message)s')

    if args.jid is None:
        args.jid = input("Usuario: ")
    if args.password is None:
        args.password = getpass("Password: ")
    if args.receiver is None:
        args.receiver = input("Enviar a: ")
    if args.filename is None:
        args.filename = input("File path: ")

    xmpp = S5BSender(args.jid, args.password, args.receiver, args.filename)
    xmpp.register_plugin('xep_0030')
    xmpp.register_plugin('xep_0065')

    xmpp.connect()
    xmpp.process(forever=False)