from PIL import Image,ImageFont
from PIL.PngImagePlugin import PngInfo

try:
    from OpenGL.GL import *
    from OpenGL.GLUT import *
except:
    msg=_('Error importing OpenGL library')
    msg+=_('   Python version : ' + sys.version)
    msg+=_('   Please check your version of opengl32.dll -- conflict may exist between different files present on your desktop')
    raise Exception(msg)

from os.path import exists
from io import BytesIO
import math
import numpy as np

from .PyTranslate import _
from .PyWMS import getIGNFrance, getWalonmap
from .textpillow import Font_Priority, Text_Image,Text_Infos
from .drawing_obj import Element_To_Draw

class genericImagetexture(Element_To_Draw):
    """
    Affichage d'une image en OpenGL via une texture
    """
    name: str
    idtexture: int

    width: int
    height: int

    which: str

    myImage: Image

    def __init__(self, which: str, label: str, mapviewer, xmin, xmax, ymin, ymax, imageFile="",
                 imageObj=None) -> None:

        super().__init__(label, True, mapviewer, False)

        try:
            self.mapviewer.canvas.SetCurrent(mapviewer.context)
        except:
            logging.error(_('Opengl setcurrent -- Do you have a active canvas ?'))

        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.idtexture = (GLuint * 1)()
        self.idx = 'texture_{}'.format(self.idtexture)

        try:
            glGenTextures(1, self.idtexture)
        except:
            raise NameError(
                'Opengl glGenTextures -- maybe a conflict with an existing opengl32.dll file - please rename the opengl32.dll in the libs directory and retry')

        self.which = which.lower()
        self.name = label
        self.imageFile = imageFile
        self.myImage = imageObj

        if imageFile != "":
            if exists(imageFile):
                self.myImage = Image.open(imageFile).convert('RGBA')

        if self.myImage is not None:
            self.width = self.myImage.width
            self.height = self.myImage.height
        else:
            self.width = -99999
            self.height = -99999

        self.update_minmax()

        self.oldview = [self.xmin, self.xmax, self.ymin, self.ymax, self.width, self.height]

        self.load(self.imageFile)

    def load(self, imageFile=""):
        if self.width == -99999 or self.height == -99999:
            return

        if self.mapviewer.canvas.SetCurrent(self.mapviewer.context):
            mybytes: BytesIO

            if imageFile != "":
                if not exists(imageFile):
                    return
                self.myImage = Image.open(imageFile).convert('RGBA')
            elif self.myImage is None:
                return

            glBindTexture(GL_TEXTURE_2D, self.idtexture[0])
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.myImage.width, self.myImage.height, 0, GL_RGBA,
                         GL_UNSIGNED_BYTE, self.myImage.tobytes())

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            glGenerateMipmap(GL_TEXTURE_2D)
        else:
            raise NameError(
                'Opengl setcurrent -- maybe a conflict with an existing opengl32.dll file - please rename the opengl32.dll in the libs directory and retry')

    def update_minmax(self):

        if self.myImage is None:
            return

        dx = self.xmax - self.xmin
        dy = self.ymax - self.ymin

        scale=dy/dx

        if int(scale*4) != int(float(self.height)/float(self.width)*4):
            scale = float(self.height)/float(self.width)

            self.ymax = self.ymin + dx *scale

    def reload(self,xmin=-99999,xmax=-99999,ymin=-99999,ymax=-99999):

        if xmin !=-99999:
            self.xmin = xmin
        if xmax !=-99999:
            self.xmax = xmax
        if ymin !=-99999:
            self.ymin = ymin
        if ymax !=-99999:
            self.ymax = ymax

        self.update_minmax()

        self.newview = [self.xmin, self.xmax, self.ymin, self.ymax, self.width, self.height]
        if self.newview != self.oldview:
            self.load()
            self.oldview = self.newview

    def plot(self, sx=None, sy=None, xmin=None, ymin=None, xmax=None, ymax=None, size=None):
        """ alias for paint"""
        self.paint()

    def find_minmax(self,update=False):
        """
        Generic function to find min and max spatial extent in data
        """
        # Nothing to do, set during initialization phase
        pass

    def paint(self):

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glColor4f(1., 1., 1., 1.)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glBindTexture(GL_TEXTURE_2D, self.idtexture[0])

        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(self.xmin, self.ymax)
        glTexCoord2f(1.0, 0.0)
        glVertex2f(self.xmax, self.ymax)
        glTexCoord2f(1.0, 1.0)
        glVertex2f(self.xmax, self.ymin)
        glTexCoord2f(0.0, 1.0)
        glVertex2f(self.xmin, self.ymin)
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)

        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)


