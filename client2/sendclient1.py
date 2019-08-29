import logging
from copy import deepcopy
from getpass import getpass
from argparse import ArgumentParser
import slixmpp
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.asyncio import asyncio
import sys 
import os
from linkstaterouting import call_linkstaterouting

class SendMessageLinkStateRouting(slixmpp.ClientXMPP):
    start = 0
    end = 0
    #recipiente sera el usuario a quien se lo vamos a enviar y mensaje el mensaje que vamos a enviar.
    def __init__(self, jid, password, recipient, recipient2, message, start, end):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        #mensaje que vamos a enviar y mensaje que vamos a recibir.
        self.recipient = recipient
        self.recipient2 = recipient2
        self.msg = message
        self.add_event_handler("session_start", self.start)
        self.start = start
        self.end = end
        #se carga message para estar recibiendo mensajes
        #self.add_event_handler("message", self.message)
        self.add_event_handler("message", self.call_linkstaterouting)

    #en mtype se define como chat por lo que al levantarse entrara directo al area del chat.
    def start(self, event):
        self.send_presence()
        self.get_roster()
        self.send_message(mto=self.recipient,
                          mbody=self.msg,
                          mtype='chat')
        self.send_message(mto=self.recipient2,
                          mbody=self.msg,
                          mtype='chat')
    #se ingresa funcion de reply para responder mensajes, recordando que este no es asincrono
    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            print(msg)
            print("Mensaje recibido:\n%(body)s" % msg)
            nuevomensaje = input("envia un mensaje:")
            msg.reply(nuevomensaje).send()
            print("Enviaste un nuevo mensaje:", nuevomensaje)
            if (nuevomensaje == "exit"):
                self.disconnect()
                os.system("python menu.py")
                sys.exit()
    def Dijkstra(G,start,end=None):
        D = {}	#distancia final
        P = {}	# predecedores
    
        Q = priorityDictionary()   
        Q[start] = 0
        for v in Q:
            D[v] = Q[v]
            if v == end: break
            for w in G[v]:
                vwLength = D[v] + G[v][w]
                if w in D:
                    if vwLength < D[w]:
                        pass
                elif w not in Q or vwLength < Q[w]:
                    Q[w] = vwLength
                    P[w] = v
        return (D,P)
    def shortestPath(G,start,end):
        D,P = Dijkstra(G,start,end)
        Path = []
        while 1:
            Path.append(end)
            if end == start: break
            end = P[end]
        Path.reverse()
        return Path
    #linkstaterouting
    def call_linkstaterouting(self, msg):
        graph = {}
        data = []
        path = []
    
        while True:
            try:
                localgraph = deepcopy(graph)
                G = {}
                for x in graph:
                    G[x] = {}
                    for y in localgraph[x]["data"]:
                        G[x][y[0]] = float(y[1])
                        for x in graph:
                            if x != recipient:
                                path = shortestPath(G, recipient, x)
                                self.send_message(mto=self.recipient,mbody=self.msg,mtype='chat')
                                if msg['type'] in ('chat', 'normal'):
                                    print(msg)
                                    print("Mensaje recibido:\n%(body)s" % msg)
                                    nuevomensaje = input("envia un mensaje:")
                                    msg.reply(nuevomensaje).send()
                                    print("Enviaste un nuevo mensaje:", nuevomensaje)
                                    if (nuevomensaje == "exit"):
                                        self.disconnect()
                                        os.system("python menu.py")
                                        sys.exit()
                                cost = 0
                                for x in range(0, len(path)-1):
                                    cost += G[path[x]][path[x+1]]
                                    print(path[x], end="")
                                    print(path[len(path)-1],end="")
                                    print("%.1f" % cost)
            except Exception as e:
                print(e)
                pass
                
    

