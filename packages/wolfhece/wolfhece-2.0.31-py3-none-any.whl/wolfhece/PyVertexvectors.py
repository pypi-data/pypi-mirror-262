from os import path
from typing import Union
import numpy as np
import wx
from wx.dataview import *
from wx.core import BoxSizer, FlexGridSizer, TreeItemId
from OpenGL.GL  import *
from shapely.geometry import LineString, MultiLineString,Point,MultiPoint,Polygon,JOIN_STYLE, MultiPolygon
from shapely.ops import nearest_points,substring, split
import pygltflib
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import struct
import pyvista as pv
from typing import Union, Literal
import logging
from tqdm import tqdm
import copy
import geopandas as gpd
import io
from typing import Union, Literal
from pathlib import Path

from .textpillow import Font_Priority
from .PyTranslate import _
from .CpGrid import CpGrid
from .PyVertex import wolfvertex,getIfromRGB,getRGBfromI
from .PyParams import Wolf_Param, key_Param, Type_Param
from .lazviewer.laz_viewer import myviewer
from .wolf_texture import Text_Image_Texture,Text_Infos
from .drawing_obj import Element_To_Draw

class Triangulation(Element_To_Draw):
    def __init__(self, fn='', pts=[],tri=[], idx: str = '', plotted: bool = True, mapviewer=None, need_for_wx: bool = False) -> None:
        super().__init__(idx, plotted, mapviewer, need_for_wx)

        self.filename = ''
        self.tri= tri
        self.pts = pts
        self.id_list = -99999

        self.nb_tri = len(tri)
        self.nb_pts = len(pts)

        if fn !='':
            self.filename=fn
            self.read(fn)
        pass

    def valid_format(self):
        if isinstance(self.pts,list):
            self.pts = np.asarray(self.pts)
        if isinstance(self.tri,list):
            self.tri = np.asarray(self.tri)

    def as_polydata(self) -> pv.PolyData:

        return pv.PolyData(np.asarray(self.pts),np.column_stack([[3]*self.nb_tri,self.tri]), self.nb_tri)

    def from_polydata(self,poly:pv.PolyData):

        self.pts = np.asarray(poly.points.copy())
        self.tri = np.asarray(poly.faces.reshape([int(len(poly.faces)/4),4])[:,1:4])

        self.nb_pts = len(self.pts)
        self.nb_tri = len(self.tri)

    def clip_surface(self,other,invert=True,subdivide=0):

        if subdivide==0:
            mypoly = self.as_polydata()
            mycrop = other.as_polydata()
        else:
            mypoly = self.as_polydata().subdivide(subdivide)
            mycrop = other.as_polydata().subdivide(subdivide)

        res = mypoly.clip_surface(mycrop,invert=invert)

        if len(res.faces)>0:
            self.from_polydata(res)
        else:
            return None

    def get_mask(self,eps=1e-10):
        """
        Teste si la surface de tous les triangles est positive

        Retire les triangles problématiques
        """

        if self.nb_tri>0:
            v1 = [self.pts[curtri[1]][:2] - self.pts[curtri[0]][:2] for curtri in self.tri]
            v2 = [self.pts[curtri[2]][:2] - self.pts[curtri[0]][:2] for curtri in self.tri]
            self.areas = np.cross(v2,v1,)/2
            return self.areas<=eps

            # invalid_tri = np.sort(np.where(self.areas<=eps)[0])
            # for curinv in invalid_tri[::-1]:
            #     self.tri.pop(curinv)

            # self.nb_tri = len(self.tri)

    def import_from_gltf(self, fn=''):

        if fn =='':
            dlg=wx.FileDialog(None,_('Choose filename'),wildcard='binary gltf2 (*.glb)|*.glb|gltf2 (*.gltf)|*.gltf|All (*.*)|*.*',style=wx.FD_OPEN)
            ret=dlg.ShowModal()
            if ret==wx.ID_CANCEL:
                dlg.Destroy()
                return

            fn=dlg.GetPath()
            dlg.Destroy()

        gltf = pygltflib.GLTF2().load(fn)

        # get the first mesh in the current scene
        mesh = gltf.meshes[gltf.scenes[gltf.scene].nodes[0]]

        # get the vertices for each primitive in the mesh
        for primitive in mesh.primitives:

            # get the binary data for this mesh primitive from the buffer
            accessor = gltf.accessors[primitive.attributes.POSITION]

            bufferView = gltf.bufferViews[accessor.bufferView]
            buffer = gltf.buffers[bufferView.buffer]
            data = gltf.get_data_from_buffer_uri(buffer.uri)

            # pull each vertex from the binary buffer and convert it into a tuple of python floats
            points = np.zeros([accessor.count, 3], order='F', dtype=np.float64)
            for i in range(accessor.count):
                index = bufferView.byteOffset + accessor.byteOffset + i * 12  # the location in the buffer of this vertex
                d = data[index:index + 12]  # the vertex data
                v = struct.unpack("<fff", d)  # convert from base64 to three floats

                points[i, :] = np.asarray([v[0], -v[2], v[1]])

            accessor = gltf.accessors[primitive.indices]

            bufferView = gltf.bufferViews[accessor.bufferView]
            buffer = gltf.buffers[bufferView.buffer]
            data = gltf.get_data_from_buffer_uri(buffer.uri)

            triangles = []
            if accessor.componentType==pygltflib.UNSIGNED_SHORT:
                size=6
                format='<HHH'
            elif accessor.componentType==pygltflib.UNSIGNED_INT:
                size=12
                format='<LLL'

            for i in range(int(accessor.count/3)):

                index = bufferView.byteOffset + accessor.byteOffset + i*size  # the location in the buffer of this vertex
                d = data[index:index+size]  # the vertex data
                v = struct.unpack(format, d)   # convert from base64 to three floats
                triangles.append(list(v))

        # On souhaite obtenir une triangulation du type :
        #   - liste de coordonnées des sommets des triangles
        #   - par triangle, liste de 3 indices, un pour chaque sommet
        #
        # Si le fichier GLTF vient de Blender, il y aura des informations de normales ...
        # Il est donc préférable de filtrer les points pour ne garder que des valeurs uniques
        # On ne souhaite pas gérer le GLTF dans toute sa généralité mais uniquement la triangulation de base
        xyz_u,indices = np.unique(np.array(points),return_inverse=True,axis=0)
        triangles = [[indices[curtri[0]],indices[curtri[1]],indices[curtri[2]]] for curtri in list(triangles)]

        self.pts = xyz_u
        self.tri = triangles

        self.nb_pts = len(self.pts)
        self.nb_tri = len(self.tri)

    def export_to_gltf(self,fn=''):

        #on force les types de variables
        triangles = np.asarray(self.tri).astype(np.uint32)
        points = np.column_stack([self.pts[:,0],self.pts[:,2],-self.pts[:,1]]).astype(np.float32)

        triangles_binary_blob = triangles.flatten().tobytes()
        points_binary_blob = points.flatten().tobytes()

        gltf = pygltflib.GLTF2(
            scene=0,
            scenes=[pygltflib.Scene(nodes=[0])],
            nodes=[pygltflib.Node(mesh=0)],
            meshes=[
                pygltflib.Mesh(
                    primitives=[
                        pygltflib.Primitive(
                            attributes=pygltflib.Attributes(POSITION=1), indices=0
                        )
                    ]
                )
            ],
            accessors=[
                pygltflib.Accessor(
                    bufferView=0,
                    componentType=pygltflib.UNSIGNED_INT,
                    count=self.nb_tri*3,
                    type=pygltflib.SCALAR,
                    max=[int(triangles.max())],
                    min=[int(triangles.min())],
                ),
                pygltflib.Accessor(
                    bufferView=1,
                    componentType=pygltflib.FLOAT,
                    count=self.nb_pts,
                    type=pygltflib.VEC3,
                    max=points.max(axis=0).tolist(),
                    min=points.min(axis=0).tolist(),
                ),
            ],
            bufferViews=[
                pygltflib.BufferView(
                    buffer=0,
                    byteLength=len(triangles_binary_blob),
                    target=pygltflib.ELEMENT_ARRAY_BUFFER,
                ),
                pygltflib.BufferView(
                    buffer=0,
                    byteOffset=len(triangles_binary_blob),
                    byteLength=len(points_binary_blob),
                    target=pygltflib.ARRAY_BUFFER,
                ),
            ],
            buffers=[
                pygltflib.Buffer(
                    byteLength=len(triangles_binary_blob) + len(points_binary_blob)
                )
            ],
        )
        gltf.set_binary_blob(triangles_binary_blob + points_binary_blob)

        if fn =='':
            dlg=wx.FileDialog(None,_('Choose filename'),wildcard='binary gltf2 (*.glb)|*.glb|gltf2 (*.gltf)|*.gltf|All (*.*)|*.*',style=wx.FD_SAVE)
            ret=dlg.ShowModal()
            if ret==wx.ID_CANCEL:
                dlg.Destroy()
                return

            fn=dlg.GetPath()
            dlg.Destroy()

        gltf.save(fn)
        return fn

    def saveas(self,fn=''):
        """
        Binary '.TRI' format on disk is, little endian :
           - int32 for number of points
           - int32 as 64 ou 32 for float64 or float32
           - VEC3 (float64 or float32) for points
           - int32 for number of triangles
           - VEC3 uint32  for triangles
        """
        if self.filename=='' and fn=='':
            return

        if fn!='':
            self.filename=fn

        triangles = np.asarray(self.tri).astype(np.uint32)
        points = np.asarray(self.pts) #.astype(np.float64)

        with open(self.filename,'wb') as f:
            f.write(self.nb_pts.to_bytes(4,'little'))

            if points.dtype == np.float64:
                f.write(int(64).to_bytes(4,'little'))
            else:
                f.write(int(32).to_bytes(4,'little'))
            points.tofile(f,"")

            f.write(self.nb_tri.to_bytes(4,'little'))
            triangles.tofile(f,"")

    def read(self,fn:str):

        if fn.endswith('.dxf'):
            self.import_dxf(fn)
        elif fn.endswith('.gltf') or fn.endswith('.glb'):
            self.import_from_gltf(fn)
        elif fn.endswith('.tri'):
            with open(fn,'rb') as f:
                self.nb_pts = int.from_bytes(f.read(4),'little')
                which_type = int.from_bytes(f.read(4),'little')
                if which_type == 64:
                    buf = np.frombuffer(f.read(8 * self.nb_pts * 3), dtype=np.float64)
                    self.pts = np.array(buf.copy(), dtype=np.float64).reshape([self.nb_pts,3])
                elif which_type == 32:
                    buf = np.frombuffer(f.read(4 * self.nb_pts * 3), dtype=np.float32)
                    self.pts = np.array(buf.copy(), dtype=np.float32).reshape([self.nb_pts,3]).astype(np.float64)

                self.nb_tri = int.from_bytes(f.read(4),'little')
                buf = np.frombuffer(f.read(4 * self.nb_tri * 3), dtype=np.uint32)
                self.tri = np.array(buf.copy(), dtype=np.uint32).reshape([self.nb_tri,3]).astype(np.int32)

        self.valid_format()
        self.find_minmax(True)
        self.reset_plot()

    def reset_plot(self):
        try:
            if self.id_list!=-99999:
                glDeleteLists(self.id_list)
        except:
            pass

        self.id_list = -99999

    def plot(self, sx=None, sy=None, xmin=None, ymin=None, xmax=None, ymax=None, size=None ):

        if self.id_list == -99999:
            self.id_list = glGenLists(1)

            glNewList(self.id_list, GL_COMPILE)

            glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)

            for curtri in self.tri:
                glBegin(GL_LINE_STRIP)

                glColor3ub(int(0),int(0),int(0))

                glVertex2d(self.pts[curtri[0]][0], self.pts[curtri[0]][1])
                glVertex2d(self.pts[curtri[1]][0], self.pts[curtri[1]][1])
                glVertex2d(self.pts[curtri[2]][0], self.pts[curtri[2]][1])
                glVertex2d(self.pts[curtri[0]][0], self.pts[curtri[0]][1])

                glEnd()

            glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)

            glEndList()
        else:
            glCallList(self.id_list)

    def find_minmax(self,force):
        if force:
            if self.nb_pts>0:
                self.xmin=np.min(self.pts[:,0])
                self.ymin=np.min(self.pts[:,1])
                self.xmax=np.max(self.pts[:,0])
                self.ymax=np.max(self.pts[:,1])

    def import_dxf(self,fn):
        import ezdxf

        if not path.exists(fn):
            logging.warning(_('File not found !') + ' ' + fn)
            return

        # Lecture du fichier dxf et identification du modelspace
        doc = ezdxf.readfile(fn)
        msp = doc.modelspace()

        # Liste de stockage des coordonnées des faces 3D
        xyz = []

        # Bouclage sur les éléments du DXF
        for e in msp:
            if e.dxftype() == "3DFACE":
                # récupération des coordonnées
                # --> on suppose que ce sont des triangles (!! une face3D peut être un quadrangle !! on oublie donc la 4ème coord)
                xyz += [e[0],e[1],e[2]]

        # On souhaite obtenir une triangulation du type :
        #   - liste de coordonnées des sommets des triangles
        #   - par triangle, liste de 3 indices, un pour chaque sommet
        #
        # Actuellement, les coordonnées sont multipliées car chaque face a été extraite indépendamment
        # On commence donc par identifier les coordonnées uniques, par tuple
        # return_inverse permet de constituer la liste d'indices efficacement
        #
        xyz_u,indices = np.unique(np.array(xyz),return_inverse=True,axis=0)
        triangles = indices.reshape([int(len(indices)/3),3])

        self.tri = triangles.astype(np.int32)
        self.pts = xyz_u
        self.nb_pts = len(self.pts)
        self.nb_tri = len(self.tri)
        self.valid_format()
class vectorproperties:
    """ Vector properties """
    used:bool

    color:int
    width:int
    style:int
    alpha:int
    closed=bool
    filled:bool
    legendvisible:bool
    transparent:bool
    flash:bool

    legendtext:str
    legendrelpos:int
    legendx:float
    legendy:float

    legendbold:bool
    legenditalic:bool
    legendunderlined:bool
    legendfontname=str
    legendfontsize:int
    legendcolor:int

    extrude:bool = False

    myprops:Wolf_Param = None

    def __init__(self, lines:list[str]=[], parent:"vector"=None) -> None:
        """
        Init the vector properties -- Compatibility with VB6, Fortran codes --> Modify with care

        :param lines: list of lines from a file
        :param parent: parent vector
        """

        self.parent:vector
        self.parent=parent

        if len(lines)>0:
            line1=lines[0].split(',')
            line2=lines[1].split(',')

            self.color=int(line1[0])
            self.width=int(line1[1])
            self.style=int(line1[2])
            self.closed=line1[3]=='#TRUE#'
            self.filled=line1[4]=='#TRUE#'
            self.legendvisible=line1[5]=='#TRUE#'
            self.transparent=line1[6]=='#TRUE#'
            self.alpha=int(line1[7])
            self.flash=line1[8]=='#TRUE#'

            self.legendtext=line2[0]
            self.legendrelpos=int(line2[1])
            self.legendx=float(line2[2])
            self.legendy=float(line2[3])
            self.legendbold=line2[4]=='#TRUE#'
            self.legenditalic=line2[5]=='#TRUE#'
            self.legendfontname=str(line2[6])
            self.legendfontsize=int(line2[7])
            self.legendcolor=int(line2[8])
            self.legendunderlined=line2[9]=='#TRUE#'

            self.used=lines[2]=='#TRUE#'
        else:
            # default values in case of new vector
            self.color=0
            self.width=1
            self.style=1
            self.closed=False
            self.filled=False
            self.legendvisible=False
            self.transparent=False
            self.alpha=0
            self.flash=False

            self.legendtext=''
            self.legendrelpos=5
            self.legendx=0.
            self.legendy=0.
            self.legendbold=False
            self.legenditalic=False
            self.legendfontname='Arial'
            self.legendfontsize=10
            self.legendcolor=0
            self.legendunderlined=False

            self.used=True

        self.init_extra()

    def init_extra(self):
        """
        Init extra properties --> not compatible with VB6, Fortran codes

        Useful for Python UI, OpenGL legend, etc.
        """
        self.legendlength = 100.
        self.legendheight = 100.
        self.legendpriority = 2
        self.legendorientation = 0.

    def get_extra(self) -> list[float,float,int,float]:
        """ Return extra properties """
        return [self.legendlength,
                self.legendheight,
                self.legendpriority,
                self.legendorientation]

    def set_extra(self, linesextra:list[float,float,int,float] = None):
        """ Set extra properties """

        if linesextra is None:
            return

        assert len(linesextra)==4, 'Extra properties must be a list of [float, float, int, float]'

        self.legendlength = float(linesextra[0])
        self.legendheight = float(linesextra[1])
        self.legendpriority = float(linesextra[2])
        self.legendorientation = float(linesextra[3])


    def save_extra(self, f:io.TextIOWrapper):
        """ Save extra properties to opened file """

        extras = self.get_extra()

        f.write(self.parent.myname+'\n')
        f.write('{}\n'.format(len(extras)))
        for curextra in extras:
            f.write('{}'.format(curextra)+'\n')

    def save(self, f:io.TextIOWrapper):
        """
        Save properties to opened file

        Pay attention to the order of the lines and the format to be compatible with VB6, Fortran codes
        """
        line1 = str(self.color) + ',' + str(self.width)+','+ str(self.style)

        added = ',#TRUE#' if self.closed else ',#FALSE#'
        line1+=added
        added = ',#TRUE#' if self.filled else ',#FALSE#'
        line1+=added
        added = ',#TRUE#' if self.legendvisible else ',#FALSE#'
        line1+=added
        added = ',#TRUE#' if self.transparent else ',#FALSE#'
        line1+=added
        line1+=','+str(self.alpha)
        added = ',#TRUE#' if self.flash else ',#FALSE#'
        line1+=added

        f.write(line1+'\n')

        line1 = self.legendtext + ',' + str(self.legendrelpos)+','+ str(self.legendx)+','+ str(self.legendy)
        added = ',#TRUE#' if self.legendbold else ',#FALSE#'
        line1+=added
        added = ',#TRUE#' if self.legenditalic else ',#FALSE#'
        line1+=added
        line1+= ','+self.legendfontname + ',' + str(self.legendfontsize)+ ',' + str(self.legendcolor)
        added = ',#TRUE#' if self.legendunderlined else ',#FALSE#'
        line1+=added

        f.write(line1+'\n')

        added = '#TRUE#' if self.used else '#FALSE#'
        f.write(added+'\n')

    def fill_property(self):
        """
        Callback for the properties UI

        When the 'Apply' button is pressed, this function is called
        """
        props = self.myprops

        self.color = getIfromRGB(props[('Draw','Color')])
        self.width = props[('Draw','Width')]
        self.style = props[('Draw','Style')]
        self.closed = props[('Draw','Closed')]
        self.filled = props[('Draw','Filled')]
        self.transparent = props[('Draw','Transparent')]
        self.alpha = props[('Draw','Alpha')]
        self.flash = props[('Draw','Flash')]

        self.legendunderlined = props[('Legend','Underlined')]
        self.legendbold = props[('Legend','Bold')]
        self.legendfontname = props[('Legend','Font name')]
        self.legendfontsize = props[('Legend','Font size')]
        self.legendcolor = getIfromRGB(self.myprops[('Legend','Color')])
        self.legenditalic = props[('Legend','Italic')]
        self.legendrelpos = props[('Legend','relative Position')]
        self.legendtext = props[('Legend','Text')]
        self.legendvisible = props[('Legend','Visible')]
        self.legendx = props[('Legend','X')]
        self.legendy = props[('Legend','Y')]

        self.legendlength = props[('Legend','Length')]
        self.legendheight = props[('Legend','Height')]
        self.legendpriority = props[('Legend','Priority')]
        self.legendorientation = props[('Legend','Orientation')]

        if self.legendvisible:
            self.parent.textimage = Text_Image_Texture(self.legendtext,
                                                self.parent.parentzone.parent.mapviewer, # mapviewer de l'instance Zones qui contient le vecteur
                                                self.get_textfont(),
                                                self.parent,
                                                self.legendx,
                                                self.legendy)
        else:
            self.parent.textimage=None

        try:
            self.parent.parentzone.parent.mapviewer.Refresh()
        except:
            pass

    def get_textfont(self):
        """ Retunr a 'Text_Infos' instance for the legend """

        r,g,b = getRGBfromI(self.legendcolor)
        return Text_Infos(self.legendpriority,
                          (np.cos(self.legendorientation/180*np.pi),np.sin(self.legendorientation/180*np.pi)),
                          self.legendfontname.lower().endswith('.ttf'),
                          self.legendfontsize,
                          colour=(r,g,b,255),
                          dimsreal=(self.legendlength,self.legendheight))

    def _defaultprop(self):
        """
        Create the default properties for the vector and the associated UI
        """

        if self.myprops is None:
            self.myprops=Wolf_Param(title='Vector Properties', w=500, h=800, to_read=False)
            self.myprops.show_in_active_if_default = True
            self.myprops._callbackdestroy = self.destroyprop
            self.myprops._callback=self.fill_property

            self.myprops.hide_selected_buttons() # only 'Apply' button
            # self.myprops.saveme.Disable()
            # self.myprops.loadme.Disable()
            # self.myprops.reloadme.Disable()

        self.myprops.addparam('Draw','Color',(0,0,0),'Color','Drawing color',whichdict='Default')
        self.myprops.addparam('Draw','Width',1,'Integer','Drawing width',whichdict='Default')
        self.myprops.addparam('Draw','Style',1,'Integer','Drawing style',whichdict='Default')
        self.myprops.addparam('Draw','Closed',False,'Logical','',whichdict='Default')
        self.myprops.addparam('Draw','Filled',False,'Logical','',whichdict='Default')
        self.myprops.addparam('Draw','Transparent',False,'Logical','',whichdict='Default')
        self.myprops.addparam('Draw','Alpha',0,'Integer','Transparency intensity (255 is opaque)',whichdict='Default')
        self.myprops.addparam('Draw','Flash',False,'Logical','',whichdict='Default')

        self.myprops.addparam('Legend','Visible',False,'Logical','',whichdict='Default')
        self.myprops.addparam('Legend','Text','','String','',whichdict='Default')
        self.myprops.addparam('Legend','relative Position',5,'Integer','',whichdict='Default')
        self.myprops.addparam('Legend','X',0,'Float','',whichdict='Default')
        self.myprops.addparam('Legend','Y',0,'Float','',whichdict='Default')
        self.myprops.addparam('Legend','Bold',False,'Logical','',whichdict='Default')
        self.myprops.addparam('Legend','Italic',False,'Logical','',whichdict='Default')
        self.myprops.addparam('Legend','Font name','Arial', 'String','',whichdict='Default')
        self.myprops.addparam('Legend','Font size',10,'Integer','',whichdict='Default')
        self.myprops.addparam('Legend','Color',(0,0,0),'Color','',whichdict='Default')
        self.myprops.addparam('Legend','Underlined',False,'Logical','',whichdict='Default')
        self.myprops.addparam('Legend','Length',0,'Float','',whichdict='Default')
        self.myprops.addparam('Legend','Height',0,'Float','',whichdict='Default')
        self.myprops.addparam('Legend','Priority',2,'Integer','',whichdict='Default')
        self.myprops.addparam('Legend','Orientation',0,'Float','',whichdict='Default')

    def destroyprop(self):
        """
        Nullify the properties UI

        Destroy has been called, so the UI is not visible anymore
        """
        self.myprops=None

    def show(self):
        """
        Show the properties

        Firstly, set default values
        Then, add the current properties to the UI
        """
        self._defaultprop()

        self.myprops.addparam('Draw','Color',getRGBfromI(self.color),'Color','Drawing color')
        self.myprops.addparam('Draw','Width',self.width,'Integer','Drawing width')
        self.myprops.addparam('Draw','Style',self.style,'Integer','Drawing style')
        self.myprops.addparam('Draw','Closed',self.closed,'Logical','')
        self.myprops.addparam('Draw','Filled',self.filled,'Logical','')
        self.myprops.addparam('Draw','Transparent',self.transparent,'Logical','')
        self.myprops.addparam('Draw','Alpha',self.alpha,'Integer','Transparent intensity')
        self.myprops.addparam('Draw','Flash',self.flash,'Logical','')

        self.myprops.addparam('Legend','Visible',self.legendvisible,'Logical','')
        self.myprops.addparam('Legend','Text',self.legendtext,'String','')
        self.myprops.addparam('Legend','relative Position',self.legendrelpos,'Integer','')
        self.myprops.addparam('Legend','X',self.legendx,'Float','')
        self.myprops.addparam('Legend','Y',self.legendy,'Float','')
        self.myprops.addparam('Legend','Bold',self.legendbold,'Logical','')
        self.myprops.addparam('Legend','Italic',self.legenditalic,'Logical','')
        self.myprops.addparam('Legend','Font name',self.legendfontname,'String','')
        self.myprops.addparam('Legend','Font size',self.legendfontsize,'Integer','')
        self.myprops.addparam('Legend','Color',getRGBfromI(self.legendcolor),'Color','')
        self.myprops.addparam('Legend','Underlined',self.legendunderlined,'Logical','')

        self.myprops.addparam('Legend','Length',self.legendlength,'Float','')
        self.myprops.addparam('Legend','Height',self.legendheight,'Float','')
        self.myprops.addparam('Legend','Priority',self.legendpriority,'Integer','')
        self.myprops.addparam('Legend','Orientation',self.legendorientation,'Float','')

        self.myprops.Populate()
        self.myprops.Layout()
        self.myprops.SetSizeHints(500,800)
        self.myprops.Show()

