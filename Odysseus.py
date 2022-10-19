#Copyright Nick von Podewils 2022
#
#Versions Log:
#   1.0 ===== 09.10.22 ===== Hauptanwendung
#   1.1 ===== 10.10.22 ===== Optionsmenü, Appearance Mode Wechselbar
#   1.1.1 ===== 10.10.2022 ===== Bugfixes
#   1.1.2 ===== 10.10.2022 ===== Sidebar besser beschriftet, Out.txt label kann refreshed werden
#   1.1.3 ===== 10.10.2022 ===== ToolTips Eingebaut, Progressbar eingebaut, welcomelabel zentriert
#   1.1.4 ===== 11.10.2022 ===== Unter Optionen kann Font und Größe geändert werden, wird in font.txt gespeichert
#
#
#
#
#
#
#
#
#
#
#
import tkinter as tk
import tkinter.messagebox
import customtkinter as ctk
import webbrowser
from PIL import Image, ImageTk
import os


f = open(r"out.txt","w")
f.write("")
f.close()

global PATH
PATH = os.path.dirname(os.path.realpath(__file__))

am = "System"
ct = "blue"

font_txt_file = open(PATH+"/font.txt","r")
font_type = font_txt_file.readline().replace("\n","")
font_size = int(font_txt_file.readline())
global font
font = (font_type,font_size)

class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = ctk.CTkToplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = ctk.CTkLabel(tw, text=self.text, justify=tk.LEFT, background="#ffffe0", relief=tk.SOLID,  text_font=("Roboto Medium", 8))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


class App(ctk.CTk):
    
    #namespace
    ctk.set_appearance_mode(am)  # Modes: "System" (standard), "Dark", "Light"
    ctk.set_default_color_theme(ct)  # Themes: "blue" (standard), "green", "dark-blue"

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.title("Odysseus")
        self.geometry("600x500")
        #self.iconbitmap(PATH + "/logo.ico")
        self.protocol("WM_DELETE_WINDOW", self.on_closing) # call .on_closing when window is closed

        # ===== create frames =====
        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_sidebar = ctk.CTkFrame(self, width=180, corner_radius=0)
        self.frame_sidebar.grid(row=0, column=0, sticky="nswe", pady=20)

        container = ctk.CTkFrame(self)
        container.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # ===== frame sidebar ====
        # gridlayout nx1 n=anzahl indexbuttons


        self.settings_image = self.load_image("//Gear.png", 20)

        self.frame_sidebar.grid_rowconfigure(0, minsize=0)

        self.indexbutton0 = ctk.CTkButton(self.frame_sidebar, text="Startseite", text_font=font, width=140, command=lambda: self.show_frame("StartPage"))
        self.indexbutton1 = ctk.CTkButton(self.frame_sidebar, text="Switchname", text_font=font, width=140, command=lambda: self.show_frame("PageOne"))
        self.indexbutton2 = ctk.CTkButton(self.frame_sidebar, text="MGMT-Vlan", text_font=font, width=140, command=lambda: self.show_frame("PageTwo"))
        self.indexbutton3 = ctk.CTkButton(self.frame_sidebar, text="Portconfig", text_font=font, width=140, command=lambda: self.show_frame("PageThree"))
        self.indexbutton4 = ctk.CTkButton(self.frame_sidebar, text="Vlanconfig", text_font=font, width=140, command=lambda: self.show_frame("PageFour"))
        self.indexbutton5 = ctk.CTkButton(self.frame_sidebar, text="Trunkport", text_font=font, width=140, command=lambda: self.show_frame("PageFive"))
        self.indexbutton6 = ctk.CTkButton(self.frame_sidebar, text="Gateway", text_font=font, width=140, command=lambda: self.show_frame("PageSix"))
        self.indexbutton7 = ctk.CTkButton(self.frame_sidebar, text="Users", text_font=font, width=140, command=lambda: self.show_frame("PageSeven"))
        self.indexbutton8 = ctk.CTkButton(self.frame_sidebar, text="Output", text_font=font, width=140, command=lambda: self.show_frame("PageAight"))
        self.options = ctk.CTkButton(self.frame_sidebar, text="Options", image= self.settings_image, compound="right", text_font=font, width=140, command=lambda: self.show_frame("Options"))


        # ===== pack center =====
        self.indexbutton0.pack()
        self.indexbutton1.pack(pady=5)
        self.indexbutton2.pack()
        self.indexbutton3.pack(pady=5)
        self.indexbutton4.pack()
        self.indexbutton5.pack(pady=5)
        self.indexbutton6.pack()
        self.indexbutton7.pack(pady=5)
        self.indexbutton8.pack()
        self.options.pack(side=tk.BOTTOM)

        # ===== screens =====
        self.frames = {}
        for F in (Options, StartPage, PageOne, PageTwo, PageThree, PageFour, PageFive, PageSix, PageSeven, PageAight):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")
        
    # ===== methods =====
    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def on_closing(self, event=0):
        self.destroy()

    def load_image(self, path, image_size):

        return ImageTk.PhotoImage(Image.open(PATH + path).resize((image_size, image_size)))