#clase para eliminar usuario
class EliminarUsuario (slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        #mensaje que vamos a enviar y mensaje que vamos a recibir.
        self.add_event_handler("session_start", self.start)
        #llamando a la funcion de eliminar
        self.add_event_handler("eliminar", self.eliminar)
    def start(self, event):
        self.send_presence()
        self.get_roster()
        print("HAS ELIMINADO AL USUARIO")
        os.system("python menu.py")
        sys.exit()
        #funcion de eliminar
    def eliminar(self):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['from'] = self.boundjid.user
        resp['register'] = ' '
        #resp['register']['remove'] = ' '
        resp['register']['unregistered_user'] = ' '
        try:
            resp.send(now=True)
            print("Account deleted for %s!" % self.boundjid)
        except IqError as e:
            logging.error("Could not delete account: %s" %
                    e.iq['error']['text'])
            self.disconnect()
            os.system("python menu.py")
            sys.exit()
        except IqTimeout:
            logging.error("No response from server.")
            self.disconnect()
            os.system("python menu.py")
            sys.exit()
#funcion para Enviar un mensaje
class SendMessage(slixmpp.ClientXMPP):
    #recipiente sera el usuario a quien se lo vamos a enviar y mensaje el mensaje que vamos a enviar.
    def __init__(self, jid, password, recipient, message):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        #mensaje que vamos a enviar y mensaje que vamos a recibir.
        self.recipient = recipient
        self.msg = message
        self.add_event_handler("session_start", self.start)
        #se carga message para estar recibiendo mensajes
        self.add_event_handler("message", self.message)
        
#en mtype se define como chat por lo que al levantarse entrara directo al area del chat.
    def start(self, event):
        self.send_presence()
        self.get_roster()
        self.send_message(mto=self.recipient,
                          mbody=self.msg,
                          mtype='chat')
#se ingresa funcion de reply para responder mensajes, recordando que este no es asincrono
    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            print(msg)
            print("Mensaje recibido:\n%(body)s" % msg)
            nuevomensaje = input("envia un mensaje:")
            msg.reply(nuevomensaje).send()
            print("Enviaste un nuevo mensaje:", nuevomensaje)
            if (nuevomensaje == "exit"):
                self.disconnect()
                os.system("python menu.py")
                sys.exit()
 #funcion para mandar mensaje de presencia  , se llamo la funcion make_presence al ingresar a un chat. en el chat en grupo se ve mejor la funcionalidad del mensaje de presencia         
class SendMessagePresence(slixmpp.ClientXMPP):

    def __init__(self, jid, password, recipient, message):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        #mensaje que vamos a enviar y mensaje que vamos a recibir.
        self.recipient = recipient
        self.msg = message
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)
        

    def start(self, event):
        self.make_presence(pfrom = "dia151378@alumchat.xyz", pstatus ="connected", pshow = "dia151378@alumchat.xyz is connected")
        self.send_presence()
        self.get_roster()
        self.send_message(mto=self.recipient,
                          mbody=self.msg,
                          mtype='chat')
        
    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            print(msg)
            print("Mensaje recibido:\n%(body)s" % msg)
            nuevomensaje = input("envia un mensaje:")
            msg.reply(nuevomensaje).send()
            print("Enviaste un nuevo mensaje:", nuevomensaje)
            if (nuevomensaje == "exit"):
                self.disconnect()
                os.system("python menu.py")
                sys.exit()
            elif user_to_send in xmpp.neighbors:
                distance_index = xmpp.neighbors.index(user_to_send) + 1
                dest_distance = xmpp.neighbors[distance_index]
                xmpp.compound_msg = start_of_message + " " + dest_distance + " " + "nodes: " + " ".join(
                    xmpp.received_from) + " " + msg_to_send
                print(compound_msg)

            else:
                for i in range(len(xmpp.neighbors)):
                    if (i % 2 == 0 and xmpp.neighbors[i] not in xmpp.received_from):
                        xmpp.send_message(mto=xmpp.neighbors[i], mbody=xmpp.compound_msg, mtype='chat')
