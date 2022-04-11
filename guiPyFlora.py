###################################################
from tkinter import *                              
from tkinter import ttk
from PIL import Image, ImageTk                     
from tkinter.messagebox import askyesno, showwarning
from tkinter import filedialog
from io import BytesIO
from baze import query_handle as qb
from datetime import datetime as dt
from random import randint as rnd 
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import sqlite3
from baze import query_admin as adq
import os
######################################################

class guiFlora():
    def __init__(self, r) -> None:
        ###  root  ###
        self.r = r
        self.r.resizable(False, False)

        ###  style  ###
        self.style = ttk.Style(self.r)
        self.style.theme_names()

        ###  administracija.db  ###
        self.db_admin = 'baze\\administracija.db'
        self.tb_admin = 'administracija'


        ##   pybiljke.db   ##
        self.db_posude = 'baze\\pyFlora.db'
        self.tb_biljke = 'pybiljke'
        self.tb_posude = 'pyposude'
        self.tb_senzori = 'pynjega'
        self.tb_povezano = 'konekcija'

        ###  datetime  ###
        self.datetime = dt.now().strftime('%d.%m.%Y. %H:%M:%S')
        print(self.datetime)

        ### lists  ###
        self.lst_biljka_zalijevanje = ['Dnevno', 'Tjedno', 'Mjesecno']
        self.lst_biljka_svjetlost = ['Jarko', 'Sjenovito', 'Tamno']
        self.lst_biljka_toplina = ['Toplija', 'Umjerena', 'Hladnija']
        self.lst_biljke = []
        self.lst_plant_names = []
        self.lst_pot_names = []
        self.lst_frms_p = []
        self.lst_frms_b = []


        ###  color style  ###
        self.bgc = '#D3E4CD'
        self.stycolor = '#ADC2A9'
        self.styhover = '#FEF5ED'
        self.fgc = '#FEF5ED'
        self.fgh ='#99A799'

        ###  OKVIRI  ###
        # root frames
        self.fr_login = Frame (self.r, bg=self.bgc)
        self.fr_login.place(x=5, y=5)
        self.fr_admin = Frame (self.r, bg=self.bgc)
        self.fr_biljke = Frame (self.r, bg=self.bgc)
        self.fr_posude = Frame (self.r, bg=self.bgc)

        # root frames ažuriranje
        self.fread_biljke = Frame (self.r, background=self.bgc)
        self.frnew_biljke = Frame (self.r, background=self.bgc)
        self.frnew_posude = Frame (self.r, background=self.bgc)


        ### Scrollbar frames  ###
        self.cnv_biljke = Canvas (self.fr_biljke, background=self.bgc, highlightthickness=0, height=350, width=680)
        self.scroll_biljke = Scrollbar(self.fr_biljke, orient="vertical", 
                                background=self.stycolor,
                                activebackground=self.fgc,
                                relief='flat',
                                activerelief='flat',
                                command=self.cnv_biljke.yview)
        self.frs_biljke = Frame (self.cnv_biljke, background=self.bgc, highlightthickness=0)

        self.frs_biljke.bind("<Configure>",
                            lambda e: self.cnv_biljke.configure(
                            scrollregion=self.cnv_biljke.bbox("all")))
        self.frs_biljke.bind_all('<MouseWheel>', self.OnMouseWheel)

        self.cnv_biljke.create_window((0,0), anchor='nw', window=self.frs_biljke)
        self.cnv_biljke.configure(yscrollcommand=self.scroll_biljke.set)

        self.cnv_biljke.grid(column=0, row=0, columnspan=2, padx=10, pady=5, sticky='nw')

        self.cnv_posude = Canvas (self.fr_posude, background=self.bgc, highlightthickness=0, height=350, width=680)
        self.scroll_posude = Scrollbar(self.fr_posude, orient="vertical", 
                                background=self.stycolor,
                                activebackground=self.fgc,
                                relief='flat',
                                activerelief='flat',
                                command=self.cnv_posude.yview)
        self.frs_posude = Frame (self.cnv_posude, background=self.bgc, highlightthickness=0)

        self.frs_posude.bind("<Configure>",
                            lambda e: self.cnv_posude.configure(
                            scrollregion=self.cnv_posude.bbox("all")))
        self.frs_posude.bind_all('<MouseWheel>', self.OnMouseWheel)

        self.cnv_posude.create_window((0,0), anchor='nw', window=self.frs_posude)
        self.cnv_posude.configure(yscrollcommand=self.scroll_posude.set)

        self.cnv_posude.grid(column=0, row=0, columnspan=2, padx=10, pady=5, sticky='nw')

        self.cnv_plot = Canvas (self.frnew_posude, width=680, height=195)

        # admin frames
        self.fr_head = Frame (self.r, bg=self.stycolor)
        self.frm_liste = Frame(self.fr_admin, background=self.stycolor, height=350, width=250)

        ###  list box  ###
        self.lstbx_plant = Listbox (self.frm_liste, bg=self.fgc, fg=self.stycolor, 
                                selectbackground=self.bgc,
                                relief='flat', height=10, width=15,
                                activestyle='none', justify='center',
                                font=('Euphemia', 10))


        self.lstbx_pot = Listbox (self.frm_liste, bg=self.fgc, fg=self.stycolor, 
                                selectbackground=self.bgc,
                                relief='flat', height=10, width=15,
                                activestyle='none', justify='center',
                                font=('Euphemia', 10))

        ###  IKONE PROGRAMA  ###
        #  image open  
        self.logo_open = Image.open("photo\\pylogo.png")
        self.logo_bg_open = Image.open("photo\\logo_bg.png")
        self.avatar_open = Image.open("photo\\user-286.png")
        self.biljke_naslov = Image.open("photo\\biljke_naslov.png")
        self.mojprofil_naslov = Image.open("photo\\mojprofil_naslov.png")
        self.pyposude_naslov = Image.open("photo\\pyposude_naslov.png")
        self.empty_pot = Image.open("biljke\\empty_pot.png")
        self.add_new = Image.open("photo\\add_new.png")
        self.add_temperature = Image.open("photo\\add_temperature.png")
        self.reduce_sunlight2 = Image.open("photo\\reduce_sunlight2.png")
        self.reduce_temperature = Image.open("photo\\reduce_temperature.png")
        self.sunlight2 = Image.open("photo\\sunlight2.png")
        self.suplement = Image.open("photo\\suplement.jpg")
        self.watering = Image.open("photo\\watering2.png")
        self.status_ok = Image.open("photo\\ok.png")
        
        # icons
        self.logo_img = ImageTk.PhotoImage(self.logo_open.resize((150, 150), Image.ANTIALIAS))
        self.bg_logo = ImageTk.PhotoImage(self.logo_bg_open.resize((100, 150), Image.ANTIALIAS))
        self.avatar_img = ImageTk.PhotoImage(self.avatar_open.resize((40, 30), Image.ANTIALIAS))
        self.biljke_naslov_img = ImageTk.PhotoImage(self.biljke_naslov.resize((150, 40), Image.ANTIALIAS))
        self.mojprofil_naslov_img = ImageTk.PhotoImage(self.mojprofil_naslov.resize((170, 40), Image.ANTIALIAS))
        self.pyposude_naslov_img = ImageTk.PhotoImage(self.pyposude_naslov.resize((170, 40), Image.ANTIALIAS))
        self.add_new_img = ImageTk.PhotoImage(self.add_new.resize((50, 50), Image.ANTIALIAS))
        self.img_watering = ImageTk.PhotoImage(self.watering.resize((35, 30), Image.ANTIALIAS))
        self.img_suplement = ImageTk.PhotoImage(self.suplement.resize((40, 40), Image.ANTIALIAS))
        self.img_sunlight = ImageTk.PhotoImage(self.sunlight2.resize((40, 40), Image.ANTIALIAS))
        self.img_reduce_temperature = ImageTk.PhotoImage(self.reduce_temperature.resize((30, 30), Image.ANTIALIAS))
        self.img_reduce_sunlight = ImageTk.PhotoImage(self.reduce_sunlight2.resize((40, 40), Image.ANTIALIAS))
        self.img_add_temperature = ImageTk.PhotoImage(self.add_temperature.resize((25, 30), Image.ANTIALIAS))
        self.img_ok = ImageTk.PhotoImage(self.status_ok.resize((30, 30), Image.ANTIALIAS))
        self.img_empty = ImageTk.PhotoImage(self.empty_pot.resize((100, 100), Image.ANTIALIAS))


        ###  LABELS  ###
        # labels login ekrana
        self.lbl_logo = Label (self.fr_login, 
            image=self.logo_img,
            borderwidth=0)

        self.lbl_pogreska = Label (self.fr_login,
            text='Korisnicko ime', 
            bg=self.bgc, 
            foreground=self.fgh)

        self.lbl_pass = Label (self.fr_login,
            text='Lozinka',
            bg=self.bgc,
            foreground=self.fgh)
        
        self.lbl_log = Label (text='Korisnicko ime',
            bg=self.bgc, 
            fg=self.fgh)

        self.lbl_admin_name = Label (self.fr_admin, 
            text='proba', 
            background=self.stycolor, 
            foreground=self.fgc, 
            font=('Euphemia', 12, 'bold'),
            justify='center') 

        self.lbl_bg_logo = Label(self.fr_admin, 
            image=self.bg_logo, 
            background=self.bgc)         

        ## Label - naslovi
        self.lbl_naslov = Label(self.fr_head, image=self.mojprofil_naslov_img, borderwidth=0)
        self.lbl_naslov.place(x=270, y=5)

        ## Label - naslov za unos u bazu
        self.lbl_title_new = ttk.Label (self.frnew_biljke, 
                        background=self.bgc, 
                        foreground=self.fgh,
                        text='', 
                        font= ('Euphemia', 12, 'bold'))
        self.lbl_titlep_new = ttk.Label (self.frnew_posude, 
                        background=self.bgc, 
                        foreground=self.fgh,
                        text='', 
                        font= ('Euphemia', 12, 'bold'))

        ## Label posude
        self.lbl_pot_name = ttk.Label (self.frnew_posude, 
                    text='Unesi ime posude: ', 
                    background=self.bgc, 
                    foreground=self.fgh,
                    font=('Helvetica', 10))

        self.lbl_prazno = ttk.Label (self.frnew_posude, 
                    text='Sadnica: ', 
                    background=self.bgc, 
                    foreground=self.fgh,
                    font=('Helvetica', 10))

        self.lbl_biljka  = ttk.Label (self.frnew_posude, 
                    text='Odaberi sadnicu: ', 
                    background=self.bgc, 
                    foreground=self.fgh,
                    font=('Helvetica', 10))

        self.lbl_values = ttk.Label (self.frnew_posude, 
                        image='', 
                        background=self.stycolor, 
                        foreground=self.fgc, 
                        font=('Helvetica', '10'))
        self.lbl_empty = ttk.Label (self.frnew_posude, 
                        image='', 
                        background=self.stycolor, 
                        foreground=self.fgc, 
                        font=('Helvetica', '10'))

        
        ### choice boxes ###
        self.var_zalijevanje = StringVar()
        self.ch_zalijevanje = ttk.OptionMenu(self.frnew_biljke, 
                                self.var_zalijevanje,
                                'Odaberi',
                                *self.lst_biljka_zalijevanje)

        self.var_svjetlost = StringVar()
        self.ch_svjetlost = ttk.OptionMenu(self.frnew_biljke, 
                                self.var_svjetlost,
                                'Odaberi',
                                *self.lst_biljka_svjetlost)

        self.var_temperatura = StringVar()
        self.ch_temperatura = ttk.OptionMenu(self.frnew_biljke, 
                                self.var_temperatura,
                                'Odaberi',
                                *self.lst_biljka_toplina)

        
        self.rows_biljke= qb.select_all(self.db_posude, self.tb_biljke, 'naziv_biljke')
        for biljka in self.rows_biljke:
            if biljka not in self.lst_biljke:
                self.lst_biljke.append(biljka[0])
     
        self.var_baza_biljka = StringVar()
        self.ch_baza_biljka = ttk.OptionMenu(self.frnew_posude, 
                                self.var_baza_biljka,
                                'Odaberi',
                                *self.lst_biljke)
        self.var_baza_biljka.trace('w', self.option_select)

        ###  checkbutton  ###
        self.boolvar_biljke = BooleanVar()
        self.boolvar_biljke.set(False) 

        self.cb_dohrana = Checkbutton(self.frnew_biljke, 
                            background=self.bgc, 
                            activeforeground=self.fgc, 
                            variable = self.boolvar_biljke,
                            command=lambda: guiFlora.get_cb_value(self, self.boolvar_biljke),
                            relief='flat')
        self.cb_dohrana.var = self.boolvar_biljke

        self.boolvar_posude = BooleanVar()
        self.boolvar_posude.set(False) 
        
        self.cb_posadeno = Checkbutton(self.frnew_posude, 
                            background=self.bgc, 
                            activeforeground=self.fgc, 
                            variable = self.boolvar_posude,
                            command=lambda: guiFlora.get_cb_value(self, self.boolvar_posude),
                            relief='flat')
        self.cb_posadeno.var = self.boolvar_posude

        ###  ENTRY  ###
        ## entry login ekran
        self.ent_name = Entry (self.fr_login,
            background=self.styhover,
            foreground=self.fgh,
            relief='flat')

        self.ent_pass = Entry (self.fr_login,
            background=self.styhover,
            foreground=self.fgh,
            show='*',
            relief='flat')

        ## entry ime biljke
        self.ent_plant_name = Entry (self.frnew_biljke,
            background=self.styhover,
            foreground=self.fgh,
            relief='flat',
            width=30)

        ## entry path datoteke iz baze
        self.ent_path = Entry (self.frnew_biljke,
            background=self.fgh,
            foreground=self.fgc,
            relief='flat',
            width=30)

        ## entry ime posude
        self.ent_pot_name = Entry (self.frnew_posude,
            background=self.styhover,
            foreground=self.fgh,
            relief='flat',
            width=30)

        ### text ###
        self.txt_opis = Text (self.frnew_biljke,
                            background=self.bgc,
                            foreground=self.fgh,
                            height=10,
                            width=75)

        ###  BUTTONS  ###
        self.btn_log = Button (self.fr_login,
            text='Log in', 
            bg=self.stycolor, 
            relief='flat', 
            fg=self.fgc,
            activeforeground=self.fgh,
            activebackground=self.styhover,
            pady=5,
            padx=95,
            command= self.log_command)

        self.btn_see = Button(self.frm_liste, bg=self.bgc, text='Pogledaj', fg=self.fgh, 
                            relief='flat', height=2, width=31, activebackground=self.fgh,
                            activeforeground=self.fgc, command=lambda: Admin.see_base(self))

        self.btn_return = Button (self.r,
            text='Izlaz', 
            bg=self.stycolor, 
            relief='flat', 
            fg=self.fgc,
            activeforeground=self.fgh,
            activebackground=self.styhover,
            pady=5,
            padx=40,
            command=lambda:guiFlora.izlazak_iz_admimnistracije(self))

        self.btn_pofil_posuda = Button (self.fr_head,
            text='PyPosude',
            font=('Helvetica', '11', 'bold'), 
            bg=self.stycolor, 
            relief='flat', 
            fg=self.fgc,
            activeforeground=self.fgh,
            activebackground=self.styhover,
            pady=5,
            padx=130,
            command=lambda:Admin.view_pots(self))

        self.btn_profil_biljke = Button (self.fr_head,
            text='Biljke',
            font=('Helvetica', '11', 'bold'),  
            bg=self.stycolor, 
            relief='flat', 
            fg=self.fgc,
            activeforeground=self.fgh,
            activebackground=self.styhover,
            pady=5,
            padx=95,
            command=lambda:Admin.view_plants(self))

        self.btn_moj_profil = Button (self.fr_head,
            text='Moj Profil', 
            image= self.avatar_img,
            bg=self.stycolor, 
            relief='flat', 
            fg=self.fgc,
            activeforeground=self.fgh,
            activebackground=self.styhover,
            pady=5,
            padx=95,
            command=lambda:Admin.view_admin(self))
        
        self.btn_upload = Button (self.frnew_biljke,
                background=self.stycolor,
                image=self.add_new_img,
                relief='flat',
                height=120,
                width=90,
                command=lambda: Admin.upload_img(self))
        
        self.btn_addfile = Button (self.frnew_biljke,
                background=self.stycolor,
                foreground=self.fgc,
                activebackground=self.bgc,
                activeforeground=self.fgh,
                text='Odaberi folder',
                relief='flat',
                command=lambda: [self.ent_path.delete(0, END), Admin.upload_file(self)])
        self.btn_save = Button (self.r,
            text='Spremi', 
            bg=self.stycolor, 
            relief='flat', 
            fg=self.fgc,
            activeforeground=self.fgh,
            activebackground=self.styhover,
            pady=5,
            padx=40)

        self.btn_sync = Button (self.r,
            background=self.stycolor,
            foreground=self.fgc,
            activebackground=self.bgc,
            activeforeground=self.fgh,
            text='Ocitaj',
            compound='top',
            relief='flat',
            pady=5,
            padx=40,
            command=lambda: Admin.sync_measuring(self))

        self.btn_update_pot = Button (self.frnew_posude,
            text='Azuriraj', 
            bg=self.stycolor, 
            relief='flat', 
            fg=self.fgc,
            activeforeground=self.fgh,
            activebackground=self.styhover,
            pady=5,
            padx=40,
            command= lambda: Admin.update_pot_data(self))
        
        self.btn_delete_pot = Button (self.frnew_posude,
            text='Obrisi', 
            bg=self.stycolor, 
            relief='flat', 
            fg=self.fgc,
            activeforeground=self.fgh,
            activebackground=self.styhover,
            pady=5,
            padx=40)
            
        self.btn_delete_plant= Button (self.frnew_biljke, 
            text='Obrisi', 
            bg=self.stycolor, fg=self.fgc, 
            relief='flat',
            command=lambda:Admin.delete_plant(self),
            width=11, height=2)

    def get_cb_value(self, boolvar):
        ''' Ova funkcija uzima string vrijednost Checkbuttona '''
        # print(boolvar.get())
        
        if self.boolvar_posude.get() == False:
            self.ch_baza_biljka.configure(state=DISABLED)
        else:
            self.ch_baza_biljka.configure(state=NORMAL)

    def update_option_menu(self):
        ''' Ova funkcija unosi podatke svih biljaka iz baze u Optionmenu '''
        menu = self.ch_baza_biljka["menu"]
        menu.delete(0, "end")
        for string in self.lst_biljke:
            menu.add_command(label=string, 
                             command=lambda value=string: self.var_baza_biljka.set(value))

    def option_select(self, *args):
        ''' Ova funkcija vraca string odabrane biljke iz Optionmenu-a '''
        print (self.var_baza_biljka.get())

    def OnMouseWheel(self,event):
        ''' Ova funkcija bind-a scroll-anja s kotacicem misa '''
        self.cnv_biljke.yview("scroll",int(-1*(event.delta/120)),"units")
        self.cnv_posude.yview("scroll",int(-1*(event.delta/120)),"units")
        return "break"

    def login_window(self):
        ''' Ova funkcija otvara pocetni LOGIN EKRAN '''
        guiFlora.forget_placing(self)

        self.r.geometry('425x500')
        self.r.title('Py Flora')
        self.r.configure(bg=self.bgc)

        ### frame placing  ###
        self.fr_login.place(width=420, height=400, x=5, y=5)
        ##  logo
        self.lbl_logo.place(x=140, y=10)
        ##  name
        self.lbl_pogreska.place(x=100, y=200)
        self.ent_name.place(x=200, y=200)
        ## pass
        self.lbl_pass.place(x=100, y=230)
        self.ent_pass.place(x=200, y=230)
        ## button
        self.btn_log.place(x=100, y=300)
        ### run program  ###
        self.r.mainloop()

    def izlazak_iz_admimnistracije(self):
        ''' Ova funkcija zatvara aplikaciju i vraca Login ekran '''
        guiFlora.confirm(self)
        
    def confirm(self):
        ''' Ova funkcija potvrduje izlazak iz aplikacije '''
        answer = askyesno(title='Potvrdi izlazak',
                          message='Zelite li izaci iz administracije?')
        if answer:
            guiFlora.forget_placing(self)
            guiFlora.login_window(self)


    def forget_placing(self):
        ''' Ova funkcija brise sve postojece ekrane i vraca postavke okvira na pocetno stanje '''
        self.lbl_log.place_forget()
        self.fr_login.place_forget()
        self.fr_admin.place_forget()
        self.ent_name.delete(0, END)
        self.ent_pass.delete(0, END)
        self.ent_name.focus()
        self.fr_biljke.place_forget()
        self.fr_posude.place_forget()
        self.fr_head.place_forget()
        self.btn_return.place_forget()
        self.fread_biljke.place_forget()
        self.frnew_biljke.place_forget()
        self.btn_save.place_forget()
        self.frnew_posude.place_forget()
        self.btn_sync.place_forget()
        self.lbl_empty.place_forget()

    def log_command(self):
        ''' Ova funkcija priprema podatke za administracijski okvir '''
        rows = qb.select_all(self.db_admin, self.tb_admin, 'korisnicko_ime')
        for row in rows:
            if self.ent_name.get() == row[0] and self.ent_pass.get() == row[1]:
                Admin.view_admin(self)
                self.lbl_admin_name.configure(text=f'Dobrodosli {row[2]} {row[3]}')

            else:
                self.lbl_log.configure(text='Pogresan unos, pokusajte ponovo') 
                self.ent_name.delete(0, END)
                self.ent_pass.delete(0, END)
                self.ent_name.focus()
                self.lbl_log.place(x=120, y=400)