# ===== Schablone für neue Page =====
# class n(ctk.CTkFrame):
#     def __init__(self, parent, controller):
#         ctk.CTkFrame.__init__(self, parent)
#         self.controller = controller
#         # ===== define =====
#
#         # ===== pack =====
#



class Options(ctk.CTkFrame):
    
    def dropdown(choice):
        if choice == "Dark Mode":
            ctk.set_appearance_mode("Dark")
        if choice == "White Mode":
            ctk.set_appearance_mode("Light")
        if choice == "Systemstandard":
            ctk.set_appearance_mode("System")

    def change_font_type(choice):
        font_list = ["default","Calibri","Arial","Microsoft YaHei","Segoe UI", "Arial Itlaic"]
        for x in font_list:
            if choice == "default":
                font_txt = open(PATH+"/font.txt","r")
                font_size_temp = font_txt.readline()
                font_size_temp = font_txt.readline()
                font_txt.close()
                font_txt = open(PATH+"/font.txt","w")
                font_txt.write(f"Roboto Medium\n{font_size_temp}")
            elif choice == x and choice != "default":
                font_txt = open(PATH+"/font.txt","r")
                font_size_temp = font_txt.readline()
                font_size_temp = font_txt.readline()
                font_txt.close()
                font_txt = open(PATH+"/font.txt","w")
                font_txt.write(f"{choice}\n{font_size_temp}")

    def change_font_size(choice):
        font_list = ["8","10","12","14","16","18","20","22","24","26","28"]
        for x in font_list:
            if choice == x:
                font_txt = open(PATH+"/font.txt","r")
                font_type_temp = font_txt.readline()
                font_txt.close()
                font_txt = open(PATH+"/font.txt","w")
                font_txt.write(f"{font_type_temp}-{choice}")

        
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.label = ctk.CTkLabel(self, text="Appearance Mode: ", text_font=font)
        self.dropdown = ctk.CTkOptionMenu(self, values=["Dark Mode","White Mode","Systemstandard"], command=Options.dropdown)
        self.ph = ctk.CTkLabel(self, text="")
        self.button = ctk.CTkButton(self, text="zurück", command=lambda: controller.show_frame("StartPage"))
        self.versionlabel = ctk.CTkLabel(self, text="Version: 1.1.4")
        self.font_frame = ctk.CTkFrame(self)
        self.font_frame2 = ctk.CTkFrame(self)
        self.font_label = ctk.CTkLabel(self.font_frame, text="Font:         ", text_font=font)
        self.font_dropdown = ctk.CTkOptionMenu(self.font_frame2, values=["default","Calibri","Arial","Microsoft YaHei","Segoe UI", "Arial Itlaic"], command=Options.change_font_type)
        self.ph2 = ctk.CTkLabel(self, text="")
        self.font_label2 = ctk.CTkLabel(self.font_frame, text="Textgröße:", text_font=font)
        self.font_dropdown2 = ctk.CTkOptionMenu(self.font_frame2, values=["8","10","12","14","16","18","20","22","24","26","28"], command=Options.change_font_size)

        self.label.pack(anchor="w", padx=5)
        self.dropdown.pack(anchor="w", padx=5)
        self.ph.pack(anchor="w", padx=5)
        self.font_frame.pack(anchor="w", padx=5)
        self.font_frame2.pack(anchor="w", padx=5)
        self.font_label.pack(anchor="w", padx=5, side=tk.LEFT)
        self.font_dropdown.pack(anchor="w", padx=5, side=tk.LEFT)
        self.ph2.pack()
        self.font_label2.pack(anchor="w", padx=5)
        self.font_dropdown2.pack(anchor="w", padx=5)
        self.button.pack(anchor="se", padx=5)
        self.versionlabel.pack(anchor="center", side=tk.BOTTOM)

        CreateToolTip(self.font_label, "Benötigt Neustart")
        CreateToolTip(self.font_dropdown, "Benötigt Neustart")
        CreateToolTip(self.font_label2, "Benötigt Neustart")
        CreateToolTip(self.font_dropdown2, "Benötigt Neustart")
    