#clase de SignIN se llama al plugin xep0047, se vuelve a enviar el mensaje de presencia.
class SignIn(slixmpp.ClientXMPP):

    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("ibb_stream_start", self.abrirdata)
        self.add_event_handler("ibb_stream_data", self.datacorriente)
        self.register_plugin('xep_0047', {
            'auto_accept': True
        })
        self.neighbors = []

    def start(self, event):
        self.make_presence(pfrom = "dia151378@alumchat.xyz", pstatus ="connected", pshow = "dia151378@alumchat.xyz is connected")
        self.send_presence()
        self.make_message
        #self.send_presence(pfrom = "dia151378@alumchat.xyz", pstatus ="connected", pshow = "dia151378@alumchat.xyz is connected")
        print(self.make_presence(pfrom = "dia151378@alumchat.xyz", pstatus ="connected", pshow = "dia151378@alumchat.xyz is connected"))
        #print("send_presence",self.send_presence(pfrom = "dia151378@alumchat.xyz", pstatus ="connected", pshow = "dia151378@alumchat.xyz is connected"))
        self.get_roster()
        #self.makePresence(pshow=None, pstatus=None, ppriority=None, pto=None, ptype=None, pfrom=None, pnick=None)
        print("YOU HAVE SUCCESFULLY SIGN IN")
        #self.disconnect()
    #otro intento para eliminar usuario basado en lo que dice la libreria que se haga pero no funciona.
    def eliminar_usuario(self, iq):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['from'] = self.boundjid.user
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password
        resp['register']['remove'] = ""

        try:
            resp.send(now=True)
            print(" Se a eliminado la cuenta%s!" % self.boundjid)
        except IqError as e:
            logging.error("Could not delete account: %s" %
                    e.iq['error']['text'])
            self.disconnect()
            os.system("python menu.py")
            sys.exit()

    #funciones para enviar archivo, al final no se utilizaron
    def abrirdata(self, stream):
         print('Stream opened: %s from %s' % (stream.sid, stream.peer_jid))
    def datacorriente(self, event):
            print(event['data'])
    def Enviar_Archivo(self,whotosend, filetosend):
            stream = self['xep_0047'].open_stream(whotosend)
            with open(filetosend) as f:
                data = f.read()
                stream.sendall(data)
#otro intento de enviar mensaje de presencia
class SendPresenceMessage(slixmpp.ClientXMPP):

    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)

    def start(self, event):
        self.send_presence()
        xmpp.make_presence(pfrom=jid, pstatus='Ana lucia esta conectada', pshow='xa')
        
        self.get_roster()
        print(xmpp.make_presence(pfrom=jid, pstatus='Ana lucia esta conectada', pshow='xa'))
        self.disconnect()
        os.system("python menu.py")
        sys.exit()
#funcion para salir
class LogOut(slixmpp.ClientXMPP):

    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)

    def start(self, event):
        self.disconnect()
        os.system("python menu.py")
        sys.exit()
#funcion para enviar notificacion, envia una notificacion en https://jwchat.org/ nos muestra como se abre la ventana al utilizarlo
class Enviar_Notificacion(slixmpp.ClientXMPP):

    def __init__(self, jid, password, recipient, message):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        #mensaje que vamos a enviar y mensaje que vamos a recibir.
        self.recipient = recipient
        self.msg = message
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)
        

    def start(self, event):
        self.make_presence(pfrom = "dia151378@alumchat.xyz", pstatus ="connected", pshow = "dia151378@alumchat.xyz is connected")
        self.send_presence()
        self.get_roster()
        self.send_message(mto=self.recipient,
                          mbody=self.msg)
        
    def message(self, msg):
        if msg['type'] in ('', 'normal'):
            #msg.reply("Thanks for sending\n%(body)s" % msg).send()
            print(msg)
            print("Notificacion recibida:\n%(body)s" % msg)
            nuevomensaje = input("responde la notificacion:")
            msg.reply(nuevomensaje).send()
            print("Enviaste un nuevo mensaje:", nuevomensaje)
            if (nuevomensaje == "exit"):
                self.disconnect()
                os.system("python menu.py")
                sys.exit()