class imagetexture(Element_To_Draw):
    """
    Affichage d'une image, obtenue depuis un Web service, en OpenGL via une texture
    """

    name: str
    idtexture: int

    width: int
    height: int

    which: str
    category: str
    subcategory: str

    France: bool
    epsg: str

    def __init__(self, which: str, label: str, cat: str, subc: str, mapviewer, xmin, xmax, ymin, ymax, width=1000,
                 height=1000, France=False, epsg='31370') -> None:

        super().__init__(label+cat+subc, plotted=False, mapviewer=mapviewer, need_for_wx=False)

        try:
            mapviewer.canvas.SetCurrent(mapviewer.context)
        except:
            logging.error(_('Opengl setcurrent -- Do you have a active canvas ?'))

        self.France = France
        self.epsg = epsg

        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.idtexture = (GLuint * 1)()
        self.idx = 'texture_{}'.format(self.idtexture)

        try:
            glGenTextures(1, self.idtexture)
        except:
            raise NameError(
                'Opengl glGenTextures -- maybe a conflict with an existing opengl32.dll file - '
                'please rename the opengl32.dll in the libs directory and retry')
        self.width = width
        self.height = height
        self.which = which.lower()
        self.category = cat  # .upper()
        self.name = label
        self.subcategory = subc  # .upper()
        self.oldview = [self.xmin, self.xmax, self.ymin, self.ymax, self.width, self.height]

        self.load()

    def load(self):
        if self.width == -99999 or self.height == -99999:
            return

        if self.mapviewer.canvas.SetCurrent(self.mapviewer.context):
            mybytes: BytesIO

            if self.France:
                mybytes = getIGNFrance(self.category, self.epsg,
                                       self.xmin, self.ymin, self.xmax, self.ymax,
                                       self.width, self.height, False)
            else:
                mybytes = getWalonmap(self.category + '/' + self.subcategory,
                                      self.xmin, self.ymin, self.xmax, self.ymax,
                                      self.width, self.height, False)
            image = Image.open(mybytes)

            glBindTexture(GL_TEXTURE_2D, self.idtexture[0])
            if self.subcategory[:5] == 'ORTHO':
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE,
                             image.tobytes())
            elif image.mode == 'RGB':
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGB, GL_UNSIGNED_BYTE,
                             image.tobytes())
            else:
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE,
                             image.tobytes())
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            glGenerateMipmap(GL_TEXTURE_2D)
        else:
            raise NameError(
                'Opengl setcurrent -- maybe a conflict with an existing opengl32.dll file - '
                'please rename the opengl32.dll in the libs directory and retry')

    def reload(self):
        dx = self.mapviewer.xmax - self.mapviewer.xmin
        dy = self.mapviewer.ymax - self.mapviewer.ymin
        cx = self.mapviewer.mousex
        cy = self.mapviewer.mousey

        coeff = .5
        self.xmin = cx - dx * coeff
        self.xmax = cx + dx * coeff
        self.ymin = cy - dy * coeff
        self.ymax = cy + dy * coeff
        self.width = self.mapviewer.canvaswidth * 2 * coeff
        self.height = self.mapviewer.canvasheight * 2 * coeff

        self.newview = [self.xmin, self.xmax, self.ymin, self.ymax, self.width, self.height]
        if self.newview != self.oldview:
            self.load()
            self.oldview = self.newview

    def plot(self, sx=None, sy=None, xmin=None, ymin=None, xmax=None, ymax=None, size=None):
        """ alias for paint"""
        self.paint()

    def find_minmax(self,update=False):
        """
        Generic function to find min and max spatial extent in data
        """
        # Nothing to do, set during initialization phase
        pass

    def paint(self):

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        glColor4f(1., 1., 1., 1.)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glBindTexture(GL_TEXTURE_2D, self.idtexture[0])

        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(self.xmin, self.ymax)
        glTexCoord2f(1.0, 0.0)
        glVertex2f(self.xmax, self.ymax)
        glTexCoord2f(1.0, 1.0)
        glVertex2f(self.xmax, self.ymin)
        glTexCoord2f(0.0, 1.0)
        glVertex2f(self.xmin, self.ymin)
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    def check_plot(self):
        self.plotted = True

    def uncheck_plot(self, unload=True):
        self.plotted = False