class StartPage(ctk.CTkFrame):
    
    def create_toplevel():
        path = __file__
        path2 = path.replace("Odysseus.py","")
        path2 = path2 + "Dokumentation.pdf"
        webbrowser.open_new(path2)

    def __init__(self, parent, controller):
        i = 0
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        welcomeLabel = ctk.CTkLabel(self, text="Willkommen bei Odysseus!", text_font=("Roboto Medium", -18))
        welcomeLabel2 = ctk.CTkLabel(self, text="Konfigurationsprogramm für die Aruba 6000 Serie.\n\n", text_font=font)
        welcomeLabel3 = ctk.CTkLabel(self, text="Made with       ❤️by Nick von Podewils", text_font=font)
        welcomeButton = ctk.CTkButton(self,text="Start",command=lambda: controller.show_frame("PageOne"))
        dokubutton = ctk.CTkButton(self, text="Dokumentation", command=lambda: StartPage.create_toplevel())

        welcomeLabel.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)
        welcomeLabel2.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
        welcomeButton.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)
        welcomeLabel3.place(relx=0.498, rely=0.952, anchor=tkinter.CENTER)
        dokubutton.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER )

class PageOne(ctk.CTkFrame):

    def get_entry_data(self):
        f = open(r"out.txt","a")
        switchname = self.entry.get()
        f.write("conf\n")
        f.write(f"hostname {switchname}\n")
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
        f.close()
        # ===== prof of concept! =====
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.label = ctk.CTkLabel(self, text="Bitte geben sie den Namen des Switches ein.", text_font=font)
        self.entry = ctk.CTkEntry(self)
        self.label2 = ctk.CTkLabel(self, text="")
        self.button = ctk.CTkButton(self, text="weiter",command=lambda: [controller.show_frame("PageTwo"), PageOne.get_entry_data(self)])
        self.welcomeLabel3 = ctk.CTkLabel(self, text="Made with       ❤️by Nick von Podewils", text_font=font)
        self.progressbar = ctk.CTkProgressBar(self, width=225)

        self.label.pack(anchor="w", padx=5)
        self.entry.pack(anchor="w", padx=5)
        self.label2.pack(anchor="w")
        self.button.pack(anchor="se", padx=5)
        self.progressbar.pack(anchor="center", side=tk.BOTTOM)
        self.welcomeLabel3.pack(anchor="center", side=tk.BOTTOM)
        
        self.progressbar.set(0)

