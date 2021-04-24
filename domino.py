from tkinter import *
from PIL import ImageTk, Image

class tile:
    topval = 0
    bottomval = 0
    image = None
    imagef = None
    f = None
    
    def __init__(self,filename,t,b):
        imagef = Image.open(filename)
        imagef = imagef.resize((40,40),Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(imagef)
        self.topval = t
        self.bottomval = b
        self.f = filename
        
    def align_tile(self,angle):
        imagef = Image.open(self.f)
        imagef = imagef.resize((40,40),Image.ANTIALIAS)
        imagef = imagef.rotate(angle)
        self.image = ImageTk.PhotoImage(imagef)
        
class place_t:
    x = 0
    y = 0
    openval = 0
    
    def __init__(self,val,xx,yy):
        self.x = xx
        self.y = yy
        self.openval = val