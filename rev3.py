#automatisches ausgeben der befehlskette durch nutzereingabe und verknüpfung mit blanko konfiguration
#nutzereingabe über while schleifen für eventuelle manuelle fehlerkorektur
#Copyright: Nick von Podewils, Relaxo Software©
#
#ToDos:
#-Eine Type überprüfung wäre gut, funktion steht, da input() aber standartmäßig str als return hat, muss wahrscheinlich 
#eigene überarbeitete input() geschrieben werden, die den kleinstmöglichen datentyp returnt
#-Tabellenüberprüfung muss an lvl ende eingefügt werden
#   Wenn fertig:
#       -alle rückfragen auf richtigkeit überprüfen 
#       -editierbare tabelle einpflegen
#Wenn alles fertig:
#   -auf zettel steht mehr
#
#

from tabulate import tabulate

from time import sleep 
import os

f = open(r"out.txt","w")


# def test_for_right(erwarteter_typ,eingabe,frage,level = 0):
#     print(eingabe)
#     #tests for type error
#     if erwarteter_typ == "str":
#         if type(eingabe) != str:
#             while True:
#                 print("Ihre Eingabe war falsch. Bitte geben sie eine Zechenfolge des Types \"String\" an (ASCII/Unicode).")
#                 print(frage)
#                 action = input()
#                 if type(action) == str:
#                     return
#         else:
#             return
#     if erwarteter_typ == "int":
#         if type(eingabe) != int:
#             while True:
#                 print("Ihre Eingabe war falsch. Bitte geben sie einen Integer ein (Zahlen zwischen -2,1 und +2,1 Milliarden)")
#                 print(frage)
#                 action = input()
#                 if type(action) == int:
#                     return
#         else:
#             return


#wenn untere funktion fertig, alle rückfragen auf richtigkeit entfernen!
def tabelle(Eingaben):
    #Eingaben muss dem schema Eingaben[[Frage,Antwort],[Frage,Antwort],[etc],etc]
    print(tabulate(Eingaben), headers = ["Frage","Eingabe"])
        
#nimmt fragen auf, wird nach jedem level resettet



level = 0

