#------------------------------------------- Requirements ----------------------------------------------#
    # - browse
    #     - Picture folder
    #     - Logo folder
    # - Options for each logo:
    #     - size                (counter)
    #     - location            (radio buttons)
    #         - top right   
    #         - top left
    #         - bottom right
    #         - bottom left
    #     - opacity (problem: makes invisible part of png darker when you decrease opacity)
    #     - user can enter name and location for final folder
#------------------------------------------------------------------------------------------------------#

import os
from tkinter import *
import tkinter.filedialog as tkFileDialog
from PIL import Image


def initialize():  
    global max_logo_size      # this is the percent logo will be of the shorter side of the image
    max_logo_size = 10
    
    global values_master
    values_master = {}
    
    global logo_choice
    logo_choice = {}

    global pictures_directory
    pictures_directory = ''
    
    global logos_directory
    logos_directory = ''
    
    global withlogo_directory
    withlogo_directory = ''

    global frames
    frames = []
    
    global widgets
    widgets = []

class logofier():

    def __init__(self, pictures_directory=None, logos_directory=None):
        self.tr_margin = 0
        self.tl_margin = 0
        self.br_margin = 0
        self.bl_margin = 0
        self.pictures_directory = pictures_directory
        self.logos_directory = logos_directory
        self.im = ''

    def logofy(self):
        global max_logo_size
        global values_master
        global logo_choice
        global pictures_directory
        global logos_directory
        global withlogo_directory
        global frames
        global widgets

        for filename in os.listdir(self.pictures_directory):

            print('Processing ', filename, '...')
            if not (filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.PNG') or filename.endswith('.JPG')):# or filename == logo_file:
                continue
            self.im = Image.open(self.pictures_directory+'/'+filename).convert("RGBA")
            width, height = self.im.size
            self.card = Image.new("RGBA", (width, height), (255, 255, 255))     # CARD
            # self.card.paste(self.im, (0, 0, width, height), self.im)                     # CARD
            self.card.paste(self.im, (0, 0, width, height))                     # CARD
            sq_fit_size = 0
            padding = 0
            
            if width > height:
                sq_fit_size = int(max_logo_size/100 * height)
                padding = int(1/100 * height)
            else:
                sq_fit_size = int(max_logo_size/100 * width)
                padding = int(1/100 * width)

            for logo_file, value in logo_choice.items():        
                valueInt = value.get()         # value in tk.IntVar() to get Int we will have to .get()

                logoIm = Image.open(self.logos_directory+'/'+logo_file).convert("RGBA")
                logoWidth, logoHeight = logoIm.size
                logo_area = logoHeight * logoWidth

                os.makedirs(withlogo_directory, exist_ok = True)        # check if such directory exists or not. If not it will create a new one.
                
                # ---------- Resizes logo to required size ----------
                if logoWidth > sq_fit_size and logoHeight > sq_fit_size:
                    if logoWidth > logoHeight:
                        logoHeight = int((sq_fit_size / logoWidth) * logoHeight)
                        logoWidth = sq_fit_size
                    else:
                        logoWidth = int((sq_fit_size / logoHeight) * logoWidth)
                        logoHeight = sq_fit_size
                    print("Resizing %s"% (logo_file)) 
                    logoIm = logoIm.resize((logoWidth, logoHeight))

                # logoIm.putalpha(50) # opacity

                # ---------- Checks position and pastes logo onto that position ----------
                if valueInt == 1:      # tr
                    # self.card.paste(logoIm, (width - logoWidth - self.tr_margin - 20, 20), logoIm)  # paste logo onto image
                    self.card.paste(logoIm, (width - logoWidth - self.tr_margin - padding, padding), logoIm)  # paste logo onto image
                    self.tr_margin += sq_fit_size
                elif valueInt == 2:      # tl
                    # self.card.paste(logoIm, ( self.tl_margin + 20, 20), logoIm)  # paste logo onto image
                    self.card.paste(logoIm, ( self.tl_margin + padding, padding), logoIm)  # paste logo onto image
                    self.tl_margin += sq_fit_size
                elif valueInt == 3:      # br
                    # self.card.paste(logoIm, (width - logoWidth - self.br_margin - 20, height - logoHeight - 20), logoIm)  # paste logo onto image
                    self.card.paste(logoIm, (width - logoWidth - self.br_margin - padding, height - logoHeight - padding), logoIm)  # paste logo onto image
                    self.br_margin += sq_fit_size
                elif valueInt == 4:      # bl
                    # self.card.paste(logoIm, ( self.bl_margin + 20, height - logoHeight - 20), logoIm)  # paste logo onto image
                    self.card.paste(logoIm, ( self.bl_margin + padding, height - logoHeight - padding), logoIm)  # paste logo onto image
                    self.bl_margin += sq_fit_size

            
        
            # self.card.save(os.path.join(withlogo_directory, filename), format='JPEG', quality=95)                      # save the logo-ed file

            self.card.load()
            background = Image.new("RGB", self.card.size, (255, 255, 255))
            background.paste(self.card, mask=self.card.split()[3]) # 3 is the alpha channel
            background.save(os.path.join(withlogo_directory, filename), 'JPEG', quality=100)
        
            self.tr_margin = 0
            self.tl_margin = 0
            self.br_margin = 0
            self.bl_margin = 0















# ------- Making the window layout -------
root=Tk(className=' Logofier - Add multiple logos to multiple images!')    
root.geometry("1000x650")                         # set window size
# root.iconbitmap("C:\\Users\\muhidabid\\Desktop\\JUMBO\\FAST\\projects\\logos_adder\\icons\\maswork_black.ico")     # set window icon
root.configure(bg='#F6ECBF')

# ----------- Working of window -----------
def increase_stat():
    global max_logo_size
    if max_logo_size < 100:
        max_logo_size += 1
        size_label.config(text = max_logo_size)

def decrease_stat():
    global max_logo_size
    if max_logo_size > 0:
        max_logo_size -= 1
        size_label.config(text = max_logo_size)
        
def logofy():
    global pictures_directory
    global logos_directory
    # ------ calling logofy functions ------
    logofier_obj = logofier(pictures_directory, logos_directory)
    logofier_obj.logofy()

def browsePics():
    global pictures_directory
    directory = tkFileDialog.askdirectory()
    ent1.insert(END, tkFileDialog)              # displays path onto 'Entry' bar
    print("Pictures Directory-------->   ", directory)
    pictures_directory = directory

def browseLogos():
    global logos_directory
    directory = tkFileDialog.askdirectory()
    ent2.insert(END, tkFileDialog)              # displays path onto 'Entry' bar
    print("Logos Directory-------->   ", directory)
    logos_directory = directory
    makeLogosList()                             # give options for each logo

def browseLocation():
    global withlogo_directory
    directory = tkFileDialog.askdirectory()
    ent3.insert(END, tkFileDialog)              # displays path onto 'Entry' bar
    print("Where to save Directory-------->   ", directory)
    withlogo_directory = directory

def makeLogosList():
    global max_logo_size
    global values_master
    global logo_choice
    global pictures_directory
    global logos_directory
    global withlogo_directory
    global frames
    global widgets
    global root
    logo_options_row = 1
    
    # Destroy previous frames:
    for frame in frames:
        frame.destroy()

    for logo_file in os.listdir(logos_directory):

        # Each logo will have a separate frame containing a set of widgets
        logo_frame = Frame(root, padx=5, pady=5)
        logo_frame.pack()
        frames.append(logo_frame)

        # -- 2 -- Label stating logo name
        l1 = Label( logo_frame, text=logo_file, font='Helvetica 9 bold').grid(row=0,column=1)
        widgets.append(l1)

        # -- 3 -- Radio buttons to specify location
        l2 = Label( logo_frame, text='Select logo position:').grid(row=logo_options_row,column=1)
        widgets.append(l2)

        # Dictionary to create multiple buttons
        values = {"Top right" : 1,           #   1 = tr
                "Top left" : 2,              #   2 = tl
                "Bottom right" : 3,          #   3 = br
                "Bottom left" : 4,}          #   4 = bl
        
        # values_master[logo_file] = values
        logo_choice[logo_file] = IntVar()
        
        # Loop is used to create multiple Radiobuttons rather than creating each button separately
        for (text, value) in values.items():
            r = Radiobutton(logo_frame, text = text, variable = logo_choice[logo_file], value = value, indicator = 1, bg = "#F9F9F9").grid(row=logo_options_row,column=value+1)
            widgets.append(r)

        logo_options_row+=1

if __name__ == "__main__": 
        
    initialize()

    logofy_frame = LabelFrame(root, text='Click here to apply logos to all your pictures', padx=5, pady=5)
    logofy_frame.pack(padx=10, pady=10)

    b1=Button(logofy_frame,text="LOGOFY!",font=40,command=logofy, bg='#C886E5')
    b1.pack()

    browse_frame = Frame(root)
    browse_frame.pack(padx=10, pady=10)

    Label(browse_frame, text="Choose folder containing pictures you want to apply logos to: ").grid(row=0, column=0)
    ent1=Entry(browse_frame,font=40)
    ent1.grid(row=0, column=1)
    b2=Button(browse_frame,text="Browse Pictures folder",font=40,command=browsePics, bg='#F9F9F9')
    b2.grid(row=0, column=2)

    Label(browse_frame, text="Choose folder containing all the logos you want to apply: ").grid(row=1, column=0)
    ent2=Entry(browse_frame,font=40)
    ent2.grid(row=1, column=1)
    b3=Button(browse_frame,text="Browse Logos folder",font=40,command=browseLogos, bg='#F9F9F9')
    b3.grid(row=1, column=2)

    Label(browse_frame, text="Choose location to save pictures: ").grid(row=2, column=0)
    ent3=Entry(browse_frame,font=40)
    ent3.grid(row=2, column=1)
    b4=Button(browse_frame,text="Browse location",font=40,command=browseLocation, bg='#F9F9F9')
    b4.grid(row=2, column=2)

    # -- 1 -- Counter to set logos size
    # make a frame so we can use grid inside
    logo_size_frame = Frame(root, padx=5, pady=5)
    logo_size_frame.pack()

    Label(logo_size_frame, text="Set logos size").grid(row=0, column=0)
    size_label = Label(logo_size_frame, text=max_logo_size)
    size_label.grid(row=1, column=1)            # Calling .grid directly in previous line gave the error 
                                                # AttributeError: 'NoneType' object has no attribute 'config'
                                                # The reason: https://stackoverflow.com/questions/23231563/nonetype-object-has-no-attribute-config
    Button(logo_size_frame, text="-", command=decrease_stat).grid(row=1, column=0)
    Button(logo_size_frame, text="+", command=increase_stat).grid(row=1, column=2)

    root.mainloop()