class PageTwo(ctk.CTkFrame):

    def get_entry_data(self):
        f = open(r"out.txt","a")
        global MGMT_VLAN_TAG
        MGMT_VLAN_TAG = self.entry.get()
        f.write(f"vlan {MGMT_VLAN_TAG}\n")
        MGMT_VLAN_DESC = self.entry2.get()
        f.write(f"desc {MGMT_VLAN_DESC}\n")
        f.write(f"name {MGMT_VLAN_DESC}\n")
        MGMT_VLAN_IP = self.entry3.get()
        f.write(f"ip address {MGMT_VLAN_IP}\n")
        f.close()
        
    
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.label = ctk.CTkLabel(self, text="Wie heißt das MGMT-Vlan? (VLAN-Tag)", text_font=font)
        self.entry = ctk.CTkEntry(self)
        self.ph = ctk.CTkLabel(self, text="")
        self.label2 = ctk.CTkLabel(self, text="Wie lauten Name und Beschreibung?", text_font=font)
        self.entry2 = ctk.CTkEntry(self)
        self.ph2 = ctk.CTkLabel(self, text="")
        self.label3 = ctk.CTkLabel(self, text="Wie lautet die IP-Adresse?", text_font=font)
        self.entry3 = ctk.CTkEntry(self)
        self.ph3 = ctk.CTkLabel(self, text="")
        self.button = ctk.CTkButton(self, text="weiter",command=lambda: [controller.show_frame("PageThree"), PageTwo.get_entry_data(self)])
        self.welcomeLabel3 = ctk.CTkLabel(self, text="Made with       ❤️by Nick von Podewils", text_font=font)
        self.progressbar = ctk.CTkProgressBar(self, width=225)
        
        self.label.pack(anchor="w", padx=5)
        self.entry.pack(anchor="w", padx=5)
        self.ph.pack(anchor="w", padx=5)
        self.label2.pack(anchor="w", padx=5)
        self.entry2.pack(anchor="w", padx=5)
        self.ph2.pack(anchor="w", padx=5)
        self.label3.pack(anchor="w", padx=5)
        self.entry3.pack(anchor="w", padx=5)
        self.ph3.pack(anchor="w", padx=5)
        self.button.pack(anchor="se", padx=5)
        self.progressbar.pack(anchor="center", side=tk.BOTTOM)
        self.welcomeLabel3.pack(anchor="center", side=tk.BOTTOM)

        self.progressbar.set(0.15)

class PageThree(ctk.CTkFrame):

    def get_entry_data(self):
        f = open(r"out.txt","a")
        ANZ_PORTS = self.entry.get()
        LISTE_DER_VLAN_ZUGEHÖRIGKEIT_DER_PORTS_STRING = self.entry2.get()
        LISTE_DER_VLAN_ZUGEHÖRIGKEIT_DER_PORTS_ARRAY = LISTE_DER_VLAN_ZUGEHÖRIGKEIT_DER_PORTS_STRING.split(";")
        i = 1
        try:
            while i < int(ANZ_PORTS) + 1:
                #Testet ob Eingabe ein X ist. Falls ja, wird entsprechender Port übersprungen
                if LISTE_DER_VLAN_ZUGEHÖRIGKEIT_DER_PORTS_ARRAY[i-1] == "X":
                    i = i + 1
                    continue
                f.write(f"int 1/1/{i}\n")
                f.write(f"description {LISTE_DER_VLAN_ZUGEHÖRIGKEIT_DER_PORTS_ARRAY[i-1]}\n")
                i = i + 1
        except:
            pass
        f.close()

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.label = ctk.CTkLabel(self, text="Wie viele Ports hat der Switch?", text_font=font)
        self.entry = ctk.CTkEntry(self)
        self.ph = ctk.CTkLabel(self, text="")
        self.label2 = ctk.CTkLabel(self, text="Geben sie nun in aufsteigender Reihenfolge,\nbeim ersten Port beginnend, die Portnamen ein.", text_font=font, height=2)
        self.label22 = ctk.CTkLabel(self, text="Halten sie dabei Folgende form ein:\n    [Portname1];[Portname2];usw...", text_font=font, height=2)
        self.entry2 = ctk.CTkEntry(self)
        self.ph2 = ctk.CTkLabel(self, text="")
        self.button = ctk.CTkButton(self, text="weiter", command=lambda: [controller.show_frame("PageFour"), PageThree.get_entry_data(self)])
        self.welcomeLabel3 = ctk.CTkLabel(self, text="Made with       ❤️by Nick von Podewils", text_font=font)
        self.progressbar = ctk.CTkProgressBar(self, width=225)

        self.label.pack(anchor="w", padx=5)
        self.entry.pack(anchor="w", padx=5)
        self.ph.pack(anchor="w", padx=5)
        self.label2.pack(anchor="w", padx=5)
        self.label22.pack(anchor="w", padx=5)
        self.entry2.pack(anchor="w", padx=5, pady=5)
        self.ph2.pack(anchor="w", padx = 5)
        self.button.pack(anchor="se", padx=5)
        self.progressbar.pack(anchor="center", side=tk.BOTTOM)
        self.welcomeLabel3.pack(anchor="center", side=tk.BOTTOM)

        self.progressbar.set(0.29)