class vector:
    """
    Objet de gestion d'informations vectorielles

    Une instance 'vector' contient une liste de 'wolfvertex'
    """

    myname:str
    parentzone:"zone"
    #parentzone:Zones
    nbvertices:int
    myvertices:list[wolfvertex]
    myprop:vectorproperties

    xmin:float
    ymin:float
    xmax:float
    ymax:float

    mytree:TreeListCtrl
    myitem:TreeItemId

    def __init__(self, lines:list=[], is2D=True, name='NoName', parentzone:"zone"=None, fromshapely=None) -> None:
        """
        lines : utile pour lecture de fichier
        is2D : on interprète les 'vertices' comme 2D même si chaque 'wolfvertex' contient toujours x, y et z
        name : nom du vecteur
        parentzone : instance de type 'zone' qui contient le 'vector'
        """
        self.myname=''
        self.is2D = is2D
        self.closed=False

        self.mytree = None

        self.parentzone:zone
        self.parentzone=parentzone
        self.xmin=-99999.
        self.ymin=-99999.
        self.xmax=-99999.
        self.ymax=-99999.

        self.mylimits = None

        self.textimage:Text_Image_Texture=None

        self.length2D=None
        self.length3D=None
        self._lengthparts2D=None
        self._lengthparts3D=None

        if type(lines)==list:
            if len(lines)>0:
                self.myname=lines[0]
                tmp_nbvertices=int(lines[1])
                self.myvertices=[]

                if is2D:
                    for i in range(tmp_nbvertices):
                        try:
                            curx,cury=lines[2+i].split()
                        except:
                            curx,cury=lines[2+i].split(',')
                        curvert = wolfvertex(float(curx),float(cury))
                        self.myvertices.append(curvert)
                else:
                    for i in range(tmp_nbvertices):
                        try:
                            curx,cury,curz=lines[2+i].split()
                        except:
                            curx,cury,curz=lines[2+i].split(',')
                        curvert = wolfvertex(float(curx),float(cury),float(curz))
                        self.myvertices.append(curvert)

                self.myprop=vectorproperties(lines[tmp_nbvertices+2:],parent=self)

        if name!='' and self.myname=='':
            self.myname=name
            self.myvertices=[]
            self.myprop=vectorproperties(parent=self)

        self.linestring = None

        # Utile surtout pour les sections en travers
        self.zdatum = 0.
        self.add_zdatum=False
        self.sdatum = 0.
        self.add_sdatum=False

        if fromshapely is not None:
            self.import_shapelyobj(fromshapely)


    def get_normal_segments(self) -> np.ndarray:
        """
        Return the normals of each segment

        The normals are oriented to the left
        """

        if self.nbvertices<2:
            return None

        xy = self.asnparray()
        delta = xy[1:]-xy[:-1]
        norm = np.sqrt(delta[:,0]**2+delta[:,1]**2)
        normals = np.zeros_like(delta)
        notnull = np.where(norm!=0)
        normals[notnull,0] = -delta[notnull,1]/norm[notnull]
        normals[notnull,1] = delta[notnull,0]/norm[notnull]

        return normals

    def get_center_segments(self) -> np.ndarray:
        """
        Return the center of each segment
        """

        if self.nbvertices<2:
            return None

        xy = self.asnparray()
        centers = (xy[1:]+xy[:-1])/2.
        return centers

    @property
    def nbvertices(self) -> int:
        return len(self.myvertices)

    @property
    def used(self) -> bool:
        return self.myprop.used

    @used.setter
    def used(self, value:bool):
        self.myprop.used = value

    def import_shapelyobj(self, obj):
        """ Importation d'un objet shapely """

        if isinstance(obj, LineString):
            xy = np.array(obj.xy).T
            self.is2D =  xy.shape[1]==2
            self.add_vertices_from_array(xy)
        elif isinstance(obj, Polygon):
            xy = np.array(obj.exterior.xy).T
            self.is2D =  xy.shape[1]==2
            self.add_vertices_from_array(xy)
            self.close_force()
        else:
            logging.warning(_('Object type {} not supported -- Update "import_shapelyobj"').format(type(obj)))

    def get_bounds(self, grid:float = None):
        """
        Return tuple with :
          - (lower-left corner), (upper-right corner)
        """
        if grid is None:
            return ((self.xmin, self.ymin), (self.xmax, self.ymax))
        else:
            xmin = float(np.int(self.xmin/grid)*grid)
            ymin = float(np.int(self.ymin/grid)*grid)

            xmax = float(np.ceil(self.xmax/grid)*grid)
            ymax = float(np.ceil(self.ymax/grid)*grid)
            return ((xmin, ymin), (xmax, ymax))

    def get_bounds_xx_yy(self, grid:float = None):
        """
        Return tuple with :
          - (xmin,xmax), (ymin, ymax)
        """
        if grid is None:
            return ((self.xmin, self.xmax), (self.ymin, self.ymax))
        else:
            xmin = float(np.int(self.xmin/grid)*grid)
            ymin = float(np.int(self.ymin/grid)*grid)

            xmax = float(np.ceil(self.xmax/grid)*grid)
            ymax = float(np.ceil(self.ymax/grid)*grid)
            return ((xmin, xmax), (ymin, ymax))

    def get_mean_vertex(self, asshapelyPoint = False):
        """ Return the mean vertex """

        if self.closed or (self.myvertices[0].x == self.myvertices[-1].x and self.myvertices[0].y == self.myvertices[-1].y):
            # if closed, we don't take the last vertex otherwise we have a double vertex
            x_mean = np.mean([curvert.x for curvert in self.myvertices[:-1]])
            y_mean = np.mean([curvert.y for curvert in self.myvertices[:-1]])
            z_mean = np.mean([curvert.z for curvert in self.myvertices[:-1]])
        else:
            x_mean = np.mean([curvert.x for curvert in self.myvertices])
            y_mean = np.mean([curvert.y for curvert in self.myvertices])
            z_mean = np.mean([curvert.z for curvert in self.myvertices])

        if asshapelyPoint:
            return Point(x_mean, y_mean, z_mean)
        else:
            return wolfvertex(x_mean, y_mean, z_mean)

    def highlighting(self, rgb=(255,0,0), linewidth=3):
        """
        Mise en évidence
        """
        self._oldcolor = self.myprop.color
        self._oldwidth = self.myprop.color

        self.myprop.color = getIfromRGB(rgb)
        self.myprop.width = linewidth

    def withdrawal(self):
        """
        Mise en retrait
        """
        try:
            self.myprop.color = self._oldcolor
            self.myprop.width = self._oldwidth
        except:
            self.myprop.color = 0
            self.myprop.width = 1

    def save(self,f):
        """
        Sauvegarde sur disque
        """
        f.write(self.myname+'\n')
        f.write(str(self.nbvertices)+'\n')

        force3D=False
        if self.parentzone is not None:
            force3D = self.parentzone.parent.force3D

        if self.is2D and not force3D:
            for curvert in self.myvertices:
                f.write(f'{curvert.x},{curvert.y}'+'\n')
        else:
            for curvert in self.myvertices:
                f.write(f'{curvert.x},{curvert.y},{curvert.z}'+'\n')

        self.myprop.save(f)

    def reverse(self):
        """Renverse l'ordre des vertices"""
        self.myvertices.reverse()

    def isinside(self,x,y):
        """Teste si la coordonnée (x,y) est dans l'objet -- en 2D"""
        if self.nbvertices==0:
            return False

        poly = self.asshapely_pol()
        inside2 = poly.contains(Point([x,y]))
        return inside2

    def asshapely_pol(self) -> Polygon:
        """
        Conversion des coordonnées en Polygon Shapely
        """
        coords=self.asnparray()
        return Polygon(coords)

    def asshapely_ls(self) -> LineString:
        """
        Conversion des coordonnées en Linestring Shapely
        """
        coords=self.asnparray3d()
        return LineString(coords)

    def asshapely_mp(self) -> MultiPoint:
        """
        Conversion des coordonnées en Multipoint Shapely
        """
        multi=self.asnparray3d()
        return MultiPoint(multi)

    def asnparray(self):
        """
        Conversion des coordonnées en Numpy array -- en 2D
        """
        return np.asarray(list([vert.x,vert.y] for vert in self.myvertices))

    def asnparray3d(self):
        """
        Conversion des coordonnées en Numpy array -- en 3D
        """
        xyz= np.asarray(list([vert.x,vert.y,vert.z] for vert in self.myvertices))

        if self.add_zdatum:
            xyz[:,2]+=self.zdatum
        return xyz

    def prepare_shapely(self):
        """
        Conversion Linestring Shapely et rétention de l'objet afin d'éviter de multiples appel
         par ex. dans une boucle
        """
        self.linestring = self.asshapely_ls()

    def projectontrace(self, trace):
        """
        Projection du vecteur sur une trace (type 'vector')

        Return :
          Nouveau vecteur contenant les infos de position sur la trace et d'altitude (s,z)
        """
        # trace:vector
        tracels:LineString
        tracels = trace.asshapely_ls() # conversion en linestring Shapely

        xyz = self.asnparray3d() # récupération des vertices en numpy array
        all_s = [tracels.project(Point(cur[0],cur[1])) for cur in xyz] # Projection des points sur la trace et récupération de la coordonnées curviligne

        # création d'un nouveau vecteur
        newvec = vector(name=_('Projection on ')+trace.myname)
        for s,(x,y,z) in zip(all_s,xyz):
            newvec.add_vertex(wolfvertex(s,z))

        return newvec

    def parallel_offset(self, distance=5., side='left'):
        """
        The distance parameter must be a positive float value.

        The side parameter may be ‘left’ or ‘right’. Left and right are determined by following the direction of the given geometric points of the LineString.
        """

        if self.nbvertices<2:
            return None

        myls = self.asshapely_ls()

        mypar = myls.parallel_offset(distance=abs(distance),side=side,join_style=JOIN_STYLE.round)

        if mypar.geom_type=='MultiLineString':
            return None


        if len(mypar.coords) >0:
            # if side=='right':
            #     #On souhaite garder une même orientation pour les vecteurs
            #     mypar = substring(mypar, 1., 0., normalized=True)

            newvec = vector(name='par'+str(distance), parentzone=self.parentzone)

            for x,y in mypar.coords:
                xy = Point(x,y)
                curs = mypar.project(xy,True)
                curz = myls.interpolate(curs,True).z

                newvert = wolfvertex(x,y,curz)
                newvec.add_vertex(newvert)

            return newvec
        else:
            return None

    def intersection(self, vec2 = None, eval_dist=False,norm=False, force_single=False):
        """
        Calcul de l'intersection avec un autre vecteur

        Return :
         - le point d'intersection
         - la distance (optional) le long de 'self'

        Utilisation de Shapely
        """
        ls1 = self.asshapely_ls() if self.linestring is None else self.linestring
        ls2 = vec2.asshapely_ls() if vec2.linestring is None else vec2.linestring

        myinter = ls1.intersection(ls2)

        if isinstance(myinter, MultiPoint):
            if force_single:
                myinter = myinter.geoms[0]
        elif isinstance(myinter, MultiLineString):
            if force_single:
                myinter = Point(myinter.geoms[0].xy[0][0],myinter.geoms[0].xy[1][0])

        if myinter.is_empty:
            if eval_dist:
                return None, None
            else:
                return None

        if eval_dist:
            mydists = ls1.project(myinter,normalized=norm)
            return myinter,mydists
        else:
            return myinter

    def reset(self):
        """Remise à zéro"""
        self.myvertices=[]
        self.linestring=None

    def add_vertex(self,addedvert: Union[list[wolfvertex], wolfvertex]):
        """
        Ajout d'un wolfvertex
        Le compteur est automatqiuement incrémenté
        """
        if type(addedvert) is list:
            for curvert in addedvert:
                self.add_vertex(curvert)
        else:
            assert(addedvert is not None)
            assert isinstance(addedvert, wolfvertex)
            self.myvertices.append(addedvert)

    def add_vertices_from_array(self, xyz:np.ndarray):
        """
        Ajout de vertices depuis une matrice numpy -- shape = (nb_vert,2 ou 3)
        """
        if xyz.dtype==np.int32:
            xyz = xyz.astype(np.float64)

        if xyz.shape[1]==3:
            for cur in xyz:
                self.add_vertex(wolfvertex(cur[0], cur[1], cur[2]))
        elif xyz.shape[1]==2:
            for cur in xyz:
                self.add_vertex(wolfvertex(cur[0], cur[1]))

    def count(self):
        """
        Retroune le nombre de vertices

        For compatibility with older version of the code --> use 'nbvertices' property instead
        Must be removed in the future
        """
        # Nothing to do because nbvertices is a property
        # self.nbvertices=len(self.myvertices)
        return

    def close_force(self):
        """
        Force la fermeture du 'vector'

        Commence par vérifier si le premier point possède les mêmes coords que le dernier
        Si ce n'est pas le cas, on ajoute un wolfvertes

        self.closed -> True
        """
        """ A polygon is closed either if
        - it has the `closed` attribute.
        - it has not the `closed` attribute, in which case there must be
          a repeated vertex in its vertices.
        """
        # FIXME With this code, it is possible to have apolygon marked
        # as closed but without an actual closing vertex...

        # FIXME Wouldn't it be better to have a vector that can be
        # requested to become a closed or not closed one, depending
        # on the needs of the caller ?

        # First condition checks that the same vertex is not at the
        # beginning and end of the vector (it it was, vector would be closed)
        # second and third condition tests that, if begin and end vertices
        # are different, they also have different coordinates (this
        # again checks that the vector is not closed; in the case where
        # two vertices are not the same one but have the same coordinates)

        is_open = self.myvertices[-1] is not self.myvertices[0] and \
            (self.myvertices[-1].x!=self.myvertices[0].x and \
             self.myvertices[-1].y!=self.myvertices[0].y)

        if not self.is2D :
            is_open = is_open and self.myvertices[-1].z!=self.myvertices[0].z

        if is_open:
            self.add_vertex(self.myvertices[0])
            self.closed=True

    def _nblines(self):
        """
        routine utile pour l'initialisation sur base de 'lines'
        """
        return self.nbvertices+5

    def verify_s_ascending(self):
        """
        Vérifie que les points d'un vecteur sont énumérés par distances 2D croissantes

        Utile notamment pour le traitement d'interpolation de sections en travers afin d'éviter une triangulation non valable suite à des débords
        """
        s,z=self.get_sz(cumul=False)

        correction=False
        where=[]

        for i in range(self.nbvertices-1):
            if s[i]>s[i+1]:
                #inversion si le points i est plus loin que le i+1
                correction=True
                where.append(i+1)

                x=self.myvertices[i].x
                y=self.myvertices[i].y

                self.myvertices[i].x=self.myvertices[i+1].x
                self.myvertices[i].y=self.myvertices[i+1].y

                self.myvertices[i+1].x=x
                self.myvertices[i+1].y=y

        return correction,where

    def find_nearest_vert(self,x,y):
        """
        Trouve le vertex le plus proche de la coordonnée (x,y) -- en 2D
        """
        xy=Point(x,y)
        mynp = self.asnparray()
        mp = MultiPoint(mynp)
        near = np.asarray(nearest_points(mp,xy)[0].coords)
        return self.myvertices[np.asarray(np.argwhere(mynp==near[0])[0,0])]

    def insert_nearest_vert(self,x,y):
        """
        Insertion d'un nouveau vertex au plus proche de la coordonnée (x,y) -- en 2D
        """
        xy=Point(x,y)
        mynp = self.asnparray()
        mp = MultiPoint(mynp)
        ls = LineString(mynp)

        nearmp = nearest_points(mp,xy) #point le plus proche sur base du nuage
        nearls = nearest_points(ls,xy) #point le plus proche sur base de la ligne

        smp = ls.project(nearmp[0]) #distance le long de la ligne du sommet le plus proche
        sls = ls.project(nearls[0]) #distance le long de la ligne du point le plus proche au sens géométrique (perpendiculaire au segment)

        indexmp= np.argwhere(mynp==np.asarray([nearmp[0].x, nearmp[0].y]))[0,0] #index du vertex

        if indexmp==0 and self.closed:
            #le vecteur est fermé
            #il faut donc chercher à savoir si le point est après le premier point ou avant le dernier (qui possèdent les mêmes coords)
            if sls<=ls.length and sls >=ls.project(Point([self.myvertices[-2].x,self.myvertices[-2].y])):
                smp=ls.length
                indexmp=self.nbvertices-1
            else:
                indexmp=1
        else:
            if sls >= smp:
                #le point projeté sur la droite est au-delà du vertex le plus proche
                #on ajoute donc le point après
                indexmp+=1

        myvert=wolfvertex(x,y)
        self.myvertices.insert(indexmp,myvert)

        return self.myvertices[indexmp]

    def find_minmax(self, only_firstlast:bool=False):
        """
        Recherche l'extension spatiale du vecteur

        :param only_firstlast: si True, on ne recherche que les coordonnées du premier et du dernier vertex
        """
        if len(self.myvertices)>0:

            if only_firstlast:
                self.xmin=min(self.myvertices[0].x, self.myvertices[-1].x)
                self.ymin=min(self.myvertices[0].y, self.myvertices[-1].y)
                self.xmax=max(self.myvertices[0].x, self.myvertices[-1].x)
                self.ymax=max(self.myvertices[0].y, self.myvertices[-1].y)
            else:
                self.xmin=min(vert.x for vert in self.myvertices)
                self.ymin=min(vert.y for vert in self.myvertices)
                self.xmax=max(vert.x for vert in self.myvertices)
                self.ymax=max(vert.y for vert in self.myvertices)

    def plot(self, sx=None, sy=None, xmin=None, ymin=None, xmax=None, ymax=None, size=None):
        """
        Plot OpenGL
        """
        if self.myprop.used:

            if self.myprop.filled:
                glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
            else:
                glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)

            rgb=getRGBfromI(self.myprop.color)

            if self.myprop.transparent:
                glEnable(GL_BLEND)
                glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA)
            else:
                glDisable(GL_BLEND)

            glLineWidth(float(self.myprop.width))
            #glPointSize(float(self.myprop.width))

            if self.myprop.filled:
                glBegin(GL_POLYGON)
            else:
                glBegin(GL_LINE_STRIP)

            if self.myprop.transparent:
                glColor4ub(int(rgb[0]),int(rgb[1]),int(rgb[2]),int(self.myprop.alpha))
            else:
                glColor3ub(int(rgb[0]),int(rgb[1]),int(rgb[2]))

            for curvertex in self.myvertices:
                glVertex2d(curvertex.x, curvertex.y)

            if self.myprop.closed and (self.myvertices[0].x != self.myvertices[-1].x or self.myvertices[0].y != self.myvertices[-1].y):
                curvertex = self.myvertices[0]
                glVertex2d(curvertex.x, curvertex.y)

            glEnd()

            glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
            glDisable(GL_BLEND)

            if self.myprop.legendvisible:
                self.textimage.paint()

    def add2tree(self, tree:TreeListCtrl, root):
        """
        Ajout de l'objte à un TreeListCtrl wx
        """
        self.mytree=tree
        self.myitem=tree.AppendItem(root, self.myname,data=self)
        if self.myprop.used:
            tree.CheckItem(self.myitem)

    def unuse(self):
        """
        L'objet n'est plus à utiliser
        """
        self.myprop.used=False
        if self.mytree is not None:
            self.mytree.UncheckItem(self.myitem)

    def use(self):
        """
        L'objet n'est plus à utiliser
        """
        self.myprop.used=True
        if self.mytree is not None:
            self.mytree.CheckItem(self.myitem)

    def fillgrid(self,gridto:CpGrid):
        """
        Remplissage d'un CpGrid
        """
        curv:wolfvertex

        gridto.SetColLabelValue(0,'X')
        gridto.SetColLabelValue(1,'Y')
        gridto.SetColLabelValue(2,'Z')
        gridto.SetColLabelValue(3,'value')
        gridto.SetColLabelValue(4,'s curvi')

        nb=gridto.GetNumberRows()
        if len(self.myvertices)-nb>0:
            gridto.AppendRows(len(self.myvertices)-nb)
        k=0
        for curv in self.myvertices:
           gridto.SetCellValue(k,0,str(curv.x))
           gridto.SetCellValue(k,1,str(curv.y))
           gridto.SetCellValue(k,2,str(curv.z))
           k+=1

    def updatefromgrid(self,gridfrom:CpGrid):
        """
        Mise à jour depuis un CpGrid
        """
        curv:wolfvertex

        nbl=gridfrom.GetNumberRows()
        k=0
        while k<nbl:
            x=gridfrom.GetCellValue(k,0)
            y=gridfrom.GetCellValue(k,1)
            z=gridfrom.GetCellValue(k,2)
            if z=='':
                z=0.
            if x!='':
                if k<self.nbvertices:
                    self.myvertices[k].x=float(x)
                    self.myvertices[k].y=float(y)
                    self.myvertices[k].z=float(z)
                else:
                    newvert=wolfvertex(float(x),float(y),float(z))
                    self.add_vertex(newvert)
                k+=1
            else:
                break

        while k<self.nbvertices:
            self.myvertices.pop(k)

        if self.linestring is not None:
            self.prepare_shapely()

    def get_s2d(self):
        """
        calcul et retour des positions curvilignes 2D
        """
        s2d=np.zeros[self.nbvertices]
        for k in range(1,self.nbvertices+1):
            s2d[k]=s2d[k-1]+self.myvertices[k-1].dist2D(self.myvertices[k])

        return s2d

    def get_s3d(self):
        """
        calcul et retour des positions curvilignes 3D
        """
        s3d=np.zeros[self.nbvertices]
        for k in range(1,self.nbvertices+1):
            s3d[k]=s3d[k-1]+self.myvertices[k-1].dist3D(self.myvertices[k])

        return s3d

    def get_sz(self,cumul=True):
        """
        Calcule et retourne la distance horizontale cumulée ou non de chaque point vis-à-vis du premier point

        Utile pour le tracé de sections en travers ou des vérifications de position
        """
        z = np.asarray([self.myvertices[i].z for i in range(self.nbvertices)])

        nb = len(z)
        s = np.zeros(nb)

        if cumul:
            x1 = self.myvertices[0].x
            y1 = self.myvertices[0].y
            for i in range(nb-1):
                x2 = self.myvertices[i+1].x
                y2 = self.myvertices[i+1].y

                length = np.sqrt((x2-x1)**2.+(y2-y1)**2.)
                s[i+1] = s[i]+length

                x1=x2
                y1=y2
        else:
            for i in range(nb):
                s[i] = self.myvertices[0].dist2D(self.myvertices[i])

        return s,z

    def update_lengths(self):
        """
        Mise à jour de la longueur
         - en 2D
         - en 3D

        Retient également les longueurs de chaque segment
        """
        self._lengthparts2D=np.zeros(self.nbvertices-1)
        self._lengthparts3D=np.zeros(self.nbvertices-1)

        for k in range(self.nbvertices-1):
            self._lengthparts2D[k] = self.myvertices[k].dist2D(self.myvertices[k+1])
            self._lengthparts3D[k] = self.myvertices[k].dist3D(self.myvertices[k+1])

        if self.closed and self.myvertices[0]!=self.myvertices[-1]:
            self._lengthparts2D[-1] = self.myvertices[-2].dist2D(self.myvertices[-1])
            self._lengthparts3D[-1] = self.myvertices[-2].dist3D(self.myvertices[-1])

        self.length2D = np.sum(self._lengthparts2D)
        self.length3D = np.sum(self._lengthparts3D)

    def get_segment(self, s, is3D, adim=True,frombegin=True):
        """
        Retrouve le segment associé aux paramètres passés
        """
        if is3D:
            length = self.length3D
            lengthparts = self._lengthparts3D
        else:
            length = self.length2D
            lengthparts = self._lengthparts2D

        if length is None:
            self.update_lengths()
            if is3D:
                length = self.length3D
                lengthparts = self._lengthparts3D
            else:
                length = self.length2D
                lengthparts = self._lengthparts2D

        cums = np.cumsum(lengthparts)

        if adim:
            cums = cums.copy()/length
            cums[-1]=1.
            lengthparts = lengthparts.copy()/length
            if s>1.:
                s=1.
            if s<0.:
                s=0.
        else:
            if s>length:
                s=length
            if s<0.:
                s=0.

        if frombegin:
            k=0
            while s>cums[k]:
                k+=1
        else:
            k=self.nbvertices-2
            if k>0:
                while s<cums[k] and k>0:
                    k-=1
                if (k==0 and s<cums[0]) or s==cums[self.nbvertices-2]:
                    pass
                else:
                    k+=1

        if k==len(cums):
            k-=1

        return k,cums[k],lengthparts

    def _refine2D(self, ds):
        """
        Raffine un vecteur selon un pas 'ds'

        Return :
         Liste Python avec des Point Shapely
        """

        myls = self.asshapely_ls()
        length = myls.length

        nb = int(np.ceil(length/ds))+1

        if length<1:
            length*=1000.
            alls = np.linspace(0,int(length),nb)
            alls/=1000.
        else:
            alls = np.linspace(0,int(length),nb,endpoint=True)

        pts = [myls.interpolate(curs) for curs in alls]
        # pts = [(curpt.x, curpt.y) for curpt in pts]

        return pts

    def split(self,ds, new=True):
        """
        Création d'un nouveau vecteur sur base du découpage d'un autre et d'un pas spatial à respecter
        Le nouveau vecteur contient tous les points de l'ancien et des nouveaux sur base d'un découpage 3D
        """
        newvec = vector(name=self.myname+'_split',parentzone=self.parentzone)

        self.update_lengths()

        locds = ds/self.length3D

        dist3d = np.concatenate([np.arange(0.,1.,locds),np.cumsum(self._lengthparts3D)/self.length3D])
        dist3d = np.unique(dist3d)

        for curs in dist3d:
            newvec.add_vertex(self.interpolate(curs,is3D=True,adim=True))

        if new:
            curzone:zone
            curzone=self.parentzone
            if curzone is not None:
                curzone.add_vector(newvec)
                try:
                    curzone.parent.fill_structure()
                except:
                    pass
        else:
            self.myvertices = newvec.myvertices
            self.update_lengths()

    def interpolate(self,s,is3D=True,adim=True,frombegin=True):
        """
        Interpolation linéaire à une abscisse curviligne 's' donnée

        Calcul par défaut :
          - en 3D
          - en adimensionnel
        """
        k,cums,lengthparts=self.get_segment(s,is3D,adim,frombegin)

        pond = (cums-s)/lengthparts[k]

        return wolfvertex(self.myvertices[k].x*pond+self.myvertices[k+1].x*(1.-pond),
                          self.myvertices[k].y*pond+self.myvertices[k+1].y*(1.-pond),
                          self.myvertices[k].z*pond+self.myvertices[k+1].z*(1.-pond))

    def substring(self,s1,s2,is3D=True,adim=True,eps=1.e-2):
        """
        Récupération d'une fraction de vector entre 's1' et 's2'
        Nom similaire à la même opération dans Shapely mais qui ne gère, elle, que le 2D
        """
        if s1==s2:
            s2+=eps

        k1,cums1,lengthparts1=self.get_segment(s1,is3D,adim,True)
        k2,cums2,lengthparts2=self.get_segment(s2,is3D,adim,False)

        pond1 = max((cums1-s1)/lengthparts1[k1],0.)
        pond2 = min((cums2-s2)/lengthparts2[k2],1.)

        v1= wolfvertex(self.myvertices[k1].x*pond1+self.myvertices[k1+1].x*(1.-pond1),
                       self.myvertices[k1].y*pond1+self.myvertices[k1+1].y*(1.-pond1),
                       self.myvertices[k1].z*pond1+self.myvertices[k1+1].z*(1.-pond1))

        v2= wolfvertex(self.myvertices[k2].x*pond2+self.myvertices[k2+1].x*(1.-pond2),
                       self.myvertices[k2].y*pond2+self.myvertices[k2+1].y*(1.-pond2),
                       self.myvertices[k2].z*pond2+self.myvertices[k2+1].z*(1.-pond2))

        newvec = vector(name='substr')

        newvec.add_vertex(v1)

        if s1<=s2:
            if is3D:
                for k in range(k1+1,k2+1):
                    if self.myvertices[k].dist3D(newvec.myvertices[-1])!=0.:
                        newvec.add_vertex(self.myvertices[k])
            else:
                for k in range(k1+1,k2+1):
                    if self.myvertices[k].dist2D(newvec.myvertices[-1])!=0.:
                        newvec.add_vertex(self.myvertices[k])
        else:
            if is3D:
                for k in range(k1+1,k2+1,-1):
                    if self.myvertices[k].dist3D(newvec.myvertices[-1])!=0.:
                        newvec.add_vertex(self.myvertices[k])
            else:
                for k in range(k1+1,k2+1,-1):
                    if self.myvertices[k].dist2D(newvec.myvertices[-1])!=0.:
                        newvec.add_vertex(self.myvertices[k])

        if [v2.x,v2.y,v2.z] != [newvec.myvertices[-1].x,newvec.myvertices[-1].y,newvec.myvertices[-1].z]:
            newvec.add_vertex(v2)

        # if newvec.nbvertices==0:
        #     a=1
        # if newvec.nbvertices==1:
        #     a=1
        # newvec.update_lengths()
        # if np.min(newvec._lengthparts2D)==0.:
        #     a=1
        return newvec

    def get_values_linked_polygon(self, linked_arrays:list, getxy=False) -> dict:
        """
        Retourne les valeurs contenue dans le polygone

        linked_arrays : liste Python d'objet matriciels WolfArray (ou surcharge)
        """
        vals={}

        for curarray in linked_arrays:
            if curarray.plotted:
                vals[curarray.idx] = curarray.get_values_insidepoly(self, getxy=getxy)
            else:
                vals[curarray.idx] = None

        return vals

    def get_all_values_linked_polygon(self, linked_arrays, getxy=False) -> dict:
        """
        Retourne toutes les valeurs contenue dans le polygone --> utile au moins pour les résultats WOLF2D

        linked_arrays : liste Python d'objet matriciels WolfArray (ou surcharge)
        """
        vals={}

        for curarray in linked_arrays:
            if curarray.plotted:
                vals[curarray.idx] = curarray.get_all_values_insidepoly(self, getxy=getxy)
            else:
                vals[curarray.idx] = None

        return vals

    def get_all_values_linked_polyline(self,linked_arrays, getxy=True) -> dict:
        """
        Retourne toutes les valeurs sous la polyligne --> utile au moins pour les résultats WOLF2D

        linked_arrays : liste Python d'objet matriciels WolfArray (ou surcharge)
        """
        vals={}

        for curarray in linked_arrays:
            if curarray.plotted:
                vals[curarray.idx], xy = curarray.get_all_values_underpoly(self, getxy=getxy)
            else:
                vals[curarray.idx] = None

        return vals

    def get_values_on_vertices(self,curarray):
        """
        Récupération des valeurs sous les vertices et stockage dans la coordonnée 'z'
        """
        if not curarray.plotted:
            return

        for curpt in self.myvertices:
            curpt.z = curarray.get_value(curpt.x,curpt.y)

    def get_values_linked(self, linked_arrays:dict, refine=True, filter_null = False):
        """
        Récupération des valeurs dans les matrices liées sous les vertices et stockage dans la coordonnée 'z'
        Possibilité de raffiner la discrétisation pour obtenir au moins une valeur par maille
        """

        exit=True
        for curlabel, curarray in linked_arrays.items():
            if curarray.plotted:
                # at least one plotted array
                exit=False

        if exit:
            return

        if refine:
            myzone=zone(name='linked_arrays - fine step')

            for curlabel, curarray in linked_arrays.items():
                if curarray.plotted:

                    myvec=vector(name=curlabel,parentzone=myzone)
                    myzone.add_vector(myvec)

                    ds = min(curarray.dx,curarray.dy)

                    pts = self._refine2D(ds)

                    allz = [curarray.get_value(curpt.x, curpt.y, nullvalue=-99999) for curpt in pts]

                    if filter_null:
                        for curpt,curz in zip(pts,allz):
                            if curz!=-99999:
                                myvec.add_vertex(wolfvertex(curpt.x,curpt.y,curz))
                    else:
                        for curpt,curz in zip(pts,allz):
                            myvec.add_vertex(wolfvertex(curpt.x,curpt.y,curz))

        else:
            myzone=zone(name='linked_arrays')
            for curlabel, curarray in linked_arrays.items():
                if curarray.plotted:

                    myvec=vector(name=curlabel,parentzone=myzone)
                    myzone.add_vector(myvec)

                    if filter_null:
                        for curpt in self.myvertices:
                            locval = curarray.get_value(curpt.x, curpt.y, nullvalue=-9999)
                            if locval !=-99999:
                                myvec.add_vertex(wolfvertex(curpt.x, curpt.y, locval))
                    else:
                        for curpt in self.myvertices:
                            locval = curarray.get_value(curpt.x, curpt.y, nullvalue=-9999)
                            myvec.add_vertex(wolfvertex(curpt.x, curpt.y, locval))

        return myzone

    def plot_linked(self, fig, ax, linked_arrays:dict):
        """
        Graphique Matplolib de valeurs dans les matrices liées
        """
        colors=['red','blue','green']

        exit=True
        for curlabel, curarray in linked_arrays.items():
            if curarray.plotted:
                exit=False

        if exit:
            return

        k=0

        myls = self.asshapely_ls()
        length = myls.length
        tol=length/10.
        ax.set_xlim(0-tol,length+tol)

        zmin=99999.
        zmax=-99999.

        for curlabel, curarray in linked_arrays.items():
            if curarray.plotted:

                ds = min(curarray.dx,curarray.dy)
                nb = int(np.ceil(length/ds*2))

                alls = np.linspace(0,int(length),nb)

                pts = [myls.interpolate(curs) for curs in alls]

                allz = [curarray.get_value(curpt.x,curpt.y) for curpt in pts]

                zmaxloc=np.max(allz)
                zminloc=np.min(allz)

                zmax=max(zmax,zmaxloc)
                zmin=min(zmin,zminloc)

                if np.max(allz)>-99999:
                    ax.plot(alls,allz,
                            color=colors[np.mod(k,3)],
                            lw=2.0,
                            label=curlabel)
                k+=1

        ax.set_ylim(zmin,zmax)
        ax.legend()
        ax.grid()
        fig.canvas.draw()

        return fig,ax

    def plot_mpl(self,show=False,forceaspect=True,fig:Figure=None,ax:Axes=None,labels:dict={}):
        """
        Graphique Matplolib du vecteur
        """

        x,y=self.get_sz()

        xmin=x[0]
        xmax=x[-1]
        ymin=np.min(y)
        ymax=np.max(y)

        if ax is None:
            redraw=False
            fig = plt.figure()
            ax=fig.add_subplot(111)
        else:
            redraw=True
            ax.cla()

        if 'title' in labels.keys():
            ax.set_title(labels['title'])
        if 'xlabel' in labels.keys():
            ax.set_xlabel(labels['xlabel'])
        if 'ylabel' in labels.keys():
            ax.set_ylabel(labels['ylabel'])

        if ymax>-99999.:

            dy=ymax-ymin
            ymin-=dy/4.
            ymax+=dy/4.

            ax.plot(x,y,color='black',
                    lw=2.0,
                    label=self.myname)

            ax.legend()

            tol=(xmax-xmin)/10.
            ax.set_xlim(xmin-tol,xmax+tol)
            ax.set_ylim(ymin,ymax)

            if forceaspect:
                aspect=1.0*(ymax-ymin)/(xmax-xmin)*(ax.get_xlim()[1] - ax.get_xlim()[0]) / (ax.get_ylim()[1] - ax.get_ylim()[0])
                ax.set_aspect(aspect)

        if show:
            fig.show()

        if redraw:
            fig.canvas.draw()

        return fig,ax

    def deepcopy_vector(self, name: str = None, parentzone : str = None):
        """
        Return a deep copy of the vector.
        """

        if name is None:
            name = self.myname + "_copy"
            if parentzone:
                copied_vector = vector(name=name,parentzone=parentzone)
            else:
                copied_vector = vector(name=name)

            copied_vector.myvertices = copy.deepcopy(self.myvertices)
            # copied_vector.nbvertices = copy.deepcopy(self.nbvertices)

            return copied_vector


