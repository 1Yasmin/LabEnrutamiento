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
import ssl


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
        #recibiods
        self.received_from = []
        #neighbors
        self.neighbors = []
        #message
        self.compound_msg = ""
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
            print ("%(body)s" % msg)
            #add to received from
            
            partir_mensaje = msg['body'].split()
            usuario_que_envio = partir_mensaje[0]
            xmpp.received_from.append(usuario_que_envio)
            #who is the message for?
            am_i_final = partir_mensaje[1]
            if am_i_final == xmpp.jid:
                print("Flood has finished")
            elif user_to_send in xmpp.neighbors:
                # obtain index of element
                distance_index = xmpp.neighbors.index(user_to_send) + 1
                dest_distance = xmpp.neighbors[distance_index]
                xmpp.compound_msg = start_of_message + " " + dest_distance + " " + "nodes: " + " ".join(
                    xmpp.received_from) + " " + msg_to_send
                print(compound_msg)
            else:
                for i in range(len(xmpp.neighbors)):
                    if (i % 2 == 0 and xmpp.neighbors[i] not in xmpp.received_from):
                        xmpp.send_message(mto=xmpp.neighbors[i], mbody=xmpp.compound_msg, mtype='chat')


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

        #if opts.jid is None:
          #      opts.jid = raw_input("Username: ")
        
        #if opts.password is None:
          #      opts.password = getpass.getpass("Password: ")
        #if opts.to is None:
                #opts.to = raw_input("Send To: ")
        #if opts.message is None:
                #opts.message = raw_input("Message: ")

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

        
        #authentication over an unencrypted connection
        xmpp['feature_mechanisms'].unencrypted_plain = True
        xmpp.ssl_version = ssl.PROTOCOL_TLS

        
        if xmpp.connect(('alumchat.xyz', 5222)):
        #if xmpp.connect():
                xmpp.process(block=False)
                #xmpp.remove_item()
                time.sleep(5)
                while True:
                    print("press 1 to use Flooding")
                    print("press 2 to use fast message to esam")
                    print("press 3 to use Link state routing")
                    ch = raw_input(">: ")
                #send a message
                    if(ch==str(1)):
                        print("Flooding")
                        print("write your neighbors and distance separated by a space")
                        print("example: node@alumchat.xyz 10 quack@alumchat.xyz 8")
                        neigh = raw_input("my neighbors are: ")
                        try:
                            neighbors = neigh.split()
                        except:
                            print("error defining neighbors")
                        print("neighbors: {}".format(neighbors))
                        print("who is the message for?")
                        user_to_send = raw_input(">: ")
                        print("what is your message?")
                        msg_to_send = raw_input(">: ")
                        #compose message according to the requirements
                        start_of_message = str(xmpp.jid) + " " + user_to_send + " " + str(jumps)
                        #send msg to neighbors
                        #in this case destination can be found in neighbors and does not need to be send to every single neighbor
                        if user_to_send in neighbors:
                            #obtain index of element
                            distance_index = neighbors.index(user_to_send) + 1
                            dest_distance = neighbors[distance_index]
                            compound_msg = start_of_message + " " + dest_distance + " " + "nodes: " + " ".join(xmpp.received_from) + " " + msg_to_send
                            print(compound_msg)
                        else:
                            for i in range(len(xmpp.neighbors)):
                                if(i % 2 == 0 and xmpp.neighbors[i] not in xmpp.received_from):
                                    print("sending to: {}".format(xmpp.neighbors))
                                    xmpp.send_message(mto=xmpp.neighbors[i], mbody=xmpp.compound_msg, mtype='chat')
                            
                            
                                #print("who is the message for?")
                                #user_to_send = raw_input(">: ")
                                #print("what is your message?")
                                #msg_to_send = raw_input(">: ")
                                #print("sending msg")
                                #xmpp.send_message(mto=user_to_send, mbody = msg_to_send, mtype = 'chat')
                    elif(ch==str(2)):
                        xmpp.send_message(mto="megaman@alumchat.xyz", mbody="pika pika", mtype='chat')
                    elif(ch==str(3)):
                        print("Link state routing")
                        call_linkstaterouting()
                        
                                
        else:
            print("Unable to connect.")