class PageFour(ctk.CTkFrame):

    def get_entry_data(self):
        f = open(r"out.txt","a")
        VLAN = self.entry.get()
        LISTE_PORTS_DIE_ZU_VLAN_GEHOEREN_STRING = self.entry2.get()
        LISTE_PORTS_DIE_ZU_VLAN_GEHOEREN_ARRAY = LISTE_PORTS_DIE_ZU_VLAN_GEHOEREN_STRING.split(";")
        i = 0
        
        try:
            for x in LISTE_PORTS_DIE_ZU_VLAN_GEHOEREN_ARRAY:
                if MGMT_VLAN_TAG != VLAN:
                    f.write(f"int 1/1/{LISTE_PORTS_DIE_ZU_VLAN_GEHOEREN_ARRAY[i]}\n")
                    f.write(f"vlan access {VLAN}\n")
                    i = i + 1
                else:
                    f.write(f"int 1/1/{LISTE_PORTS_DIE_ZU_VLAN_GEHOEREN_ARRAY[i]}\n")
                    f.write(f"vlan trunk {VLAN}\n")
                    i = i + 1
        except:
            pass

        self.entry.delete(0, tk.END)
        self.entry2.delete(0, tk.END)
        f.close()

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.label = ctk.CTkLabel(self, text="Welchem Vlan wollen sie Ports zuweisen?", text_font=font)
        self.entry = ctk.CTkEntry(self)
        self.ph = ctk.CTkLabel(self, text="")
        self.label2 = ctk.CTkLabel(self, text="Bitte geben sie alle Ports an,\ndie zu diesem VLAN gehören.\nSeparieren sie die Portnummern mit \";\".\nBeachten sie, dass sie nicht \ndas MGMT-VLAN eingeben.", text_font=font)
        self.entry2 = ctk.CTkEntry(self)
        self.ph3 = ctk.CTkLabel(self, text="")
        self.button1 = ctk.CTkButton(self, text="neues Vlan", command=lambda: PageFour.get_entry_data(self))
        self.ph2 = ctk.CTkLabel(self, text="")
        self.button2 = ctk.CTkButton(self, text="weiter", command=lambda: [controller.show_frame("PageFive"), PageFour.get_entry_data(self)])
        self.welcomeLabel3 = ctk.CTkLabel(self, text="Made with       ❤️by Nick von Podewils", text_font=font)
        self.progressbar = ctk.CTkProgressBar(self, width=225)

        self.label.pack(anchor="w", padx=5)
        self.entry.pack(anchor="w", padx=5)
        self.ph.pack(anchor="w", padx=5)
        self.label2.pack(anchor="w", padx=5)
        self.entry2.pack(anchor="w", padx=5, pady=5)
        self.ph3.pack()
        self.button1.pack(anchor="se", padx=5)
        self.ph2.pack()
        self.button2.pack(anchor="se", padx=5)
        self.progressbar.pack(anchor="center", side=tk.BOTTOM)
        self.welcomeLabel3.pack(anchor="center", side=tk.BOTTOM)

        self.progressbar.set(0.44)