class zone:
    """
    Objet de gestion d'informations vectorielles

    Une instance 'zone' contient une listde de 'vector' (segment, ligne, polyligne, polygone...)
    """

    myname:str
    nbvectors:int
    myvectors:list[vector]

    xmin:float
    ymin:float
    xmax:float
    ymax:float

    selected_vectors:list[tuple[vector,float]]
    mytree:TreeListCtrl
    myitem:TreeItemId

    def __init__(self,
                 lines:list[str]=[],
                 name:str='NoName',
                 parent:"Zones"=None,
                 is2D:bool=True,
                 fromshapely:Union[LineString,Polygon,MultiLineString, MultiPolygon]=None) -> None:

        self.myname = ''        # name of the zone
        self.idgllist = -99999  # id of the zone in the gllist
        self.active_vector=None # current active vector
        self.parent=parent      # parent object - type(Zones)

        self.xmin = 0.
        self.ymin = 0.
        self.xmax = 0.
        self.ymax = 0.

        if len(lines)>0:
            # Decoding from lines -- lines is a list of strings provided by the parent during reading
            # The order of the lines is important to ensure compatibility with the WOLF2D format
            self.myname=lines[0]
            tmp_nbvectors=int(lines[1])
            self.myvectors=[]
            curstart=2

            if tmp_nbvectors>1000:
                logging.info(_('Many vectors in zone -- {} -- Be patient !').format(tmp_nbvectors))

            for i in range(tmp_nbvectors):
                curvec=vector(lines[curstart:],parentzone=self,is2D=is2D)
                curstart+=curvec._nblines()
                self.myvectors.append(curvec)
                if tmp_nbvectors>1000:
                    if i%100==0:
                        logging.info(_('{} vectors read').format(i))

        if name!='' and self.myname=='':
            self.myname=name
            self.myvectors=[]

        self.selected_vectors=[]                # list of selected vectors
        self.multils:MultiLineString = None     # MultiLineString shapely
        self.used = True                        # indicate if the zone must used or not --> corresponding to checkbox in the tree

        self.mytree=None                        # TreeListCtrl wx

        if fromshapely is not None:
            # Object can be created from a shapely object
            self.import_shapelyobj(fromshapely)

    @property
    def nbvectors(self):
        return len(self.myvectors)

    def import_shapelyobj(self, obj):
        """ Importation d'un objet shapely """

        if isinstance(obj, LineString):
            curvec = vector(fromshapely= obj, parentzone=self, name = self.myname)
            self.add_vector(curvec)
        elif isinstance(obj, Polygon):
            curvec = vector(fromshapely= obj, parentzone=self, name = self.myname)
            self.add_vector(curvec)
        elif isinstance(obj, MultiLineString):
            for curls in list(obj.geoms):
                curvec = vector(fromshapely= curls, parentzone=self, name = self.myname)
                self.add_vector(curvec)
        elif isinstance(obj, MultiPolygon):
            for curpoly in list(obj.geoms):
                curvec = vector(fromshapely= curpoly, parentzone=self, name = self.myname)
                self.add_vector(curvec)
        else:
            logging.warning(_('Object type {} not supported -- Update "import_shapelyobj"').format(type(obj)))

    def get_vector(self,keyvector:Union[int, str])->vector:
        """
        Retrouve le vecteur sur base de son nom ou de sa position
        Si plusieurs vecteurs portent le même nom, seule le premier est retourné
        """
        if isinstance(keyvector,int):
            if keyvector < self.nbvectors:
                return self.myvectors[keyvector]
            return None
        if isinstance(keyvector,str):
            zone_names = [cur.myname for cur in self.myvectors]
            if keyvector in zone_names:
                return self.myvectors[zone_names.index(keyvector)]
            return None

    def __getitem__(self, ndx:Union[int,str]) -> vector:
        """ Permet de retrouver un vecteur sur base de son index """
        return self.get_vector(ndx)

    def export_shape(self, fn:str = ''):
        """ Export to shapefile using GDAL/OGR """

        from osgeo import gdal, osr, gdalconst,ogr

        # create the spatial reference system, Lambert72
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(31370)

        # create the data source
        driver: ogr.Driver
        driver = ogr.GetDriverByName("ESRI Shapefile")

        # create the data source
        if not fn.endswith('.shp'):
            fn += '.shp'
        ds = driver.CreateDataSource(fn)

        # create one layer
        layer = ds.CreateLayer("poly", srs, ogr.wkbPolygon) # FIXME What about other geometries (line, points)?

        # Add ID fields
        idFields=[]
        idFields.append(ogr.FieldDefn('curvi', ogr.OFTReal))
        layer.CreateField(idFields[-1])

        # Create the feature and set values
        featureDefn = layer.GetLayerDefn()
        feature = ogr.Feature(featureDefn)

        for curvec in self.myvectors:
            ring = ogr.Geometry(ogr.wkbLinearRing)
            for curvert in curvec.myvertices:
                # Creating a line geometry
                ring.AddPoint(curvert.x,curvert.y)

            # Create polygon
            poly = ogr.Geometry(ogr.wkbPolygon)
            poly.AddGeometry(ring)

            feature.SetGeometry(poly)
            feature.SetField('curvi', float(curvec.myvertices[0].z))

            layer.CreateFeature(feature)

        feature = None

        # Save and close DataSource
        ds = None

    def save(self, f:io.TextIOWrapper):
        """
        Ecriture sur disque
        """
        f.write(self.myname+'\n')
        f.write(str(self.nbvectors)+'\n')
        for curvect in self.myvectors:
            curvect.save(f)

    def save_extra(self, f:io.TextIOWrapper):
        """
        Ecriture des options EXTRA
        """
        f.write(self.myname+'\n')
        curvect:vector
        for curvect in self.myvectors:
            curvect.myprop.save_extra(f)

    def add_vector(self, addedvect:vector, index=-99999, forceparent=False):
        """
        Ajout d'une instance 'vector'
        Le compteur est incrémenté
        """
        if index==-99999 or index >self.nbvectors:
            self.myvectors.append(addedvect)
        else:
            self.myvectors.insert(index,addedvect)

        # FIXME set vector's parent to self ?
        # NOT necessary because, in some situation, we can add a vector
        #  to a temporary zone without forcing its parent to be this zone
        if forceparent:
            addedvect.parentzone = self

        if self.nbvectors==1:
            self.active_vector = addedvect
            # FIXME else ?
            # NOTHING because the active vector is normally choosen by the UI or during special operations
            # Here, we select the first added vector

    def count(self):
        """
        Compte le nombre de vecteurs

        For compatibility with older versions --> Must be removed in future version
        """
        # self.nbvectors=len(self.myvectors)
        # Nothing to do because the number of vectors is a property
        return

    def _nblines(self):
        """
        Utile pour init par 'lines'
        """
        nb=2
        for curvec in self.myvectors:
            nb+=curvec._nblines()

        return nb

    def find_minmax(self, update=False, only_firstlast:bool=False):
        """
        Recherche de l'emprise spatiale de toute la zone

        :param update: True = mise à jour des valeurs ; False = utilisation des valeurs déjà calculées
        :param only_firstlast: True = recherche uniquement sur les premiers et derniers points de chaque vecteur
        """
        if update:
            for vect in self.myvectors:
                vect.find_minmax(only_firstlast=only_firstlast)

        if self.nbvectors==0:
            self.xmin=-99999.
            self.ymin=-99999.
            self.xmax=-99999.
            self.ymax=-99999.
        else:
            minsx=np.asarray([vect.xmin for vect in self.myvectors])
            minsy=np.asarray([vect.ymin for vect in self.myvectors])
            maxsx=np.asarray([vect.xmax for vect in self.myvectors])
            maxsy=np.asarray([vect.ymax for vect in self.myvectors])

            # if len(minsx)>1: # FIXME what if more than one vector is empty.
            if max(max(minsx),max(minsy), max(maxsx), max(maxsy)) != -99999.:
                self.xmin=np.min(minsx[np.where(minsx!=-99999.)])
                self.xmax=np.max(maxsx[np.where(maxsx!=-99999.)])
                self.ymin=np.min(minsy[np.where(minsy!=-99999.)])
                self.ymax=np.max(maxsy[np.where(maxsy!=-99999.)])
            else:
                self.xmin=minsx[0]
                self.xmax=maxsx[0]
                self.ymin=minsy[0]
                self.ymax=maxsy[0]

    def prep_listogl(self):
        """
        Préparation des listes OpenGL pour augmenter la vitesse d'affichage
        """
        self.plot(prep = True)

    def plot(self, prep:bool=False):
        """
        Graphique OpenGL
        """
        if prep:
            if self.idgllist==-99999:
                self.idgllist = glGenLists(1)

            glNewList(self.idgllist,GL_COMPILE)
            for curvect in self.myvectors:
                curvect.plot()
            glEndList()
        else:
            if self.idgllist!=-99999:
                glCallList(self.idgllist)
            else:
                for curvect in self.myvectors:
                    curvect.plot()

    def select_vectors_from_point(self,x:float,y:float,inside=True):
        """
        Sélection du vecteur de la zone sur base d'une coordonnée (x,y) -- en 2D

        inside : True = le point est contenu ; False = le point le plus proche
        """
        curvect:vector
        self.selected_vectors.clear()

        if inside:
            for curvect in self.myvectors:
                if curvect.isinside(x,y):
                    self.selected_vectors.append((curvect,99999.))
        else:
            distmin=99999.
            for curvect in self.myvectors:
                nvert:wolfvertex
                nvert= curvect.find_nearest_vert(x,y)
                dist=np.sqrt((nvert.x-x)**2.+(nvert.y-y)**2.)
                if dist<distmin:
                    distmin=dist
                    vectmin=curvect

            self.selected_vectors.append((vectmin,distmin))

    def add2tree(self,tree:TreeListCtrl,root):
        """
        Ajout à un objet TreeListCtrl
        """
        self.mytree=tree
        self.myitem=tree.AppendItem(root, self.myname,data=self)

        for curvect in self.myvectors:
            curvect.add2tree(tree,self.myitem)

        if self.used:
            tree.CheckItem(self.myitem)
        else:
            tree.UncheckItem(self.myitem)

    def unuse(self):
        """
        Ne plus utiliser
        """
        for curvect in self.myvectors:
            curvect.unuse()
        self.used=False

        if self.mytree is not None:
            self.mytree.UncheckItem(self.myitem)

    def use(self):
        """
        A utiliser
        """
        for curvect in self.myvectors:
            curvect.use()
        self.used=True

        if self.mytree is not None:
            self.mytree.CheckItem(self.myitem)

    def asshapely_ls(self):
        """
        Retroune la zone comme MultiLineString Shaely
        """
        mylines=[]
        curvect:vector
        for curvect in self.myvectors:
            mylines.append(curvect.asshapely_ls())
        return MultiLineString(mylines)

    def prepare_shapely(self):
        """
        Converti l'objet en MultiLineString Shapely et stocke dans self.multils
        """
        self.multils = self.asshapely_ls()

    def get_selected_vectors(self,all=False):
        """
        Retourne la liste du/des vecteur(s) sélectionné(s)
        """
        if all:
            mylist=[]
            if len(self.selected_vectors)>0:
                mylist.append(self.selected_vectors)
            return mylist
        else:
            if len(self.selected_vectors)>0:
                return self.selected_vectors[0]

        return None

    def add_parallel(self,distance):
        """
        Ajoute une parallèle au vecteur actif
        """

        if distance>0.:
            mypl = self.active_vector.parallel_offset(distance,'right')
        elif distance<0.:
            mypl = self.active_vector.parallel_offset(distance,'left')
        else:
            mypl = vector(name=self.active_vector.myname+"_duplicate")
            mypl.myvertices = [wolfvertex(cur.x,cur.y,cur.z) for cur in self.active_vector.myvertices]
            # mypl.nbvertices = self.active_vector.nbvertices # No longer needed

        if mypl is None:
            return

        mypl.parentzone = self
        self.add_vector(mypl)

    def parallel_active(self,distance):
        """
        Ajoute une parallèle 'left' et 'right' au vecteur actif
        """

        if self.nbvectors>1:
            self.myvectors = [curv for curv in self.myvectors if curv ==self.active_vector]

        mypl = self.active_vector.parallel_offset(distance,'left')
        mypr = self.active_vector.parallel_offset(distance,'right')

        if mypl is None or mypr is None:
            return

        self.add_vector(mypl,0)
        self.add_vector(mypr,2)

    def createmultibin(self, nb=None, nb2=0) -> Triangulation:
        """
        Création d'une triangulation sur base des vecteurs
        Tient compte de l'ordre

        :param nb : nombre de points de découpe des vecteurs
        :param nb2 : nombre de points en perpendiculaire

        return :
         - instance de 'Triangulation'
        """

        wx_exists = wx.App.Get() is not None

        # transformation des vecteurs en polyline shapely
        nbvectors = self.nbvectors
        myls = []
        for curv in self.myvectors:
            myls.append(curv.asshapely_ls())

        if nb is None and wx_exists:
            dlg=wx.NumberEntryDialog(None,
                                     _('How many points along polylines ?')+'\n'+
                                     _('Length size is {} meters').format(myls[0].length),
                                     'nb',
                                     'dl size',
                                     100,
                                     1,
                                     10000)
            ret=dlg.ShowModal()
            if ret==wx.ID_CANCEL:
                dlg.Destroy()
                return

            nb=int(dlg.GetValue())
            dlg.Destroy()
        else:
            logging.warning( _('Bad parameter nb'))

        # redécoupage des polylines
        s = np.linspace(0.,1.,num=nb,endpoint=True)

        newls = []
        for curls in myls:
            newls.append(LineString([curls.interpolate(curs,True) for curs in s]))

        if nb2==0 and wx_exists:
            dlg=wx.NumberEntryDialog(None,
                                     _('How many points between two polylines ?'),
                                     'nb2',
                                     'perpendicular',
                                     0,
                                     1,
                                     10000)
            ret=dlg.ShowModal()
            if ret==wx.ID_CANCEL:
                dlg.Destroy()
                return

            nb2=int(dlg.GetValue())
            dlg.Destroy()

        if nb2>0:
            finalls = []
            ds = 1./float(nb2+1)
            sperp = np.arange(ds,1.,ds)

            for j in range(len(newls)-1):
                myls1:LineString
                myls2:LineString
                myls1 = newls[j]
                myls2 = newls[j+1]
                xyz1 = np.asarray(myls1.coords[:])
                xyz2 = np.asarray(myls2.coords[:])

                finalls.append(myls1)

                for curds in sperp:
                    finalls.append(LineString(xyz1*(1.-curds)+xyz2*curds))

            finalls.append(myls2)
            newls = finalls

        nbvectors = len(newls)
        points=np.zeros((nb*nbvectors,3),dtype=np.float64)

        xyz=[]
        for curls in newls:
            xyz.append(np.asarray(curls.coords[:]))

        decal=0
        for i in range(len(xyz[0])):
            for k in range(nbvectors):
                points[k+decal,:] = xyz[k][i]
            decal+=nbvectors

        decal=0
        triangles=[]

        nbpts=nbvectors
        triangles.append([[i+decal,i+decal+1,i+decal+nbpts] for i in range(nbpts-1)])
        triangles.append([[i+decal+nbpts,i+decal+1,i+decal+nbpts+1] for i in range(nbpts-1)])

        for k in range(1,nb-1):
            decal=k*nbpts
            triangles.append([ [i+decal,i+decal+1,i+decal+nbpts] for i in range(nbpts-1)])
            triangles.append([ [i+decal+nbpts,i+decal+1,i+decal+nbpts+1] for i in range(nbpts-1)])
        triangles=np.asarray(triangles,dtype=np.uint32).reshape([(2*nbpts-2)*(nb-1),3])

        mytri=Triangulation(pts=points,tri=triangles)
        mytri.find_minmax(True)

        return mytri

    def createmultibin_proj(self, nb=None, nb2=0) -> Triangulation:
        """
        Création d'une triangulation sur base des vecteurs par projection au plus proche du veteur central
        Tient compte de l'ordre

        :param nb : nombre de points de découpe des vecteurs
        :param nb2 : nombre de points en perpendiculaire

        return :
         - instance de 'Triangulation'
        """

        wx_exists = wx.App.Get() is not None

        # transformation des vecteurs en polyline shapely
        nbvectors = self.nbvectors
        myls = []
        for curv in self.myvectors:
            myls.append(curv.asshapely_ls())

        if nb is None and wx_exists:
            dlg=wx.NumberEntryDialog(None,_('How many points along polylines ?')+'\n'+
                                        _('Length size is {} meters').format(myls[0].length),'nb','dl size',100,1,10000)
            ret=dlg.ShowModal()
            if ret==wx.ID_CANCEL:
                dlg.Destroy()
                return

            nb=int(dlg.GetValue())
            dlg.Destroy()
        else:
            logging.warning( _('Bad parameter nb'))

        # redécoupage des polylines
        s = np.linspace(0.,1.,num=nb,endpoint=True)

        newls = []
        supportls = myls[int(len(myls)/2)]
        supportls = LineString([supportls.interpolate(curs,True) for curs in s])
        for curls in myls:
            curls:LineString
            news = [curls.project(Point(curpt[0], curpt[1])) for curpt in supportls.coords]
            news.sort()
            newls.append(LineString([curls.interpolate(curs) for curs in news]))

        if nb2==0 and wx_exists:
            dlg=wx.NumberEntryDialog(None,_('How many points between two polylines ?'), 'nb2','perpendicular',0,0,10000)
            ret=dlg.ShowModal()
            if ret==wx.ID_CANCEL:
                dlg.Destroy()
                return

            nb2=int(dlg.GetValue())
            dlg.Destroy()

        if nb2>0:
            finalls = []
            ds = 1./float(nb2+1)
            sperp = np.arange(ds,1.,ds)

            for j in range(len(newls)-1):
                myls1:LineString
                myls2:LineString
                myls1 = newls[j]
                myls2 = newls[j+1]
                xyz1 = np.asarray(myls1.coords[:])
                xyz2 = np.asarray(myls2.coords[:])

                finalls.append(myls1)

                for curds in sperp:
                    finalls.append(LineString(xyz1*(1.-curds)+xyz2*curds))

            finalls.append(myls2)
            newls = finalls

        nbvectors = len(newls)
        points=np.zeros((nb*nbvectors,3),dtype=np.float64)

        xyz=[]
        for curls in newls:
            xyz.append(np.asarray(curls.coords[:]))

        decal=0
        for i in range(len(xyz[0])):
            for k in range(nbvectors):
                points[k+decal,:] = xyz[k][i]
            decal+=nbvectors

        decal=0
        triangles=[]

        nbpts=nbvectors
        triangles.append([[i+decal,i+decal+1,i+decal+nbpts] for i in range(nbpts-1)])
        triangles.append([[i+decal+nbpts,i+decal+1,i+decal+nbpts+1] for i in range(nbpts-1)])

        for k in range(1,nb-1):
            decal=k*nbpts
            triangles.append([ [i+decal,i+decal+1,i+decal+nbpts] for i in range(nbpts-1)])
            triangles.append([ [i+decal+nbpts,i+decal+1,i+decal+nbpts+1] for i in range(nbpts-1)])
        triangles=np.asarray(triangles,dtype=np.uint32).reshape([(2*nbpts-2)*(nb-1),3])

        mytri=Triangulation(pts=points,tri=triangles)
        mytri.find_minmax(True)

        return mytri

    def create_polygon_from_parallel(self, ds:float, howmanypoly=1) ->None:
        """
        Création de polygones depuis des vecteurs parallèles

        La zone à traiter ne peut contenir que 3 vecteurs

        Une zone de résultat est ajouté à l'objet

        ds : desired size/length of the polygon, adjusted on the basis of a number of polygons rounded up to the nearest integer
        howmanypoly : Number of transversal polygons (1 = one large polygon, 2 = 2 polygons - one left and one right)
        """

        assert self.nbvectors==3, _('The zone must contain 3 and only 3 vectors')

        vecleft:vector
        vecright:vector
        veccenter:vector
        vecleft = self.myvectors[0]
        veccenter = self.myvectors[1]
        vecright = self.myvectors[2]

        #Shapely LineString
        lsl = vecleft.asshapely_ls()
        lsr = vecright.asshapely_ls()
        lsc = veccenter.asshapely_ls()

        #Number of points
        nb = int(np.ceil(lsc.length / ds))
        #Adimensional distances along center vector
        sloc = np.linspace(0.,1.,nb,endpoint=True)
        #Points along center vector
        ptsc = [lsc.interpolate(curs,True) for curs in sloc]
        #Real distances along left, right and center vector
        sl = [lsl.project(curs) for curs in ptsc]
        sr = [lsr.project(curs) for curs in ptsc]
        sc = [lsc.project(curs) for curs in ptsc]

        if howmanypoly==1:
            #un seul polygone sur base des // gauche et droite
            zonepoly = zone(name='polygons_'+self.myname,parent=self.parent)

            self.parent.add_zone(zonepoly)

            for i in range(len(sl)-1):

                #mean distance along center will be stored as Z value of each vertex
                smean =(sc[i]+sc[i+1])/2.
                curvec=vector(name='poly'+str(i+1),parentzone=zonepoly)
                #Substring for Left and Right
                sublsl = vecleft.substring(sl[i], sl[i+1], False, False)
                sublsr = vecright.substring(sr[i], sr[i+1], False, False)
                # sublsl=substring(lsl,sl[i],sl[i+1])
                # sublsr=substring(lsr,sr[i],sr[i+1])

                #Test if the substring result is Point or LineString
                if isinstance(sublsl, vector):
                    vr = sublsr.myvertices.copy()
                    vr.reverse()
                    curvec.myvertices = sublsl.myvertices.copy() + vr
                    # curvec.nbvertices = len(curvec.myvertices) FIXME Not needed anymore
                    for curv in curvec.myvertices:
                        curv.z = smean
                else:
                    if sublsl.geom_type=='Point':
                        curvec.add_vertex(wolfvertex(sublsl.x,sublsl.y,smean))
                    elif sublsl.geom_type=='LineString':
                        xy=np.asarray(sublsl.coords)
                        for (x,y) in xy:
                            curvec.add_vertex(wolfvertex(x,y,smean))

                    if sublsr.geom_type=='Point':
                        curvec.add_vertex(wolfvertex(sublsr.x,sublsr.y,smean))
                    elif sublsr.geom_type=='LineString':
                        xy=np.asarray(sublsr.coords)
                        xy=np.flipud(xy)
                        for (x,y) in xy:
                            curvec.add_vertex(wolfvertex(x,y,smean))

                #force to close the polygon
                curvec.close_force()
                #add vector to zone
                zonepoly.add_vector(curvec)

            #force to update minmax in the zone --> mandatory to plot
            zonepoly.find_minmax(True)
        else:
            #deux polygones sur base des // gauche et droite
            zonepolyleft = zone(name='polygons_left_'+self.myname,parent=self.parent)
            zonepolyright = zone(name='polygons_right_'+self.myname,parent=self.parent)
            self.parent.add_zone(zonepolyleft)
            self.parent.add_zone(zonepolyright)

            for i in range(len(sl)-1):

                smean =(sc[i]+sc[i+1])/2.
                curvecleft=vector(name='poly'+str(i+1),parentzone=zonepolyleft)
                curvecright=vector(name='poly'+str(i+1),parentzone=zonepolyright)

                # sublsl=substring(lsl,sl[i],sl[i+1])
                # sublsr=substring(lsr,sr[i],sr[i+1])
                # sublsc=substring(lsc,sc[i],sc[i+1])
                sublsl = vecleft.substring(sl[i], sl[i+1], False, False)
                sublsr = vecright.substring(sr[i], sr[i+1], False, False)
                sublsc = veccenter.substring(sc[i], sc[i+1], False, False)

                if isinstance(sublsl, vector):
                    vr = sublsr.myvertices.copy()
                    vr.reverse()
                    vcr = sublsc.myvertices.copy()
                    vcr.reverse()
                    curvecleft.myvertices = sublsl.myvertices.copy() + vcr
                    curvecright.myvertices = sublsc.myvertices.copy() + vr
                    for curv in curvecleft.myvertices:
                        curv.z = smean
                    for curv in curvecright.myvertices:
                        curv.z = smean
                    curvecleft.nbvertices = len(curvecleft.myvertices)
                    curvecright.nbvertices = len(curvecright.myvertices)
                else:
                    #left poly
                    if sublsl.geom_type=='Point':
                        curvecleft.add_vertex(wolfvertex(sublsl.x,sublsl.y,smean))
                    elif sublsl.geom_type=='LineString':
                        xy=np.asarray(sublsl.coords)
                        for (x,y) in xy:
                            curvecleft.add_vertex(wolfvertex(x,y,smean))

                    if sublsc.geom_type=='Point':
                        curvecleft.add_vertex(wolfvertex(sublsc.x,sublsc.y,smean))
                    elif sublsc.geom_type=='LineString':
                        xy=np.asarray(sublsc.coords)
                        xy=np.flipud(xy)
                        for (x,y) in xy:
                            curvecleft.add_vertex(wolfvertex(x,y,smean))

                    #right poly
                    if sublsc.geom_type=='Point':
                        curvecright.add_vertex(wolfvertex(sublsc.x,sublsc.y,smean))
                    elif sublsc.geom_type=='LineString':
                        xy=np.asarray(sublsc.coords)
                        for (x,y) in xy:
                            curvecright.add_vertex(wolfvertex(x,y,smean))

                    if sublsr.geom_type=='Point':
                        curvecright.add_vertex(wolfvertex(sublsr.x,sublsr.y,smean))
                    elif sublsr.geom_type=='LineString':
                        xy=np.asarray(sublsr.coords)
                        xy=np.flipud(xy)
                        for (x,y) in xy:
                            curvecright.add_vertex(wolfvertex(x,y,smean))

                curvecleft.close_force()
                curvecright.close_force()

                zonepolyleft.add_vector(curvecleft)
                zonepolyright.add_vector(curvecright)


            zonepolyleft.find_minmax(True)
            zonepolyright.find_minmax(True)

        self.parent.fill_structure()

    def create_sliding_polygon_from_parallel(self,
                                             ds:float,
                                             ds_sliding:float,
                                             dpar:float,
                                             dspar:float=None,
                                             intersect=None,
                                             howmanypoly=1,
                                             eps_inter:float=0.25):
        """
        Création de polygones depuis des vecteurs parallèles

        La zone à traiter ne peut contenir qu'un seul vecteur

        Une zone de résultat est ajouté à l'objet

        ds :            size/length of the polygon, adjusted on the basis of a number of polygons rounded up to the nearest integer
        ds_sliding :    sliding length
        dpar :          position of the parallels
        dspar :         parallel intervals (internal computation)
        intersect :     zone class containing constraints
        howmanypoly :   number of transversal polygons (1 = one large polygon, 2 = 2 polygons - one left and one right)
        eps_inter :     space width impose to the "intersect"
        """

        assert self.nbvectors==1, _('The zone must contain 1 and only 1 vector')

        veccenter:vector

        # All parallels on the left
        vecleft:dict[str,vector]={}
        # All parallels on the right
        vecright:dict[str,vector]={}
        veccenter = self.myvectors[0]
        veccenter.update_lengths()

        # Returned zone
        myparallels = zone()

        if dspar is None :
            dspar : dpar

        # All parallel distances
        all_par = np.arange(0, dpar, dspar)[1:]
        all_par = np.concatenate((all_par,[dpar]))

        for curpar in tqdm(all_par):
            # add current parallel to the dicts
            vecleft[curpar] = veccenter.parallel_offset(curpar, 'left')
            vecright[curpar]= veccenter.parallel_offset(curpar, 'right')

            myparallels.add_vector(vecleft[curpar], forceparent=True)
            myparallels.add_vector(vecright[curpar], forceparent=True)

            if isinstance(intersect, zone):
                # gestion de vecteurs d'intersection
                for curint in intersect.myvectors:
                    # bouclage sur les vecteurs
                    curint2 = curint.parallel_offset(eps_inter, side='right')

                    # recherche si une intersection existe
                    pt, dist = vecleft[curpar].intersection(curint, eval_dist=True, force_single=True)
                    if pt is not None:
                        #Une intersection existe --> on ajoute la portion de vecteur

                        # Projection du point d'intersection sur le vecteur à suivre
                        curls = curint.asshapely_ls()
                        dist2 = curls.project(pt)
                        # recherche de la portion de vecteur
                        # subs = extrêmité -> intersection
                        # subs_inv = intersection -> extrêmité
                        subs  = curint.substring(0. , dist2, is3D=False, adim=False)
                        subs.reverse()
                        subs2 = curint2.substring(0., dist2, is3D=False, adim=False)

                        vec1 = vecleft[curpar].substring(0., dist, is3D=False, adim=False)
                        vec2 = vecleft[curpar].substring(dist, vecleft[curpar].length2D, is3D=False, adim=False)

                        # combinaison du nouveau vecteur vecleft constitué de :
                        #  - la partie avant l'intersection
                        #  - l'aller-retour
                        #  - la partie après l'intersection
                        vecleft[curpar].myvertices = vec1.myvertices.copy() + subs.myvertices.copy() + subs2.myvertices.copy() + vec2.myvertices.copy()

                        # mise à jour des caractéristiques
                        vecleft[curpar].find_minmax()
                        vecleft[curpar].nbvertices = len(vecleft[curpar].myvertices)
                        vecleft[curpar].update_lengths()

                    pt, dist = vecright[curpar].intersection(curint, eval_dist=True, force_single=True)
                    if pt is not None:
                        curls = curint.asshapely_ls()
                        dist2 = curls.project(pt)
                        #Une intersection existe --> on ajoute la portion de vecteur
                        subs = curint.substring(0., dist2, is3D=False, adim=False)
                        subs2 = curint2.substring(0., dist2, is3D=False, adim=False)
                        subs2.reverse()

                        vec1 = vecright[curpar].substring(0., dist, is3D=False, adim=False)
                        vec2 = vecright[curpar].substring(dist, vecright[curpar].length2D, is3D=False, adim=False)

                        vecright[curpar].myvertices = vec1.myvertices.copy() + subs2.myvertices.copy() + subs.myvertices.copy() + vec2.myvertices.copy()

                        vecright[curpar].nbvertices = len(vecright[curpar].myvertices)
                        vecright[curpar].update_lengths()
                        vecright[curpar].find_minmax()

        #Shapely LineString
        lsl:dict[str,LineString] = {key:vec.asshapely_ls() for key,vec in vecleft.items()}
        lsr:dict[str,LineString] = {key:vec.asshapely_ls() for key,vec in vecright.items()}
        lsc = veccenter.asshapely_ls()

        #Number of points
        nb = int(np.ceil(lsc.length / float(ds_sliding)))

        #Dimensional distances along center vector
        sloc = np.asarray([float(ds_sliding) * cur for cur in range(nb)])
        sloc2 = sloc + float(ds)
        sloc2[sloc2>veccenter.length2D]=veccenter.length2D

        #Points along center vector
        ptsc  = [veccenter.interpolate(curs, is3D=False, adim=False) for curs in sloc]
        ptsc2 = [veccenter.interpolate(curs, is3D=False, adim=False) for curs in sloc2]

        sc = [lsc.project(Point(curs.x, curs.y)) for curs in ptsc]
        sc2 = [lsc.project(Point(curs.x, curs.y)) for curs in ptsc2]

        #Real distances along left, right and center vector
        sl={}
        sr={}
        sl2={}
        sr2={}
        ptl={}
        ptl2={}
        ptr={}
        ptr2={}

        # on calcule les points de proche en proche (// par //)
        # utile pour la prise en compte des intersections avec les polylignes de contrainte
        curpts = ptsc
        for key,ls in lsl.items():
            sl[key]  = [ls.project(Point(curs.x, curs.y)) for curs in curpts]
            ptl[key] = [ls.interpolate(curs) for curs in sl[key]]
            curpts = ptl[key]

        curpts = ptsc2
        for key,ls in lsl.items():
            sl2[key]  = [ls.project(Point(curs.x, curs.y)) for curs in curpts]
            ptl2[key] = [ls.interpolate(curs) for curs in sl2[key]]
            curpts = ptl2[key]

        curpts = ptsc
        for key,ls in lsr.items():
            sr[key]  = [ls.project(Point(curs.x, curs.y)) for curs in curpts]
            ptr[key] = [ls.interpolate(curs) for curs in sr[key]]
            curpts = ptr[key]

        curpts = ptsc2
        for key,ls in lsr.items():
            sr2[key]  = [ls.project(Point(curs.x, curs.y)) for curs in curpts]
            ptr2[key] = [ls.interpolate(curs) for curs in sr2[key]]
            curpts = ptr2[key]

        if howmanypoly==1:
            #un seul polygone sur base des // gauche et droite
            zonepoly = zone(name='polygons_'+self.myname,parent=self.parent)

            self.parent.add_zone(zonepoly)

            for i in range(nb):
                ptc1 = sc[i]
                ptc2 = sc2[i]
                pt1 = [cur[i] for cur in sl.values()]
                pt2 = [cur[i] for cur in sl2.values()]
                pt3 = [cur[i] for cur in sr.values()]
                pt4 = [cur[i] for cur in sr2.values()]

                #mean distance along center will be stored as Z value of each vertex
                smean =(ptc1+ptc2)/2.
                curvec=vector(name='poly'+str(i), parentzone=zonepoly)

                #Substring for Left and Right
                sublsl=vecleft[dpar].substring(pt1[-1], pt2[-1], is3D=False, adim=False)
                sublsr=vecright[dpar].substring(pt3[-1], pt4[-1], is3D=False, adim=False)
                sublsr.reverse()
                sublsc=veccenter.substring(ptc1,ptc2,is3D=False, adim=False)

                upl   = [wolfvertex(pt[i].x, pt[i].y) for pt in ptl.values()]
                upr   = [wolfvertex(pt[i].x, pt[i].y) for pt in ptr.values()]
                upr.reverse()
                downl = [wolfvertex(pt[i].x, pt[i].y) for pt in ptl2.values()]
                downl.reverse()
                downr = [wolfvertex(pt[i].x, pt[i].y) for pt in ptr2.values()]

                curvec.myvertices = sublsl.myvertices.copy() + downl[1:].copy() + [sublsc.myvertices[-1].copy()] + downr[:-1].copy() + sublsr.myvertices.copy() + upr[1:].copy() + [sublsc.myvertices[0].copy()] + upl[:-1].copy()
                for curvert in curvec.myvertices:
                    curvert.z = smean
                curvec.nbvertices = len(curvec.myvertices)

                #force to close the polygon
                curvec.close_force()
                #add vector to zone
                zonepoly.add_vector(curvec)

            #force to update minmax in the zone --> mandatory to plot
            zonepoly.find_minmax(True)
        else:
            #deux polygones sur base des // gauche et droite
            zonepolyleft = zone(name='polygons_left_'+self.myname,parent=self.parent)
            zonepolyright = zone(name='polygons_right_'+self.myname,parent=self.parent)
            self.parent.add_zone(zonepolyleft)
            self.parent.add_zone(zonepolyright)

            for i in range(nb):
                ptc1 = sc[i]
                ptc2 = sc2[i]
                pt1 = [cur[i] for cur in sl.values()]
                pt2 = [cur[i] for cur in sl2.values()]
                pt3 = [cur[i] for cur in sr.values()]
                pt4 = [cur[i] for cur in sr2.values()]

                #mean distance along center will be stored as Z value of each vertex
                smean =(ptc1+ptc2)/2.
                curvecleft=vector(name='poly'+str(i+1),parentzone=zonepolyleft)
                curvecright=vector(name='poly'+str(i+1),parentzone=zonepolyright)

                #Substring for Left and Right
                sublsl=vecleft[dpar].substring(pt1[-1], pt2[-1], is3D=False, adim=False)
                sublsr=vecright[dpar].substring(pt3[-1], pt4[-1], is3D=False, adim=False)
                sublsr.reverse()

                sublsc=veccenter.substring(ptc1,ptc2,is3D=False, adim=False)
                sublscr = sublsc.copy()
                sublscr.reverse()

                upl   = [wolfvertex(pt[i].x, pt[i].y) for pt in ptl.values()]
                upr   = [wolfvertex(pt[i].x, pt[i].y) for pt in ptr.values()]
                upr.reverse()
                downl = [wolfvertex(pt[i].x, pt[i].y) for pt in ptl2.values()]
                downl.reverse()
                downr = [wolfvertex(pt[i].x, pt[i].y) for pt in ptr2.values()]

                curvecleft.myvertices  = sublsl.myvertices.copy() + downl[1:-1].copy() + [sublscr.myvertices.copy()] + upl[1:-1].copy()
                curvecright.myvertices = sublsc.myvertices.copy() + downr[1:-1].copy() + [sublsr.myvertices.copy()] + upr[1:-1].copy()

                for curvert in curvecleft.myvertices:
                    curvert.z = smean
                for curvert in curvecright.myvertices:
                    curvert.z = smean
                curvecleft.nbvertices = len(curvecleft.myvertices)
                curvecright.nbvertices = len(curvecright.myvertices)

                curvecleft.close_force()
                curvecright.close_force()

                zonepolyleft.add_vector(curvecleft)
                zonepolyright.add_vector(curvecright)

            zonepolyleft.find_minmax(True)
            zonepolyright.find_minmax(True)

        self.parent.fill_structure()

        return myparallels

    def get_values_linked_polygons(self, linked_arrays, stats=True) -> dict:
        """
        Récupération des valeurs contenues dans tous les polygones de la zone

        Retourne un dictionnaire contenant les valeurs pour chaque polygone

        Les valeurs de chaque entrée du dict peuvent contenir une ou plusieurs listes en fonction du retour de la fonction de l'objet matriciel appelé
        """
        exit=True
        for curarray in linked_arrays:
            if curarray.plotted:
                exit=False

        if exit:
            return None

        vals= {idx: {'values' : curpol.get_values_linked_polygon(linked_arrays)} for idx, curpol in enumerate(self.myvectors)}

        if stats:
            self._stats_values(vals)

        return vals

    def get_all_values_linked_polygon(self, linked_arrays, stats=True, key_idx_names:Literal['idx', 'name']='idx', getxy=False) -> dict:
        """
        Récupération des valeurs contenues dans tous les polygones de la zone

        Retourne un dictionnaire contenant les valeurs pour chaque polygone

        ATTENTION :
           Il est possible de choisir comme clé soit l'index du vecteur dans la zone, soit non nom
           Si le nom est choisi, cela peut aboutir à une perte d'information car il n'y a pas de certitude que les noms de vecteur soient uniques
           --> il est nécessaire que l'utilisateur soit conscient de cette possibilité

        Les valeurs de chaque entrée du dict peuvent contenir une ou plusieurs listes en fonction du retour de la fonction de l'objet matriciel appelé
        """
        exit=True
        for curarray in linked_arrays:
            if curarray.plotted:
                exit=False

        if exit:
            return None

        if key_idx_names=='idx':
            vals= {idx: {'values' : curpol.get_all_values_linked_polygon(linked_arrays, getxy=getxy)} for idx, curpol in enumerate(self.myvectors)}
        else:
            vals= {curpol.myname: {'values' : curpol.get_all_values_linked_polygon(linked_arrays, getxy=getxy)} for idx, curpol in enumerate(self.myvectors)}

        # if stats:
        #     self._stats_values(vals)

        return vals

    def _stats_values(self,vals:dict):
        """
        Compute statistics on values dict resulting from 'get_values_linked_polygons'
        """
        for curpol in vals.values():
            medianlist  =curpol['median'] = []
            meanlist = curpol['mean'] = []
            minlist = curpol['min'] = []
            maxlist = curpol['max'] = []
            p95 = curpol['p95'] = []
            p5 = curpol['p5'] = []
            for curval in curpol['values']:

                if curval[1] is not None:

                    if curval[0] is not None and len(curval[0])>0:

                        medianlist.append(  (np.median(curval[0]),  np.median(curval[1]) ) )
                        meanlist.append(    (np.mean(curval[0]),    np.mean(curval[1]) ) )
                        minlist.append(     (np.min(curval[0]),      np.min(curval[1]) ) )
                        maxlist.append(     (np.max(curval[0]),      np.max(curval[1]) ) )
                        p95.append(         (np.percentile(curval[0],95),   np.percentile(curval[1],95) ) )
                        p5.append(          (np.percentile(curval[0],5),    np.percentile(curval[1],5)  ) )

                    else:
                        medianlist.append((None,None))
                        meanlist.append((None,None))
                        minlist.append((None,None))
                        maxlist.append((None,None))
                        p95.append((None,None))
                        p5.append((None,None))
                else:

                    if curval[0] is not None and len(curval[0])>0:
                        medianlist.append(np.median(curval[0]))
                        meanlist.append(np.mean(curval[0]))
                        minlist.append(np.min(curval[0]))
                        maxlist.append(np.max(curval[0]))
                        p95.append(np.percentile(curval[0],95))
                        p5.append(np.percentile(curval[0],5))
                    else:
                        medianlist.append(None)
                        meanlist.append(None)
                        minlist.append(None)
                        maxlist.append(None)
                        p95.append(None)
                        p5.append(None)

    def plot_linked_polygons(self, fig:Figure, ax:Axes, linked_arrays:dict, linked_vec:dict[str,"Zones"]=None, linestyle:str='-', onlymedian:bool=False, withtopography:bool = True, ds:float = None):
        """
        Création d'un graphique sur base des polygones

        Chaque polygone se positionnera sur base de la valeur Z de ses vertices
           - façon conventionnelle de définir une longueur
           - ceci est normalement fait lors de l'appel à 'create_polygon_from_parallel'
           - si les polygones sont créés manuellement, il faut donc prendre soin de fournir l'information adhoc ou alors utiliser l'rgument 'ds'

        ATTENTION : Les coordonnées Z ne sont sauvegardées sur disque que si le fichier est 3D, autrement dit au format '.vecz'

        :param fig: Figure
        :param ax: Axes
        :param linked_arrays: dictionnaire contenant les matrices à lier -- les clés sont les labels
        :param linked_vec: dictionnaire contenant les instances Zones à lier -- Besoin d'une zone et d'un vecteur 'trace/trace' pour convertir les positions en coordonnées curvilignes
        :param linestyle: style de ligne
        :param onlymedian: affiche uniquement la médiane
        :param withtopography: affiche la topographie
        :param ds: pas spatial le long de l'axe

        """
        colors=['red','blue','green','darkviolet','fuchsia','lime']

        #Vérifie qu'au moins une matrice liée est fournie, sinon rien à faire
        exit=True
        for curlabel, curarray in linked_arrays.items():
            if curarray.plotted:
                exit=False
        if exit:
            return

        k=0

        zmin=99999.
        zmax=-99999.

        if ds is None:
            # Récupération des positions
            srefs=np.asarray([curpol.myvertices[0].z for curpol in self.myvectors])
        else:
            # Création des positions sur base de 'ds'
            srefs=np.arange(0., float(self.nbvectors) * ds, ds)

        for idx, (curlabel, curarray) in enumerate(linked_arrays.items()):
            if curarray.plotted:

                logging.info(_('Plotting linked polygons for {}'.format(curlabel)))
                logging.info(_('Number of polygons : {}'.format(self.nbvectors)))
                logging.info(_('Extracting values inside polygons...'))

                vals= [curarray.get_values_insidepoly(curpol) for curpol in self.myvectors]

                logging.info(_('Computing stats...'))

                values = np.asarray([cur[0] for cur in vals],dtype=object)
                valel  = np.asarray([cur[1] for cur in vals],dtype=object)

                zmaxloc=np.asarray([np.max(curval) if len(curval) >0 else -99999. for curval in values])
                zminloc=np.asarray([np.min(curval) if len(curval) >0 else -99999. for curval in values])

                zmax=max(zmax,np.max(zmaxloc[np.where(zmaxloc>-99999.)]))
                zmin=min(zmin,np.min(zminloc[np.where(zminloc>-99999.)]))

                if zmax>-99999:

                    zloc = np.asarray([np.median(curpoly) if len(curpoly) >0 else -99999. for curpoly in values])

                    ax.plot(srefs[np.where(zloc!=-99999.)],zloc[np.where(zloc!=-99999.)],
                            color=colors[np.mod(k,3)],
                            lw=2.0,
                            linestyle=linestyle,
                            label=curlabel+'_median')

                    zloc = np.asarray([np.min(curpoly) if len(curpoly) >0 else -99999. for curpoly in values])

                    if not onlymedian:

                        ax.plot(srefs[np.where(zloc!=-99999.)],zloc[np.where(zloc!=-99999.)],
                                color=colors[np.mod(k,3)],alpha=.3,
                                lw=2.0,
                                linestyle=linestyle,
                                label=curlabel+'_min')

                        zloc = np.asarray([np.max(curpoly) if len(curpoly) >0 else -99999. for curpoly in values])

                        ax.plot(srefs[np.where(zloc!=-99999.)],zloc[np.where(zloc!=-99999.)],
                                color=colors[np.mod(k,3)],alpha=.3,
                                lw=2.0,
                                linestyle=linestyle,
                                label=curlabel+'_max')

                if withtopography and idx==0:
                    if valel[0] is not None:
                        zmaxloc=np.asarray([np.max(curval) if len(curval) >0 else -99999. for curval in valel])
                        zminloc=np.asarray([np.min(curval) if len(curval) >0 else -99999. for curval in valel])

                        zmax=max(zmax,np.max(zmaxloc[np.where(zmaxloc>-99999.)]))
                        zmin=min(zmin,np.min(zminloc[np.where(zminloc>-99999.)]))

                        if zmax>-99999:

                            zloc = np.asarray([np.median(curpoly) if len(curpoly) >0 else -99999. for curpoly in valel])

                            ax.plot(srefs[np.where(zloc!=-99999.)],zloc[np.where(zloc!=-99999.)],
                                    color='black',
                                    lw=2.0,
                                    linestyle=linestyle,
                                    label=curlabel+'_top_median')

                        # if not onlymedian:
                            # zloc = np.asarray([np.min(curpoly) for curpoly in valel])

                            # ax.plot(srefs[np.where(zloc!=-99999.)],zloc[np.where(zloc!=-99999.)],
                            #         color='black',alpha=.3,
                            #         lw=2.0,
                            #         linestyle=linestyle,
                            #         label=curlabel+'_top_min')

                            # zloc = np.asarray([np.max(curpoly) for curpoly in valel])

                            # ax.plot(srefs[np.where(zloc!=-99999.)],zloc[np.where(zloc!=-99999.)],
                            #         color='black',alpha=.3,
                            #         lw=2.0,
                            #         linestyle=linestyle,
                            #         label=curlabel+'_top_max')

                k+=1

        for curlabel, curzones in linked_vec.items():
            curzones:Zones
            names = [curzone.myname for curzone in curzones.myzones]
            trace = None
            tracels = None

            logging.info(_('Plotting linked zones for {}'.format(curlabel)))

            curzone: zone
            if 'trace' in names:
                curzone = curzones.get_zone('trace')
                trace = curzone.get_vector('trace')

                if trace is None:
                    if curzone is not None:
                        if curzone.nbvectors>0:
                            trace = curzone.myvectors[0]

                if trace is not None:
                    tracels = trace.asshapely_ls()
                else:
                    logging.warning(_('No trace found in the vectors {}'.format(curlabel)))
                    break

            if ('marks' in names) or ('repères' in names):
                if ('marks' in names):
                    curzone = curzones.myzones[names.index('marks')]
                else:
                    curzone = curzones.myzones[names.index('repères')]

                logging.info(_('Plotting marks for {}'.format(curlabel)))
                logging.info(_('Number of marks : {}'.format(curzone.nbvectors)))

                for curvect in curzone.myvectors:
                    curls = curvect.asshapely_ls()

                    if curls.intersects(tracels):
                        inter = curls.intersection(tracels)
                        curs = float(tracels.project(inter))

                        ax.plot([curs, curs], [zmin, zmax], linestyle='--', label=curvect.myname)
                        ax.text(curs, zmax, curvect.myname, fontsize=8, ha='center', va='bottom')

            if ('banks' in names) or ('berges' in names):

                if ('banks' in names):
                    curzone = curzones.myzones[names.index('banks')]
                else:
                    curzone = curzones.myzones[names.index('berges')]

                logging.info(_('Plotting banks for {}'.format(curlabel)))
                logging.info(_('Number of banks : {}'.format(curzone.nbvectors)))

                for curvect in curzone.myvectors:
                    curvect: vector

                    curproj = curvect.projectontrace(trace)
                    sz = curproj.asnparray()
                    ax.plot(sz[:,0], sz[:,1], label=curvect.myname)

            if ('bridges' in names) or ('ponts' in names):
                if ('bridges' in names):
                    curzone = curzones.myzones[names.index('bridges')]
                else:
                    curzone = curzones.myzones[names.index('ponts')]

                logging.info(_('Plotting bridges for {}'.format(curlabel)))

                for curvect in curzone.myvectors:
                    curvect: vector
                    curls = curvect.asshapely_ls()

                    if curls.intersects(tracels):

                        logging.info(_('Bridge {} intersects the trace'.format(curvect.myname)))

                        inter = curls.intersection(tracels)
                        curs = float(tracels.project(inter))
                        locz = np.asarray([vert.z for vert in curvect.myvertices])
                        zmin = np.amin(locz)
                        zmax = np.amax(locz)

                        ax.scatter(curs, zmin, label=curvect.myname + ' min')
                        ax.scatter(curs, zmax, label=curvect.myname + ' max')

        ax.set_ylim(zmin,zmax)
        zmodmin= np.floor_divide(zmin*100,25)*25/100
        ax.set_yticks(np.arange(zmodmin,zmax,.25))
        fig.canvas.draw()

    def reset_listogl(self):
        """
        Reset des liste OpenGL
        """
        if self.idgllist!=-99999:
            glDeleteLists(self.idgllist,1)
            self.idgllist=-99999

    def deepcopy_zone(self, name: str =None, parent: str= None):
        """
        Return a deep copy of the zone.
        """
        if name is None:
            name =  self.myname + '_copy'
            if parent:
                copied_zone = zone(name=name, parent=parent)
            else:
                copied_zone = zone(name=name)
            copied_zone.myvectors = []
            for vec in self.myvectors:
                copied_vec = vec.deepcopy_vector(parentzone = copied_zone)
                copied_zone.add_vector(copied_vec)
            #     copied_zone.myvectors.append(copied_vec)
            # copied_zone.nbvectors = len(copied_zone.myvectors) FIXME not needed anymore
            return copied_zone