class Text_Image_Texture(genericImagetexture):

    def __init__(self, text: str, mapviewer, proptext:Text_Infos, vector, x:float, y:float) -> None:
        """Gestion d'un texte sous forme de texture OpenGL

        Args:
            text (str): texte à afficher
            mapviewer (wolf_mapviewer): objet parent sur lequel dessiner
            proptext (Text_Infos): infos sur la mise en forme
            vector (vector): vecteur associé au texte
            x (float): point d'accroche X
            y (float): point d'accroche Y
        """
        self.x = x
        self.y = y

        self.vector = vector
        self.proptext = proptext

        self.mapviewer = mapviewer

        self.findscale()

        self.proptext.findsize(text)
        xmin, xmax, ymin, ymax = proptext.getminmax(self.x,self.y)

        super().__init__('other', text, mapviewer, xmin, xmax, ymin, ymax)

        if self.myImage is not None:
            self.width = self.myImage.width
            self.height = self.myImage.height

        self.oldview = [self.xmin, self.xmax, self.ymin, self.ymax, self.width, self.height]

    def findscale(self):
        w,h = self.mapviewer.GetSize()
        dx = self.mapviewer.xmax - self.mapviewer.xmin
        dy = self.mapviewer.ymax - self.mapviewer.ymin
        self.proptext.findscale(dx,dy,w,h)

    def load(self, imageFile=""):


        if self.mapviewer.canvas.SetCurrent(self.mapviewer.context):

            if imageFile != "":
                if not exists(imageFile):
                    return
                self.myImage = Image.open(imageFile).convert('RGBA')
            else:
                self.myImage = Text_Image(self.name,self.proptext)._image

            if self.myImage is None:
                return

            glEnable(GL_TEXTURE_2D)

            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
            glBindTexture(GL_TEXTURE_2D, self.idtexture[0])
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.myImage.width, self.myImage.height, 0, GL_RGBA,
                         GL_UNSIGNED_BYTE, self.myImage.transpose(Image.FLIP_TOP_BOTTOM).tobytes())

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            glGenerateMipmap(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, 0)

            glDisable(GL_TEXTURE_2D)
        else:
            raise NameError(
                'Opengl setcurrent -- maybe a conflict with an existing opengl32.dll file - please rename the opengl32.dll in the libs directory and retry')

    def paint(self):

        self.findscale()
        self.proptext.setsize_real()
        if self.proptext.adapt_fontsize(self.name):
            self.update_image()
        x,y = self.proptext.getcorners(self.x,self.y)

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glColor4f(1., 1., 1., 1.)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA)

        glBindTexture(GL_TEXTURE_2D, self.idtexture[0])

        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(x[0], y[0])
        glTexCoord2f(1.0, 0.0)
        glVertex2f(x[1], y[1])
        glTexCoord2f(1.0, 1.0)
        glVertex2f(x[2], y[2])
        glTexCoord2f(0.0, 1.0)
        glVertex2f(x[3], y[3])
        glEnd()

        glBindTexture(GL_TEXTURE_2D, 0)

        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)

        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    def update_image(self,newtext="",proptext=None):

        if newtext !="":
            self.name = newtext

        if proptext is not None:
            self.proptext = proptext

        self.myImage = Text_Image(self.name,self.proptext).image
        self.load()