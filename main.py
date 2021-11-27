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

# from source import *
# os.system("python source.py")
import os
# import source
# import all_globals
from source import *
from all_globals import *
from tkinter import *
import tkinter.filedialog as tkFileDialog

all_globals.initialize()

# ------- Making the window layout -------
root=Tk(className=' Logofier - Add multiple logos to multiple images!')    
root.geometry("1000x650")                         # set window size
# root.iconbitmap("C:\\Users\\muhidabid\\Desktop\\JUMBO\\FAST\\projects\\logos_adder\\icons\\maswork_black.ico")     # set window icon
root.configure(bg='#F6ECBF')

# ----------- Working of window -----------
def increase_stat():
    if all_globals.max_logo_size < 100:
        all_globals.max_logo_size += 1
        size_label.config(text = all_globals.max_logo_size)

def decrease_stat():
    if all_globals.max_logo_size > 0:
        all_globals.max_logo_size -= 1
        size_label.config(text = all_globals.max_logo_size)
        
def logofy():
    # ------ calling logofy functions ------
    logofier_obj = source.logofier(all_globals.pictures_directory, all_globals.logos_directory)
    logofier_obj.logofy()

def browsePics():
    directory = tkFileDialog.askdirectory()
    ent1.insert(END, tkFileDialog)              # displays path onto 'Entry' bar
    print("Pictures Directory-------->   ", directory)
    all_globals.pictures_directory = directory

def browseLogos():
    directory = tkFileDialog.askdirectory()
    ent2.insert(END, tkFileDialog)              # displays path onto 'Entry' bar
    print("Logos Directory-------->   ", directory)
    all_globals.logos_directory = directory
    makeLogosList()                             # give options for each logo

def browseLocation():
    directory = tkFileDialog.askdirectory()
    ent3.insert(END, tkFileDialog)              # displays path onto 'Entry' bar
    print("Where to save Directory-------->   ", directory)
    all_globals.withlogo_directory = directory

def makeLogosList():
    global root
    logo_options_row = 1
    
    # Destroy previous frames:
    for frame in all_globals.frames:
        frame.destroy()

    for logo_file in os.listdir(all_globals.logos_directory):

        # Each logo will have a separate frame containing a set of widgets
        logo_frame = Frame(root, padx=5, pady=5)
        logo_frame.pack()
        all_globals.frames.append(logo_frame)

        # -- 2 -- Label stating logo name
        l1 = Label( logo_frame, text=logo_file, font='Helvetica 9 bold').grid(row=0,column=1)
        all_globals.widgets.append(l1)

        # -- 3 -- Radio buttons to specify location
        l2 = Label( logo_frame, text='Select logo position:').grid(row=logo_options_row,column=1)
        all_globals.widgets.append(l2)

        # Dictionary to create multiple buttons
        values = {"Top right" : 1,           #   1 = tr
                "Top left" : 2,              #   2 = tl
                "Bottom right" : 3,          #   3 = br
                "Bottom left" : 4,}          #   4 = bl
        
        # values_master[logo_file] = values
        all_globals.logo_choice[logo_file] = IntVar()
        
        # Loop is used to create multiple Radiobuttons rather than creating each button separately
        for (text, value) in values.items():
            r = Radiobutton(logo_frame, text = text, variable = all_globals.logo_choice[logo_file], value = value, indicator = 1, bg = "#F9F9F9").grid(row=logo_options_row,column=value+1)
            all_globals.widgets.append(r)

        logo_options_row+=1

if __name__ == "__main__": 
        
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
    size_label = Label(logo_size_frame, text=all_globals.max_logo_size)
    size_label.grid(row=1, column=1)            # Calling .grid directly in previous line gave the error 
                                                # AttributeError: 'NoneType' object has no attribute 'config'
                                                # The reason: https://stackoverflow.com/questions/23231563/nonetype-object-has-no-attribute-config
    Button(logo_size_frame, text="-", command=decrease_stat).grid(row=1, column=0)
    Button(logo_size_frame, text="+", command=increase_stat).grid(row=1, column=2)

    root.mainloop()