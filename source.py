import all_globals
import os
from PIL import Image

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

        for filename in os.listdir(self.pictures_directory):

            print('Processing ', filename, '...')
            if not (filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.PNG') or filename.endswith('.JPG')):# or filename == logo_file:
                continue
            self.im = Image.open(self.pictures_directory+'/'+filename)
            width, height = self.im.size
            sq_fit_size = 0
            print(all_globals.max_logo_size)
            
            if width > height:
                sq_fit_size = int(all_globals.max_logo_size/100 * height)
            else:
                sq_fit_size = int(all_globals.max_logo_size/100 * width)

            for logo_file, value in all_globals.logo_choice.items():        
                valueInt = value.get()         # value in tk.IntVar() to get Int we will have to .get()

                logoIm = Image.open(self.logos_directory+'/'+logo_file)
                logoWidth, logoHeight = logoIm.size
                logo_area = logoHeight * logoWidth

                os.makedirs(all_globals.withlogo_directory, exist_ok = True)        # check if such directory exists or not. If not it will create a new one.
                
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

                # ---------- Checks position and pastes logo onto that position ----------
                if valueInt == 1:      # tr
                    self.im.paste(logoIm, (width - logoWidth - self.tr_margin - 20, 20), logoIm)  # paste logo onto image
                    self.tr_margin += sq_fit_size
                elif valueInt == 2:      # tl
                    self.im.paste(logoIm, ( self.tl_margin + 20, 20), logoIm)  # paste logo onto image
                    self.tl_margin += sq_fit_size
                elif valueInt == 3:      # br
                    self.im.paste(logoIm, (width - logoWidth - self.br_margin - 20, height - logoHeight - 20), logoIm)  # paste logo onto image
                    self.br_margin += sq_fit_size
                elif valueInt == 4:      # bl
                    self.im.paste(logoIm, ( self.bl_margin + 20, height - logoHeight - 20), logoIm)  # paste logo onto image
                    self.bl_margin += sq_fit_size

                # # logoIm.putalpha(95) # opacity

            self.im.save(os.path.join(all_globals.withlogo_directory, filename), quality=100)                      # save the logo-ed file
            self.tr_margin = 0
            self.tl_margin = 0
            self.br_margin = 0
            self.bl_margin = 0