while True:
    while level == 0:
        print("Willkommen")
        sleep(2)
        #os.system('cls' if os.name == 'nt' else 'clear')
        #fragen = fragen + ["Bitte geben sie den Namen des Switches ein"]
        #frage_index = 0
        #print(fragen[frage_index])
        print("Bitte geben sie den Namen des Switches ein")
        switchname = input()
        #os.system('cls' if os.name == 'nt' else 'clear')
        #print("Ist die Eingabe richtig?(y/n)")
        #print(switchname)
        action = input()
        print(action)
        if action == "y":
            level = 1
            f.write("conf")
            f.write("\n")
            f.write(f"hostname {switchname}")
            f.write(f"\n")
            os.system('cls' if os.name == 'nt' else 'clear')
            
    while level == 1:
        print("VLAN-Config (automatisch)")
        sleep(2)
        #os.system('cls' if os.name == 'nt' else 'clear')
        f.write("conf")
        f.write("\n")
        f.write("vlan 2")
        f.write("\n")
        f.write("description CTX")
        f.write("\n")
        f.write("name CTX")
        f.write("\n")
        f.write("vlan 4")
        f.write("\n")
        f.write("description POS")
        f.write("\n")
        f.write("name POS")
        f.write("\n")
        f.write("vlan 5")
        f.write("\n")
        f.write("description LDT")
        f.write("\n")
        f.write("name LDT")
        f.write("\n")
        f.write("vlan 7")
        f.write("\n")
        f.write("description SI")
        f.write("\n")
        f.write("name SI")
        f.write("\n")
        f.write("vlan 8")
        f.write("\n")
        f.write("description VI")
        f.write("\n")
        f.write("name VI")
        f.write("\n")
        f.write("vlan 9")
        f.write("\n")
        f.write("description PMS")
        f.write("\n")
        f.write("name PMS")
        f.write("\n")
        #f.write("vlan 22")
        #f.write("\n")
        #f.write("description SW")
        #f.write("\n")
        #f.write("name SW")
        #f.write("\n")
        f.write("vlan 30")
        f.write("\n")
        f.write("description REM")
        f.write("\n")
        f.write("name REM")
        f.write("\n")
        f.write("vlan 70")
        f.write("\n")
        f.write("description VoIP")
        f.write("\n")
        f.write("name VoIP")
        f.write("\n")
        f.write("vlan 91")
        f.write("\n")
        f.write("description LT")
        f.write("\n")
        f.write("name LT")
        f.write("\n")
        f.write("vlan 92")
        f.write("\n")
        f.write("description PLS")
        f.write("\n")
        f.write("name PLS")
        f.write("\n")
        f.write("vlan 134")
        f.write("\n")
        f.write("description VI-EX")
        f.write("\n")
        f.write("name VI-EX")
        f.write("\n")
        f.write("conf")
        f.write("\n")
        level = 2
        sleep(5)

    while level == 2:
        print("Wie heißt das MGMT-Vlan? (VLAN-Tag)")
        MGMT_VLAN_TAG = int(input())
        #os.system('cls' if os.name == 'nt' else 'clear')
        print("Ist die Eingabe richtig?(y/n)")
        print(MGMT_VLAN_TAG)
        action = input()
        if action == "y":
            f.write(f"vlan {MGMT_VLAN_TAG}")
            f.write("\n")
            while level == 2:
                print("Wie lautet die Beschreibung?")
                MGMT_VLAN_DESCR = input()
                #os.system('cls' if os.name == 'nt' else 'clear')
                print("Ist die Eingabe richtig?(y/n)")
                print(MGMT_VLAN_DESCR)
                action = input()
                if action == "y":
                    f.write(f"description {MGMT_VLAN_DESCR}")
                    f.write("\n")
                    while level == 2:
                        #Hier muss eventuell NAME und DESCRIPTION zusammengeführt werden
                        print("Wie lautet der Name?")
                        MGMT_VLAN_NAME = input()
                        #os.system('cls' if os.name == 'nt' else 'clear')
                        print("Ist die Eingabe richtig?(y/n)")
                        print(MGMT_VLAN_NAME)
                        action = input()
                        if action == "y":
                            f.write(f"name {MGMT_VLAN_NAME}")
                            f.write("\n")
                            f.write(f"int vlan {MGMT_VLAN_TAG}")
                            f.write("\n")
                            print("Wie lautet die IP-Adresse?")
                            print("Bitte halten sie die Form: x.x.x.x/xx ein!")
                            MGMT_VLAN_IP = input()
                            print("ist die Eingabe richtig? (y/n)")
                            print(MGMT_VLAN_IP)
                            action = input()
                            if action == "y":
                                f.write(f"ip address {MGMT_VLAN_IP}")
                                f.write("\n")
                                level = 3
                                os.system('cls' if os.name == 'nt' else 'clear')
    
    while level == 3:
        print("Wie viele Ports hat der Switch?")
        ANZ_PORTS = int(input())
        #os.system('cls' if os.name == 'nt' else 'clear')
        print("Ist die Eingabe richtig?(y/n)")
        print(ANZ_PORTS)
        action = input()
        if action == "y":
            #os.system('cls' if os.name == 'nt' else 'clear')
            print("Geben sie nun in aufsteigender Reihenfolge, beim ersten Port beginnend, die Portnamen ein.")
            print("Halten sie dabei Folgende form ein:")
            print("    [Portname1];[Portname2];usw...")
            LISTE_DER_VLAN_ZUGEHÖRIGKEIT_DER_PORTS_STRING = input()
            #os.system('cls' if os.name == 'nt' else 'clear')
            print("Ist die Eingabe richtig?(y/n)")
            print(LISTE_DER_VLAN_ZUGEHÖRIGKEIT_DER_PORTS_STRING)
            action = input() 
            if action == "y":
                i = 1
                LISTE_DER_VLAN_ZUGEHÖRIGKEIT_DER_PORTS_ARRAY = LISTE_DER_VLAN_ZUGEHÖRIGKEIT_DER_PORTS_STRING.split(";")
                while i < ANZ_PORTS:
                    #Testet ob Eingabe ein X ist. Falls ja, wird entsprechender Port übersprungen
                    if LISTE_DER_VLAN_ZUGEHÖRIGKEIT_DER_PORTS_ARRAY[i-1] == "X":
                        i = i + 1
                        continue
                    f.write(f"int 1/1/{i}")
                    f.write("\n")
                    f.write(f"description {LISTE_DER_VLAN_ZUGEHÖRIGKEIT_DER_PORTS_ARRAY[i-1]}")
                    f.write("\n")
                    i = i + 1
                    level = 4
                    os.system('cls' if os.name == 'nt' else 'clear')
                break
            break
        break
    
    while level == 4:
        print("VLAN Config access Ports (manuell)")
        sleep(2)
        print("Möchten sie einem VLAn Ports zuweisen?(y/n)")
        action = input()
        if action == "y":
            print("Welchem VLAN wollen sie Ports zuweisen?")
            VLAN = input()
            #os.system('cls' if os.name == 'nt' else 'clear')
            print("Ist die Eingabe richtig?(y/n)")
            print(VLAN)
            action = input()
            if action =="y":
                print(f"Bitte geben sie alle Ports an, die zu dem VLAN {VLAN} gehören. Separieren sie die Portnummern mit \";\". Beachten sie, dass sie nicht das MGMT-VLAN eingeben. ")
                LISTE_PORTS_DIE_ZU_VLAN_GEHOEREN_STRING = input()
                LISTE_PORTS_DIE_ZU_VLAN_GEHOEREN_ARRAY = LISTE_PORTS_DIE_ZU_VLAN_GEHOEREN_STRING.split(";")
                i = 0
                for x in LISTE_PORTS_DIE_ZU_VLAN_GEHOEREN_ARRAY:
                    f.write(f"int 1/1/{LISTE_PORTS_DIE_ZU_VLAN_GEHOEREN_ARRAY[i]}")
                    f.write("\n")
                    f.write(f"vlan access {VLAN}")
                    f.write("\n")
                    i = i + 1
        print("Möchten sie ein weiteres VLAN konfigurieren?(y/n)")
        action = input()
        if action == "n":
            level = 5
            os.system('cls' if os.name == 'nt' else 'clear')

    while level == 5:
        print("Wie lautet der Trunk-Port?")
        TRUNK_PORT = input()
        print("Ist die eingabe richtig?(y/n)")
        print(TRUNK_PORT)
        action = input()
        if action == "y":
            f.write(f"int 1/1/{TRUNK_PORT}")
            f.write("\n")
            print("Bitte geben sie alle VLANS, die auf diesen Port zugreifen, ein, außer das MGMT-VLAN. Separieren sie bei mehreren VLANs mit dem ;")
            TRUNK_PORT_ZUGRIFFS_PORTS_STRING = input()
            print("Ist die Eingabe richtig?(y/n)")
            print(TRUNK_PORT_ZUGRIFFS_PORTS_STRING)
            action = input()
            if action == "y":
                TRUNK_PORT_ZUGRIFFS_PORTS_STRING = TRUNK_PORT_ZUGRIFFS_PORTS_STRING.replace(";",",")
                f.write(f"vlan trunk allowed {MGMT_VLAN_TAG},{TRUNK_PORT_ZUGRIFFS_PORTS_STRING}")
                f.write("\n")
                #os.system('cls' if os.name == 'nt' else 'clear')
                print("Möchten sie einen weiteren Trunkport einrichten?(y/n)")
                action = input()
                if action == "n":
                    level = 6
                    os.system('cls' if os.name == 'nt' else 'clear')

    while level == 6:
        print("Bitte geben sie das Gateway an.")
        GATEWAY = input()
        #os.system('cls' if os.name == 'nt' else 'clear')
        print("Ist die Eingabe richtig?(y/n)")
        print(GATEWAY)
        action = input()
        if action == "y":
            level = 7
            while level == 7:
                f.write(f"ip route 0.0.0.0/0 {GATEWAY}")
                f.write("\n")
                f.write("aruba-central")
                f.write("\n")
                f.write("disable")
                f.write("\n")
                f.write("no ntp server pool.ntp.org")
                f.write("\n")
                print("Bitte geben sie die IP ihres NTP-Servers ein")
                IP_NTP_SERVER = input()
                #os.system('cls' if os.name == 'nt' else 'clear')
                print("Ist die Eingabe richtig?(y/n)")
                print(IP_NTP_SERVER)
                action = input()
                if action == "y":
                    f.write(f"ntp server {IP_NTP_SERVER}")
                    f.write("\n")
                    level = 8
                    os.system('cls' if os.name == 'nt' else 'clear')

    while level == 8:
        print("Möchten sie einen neuen User anlegen?(y/n)")
        action = input()
        if action == "n":
            level = 8
            break
        print("Wie soll der neue User heißen?")
        USER_NAME = input()
        #os.system('cls' if os.name == 'nt' else 'clear')
        print("Ist die Eingabe richtig?(y/n)")
        print(USER_NAME)
        action = input()
        if action == "y":
            print("Zu welcher Gruppe soll der User hinzugefügt werden?")
            USER_GROUP = input()
            #os.system('cls' if os.name == 'nt' else 'clear')
            print("Ist die Eingabe richtig?(y/n)")
            print(USER_GROUP)
            action = input()
            if action == "y":
                print("Wie lautet das Password?")
                USER_PW = input()
                #os.system('cls' if os.name == 'nt' else 'clear')
                print("Ist die Eingabe richtig?(y/n)")
                print(USER_PW)
                action = input()
                if action == "y":
                    f.write(f"user {USER_NAME} group {USER_GROUP} password plaintext {USER_PW}")
                    f.write("\n")
                    print("Möchten sie einen weiteren User anlegen?(y/n)")
                    action = input()
                    if action == "n":
                        os.system('cls' if os.name == 'nt' else 'clear')
                        break
                
    f.write("port-access port-security enable")
    f.write("\n")
    i = 1
    while i <= ANZ_PORTS:
        f.write(f"int 1/1/{i}")
        f.write("\n")
        f.write("port-access port-security enable")
        f.write("\n")
        f.write("port-access port-security sticky-learn enable")
        f.write("\n")
        f.write("port-access port-security client-limit 5")
        f.write("\n")
        i = i + 1
        os.system('cls' if os.name == 'nt' else 'clear') 

    f.write("show running-config")
    break

print("Das Programm ist nun fertig, die Befehlskette finden sie in der out.txt.")
print("Das programm schließt sich in 10 Sekuden selbst")
sleep(10)

    




