#funcion para ver usuarios conectados       
class VerUsuarios(slixmpp.ClientXMPP):

    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("changed_status", self.wait_for_presences)
        self.received = set()
        self.presences_received = asyncio.Event()
        

#funcion asincrona para iniciar en donde iniciamos el cargando usuarios es importante mencionar que se realiza por roster, tiene un tiempo de espera de 10 segundos
#luego de esta entra a grupos de roster en donde vemos sus caracteristicas.
    async def start(self, event):
        future = asyncio.Future()
        def callback(result):
            future.set_result(None)
        try:
            self.get_roster(callback=callback)
            await future
        except IqError as err:
            print('Error: %s' % err.iq['error']['condition'])
        except IqTimeout:
            print('Error: Request timed out')
        self.send_presence()
        print('Cargando usuarios...\n')
        await asyncio.sleep(10)
        print('Roster para %s' % self.boundjid.bare)
        groups = self.client_roster.groups()
        for group in groups:
            print('\n%s' % group)
            print('-' * 72)
            for jid in groups[group]:
                sub = self.client_roster[jid]['subscription']
                name = self.client_roster[jid]['name']
                if self.client_roster[jid]['name']:
                    print(' %s (%s) [%s]' % (name, jid, sub))
                else:
                    print(' %s [%s]' % (jid, sub))
                connections = self.client_roster.presence(jid)
                for res, pres in connections.items():
                    show = 'available'
                    if pres['show']:
                        show = pres['show']
                    print('   - %s (%s)' % (res, show))
                    if pres['status']:
                        print('       %s' % pres['status'])
        self.send_presence()
        self.get_roster()
        #funcion para Agregar o Ver Detalles si se presiona 1 Se agrega y 2 se ven Detalles
        print("Agregar usuario")
        print("_______________________________________")
        pregunta = input("Deseas agregar un nuevo usuario (1) o ver Detalles de Usuario (2)")
        if pregunta == "1":
             newuser = input("Ingresa un nuevo usuario >>")
             #para agregar usuario era simplemente un send_presence del nuevo usuario con tipo subscribe
             xmpp.send_presence(pto=newuser, ptype = 'subscribe')
             print("Se a ingresado nuevo usuario")
             os.system("python menu.py")
             sys.exit()
        if pregunta =="2":
            #para ver el contacto ingresar al client_roster y dentro del client_roster buscamos el userdata en base a como se llama
            userdata = input("Ingrese el contacto que desea ver detalles: ")
            userroster = self.client_roster
            print("Detalles de usuario" + userdata + " :")
            print(userroster[userdata])
            os.system("python menu.py")
            sys.exit()

    def wait_for_presences(self, pres):
        self.received.add(pres['from'].bare)
        if len(self.received) >= len(self.client_roster.keys()):
            self.presences_received.set()
        else:
            self.presences_received.clear()