class PageFive(ctk.CTkFrame):

    def get_entry_data(self):
        f = open(r"out.txt","a")
        try:
            TRUNK_PORT = self.entry.get()
            f.write(f"int 1/1/{TRUNK_PORT}\n")
            TRUNK_PORT_ZUGRIFFS_PORTS_STRING = self.entry2.get()
            TRUNK_PORT_ZUGRIFFS_PORTS_STRING = TRUNK_PORT_ZUGRIFFS_PORTS_STRING.replace(";",",")
            f.write(f"vlan trunk allowed {TRUNK_PORT_ZUGRIFFS_PORTS_STRING}\n")
        except:
            pass
        self.entry.delete(0, tk.END)
        self.entry2.delete(0, tk.END)
        f.close()

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.label = ctk.CTkLabel(self, text="Wie lautet der Trunkport?", text_font=font)
        self.entry = ctk.CTkEntry(self)
        self.ph = ctk.CTkLabel(self, text="")
        self.label2 = ctk.CTkLabel(self, text="Bitte geben sie alle VLANS,\ndie auf diesen Port zugreifen ein.Separieren\n sie bei mehreren VLANs mit dem ;", text_font=font)
        self.entry2 = ctk.CTkEntry(self)
        self.ph2 = ctk.CTkLabel(self, text="")
        self.button = ctk.CTkButton(self, text="neuer Trunk", command=lambda: PageFive.get_entry_data(self))
        self.ph3 = ctk.CTkLabel(self, text="")
        self.button2 = ctk.CTkButton(self, text="weiter", command=lambda: [controller.show_frame("PageSix"), PageFive.get_entry_data(self)])
        self.welcomeLabel3 = ctk.CTkLabel(self, text="Made with       ❤️by Nick von Podewils", text_font=font)
        self.progressbar = ctk.CTkProgressBar(self, width=225)

        self.label.pack(anchor="w", padx=5)
        self.entry.pack(anchor="w", padx=5)
        self.ph.pack()
        self.label2.pack(anchor="w", padx=5)
        self.entry2.pack(anchor="w", padx=5)
        self.ph2.pack()
        self.button.pack(anchor="se", padx=5)
        self.ph3.pack()
        self.button2.pack(anchor="se", padx=5)
        self.progressbar.pack(anchor="center", side=tk.BOTTOM)
        self.welcomeLabel3.pack(anchor="center", side=tk.BOTTOM)

        self.progressbar.set(0.58)

class PageSix(ctk.CTkFrame):

    def get_entry_data(self):
        f = open(r"out.txt","a")
        try:
            GATEWAY = self.entry.get()
            IP_NTP = self.entry2.get()
            f.write(f"ip route 0.0.0.0/0 {GATEWAY}\n")
            f.write("aruba-central\n")
            f.write("disable\n")
            f.write("no ntp server pool.ntp.org\n")
            f.write(f"ntp server {IP_NTP}\n")
        except:
            pass
        f.close()

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.label = ctk.CTkLabel(self, text="Wie lautet das Gateway?", text_font=font)
        self.entry = ctk.CTkEntry(self)
        self.ph = ctk.CTkLabel(self, text="")
        self.label2 = ctk.CTkLabel(self, text="Wie lautet die IP-Adresse ihres NTP-Servers?", text_font=font)
        self.entry2 = ctk.CTkEntry(self)
        self.ph2 = ctk.CTkLabel(self, text="")
        self.button = ctk.CTkButton(self, text="weiter", command=lambda: [controller.show_frame("PageSeven"), PageSix.get_entry_data(self)])
        self.welcomeLabel3 = ctk.CTkLabel(self, text="Made with       ❤️by Nick von Podewils", text_font=("Roboto Medium", -12))
        self.progressbar = ctk.CTkProgressBar(self, width=225)

        self.label.pack(anchor="w", padx=5)
        self.entry.pack(anchor="w", padx=5)
        self.ph.pack(anchor="w", padx=5)
        self.label2.pack(anchor="w", padx=5)
        self.entry2.pack(anchor="w", padx=5)
        self.ph2.pack()
        self.button.pack(anchor="se", padx=5)
        self.progressbar.pack(anchor="center", side=tk.BOTTOM)
        self.welcomeLabel3.pack(anchor="center", side=tk.BOTTOM)

        self.progressbar.set(0.73)

