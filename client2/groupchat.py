import logging
from getpass import getpass
from argparse import ArgumentParser
import slixmpp
import sys 
import os
class GroupChat(slixmpp.ClientXMPP):

    def __init__(self, jid, password, room, nick):
        #se determina el cuarto, el nick que es el nombre dentro del chat y se inicia el mensaje de presencia con muc 
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.room = room
        self.nick = nick
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("groupchat_message", self.muc_message)
        self.add_event_handler("muc::%s::got_online" % self.room,self.muc_online)
        self.add_event_handler("message", self.message)
        #se inicia plugin xep_0045 en donde se realiza un join_much osea al grupo
    def start(self, event):
        self.get_roster()
        self.send_presence()
        self.plugin['xep_0045'].join_muc(self.room,self.nick,wait=True)
        self.send_presence()
        self.get_roster()
       
        #basado en el ejemplo de slixmpp
    def muc_message(self, msg):
        if msg['mucnick'] != self.nick and self.nick in msg['body']:
            self.send_message(mto=msg['from'].bare,
                              mbody="I heard that, %s." % msg['mucnick'],
                              mtype='groupchat')
    #se ingresa la opcion para enviar mensajes cuando sienta la presencia de alguien 
    def muc_online(self, presence):
        if presence['muc']['nick'] != self.nick:
            nuevomensaje = input("Ingresa un mensaje >>")
            self.send_message(mto=presence['from'].bare,mbody= nuevomensaje,mtype='groupchat')
            if (nuevomensaje == "exit"):
                os.system("python menu.py")
                sys.exit()
        else:
            nuevomensaje = input("Ingresa un mensaje >>")
            self.send_message(mto=presence['from'].bare,mbody= nuevomensaje,mtype='groupchat')
            if (nuevomensaje == "exit"):
                os.system("python menu.py")
                sys.exit()
#se ingresa la opcion para recibir mensajes

    def message(self, msg):
        if msg['type'] in ('groupchat', 'normal'):
            print(msg)
            print("Mensaje recibido:\n%(body)s" % msg)
            nuevomensaje = input("envia un mensaje:")
            msg.reply(nuevomensaje).send()
            print("Enviaste un nuevo mensaje:", nuevomensaje)
            if (nuevomensaje == "exit"):
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

    parser.add_argument("-r", "--room", dest="room",

                        help="MUC room to join")

    parser.add_argument("-n", "--nick", dest="nick",

                        help="MUC nickname")

    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel,

                        format='%(levelname)-8s %(message)s')

    if args.jid is None:

        args.jid = input("Username: ")

    if args.password is None:

        args.password = getpass("Password: ")

    if args.room is None:

        args.room = input("Group Chat room: ")

    if args.nick is None:

        args.nick = input("Apodo: ")


    xmpp = GroupChat(args.jid, args.password, args.room, args.nick)

    xmpp.register_plugin('xep_0030') # Service Discovery

    xmpp.register_plugin('xep_0045') # Multi-User Chat

    xmpp.register_plugin('xep_0199') # XMPP Ping


    xmpp.connect()

    xmpp.process()