class Zones(wx.Frame, Element_To_Draw):
    """
    Objet de gestion d'informations vectorielles

    Une instance 'Zones' contient une liste de 'zone'

    Une instance 'zone' contient une listde de 'vector' (segment, ligne, polyligne, polygone...)
    """

    tx:float
    ty:float

    # nbzones:int

    myzones:list[zone]
    treelist:TreeListCtrl
    xls:CpGrid

    def __init__(self,
                 filename:Union[str, Path]='',
                 ox:float=0.,
                 oy:float=0.,
                 tx:float=0.,
                 ty:float=0.,
                 parent=None,
                 is2D=True,
                 idx: str = '',
                 plotted: bool = True,
                 mapviewer=None,
                 need_for_wx: bool = False,
                 bbox:Polygon = None,
                 find_minmax:bool = True) -> None:
        """
        Objet de gestion et d'affichage d'informations vectorielles

        :param filename: nom du fichier à lire
        :param ox: origine X
        :param oy: origine Y
        :param tx: Translation selon X
        :param ty: Translation selon Y
        :param parent: objet parent -- soit une instance 'WolfMapViewer', soit une instance 'Ops_Array' --> est utile pour transférer la propriété 'active_vector' et obtenir diverses informations ou lancer des actions
        :param is2D: si True --> les vecteurs sont en 2D
        :param idx: identifiant
        :param plotted: si True --> les vecteurs sont prêts à être affichés
        :param mapviewer: instance WolfMapViewer
        :param need_for_wx: si True --> permet l'affichage de la structure via WX car une app WX existe et est en cours d'exécution
        :param bbox: bounding box
        :param find_minmax: si True --> recherche des valeurs min et max

        wx_exists : si True --> permet l'affichage de la structure via WX car une app WX existe et est en cours d'exécution

        Si wx_exists alors on cherche une instance WolfMapViewer depuis le 'parent' --> set_mapviewer()
        Dans ce cas, le parent doit posséder une routine du type 'get_mapviewer()'

        Exemple :

        def get_mapviewer(self):
            # Retourne une instance WolfMapViewer
            return self.mapviewer
        """

        Element_To_Draw.__init__(self, idx, plotted, mapviewer, need_for_wx)

        self.loaded=True

        self.active_vector:vector = None
        self.active_zone:zone = None
        self.last_active = None # dernier élément activé dans le treelist

        self.force3D=False
        self.is2D=is2D

        self.filename=str(filename)

        self.parent = parent        # objet parent (PyDraw, OpsArray, Wolf2DModel...)

        self.wx_exists = wx.App.Get() is not None
        self.xls = None
        self.labelactvect = None
        self.labelactzone = None

        if self.wx_exists:

            self.set_mapviewer()

            try:
                super(Zones, self).__init__(None, size=(300, 400))
                self.Bind(wx.EVT_CLOSE,self.OnClose) # on lie la procédure de fermeture de façon à juste masquer le Frame et non le détruire
            except:
                raise Warning(_('Bad wx context -- see Zones.__init__'))

        self.init_struct=True # il faudra initialiser la structure dans showstructure lors du premier appel

        self.xmin=ox
        self.ymin=oy
        self.tx=tx
        self.ty=ty
        self.myzones=[]

        if self.filename!='':
            # lecture du fichier

            if self.filename.endswith('.dxf'):
                self.is2D=False
                self.import_dxf(self.filename)
            elif self.filename.endswith('.shp'):
                self.is2D=False
                self.import_shapefile(self.filename, bbox=bbox)
            elif self.filename.endswith('.gpkg'):
                self.is2D=False
                self.import_gpkg(self.filename, bbox=bbox)
            elif Path(filename).is_dir() and self.filename.endswith('.gdb'):
                self.is2D=False
                self.import_gdb(self.filename, bbox=bbox)
            else:
                if self.filename.endswith('.vecz'):
                    self.is2D=False

                f = open(self.filename, 'r')
                lines = f.read().splitlines()
                f.close()

                try:
                    tx,ty=lines[0].split()
                except:
                    tx,ty=lines[0].split(',')

                self.tx=float(tx)
                self.ty=float(ty)
                tmp_nbzones=int(lines[1])

                curstart=2
                for i in range(tmp_nbzones):
                    curzone=zone(lines[curstart:],parent=self,is2D=self.is2D)
                    self.myzones.append(curzone)
                    curstart+=curzone._nblines()

            if find_minmax:
                self.find_minmax(True)

        if plotted:
            self.prep_listogl()

    @property
    def nbzones(self):
        return len(self.myzones)

    def import_shapefile(self, fn:str, bbox:Polygon = None):
        """ Import shapefile by using geopandas """

        content = gpd.read_file(fn, bbox=bbox)

        for idx, row in content.iterrows():
            if 'NAME' in row.keys():
                name = row['NAME']
            elif 'MAJ_NIV3T' in row.keys():
                # WALOUS
                name = row['MAJ_NIV3T']
            elif 'NATUR_DESC' in row.keys():
                name = row['NATUR_DESC']
            else:
                name = str(idx)

            poly = row['geometry']

            newzone = zone(name=name, parent = self, fromshapely = poly)
            self.add_zone(newzone)

    def import_gdb(self, fn:str, bbox:Polygon = None):
        """ Import gdb by using geopandas and Fiona"""

        import fiona

        layers = fiona.listlayers(fn)

        if self.wx_exists:
            dlg = wx.MultiChoiceDialog(None, _('Choose the layers to import'), _('Choose the layers'), layers)

            if dlg.ShowModal() == wx.ID_OK:
                layers = [layers[i] for i in dlg.GetSelections()]
            else:
                return

        for curlayer in layers:

            content = gpd.read_file(fn, bbox=bbox, layer=curlayer)

            if len(content)>1000:
                logging.warning(_('Layer {} contains more than 1000 elements -- it may take a while to import'.format(curlayer)))

            for idx, row in content.iterrows():
                if 'NAME' in row.keys():
                    name = row['NAME']
                elif 'MAJ_NIV3T' in row.keys():
                    # WALOUS
                    name = row['MAJ_NIV3T']
                elif 'NATUR_DESC' in row.keys():
                    name = row['NATUR_DESC']
                else:
                    name = str(idx)

                poly = row['geometry']

                newzone = zone(name=name, parent = self, fromshapely = poly)
                self.add_zone(newzone)

                if len(content)>1000:
                    if idx%100==0:
                        logging.info(_('Imported {} elements'.format(idx)))

    def import_gpkg(self, fn:str, bbox:Polygon = None):
        """ Import gdb by using geopandas and Fiona"""

        import fiona

        layers = fiona.listlayers(fn)

        if self.wx_exists:
            dlg = wx.MultiChoiceDialog(None, _('Choose the layers to import'), _('Choose the layers'), layers)

            if dlg.ShowModal() == wx.ID_OK:
                layers = [layers[i] for i in dlg.GetSelections()]
            else:
                return

        for curlayer in layers:

            content = gpd.read_file(fn, bbox=bbox, layer=curlayer)

            if len(content)>1000:
                logging.warning(_('Layer {} contains more than 1000 elements -- it may take a while to import'.format(curlayer)))

            for idx, row in content.iterrows():
                if 'NAME' in row.keys():
                    name = row['NAME']
                elif 'MAJ_NIV3T' in row.keys():
                    # WALOUS
                    name = row['MAJ_NIV3T']
                elif 'NATUR_DESC' in row.keys():
                    name = row['NATUR_DESC']
                elif 'Type' in row.keys():
                    name = row['Type']
                else:
                    name = str(idx)

                poly = row['geometry']

                newzone = zone(name=name, parent = self, fromshapely = poly)
                self.add_zone(newzone)

                if len(content)>1000:
                    if idx%100==0:
                        logging.info(_('Imported {} elements'.format(idx)))

    def set_mapviewer(self):
        """ Recherche d'une instance WolfMapViewer depuis le parent """
        from .PyDraw import WolfMapViewer

        if self.parent is None:
            # Nothing to do because 'parent' is None
            return

        try:
            self.mapviewer = self.parent.get_mapviewer()
        except:
            self.mapviewer = None

            assert isinstance(self.mapviewer, WolfMapViewer), _('Bad mapviewer -- verify your code or bad parent')

    def colorize_data(self, colors:dict[str:list[int]]) -> None:
        """
        Colorize zones based on a dictionary of colors

        Zone's name must be the key of the dictionary

        """

        std_color = getIfromRGB([10, 10, 10])

        for curzone in self.myzones:
            if curzone.myname in colors:
                curcolor = getIfromRGB(colors[curzone.myname])
            else:
                curcolor = std_color

            for curvect in curzone.myvectors:
                curvect.myprop.color = curcolor
                curvect.myprop.alpha = 180
                curvect.myprop.transparent = True
                curvect.myprop.filled = True

    def set_width(self, width:int) -> None:
        """ Change with of all vectors in all zones """
        for curzone in self.myzones:
            for curvect in curzone.myvectors:
                curvect.myprop.width = width

        self.prep_listogl()

    def get_zone(self,keyzone:Union[int, str])->zone:
        """
        Retrouve la zone sur base de son nom ou de sa position
        Si plusieurs zones portent le même nom, seule la première est retournée
        """
        if isinstance(keyzone,int):
            if keyzone<self.nbzones:
                return self.myzones[keyzone]
            return None
        if isinstance(keyzone,str):
            zone_names = [cur.myname for cur in self.myzones]
            if keyzone in zone_names:
                return self.myzones[zone_names.index(keyzone)]
            return None

    def __getitem__(self, ndx:Union[int, str, tuple]) -> Union[zone, vector]:
        """
        Retourne la zone sur base de son nom ou de sa position

        :param ndx: Clé ou index de zone -- si tuple, alors (idx_zone, idx_vect)

        """

        if isinstance(ndx,tuple):
            idx_zone = ndx[0]
            idx_vect = ndx[1]

            return self.get_zone(idx_zone)[idx_vect]
        else:
            return self.get_zone(ndx)

    def import_dxf(self, fn, imported_elts=['POLYLINE','LWPOLYLINE','LINE']):
        """
        Import d'un fichier DXF en tant qu'objets WOLF
        """
        import ezdxf

        if not path.exists(fn):
            try:
                logging.warning(_('File not found !') + ' ' + fn)
            except:
                pass
            return

        # Lecture du fichier dxf et identification du modelspace
        doc = ezdxf.readfile(fn)
        msp = doc.modelspace()
        layers = doc.layers

        used_layers = {}
        # Bouclage sur les éléments du DXF pour identifier les layers utiles et ensuite créer les zones adhoc
        for e in msp:
            if doc.layers.get(e.dxf.layer).is_on():
                if e.dxftype() == "POLYLINE":
                    if e.dxf.layer not in used_layers.keys():
                        curlayer = used_layers[e.dxf.layer]={}
                    else:
                        curlayer = used_layers[e.dxf.layer]
                    curlayer[e.dxftype().lower()]=0

                elif e.dxftype() == "LWPOLYLINE":
                    if e.dxf.layer not in used_layers.keys():
                        curlayer = used_layers[e.dxf.layer]={}
                    else:
                        curlayer = used_layers[e.dxf.layer]
                    curlayer[e.dxftype().lower()]=0

                elif e.dxftype() == "LINE": # dans ce cas spécifique, ce sont a priori les lignes composant les croix sur les points levés
                    if e.dxf.layer not in used_layers.keys():
                        curlayer = used_layers[e.dxf.layer]={}
                    else:
                        curlayer = used_layers[e.dxf.layer]
                    curlayer[e.dxftype().lower()]=0
            else:
                pass

        # Création des zones
        for curlayer in used_layers.keys():
            for curtype in used_layers[curlayer].keys():
                curzone = used_layers[curlayer][curtype] = zone(name = '{} - {}'.format(curlayer,curtype),is2D=self.is2D,parent=self)
                self.add_zone(curzone)

        # Nouveau bouclage sur les éléments du DXF pour remplissage
        nbid=0
        for e in msp:
            if doc.layers.get(e.dxf.layer).is_on():

                if e.dxftype() == "POLYLINE":
                    nbid+=1
                    # récupération des coordonnées
                    verts = [cur.dxf.location.xyz for cur in e.vertices]

                    curzone = used_layers[e.dxf.layer][e.dxftype().lower()]

                    curpoly = vector(is2D=False,name=e.dxf.handle,parentzone=curzone)
                    curzone.add_vector(curpoly)

                    for cur in verts:
                        myvert = wolfvertex(cur[0],cur[1],cur[2])
                        curpoly.add_vertex(myvert)

                elif e.dxftype() == "LWPOLYLINE":
                    nbid+=1
                    # récupération des coordonnées
                    verts = np.array(e.lwpoints.values)
                    verts = verts.reshape([int(len(verts)/5),5])[:,:2]
                    verts = np.column_stack([verts,[e.dxf.elevation]*len(verts)])

                    curzone = used_layers[e.dxf.layer][e.dxftype().lower()]

                    curpoly = vector(is2D=False,name=e.dxf.handle,parentzone=curzone)
                    curzone.add_vector(curpoly)
                    for cur in verts:
                        myvert = wolfvertex(cur[0],cur[1],cur[2])
                        curpoly.add_vertex(myvert)

                elif e.dxftype() == "LINE":
                    nbid+=1

                    curzone = used_layers[e.dxf.layer][e.dxftype().lower()]

                    curpoly = vector(is2D=False,name=e.dxf.handle,parentzone=curzone)
                    curzone.add_vector(curpoly)

                    # récupération des coordonnées
                    myvert = wolfvertex(e.dxf.start[0],e.dxf.start[1],e.dxf.start[2])
                    curpoly.add_vertex(myvert)
                    myvert = wolfvertex(e.dxf.end[0],e.dxf.end[1],e.dxf.end[2])
                    curpoly.add_vertex(myvert)

        logging.info(_('Number of imported elements : ')+str(nbid))

    def find_nearest_vector(self, x:float, y:float) -> vector:
        """
        Trouve le vecteur le plus proche de la coordonnée (x,y)
        """
        xy=Point(x,y)

        distmin=99999.
        minvec=None
        curzone:zone
        for curzone in self.myzones:
            curvect:vector
            for curvect in curzone.myvectors:
                mynp = curvect.asnparray()
                mp = MultiPoint(mynp)
                near = nearest_points(mp,xy)[0]
                dist = xy.distance(near)
                if dist < distmin:
                    minvec=curvect
                    distmin=dist

        return minvec

    def reset_listogl(self):
        """
        Reset des listes OpenGL pour toutes les zones
        """
        for curzone in self.myzones:
            curzone.reset_listogl()

    def prep_listogl(self):
        """
        Préparation des listes OpenGL pour augmenter la vitesse d'affichage
        """
        for curzone in self.myzones:
            curzone.prep_listogl()

    def check_plot(self):
        """
        L'objet doit être affiché

        Fonction principalement utile pour l'objet WolfMapViewer et le GUI
        """
        self.plotted = True

    def uncheck_plot(self, unload=True):
        """
        L'objet ne doit pas être affiché

        Fonction principalement utile pour l'objet WolfMapViewer et le GUI
        """
        self.plotted = False

    def saveas(self, filename=''):
        """
        Sauvegarde sur disque

        filename : chemin d'accès potentiellement différent de self.filename

        si c'est le cas, self.filename est modifié
        """
        if filename!='':
            self.filename=filename

        if self.filename.endswith('.vecz'):
            self.force3D=True #on veut un fichier 3D --> forcage du paramètre

        with open(self.filename, 'w') as f:
            f.write(f'{self.tx} {self.ty}'+'\n')
            f.write(str(self.nbzones)+'\n')
            for curzone in self.myzones:
                curzone.save(f)

        with open(self.filename + '.extra', 'w') as f:
            for curzone in self.myzones:
                curzone.save_extra(f)

    def OnClose(self, e):
        """
        Fermeture de la fenêtre
        """
        if self.wx_exists:
            self.Hide()

    def add_zone(self, addedzone:zone, forceparent=False):
        """
        Ajout d'une zone à la liste
        """
        self.myzones.append(addedzone)

        if forceparent:
            addedzone.parent = self

    def find_minmax(self, update=False, only_firstlast:bool=False):
        """
        Trouve les bornes des vertices pour toutes les zones et tous les vecteurs

        :param update : si True, force la MAJ des minmax dans chaque zone; si False, compile les minmax déjà présents
        :param only_firstlast : si True, ne prend en compte que le premier et le dernier vertex de chaque vecteur
        """
        if update:
            for zone in self.myzones:
                zone.find_minmax(update, only_firstlast)

        if len(self.myzones)>0:

            minsx=np.asarray([zone.xmin for zone in self.myzones])
            minsy=np.asarray([zone.ymin for zone in self.myzones])
            maxsx=np.asarray([zone.xmax for zone in self.myzones])
            maxsy=np.asarray([zone.ymax for zone in self.myzones])

            if len(minsx)>1:
                self.xmin=np.min(minsx[np.where(minsx!=-99999.)])
                self.xmax=np.max(maxsx[np.where(maxsx!=-99999.)])
                self.ymin=np.min(minsy[np.where(minsy!=-99999.)])
                self.ymax=np.max(maxsy[np.where(maxsy!=-99999.)])
            else:
                self.xmin=minsx[0]
                self.xmax=maxsx[0]
                self.ymin=minsy[0]
                self.ymax=maxsy[0]
        else:
            self.xmin=0.
            self.ymin=0.
            self.xmax=1.
            self.ymax=1.

    def plot(self, sx=None, sy=None, xmin=None, ymin=None, xmax=None, ymax=None, size=None):
        """
        Dessine les zones
        """
        for curzone in self.myzones:
            curzone.plot()

    def select_vectors_from_point(self, x:float, y:float, inside=True):
        """
        Sélection de vecteurs dans chaque zones sur base d'une coordonnée
          --> remplit la liste 'selected_vectors' de chaque zone

        inside : si True, teste si le point est contenu dans le polygone; si False, sélectionne le vecteur le plus proche
        """
        xmin=1e30
        for curzone in self.myzones:
            xmin = curzone.select_vectors_from_point(x,y,inside)

    def show_properties(self, parent=None, forceupdate=False):
        """
        Affichage des propriétés des zones

        parent : soit une instance 'WolfMapViewer', soit une instance 'Ops_Array'  --> est utile pour transférer la propriété 'active_vector' et obtenir diverses informations
          si parent est d'un autre type, il faut s'assurer que les options/actions sont consistantes

        """
        self.showstructure(parent,forceupdate)

    def showstructure(self, parent=None, forceupdate=False):
        """
        Affichage de la structure des zones

        parent : soit une instance 'WolfMapViewer', soit une instance 'Ops_Array'  --> est utile pour transférer la propriété 'active_vector' et obtenir diverses informations
          si parent est d'un autre type, il faut s'assurer que les options/actions sont consistantes

        """
        if self.parent is None:
            self.parent = parent

        self.wx_exists = wx.App.Get() is not None

        if forceupdate:
            self.init_struct = True
            self.parent = parent

        if self.wx_exists:
            self.set_mapviewer()
            # wx est initialisé et tourne --> on peut créer le Frame associé aux vecteurs
            if self.init_struct:
                self.init_ui()

            self.Show()

    def init_ui(self):
        """
        Création de l'interface wx de gestion de l'objet
        """
        if self.wx_exists:
            # la strcuture n'existe pas encore
            box = BoxSizer(orient=wx.HORIZONTAL)

            boxleft = BoxSizer(orient=wx.VERTICAL)
            boxright = BoxSizer(orient=wx.VERTICAL)

            boxadd = BoxSizer(orient=wx.VERTICAL)
            boxdelete = BoxSizer(orient=wx.VERTICAL)
            boxupdown = BoxSizer(orient=wx.HORIZONTAL)
            boxupdownv = BoxSizer(orient=wx.VERTICAL)
            boxupdownz = BoxSizer(orient=wx.VERTICAL)

            self.xls=CpGrid(self,-1,wx.WANTS_CHARS)
            self.xls.CreateGrid(10,5)

            self.addrows = wx.Button(self,label=_('Add rows'))
            self.addrows.SetToolTip(_("Add rows to the grid --> Useful for manually adding some points to a vector"))
            self.addrows.Bind(wx.EVT_BUTTON,self.Onaddrows)

            self.updatevertices = wx.Button(self,label=_('Update coordinates'))
            self.updatevertices.SetToolTip(_("Transfer the coordinates from the editor to the memory and update the plot"))
            self.updatevertices.Bind(wx.EVT_BUTTON,self.Onupdatevertices)

            self.capturevertices = wx.Button(self,label=_('Add'))
            self.capturevertices.SetToolTip(_("Capture new points from mouse clicks \n\n Keyboard 'Return' to stop the action ! "))
            self.capturevertices.Bind(wx.EVT_BUTTON,self.Oncapture)

            self.modifyvertices = wx.Button(self,label=_('Modify'))
            self.modifyvertices.SetToolTip(_("Modify some point from mouse clicks \n\n - First click around the desired point \n - Move the position \n - Validate by a click \n\n Keyboard 'Return' to stop the action ! "))
            self.modifyvertices.Bind(wx.EVT_BUTTON,self.Onmodify)

            self.dynapar = wx.Button(self,label=_('Add and parallel'))
            self.dynapar.SetToolTip(_("Capture new points from mouse clicks and create parallel \n\n - MAJ + Middle Mouse Button to adjust the semi-distance \n - CTRL + MAJ + Middle Mouse Button to choose specific semi-distance \n\n Keyboard 'Return' to stop the action ! "))
            self.dynapar.Bind(wx.EVT_BUTTON,self.OncaptureandDynapar)

            self.createapar = wx.Button(self,label=_('Create parallel'))
            self.createapar.SetToolTip(_("Create a single parallel to the currently activated vector as a new vector in the same zone"))
            self.createapar.Bind(wx.EVT_BUTTON,self.OnAddPar)

            self.reverseorder = wx.Button(self,label=_('Reverse points order'))
            self.reverseorder.SetToolTip(_("Reverse the order/sens of the currently activated vector -- Overwrite the data"))
            self.reverseorder.Bind(wx.EVT_BUTTON,self.OnReverse)

            self.sascending = wx.Button(self,label=_('Verify vertices positions'))
            self.sascending.SetToolTip(_("Check whether the vertices of the activated vector are ordered according to increasing 's' defined as 2D geometric distance \n If needed, invert some positions and return information to the user"))
            self.sascending.Bind(wx.EVT_BUTTON,self.Onsascending)

            self.insertvertices = wx.Button(self,label=_('Insert'))
            self.insertvertices.SetToolTip(_("Insert new vertex into the currently active vector from mouse clicks \n The new vertex is inserted along the nearest segment  \n\n Keyboard 'Return' to stop the action ! "))
            self.insertvertices.Bind(wx.EVT_BUTTON,self.Oninsert)

            self.splitvertices = wx.Button(self,label=_('Copy and Split'))
            self.splitvertices.SetToolTip(_("Make a copy of the currently active vector and add new vertices according to a user defined length \n The new vertices are evaluated based on a 3D curvilinear distance"))
            self.splitvertices.Bind(wx.EVT_BUTTON,self.Onsplit)

            self.interpxyz = wx.Button(self,label=_('Interpolate coords'))
            self.interpxyz.SetToolTip(_("Linear Interpolation of the Z values if empty or egal to -99999 \n The interpolation uses the 's' value contained in the 5th column of the grid, X being the first one"))
            self.interpxyz.Bind(wx.EVT_BUTTON,self.Oninterpvec)

            self.evaluates = wx.Button(self,label=_('Evaluate s'))
            self.evaluates.SetToolTip(_("Calculate the curvilinear 's' distance using a '2D' or '3D' approach and store the result in the 5th column of the grid, X being the first one"))
            self.evaluates.Bind(wx.EVT_BUTTON,self.Onevaluates)

            #  Modified
            self.zoomonactive = wx.Button(self,label=_('Zoom on active vector'))
            self.zoomonactive.SetToolTip(_("Zoom on the active vector and a default view size of 500 m x 500 m"))
            self.zoomonactive.Bind(wx.EVT_BUTTON,self.Onzoom)

            # Added
            self.zoomonactivevertex = wx.Button(self, label =_('Zoom on active vertex'))
            self.zoomonactivevertex.SetToolTip(_("Zoom on the active vertex and a default view size of 50 m x 50 m"))
            self.zoomonactivevertex.Bind(wx.EVT_BUTTON, self.Onzoomvertex)
            boxzoom = BoxSizer(orient=wx.HORIZONTAL)
            boxzoom.Add(self.zoomonactive,1, wx.EXPAND)
            boxzoom.Add(self.zoomonactivevertex,1, wx.EXPAND)

            self.saveimages = wx.Button(self,label=_('Save images from active zone'))
            self.saveimages.Bind(wx.EVT_BUTTON,self.Onsaveimages)

            self.binfrom3 = wx.Button(self,label=_('Create bin from 3 vectors'))
            self.binfrom3.SetToolTip(_("Create a bin/rectangular channel based on 3 vectors in the currently active zone \n Some parameters will be prompted to the user (lateral height, ...) and if a triangular mesh must be created --> Blender"))
            self.binfrom3.Bind(wx.EVT_BUTTON,self.Oncreatebin)

            self.trifromall = wx.Button(self,label=_('Create tri from all vectors'))
            self.trifromall.SetToolTip(_("Create a triangular mesh based on all vectors in the currently active zone and add the result to the GUI \n Useful in some interpolation method"))
            self.trifromall.Bind(wx.EVT_BUTTON,self.Oncreatemultibin)

            self.trifromall_proj = wx.Button(self,label=_('Create tri from all vectors (projection)'))
            self.trifromall_proj.SetToolTip(_("Create a triangular mesh based on all vectors in the currently active zone and add the result to the GUI \n Useful in some interpolation method"))
            self.trifromall_proj.Bind(wx.EVT_BUTTON,self.Oncreatemultibin_project)

            self.polyfrompar = wx.Button(self,label=_('Create polygons from parallels'))
            self.polyfrompar.SetToolTip(_("Create polygons in a new zone from parallels defined by " + _('Add and parallel') + _(" and a 2D curvilinear distance \n Useful for plotting some results or analyse data inside each polygon")))
            self.polyfrompar.Bind(wx.EVT_BUTTON,self.Oncreatepolygons)

            # Added
            self.getxyfromsz = wx.Button(self, label = _('Get xy from sz'))
            self.getxyfromsz.SetToolTip(_("Populate the X an Y columns based on: \n - Given sz coordinates, \n - The X and Y coordinates of the initial point (s = 0) and,  \n - The X and Y coordinates of a second point (any other point with an S coordinate)"))
            self.getxyfromsz.Bind(wx.EVT_BUTTON, self.get_xy_from_sz)

            boxright.Add(self.xls,1,wx.EXPAND)
            boxright.Add(self.addrows,0,wx.EXPAND)
            boxright.Add(self.capturevertices,0,wx.EXPAND)
            boxright.Add(self.dynapar,0,wx.EXPAND)
            boxright.Add(self.createapar,0,wx.EXPAND)
            boxright.Add(self.modifyvertices,0,wx.EXPAND)
            boxright.Add(self.insertvertices,0,wx.EXPAND)
            boxright.Add(self.splitvertices,0,wx.EXPAND)
            # boxright.Add(self.zoomonactive,0,wx.EXPAND)
            boxright.Add(boxzoom,0,wx.EXPAND)
            boxright.Add(self.sascending,0,wx.EXPAND)
            boxright.Add(self.evaluates,0,wx.EXPAND)
            boxright.Add(self.getxyfromsz,0,wx.EXPAND) # Added
            boxright.Add(self.interpxyz,0,wx.EXPAND)
            boxright.Add(self.updatevertices,0,wx.EXPAND)

            self.butgetval = wx.Button(self,label=_('Get values (self or active array)'))
            self.butgetval.SetToolTip(_("Get values of the attached/active array on each vertex of the active vector and update the editor"))
            self.butgetval.Bind(wx.EVT_BUTTON,self.Ongetvalues)
            boxright.Add(self.butgetval,0,wx.EXPAND)

            self.butgetvallinked = wx.Button(self,label=_('Get values (all arrays)'))
            self.butgetvallinked.SetToolTip(_("Get values of all the visible arrays and 2D results on each vertex of the active vector \n\n Create a new zone containing the results"))
            self.butgetvallinked.Bind(wx.EVT_BUTTON,self.Ongetvalueslinked)

            self.butgetrefvallinked = wx.Button(self,label=_('Get values (all arrays and remeshing)'))
            self.butgetrefvallinked.SetToolTip(_("Get values of all the visible arrays and 2D results on each vertex of the active vector \n and more is the step size of the array is more precise \n\n Create a new zone containing the results"))
            self.butgetrefvallinked.Bind(wx.EVT_BUTTON,self.Ongetvalueslinkedandref)

            boxright.Add(self.butgetvallinked,0,wx.EXPAND)
            boxright.Add(self.butgetrefvallinked,0,wx.EXPAND)

            self.treelist = TreeListCtrl(self,style=TL_CHECKBOX|wx.TR_FULL_ROW_HIGHLIGHT|wx.TR_EDIT_LABELS)
            self.treelist.AppendColumn('Zones')
            self.treelist.Bind(EVT_TREELIST_ITEM_CHECKED, self.OnCheckItem)
            self.treelist.Bind(EVT_TREELIST_ITEM_ACTIVATED, self.OnActivateItem)
            self.treelist.Bind(EVT_TREELIST_ITEM_CONTEXT_MENU,self.OnRDown)

            self.treelist.Bind(wx.EVT_CHAR,self.OnEditLabel)

            self.labelactvect = wx.StaticText( self, wx.ID_ANY, _("None"), style=wx.ALIGN_CENTER_HORIZONTAL )
            self.labelactvect.Wrap( -1 )
            self.labelactvect.SetToolTip(_('Name of the active vector'))
            self.labelactzone = wx.StaticText( self, wx.ID_ANY, _("None"), style=wx.ALIGN_CENTER_HORIZONTAL )
            self.labelactzone.Wrap( -1 )
            self.labelactzone.SetToolTip(_('Name of the active zone'))

            self.addzone = wx.Button(self,label=_('Add zone'))
            self.addvector = wx.Button(self,label=_('Add vector'))
            self.deletezone = wx.Button(self,label=_('Delete zone'))
            self.findactivevector = wx.Button(self,label=_('Find in whole zones'))
            self.findactivevector.SetToolTip(_("Search and activate the nearest vector by mouse click (Searching window : all zones)"))
            self.findactivevectorcurz = wx.Button(self,label=_('Find in active zone'))
            self.findactivevectorcurz.SetToolTip(_("Search and activate the nearest vector by mouse click (Searching window : active zone)"))
            self.deletevector = wx.Button(self,label=_('Delete vector'))

            self.upvector = wx.Button(self,label=_('Up vector'))
            self.downvector = wx.Button(self,label=_('Down vector'))
            self.upzone = wx.Button(self,label=_('Up zone'))
            self.downzone = wx.Button(self,label=_('Down zone'))
            # self.interpolate = wx.Button(self,label=_('Interpolate vector'))

            self.addzone.Bind(wx.EVT_BUTTON,self.OnClickadd_zone)
            self.addvector.Bind(wx.EVT_BUTTON,self.OnClickadd_vector)
            self.deletezone.Bind(wx.EVT_BUTTON,self.OnClickdelete_zone)
            self.deletevector.Bind(wx.EVT_BUTTON,self.OnClickdelete_vector)
            self.upvector.Bind(wx.EVT_BUTTON,self.OnClickup_vector)
            self.downvector.Bind(wx.EVT_BUTTON,self.OnClickdown_vector)

            self.upzone.Bind(wx.EVT_BUTTON,self.OnClickup_zone)
            self.downzone.Bind(wx.EVT_BUTTON,self.OnClickdown_zone)

            # self.interpolate.Bind(wx.EVT_BUTTON,self.OnClickInterpolate)
            self.findactivevector.Bind(wx.EVT_BUTTON,self.OnClickfindactivate_vector)
            self.findactivevectorcurz.Bind(wx.EVT_BUTTON,self.OnClickfindactivate_vector2)

            boxadd.Add(self.labelactvect,1,wx.EXPAND)
            boxadd.Add(self.labelactzone,1,wx.EXPAND)
            boxadd.Add(self.addzone,1,wx.EXPAND)
            boxadd.Add(self.addvector,1,wx.EXPAND)
            boxadd.Add(self.findactivevector,1,wx.EXPAND)
            boxadd.Add(self.findactivevectorcurz,1,wx.EXPAND)
            boxdelete.Add(self.deletezone,1,wx.EXPAND)
            boxdelete.Add(self.deletevector,1,wx.EXPAND)
            boxdelete.Add(boxupdown,1,wx.EXPAND)

            boxupdown.Add(boxupdownz,1,wx.EXPAND)
            boxupdown.Add(boxupdownv,1,wx.EXPAND)

            boxupdownv.Add(self.upvector,1,wx.EXPAND)
            boxupdownv.Add(self.downvector,1,wx.EXPAND)
            boxupdownz.Add(self.upzone,1,wx.EXPAND)
            boxupdownz.Add(self.downzone,1,wx.EXPAND)

            # boxdelete.Add(self.interpolate,1,wx.EXPAND)
            boxdelete.Add(self.saveimages,1,wx.EXPAND)
            boxdelete.Add(self.binfrom3,1,wx.EXPAND)
            boxdelete.Add(self.trifromall,1,wx.EXPAND)
            boxdelete.Add(self.trifromall_proj,1,wx.EXPAND)
            boxdelete.Add(self.polyfrompar,1,wx.EXPAND)

            boxleft.Add(self.treelist,1,wx.EXPAND)
            boxleft.Add(boxadd,0,wx.EXPAND)
            boxleft.Add(boxdelete,0,wx.EXPAND)

            box.Add(boxleft,1,wx.EXPAND)
            box.Add(boxright,1,wx.EXPAND)

            self.fill_structure()

            self.treelist.SetSize(200,500)
            self.SetSize(600,700)

            self.SetSizer(box)

            self.init_struct=False


    def get_xy_from_sz(self, event: wx.Event):
        """
        Add vertices and their respectives xy coordinates from s and Z entries in the xls grid:
            - NB: The coordinates of the initial point s= 0 and one other points should be explicitly given in the xls grid.
        """
        if self.wx_exists:
            if self.verify_activevec():
                return
        curv  = self.active_vector
        n_rows = self.xls.GetNumberRows()

        # Getting the 2 first XY coordinates
        X =[]
        Y = []

        z_row = 1 #Starting from the second row because the first one is the initial point

        # First row coordinates
        x1 = self.xls.GetCellValue(0,0)
        y1 = self.xls.GetCellValue(0,1)


        if x1 != '' and y1 != '':
            X.append(float(x1))
            Y.append(float(y1))

        else:
            raise Exception('Encode the coordinates of the initial point (S = 0 -->  first point)')

        # Coordinates of the second points
        while z_row < n_rows:
            if len(X) < 2 and len(Y) < 2:
                x2 = self.xls.GetCellValue(z_row,0)
                y2 = self.xls.GetCellValue(z_row,1)

                if x2 != '' and y2 != '':
                    X.append(float(x2))
                    Y.append(float(y2))

                z_row += 1

            else:
                break

        xy1 = np.array([X[0], Y[0]])
        xy2 = np.array([X[1], Y[1]])

        # Collection of sz coordinates
        row = 0

        SZ = []

        while row < n_rows:
            s = self.xls.GetCellValue(row,4)
            z = self.xls.GetCellValue(row,2)

            if z=='':
                z=0.

            if s != '':
                SZ.append((s,z))
                row += 1

            elif s=='':         #FIXME logging msg to notify the user a point is missing
                break

            else:
                raise Exception (_("Recheck your data inputs"))
                break

        sz = np.asarray(SZ,dtype='float64') # FIXME The type is required otherwise type == <U

        # Creation of vertices
        if sz.shape[1]==2 and xy1.shape==(2,) and xy2.shape==(2,):
            if not np.array_equal(xy1,xy2):
                curv.myvertices=[]
                curv.nbvertices = 0

                dx, dy = xy2[0]-xy1[0], xy2[1]-xy1[1]
                norm = np.linalg.norm([dx,dy])
                dx, dy = dx/norm, dy/norm

                for cur in sz:
                    x, y = xy1[0] + dx*cur[0], xy1[1] + dy*cur[0]
                    curv.add_vertex(wolfvertex(x, y, float(cur[1])))

        # update of the xls grid
        for k in range(curv.nbvertices ):
            self.xls.SetCellValue(k,0,str(curv.myvertices[k].x))
            self.xls.SetCellValue(k,1,str(curv.myvertices[k].y))


    def get_xy_from_sz(self, event: wx.Event):
        """
        Add vertices and their respectives xy coordinates from s and Z entries in the xls grid:
            - NB: The coordinates of the initial point s= 0 and one other points should be explicitly given in the xls grid.
        """
        if self.wx_exists:
            if self.verify_activevec():
                return
        curv  = self.active_vector
        n_rows = self.xls.GetNumberRows()

        # Getting the 2 first XY coordinates
        X =[]
        Y = []

        z_row = 1 #Starting from the second row because the first one is the initial point

        # First row coordinates
        x1 = self.xls.GetCellValue(0,0)
        y1 = self.xls.GetCellValue(0,1)


        if x1 != '' and y1 != '':
            X.append(float(x1))
            Y.append(float(y1))

        else:
            raise Exception('Encode the coordinates of the initial point (S = 0 -->  first point)')

        # Coordinates of the second points
        while z_row < n_rows:
            if len(X) < 2 and len(Y) < 2:
                x2 = self.xls.GetCellValue(z_row,0)
                y2 = self.xls.GetCellValue(z_row,1)

                if x2 != '' and y2 != '':
                    X.append(float(x2))
                    Y.append(float(y2))

                z_row += 1

            else:
                break

        xy1 = np.array([X[0], Y[0]])
        xy2 = np.array([X[1], Y[1]])

        # Collection of sz coordinates
        row = 0

        SZ = []

        while row < n_rows:
            s = self.xls.GetCellValue(row,4)
            z = self.xls.GetCellValue(row,2)

            if z=='':
                z=0.

            if s != '':
                SZ.append((s,z))
                row += 1

            elif s=='':         #FIXME logging msg to notify the user a point is missing
                break

            else:
                raise Exception (_("Recheck your data inputs"))
                break

        sz = np.asarray(SZ,dtype='float64') # FIXME The type is required otherwise type == <U

        # Creation of vertices
        if sz.shape[1]==2 and xy1.shape==(2,) and xy2.shape==(2,):
            if not np.array_equal(xy1,xy2):
                curv.myvertices=[]
                curv.nbvertices = 0

                dx, dy = xy2[0]-xy1[0], xy2[1]-xy1[1]
                norm = np.linalg.norm([dx,dy])
                dx, dy = dx/norm, dy/norm

                for cur in sz:
                    x, y = xy1[0] + dx*cur[0], xy1[1] + dy*cur[0]
                    curv.add_vertex(wolfvertex(x, y, float(cur[1])))

        # update of the xls grid
        for k in range(curv.nbvertices ):
            self.xls.SetCellValue(k,0,str(curv.myvertices[k].x))
            self.xls.SetCellValue(k,1,str(curv.myvertices[k].y))


    def fill_structure(self):
        """
        Remplissage de la structure wx
        """
        if self.wx_exists:
            if self.xls is not None:
                self.treelist.DeleteAllItems()

                root = self.treelist.GetRootItem()
                mynode=self.treelist.AppendItem(root, 'All zones', data=self)
                self.treelist.CheckItem(mynode)

                for curzone in self.myzones:
                    curzone.add2tree(self.treelist,mynode)

                self.treelist.Expand(mynode)

    def expand_tree(self, objzone=None):
        """
        Développe la structure pour un objet spécifique stocké dans la self.treelist

        L'objet peut être une 'zone' ou un 'vector' --> see more in 'fill_structure'
        """
        if self.wx_exists:
            if self.xls is not None:
                root = self.treelist.GetRootItem()

                curchild = self.treelist.GetFirstChild(root)
                curzone=self.treelist.GetItemData(curchild)

                while curchild is not None:
                    if curzone is objzone:
                        self.treelist.Expand(curchild)
                        break
                    else:
                        curchild=self.treelist.GetNextItem(curchild)
                        curzone=self.treelist.GetItemData(curchild)

    def Oncapture(self, event:wx.MouseEvent):
        """
        Ajoute de nouveaux vertices au vecteur courant
        Fonctionne par clicks souris via le GUI wx de WolfMapViewer
        """
        if self.wx_exists:
            # N'est pas à strictement parlé dépendant de wx mais n'a de sens
            # que si le mapviewer est défini --> si un GUI wx existe
            if self.verify_activevec():
                return

            self.mapviewer.start_action('capture vertices', _('Capture vertices'))
            firstvert=wolfvertex(0.,0.)
            self.active_vector.add_vertex(firstvert)
            self.active_vector.parentzone.reset_listogl()
            self.mapviewer.mimicme()

    def OnReverse(self, event:wx.MouseEvent):
        """
        Renverse le vecteur courant
        """
        if self.wx_exists:
            # N'est pas à strictement parlé dépendant de wx mais n'a de sens
            # que si le mapviewer est défini --> si un GUI wx existe
            if self.verify_activevec():
                return

            self.active_vector.reverse()
            self.fill_structure()

    def OnAddPar(self, event:wx.MouseEvent):
        """
        Ajout d'une parallèle au vecteur courant via le bouton adhoc
        """
        if self.wx_exists:
            if self.verify_activevec():
                return

            dlg = wx.TextEntryDialog(None,_('Normal distance ? \nd > 0 is right \n d < 0 is left'),value='0.0')
            ret=dlg.ShowModal()
            dist=dlg.GetValue()
            dlg.Destroy()
            try:
                dist = float(dist)
            except:
                logging.warning(_('Bad value -- Retry !'))
                return

            self.active_zone.add_parallel(dist)
            self.fill_structure()
            self.find_minmax(True)
            self.expand_tree(self.active_zone)

    def OncaptureandDynapar(self, event:wx.MouseEvent):
        """
        Ajoute des vertices au vecteur courant et crée des parallèles gauche-droite
        """
        if self.wx_exists:
            if self.verify_activevec():
                return

            self.mapviewer.start_action('dynamic parallel', _('Dynamic parallel'))

            firstvert=wolfvertex(0.,0.)
            self.active_vector.add_vertex(firstvert)
            self.mapviewer.mimicme()
            self.active_zone.reset_listogl()


    def Onsascending(self, e:wx.MouseEvent):
        """
        S'assure que les points sont ordonnés avec une distance 2D croissante

        Retourne un message avec les valeurs modifiées le cas échéant
        """
        if self.wx_exists:
            if self.verify_activevec():
                return

            correct,wherec= self.active_vector.verify_s_ascending()
            self.xls_active_vector()

            if correct:
                msg=_('Modification on indices :\n')
                for curi in wherec:
                    msg+= str(curi)+'<-->'+str(curi+1)+'\n'
                dlg=wx.MessageDialog(None,msg)
                dlg.ShowModal()
                dlg.Destroy()

    def Onmodify(self, event:wx.MouseEvent):
        """
        Permet la modification interactive de vertex dans le vector actif

        Premier click : recherche du vertex le plus proche
        Second click  : figer la nouvelle position

        --> action active jusqu'à sélectionne une autre action ou touche Entrée
        """
        if self.wx_exists:
            if self.verify_activevec():
                return

            self.mapviewer.start_action('modify vertices', _('Modify vertices'))
            self.mapviewer.mimicme()
            self.active_zone.reset_listogl()

    def Onzoom(self, event:wx.MouseEvent):
        """
        Zoom sur le vecteur actif dans le mapviewer
        """
        if self.wx_exists:
            if self.verify_activevec():
                return

            self.mapviewer.zoomon_activevector()

    def Onzoomvertex(self, event:wx.MouseEvent):
        """
        Zoom sur le vertex actif dans le mapviewer
        """
        if self.wx_exists:
            if self.verify_activevec():
                return

            self.mapviewer.zoomon_active_vertex()

    def Ongetvalues(self, e:wx.MouseEvent):
        """
        Récupère les valeurs dans une matrice

        --> soit la matrice courante
        --> soit la matrice active de l'interface parent
        """
        if self.verify_activevec():
            return

        try:
            curarray = self.parent.active_array
            if curarray is not None:
                self.active_vector.get_values_on_vertices(curarray)
                self.active_vector.fillgrid(self.xls)
            else:
                logging.info(_('Please activate the desired array'))
        except:
            raise Warning(_('Not supported in the current parent -- see PyVertexVectors in Ongetvalues function'))

    def Ongetvalueslinked(self, e:wx.MouseEvent):
        """
        Récupération des valeurs sous toutes les matrices liées pour le vecteur actif

        Crée une nouvelle zone contenant une copie du vecteur
        Le nombre de vertices est conservé
        """
        if self.parent is not None:
            if self.verify_activevec():
                return

            try:
                linked = self.parent.get_linked_arrays()

                if len(linked)>0:
                    newzone:zone
                    newzone = self.active_vector.get_values_linked(linked, False)

                    self.add_zone(newzone)
                    newzone.parent=self

                    self.fill_structure()
            except:
                raise Warning(_('Not supported in the current parent -- see PyVertexVectors in Ongetvalueslinked function'))

    def Ongetvalueslinkedandref(self, e:wx.MouseEvent):
        """
        Récupération des valeurs sous toutes les matrices liées pour le vecteur actif

        Crée une nouvelle zone contenant une copie du vecteur.

        Le nombre de vertices est adapté pour correspondre au mieux à la matrice de liée et ne pas perdre, si possible, d'information.
        """
        if self.parent is not None:
            if self.verify_activevec():
                return

            linked=self.parent.get_linked_arrays()

            if len(linked)>0:
                newzone:zone
                newzone=self.active_vector.get_values_linked(linked)

                self.add_zone(newzone)
                newzone.parent=self

                self.fill_structure()

    def Onsaveimages(self, event:wx.MouseEvent):
        """
        Enregistrement d'une image pour tous les vecteurs
        """
        self.save_images_fromvec()

    def Oncreatepolygons(self, event:wx.MouseEvent):
        """
        Création de polygones depuis des paralèles contenues dans la zone active
        """
        if self.active_zone is None:
            return

        if self.wx_exists:
            curz = self.active_zone

            if curz.nbvectors!=3:
                logging.warning(_('The active zone must contain 3 vectors and only 3'))
                return

            dlg=wx.NumberEntryDialog(None,_('What is the desired longitudinal size [cm] ?'),'ds','ds size',500,1,10000)
            ret=dlg.ShowModal()
            if ret==wx.ID_CANCEL:
                dlg.Destroy()
                return

            ds=float(dlg.GetValue())/100.
            dlg.Destroy()

            dlg=wx.NumberEntryDialog(None,_('How many polygons ? \n\n 1 = one large polygon from left to right\n 2 = two polygons - one left and one right'),'Number','Polygons',1,1,2)
            ret=dlg.ShowModal()
            if ret==wx.ID_CANCEL:
                dlg.Destroy()
                return

            nb=int(dlg.GetValue())
            dlg.Destroy()

            self.active_zone.create_polygon_from_parallel(ds,nb)

    def Oncreatebin(self,event:wx.MouseEvent):
        """
        Création d'un canal sur base de 3 parallèles
        """
        if self.wx_exists:
            if self.active_zone is None:
                return

            curz = self.active_zone

            if curz.nbvectors!=3:
                logging.warning(_('The active zone must contain 3 vectors and only 3'))

            dlg=wx.MessageDialog(None,_('Do you want to copy the center elevations to the parallel sides ?'),style=wx.YES_NO)
            ret=dlg.ShowModal()
            if ret==wx.ID_YES:
                left:LineString
                center:LineString
                right:LineString

                left = curz.myvectors[0].asshapely_ls()
                center = curz.myvectors[1].asshapely_ls()
                right = curz.myvectors[2].asshapely_ls()

                for idx,coord in enumerate(left.coords):
                    xy = Point(coord[0],coord[1])
                    curs = left.project(xy,True)
                    curz.myvectors[0].myvertices[idx].z=center.interpolate(curs,True).z

                for idx,coord in enumerate(right.coords):
                    xy = Point(coord[0],coord[1])
                    curs = right.project(xy,True)
                    curz.myvectors[2].myvertices[idx].z=center.interpolate(curs,True).z

            dlg.Destroy()

            left:LineString
            center:LineString
            right:LineString

            left = curz.myvectors[0].asshapely_ls()
            center = curz.myvectors[1].asshapely_ls()
            right = curz.myvectors[2].asshapely_ls()

            dlg=wx.NumberEntryDialog(None,_('What is the desired lateral size [cm] ?'),'ds','ds size',500,1,10000)
            ret=dlg.ShowModal()
            if ret==wx.ID_CANCEL:
                dlg.Destroy()
                return

            addedz=float(dlg.GetValue())/100.
            dlg.Destroy()

            dlg=wx.NumberEntryDialog(None,_('How many points along center polyline ?')+'\n'+
                                        _('Length size is {} meters').format(center.length),'nb','dl size',100,1,10000)
            ret=dlg.ShowModal()
            if ret==wx.ID_CANCEL:
                dlg.Destroy()
                return

            nb=int(dlg.GetValue())
            dlg.Destroy()

            s = np.linspace(0.,1.,num=nb,endpoint=True)
            points=np.zeros((5*nb,3),dtype=np.float32)

            decal=0
            for curs in s:

                ptl=left.interpolate(curs,True)
                ptc=center.interpolate(curs,True)
                ptr=right.interpolate(curs,True)

                points[0+decal,:] = np.asarray([ptl.coords[0][0],ptl.coords[0][1],ptl.coords[0][2]])
                points[1+decal,:] = np.asarray([ptl.coords[0][0],ptl.coords[0][1],ptl.coords[0][2]])
                points[2+decal,:] = np.asarray([ptc.coords[0][0],ptc.coords[0][1],ptc.coords[0][2]])
                points[3+decal,:] = np.asarray([ptr.coords[0][0],ptr.coords[0][1],ptr.coords[0][2]])
                points[4+decal,:] = np.asarray([ptr.coords[0][0],ptr.coords[0][1],ptr.coords[0][2]])

                points[0+decal,2] += addedz
                points[4+decal,2] += addedz

                decal+=5

            decal=0
            triangles=[]

            nbpts=5
            triangles.append([[i+decal,i+decal+1,i+decal+nbpts] for i in range(nbpts-1)])
            triangles.append([[i+decal+nbpts,i+decal+1,i+decal+nbpts+1] for i in range(nbpts-1)])

            for k in range(1,nb-1):
                decal=k*nbpts
                triangles.append([ [i+decal,i+decal+1,i+decal+nbpts] for i in range(nbpts-1)])
                triangles.append([ [i+decal+nbpts,i+decal+1,i+decal+nbpts+1] for i in range(nbpts-1)])
            triangles=np.asarray(triangles,dtype=np.uint32).reshape([(2*nbpts-2)*(nb-1),3])

            mytri=Triangulation(pts=points,tri=triangles)
            mytri.find_minmax(True)
            fn=mytri.export_to_gltf()

            dlg=wx.MessageDialog(None,_('Do you want to add triangulation to parent gui ?'),style=wx.YES_NO)
            ret=dlg.ShowModal()
            if ret==wx.ID_YES:

                self.mapviwer.add_object('triangulation',newobj=mytri)

            dlg.Destroy()

    def Oncreatemultibin(self, event:wx.MouseEvent):
        """
        Création d'une triangulation sur base de plusieurs vecteurs
        """
        if self.wx_exists:
            if self.active_zone is None:
                return

            myzone = self.active_zone

            if myzone.nbvectors<2:

                dlg = wx.MessageDialog(None,_('Not enough vectors/polylines in the active zone -- Add element and retry !!'))
                ret = dlg.ShowModal()
                dlg.Destroy()
                return

            mytri = myzone.createmultibin()
            self.mapviewer.add_object('triangulation',newobj=mytri)

    def Oncreatemultibin_project(self, event:wx.MouseEvent):
        """
        Création d'une triangulation sur base de plusieurs vecteurs
        Les sommets sont recherchés par projection d'un vecteur sur l'autre
        """
        if self.wx_exists:
            if self.active_zone is None:
                return

            myzone = self.active_zone

            if myzone.nbvectors<2:

                dlg = wx.MessageDialog(None,_('Not enough vectors/polylines in the active zone -- Add element and retry !!'))
                ret = dlg.ShowModal()
                dlg.Destroy()
                return

            mytri = myzone.createmultibin_proj()
            self.mapviewer.add_object('triangulation',newobj=mytri)

    def save_images_fromvec(self, dir=''):
        """
        Sauvegarde d'images des vecteurs dans un répertoire

        FIXME : pas encore vraiment au point
        """
        if dir=='':
            if self.wx_exists:
                dlg = wx.DirDialog(None,"Choose directory to store images",style=wx.FD_SAVE)
                ret=dlg.ShowModal()

                if ret==wx.ID_CANCEL:
                    dlg.Destroy()
                    return

                dir = dlg.GetPath()
                dlg.Destroy()

        if dir=='':
            return

        for curzone in self.myzones:
            for curvec in curzone.myvectors:
                if curvec.nbvertices>1:
                    oldwidth=curvec.myprop.width
                    curvec.myprop.width=4
                    myname = curvec.myname

                    self.Activate_vector(curvec)

                    if self.mapviewer is not None:
                        if self.mapviewer.linked:
                            for curview in self.mapviewer.linkedList:
                                title = curview.GetTitle()
                                curview.zoomon_activevector()
                                fn = path.join(dir,title + '_' + myname+'.png')
                                curview.save_canvasogl(fn)
                        else:
                            self.mapviewer.zoomon_activevector()
                            fn = path.join(dir,myname+'.png')
                            self.mapviewer.save_canvasogl(fn)

                            fn = path.join(dir,'palette_v_' + myname+'.png')
                            self.mapviewer.active_array.mypal.export_image(fn,'v')
                            fn = path.join(dir,'palette_h_' + myname+'.png')
                            self.mapviewer.active_array.mypal.export_image(fn,'h')

                    curvec.myprop.width = oldwidth

    def Oninsert(self, event:wx.MouseEvent):
        """
        Insertion de vertex dans le vecteur courant
        """
        if self.wx_exists:
            if self.verify_activevec():
                return

            self.mapviewer.start_action('insert vertices', _('Insert vertices'))
            self.mapviewer.mimicme()

            self.active_zone.reset_listogl()

    def Onsplit(self, event:wx.MouseEvent):
        """
        Split le vecteur courant selon un pas spatial déterminé
        """
        if self.wx_exists:
            if self.verify_activevec():
                return

        dlg=wx.NumberEntryDialog(None,_('What is the desired longitudinal size [cm] ?'),'ds','ds size',100,1,100000)
        ret=dlg.ShowModal()
        if ret==wx.ID_CANCEL:
            dlg.Destroy()
            return

        ds=float(dlg.GetValue())/100.
        dlg.Destroy()

        self.active_vector.split(ds)

    def Onevaluates(self, event:wx.MouseEvent):
        """
        Calcule la position curviligne du vecteur courant

        Le calcul peut être mené en 2D ou en 3D
        Remplissage du tableur dans la 5ème colonne
        """
        if self.wx_exists:
            if self.verify_activevec():
                return

        curv = self.active_vector
        curv.update_lengths()

        dlg = wx.SingleChoiceDialog(None, "Which mode?", "How to evaluate lengths?", ['2D','3D'])
        ret=dlg.ShowModal()

        if ret==wx.ID_CANCEL:
            dlg.Destroy()
            return

        method=dlg.GetStringSelection()
        dlg.Destroy()

        self.xls.SetCellValue(0,4,'0.0')
        s=0.
        if method=='2D':
            for k in range(curv.nbvertices-1):
                s+=curv._lengthparts2D[k]
                self.xls.SetCellValue(k+1,4,str(s))
        else:
            for k in range(curv.nbvertices-1):
                s+=curv._lengthparts3D[k]
                self.xls.SetCellValue(k+1,4,str(s))

    def evaluate_s (self, vec: vector =None, dialog_box = True):
        """
        Calcule la position curviligne du vecteur encodé

        Le calcul peut être mené en 2D ou en 3D
        Remplissage du tableur dans la 5ème colonne
        """

        curv = vec
        curv.update_lengths()

        if dialog_box:
            dlg = wx.SingleChoiceDialog(None, "Which mode?", "How to evaluate lengths?", ['2D','3D'])
            ret=dlg.ShowModal()
            if ret==wx.ID_CANCEL:
                dlg.Destroy()
                return

            method=dlg.GetStringSelection()
            dlg.Destroy()
        else:
            method = '2D'

        self.xls.SetCellValue(0,4,'0.0')
        s=0.
        if curv.nbvertices > 0:
            if method=='2D':
                for k in range(curv.nbvertices-1):
                    s+=curv._lengthparts2D[k]
                    self.xls.SetCellValue(k+1,4,str(s))
            else:
                for k in range(curv.nbvertices-1):
                    s+=curv._lengthparts3D[k]
                    self.xls.SetCellValue(k+1,4,str(s))

    def Oninterpvec(self, event:wx.MouseEvent):
        """
        Interpole les valeurs Z de l'éditeur sur base des seules valeurs connues,
        càd autre que vide ou -99999
        """
        if self.verify_activevec():
            return

        curv = self.active_vector

        s=[]
        z=[]

        for k in range(curv.nbvertices):
            zgrid = self.xls.GetCellValue(k,2)
            sgrid = self.xls.GetCellValue(k,4)
            if zgrid!='' and float(zgrid)!=-99999.:
                z.append(float(zgrid))
                s.append(float(sgrid))

        if len(z)==0:
            return

        f = interp1d(s,z)

        for k in range(curv.nbvertices):
            zgrid = self.xls.GetCellValue(k,2)
            sgrid = self.xls.GetCellValue(k,4)
            if zgrid=='' or float(zgrid)==-99999.:
                z = f(float(sgrid))
                self.xls.SetCellValue(k,2,str(z))

    def Onupdatevertices(self,event):
        """
        Mie à jour des vertices sur base du tableur
        """
        if self.verify_activevec():
            return

        self.active_vector.updatefromgrid(self.xls)
        self.find_minmax(True)

    def Onaddrows(self, event:wx.MouseEvent):
        """
        Ajout de lignes au tableur
        """
        if self.wx_exists:
            nbrows=None
            dlg=wx.TextEntryDialog(None,_('How many rows?'),value='1')
            while nbrows is None:
                rc = dlg.ShowModal()
                if rc == wx.ID_OK:
                    nbrows = int(dlg.GetValue())
                    self.xls.AppendRows(nbrows)
                else:
                    return

    def OnClickadd_zone(self, event:wx.MouseEvent):
        """
        Ajout d'une zone au GUI
        """
        if self.wx_exists:
            curname=None
            dlg=wx.TextEntryDialog(None,_('Choose a name for the new zone'),value='New_Zone')
            while curname is None:
                rc = dlg.ShowModal()
                if rc == wx.ID_OK:
                    curname = str(dlg.GetValue())
                    newzone = zone(name=curname,parent=self)
                    self.add_zone(newzone)
                    self.fill_structure()
                    self.active_zone = newzone
                else:
                    return

    def OnClickadd_vector(self, event:wx.MouseEvent):
        """
        Ajout d'un vecteur à la zone courante
        """
        if self.wx_exists:
            curname=None
            dlg=wx.TextEntryDialog(None,_('Choose a name for the new vector'),value='New_Vector')
            while curname is None:
                rc = dlg.ShowModal()
                if rc == wx.ID_OK:
                    curname = str(dlg.GetValue())
                    newvec = vector(name=curname,parentzone=self.active_zone)
                    self.active_zone.add_vector(newvec)
                    self.fill_structure()
                    self.Activate_vector(newvec)
                else:
                    return

    def OnClickdelete_zone(self, event:wx.MouseEvent):
        """
        Suppression de la zone courante
        """
        if self.wx_exists:
            curname=self.active_zone.myname
            r = wx.MessageDialog(
                None,
                _('The zone {n} will be deleted. Continue?').format(n=curname),
                style=wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION
                ).ShowModal()

            if r != wx.ID_YES:
                return

            self.active_zone.reset_listogl()
            self.myzones.pop(int(self.myzones.index(self.active_zone)))
            self.fill_structure()
            self.find_minmax(True)

    def OnClickfindactivate_vector(self, event:wx.MouseEvent):
        """
        Recherche et activation d'un vecteur dans toutes les zones
        """
        if self.wx_exists:

            dlg=wx.MessageDialog(None,"Search only closed polyline?",style=wx.YES_NO)
            ret=dlg.ShowModal()
            dlg.Destroy()

            if ret==wx.YES:
                self.mapviewer.start_action('select active vector inside', _('Select active vector inside'))
            else:
                self.mapviewer.start_action('select active vector all', _('Select active vector all'))

            self.mapviewer.active_zones=self

    def OnClickfindactivate_vector2(self, event:wx.MouseEvent):
        """
        Recherche et activation d'un vecteur dans la zone courante
        """
        if self.wx_exists:

            dlg=wx.MessageDialog(None,"Search only closed polyline?",style=wx.YES_NO)
            ret=dlg.ShowModal()
            dlg.Destroy()

            if ret==wx.YES:
                self.mapviewer.start_action('select active vector2 inside', _('Select active vector2 inside'))
            else:
                self.mapviewer.start_action('select active vector2 all', _('Select active vector2 all'))

            self.mapviewer.active_zone=self.active_zone
            self.mapviewer.active_zones=self

    def get_selected_vectors(self, all=False):
        """
        all = True  : Récupération et renvoi des vecteurs sélectionnés dans les zones
        all = False : Récupération et renvoi du vecteur le plus proche
        """
        if all:
            mylist=[]
            for curzone in self.myzones:
                ret = curzone.get_selected_vectors(all)
                if ret is not None:
                    mylist.append(ret)
            return mylist
        else:
            distmin=99999.
            vecmin:vector = None
            for curzone in self.myzones:
                ret = curzone.get_selected_vectors()
                if ret is not None:
                    if (ret[1]<distmin) or (vecmin is None):
                        distmin= ret[1]
                        vecmin = ret[0]

            return vecmin

    def verify_activevec(self):
        """
        Vérifie si un vecteur actif est défini, si 'None' affiche un message

        Return :
           True if self.active_vector is None
           False otherwise
        """
        if self.active_vector is None:
            if self.wx_exists:
                msg=''
                msg+=_('Active vector is None\n')
                msg+=_('\n')
                msg+=_('Retry !\n')
                wx.MessageBox(msg)
            return True
        return False

    def OnClickdelete_vector(self, event:wx.MouseEvent):
        """
        Suppression du vecteur actif
        """
        if self.wx_exists:
            if self.verify_activevec():
                return

            curname=self.active_vector.myname
            r = wx.MessageDialog(
                None,
                _('The vector {n} will be deleted. Continue?').format(n=curname),
                style=wx.YES_NO | wx.ICON_QUESTION
            ).ShowModal()

            if r != wx.ID_YES:
                return

            actzone =self.active_zone
            actzone.myvectors.pop(int(actzone.myvectors.index(self.active_vector)))
            self.fill_structure()
            self.find_minmax(True)

    def OnClickup_vector(self, event:wx.MouseEvent):
        """Remonte le vecteur actif dans la liste de la zone"""
        if self.verify_activevec():
            return

        for idx,curv in enumerate(self.active_zone.myvectors):

            if curv == self.active_vector:
                if idx==0:
                    return
                self.active_zone.myvectors.pop(idx)
                self.active_zone.myvectors.insert(idx-1,curv)

                self.fill_structure()

                break

    def OnClickdown_vector(self, event:wx.MouseEvent):
        """Descend le vecteur actif dans la liste de la zone"""
        if self.verify_activevec():
            return

        for idx,curv in enumerate(self.active_zone.myvectors):

            if curv == self.active_vector:
                if idx==self.active_zone.nbvectors:
                    return
                self.active_zone.myvectors.pop(idx)
                self.active_zone.myvectors.insert(idx+1,curv)

                self.fill_structure()

                break

    def OnClickup_zone(self, event:wx.MouseEvent):
        """Remonte la zone active dans la liste de la zones self"""

        for idx,curz in enumerate(self.myzones):

            if curz == self.active_zone:
                if idx==0:
                    return
                self.myzones.pop(idx)
                self.myzones.insert(idx-1,curz)

                self.fill_structure()

                break

    def OnClickdown_zone(self, event:wx.MouseEvent):
        """Descend la zone active dans la liste de la zones self"""
        for idx,curz in enumerate(self.myzones):

            if curz == self.active_zone:
                if idx==self.nbzones:
                    return
                self.myzones.pop(idx)
                self.myzones.insert(idx+1,curz)

                self.fill_structure()

                break

    def unuse(self):
        """
        Rend inutilisé l'ensemble des zones
        """
        for curzone in self.myzones:
            curzone.unuse()

    def use(self):
        """
        Rend utilisé l'ensemble des zones
        """
        for curzone in self.myzones:
            curzone.use()

    def OnCheckItem(self, event:wx.MouseEvent):
        """
        Coche/Décoche un ékement de la treelist
        """
        if self.wx_exists:
            myitem=event.GetItem()
            check = self.treelist.GetCheckedState(myitem)
            myitemdata=self.treelist.GetItemData(myitem)
            if check:
                myitemdata.use()
            else:
                myitemdata.unuse()

    def OnRDown(self, event:TreeListEvent):
        """
        Affiche les propriétés du vecteur courant
        Clicl-droit
        """
        if self.wx_exists:
            if self.verify_activevec():
                return
            self.active_vector.myprop.show()

    def OnActivateItem(self, event:TreeListEvent):
        """
        Activation d'un élément dans le treelist
        """
        if self.wx_exists:
            myitem=event.GetItem()
            myitemdata=self.treelist.GetItemData(myitem)

            if isinstance(myitemdata,vector):
                self.Activate_vector(myitemdata)
            elif isinstance(myitemdata,zone):
                self.Activate_zone(myitemdata)

            self.last_active = myitemdata

    def Activate_vector(self, object:vector):
        """
        Mémorise l'objet passé en argument comme vecteur actif

        Pousse la même information dans l'objet parent s'il existe
        """
        if self.wx_exists:
            self.active_vector = object
            self.xls_active_vector()

            if object.parentzone is not None:
                self.active_zone = object.parentzone
                object.parentzone.active_vector = object

            if self.parent is not None:
                try:
                    self.parent.Active_vector(self.active_vector)
                except:
                    raise Warning(_('Not supported in the current parent -- see PyVertexVectors in Activate_vector function'))

            if self.xls is not None:
                self.labelactvect.SetLabel(self.active_vector.myname)
                self.labelactzone.SetLabel(self.active_zone.myname)
                self.Layout()

    def Activate_zone(self, object:zone):
        """
        Mémorise l'objet passé en argument comme zone active

        Pousse la même information dans l'objet parent s'il existe
        """
        if self.wx_exists:
            self.active_zone = object
            if object.active_vector is not None:
                self.active_vector = object.active_vector
            elif object.nbvectors>0:
                self.Activate_vector(object.myvectors[0])

            self.labelactvect.SetLabel(self.active_vector.myname)
            self.labelactzone.SetLabel(self.active_zone.myname)
            self.Layout()

    def xls_active_vector(self):
        """
        Remplit le tableur
        """
        if self.wx_exists:
            if self.xls is not None:
                self.xls.ClearGrid()
                self.active_vector.fillgrid(self.xls)

    def OnEditLabel(self, event:wx.MouseEvent):
        """
        Edition de la clé/label de l'élément actif du treelist
        """
        if self.wx_exists:

            key=event.GetKeyCode()

            if key==wx.WXK_F2:
                if self.last_active is not None:
                    curname=None
                    dlg=wx.TextEntryDialog(None,_('Choose a new name'), value=self.last_active.myname)
                    while curname is None:
                        rc = dlg.ShowModal()
                        if rc == wx.ID_OK:
                            curname = str(dlg.GetValue())
                            dlg.Destroy()
                            self.last_active.myname = curname
                            self.fill_structure()
                        else:
                            dlg.Destroy()
                            return

    def deepcopy_zones(self, name:str = None):
        """
        Return the deep copy of the current
        Zones (a new object).
        """
        copied_Zones = Zones()
        for zne in self.myzones:
            new_zne = zne.deepcopy_zone(parent= copied_Zones)
            copied_Zones.add_zone(new_zne,forceparent=True)
        copied_Zones.find_minmax(True)
        return copied_Zones