class PageSeven(ctk.CTkFrame):

    def get_entry_data(self):
        f = open(r"out.txt","a")
        try:
            
            USERNAME = self.entry.get()
            USERPW = self.entry2.get()
            USERGROUP = self.dropdown.get()
            f.write(f"user {USERNAME} group {USERGROUP} password plaintext {USERPW}\n")

        except:
            pass
        self.entry.delete(0, tk.END)
        self.entry2.delete(0, tk.END)
        f.close()

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        #mit button label, und zwei entrys für user hinzufügen
        self.dropdown = ctk.CTkOptionMenu(self, values=["Administrators","Operators"])
        self.ph5 = ctk.CTkLabel(self, text="")
        self.label = ctk.CTkLabel(self, text="Username:", text_font=("Roboto Medium", -12))
        self.entry = ctk.CTkEntry(self)
        self.ph = ctk.CTkLabel(self, text="")
        self.label2 = ctk.CTkLabel(self, text="Password", text_font=("Roboto Medium", -12))
        self.entry2 = ctk.CTkEntry(self)
        self.ph2 = ctk.CTkLabel(self, text="")
        self.button = ctk.CTkButton(self, text="User hinzufügen", command=lambda: PageSeven.get_entry_data(self))
        self.ph3 = ctk.CTkLabel(self, text="")
        self.button2 = ctk.CTkButton(self, text="weiter", command=lambda: [controller.show_frame("PageAight"), PageSeven.get_entry_data(self)])
        # ===== Hier muss eine schleife eingabeaut werden
        self.welcomeLabel3 = ctk.CTkLabel(self, text="Made with       ❤️by Nick von Podewils", text_font=("Roboto Medium", -12))
        self.progressbar = ctk.CTkProgressBar(self, width=225)

        self.dropdown.pack(anchor="w", padx=5, pady=5)
        self.ph5.pack(anchor="w")
        self.label.pack(anchor="w", padx=5)
        self.entry.pack(anchor="w", padx=5)
        self.ph.pack(anchor="w", padx=5)
        self.label2.pack(anchor="w", padx=5)
        self.entry2.pack(anchor="w", padx=5)
        self.ph2.pack(anchor="w", padx=5)
        self.button.pack(anchor="se", padx=5)
        self.ph3.pack()
        self.button2.pack(anchor="se", padx=5)
        self.progressbar.pack(anchor="center", side=tk.BOTTOM)
        self.welcomeLabel3.pack(anchor="center", side=tk.BOTTOM)
        
        self.progressbar.set(0.89)

class PageAight(ctk.CTkFrame):

    def show_out_txt(self):
        txt_f = open(r"out.txt","r")
        txt = txt_f.read()
        txt_f.close()
        try:
            self.label.pack_forget()
        except:
            pass
        self.label = tk.Text(self)
        self.label.insert("1.0",txt)
        self.label.pack(padx=5, pady=5)
        txt_f.close()

    def copy_to_clip(self):
        txt_f = open(r"out.txt","r")
        txt = txt_f.read()
        txt_f.close()
        self.clipboard_clear()
        self.clipboard_append(txt)
        self.update()

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.button = ctk.CTkButton(self, text="Befehle anzeigen", command=lambda:[PageAight.show_out_txt(self)])
        self.button.pack(anchor="s", padx=5, pady=5)
        self.button2 = ctk.CTkButton(self, text="Copy to Clipboard", command=lambda: PageAight.copy_to_clip(self))
        self.button2.pack(anchor="s", padx=5, pady=5)
        self.welcomeLabel3 = ctk.CTkLabel(self, text="Made with       ❤️by Nick von Podewils", text_font=("Roboto Medium", -12))
        self.progressbar = ctk.CTkProgressBar(self, width=225)
        self.progressbar.pack(anchor="center", side=tk.BOTTOM)
        self.progressbar.set(1)
        self.welcomeLabel3.pack(anchor="center", side=tk.BOTTOM)

if __name__ == "__main__":
    am = "System"
    ct = "green"
    app = App(am, ct)
    app.mainloop()