if __name__ == '__main__':
    parser = ArgumentParser(description=SendMessage.__doc__)

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
    parser.add_argument("-t", "--to", dest="to",
                        help="JID to send the message to")
    parser.add_argument("-m", "--message", dest="message",
                        help="message to send")

    args = parser.parse_args()
    #log in 
    logging.basicConfig(level=args.loglevel,
                        format='%(levelname)-8s %(message)s')

    if args.jid is None:
        args.jid = input("Username: ")
    if args.password is None:
        args.password = getpass("Password: ")
    xmpp = SignIn(args.jid, args.password)
    xmpp.register_plugin('xep_0030') # service
    xmpp.register_plugin('xep_0199') # ping
    xmpp.register_plugin('xep_0047')
    xmpp.register_plugin('xep_0004')  
    xmpp.register_plugin('xep_0060')  
    xmpp.register_plugin('xep_0065')  
    xmpp.register_plugin('xep_0066')  
    xmpp.register_plugin('xep_0077')  
    xmpp.connect()
    print ("Selecciona una opción")
    print ("Selecciona 1 si deseas enviar un mensaje")
    print ("Selecciona 2 si deseas desconectarte")
    print ("Selecciona 3 si deseas ver todos los usuarios")
    print ("Selecciona 4 si deseas enviar un mensaje de presencia")
    print ("Selecciona 5 si deseas eliminar usuario")
    print ("Selecciona 6 si deseas enviar una notificacion")
    print ("Selecciona 7 si Link State Routing")
    print ("Selecciona 8 si Link State Routing vs 2")
    opcionMenu = input (" Inserta la Opcion que deseas >>")
    if opcionMenu=="1":
        if args.to is None:
            args.to = input("Send To: ")
        if args.message is None:
            args.message = input("Message: ")
        xmpp = SendMessage(args.jid, args.password, args.to, args.message)
        xmpp.connect()
        xmpp.process()
    elif opcionMenu=="8":
        usuario1 = input("Ingresa el primer usuario:  ")
        usuario2 = input("Ingresa el segundo usuario:  ")
        if args.to is None:
            args.to = input("Ingresa el usuario que deseas enviar mensaje: ")
        start = input("Ingresa el inicio: ")
        end = input("Ingresa el final: ")
        if args.message is None:
            args.message = input("Message: ")
        xmpp = SendMessageLinkStateRouting(args.jid, args.password, usuario1, usuario2, args.message, start, end)
        xmpp.connect()
        xmpp.process()

    elif opcionMenu=="2":
        print("Te has desconectado")
        LogOut(args.jid, args.password)
    elif opcionMenu=="3":
        print("Ver lista de usuarios")
        print("_____________________________")
        xmpp = VerUsuarios(args.jid, args.password)
        xmpp.connect()
        xmpp.process()
    elif opcionMenu=="4":
        #xmpp.make_presence(pfrom = xmpp.jid, pstatus ="connected", pshow = "Ana is connected")
        #xmpp = SendPresenceMessage(args.jid, args.password)
        #SendMessagePresence
        if args.to is None:
            args.to = input("Send To: ")
        if args.message is None:
            args.message = input("Message: ")
        new = "<presence from=dia151378@alumchat.xyz xml:lang=en><status>connected</status></presence>"
        xmpp = SendMessagePresence(args.jid, args.password, args.to, new)
        xmpp.connect()
        xmpp.process()
        print("has enviado un mensaje de presencia")
    elif opcionMenu=="5":
        xmpp = EliminarUsuario(args.jid, args.password)
        xmpp.connect()
        xmpp.process()
    elif opcionMenu=="6":
        print("Enviar Notificacion")
        if args.to is None:
            args.to = input("Para quien: ")
        if args.message is None:
            args.message = input("Contenido: ")
        xmpp = Enviar_Notificacion(args.jid, args.password, args.to, args.message)
        xmpp.connect()
        xmpp.process()
    elif opcionMenu=="7":
        print("Link state routing")
        print("write your neighbors and distance separated by a space")
        print("example: node@alumchat.xyz 10 quack@alumchat.xyz 8")
        neigh = input("my neighbors are: ")
        try:
            neighbors = neigh.split()
        except:
            print("error defining neighbors")
        print("neighbors: {}".format(neighbors))
        print("who is the message for?")
        user_to_send = input(">: ")
        print("what is your message?")
        msg_to_send = input(">: ")
        jumps = 0
        start_of_message = str(xmpp.jid) + " " + user_to_send + " " + str(jumps)
        if user_to_send in neighbors:
            distance_index = neighbors.index(user_to_send) + 1
            dest_distance = neighbors[distance_index]
            compound_msg = start_of_message + " " + dest_distance + " " + "nodes: "  + " " + msg_to_send
            call_linkstaterouting()
            print(compound_msg)
        else:
            for i in range(len(xmpp.neighbors)):
                if(i % 2 == 0 and xmpp.neighbors[i] not in xmpp.received_from):
                    print("sending to: {}".format(xmpp.neighbors))
                    call_linkstaterouting()
                    xmpp.send_message(mto=xmpp.neighbors[i], mbody=xmpp.compound_msg, mtype='chat')
        xmpp.connect()
        xmpp.process()

        
    
    
    else:
        print("no has seleccionado nada")