class Admin(guiFlora):
    def __init__(self, r) -> None:
        super().__init__(r)

    ### ADMINISTRACIJA  ###
    def view_admin(self):
        '''' Ova funkcija prikazuje profil administratora '''
        self.forget_placing()
        self.r.geometry('700x500')
        self.fr_admin.place(x=0, y=0, width=700, height=500)
        self.btn_return.place(x=5, y=460, width=690)
        self.fr_head.place(x=0, y=0,height=50, width=700)
        self.btn_pofil_posuda.place(x=130, y=10, width=80)
        self.btn_profil_biljke.place(x=45, y=10, width=50)
        self.btn_moj_profil.place(x=630,y=10)
        self.lbl_naslov.configure(image=self.mojprofil_naslov_img)
        self.lbl_admin_name.place(x=300, y=60, width=350, height=50)
        self.lstbx_plant.delete(0, END)
        self.lstbx_pot.delete(0, END)

        self.frm_liste.place(x=10, y=60)
        self.lbl_bg_logo.place(x=300, y =130)

        btn_add = Button (self.frm_liste,
                background=self.stycolor,
                foreground=self.fgc,
                activebackground=self.bgc,
                activeforeground=self.fgh,
                image=self.add_new_img,
                text='\nDodaj novu biljku',
                compound='top',
                relief='flat',
                command=lambda: Admin.add_new_plant(self))
        btn_add.place(x=10, y=10)

        btn_add_pot = Button (self.frm_liste,
                background=self.stycolor,
                foreground=self.fgc,
                activebackground=self.bgc,
                activeforeground=self.fgh,
                image=self.add_new_img,
                text='\nDodaj novu posudu',
                compound='top',
                relief='flat',
                command=lambda: Admin.add_new_pot(self))
        btn_add_pot.place(x=130, y=10)

        self.lstbx_plant.place(x=10, y=110)

        plants = qb.select_all(self.db_posude, self.tb_biljke, 'naziv_biljke')
        plant_names = []
        for pl in plants:
            plant_names.append(pl[0])
            self.lstbx_plant.insert(END, pl[0])


        self.btn_see.place(x=12, y=300)

        self.lstbx_pot.place(x=130, y=110)

        pots = qb.select_all(self.db_posude, self.tb_posude, 'naziv_posude')
        pot_names = []
        for pt in pots:
            pot_names.append(pt[0])
            self.lstbx_pot.insert(END, pt[0])


        self.btn_sync.configure(command=lambda: [Admin.sync_measuring(self), Admin.view_admin(self)])

        self.btn_sync.place(x=5, y=420, width=690)

        lbl_name  = Label (self.fr_admin, text='Ime:', 
                            background=self.bgc,
                            foreground=self.fgh, 
                            font=('Euphemia', 12, 'bold'))
        lbl_name.place(x=410, y=130)
        
        str_name = StringVar()
        ent_name = Entry (self.fr_admin, width=16,
                            background=self.fgc, 
                            foreground=self.fgh, 
                            relief='flat', textvariable=str_name, font=('Euphemia', 12, 'bold'))
        ent_name.place(x=500, y=130)

        lbl_sur  = Label (self.fr_admin, text='Prezime:', 
                            background=self.bgc,
                            foreground=self.fgh, 
                            font=('Euphemia', 12, 'bold'))
        lbl_sur.place(x=410, y=160)
        
        str_sur = StringVar()
        ent_sur = Entry (self.fr_admin, width=16,
                            background=self.fgc, 
                            foreground=self.fgh, 
                            relief='flat', textvariable=str_sur, font=('Euphemia', 12, 'bold'))
        ent_sur.place(x=500, y=160)

        lbl_user  = Label (self.fr_admin, text='Korisnik:', 
                            background=self.bgc,
                            foreground=self.fgh, 
                            font=('Euphemia', 12, 'bold'))
        lbl_user.place(x=410, y=190)
        
        str_user = StringVar()
        ent_user = Entry (self.fr_admin, width=16,
                            background=self.fgc, 
                            foreground=self.fgh, 
                            relief='flat', textvariable=str_user, font=('Euphemia', 12, 'bold'))
        ent_user.place(x=500, y=190)

        lbl_pass  = Label (self.fr_admin, text='Lozinka:', 
                            background=self.bgc,
                            foreground=self.fgh, 
                            font=('Euphemia', 12, 'bold'))
        lbl_pass.place(x=410, y=220)
        
        str_pass = StringVar()
        ent_pass = Entry (self.fr_admin, width=16,
                            background=self.fgc, 
                            foreground=self.fgh,
                            show = '*', 
                            relief='flat', textvariable=str_pass, font=('Euphemia', 12, 'bold'))
        ent_pass.place(x=500, y=220)

        admin_data = qb.select_all(self.db_admin, self.tb_admin, 'korisnicko_ime')
        for ad in admin_data:
            ent_name.insert(END, ad[2])
            ent_sur.insert(END, ad[3])
            ent_user.insert(END, ad[0])
            ent_pass.insert(END, ad[1])
        
        btn_ad_update = Button(self.fr_admin, bg=self.stycolor, text='Azuriraj', fg=self.fgc, 
                            relief='flat', height=1, width=20, activebackground=self.fgh,
                            activeforeground=self.fgc, command=lambda: [adq.update_korisnik(self.db_admin, ad[0], str(ent_user.get()), str(ent_pass.get()), str(ent_name.get()), str(ent_sur.get())), Admin.view_admin(self)])
        btn_ad_update.place(x=500, y=250)
        self.lbl_admin_name.configure(text=f'Dobrodosli {ad[2]} {ad[3]}')

    def see_base(self):
        ''' Ova funkcija povezuje gumb prikazi s vrijednostima na listboxima '''
        if self.lstbx_plant.curselection():
            Admin.plant_update(self,self.lstbx_plant.get(ANCHOR))
        elif self.lstbx_pot.curselection():
            Admin.pot_update(self,self.lstbx_pot.get(ANCHOR))
        else:
            print('Niste oznacili listu!') 

    ### BILJKE ###        
    def view_list(self, database, table, frame):
        '''' Ova funkcija stvara okvire za prikaz baze biljaka i baze posuda '''
        
        frm_new = Frame(frame, background=self.stycolor, highlightthickness=2, highlightcolor=self.fgc, height=155, width=290)
        lbl_new = ttk.Label(frm_new, 
                    background=self.stycolor, 
                    foreground=self.fgc, 
                    text='DODAJ NOVU BILJKU',
                    font=('Helvetica', '12', 'bold' ))
        lbl_new.place(x=60,y=15)
        btn_new = Button (frm_new, 
                    background=self.stycolor, 
                    foreground=self.fgc,
                    image=self.add_new_img,
                    relief='flat')
        btn_new.place(x=120, y=60)
        frm_new.grid(column=0, row=0, padx=20, pady=10)

        if table == self.tb_posude:
            lbl_new.configure(text='DODAJ NOVU POSUDU')
            btn_new.configure(command=lambda: Admin.add_new_pot(self))
            rows = qb.select_all(database, table, 'naziv_posude')
            lst_frms = self.lst_frms_p
            lst_names = self.lst_pot_names
        else:
            lbl_new.configure(text='DODAJ NOVU BILJKU')
            btn_new.configure(command=lambda: Admin.add_new_plant(self))
            lst_frms = self.lst_frms_p
            rows = qb.select_all(database, table, 'naziv_biljke')
            lst_names = self.lst_plant_names
        img_lst = []
        for fr in lst_frms:
            fr.destroy()
        lst_frms.clear()
        for row in rows:
            name = row[0]
            frm = Frame(frame, background=self.stycolor, highlightthickness=2, highlightcolor=self.fgc, height=155, width=290)

            lst_names.append(name)
            lst_names = [value for value in lst_names if value != name]
            
            if len(lst_names) <= len(rows):
                lst_frms.append(frm)

            has_plant = row[1]     
            for frm in lst_frms:       
                lbl_name = ttk.Label (frm, 
                            text=name.upper(), 
                            background=self.stycolor, 
                            foreground=self.fgc, 
                            font=('Helvetica', '12', 'bold'))
                btn_view  = Button (frm, 
                            text='vidi',
                            background=self.stycolor,
                            foreground=self.fgc,
                            activebackground=self.styhover,
                            activeforeground=self.fgh,
                            relief='flat')
                lbl_values = ttk.Label (frm, 
                            background=self.stycolor, 
                            foreground=self.fgc, 
                            font=('Helvetica', '10'))
                frm_status = Frame (frm, background=self.stycolor)
                lbl_status = Label(frm_status,
                            text='',
                            font=('Helvetica', '8', 'bold'),
                            background=self.stycolor, 
                            foreground=self.fgc)
                lbl_status.grid(column=0, row=0, columnspan=2)
                lbl_img1 = Label(frm_status,
                            background=self.stycolor, 
                            foreground=self.fgc,
                            image='')
                lbl_img1.grid(column=0, row=1)
                lbl_img2 = Label(frm_status, 
                            background=self.stycolor, 
                            foreground=self.fgc,
                            image='')
                lbl_img2.grid(column=1, row=1)
                lbl_img3 = Label(frm_status, 
                            background=self.stycolor, 
                            foreground=self.fgc,
                            image='')
                lbl_img3.grid(column=0, row=2)
                lbl_img4 = Label(frm_status, 
                            background=self.stycolor, 
                            foreground=self.fgc,
                            image='')
                lbl_img4.grid(column=1, row=2)

            if table == self.tb_posude:
                nm_ps=row[0]
                btn_view.configure(command= lambda m=nm_ps: Admin.pot_update(self, m))

            if table == self.tb_biljke:
                i=row[0]
                btn_view.configure(command= lambda m=i: Admin.plant_update(self, m))

            btn_view.place(x=240, y=125)
         
            if table == self.tb_biljke:
                photo = row[1]
                if type(photo) == str:
                    img_opn = Image.open(photo).resize((90, 120), Image.ANTIALIAS)
                else:
                    stream = BytesIO(photo)
                    img_opn = Image.open(stream).resize((90, 120), Image.ANTIALIAS)

                img_b = ImageTk.PhotoImage(img_opn)
                lbl_img = Label(frm, image=img_b)
                lbl_img.image = img_b
                lbl_img.place(x=15, y=15)
                lbl_name.place(x=120, y=15)
                img_lst.append(img_b)
                water = row[3]
                light = row[4]
                climate = row[5]
                tekst = f'Zalijevanje: {water}\nOsvjetljenje: {light}\nKlima: {climate}'
                lbl_values.configure(text=tekst)
                lbl_values.place(x=130, y=50)

            else:
                # print(frm)
                lbl_name.configure(text=f'Posuda: {name.upper()}')
                lbl_name.place(x=20, y=15)
                frm_status.place(x=180, y=15)
                lbl_values.place(x=20, y=50) 
                lst_txt = []
                lst_st = [] 
                
                if has_plant == 'True' or has_plant == True or has_plant == 1:
                    lbl_status.configure(text='STATUS')
                    data = qb.select_all(self.db_posude, self.tb_senzori, 'naziv_posude')
                    if len(data) == 0:
                        lbl_status.configure(text='STATUS\nprocessing...')
                        lbl_status.grid(column=0, row=0)
                        lbl_values.configure(text='Pricekaj prvo ocitanje senzora...')
                    else:
                        ocitanja = qb.get_last_row(self.db_posude, self.tb_posude, self.tb_senzori, row[0])
                        for o in ocitanja:
                            nm = row[2]
                            hum = o[6]
                            lig = o[7]
                            temp = o[8]
                            soil = o[9]
                            tekst = f'Biljka: {nm.upper()}\nVlaznost: {hum}%\nIntenzitet svjetla: {lig} lx\nTemperatura: {temp}°C\nKiselost: {soil} pH'
                            lst_txt.append(tekst)
                            lbl_values.configure(text=tekst)
                        us = qb.select_compare(self.db_posude, row[0])
                        nmpt = us[0]
                        wt, mst = us[2], us[7]
                        lt, ilm = us[3], us[8]
                        cl, tmp = us[4], us[9]
                        nb, ph = us[5], us[10]
                        if nmpt == row[0] and wt == 'Dnevno' and mst < 60:
                            lbl_img1.configure(image=self.img_watering)
                            lbl_img1.image = self.img_watering
                        elif nmpt == row[0] and wt == 'Tjedno' and mst < 40:
                            lbl_img1.configure(image=self.img_watering)
                            lbl_img1.image = self.img_watering
                        elif nmpt == row[0] and wt == 'Mjesecno' and mst < 20:
                            lbl_img1.configure(image=self.img_watering)
                            lbl_img1.image = self.img_watering
                        else:
                            lst_st.append(True)
                            lbl_img1.configure(text='', image='')

                        if nmpt == row[0] and lt == 'Jarko' and ilm < 200:
                            lbl_img2.configure(image=self.img_sunlight)
                            lbl_img2.image = self.img_sunlight
                        elif nmpt == row[0] and lt == 'Sjenovito' and ilm <= 70:
                            lbl_img2.configure(image=self.img_sunlight)
                            lbl_img2.image = self.img_sunlight
                        elif nmpt == row[0] and lt == 'Sjenovito' and ilm >= 200:
                            lbl_img2.configure(image=self.img_reduce_sunlight)
                            lbl_img2.image = self.img_reduce_sunlight
                        elif nmpt == row[0] and lt == 'Tamno' and ilm > 70:
                            lbl_img2.configure(image=self.img_reduce_sunlight)
                            lbl_img2.image = self.img_reduce_sunlight
                        else:
                            lst_st.append(True)
                            lbl_img2.configure(text='', image='')

                        if nmpt == row[0] and cl == 'Toplija' and tmp < 25:
                            lbl_img3.configure(image=self.img_add_temperature)
                            lbl_img3.image = self.img_add_temperature
                        elif nmpt == row[0] and cl == 'Umjerena' and tmp <= 15:
                            lbl_img3.configure(image=self.img_add_temperature)
                            lbl_img3.image = self.img_add_temperature
                        elif nmpt == row[0] and cl == 'Umjerena' and tmp >= 25:
                            lbl_img3.configure(image=self.img_reduce_temperature)
                            lbl_img3.image = self.img_reduce_temperature
                        elif nmpt == row[0] and cl == 'Hladnija' and tmp > 15:
                            lbl_img3.configure(image=self.img_reduce_temperature)
                            lbl_img3.image = self.img_reduce_temperature
                        else:
                            lst_st.append(True)
                            lbl_img3.configure(image='', text='')

                        if nmpt == row[0] and nb == 'True' or nb == True or nb == 1 and ph < 6 or ph > 8:
                            lbl_img4.configure(image=self.img_suplement)
                            lbl_img4.image = self.img_suplement
                        else:
                            lst_st.append(True)
                            lbl_img4.configure(image='', text='')
                        
                        if len(lst_st) == 4:
                            lbl_img1.configure(image=self.img_ok, text='')
                            lbl_img1.image = self.img_ok

                else:
                    lbl_values.configure(text='Posuda je prazna')    

        i = 1
        c = 0
        b = 0


        for fr in lst_frms:
            # print(fr)
            if (b%2) != 0:
                fr.grid(column=i, row=c, padx=20, pady=10)
                i += 1
                # print('i', i+1)
            else:
                fr.grid(column=i, row=c, padx=20, pady=10)
                i = 0
                c += 1
                # print('c', c+1)        
            b += 1
        for row in rows:
            if len(rows) > 0:   
                self.scroll_biljke.grid(column=3,row=0, rowspan=(b+1), sticky=(N,S))
                self.scroll_posude.grid(column=3,row=0, rowspan=(b+1), sticky=(N,S))
            else:
                self.scroll_biljke.grid(column=3,row=0, rowspan=1, sticky=(N,S))
                self.scroll_posude.grid(column=3,row=0, rowspan=1, sticky=(N,S))


    def upload_img(self): 

            f_types =[('Jpg Files', '*.jpg'),('Png files','*.png')]
            idir = os.path.join(os.getcwd(),'biljke')
            self.filename = filedialog.askopenfilename(initialdir=idir,filetypes=f_types)
            # print(f'ovo je filename: I{self.filename}I')
            if self.filename:
                file = os.path.basename(self.filename)
                self.img_path = os.path.join('biljke',file)
                self.img_up = ImageTk.PhotoImage(file=self.img_path)
                self.img_open = Image.open(self.img_path).resize((90, 120), Image.ANTIALIAS)
                self.img = ImageTk.PhotoImage(self.img_open)
                self.btn_upload.configure(image=self.img)
                self.btn_upload.image = self.img
            else:
                print('Molimo odaberite datoteku.')


    def upload_file(self):
        try:
            f_types = [("Text Files", "*.txt")]
            idir = os.path.join(os.getcwd(),'biljke')
            self.tf = filedialog.askopenfilename(initialdir=idir,filetypes=f_types)
            file = os.path.basename(self.tf)
            self.path = os.path.join('biljke',file)
            self.ent_path.insert(END, self.path)
            self.path_open = open(self.path, encoding='UTF-8')
            data = self.path_open.read()
            self.txt_opis.insert(END, data)
        except:
            print('Niste odabrali datoteku.')
        
        
    def view_plants(self):
        ''' Ova funkcija prikazuje listu biljaka '''
        self.forget_placing()
        self.fr_biljke.place(x=10, y=55, width=700, height=390)
        self.fr_head.place(x=0, y=0,height=50, width=700)
        self.lbl_naslov.configure(image=self.biljke_naslov_img)
        self.btn_return.place(x=5, y=460, width=690)
        Admin.view_list(self, self.db_posude, self.tb_biljke, self.frs_biljke)
        self.btn_sync.configure(command=lambda: [Admin.sync_measuring(self), Admin.view_plants(self)])
        self.btn_sync.place(x=5, y=420, width=690)

    def add_new_plant(self):
        ''' Ova funkcija otvara okvir za unos nove biljke '''
        ##  clearing  ##
        self.btn_delete_plant.place_forget()
        self.btn_upload.configure(image=self.add_new_img)
        self.ent_plant_name.delete(0, END)
        self.ent_path.delete(0, END)
        self.txt_opis.delete('1.0', END)
        self.var_zalijevanje.set('Odaberi')
        self.var_svjetlost.set('Odaberi')
        self.var_temperatura.set('Odaberi')
        self.boolvar_biljke.set('False')
        self.btn_sync.place_forget()

        ## variables  ##
    
        self.btn_return.place(x=5, y=460, width=690)
        self.lbl_title_new.configure(text='UNESITE NOVU BILJKU')

        lbl_name = ttk.Label (self.frnew_biljke, 
                    text='Unesi ime biljke: ', 
                    background=self.bgc, 
                    foreground=self.fgh,
                    font=('Helvetica', 10))

        lbl_vlaga = ttk.Label (self.frnew_biljke, 
                    text='Odaberite vrstu zalijevanja: ', 
                    background=self.bgc, 
                    foreground=self.fgh,
                    font=('Helvetica', 10))

        lbl_svj = ttk.Label (self.frnew_biljke, 
                    text='Odaberite vrstu svjetlosti: ', 
                    background=self.bgc, 
                    foreground=self.fgh,
                    font=('Helvetica', 10))

        lbl_temp = ttk.Label (self.frnew_biljke, 
                    text='Odaberite klimu: ', 
                    background=self.bgc, 
                    foreground=self.fgh,
                    font=('Helvetica', 10))

        lbl_supst = ttk.Label (self.frnew_biljke, 
                    text='Dohrana: ', 
                    background=self.bgc, 
                    foreground=self.fgh,
                    font=('Helvetica', 10))
                    
        lbl_open = ttk.Label (self.frnew_biljke, 
                    text='Dodajte opis (.txt):', 
                    background=self.bgc, 
                    foreground=self.fgh,
                    font=('Helvetica', 10))

        ##  placment ## 
        self.frnew_biljke.place(x=0, y=55, width=700, height=390)
        self.lbl_title_new.place(x=280, y=10)

        self.btn_upload.place(x=50, y=30)

        lbl_name.place(x=170, y=50)
        self.ent_plant_name.place(x=280, y=50)

        lbl_vlaga.place(x=170, y=80)
        self.ch_zalijevanje.place(x=350,y=80)

        lbl_svj.place(x=170, y=110)
        self.ch_svjetlost.place(x=350,y=110)

        lbl_temp.place(x=170, y=140)
        self.ch_temperatura.place(x=350, y=140)

        lbl_supst.place(x=440, y=140)
        self.cb_dohrana.place(x=500, y=140)

        lbl_open.place(x=50, y=170)
        self.btn_addfile.place(x=560, y=160)
        self.ent_path.place(x=160, y=170)

        self.txt_opis.place(x=50, y=190)
        self.btn_save.configure(command= lambda: Admin.save_plant(self))
        self.btn_save.place(x=5, y=420, width=690)
    
    def save_plant(self):
        ''' Ova funkcija sprema novu biljku u bazu '''
        try:
            if str(self.ent_plant_name.get()) == '' or \
                        str(self.img_path) == '' or \
                        str(self.ent_path.get()) == '' or  \
                        str(self.var_zalijevanje.get()) == 'Odaberi' or \
                        str(self.var_svjetlost.get()) == 'Odaberi' or \
                        str(self.var_temperatura.get()) == 'Odaberi':
                showwarning(title='Oprez!', message='Obavezno unesite sva polja!')
                print('Molimo ispunite sva polja!!')
            else:
                qb.insert_plant( self.db_posude, 
                        str(self.ent_plant_name.get()), 
                        str(self.img_path), 
                        str(self.ent_path.get()),
                        str(self.var_zalijevanje.get()),
                        str(self.var_svjetlost.get()),
                        str(self.var_temperatura.get()),
                        self.boolvar_biljke.get())
            if str(self.ent_plant_name.get()) not in self.lst_plant_names:
                self.lst_plant_names.append(str(self.ent_plant_name.get()))
            if str(self.ent_plant_name.get()) not in self.lst_biljke:
                self.lst_biljke.append(str(self.ent_plant_name.get()))
        except:
            print('Promjene nisu unesene!!!')

        Admin.add_new_plant(self)

    def plant_update(self, nm_pl):
        ''' Ova funkcija otvara okvir postojeće biljke i priprema je za azuriranje '''
        self.fread_biljke.place(x=0, y=55, width=700, height=390)
        self.btn_sync.place_forget()
        self.btn_return.place(x=5, y=460, width=690)
        ## variables  ##
        self.ent_plant_name.delete(0, END)
        self.ent_path.delete(0, END)
        self.txt_opis.delete('1.0', END)
        self.var_zalijevanje.set('Odaberi')
        self.var_svjetlost.set('Odaberi')
        self.var_temperatura.set('Odaberi')
        self.boolvar_biljke.set(False)


        lbl_name = ttk.Label (self.frnew_biljke, 
                    text='Unesi ime biljke: ', 
                    background=self.bgc, 
                    foreground=self.fgh,
                    font=('Helvetica', 10))

        lbl_vlaga = ttk.Label (self.frnew_biljke, 
                    text='Odaberite vrstu zalijevanja: ', 
                    background=self.bgc, 
                    foreground=self.fgh,
                    font=('Helvetica', 10))

        lbl_svj = ttk.Label (self.frnew_biljke, 
                    text='Odaberite vrstu svjetlosti: ', 
                    background=self.bgc, 
                    foreground=self.fgh,
                    font=('Helvetica', 10))

        lbl_temp = ttk.Label (self.frnew_biljke, 
                    text='Odaberite klimu: ', 
                    background=self.bgc, 
                    foreground=self.fgh,
                    font=('Helvetica', 10))

        lbl_supst = ttk.Label (self.frnew_biljke, 
                    text='Dohrana: ', 
                    background=self.bgc, 
                    foreground=self.fgh,
                    font=('Helvetica', 10))
                    
        lbl_open = ttk.Label (self.frnew_biljke, 
                    text='Dodajte opis (.txt):', 
                    background=self.bgc, 
                    foreground=self.fgh,
                    font=('Helvetica', 10))

        ##  placment ## 
        self.frnew_biljke.place(x=0, y=55, width=700, height=390)
        self.lbl_title_new.place(x=280, y=10)
        self.btn_upload.place(x=50, y=30)
        self.btn_delete_plant.place(x=560, y=80)
        self.btn_delete_plant.configure(command= lambda: Admin.delete_plant(self))
        plants = qb.select_pl_by_name(self.db_posude, nm_pl)

        for pl in plants:
            if type(pl[1]) == str:
                print(f'biljke/{os.path.basename(pl[1])}')
                img_path = f'biljke/{os.path.basename(pl[1])}'
                img_opn = Image.open(img_path).resize((90, 120), Image.ANTIALIAS)
            else:
                stream = BytesIO(pl[1])
                print(os.path.basename(pl[1]))
                img_opn = Image.open(stream).resize((90, 120), Image.ANTIALIAS)
            img_b = ImageTk.PhotoImage(img_opn)
            img_b = ImageTk.PhotoImage(img_opn)
            water = pl[3]
            light = pl[4]
            climate = pl[5]
            boost = pl[6]
            self.lbl_title_new.configure(text=f'{pl[0].upper()}')
            self.btn_upload.configure(image=img_b)
            self.btn_upload.image = img_b
            self.ent_plant_name.insert(0, pl[0])

            path_open = open(pl[2], encoding='UTF-8')
            data = path_open.read()
            self.txt_opis.insert(END, data)

            self.ent_path.insert(0, pl[2])            
            self.var_zalijevanje.set(water)
            self.var_svjetlost.set(light)
            self.var_temperatura.set(climate)
            self.boolvar_biljke.set(boost)
            self.btn_save.configure(command= lambda m = pl[1]: Admin.update_plant_data(self, nm_pl, m))

        lbl_name.place(x=170, y=50)
        self.ent_plant_name.place(x=280, y=50)
        lbl_vlaga.place(x=170, y=80)
        self.ch_zalijevanje.place(x=350,y=80)
        lbl_svj.place(x=170, y=110)
        self.ch_svjetlost.place(x=350,y=110)
        lbl_temp.place(x=170, y=140)
        self.ch_temperatura.place(x=350, y=140)
        lbl_supst.place(x=440, y=140)
        self.cb_dohrana.place(x=500, y=140)
        lbl_open.place(x=50, y=170)
        self.btn_addfile.place(x=560, y=160)
        self.ent_path.place(x=160, y=170)
        self.txt_opis.place(x=50, y=190)
        self.btn_save.place(x=5, y=420, width=690)

    def update_plant_data(self, plant_name, img):
        ''' Ova funkcija azurira podatke postojece biljke u bazi '''
        try:
            if str(self.ent_plant_name.get()) == '' or \
                        str(self.img_path) == '' or \
                        str(self.ent_path.get()) == '' or  \
                        str(self.var_zalijevanje.get()) == 'Odaberi' or \
                        str(self.var_svjetlost.get()) == 'Odaberi' or \
                        str(self.var_temperatura.get()) == 'Odaberi':
                showwarning(title='Oprez!', message='Obavezno unesite sva polja!')
                print('Molimo ispunite sva polja!!')
            else:
                qb.update_plants(self.db_posude,                         
                        str(self.ent_plant_name.get()), 
                        str(self.img_path),
                        str(self.ent_path.get()),
                        str(self.var_zalijevanje.get()),
                        str(self.var_svjetlost.get()),
                        str(self.var_temperatura.get()),
                        self.boolvar_biljke.get(),
                        plant_name)
        except:

                print('Promjene nisu unesene!!!')
        Admin.view_plants(self)

    def delete_plant(self):
        ''' Ova funkcija brise postojecu biljku iz baze '''  
        pots_with_plants = qb.select_all(self.db_posude,self.tb_senzori, 'naziv_posude')
        lst_plnts = []
        lst_full_pots = []
        for p in pots_with_plants:
            plant = p[1]
            pot = p[0]
            lst_plnts.append(plant)
            if plant == self.ent_plant_name.get():
                lst_full_pots.append(pot)

        if self.ent_plant_name.get() in lst_plnts:
            answer = askyesno(title='Brisanje biljke',
            message=f'OPREZ! Odabrali ste brisanje biljke koja posadena. Zelite li obrisati biljku {self.ent_plant_name.get()} i isprazniti posude?')
            if answer:
                qb.delete_row(self.db_posude, self.tb_biljke, 'naziv_biljke', str(self.ent_plant_name.get()))
                qb.delete_row(self.db_posude, self.tb_senzori, 'naziv_biljke', str(self.ent_plant_name.get()))
                for pot in lst_full_pots:
                    qb.update_pots(self.db_posude, pot, False, None, pot)
                if str(self.ent_plant_name.get()) in self.lst_biljke:
                    self.lst_biljke.remove(str(self.ent_plant_name.get()))
                Admin.view_plants(self)
        else:
            answer = askyesno(title='Brisanje biljke',
                message=f'OPREZ! Zelite li obrisati {self.ent_plant_name.get()} ?')
            if answer:
                qb.delete_row(self.db_posude, self.tb_biljke, 'naziv_biljke', str(self.ent_plant_name.get()))
                if str(self.ent_plant_name.get()) in self.lst_biljke:
                    self.lst_biljke.remove(str(self.ent_plant_name.get()))
                Admin.view_plants(self)

    ### POSUDE ###        
    def view_pots(self):
        ''' Ova funkcija prikazuje okvir baze posuda '''
        self.forget_placing()
        self.fr_posude.place(x=10, y=55, width=700, height=390)
        self.fr_head.place(x=0, y=0,height=50, width=700)
        self.lbl_naslov.configure(image=self.pyposude_naslov_img)
        self.btn_return.place(x=5, y=460, width=690)
        Admin.view_list(self, self.db_posude, self.tb_posude, self.frs_posude)
        self.btn_sync.configure(command=lambda: [Admin.sync_measuring(self), Admin.view_pots(self)])
        self.btn_sync.place(x=5, y=420, width=690)

    def add_new_pot(self):
        ''' Ova funkcija otvara okvir za unos nove posude '''
        self.btn_update_pot.place_forget()
        self.btn_delete_pot.place_forget()
        self.cnv_plot.place_forget()
        self.lbl_values.place_forget()
        self.ent_pot_name.delete(0, 'end')
        self.boolvar_posude.set('False')                
        self.var_baza_biljka.set('Odaberi')
        self.update_option_menu()
        self.btn_sync.place_forget()

        self.btn_return.place(x=5, y=460, width=690)
        self.lbl_titlep_new.configure(text='UNESITE NOVU POSUDU')

        self.lbl_pot_name.place(x=100, y=70)
        self.ent_pot_name.place(x=250, y=70)
        self.lbl_prazno.place(x=100, y=100)
        self.cb_posadeno.place(x=250, y=100)
        self.get_cb_value(self.boolvar_posude)
        self.lbl_biljka.place(x=100, y=130)
        self.ch_baza_biljka.place(x=250, y=130)

        self.frnew_posude.place(x=0, y=55, width=700, height=390)
        self.lbl_titlep_new.place(x=250, y=10)


        self.btn_save.configure(command=lambda:Admin.save_new_pot(self))
        self.btn_save.place(x=5, y=420, width=690)

    def save_new_pot(self):
        ''' Ova funkcija sprema novu posudu u bazu '''
        if str(self.ent_pot_name.get()) != '':
            if self.boolvar_posude.get() == True or \
                self.boolvar_posude.get() == 'True' or \
                    self.boolvar_posude.get() == 1:
                if self.var_baza_biljka.get() != 'Odaberi':
                    qb.insert_posuda(self.db_posude, 
                                    str(self.ent_pot_name.get()), 
                                    self.boolvar_posude.get(), 
                                    self.var_baza_biljka.get())
                else:
                    showwarning(title='Oprez!', message='Molimo vas da odaberete ime biljke ili odznacite popunjenost posude!')

                Admin.get_measures(self,self.ent_pot_name.get(), self.var_baza_biljka.get())
            else:
                qb.insert_posuda(self.db_posude,
                                    str(self.ent_pot_name.get()), 
                                    self.boolvar_posude.get(), 
                                    None)
            if str(self.ent_pot_name.get()) not in self.lst_pot_names:
                self.lst_pot_names.append(str(self.ent_pot_name.get()))

        else:
            showwarning(title='Oprez!', message='Obavezno unesite ime posude!')
            print('Molimo unesite ime posude!')

        Admin.add_new_pot(self)

    def pot_update(self, nm_ps):
        ''' Ova funkcija otvara novi postojecu posudu, prikazuje njeno stanje i priprema je za azuriranje '''
        self.ent_pot_name.delete(0, 'end')
        self.boolvar_posude.set(0)                
        self.var_baza_biljka.set('Odaberi')

        self.frnew_posude.place(x=0, y=55, width=700, height=390)
        self.btn_sync.configure(command=lambda: [Admin.sync_measuring(self), Admin.pot_update(self, nm_ps)])        
        self.btn_sync.place(x=5, y=420, width=690)
        self.lbl_titlep_new.place(x=280, y=10)
        self.lbl_pot_name.place(x=100, y=70)
        self.ent_pot_name.place(x=250, y=70)
        self.lbl_prazno.place(x=100, y=100)
        self.cb_posadeno.place(x=250, y=100)
        self.get_cb_value(self.boolvar_posude)
        self.lbl_biljka.place(x=100, y=130)
        self.ch_baza_biljka.place(x=250, y=130)

        pots = qb.select_one_by_name(self.db_posude, nm_ps)
        for p in pots:
            self.ent_pot_name.insert(0, p[0])
            has_plant = p[1]
            self.boolvar_posude.set(has_plant)

            if has_plant == 'True' or has_plant == True or has_plant == 1:
                self.btn_update_pot.place(x=370, y=100, width=60, height=20)
                self.btn_delete_pot.place(x=370, y=130, width=60, height=20)

                self.cb_posadeno.select()
                self.ch_baza_biljka.configure(state=NORMAL)
                self.var_baza_biljka.set(p[2])
                self.cnv_plot.place(x=10, y=160)
                self.lbl_values.place(x=450, y=60) 
                ocitanja = qb.get_last_row(self.db_posude, self.tb_posude, self.tb_senzori, nm_ps)
                for o in ocitanja:
                    nm = p[2]
                    hum = o[6]
                    lig = o[7]
                    temp =o[8]
                    soil = o[9]
                    tekst = f'Biljka: {nm.upper()}\nVlaznost: {hum}%\nIntenzitet svjetla: {lig} lx\nTemperatura: {temp}°C\nKiselost: {soil} pH'
                    take_photo = qb.select_image(p[2])
                    if type(take_photo) == str:
                        img_opn = Image.open(take_photo).resize((60, 90), Image.ANTIALIAS)
                    else:
                        photo = BytesIO(take_photo)
                        img_opn = Image.open(photo).resize((60, 90), Image.ANTIALIAS)
                    img_b = ImageTk.PhotoImage(img_opn)
                    self.lbl_values.image = img_b   
                    self.lbl_values.configure(text=tekst, image=img_b, compound='left')            
                    Admin.show_graph(self, self.cnv_plot, nm_ps)

            else:
                self.btn_update_pot.configure(text='Spremi')
                self.btn_update_pot.place(x=100, y=160, width=330, height=30)
                self.btn_delete_pot.place(x=370, y=100, width=60, height=50)
                self.lbl_empty.configure(image=self.img_empty)
                self.lbl_empty.place(x=500, y=75)
                
                self.cb_posadeno.deselect()
                self.var_baza_biljka.set('Odaberi')
                self.ch_baza_biljka.configure(state=DISABLED)
                self.lbl_values.place_forget()
                self.cnv_plot.place_forget()

                     
            self.lbl_titlep_new.configure(text=f'POSUDA: {p[0].upper()} STANJE')
            self.update_option_menu()
            plant_names = qb.select_one_by_name(self.db_posude, nm_ps)
            for nm in plant_names:
                nm_pl = nm[2]
            self.btn_update_pot.configure(command= lambda m=nm_ps, n=nm_pl: Admin.update_pot_data(self, n, m))
            self.btn_delete_pot.configure(command= lambda m=nm_ps: Admin.delete_pot_data(self, m))
            
    def update_pot_data(self, plant_name, pot_name):
        ''' Ova funkcija sprema azurirane podatke posude u bazu '''
        has_plant = self.boolvar_posude.get()
        if str(self.ent_pot_name.get()) != '':
            if has_plant == True or has_plant == 'True' or has_plant == 1:
                if plant_name == self.var_baza_biljka.get():
                    print('ocitani senzori za', pot_name)
                    qb.update_pots(self.db_posude, self.ent_pot_name.get(), self.boolvar_posude.get(), self.var_baza_biljka.get(), pot_name)
                    qb.delete_sensors(self.db_posude, pot_name, plant_name)
                    qb.update_pot_new_name(self.db_posude, self.ent_pot_name.get(), pot_name)
                    Admin.get_measures(self, self.ent_pot_name.get(), self.var_baza_biljka.get())
                else:
                    print('novi senzori za:', pot_name)
                    qb.update_pots(self.db_posude, self.ent_pot_name.get(), self.boolvar_posude.get(), self.var_baza_biljka.get(), pot_name)
                    qb.delete_sensors(self.db_posude, pot_name, plant_name)
                    qb.update_pot_new_name(self.db_posude, self.ent_pot_name.get(), pot_name)
                    Admin.get_measures(self, self.ent_pot_name.get(), self.var_baza_biljka.get())

            else:
                    print('obrisano iz baze')
                    qb.update_pots(self.db_posude, self.ent_pot_name.get(), self.boolvar_posude.get(), self.var_baza_biljka.get(), pot_name)
                    qb.delete_row(self.db_posude, self.tb_senzori, 'naziv_posude', pot_name)
        else:
            showwarning(title='Oprez!', message='Obavezno unesite ime posude!')
            print('Molimo unesite ime posude!')
        Admin.view_pots(self)

    def delete_pot_data(self, pot_name):
        ''' Ova funkcija brise odabranu posudu iz baze '''
        answer = askyesno(title='Potvrdi brisanje',
                          message='Zelite li obrisati posudu? Sva dosadasnja mjerenja ce biti obrisana!')
        if answer:
            qb.delete_row(self.db_posude, self.tb_posude, 'naziv_posude', pot_name)
            qb.delete_row(self.db_posude, self.tb_senzori, 'naziv_posude', pot_name)
        
            Admin.view_pots(self)

    def get_measures(self, posuda, biljka):
        ''' Ova funkcija stvara random podatke ocitanih senzora iz biljke, sluzi za prvo mjerenje '''
        vlaga = rnd(10,70)
        svjetlo = rnd(10,350)
        temp = rnd(10.0,30.0) 
        ph = rnd(4.0,8.0)
        qb.insert_measuring(self.db_posude,
                        posuda, 
                        biljka,
                        dt.now().strftime('%d.%m.%Y. %H:%M:%S'),
                        vlaga, svjetlo, temp, ph)

    def sync_measuring(self):
        ''' Ova funkcija azurira simulirane podatke sa senzora u bazi '''
        data = qb.select_all_full(self.db_posude)
        for d in data:
            vlaga = rnd(10,70)
            svjetlo = rnd(10,350)
            temp = rnd(10.0,30.0) 
            ph = rnd(4.0,8.0)
            qb.sync_measurements(self.db_posude, d[0], d[2], dt.now().strftime('%d.%m.%Y. %H:%M:%S'), vlaga, svjetlo, temp, ph)
        
    def show_graph(self, frame, nm_ps):
        ''' Ova funkcija sluzi za graficki prikaz ocitanih podataka sa senzora '''
        con = sqlite3.connect(self.db_posude)
        query = f"SELECT * FROM pynjega WHERE naziv_posude='{nm_ps}'"
        senzori_df = pd.read_sql_query(query, con)
        
        fig = senzori_df.tail(7).plot(x="vrijeme_mjerenja", 
                            y=["vlaznost_postotak","intenzitet_osvjetljenja_lx","temperatura_celzijus", "tlo_ph"], 
                            kind="line", rot=2, fontsize=5, figsize=(7,2)).get_figure()

        plot1 = FigureCanvasTkAgg(fig, frame)
        plot1.get_tk_widget().place(x=0, y=0)
        plt.close(fig)

        con.close()

r = Tk()
pyflora = guiFlora(r)
guiFlora.login_window(pyflora)
