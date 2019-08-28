import sys
import logging
import getpass
from optparse import OptionParser
from linkstaterouting import call_linkstaterouting
import sleekxmpp
from sleekxmpp.exceptions import IqError, IqTimeout

#time for delete user as server attempts to delete before it is created
import time
#ssl
#import ssl

paths = []
jumps = 0


if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input
#client class
class ChatBot(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password,):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        #recipient
        #self.recipient = recipient
        #message
        self.add_event_handler("message", self.message, threaded=True)
        #start
        self.add_event_handler("session_start", self.start, threaded=True)
        #register
        self.add_event_handler("register", self.register, threaded=True)

    def start(self, event):
          self.send_presence()
          self.get_roster()
          #send msg
          #self.send_message(mto=self.recipient, mbody = self.msg, mtype = 'chat')
          #disconnect
          #self.disconnect(wait=True)

    def register(self,event):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password
        try:
            resp.send(now=True)
            logging.info("Account created for %s!" % self.boundjid)
        except IqError as e:
            logging.error("Could not register account: %s" %
                    e.iq['error']['text'])
            self.disconnect()
        except IqTimeout:
            logging.error("No response from server.")
            self.disconnect()

            
    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            print("%(body)s" % msg)
            if(msg == "nodo"):
                partir_mensaje = msg['body'].split()
                usuario_que_envio = partir_mensaje[0]
                self.send_message(mto=usuario_que_envio, mbody=paths, mtype='chat')
            elif(msg in )


if __name__ == '__main__':
        optp = OptionParser()

        #verbose
        optp.add_option('-q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.INFO)
        
        optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)
        
        optp.add_option('-v', '--verbose', help='set logging to COMM',
                    action='store_const', dest='loglevel',
                    const=5, default=logging.INFO)

        #user
        optp.add_option("-j", "--jid", dest="jid",
                    help="JID to use")
        
        optp.add_option("-p", "--password", dest="password",
                    help="password to use")
        
        optp.add_option("-t", "--to", dest="to",
                    help="JID to send the message to")
        
        optp.add_option("-m", "--message", dest="message",
                    help="message to send")

        opts, args = optp.parse_args()

        #logging config
        logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')

        #initialize
        print("Press 1 to register")
        print("Press 2 to login")
        login_register = raw_input(">: ")

                
        opts.jid = raw_input("Username: ")
        opts.password = getpass.getpass("Password: ")
        
        xmpp = ChatBot(opts.jid, opts.password,)

        if(login_register == str(2)):
                xmpp.del_event_handler("register", xmpp.register)
        
        #plugins
        xmpp.register_plugin('xep_0030') # Service Discovery
        xmpp.register_plugin('xep_0004') # Data forms
        xmpp.register_plugin('xep_0060') # PubSub
        xmpp.register_plugin('xep_0199') # XMPP Ping

        #registration related
        xmpp.register_plugin('xep_0066') # Out-of-band Data
        xmpp.register_plugin('xep_0077') # In-band Registration
        
        if xmpp.connect(('alumchat.xyz', 5222)):
                xmpp.process(block=False)
                time.sleep(5)
                while True:
                    print("press 2 to use Distance vector routing")
                    ch = raw_input(">: ")
                    if(ch==str(2)):
                        print("Distance vector routing")
                        print("write your neighbors and distance separated by a space")
                        print("example: node@alumchat.xyz 10 quack@alumchat.xyz 8")
                        neigh = raw_input("my neighbors are: ")
                        try:
                            neighbors = neigh.split()
                            tmp = []
                            for node in neighbors:
                                if neighbors.index(node) %2 == 0:
                                    nodels = []
                                    nodels.append(node)
                                    tmp.append(nodels)
                                if not neighbors.index(node) % 2 == 0:
                                    tmp.append(node)
                                    paths.append(tmp)
                                    tmp = []
                                    nodels = []
                            print("path", paths)
                        except:
                            print("error defining neighbors")
                        print("who is the message for?")
                        user_to_send = raw_input(">: ")
                        print("what is your message?")
                        msg_to_send = raw_input(">: ")

                        try:
                            for p in paths:
                                user = paths[paths.index(p)][0]
                                print("user: ", user[0])
                                xmpp.send_message(mto=user, mbody="nodo", mtype='chat')
                        except:
                            print("Error al obtener los vecinos")
                        
                                
        else:
            print("Unable to connect.")