class Grid(Zones):
    """
    Grid to draw on the mapviewer.

    Contains one zone and 3 vectors (gridx, gridy, contour).

    Each gridx and gridy vector contains vertices forming a continuous line.
    Contour vector contains 4 vertices forming a closed polyline.

    Drawing all the elements on the mapviewer allows to draw a grid.

    Based on spatial extent and resolution.
    """

    def __init__(self,
                 size:float=1000.,
                 ox:float=0.,
                 oy:float=0.,
                 ex:float=1000.,
                 ey:float=1000.,
                 parent=None):

        super().__init__(ox=ox, oy=oy, parent=parent)

        mygrid=zone(name='grid',parent=self)
        self.add_zone(mygrid)

        gridx=vector(name='gridx')
        gridy=vector(name='gridy')
        contour=vector(name='contour')

        mygrid.add_vector(gridx)
        mygrid.add_vector(gridy)
        mygrid.add_vector(contour)

        self.creategrid(size,ox,oy,ex,ey)

    def creategrid(self,
                   size:float=100.,
                   ox:float=0.,
                   oy:float=0.,
                   ex:float=1000.,
                   ey:float=1000.):

        mygridx=self.myzones[0].myvectors[0]
        mygridy=self.myzones[0].myvectors[1]
        contour=self.myzones[0].myvectors[2]
        mygridx.reset()
        mygridy.reset()
        contour.reset()

        locox=int(ox/size)*size
        locoy=int(oy/size)*size
        locex=(np.ceil(ex/size))*size
        locey=(np.ceil(ey/size))*size

        nbx=int(np.ceil((locex-locox)/size))
        nby=int(np.ceil((locey-locoy)/size))

        dx=locex-locox
        dy=locey-locoy

        #grillage vertical
        xloc=locox
        yloc=locoy
        for i in range(nbx):
            newvert=wolfvertex(xloc,yloc)
            mygridx.add_vertex(newvert)

            yloc+=dy
            newvert=wolfvertex(xloc,yloc)
            mygridx.add_vertex(newvert)

            xloc+=size
            dy=-dy

        #grillage horizontal
        xloc=locox
        yloc=locoy
        for i in range(nby):
            newvert=wolfvertex(xloc,yloc)
            mygridy.add_vertex(newvert)

            xloc+=dx
            newvert=wolfvertex(xloc,yloc)
            mygridy.add_vertex(newvert)

            yloc+=size
            dx=-dx

        newvert=wolfvertex(locox,locoy)
        contour.add_vertex(newvert)
        newvert=wolfvertex(locex,locoy)
        contour.add_vertex(newvert)
        newvert=wolfvertex(locex,locey)
        contour.add_vertex(newvert)
        newvert=wolfvertex(locox,locey)
        contour.add_vertex(newvert)

        self.find_minmax(True)
