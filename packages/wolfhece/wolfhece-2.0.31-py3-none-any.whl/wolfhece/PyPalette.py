from matplotlib.cm import ScalarMappable
from matplotlib.figure import Figure
from matplotlib.transforms import Bbox
import wx
import numpy as np
import numpy.ma as ma
from bisect import bisect_left
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap,Normalize
from collections import OrderedDict
import typing
import io
import logging

from .PyTranslate import _
from .CpGrid import CpGrid
from .PyVertex import getRGBfromI, getIfromRGB

class wolfpalette(wx.Frame,LinearSegmentedColormap):
    """
    Palette de couleurs basée sur l'objet "LinearSegmentedColormap" de Matplotlib (Colormap objects based on lookup tables using linear segments)
    """
    filename:str
    nb:int
    colors:np.array
    colorsflt:np.array

    def __init__(self, parent=None, title=_('Colormap'),w=100,h=500,nseg=1024):

        self.filename=''
        self.nb = 0
        self.values = None
        self.colormin = np.array([1.,1.,1.,1.])
        self.colormax = np.array([0,0,0,1.])
        self.nseg=nseg
        self.automatic = True
        self.interval_cst = False

        self.wx_exists = wx.App.Get() is not None

        #Appel à l'initialisation d'un frame général
        if(self.wx_exists):
            wx.Frame.__init__(self, parent, title=title, size=(w,h),style=wx.DEFAULT_FRAME_STYLE)

        LinearSegmentedColormap.__init__(self,'wolf',{},nseg)
        self.set_bounds()

    def get_colors_f32(self):

        colors = self.colorsflt[:,:3].astype(np.float32)

        return colors

    def set_bounds(self):
        self.set_under(tuple(self.colormin))
        self.set_over(tuple(self.colormax))

    def get_rgba(self,x):

        dval=self.values[-1]-self.values[0]
        if dval==0.:
            dval=1.
        xloc = (x-self.values[0])/dval

        if self.interval_cst:
            rgba = np.ones((xloc.shape[0],xloc.shape[1],4))

            ij = np.where(xloc<0.)
            rgba[ij[0],ij[1]] = self.colormin
            ij = np.where(xloc>=1.)
            rgba[ij[0],ij[1]] = self.colormax

            for i in range(self.nb-1):
                val1 = (self.values[i]-self.values[0])/dval
                val2 = (self.values[i+1]-self.values[0])/dval
                c1   = self.colorsflt[i]
                ij = np.where((xloc>=val1) & (xloc<val2))
                rgba[ij[0],ij[1]] = c1

            return rgba
        else:
            return self(xloc)

    def export_palette_matplotlib(self,name):
        cmaps = OrderedDict()
        cmaps['Perceptually Uniform Sequential'] = ['viridis', 'plasma', 'inferno', 'magma', 'cividis']

        cmaps['Sequential'] = ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds','YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu','GnBu', 'PuBu', 'YlGnBu','PuBuGn', 'BuGn', 'YlGn']
        cmaps['Sequential (2)'] = ['binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink','spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia','hot', 'afmhot', 'gist_heat', 'copper']
        cmaps['Diverging'] = ['PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu','RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']
        cmaps['Cyclic'] = ['twilight', 'twilight_shifted', 'hsv']
        cmaps['Qualitative'] = ['Pastel1', 'Pastel2', 'Paired', 'Accent','Dark2', 'Set1', 'Set2', 'Set3','tab10', 'tab20', 'tab20b', 'tab20c']
        cmaps['Miscellaneous'] = ['flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern','gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg','gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar']

        for cmap_category, cmap_list in cmaps.items():
            if(name in cmaps[cmap_category]):
                self=plt.get_cmap(name)
                self.nb=len(self._segmentdata['blue'])
                self.values = np.linspace(0.,1.,self.nb)
                self.colorsflt = np.zeros((self.nb,4) , dtype=float)
                for i in range(self.nb):
                    self.colorsflt[i,0]=self._segmentdata['red'][i][2]
                    self.colorsflt[i,1]=self._segmentdata['green'][i][2]
                    self.colorsflt[i,2]=self._segmentdata['blue'][i][2]
                    self.colorsflt[i,3]=self._segmentdata['alpha'][i][2]
                test=1
                break
            else:
                test=1

        return self.nb,self.values,self._segmentdata,self.colorsflt

    def distribute_values(self, minval=-99999, maxval=-99999, step=0):

        if self.wx_exists:
            if minval==-99999:
                dlg = wx.TextEntryDialog(None, _('Minimum value'), value = str(self.values[0]))
                ret = dlg.ShowModal()
                self.values[0] = dlg.GetValue()
                dlg.Destroy()

            if maxval==-99999 and step==0:

                dlg = wx.MessageDialog(None, _('Would you like to set the incremental step value ?'),style= wx.YES_NO|wx.YES_DEFAULT)
                ret = dlg.ShowModal()
                dlg.Destroy
                if ret == wx.ID_YES:
                    dlg = wx.TextEntryDialog(None, _('Step value'), value = '1')
                    ret = dlg.ShowModal()
                    step = float(dlg.GetValue())
                    dlg.Destroy()
                else:
                    dlg = wx.TextEntryDialog(None, _('Maximum value'), value = str(self.values[-1]))
                    ret = dlg.ShowModal()
                    self.values[-1] = float(dlg.GetValue())
                    dlg.Destroy()

        if step==0:
            self.values = np.linspace(self.values[0], self.values[-1], num=self.nb, endpoint=True)
        else:
            self.values = np.arange(self.values[0], self.values[0]+(self.nb)*step, step)

        self.fill_segmentdata()

    def export_image(self,fn='',h_or_v:typing.Literal['h','v',''] ='', figax = None):
        """
        Export image from colormap

        :param : fn : filepath or io.BytesIO()
        :param : h_or_v : configuration to save 'h' = horizontal, 'v' = vertical, '' = both
        """
        if fn=='':
            file=wx.FileDialog(None,"Choose .pal file", wildcard="png (*.png)|*.png|all (*.*)|*.*",style=wx.FD_SAVE)
            if file.ShowModal() == wx.ID_CANCEL:
                return
            else:
                #récupération du nom de fichier avec chemin d'accès
                fn =file.GetPath()

        if h_or_v=='v':
            if figax is None:
                fig,ax=plt.subplots(1,1)
            else:
                fig,ax = figax
            plt.colorbar(ScalarMappable(Normalize(self.values[0],self.values[-1]),cmap=self),
                         cax=ax,
                         orientation='vertical',
                         extend='both',
                         aspect=20,
                         spacing='proportional',
                         ticks=self.values,
                         format='%.3f')
            plt.tick_params(labelsize=14)
            if figax is None:
                fig.set_size_inches((2,10))
                fig.tight_layout()

            if fn!='' and fn is not None:
                plt.savefig(fn, format='png')
            # plt.savefig(fn,bbox_inches='tight', format='png')
        elif h_or_v=='h':
            if figax is None:
                fig,ax=plt.subplots(1,1)
            else:
                fig,ax = figax
            plt.colorbar(ScalarMappable(Normalize(self.values[0],self.values[-1]),cmap=self),
                         cax=ax,
                         orientation='horizontal',
                         extend='both',
                         spacing='proportional',
                         ticks=self.values,
                         format='%.3f')
            plt.tick_params(labelsize=14,rotation=45)
            if figax is None:
                fig.set_size_inches((2,10))
                fig.tight_layout()
            if fn!='' and fn is not None:
                plt.savefig(fn, format='png')
            # plt.savefig(fn,bbox_inches='tight', format='png')
        else:
            if isinstance(fn, io.BytesIO):
                logging.warning('Bad type for "fn" - Nothing to do !')
                return

            if figax is None:
                fig,ax=plt.subplots(1,1)
            else:
                fig,ax = figax
            plt.colorbar(ScalarMappable(Normalize(self.values[0],self.values[-1]),cmap=self),
                         cax=ax,
                         orientation='vertical',
                         extend='both',
                         spacing='proportional',
                         ticks=self.values,
                         format='%.3f')
            plt.tick_params(labelsize=14)
            fig.set_size_inches((2,10))
            fig.tight_layout()
            if fn!='' and fn is not None:
                plt.savefig(fn[:-4]+'_v.png', format='png')

            if figax is None:
                fig,ax=plt.subplots(1,1)
            else:
                fig,ax = figax

            plt.colorbar(ScalarMappable(Normalize(self.values[0],self.values[-1]),cmap=self),
                         cax=ax,
                         orientation='horizontal',
                         extend='both',
                         spacing='proportional',
                         ticks=self.values,
                         format='%.3f')
            plt.tick_params(labelsize=14,rotation=45)
            fig.set_size_inches((10,2))
            fig.tight_layout()
            if fn!='' and fn is not None:
                plt.savefig(fn[:-4]+'_h.png', format='png')

        return fig,ax

    def plot(self,fig:Figure,ax:plt.Axes):
        gradient = np.linspace(0, 1, 256)
        gradient = np.vstack((gradient, gradient))
        ax.imshow(gradient, aspect='auto', cmap=self)
        ax.set_yticklabels([])

        pos=[]
        txt=[]

        dval=(self.values[-1]-self.values[0])
        if dval==0.:
            dval=1.

        for curval in self.values:
            pos.append((curval-self.values[0])/dval*256.)
            txt.append("{0:.3f}".format(curval))

        ax.set_xticks(pos)
        ax.set_xticklabels(txt,rotation=30,fontsize=6)

    def fillgrid(self,gridto:CpGrid):
        gridto.SetColLabelValue(0,'Value')
        gridto.SetColLabelValue(1,'R')
        gridto.SetColLabelValue(2,'G')
        gridto.SetColLabelValue(3,'B')

        nb=gridto.GetNumberRows()
        if len(self.values)-nb>0:
            gridto.AppendRows(len(self.values)-nb)

        k=0
        for curv,rgba in zip(self.values,self.colors):
            gridto.SetCellValue(k,0,str(curv))
            gridto.SetCellValue(k,1,str(rgba[0]))
            gridto.SetCellValue(k,2,str(rgba[1]))
            gridto.SetCellValue(k,3,str(rgba[2]))
            k+=1

    def updatefromgrid(self,gridfrom:CpGrid):
        nbl=gridfrom.GetNumberRows()

        for i in range(nbl):
            if gridfrom.GetCellValue(i,0) =='':
                nbl=i-1
                break

        if i < self.nb-1:
            self.nb = i
            self.values=self.values[0:i]
            self.colors=self.colors[0:i,:]

        update = False

        for k in range(self.nb):

            update = update or self.values[k]!=float(gridfrom.GetCellValue(k,0))
            update = update or self.colors[k,0]!=float(gridfrom.GetCellValue(k,1))
            update = update or self.colors[k,1]!=float(gridfrom.GetCellValue(k,2))
            update = update or self.colors[k,2]!=float(gridfrom.GetCellValue(k,3))

            self.values[k]=float(gridfrom.GetCellValue(k,0))
            self.colors[k,0]=int(gridfrom.GetCellValue(k,1))
            self.colors[k,1]=int(gridfrom.GetCellValue(k,2))
            self.colors[k,2]=int(gridfrom.GetCellValue(k,3))

        self.fill_segmentdata()

        return update

    def updatefrompalette(self,srcpal):
        """
        Mise à jour de la palette sur base d'une autre

        On copie les valeurs, on ne pointe pas l'objet
        """
        for k in range(len(srcpal.values)):
            self.values[k]=srcpal.values[k]

        self.fill_segmentdata()

    def lookupcolor(self,x):
        if x < self.values[0]:  return wx.Colour(self.colormin)
        if x > self.values[-1]: return wx.Colour(self.colormax)

        i = bisect_left(self.values, x)
        k = (x - self.values[i-1])/(self.values[i] - self.values[i-1])

        r=int(k*(float(self.colors[i,0]-self.colors[i-1,0]))) + self.colors[i-1,0]
        g=int(k*(float(self.colors[i,1]-self.colors[i-1,1]))) + self.colors[i-1,1]
        b=int(k*(float(self.colors[i,2]-self.colors[i-1,2]))) + self.colors[i-1,2]
        a=int(k*(float(self.colors[i,3]-self.colors[i-1,3]))) + self.colors[i-1,3]

        y = wx.Colour(r,g,b,a)

        return y

    def lookupcolorflt(self,x):
        if x < self.values[0]:  return wx.Colour(self.colormin)
        if x > self.values[-1]: return wx.Colour(self.colormax)

        i = bisect_left(self.values, x)
        k = (x - self.values[i-1])/(self.values[i] - self.values[i-1])

        r=k*(self.colorsflt[i,0]-self.colorsflt[i-1,0]) + self.colorsflt[i-1,0]
        g=k*(self.colorsflt[i,1]-self.colorsflt[i-1,1]) + self.colorsflt[i-1,1]
        b=k*(self.colorsflt[i,2]-self.colorsflt[i-1,2]) + self.colorsflt[i-1,2]
        a=k*(self.colorsflt[i,3]-self.colorsflt[i-1,3]) + self.colorsflt[i-1,3]

        y=[r,g,b,a]
        return y

    def lookupcolorrgb(self,x):
        if x < self.values[0]:  return wx.Colour(self.colormin)
        if x > self.values[-1]: return wx.Colour(self.colormax)

        i = bisect_left(self.values, x)
        k = (x - self.values[i-1])/(self.values[i] - self.values[i-1])

        r=int(k*(float(self.colors[i,0]-self.colors[i-1,0]))) + self.colors[i-1,0]
        g=int(k*(float(self.colors[i,1]-self.colors[i-1,1]))) + self.colors[i-1,1]
        b=int(k*(float(self.colors[i,2]-self.colors[i-1,2]))) + self.colors[i-1,2]
        a=int(k*(float(self.colors[i,3]-self.colors[i-1,3]))) + self.colors[i-1,3]

        return r,g,b,a

    def default16(self):
        """Palette 16 coulrurs par défaut dans WOLF"""
        self.nb=16
        self.values = np.linspace(0.,1.,16)
        self.colors = np.zeros((self.nb,4) , dtype=int)
        self.colorsflt = np.zeros((self.nb,4) , dtype=float)

        self.colors[0,:] = [128,255,255,255]
        self.colors[1,:] = [89,172,255,255]
        self.colors[2,:] = [72,72,255,255]
        self.colors[3,:] = [0,0,255,255]
        self.colors[4,:] = [0,128,0,255]
        self.colors[5,:] = [0,221,55,255]
        self.colors[6,:] = [128,255,128,255]
        self.colors[7,:] = [255,255,0,255]
        self.colors[8,:] = [255,128,0,255]
        self.colors[9,:] = [235,174,63,255]
        self.colors[10,:] = [255,0,0,255]
        self.colors[11,:] = [209,71,12,255]
        self.colors[12,:] = [128,0,0,255]
        self.colors[13,:] = [185,0,0,255]
        self.colors[14,:] = [111,111,111,255]
        self.colors[15,:] = [192,192,192,255]

        self.fill_segmentdata()

    def defaultgray(self):
        """Palette 16 coulrurs par défaut dans WOLF"""
        self.nb=2
        self.values = np.asarray([0.,1.])
        self.colors = np.asarray([[0,0,0,255],[255,255,255,255]],dtype=np.int32)
        self.colorsflt = np.asarray([[0.,0.,0.,1.],[1.,1.,1.,1.]],dtype=np.float64)

        self.fill_segmentdata()

    def fill_segmentdata(self):
        """Mise à jour de la palatte de couleurs"""

        self.colorsflt = self.colors.astype(float)/255.

        dval=self.values[-1]-self.values[0]

        normval = np.ones([len(self.values)])

        if dval>0.:
            normval = (self.values-self.values[0])/(self.values[-1]-self.values[0])

        normval[0]=0.
        normval[-1]=1.
        segmentdata = {"red": np.column_stack([normval, self.colorsflt[:,0], self.colorsflt[:,0]]),
                             "green": np.column_stack([normval, self.colorsflt[:,1], self.colorsflt[:,1]]),
                             "blue": np.column_stack([normval, self.colorsflt[:,2], self.colorsflt[:,2]]),
                             "alpha": np.column_stack([normval, self.colorsflt[:,3], self.colorsflt[:,3]])}

        LinearSegmentedColormap.__init__(self,'wolf',segmentdata,self.nseg)

    def readfile(self,*args):
        """Lecture de la palette sur base d'un fichier WOLF .pal"""
        if len(args)>0:
            #s'il y a un argument on le prend tel quel
            self.filename = str(args[0])
        else:
            if self.wx_exists:
                #ouverture d'une boîte de dialogue
                file=wx.FileDialog(None,"Choose .pal file", wildcard="pal (*.pal)|*.pal|all (*.*)|*.*")
                if file.ShowModal() == wx.ID_CANCEL:
                    file.Destroy()
                    return
                else:
                    #récuparétaion du nom de fichier avec chemin d'accès
                    self.filename =file.GetPath()
                    file.Destroy()
            else:
                return

        #lecture du contenu
        with open(self.filename, 'r') as myfile:
            #split des lignes --> récupération des infos sans '\n' en fin de ligne
            #  différent de .readlines() qui lui ne supprime pas les '\n'
            mypallines = myfile.read().splitlines()
            myfile.close()

            self.nb = int(mypallines[0])
            self.values = np.zeros(self.nb , dtype=float)
            self.colors = np.zeros((self.nb,4) , dtype=int)

            for i in range(self.nb):
                self.values[i] = mypallines[i*4+1]
                self.colors[i,0] = mypallines[i*4+2]
                self.colors[i,1] = mypallines[i*4+3]
                self.colors[i,2] = mypallines[i*4+4]
                self.colors[i,3] = 255

        self.fill_segmentdata()

    def savefile(self,*args):
        """Lecture de la palette sur base d'un fichier WOLF .pal"""
        if len(args)>0:
            #s'il y a un argument on le prend tel quel
            fn = str(args[0])
        else:
            #ouverture d'une boîte de dialogue
            file=wx.FileDialog(None,"Choose .pal file", wildcard="pal (*.pal)|*.pal|all (*.*)|*.*",style=wx.FD_SAVE)
            if file.ShowModal() == wx.ID_CANCEL:
                return
            else:
                #récuparétaion du nom de fichier avec chemin d'accès
                fn =file.GetPath()

        self.filename=fn

        #lecture du contenu
        with open(self.filename, 'w') as myfile:
            #split des lignes --> récupération des infos sans '\n' en fin de ligne
            #  différent de .readlines() qui lui ne supprime pas les '\n'
            myfile.write(str(self.nb)+'\n')
            for i in range(self.nb):
                myfile.write(str(self.values[i])+'\n')
                myfile.write(str(self.colors[i,0])+'\n')
                myfile.write(str(self.colors[i,1])+'\n')
                myfile.write(str(self.colors[i,2])+'\n')

    def isopop(self, array: ma.masked_array, nbnotnull:int=99999):
        """Remplissage des valeurs de palette sur base d'une équirépartition de valeurs"""

        sortarray = array.flatten(order='F')

        idx_nan = np.where(np.isnan(sortarray))
        if idx_nan[0].size > 0:
            sortarray = np.delete(sortarray, idx_nan)
            nbnotnull -= idx_nan[0].size
            logging.warning('NaN values found in array - removed from palette')

        sortarray.sort(axis=-1)

        #valeurs min et max
        if nbnotnull == 0:
            self.values[0] = 0
            self.values[1:] = 1

        else:
            self.values[0] = sortarray[0]

            if(nbnotnull==99999):
                self.values[-1] = sortarray[-1]
                nb = sortarray.count()
            else:
                self.values[-1] = sortarray[nbnotnull-1]
                nb = nbnotnull

            interv = int(nb / (self.nb-1))
            if interv==0:
                self.values[:] = self.values[-1]
                self.values[0] = self.values[-1]-1.
            else:
                for cur in range(1,self.nb-1):
                    self.values[cur] = sortarray[cur * interv]

        self.fill_segmentdata()

    def defaultgray_minmax(self,array: ma.masked_array,nbnotnull=99999):
        """Remplissage des valeurs de palette sur base d'une équirépartition de valeurs"""

        self.nb=2
        self.values = np.asarray([np.min(array),np.max(array)])
        self.colors = np.asarray([[0,0,0,255],[255,255,255,255]],dtype=np.int32)
        self.colorsflt = np.asarray([[0.,0.,0.,1.],[1.,1.,1.,1.]],dtype=np.float64)

        self.fill_segmentdata()

    def defaultblue_minmax(self,array: ma.masked_array,nbnotnull=99999):
        """Remplissage des valeurs de palette sur base d'une équirépartition de valeurs"""

        self.nb=2
        self.values = np.asarray([np.min(array),np.max(array)])
        self.colors = np.asarray([[255,255,255,255],[0,0,255,255]],dtype=np.int32)
        self.colorsflt = np.asarray([[0.,0.,0.,1.],[1.,1.,1.,1.]],dtype=np.float64)

        self.fill_segmentdata()

    def defaultblue(self):
        """Remplissage des valeurs de palette sur base d'une équirépartition de valeurs"""

        self.nb=2
        self.values = np.asarray([0.,1.])
        self.colors = np.asarray([[255,255,255,255],[0,0,255,255]],dtype=np.int32)
        self.colorsflt = np.asarray([[0.,0.,0.,1.],[1.,1.,1.,1.]],dtype=np.float64)

        self.fill_segmentdata()
