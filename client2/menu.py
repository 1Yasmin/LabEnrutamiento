import os
import sys
#se cargan los archivos para que corran al ser seleccionados
client = "python sendclient1.py"
register = "python register.py"
file = "python filetransfer.py"
group = "python groupchat.py"


def main():
    menu()


def menu():
    print()
    print("************XMPP Chat - Ana Lucia Diaz**************")
    print()

    opcion = input("""
                    Ingrese la letra de la Opcion requerida:
    
                      A: Registrar una cuenta en el servidor alumchat.xyz
                      B: Cliente XMPP
                      C: Grupos XMPP
                      D: Transferencia de Archivos
                      Q: Logout
                      
                    """)

    if opcion == "A" or opcion == "a":
        os.system(register)
    elif opcion == "B" or opcion == "b":
        os.system(client)
    elif opcion == "C" or opcion == "c":
        os.system(group)
    elif opcion == "D" or opcion == "d":
        os.system(file)
    elif opcion == "Q" or opcion == "q":
        sys.exit
    else:
        print("Seleccione una opcion existente")
        print("Vuelva a intentarlo!")
        menu()


main()
