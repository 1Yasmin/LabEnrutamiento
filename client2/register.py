import logging
from getpass import getpass
from argparse import ArgumentParser

import slixmpp
from slixmpp.exceptions import IqError, IqTimeout
import sys 
import os


class RegisterBot(slixmpp.ClientXMPP):


    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("register", self.register)

    def start(self, event):
        
        self.send_presence()
        self.get_roster()

        self.disconnect()

    async def register(self, iq):
        
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password

        try:
            await resp.send()
            logging.info("Account created for %s!" % self.boundjid)
            self.disconnect()
            os.system("python menu.py")
            sys.exit()
        except IqError as e:
            logging.error("Could not register account: %s" %
                    e.iq['error']['text'])
            self.disconnect()
            os.system("python menu.py")
            sys.exit()
        except IqTimeout:
            logging.error("No response from server.")
            self.disconnect()
            os.system("python menu.py")
            sys.exit()


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

    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel,
                        format='%(levelname)-8s %(message)s')

    if args.jid is None:
        args.jid = input("Username: ")
    if args.password is None:
        args.password = getpass("Password: ")

    xmpp = RegisterBot(args.jid, args.password)
    xmpp.register_plugin('xep_0030') 
    xmpp.register_plugin('xep_0004') 
    xmpp.register_plugin('xep_0066') 
    xmpp.register_plugin('xep_0077') 


    xmpp['xep_0077'].force_registration = True

    
    xmpp.connect()
    xmpp.process()
