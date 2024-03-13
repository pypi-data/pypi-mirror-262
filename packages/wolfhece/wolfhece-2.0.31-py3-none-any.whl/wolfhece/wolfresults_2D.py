import sys
import wx
from os.path import dirname, exists, join, splitext
from math import floor

import numpy.ma as ma
import numpy as np
import matplotlib.path as mpltPath
import matplotlib.pyplot as plt
from enum import Enum
from typing import Literal, Union
import logging
from tqdm import tqdm
from datetime import datetime as dt, timedelta

try:
    from OpenGL.GL import *
except:
    msg=_('Error importing OpenGL library')
    msg+=_('   Python version : ' + sys.version)
    msg+=_('   Please check your version of opengl32.dll -- conflict may exist between different files present on your desktop')
    raise Exception(msg)

from .drawing_obj import Element_To_Draw
from .PyPalette import wolfpalette
from .PyTranslate import _
from .gpuview import GRID_N, Rectangle, VectorField
from .pyshields import get_d_cr, get_d_cr_susp, izbach_d_cr, get_Shields_2D_Manning
from .pyviews import WolfViews
from .mesh2d.wolf2dprev import prev_parameters_simul, bloc_file
from .GraphNotebook import PlotPanel
from .CpGrid import CpGrid


try:
    from .libs import wolfpy
except Exception as ex:
    # This convoluted error handling is here to catch an issue
    # which was difficult to track down: wolfpy was there
    # but its DLL were not available.

    from importlib.util import find_spec
    s = find_spec('wolfhece.libs.wolfpy')
    from pathlib import Path

    # Not too sure about this find_spec. If the root
    # directory is not the good one, the import search may
    # end up in the site packages, loading the wrong wolfpy.

    base = Path(__file__).parent.parts
    package = Path(s.origin).parent.parts
    is_submodule = (len(base) <= len(package)) and all(i==j for i, j in zip(base, package))

    if is_submodule:
        msg = _("wolfpy was found but we were not able to load it. It may be an issue with its DLL dependencies")
        msg += _("The actual error was: {}").format(str(ex))
    else:
        msg=_('Error importing wolfpy.pyd')
        msg+=_('   Python version : ' + sys.version)
        msg+=_('   If your Python version is not 3.7.x or 3.9.x, you need to compile an adapted library with compile_wcython.py in wolfhece library path')
        msg+=_('   See comments in compile_wcython.py or launch *python compile_wcython.py build_ext --inplace* in :')
        msg+='      ' + dirname(__file__)

    raise Exception(msg)

from .wolf_array import WolfArray, getkeyblock, header_wolf, WolfArrayMB, WolfArrayMNAP, header_wolf, SelectionData
from .mesh2d import wolf2dprev
from .PyVertexvectors import vector, zone, Zones


def outside_domain(val):
    """ Test if a value is outside the calculated domain """
    return val[0][0] is np.ma.masked or val[1][0] =='-'

def q_splitting(q_left, q_right):
    """ Splitting of the normal flow between two nodes """
    prod_q = q_left * q_right
    sum_q = q_left + q_right
    if prod_q > 0.:
        if q_left > 0.:
            return q_left
        else:
            return q_right
    elif prod_q < 0.:
        if sum_q > 0.:
            return q_left
        elif sum_q < 0.:
            return q_right
        else:
            return 0.
    else:
        if q_left<0.:
            return 0.
        elif q_right<0.:
            return 0.
        else:
            return sum_q / 2.

def u_splitting(q_left, q_right, h_left, h_right):
    """ Splitting of the normal flow velocity between two nodes """
    prod_q = q_left * q_right
    sum_q = q_left + q_right
    if prod_q > 0.:
        if q_left > 0.:
            return q_left/h_left
        else:
            return q_right/h_right
    elif prod_q < 0.:
        if sum_q > 0.:
            return q_left/h_left
        elif sum_q < 0.:
            return q_right/h_right
        else:
            return 0.
    else:
        if q_left<0.:
            return 0.
        elif q_right<0.:
            return 0.
        else:
            return (q_left/h_left + q_right/h_right) / 2.


class Props_Res_2D(wx.Frame):
    """
    Fenêtre de propriétésd'un Wolfresults_2D
    """

    def __init__(self, parent:"Wolfresults_2D", mapviewer=None):

        self._parent:Wolfresults_2D
        self._parent = parent

        from .PyDraw import WolfMapViewer
        self._mapviewer:WolfMapViewer
        self._mapviewer = mapviewer

        self.wx_exists = wx.App.Get() is not None

        self.active_vector:vector = None
        self.active_zone:zone = None
        self.active_array:WolfArray = self._parent

        self.myzones = Zones(parent=self)
        self.myzonetmp = zone(name='tmp')
        self.vectmp = vector(name='tmp')
        self.fnsave = ''

        self.myzonetmp.add_vector(self.vectmp)
        self.myzones.add_zone(self.myzonetmp)

        if self.wx_exists:
            self.set_GUI()

    def get_mapviewer(self):
        """ Retourne une instance WolfMapViewer """
        return self._mapviewer

    def get_linked_arrays(self):
        """ Pour compatibilité avec la gestion de vecteur et WolfMapViewer """
        return {self._parent.idx: self._parent}

    def set_GUI(self):
        """Set the wx GUI"""

        super(Props_Res_2D, self).__init__(None, title=_('Properties'), size=(600, 700),
                                        style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        # GUI
        self.Bind(wx.EVT_CLOSE, self.onclose)
        self.Bind(wx.EVT_SHOW, self.onshow)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        # GUI Notebook
        self._notebook = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize)

        #  panel Selection
        # self.selection = wx.Panel(self._notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        # self._notebook.AddPage(self.selection, _("Selection"), True)

        #  panel Operations
        # self.operation = wx.Panel(self._notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        # self._notebook.AddPage(self.operation, _("Operators"), False)

        #  panel Mask
        # self.mask = wx.Panel(self._notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        # self._notebook.AddPage(self.mask, _("Mask"), False)

        #  panel Interpolation
        # self.Interpolation = wx.Panel(self._notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        # self._notebook.AddPage(self.Interpolation, _("Interpolation"), False)

        # panel Tools/Misc
        self._panel_colormap = PlotPanel(self._notebook, wx.ID_ANY, toolbar=False)
        self._notebook.AddPage(self._panel_colormap, _("Palette"), False)

        self._tools = wx.Panel(self._notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self._notebook.AddPage(self._tools, _("Miscellaneous"), False)

        #  panel PALETTE de couleurs
        self._cm_grid = CpGrid(self._panel_colormap, wx.ID_ANY, style=wx.WANTS_CHARS | wx.TE_CENTER)
        self._cm_apply = wx.Button(self._panel_colormap, wx.ID_ANY, _("Apply"), wx.DefaultPosition, wx.DefaultSize, 0)
        self._cm_apply.SetToolTip(_('Apply changes in memory'))
        self._cm_grid.CreateGrid(16, 4)

        self._cm_auto = wx.CheckBox(self._panel_colormap, wx.ID_ANY, _("Automatic"), wx.DefaultPosition, wx.DefaultSize,
                                   style=wx.CHK_CHECKED)
        self._cm_auto.SetToolTip(_('Activating/Deactivating automatic colormap values distribution'))

        self._cm_uniform_or_lerp = wx.CheckBox(self._panel_colormap, wx.ID_ANY, _("Uniform in parts"), wx.DefaultPosition, wx.DefaultSize,
                                   style=wx.CHK_UNCHECKED)
        self._cm_uniform_or_lerp.SetToolTip(_('Activating/Deactivating linear interpolation'))

        self._cm_alpha = wx.CheckBox(self._panel_colormap, wx.ID_ANY, _("Opacity"), wx.DefaultPosition, wx.DefaultSize,
                                    style=wx.CHK_CHECKED)
        self._cm_alpha.SetToolTip(_('Activating/Deactivating transparency of the array'))
        self._cm_hillshade = wx.CheckBox(self._panel_colormap, wx.ID_ANY, _("Hillshade"), wx.DefaultPosition, wx.DefaultSize,
                                     style=wx.CHK_CHECKED)
        self._cm_hillshade.SetToolTip(_('Activating/Deactivating hillshade on colors and create if necessary a gray map'))

        self._cm_slider_alpha = wx.Slider(self._panel_colormap, wx.ID_ANY, 100, 0, 100, wx.DefaultPosition, wx.DefaultSize,
                                        wx.SL_HORIZONTAL, name='palslider')
        self._cm_slider_alpha.SetToolTip(_('Global opacity (transparent --> opaque)'))

        self._cm_slider_hillshade = wx.Slider(self._panel_colormap, wx.ID_ANY, 100, 0, 100, wx.DefaultPosition, wx.DefaultSize,
                                           wx.SL_HORIZONTAL, name='palalphaslider')
        self._cm_slider_hillshade.SetToolTip(_('Hillshade transparency (transparent-->opaque)'))

        self._cm_slider_azimuth = wx.Slider(self._panel_colormap, wx.ID_ANY, 315, 0, 360, wx.DefaultPosition, wx.DefaultSize,
                                             wx.SL_HORIZONTAL, name='palazimuthslider')
        self._cm_slider_azimuth.SetToolTip(_('Hillshade azimuth (0-->360)'))

        self._cm_slider_altitude = wx.Slider(self._panel_colormap, wx.ID_ANY, 0, 0, 90, wx.DefaultPosition, wx.DefaultSize,
                                              wx.SL_HORIZONTAL, name='palaltitudeslider')
        self._cm_slider_altitude.SetToolTip(_('Hillshade altitude (0-->90)'))

        self._cm_save = wx.Button(self._panel_colormap, wx.ID_ANY, _("Save to file"), wx.DefaultPosition, wx.DefaultSize, 0)
        self._cm_save.SetToolTip(_('Save colormap on .pal file'))
        self._cm_load = wx.Button(self._panel_colormap, wx.ID_ANY, _("Load from file"), wx.DefaultPosition, wx.DefaultSize, 0)
        self._cm_load.SetToolTip(_('Load colormap from .pal file'))
        self._cm_toimage = wx.Button(self._panel_colormap, wx.ID_ANY, _("Create image"), wx.DefaultPosition, wx.DefaultSize, 0)
        self._cm_toimage.SetToolTip(_('Generate colormap image (horizontal, vertical or both) and save to disk'))
        self._cm_distribute = wx.Button(self._panel_colormap, wx.ID_ANY, _("Distribute"), wx.DefaultPosition, wx.DefaultSize, 0)
        self._cm_distribute.SetToolTip(_('Set colormap values based on minimum+maximum or minimum+step'))

        if self._parent.mypal.automatic:
            self._cm_auto.SetValue(1)
        else:
            self._cm_auto.SetValue(0)

        if self._parent.mypal.interval_cst:
            self._cm_uniform_or_lerp.SetValue(1)
        else:
            self._cm_uniform_or_lerp.SetValue(0)

        self._cm_alpha.SetValue(1)

        self._cm_choose_color = wx.Button(self._panel_colormap, wx.ID_ANY, _("Choose color for current value"),
                                        wx.DefaultPosition, wx.DefaultSize)
        self._cm_choose_color.SetToolTip(_('Color dialog box for the current selected value in the grid'))

        # Sizer Colormap
        # --------------
        self._panel_colormap.sizerfig.Add(self._cm_grid, 1, wx.EXPAND)

        self._panel_colormap.sizer.Add(self._cm_auto, 1, wx.EXPAND)
        self._panel_colormap.sizer.Add(self._cm_uniform_or_lerp, 1, wx.EXPAND)
        self._panel_colormap.sizer.Add(self._cm_alpha, 1, wx.EXPAND)
        self._panel_colormap.sizer.Add(self._cm_slider_alpha, 1, wx.EXPAND)
        # self._panel_colormap.sizer.Add(self._cm_hillshade, 1, wx.EXPAND)

        # self._panel_colormap.sizer.Add(self._cm_slider_hillshade, 1, wx.EXPAND)
        # self._panel_colormap.sizer.Add(self._cm_slider_azimuth, 1, wx.EXPAND)
        # self._panel_colormap.sizer.Add(self._cm_slider_altitude, 1, wx.EXPAND)

        self._panel_colormap.sizer.Add(self._cm_choose_color, 1, wx.EXPAND)
        self._panel_colormap.sizer.Add(self._cm_apply, 1, wx.EXPAND)
        self._panel_colormap.sizer.Add(self._cm_load, 1, wx.EXPAND)
        self._panel_colormap.sizer.Add(self._cm_save, 1, wx.EXPAND)
        self._panel_colormap.sizer.Add(self._cm_toimage, 1, wx.EXPAND)
        self._panel_colormap.sizer.Add(self._cm_distribute, 1 , wx.EXPAND)

        # HISTOGRAMMES
        self._panel_histo = PlotPanel(self._notebook, wx.ID_ANY, toolbar=True)
        self._histo_update = wx.Button(self._panel_histo, wx.ID_ANY, _("All data..."), wx.DefaultPosition, wx.DefaultSize, 0)
        self._histo_updatezoom = wx.Button(self._panel_histo, wx.ID_ANY, _("On zoom..."), wx.DefaultPosition, wx.DefaultSize, 0)
        self._histo_updateerase = wx.Button(self._panel_histo, wx.ID_ANY, _("Erase"), wx.DefaultPosition, wx.DefaultSize, 0)

        # Sizer Histogram
        # ---------------
        self._panel_histo.sizer.Add(self._histo_update, 0, wx.EXPAND)
        self._panel_histo.sizer.Add(self._histo_updatezoom, 0, wx.EXPAND)
        self._panel_histo.sizer.Add(self._histo_updateerase, 0, wx.EXPAND)

        self._notebook.AddPage(self._panel_histo, _("Histogram"), False)

        # # LINKS
        # self.links = wx.Panel(self._notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        # self._notebook.AddPage(self.links, _("Links"), False)

        # # Interpolation
        # gSizer1 = wx.GridSizer(0, 2, 0, 0)

        # self.interp2D = wx.Button(self.Interpolation, wx.ID_ANY, _("2D Interpolation on selection"), wx.DefaultPosition,
        #                           wx.DefaultSize, 0)
        # self.interp2D.SetToolTip(_('Spatial interpolation based on nodes stored in named groups. \n The interpolation apply only on the current selection.'))
        # gSizer1.Add(self.interp2D, 0, wx.EXPAND)
        # self.interp2D.Bind(wx.EVT_BUTTON, self.interpolation2D)

        # self.m_button7 = wx.Button(self.Interpolation, wx.ID_ANY, _("Stage/Volume/Surface evaluation"), wx.DefaultPosition,
        #                            wx.DefaultSize, 0)
        # self.m_button7.SetToolTip(_('Evaluate stage-volume-surface relationship. \n Results : plots and arrays saved on disk'))

        # gSizer1.Add(self.m_button7, 0, wx.EXPAND)
        # self.m_button7.Bind(wx.EVT_BUTTON, self.volumesurface)

        # self.m_button8 = wx.Button(self.Interpolation, wx.ID_ANY, _("Interpolation on active zone \n polygons"),
        #                            wx.DefaultPosition, wx.DefaultSize, 0)
        # self.m_button8.SetToolTip(_('Spatial interpolation based on all polygons in active zone'))

        # gSizer1.Add(self.m_button8, 0, wx.EXPAND)
        # self.m_button8.Bind(wx.EVT_BUTTON, self.interp2Dpolygons)

        # self.m_button9 = wx.Button(self.Interpolation, wx.ID_ANY, _("Interpolation on active zone \n 3D polylines"),
        #                            wx.DefaultPosition, wx.DefaultSize, 0)
        # self.m_button9.SetToolTip(_('Spatial interpolation based on all polylines in active zone'))

        # gSizer1.Add(self.m_button9, 0, wx.EXPAND)
        # self.m_button9.Bind(wx.EVT_BUTTON, self.interp2Dpolylines)

        # self.m_button10 = wx.Button(self.Interpolation, wx.ID_ANY, _("Interpolation on active vector \n polygon"),
        #                             wx.DefaultPosition, wx.DefaultSize, 0)
        # self.m_button10.SetToolTip(_('Spatial interpolation based on active polygon'))

        # gSizer1.Add(self.m_button10, 0, wx.EXPAND)
        # self.m_button10.Bind(wx.EVT_BUTTON, self.interp2Dpolygon)

        # self.m_button11 = wx.Button(self.Interpolation, wx.ID_ANY, _("Interpolation on active vector \n 3D polyline"),
        #                             wx.DefaultPosition, wx.DefaultSize, 0)
        # self.m_button11.SetToolTip(_('Spatial interpolation based on active polyline'))

        # gSizer1.Add(self.m_button11, 0, wx.EXPAND)
        # self.m_button11.Bind(wx.EVT_BUTTON, self.interp2Dpolyline)

        # self.Interpolation.SetSizer(gSizer1)
        # self.Interpolation.Layout()
        # gSizer1.Fit(self.Interpolation)

        # Tools
        # -----

        Toolssizer = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)

        self._label_epsilon = wx.StaticText(self._tools,label=_('Epsilon'))
        self._txt_epsilon = wx.TextCtrl(self._tools,value=str(self._parent.epsilon), style=wx.TE_CENTER)
        self._txt_epsilon.SetToolTip(_('Epsilon value under which the value is not plotted'))

        self._label_nullvalue = wx.StaticText(self._tools,label=_('Null value'))
        self._txt_nullvalue = wx.TextCtrl(self._tools,value=str(self._parent.nullvalue), style=wx.TE_CENTER)
        self._txt_nullvalue.SetToolTip(_('Null value -- All node with this value will be masked (not plotted)'))

        hbox.Add(self._label_epsilon, 0, wx.EXPAND|wx.ALL)
        hbox.Add(self._txt_epsilon, 1, wx.EXPAND|wx.ALL)

        hbox2.Add(self._label_nullvalue, 0, wx.EXPAND|wx.ALL)
        hbox2.Add(self._txt_nullvalue, 1, wx.EXPAND|wx.ALL)

        self._Apply_Tools = wx.Button(self._tools, wx.ID_ANY, _("Apply modifications"), wx.DefaultPosition,
                                 wx.DefaultSize, 0)
        self._Apply_Tools.SetToolTip(_("Save modifications into memmory/object"))

        Toolssizer.Add(hbox, 0, wx.EXPAND)
        Toolssizer.Add(hbox2, 0, wx.EXPAND)
        Toolssizer.Add(self._Apply_Tools, 1, wx.EXPAND)

        self._tools.SetSizer(Toolssizer)
        self._tools.Layout()
        Toolssizer.Fit(self._tools)

        # Selection
        # ---------

        # bSizer15 = wx.BoxSizer(wx.VERTICAL)

        # bSizer21 = wx.BoxSizer(wx.HORIZONTAL)

        # bSizer16 = wx.BoxSizer(wx.VERTICAL)

        # selectmethodChoices = [_("by clicks"), _("inside active vector"), _("inside active zone"),
        #                        _("inside temporary vector"), _("under active vector"), _("under active zone"),
        #                        _("under temporary vector")]
        # self.selectmethod = wx.RadioBox(self.selection, wx.ID_ANY, _("How to select nodes?"), wx.DefaultPosition,
        #                                 wx.DefaultSize, selectmethodChoices, 1, wx.RA_SPECIFY_COLS)
        # self.selectmethod.SetSelection(0)
        # self.selectmethod.SetToolTip(_("Selection mode : \n - one by one (keyboard shortcut N) \n- inside the currently activated polygon (keyboard shortcut V) \n- inside the currently activated zone (multipolygons) \n- inside a temporary polygon (keyboard shortcut B) \n- under the currently activated polyline \n- under the currently activated zone (multipolylines) \n- under a temporary polyline"))

        # bSizer16.Add(self.selectmethod, 0, wx.ALL, 5)

        # self.selectrestricttomask = wx.CheckBox(self.selection,wx.ID_ANY,_('Use mask to restrict'))
        # self.selectrestricttomask.SetValue(True)
        # self.selectrestricttomask.SetToolTip(_('If checked, the selection will be restricted by the mask data'))

        # bSizer16.Add(self.selectrestricttomask, 0, wx.ALL, 5)

        # self.LaunchSelection = wx.Button(self.selection, wx.ID_ANY,
        #                                  _("Action !"), wx.DefaultPosition,
        #                                  wx.DefaultSize, 0)
        # self.LaunchSelection.SetBackgroundColour((0,128,64,255))
        # self.LaunchSelection.SetDefault()
        # # self.LaunchSelection.SetForegroundColour((255,255,255,255))
        # font = wx.Font(12, wx.FONTFAMILY_DECORATIVE, 0, 90, underline = False,faceName ="")
        # self.LaunchSelection.SetFont(font)

        # bSizer16.Add(self.LaunchSelection, 0, wx.EXPAND)
        # self.AllSelection = wx.Button(self.selection, wx.ID_ANY,
        #                               _("Select all nodes"), wx.DefaultPosition,
        #                               wx.DefaultSize, 0)
        # self.AllSelection.SetToolTip(_("Select all nodes in one click - store 'All' in the selection list"))
        # bSizer16.Add(self.AllSelection, 0, wx.EXPAND)
        # self.MoveSelection = wx.Button(self.selection, wx.ID_ANY,
        #                                _("Move current selection to..."), wx.DefaultPosition,
        #                                wx.DefaultSize, 0)
        # self.MoveSelection.SetToolTip(_("Store the current selection in an indexed list -- useful for some interpolation methods"))
        # bSizer16.Add(self.MoveSelection, 0, wx.EXPAND)
        # self.ResetSelection = wx.Button(self.selection, wx.ID_ANY,
        #                                 _("Reset"), wx.DefaultPosition,
        #                                 wx.DefaultSize, 0)
        # self.ResetSelection.SetToolTip(_("Reset the current selection list (keyboard shortcut r)"))
        # bSizer16.Add(self.ResetSelection, 0, wx.EXPAND)
        # self.ResetAllSelection = wx.Button(self.selection, wx.ID_ANY,
        #                                    _("Reset All"), wx.DefaultPosition,
        #                                    wx.DefaultSize, 0)
        # self.ResetAllSelection.SetToolTip(_("Reset the current selection list and the indexed lists (keyboard shortcut R)"))
        # bSizer16.Add(self.ResetAllSelection, 0, wx.EXPAND)

        # bSizer21.Add(bSizer16, 1, wx.EXPAND, 5)

        # bSizer17 = wx.BoxSizer(wx.VERTICAL)

        # self.m_button2 = wx.Button(self.selection, wx.ID_ANY, _("Manage vectors"), wx.DefaultPosition, wx.DefaultSize,
        #                            0)
        # self.m_button2.SetToolTip(_("Open the vector manager attached to the array"))
        # bSizer17.Add(self.m_button2, 0, wx.EXPAND)

        # self.active_vector_id = wx.StaticText(self.selection, wx.ID_ANY, _("Active vector"), wx.DefaultPosition,
        #                                       wx.DefaultSize, 0)
        # self.active_vector_id.Wrap(-1)

        # bSizer17.Add(self.active_vector_id, 0, wx.EXPAND)

        # self.CurActiveparent = wx.StaticText(self.selection, wx.ID_ANY, _("Active parent"), wx.DefaultPosition,
        #                                      wx.DefaultSize, 0)
        # self.CurActiveparent.Wrap(-1)

        # bSizer17.Add(self.CurActiveparent, 0, wx.EXPAND)

        # self.loadvec = wx.Button(self.selection, wx.ID_ANY, _("Read from file..."), wx.DefaultPosition, wx.DefaultSize,
        #                          0)
        # self.loadvec.SetToolTip(_("Load a vector file into the vector manager"))
        # bSizer17.Add(self.loadvec, 0, wx.EXPAND)

        # self.saveas = wx.Button(self.selection, wx.ID_ANY, _("Save as..."), wx.DefaultPosition, wx.DefaultSize, 0)
        # bSizer17.Add(self.saveas, 0, wx.EXPAND)
        # self.saveas.SetToolTip(_("Save the vector manager to a new vector file"))

        # self.save = wx.Button(self.selection, wx.ID_ANY, _("Save"), wx.DefaultPosition, wx.DefaultSize, 0)
        # self.save.SetToolTip(_("Save the vector manager to the kwnown vector file"))
        # bSizer17.Add(self.save, 0, wx.EXPAND)

        # bSizer21.Add(bSizer17, 1, wx.EXPAND, 5)

        # bSizer15.Add(bSizer21, 1, wx.EXPAND, 5)

        # bSizer22 = wx.BoxSizer(wx.HORIZONTAL)

        # self.nbselect = wx.StaticText(self.selection, wx.ID_ANY, _("nb"), wx.DefaultPosition, wx.DefaultSize, 0)
        # self.nbselect.Wrap(-1)

        # bSizer22.Add(self.nbselect, 1, wx.EXPAND, 10)

        # self.minx = wx.StaticText(self.selection, wx.ID_ANY, _("xmin"), wx.DefaultPosition, wx.DefaultSize, 0)
        # self.minx.Wrap(-1)

        # self.minx.SetToolTip(_("X Mininum"))

        # bSizer22.Add(self.minx, 1, wx.EXPAND, 10)

        # self.maxx = wx.StaticText(self.selection, wx.ID_ANY, _("xmax"), wx.DefaultPosition, wx.DefaultSize, 0)
        # self.maxx.Wrap(-1)

        # self.maxx.SetToolTip(_("X Maximum"))

        # bSizer22.Add(self.maxx, 1, wx.EXPAND, 10)

        # self.miny = wx.StaticText(self.selection, wx.ID_ANY, _("ymin"), wx.DefaultPosition, wx.DefaultSize, 0)
        # self.miny.Wrap(-1)

        # self.miny.SetToolTip(_("Y Minimum"))

        # bSizer22.Add(self.miny, 1, wx.EXPAND, 10)

        # self.maxy = wx.StaticText(self.selection, wx.ID_ANY, _("ymax"), wx.DefaultPosition, wx.DefaultSize, 0)
        # self.maxy.Wrap(-1)

        # self.maxy.SetToolTip(_("Y Maximum"))

        # bSizer22.Add(self.maxy, 1, wx.EXPAND, 10)

        # bSizer15.Add(bSizer22, 0, wx.EXPAND, 5)

        # self.selection.SetSizer(bSizer15)
        # self.selection.Layout()
        # bSizer15.Fit(self.selection)

        # Mask
        # ----

        # sizermask = wx.BoxSizer(wx.VERTICAL)
        # self.mask.SetSizer(sizermask)

        # unmaskall = wx.Button(self.mask, wx.ID_ANY, _("Unmask all"), wx.DefaultPosition, wx.DefaultSize, 0)
        # sizermask.Add(unmaskall, 1, wx.EXPAND)
        # unmaskall.Bind(wx.EVT_BUTTON, self.Unmaskall)
        # unmaskall.SetToolTip(_("Unmask all values in the current array"))

        # unmasksel = wx.Button(self.mask, wx.ID_ANY, _("Unmask selection"), wx.DefaultPosition, wx.DefaultSize, 0)
        # sizermask.Add(unmasksel, 1, wx.EXPAND)
        # unmasksel.Bind(wx.EVT_BUTTON, self.Unmasksel)
        # unmasksel.SetToolTip(_("Unmask all values in the current selection \n If you wish to unmask some of the currently masked data, you have to first select the desired nodes by unchecking the 'Use mask to retrict' on the 'Selection' panel, otherwise it is impossible to select these nodes"))

        # invertmask = wx.Button(self.mask, wx.ID_ANY, _("Invert mask"), wx.DefaultPosition, wx.DefaultSize, 0)
        # sizermask.Add(invertmask, 1, wx.EXPAND)
        # invertmask.Bind(wx.EVT_BUTTON, self.InvertMask)
        # invertmask.SetToolTip(_("Logical operation on mask -- mask = ~mask"))

        # self.mask.Layout()
        # sizermask.Fit(self.mask)

        # Operations
        # sizeropgen = wx.BoxSizer(wx.VERTICAL)
        # sepopcond = wx.BoxSizer(wx.HORIZONTAL)
        # sizerop = wx.BoxSizer(wx.VERTICAL)
        # sizercond = wx.BoxSizer(wx.VERTICAL)
        # # bSizer26 = wx.BoxSizer( wx.VERTICAL )

        # # bSizer14.Add( bSizer26, 1, wx.EXPAND, 5 )
        # sepopcond.Add(sizercond, 1, wx.EXPAND)
        # sepopcond.Add(sizerop, 1, wx.EXPAND)
        # sizeropgen.Add(sepopcond, 1, wx.EXPAND)

        # operationChoices = [u"+", u"-", u"*", u"/", _("replace")]
        # self.choiceop = wx.RadioBox(self.operation, wx.ID_ANY,
        #                             _("Operator"), wx.DefaultPosition,
        #                             wx.DefaultSize, operationChoices, 1, wx.RA_SPECIFY_COLS)
        # self.choiceop.SetSelection(4)
        # sizerop.Add(self.choiceop, 1, wx.EXPAND)

        # self.opvalue = wx.TextCtrl(self.operation, wx.ID_ANY, u"1",
        #                            wx.DefaultPosition, wx.DefaultSize, style=wx.TE_CENTER)
        # sizerop.Add(self.opvalue, 0, wx.EXPAND)
        # self.opvalue.SetToolTip(_('Numeric value or "Null"'))

        # conditionChoices = [u"<", u"<=", u"=", u">=", u">", u"isNaN"]
        # self.condition = wx.RadioBox(self.operation, wx.ID_ANY, _("Condition"), wx.DefaultPosition, wx.DefaultSize,
        #                              conditionChoices, 1, wx.RA_SPECIFY_COLS)
        # self.condition.SetSelection(2)
        # sizercond.Add(self.condition, 1, wx.EXPAND)

        # self.condvalue = wx.TextCtrl(self.operation, wx.ID_ANY, u"0",
        #                              wx.DefaultPosition, wx.DefaultSize, style=wx.TE_CENTER)
        # sizercond.Add(self.condvalue, 0, wx.EXPAND)

        # self.ApplyOp = wx.Button(self.operation, wx.ID_ANY, _("Apply math operator (Condition and Operator)"), wx.DefaultPosition,
        #                          wx.DefaultSize, 0)
        # sizeropgen.Add(self.ApplyOp, 1, wx.EXPAND)
        # self.ApplyOp.SetToolTip(_("This action will use the condition AND the operator to manipulate the selected nodes"))

        # self.SelectOp = wx.Button(self.operation, wx.ID_ANY, _("Select nodes (only Condition)"), wx.DefaultPosition,
        #                           wx.DefaultSize, 0)
        # self.SelectOp.SetToolTip(_("This action will use the condition AND NOT the operator to select some nodes"))
        # sizeropgen.Add(self.SelectOp, 1, wx.EXPAND)

        # maskdata = wx.Button(self.operation, wx.ID_ANY, _("Mask nodes (only Condition )"), wx.DefaultPosition, wx.DefaultSize, 0)
        # maskdata.SetToolTip(_("This action will use the condition AND NOT the operator to mask some selected nodes \n If no node is selectd --> Nothing to do !!"))
        # sizeropgen.Add(maskdata, 1, wx.EXPAND)
        # maskdata.Bind(wx.EVT_BUTTON, self.Onmask)

        # self.operation.SetSizer(sizeropgen)
        # self.operation.Layout()
        # sizeropgen.Fit(self.operation)

        gensizer = wx.BoxSizer(wx.VERTICAL)
        gensizer.Add(self._notebook, 1, wx.EXPAND | wx.ALL)

        self.SetSizer(gensizer)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        # self.LaunchSelection.Bind(wx.EVT_BUTTON, self.OnLaunchSelect)
        # self.AllSelection.Bind(wx.EVT_BUTTON, self.OnAllSelect)
        # self.MoveSelection.Bind(wx.EVT_BUTTON, self.OnMoveSelect)
        # self.ResetSelection.Bind(wx.EVT_BUTTON, self.OnResetSelect)
        # self.ResetAllSelection.Bind(wx.EVT_BUTTON, self.OnResetAllSelect)
        # self.m_button2.Bind(wx.EVT_BUTTON, self.OnManageVectors)
        # self.loadvec.Bind(wx.EVT_BUTTON, self.OnLoadvec)
        # self.saveas.Bind(wx.EVT_BUTTON, self.OnSaveasvec)
        # self.save.Bind(wx.EVT_BUTTON, self.OnSavevec)
        # self.ApplyOp.Bind(wx.EVT_BUTTON, self.OnApplyOpMath)
        # self.SelectOp.Bind(wx.EVT_BUTTON, self.OnApplyOpSelect)
        self._Apply_Tools.Bind(wx.EVT_BUTTON, self.OnApplyTools)
        self._cm_apply.Bind(wx.EVT_BUTTON, self.Onupdatepal)
        self._cm_save.Bind(wx.EVT_BUTTON, self.Onsavepal)
        self._cm_load.Bind(wx.EVT_BUTTON, self.Onloadpal)
        self._cm_toimage.Bind(wx.EVT_BUTTON, self.Onpalimage)
        self._cm_distribute.Bind(wx.EVT_BUTTON, self.Onpaldistribute)
        self._cm_choose_color.Bind(wx.EVT_BUTTON, self.OnClickColorPal)
        self._histo_update.Bind(wx.EVT_BUTTON, self.OnClickHistoUpdate)
        self._histo_updatezoom.Bind(wx.EVT_BUTTON, self.OnClickHistoUpdate)
        self._histo_updateerase.Bind(wx.EVT_BUTTON, self.OnClickHistoUpdate)

    def onclose(self, event: wx.CloseEvent):
        """ Hide the window instead of closing/detsroy it """
        self.Hide()

    def onshow(self, event: wx.ShowEvent):
        """ Update the GUI when the window is shown """
        if self._parent.nullvalue == np.nan:
            self._txt_nullvalue.Value = 'nan'
        else :
            self._txt_nullvalue.Value = str(self._parent.epsilon)

        self.update_palette()

    def OnApplyTools(self, event:wx.MouseEvent):
        """ Apply modifications in the textctrl """

        neweps:str  = self._txt_epsilon.Value
        newnull:str = self._txt_nullvalue.Value

        if neweps.lower() == 'nan':
            neweps = np.nan
        else:
            neweps = float(neweps)

        if newnull.lower() == 'nan':
            newnull = np.nan
        else:
            newnull = float(newnull)

        to_update = False
        if self._parent.epsilon != neweps:
            self._parent.epsilon = neweps
            to_update = True

        if self._parent.nullvalue != newnull:
            self._parent.nullvalue = newnull
            to_update = True

        if to_update:
            self._parent.read_oneresult(self._parent.current_result)
            self._parent.set_currentview()

    def update_palette(self):
        """ Update the colormap grid and plot """

        # Update the plot
        self._panel_colormap.add_ax()
        fig, ax = self._panel_colormap.get_fig_ax()
        self._parent.mypal.plot(fig, ax)
        fig.canvas.draw()

        # Fill the grid
        self._parent.mypal.fillgrid(self._cm_grid)

    def Onsavepal(self, event):
        """ Save the colormap to a file """

        self._parent.mypal.savefile()

    def Onloadpal(self, event):
        """ Read the colormap from a file """

        self._parent.mypal.readfile()

        self._parent.mypal.automatic = False
        self._cm_auto.SetValue(0)

        self._parent.set_currentview()
        self.update_palette()

    def Onpalimage(self, event):
        """ Export the colormap to an image """

        self._parent.mypal.export_image()

    def Onpaldistribute(self, event):
        """ Distribute uniformly the colormap values """

        self._parent.mypal.distribute_values()

        self._parent.mypal.automatic = False
        self._cm_auto.SetValue(0)

        self._parent.set_currentview()
        self.update_palette()

    def Onupdatepal(self, event):
        """ Update the colormap from the grid """

        dellists = False
        auto = self._cm_auto.IsChecked()
        uni  = self._cm_uniform_or_lerp.IsChecked()

        oldalpha = self._parent.alpha
        if self._cm_alpha.IsChecked():
            self._parent.alpha=1.
        else:
            self._parent.alpha = float(self._cm_slider_alpha.GetValue()) / 100.

        ret = self._parent.mypal.updatefromgrid(self._cm_grid)
        if self._parent.mypal.automatic != auto or self._parent.alpha != oldalpha or ret or auto != self._parent.mypal.automatic or uni != self._parent.mypal.interval_cst:
            self._parent.mypal.automatic = auto
            self._parent.mypal.interval_cst = uni
            self._parent.updatepalette(0)
            dellists = True

        shadehill = self._cm_hillshade.IsChecked()
        if not self._parent.shading and shadehill:
            self._parent.shading = True
            dellists = True

        if shadehill:
            azim = float(self._cm_slider_azimuth.GetValue())
            alti = float(self._cm_slider_altitude.GetValue())

            if self._parent.azimuthhill != azim:
                self._parent.azimuthhill = azim
                self._parent.shading = True

            if self._parent.altitudehill != alti:
                self._parent.altitudehill = alti
                self._parent.shading = True

            alpha = float(self._cm_slider_hillshade.GetValue()) / 100.
            if self._parent.shaded.alpha != alpha:
                self._parent.shaded.alpha = alpha
                self._parent.shading = True

        if dellists:
            self._parent.set_currentview()

    def OnClickHistoUpdate(self, event: wx.MouseEvent):
        """ Click to update the histogram """

        itemlabel = event.GetEventObject().GetLabel()
        fig, ax = self._panel_histo.get_fig_ax()

        if itemlabel == self._histo_updateerase.LabelText:
            ax.clear()
            fig.canvas.draw()
            return

        onzoom = []
        if itemlabel == self._histo_updatezoom.LabelText:
            if self._mapviewer is not None:
                onzoom = [self._mapviewer.xmin, self._mapviewer.xmax, self._mapviewer.ymin, self._mapviewer.ymax]

        partarray = self._parent.get_working_array(onzoom).flatten(order='F')  # .sort(axis=-1)

        ax: plt.Axes
        ax.hist(partarray, 200, density=True)

        fig.canvas.draw()

    def OnClickColorPal(self, event: wx.MouseEvent):
        """ Click to open the color dialog box """

        gridto = self._cm_grid
        k = gridto.GetGridCursorRow()
        r = int(gridto.GetCellValue(k, 1))
        g = int(gridto.GetCellValue(k, 2))
        b = int(gridto.GetCellValue(k, 3))

        curcol = wx.ColourData()
        curcol.SetChooseFull(True)
        curcol.SetColour(wx.Colour(r, g, b))

        dlg = wx.ColourDialog(None, curcol)
        ret = dlg.ShowModal()

        if ret == wx.ID_CANCEL:
            dlg.Destroy()
            return

        curcol = dlg.GetColourData()
        dlg.Destroy()

        rgb = curcol.GetColour()

        k = gridto.GetGridCursorRow()
        gridto.SetCellValue(k, 1, str(rgb.red))
        gridto.SetCellValue(k, 2, str(rgb.green))
        gridto.SetCellValue(k, 3, str(rgb.blue))

    # def interpolation2D(self, event: wx.MouseEvent):
    #     self._parent.interpolation2D()

    # def Unmaskall(self, event: wx.MouseEvent):
    #     """
    #     Enlève le masque des tous les éléments
    #     @author Pierre Archambeau
    #     """
    #     curarray: WolfArray
    #     curarray = self._parent
    #     curarray.mask_reset()
    #     curarray = self._parent
    #     curarray.updatepalette()
    #     curarray.delete_lists()

    # def Unmasksel(self,event:wx.MouseEvent):
    #     """
    #     Enlève le masque des éléments sélectionnés
    #     @author Pierre Archambeau
    #     """
    #     curarray: WolfArray
    #     curarray = self._parent

    #     if len(curarray.mngselection.myselection) == 0:
    #         return
    #     else:
    #         destxy = curarray.mngselection.myselection

    #     destij = np.asarray([list(curarray.get_ij_from_xy(x, y)) for x, y in destxy])

    #     curarray.array.mask[destij[:, 0], destij[:, 1]] = False

    #     curarray.updatepalette()
    #     curarray.delete_lists()

    # def InvertMask(self, event: wx.MouseEvent):

    #     curarray: WolfArray
    #     curarray = self._parent
    #     curarray.mask_invert()
    #     curarray = self._parent
    #     curarray.updatepalette()
    #     curarray.delete_lists()

    # def interp2Dpolygons(self, event: wx.MouseEvent):
    #     """
    #     Bouton d'interpolation sous tous les polygones d'une zone
    #     cf _interp2Dpolygon
    #     """
    #     choices = ["nearest", "linear", "cubic"]
    #     dlg = wx.SingleChoiceDialog(None, "Pick an interpolate method", "Choices", choices)
    #     ret = dlg.ShowModal()
    #     if ret == wx.ID_CANCEL:
    #         dlg.Destroy()
    #         return

    #     method = dlg.GetStringSelection()
    #     dlg.Destroy()

    #     actzone = self.active_zone
    #     curarray: WolfArray
    #     curarray = self._parent

    #     for curvec in actzone.myvectors:
    #         curvec: vector
    #         self._interp2Dpolygon(curvec, method)

    #     curarray.updatepalette()
    #     curarray.delete_lists()

    # def interp2Dpolygon(self, event: wx.MouseEvent):
    #     """
    #     Bouton d'interpolation sous un polygone
    #     cf _interp2Dpolygon
    #     """
    #     choices = ["nearest", "linear", "cubic"]
    #     dlg = wx.SingleChoiceDialog(None, "Pick an interpolate method", "Choices", choices)
    #     ret = dlg.ShowModal()
    #     if ret == wx.ID_CANCEL:
    #         dlg.Destroy()
    #         return

    #     method = dlg.GetStringSelection()
    #     dlg.Destroy()

    #     actzone = self.active_zone
    #     curarray: WolfArray
    #     curarray = self._parent

    #     self._interp2Dpolygon(self.active_vector, method)

    #     curarray.updatepalette()
    #     curarray.delete_lists()

    # def _interp2Dpolygon(self, vect: vector, method):
    #     """
    #     Interpolation sous un polygone

    #     L'interpolation a lieu :
    #       - uniquement dans les mailles sélectionnées si elles existent
    #       - dans les mailles contenues dans le polygone sinon

    #     On utilise ensuite "griddata" pour interpoler les altitudes des mailles
    #     depuis les vertices 3D du polygone
    #     """
    #     curarray: WolfArray
    #     curarray = self._parent

    #     if len(curarray.mngselection.myselection) == 0:
    #         destxy = curarray.get_xy_inside_polygon(vect)
    #     else:
    #         destxy = curarray.mngselection.myselection

    #     if len(destxy)==0:
    #         return

    #     destij = np.asarray([list(curarray.get_ij_from_xy(x, y)) for x, y in destxy])

    #     xyz = vect.asnparray3d()

    #     newvalues = griddata(xyz[:, :2], xyz[:, 2], destxy, method=method, fill_value=-99999.)

    #     locmask = np.where(newvalues != -99999.)
    #     curarray.array.data[destij[locmask][:, 0], destij[locmask][:, 1]] = newvalues[locmask]

    # def interp2Dpolylines(self, event: wx.MouseEvent):
    #     """
    #     Bouton d'interpolation sous toutes les polylignes de la zone
    #     cf _interp2Dpolyline
    #     """
    #     actzone = self.active_zone
    #     curarray: WolfArray
    #     curarray = self._parent

    #     for curvec in actzone.myvectors:
    #         curvec: vector
    #         self._interp2Dpolyline(curvec)

    #     curarray.updatepalette()
    #     curarray.delete_lists()

    # def interp2Dpolyline(self, event: wx.MouseEvent):
    #     """
    #     Bouton d'interpolation sous la polyligne active
    #     cf _interp2Dpolyline
    #     """
    #     curarray: WolfArray
    #     curarray = self._parent

    #     self._interp2Dpolyline(self.active_vector)

    #     curarray.updatepalette()
    #     curarray.delete_lists()

    # def _interp2Dpolyline(self, vect: vector, usemask=True):
    #     """
    #     Interpolation sous une polyligne

    #     L'interpolation a lieu :
    #       - uniquement dans les mailles sélectionnées si elles existent
    #       - dans les mailles sous la polyligne sinon

    #     On utilise ensuite "interpolate" de shapely pour interpoler les altitudes des mailles
    #     depuis les vertices 3D de la polyligne
    #     """
    #     curarray: WolfArray
    #     curarray = self._parent

    #     vecls = vect.asshapely_ls()
    #     if len(curarray.mngselection.myselection) == 0:
    #         allij = curarray.get_ij_under_polyline(vect, usemask)
    #         allxy = [curarray.get_xy_from_ij(cur[0], cur[1]) for cur in allij]
    #     else:
    #         allxy = curarray.mngselection.myselection
    #         allij = np.asarray([curarray.get_ij_from_xy(x,y) for x,y in allxy])

    #     newz = np.asarray([vecls.interpolate(vecls.project(Point(x, y))).z for x, y in allxy])
    #     curarray.array.data[allij[:, 0], allij[:, 1]] = newz

    # def volumesurface(self, event):
    #     """
    #     Click on evaluation of stage-storage-surface relation
    #     """
    #     self._volumesurface()

    # def _volumesurface(self, show=True):
    #     """
    #     Evaluation of stage-storage-surface relation
    #     """
    #     if self._mapviewer is not None:
    #         if self._mapviewer.linked:
    #             array1 = self._mapviewer.linkedList[0].active_array
    #             array2 = self._mapviewer.linkedList[1].active_array

    #             # transfert des mailles sélectionnées dans l'autre matrice
    #             if array1 is self._parent:
    #                 array2.mngselection.myselection = array1.mngselection.myselection.copy()
    #             if array2 is self._parent:
    #                 array1.mngselection.myselection = array2.mngselection.myselection.copy()

    #             if len(self._parent.mngselection.myselection) == 0 or self._parent.mngselection.myselection == 'all':
    #                 myarray = array1
    #                 axs = myarray.volume_estimation()
    #                 myarray = array2
    #                 axs = myarray.volume_estimation(axs)
    #             else:
    #                 myarray = array1.mngselection.get_newarray()
    #                 axs = myarray.volume_estimation()
    #                 myarray = array2.mngselection.get_newarray()
    #                 axs = myarray.volume_estimation(axs)
    #         else:
    #             if len(self._parent.mngselection.myselection) == 0 or self._parent.mngselection.myselection == 'all':
    #                 myarray = self._parent
    #             else:
    #                 myarray = self._parent.mngselection.get_newarray()
    #             myarray.volume_estimation()
    #     else:
    #         if len(self._parent.mngselection.myselection) == 0 or self._parent.mngselection.myselection == 'all':
    #             myarray = self._parent
    #         else:
    #             myarray = self._parent.mngselection.get_newarray()
    #         myarray.volume_estimation()

    #     if show:
    #         plt.show()

    # def OnAllSelect(self, event):
    #     """
    #     Select all --> just put "all" in "myselection"
    #     """
    #     self._parent.mngselection.myselection = 'all'
    #     self._parent.myops.nbselect.SetLabelText('All')

    # def OnMoveSelect(self, event):
    #     """Transfert de la sélection courante dans un dictionnaire"""
    #     dlg = wx.TextEntryDialog(self, 'Choose id', 'id?')
    #     ret = dlg.ShowModal()
    #     idtxt = dlg.GetValue()

    #     dlg = wx.ColourDialog(self)
    #     ret = dlg.ShowModal()
    #     color = dlg.GetColourData()

    #     self._parent.mngselection.move_selectionto(idtxt, color.GetColour())

    # def reset_selection(self):
    #     """
    #     Reset of current selection
    #     """
    #     self._parent.mngselection.myselection = []
    #     self.nbselect.SetLabelText('0')
    #     self.minx.SetLabelText('0')
    #     self.miny.SetLabelText('0')
    #     self.maxx.SetLabelText('0')
    #     self.maxy.SetLabelText('0')

    # def reset_all_selection(self):
    #     """
    #     Reset of current selection and stored ones
    #     """
    #     self.reset_selection()
    #     self._parent.mngselection.selections = {}

    # def OnResetSelect(self, event):
    #     """
    #     Click on Reset of current selection
    #     """
    #     self.reset_selection()

    # def OnResetAllSelect(self, event):
    #     """
    #     Click on reset all
    #     """
    #     self.reset_all_selection()

    # def OnApplyOpSelect(self, event):
    #     curcond = self.condition.GetSelection()

    #     curcondvalue = float(self.condvalue.GetValue())

    #     self._parent.mngselection.condition_select(curcond, curcondvalue)

    # def OnApplyOpMath(self, event):

    #     curop = self.choiceop.GetSelection()
    #     curcond = self.condition.GetSelection()

    #     opval = self.opvalue.GetValue()
    #     if opval.lower() == 'null' or opval.lower() == 'nan':
    #         curopvalue = self._parent.nullvalue
    #     else:
    #         curopvalue = float(opval)
    #     curcondvalue = float(self.condvalue.GetValue())

    #     self._parent.mngselection.treat_select(curop, curcond, curopvalue, curcondvalue)

    # def Onmask(self, event):

    #     curop = self.choiceop.GetSelection()
    #     curcond = self.condition.GetSelection()

    #     curopvalue = float(self.opvalue.GetValue())
    #     curcondvalue = float(self.condvalue.GetValue())

    #     self._parent.mngselection.mask_condition(curop, curcond, curopvalue, curcondvalue)
    #     self._parent.reset_plot()
    #     pass

    # def OnManageVectors(self, event):
    #     if self._mapviewer is not None:
    #         if self._mapviewer.linked:
    #             if self._mapviewer.link_shareopsvect:
    #                     if self.myzones.parent in self._mapviewer.linkedList:
    #                         self.myzones.showstructure()
    #                     return

    #     self.myzones.showstructure()

    # def OnLoadvec(self, event):
    #     dlg = wx.FileDialog(None, 'Select file',
    #                         wildcard='Vec file (*.vec)|*.vec|Vecz file (*.vecz)|*.vecz|Dxf file (*.dxf)|*.dxf|All (*.*)|*.*', style=wx.FD_OPEN)

    #     ret = dlg.ShowModal()
    #     if ret == wx.ID_CANCEL:
    #         dlg.Destroy()
    #         return

    #     self.fnsave = dlg.GetPath()
    #     dlg.Destroy()
    #     self.myzones = Zones(self.fnsave, parent=self)

    #     if self._mapviewer is not None:
    #         if self._mapviewer.linked:
    #             if not self._mapviewer.linkedList is None:
    #                 for curFrame in self._mapviewer.linkedList:
    #                     if curFrame.link_shareopsvect:
    #                         curFrame.active_array.myops.myzones = self.myzones
    #                         curFrame.active_array.myops.fnsave = self.fnsave

    # def OnSaveasvec(self, event):

    #     dlg = wx.FileDialog(None, 'Select file', wildcard='Vec file (*.vec)|*.vec|Vecz file (*.vecz)|*.vecz|All (*.*)|*.*', style=wx.FD_SAVE)

    #     ret = dlg.ShowModal()
    #     if ret == wx.ID_CANCEL:
    #         dlg.Destroy()
    #         return

    #     self.fnsave = dlg.GetPath()
    #     dlg.Destroy()

    #     self.myzones.saveas(self.fnsave)

    #     if self._mapviewer is not None:
    #         if self._mapviewer.linked:
    #             if not self._mapviewer.linkedList is None:
    #                 for curFrame in self._mapviewer.linkedList:
    #                     if curFrame.link_shareopsvect:
    #                         curFrame.active_array.myops.fnsave = self.fnsave

    # def OnSavevec(self, event):

    #     if self.fnsave == '':
    #         return

    #     self.myzones.saveas(self.fnsave)

    def select_node_by_node(self):
        if self._mapviewer is not None:
            self._mapviewer.action = 'select node by node - results'
            self._mapviewer.active_res2d = self._parent

    # def select_zone_inside_manager(self):

    #     if self.active_zone is None:
    #         wx.MessageBox('Please select an active zone !')
    #         return

    #     for curvec in self.active_zone.myvectors:
    #         self._select_vector_inside_manager(curvec)

    # def select_vector_inside_manager(self):
    #     if self.active_vector is None:
    #         wx.MessageBox('Please select an active vector !')
    #         return

    #     self._select_vector_inside_manager(self.active_vector)

    # def _select_vector_inside_manager(self, vect: vector):

    #     if len(vect.myvertices) > 2:
    #         self._parent.mngselection.select_insidepoly(vect)

    #     elif self._mapviewer is not None:
    #         if len(vect.myvertices) < 3:
    #             wx.MessageBox('Please add points to vector by clicks !')

    #         self._mapviewer.action = 'select by vector inside'
    #         self._mapviewer.active_array = self._parent
    #         self.Active_vector(vect)

    #         firstvert = wolfvertex(0., 0.)
    #         self.vectmp.add_vertex(firstvert)

    # def select_zone_under_manager(self):

    #     if self.active_zone is None:
    #         wx.MessageBox('Please select an active zone !')
    #         return

    #     for curvec in self.active_zone.myvectors:
    #         self._select_vector_under_manager(curvec)

    # def select_vector_under_manager(self):
    #     if self.active_vector is None:
    #         wx.MessageBox('Please select an active vector !')
    #         return

    #     self._select_vector_under_manager(self.active_vector)

    # def _select_vector_under_manager(self, vect: vector):

    #     if len(vect.myvertices) > 1:
    #         self._parent.mngselection.select_underpoly(vect)

    #     elif self._mapviewer is not None:
    #         if len(vect.myvertices) < 2:
    #             wx.MessageBox('Please add points to vector by clicks !')

    #         self._mapviewer.action = 'select by vector under'
    #         self._mapviewer.active_array = self._parent
    #         self.Active_vector(vect)

    #         firstvert = wolfvertex(0., 0.)
    #         self.vectmp.add_vertex(firstvert)

    # def select_vector_inside_tmp(self):
    #     if self._mapviewer is not None:
    #         self._mapviewer.action = 'select by tmp vector inside'
    #         self.vectmp.reset()
    #         self.Active_vector(self.vectmp)
    #         self._mapviewer.active_array = self._parent

    #         firstvert = wolfvertex(0., 0.)
    #         self.vectmp.add_vertex(firstvert)

    # def select_vector_under_tmp(self):
    #     if self._mapviewer is not None:
    #         self._mapviewer.action = 'select by tmp vector under'
    #         self.vectmp.reset()
    #         self.Active_vector(self.vectmp)
    #         self._mapviewer.active_array = self._parent

    #         firstvert = wolfvertex(0., 0.)
    #         self.vectmp.add_vertex(firstvert)

    # def OnLaunchSelect(self, event):
    #     id = self.selectmethod.GetSelection()

    #     if id == 0:
    #         logging.info(_('Node selection by individual clicks'))
    #         logging.info(_(''))
    #         logging.info(_('   Clicks on the desired nodes...'))
    #         logging.info(_(''))
    #         self.select_node_by_node()
    #     elif id == 1:
    #         logging.info(_('Node selection inside active vector (manager)'))
    #         self.select_vector_inside_manager()
    #     elif id == 2:
    #         logging.info(_('Node selection inside active zone (manager)'))
    #         self.select_zone_inside_manager()
    #     elif id == 3:
    #         logging.info(_('Node selection inside temporary vector'))
    #         logging.info(_(''))
    #         logging.info(_('   Choose vector by clicks...'))
    #         logging.info(_(''))
    #         self.select_vector_inside_tmp()
    #     elif id == 4:
    #         logging.info(_('Node selection under active vector (manager)'))
    #         self.select_vector_under_manager()
    #     elif id == 5:
    #         logging.info(_('Node selection under active zone (manager)'))
    #         self.select_zone_under_manager()
    #     elif id == 6:
    #         logging.info(_('Node selection under temporary vector'))
    #         logging.info(_(''))
    #         logging.info(_('   Choose vector by clicks...'))
    #         logging.info(_(''))
    #         self.select_vector_under_tmp()

    # def Active_vector(self, vect: vector, copyall=True):
    #     if vect is None:
    #         return
    #     self.active_vector = vect
    #     self.active_vector_id.SetLabelText(vect.myname)

    #     if vect.parentzone is not None:
    #         self.active_zone = vect.parentzone

    #     if self._mapviewer is not None and copyall:
    #         self._mapviewer.Active_vector(vect)

    # def Active_zone(self, zone):
    #     self.active_zone = zone
    #     if self._mapviewer is not None:
    #         self._mapviewer.Active_zone(zone)

class views_2D(Enum):
    WATERDEPTH = _('Water depth [m]')
    WATERLEVEL = _('Water level [m]')
    TOPOGRAPHY = _('Bottom level [m]')
    QX = _('Discharge X [m2s-1]')
    QY = _('Discharge Y [m2s-1]')
    QNORM = _('Discharge norm [m2s-1]')
    UX  =_('Velocity X [ms-1]')
    UY = _('Velocity Y [ms-1]')
    UNORM = _('Velocity norm [ms-1]')
    HEAD = _('Head [m]')
    FROUDE = _('Froude [-]')
    KINETIC_ENERGY = _('Kinetic energy k')
    EPSILON = _('Rate of dissipation e')
    TURB_VISC_2D = _('Turbulent viscosity 2D')
    TURB_VISC_3D = _('Turbulent viscosity 3D')
    VECTOR_FIELD_Q = _('Discharge vector field')
    VECTOR_FIELD_U = _('Velocity vector field')
    SHIELDS_NUMBER = _('Shields number - Manning-Strickler')
    CRITICAL_DIAMETER_SHIELDS = _('Critical grain diameter - Shields')
    CRITICAL_DIAMETER_IZBACH = _('Critical grain diameter - Izbach')
    CRITICAL_DIAMETER_SUSPENSION_50 = _('Critical grain diameter - Suspension 50%')
    CRITICAL_DIAMETER_SUSPENSION_100 = _('Critical grain diameter - Suspension 100%')
    QNORM_FIELD = _('Q norm + Field')
    UNORM_FIELD = _('U norm + Field')
    WL_Q = _('WL + Q')
    WD_Q = _('WD + Q')
    WL_U = _('WL + U')
    WD_U = _('WD + U')
    T_WL_Q = _('Top + WL + Q')
    T_WD_Q = _('Top + WD + Q')
    T_WD_U = _('Top + WD + U')

VIEWS_SEDIMENTARY = [views_2D.SHIELDS_NUMBER,
                     views_2D.CRITICAL_DIAMETER_SHIELDS,
                     views_2D.CRITICAL_DIAMETER_IZBACH,
                     views_2D.CRITICAL_DIAMETER_SUSPENSION_50,
                     views_2D.CRITICAL_DIAMETER_SUSPENSION_100]

VIEWS_COMPLEX = [views_2D.T_WD_Q,
                 views_2D.T_WD_U,
                 views_2D.T_WL_Q,
                 views_2D.WL_Q,
                 views_2D.WD_Q,
                 views_2D.WL_U,
                 views_2D.WD_U,
                 views_2D.QNORM_FIELD,
                 views_2D.UNORM_FIELD]

VIEWS_VECTOR_FIELD = [views_2D.VECTOR_FIELD_Q, views_2D.VECTOR_FIELD_U]

class OneWolfResult:
    """
    Stockage des résultats d'un bloc de modèle WOLF2D
    """
    def __init__(self, idx:int=0, parent = None):

        self.parent = parent

        self.wx_exists = wx.GetApp() is not None

        self.blockindex = idx          # index du bloc en numérotation Python --> penser à ajouter 1 si retour type VB6/Fortran
        self.idx = getkeyblock(idx)
        self.linkedvec = None
        self.epsilon = 0.

        self.waterdepth = WolfArray()
        self.top = WolfArray()
        self.qx = WolfArray()
        self.qy = WolfArray()
        self.rough_n = WolfArray()
        self.set_current(views_2D.WATERDEPTH)

        self.k = WolfArray()
        self.eps = WolfArray()

        self.ShieldsNumber = None
        self.critShields = None
        self.critIzbach = None
        self.critSusp50 = None
        self.critSusp100 = None

        self._vec_field = None
        self._min_field_size = .1

        self._sedimentdiam = 1e-3
        self._sedimentdensity = 2.65
        self._force_update_shields = True # Force la MAJ du Shields si le diametre ou la densité change

    @property
    def sediment_diameter(self):
        """ Diamètre des particules de sédiment [m] """

        return self._sedimentdiam

    @sediment_diameter.setter
    def sediment_diameter(self, value:float):
        """ Diamètre des particules de sédiment [m] """

        self._force_update_shields = self._sedimentdiam != value
        self._sedimentdiam = value
        # forcer la MAJ si nécessaire
        if self._which_current == views_2D.SHIELDS_NUMBER:
            self.set_current(views_2D.SHIELDS_NUMBER)

    @property
    def sediment_density(self):
        """ Densité des particules de sédiment [-] """

        return self._sedimentdensity

    @sediment_density.setter
    def sediment_density(self, value:float):
        """ Densité des particules de sédiment [-] """

        self._force_update_shields = self._sedimentdensity != value
        self._sedimentdensity = value
        # forcer la MAJ si nécessaire
        if self._which_current == views_2D.SHIELDS_NUMBER:
            self.set_current(views_2D.SHIELDS_NUMBER)

    @property
    def current(self):
        """ Vue courante """

        return self._current

    def set_linkedvec(self, link:vector):
        """ Set the linked vecteor -- used for masking outside the vector """
        self.linkedvec = link

    def set_epsilon(self, eps:float):
        """
        Définit la valeur de l'epsilon pour le masquage des données.

        Toute valeur de waterdepth inférieure à eps sera masquée. see "filter_inundation"

        :param eps: valeur de l'epsilon
        """

        self.epsilon = eps

    def filter_inundation(self):
        """
        Apply filter on array :
            - mask data below eps
            - mask data outisde linkedvec
        """
        mask = self.waterdepth.array < self.epsilon
        self._current.filter_inundation(mask = mask)

    def set_current(self, which:views_2D):
        """
        Définition de la vue courante

        :param which: vue courante (voir enum views_2D)
        """

        self._which_current = which

        if which==views_2D.WATERDEPTH:
            self._current=self.waterdepth
            nullvalue = self.waterdepth.nullvalue
        elif which==views_2D.TOPOGRAPHY:
            self._current=self.top
            nullvalue = self.top.nullvalue
        elif which==views_2D.QX:
            self._current=self.qx
            nullvalue = self.qx.nullvalue
        elif which==views_2D.QY:
            self._current=self.qy
            nullvalue = self.qy.nullvalue
        elif which==views_2D.QNORM:
            self._current=(self.qx**2.+self.qy**2.)**.5
            nullvalue = self.qx.nullvalue
        elif which==views_2D.UNORM:
            self._current=(self.qx**2.+self.qy**2.)**.5/self.waterdepth
            nullvalue = self.qx.nullvalue
        elif which==views_2D.UX:
            self._current=self.qx/self.waterdepth
            nullvalue = self.qx.nullvalue
        elif which==views_2D.UY:
            self._current=self.qy/self.waterdepth
            nullvalue = self.qy.nullvalue
        elif which==views_2D.WATERLEVEL:
            self._current=self.waterdepth+self.top
            nullvalue = self.waterdepth.nullvalue
        elif which==views_2D.FROUDE:
            self._current=(self.qx**2.+self.qy**2.)**.5/self.waterdepth/(self.waterdepth*9.81)**.5
            nullvalue = self.qx.nullvalue
        elif which==views_2D.HEAD:
            self._current=(self.qx**2.+self.qy**2.)**.5/self.waterdepth/(2.*9.81)+self.waterdepth+self.top
            nullvalue = self.qx.nullvalue
        elif which==views_2D.KINETIC_ENERGY:
            self._current=self.k
            nullvalue = self.k.nullvalue
        elif which==views_2D.EPSILON:
            self._current=self.eps
            nullvalue = self.eps.nullvalue
        elif which==views_2D.VECTOR_FIELD_Q:
            self._current=(self.qx**2.+self.qy**2.)**.5
            nullvalue = self.qx.nullvalue
            self._vec_field = VectorField(self.qx.array, self.qy.array, self.qx.get_bounds(), self.qx.dx, self.qy.dy, minsize=self._min_field_size)
        elif which==views_2D.VECTOR_FIELD_U:
            ux = self.qx/self.waterdepth
            uy = self.qy/self.waterdepth
            self._current=(ux**2.+uy**2.)**.5
            self._vec_field = VectorField(ux.array, uy.array, ux.get_bounds(), ux.dx, ux.dy, minsize=self._min_field_size)

            nullvalue = self.qx.nullvalue

        elif which ==views_2D.QNORM_FIELD:

            self._current = (self.qx**2.+self.qy**2.)**.5
            self._view = WolfViews()

            self._vec_field = VectorField(self.qx.array, self.qy.array, self.qx.get_bounds(), self.qx.dx, self.qy.dy, minsize=self._min_field_size)
            self._view.add_elemts([self._current, self._vec_field])

            nullvalue = self.qx.nullvalue

        elif which ==views_2D.UNORM_FIELD:

            self._current = (self.qx**2.+self.qy**2.)**.5/self.waterdepth
            self._view = WolfViews()

            ux = self.qx/self.waterdepth
            uy = self.qy/self.waterdepth

            self._vec_field = VectorField(ux.array, uy.array, self.qx.get_bounds(), self.qx.dx, self.qy.dy, minsize=self._min_field_size)
            self._view.add_elemts([self._current, self._vec_field])

            nullvalue = self.qx.nullvalue

        elif which ==views_2D.WL_U:

            self._current = self.waterdepth+self.top
            self._view = WolfViews()

            ux = self.qx/self.waterdepth
            uy = self.qy/self.waterdepth

            self._vec_field = VectorField(ux.array, uy.array, self.qx.get_bounds(), self.qx.dx, self.qy.dy, minsize=self._min_field_size)
            self._view.add_elemts([self._current, self._vec_field])

            nullvalue = self.waterdepth.nullvalue

        elif which ==views_2D.WL_Q:

            self._current = self.waterdepth+self.top
            self._view = WolfViews()

            self._vec_field = VectorField(self.qx.array, self.qy.array, self.qx.get_bounds(), self.qx.dx, self.qy.dy, minsize=self._min_field_size)

            self._view.add_elemts([self._current, self._vec_field])

            nullvalue = self.waterdepth.nullvalue

        elif which ==views_2D.WD_Q:

            self._current = self.waterdepth
            self._view = WolfViews()
            self._vec_field =VectorField(self.qx.array, self.qy.array, self.qx.get_bounds(), self.qx.dx, self.qy.dy, minsize=self._min_field_size)
            self._view.add_elemts([self._current, self._vec_field])

            nullvalue = self.waterdepth.nullvalue

        elif which ==views_2D.WD_U:

            self._current = self.waterdepth
            self._view = WolfViews()

            ux = self.qx/self.waterdepth
            uy = self.qy/self.waterdepth

            self._vec_field =VectorField(ux.array, uy.array, self.qx.get_bounds(), self.qx.dx, self.qy.dy, minsize=self._min_field_size)
            self._view.add_elemts([self._current, self._vec_field])

            nullvalue = self.waterdepth.nullvalue

        elif which ==views_2D.T_WL_Q:

            self._current = self.waterdepth+self.top
            self._view = WolfViews()

            self._vec_field =VectorField(self.qx.array, self.qy.array, self.qx.get_bounds(), self.qx.dx, self.qy.dy, minsize=self._min_field_size)
            self._view.add_elemts([self.top, self._current, self._vec_field])

            nullvalue = self.waterdepth.nullvalue

        elif which ==views_2D.T_WD_Q:

            self._current = self.waterdepth
            self.waterdepth.mypal.defaultblue_minmax(self.waterdepth.array)
            self._view = WolfViews()

            self._vec_field =VectorField(self.qx.array, self.qy.array, self.qx.get_bounds(), self.qx.dx, self.qy.dy, minsize=self._min_field_size)
            self._view.add_elemts([self.top, self._current, self._vec_field])

            nullvalue = self.waterdepth.nullvalue

        elif which ==views_2D.T_WD_U:

            self._current = self.waterdepth
            self.waterdepth.mypal.defaultblue_minmax(self.waterdepth.array)
            self._view = WolfViews()

            ux = self.qx/self.waterdepth
            uy = self.qy/self.waterdepth

            self._vec_field =VectorField(ux.array, uy.array, self.qx.get_bounds(), self.qx.dx, self.qy.dy, minsize=self._min_field_size)
            self._view.add_elemts([self.top, self._current, self._vec_field ])

            nullvalue = self.waterdepth.nullvalue

        elif which==views_2D.SHIELDS_NUMBER:
            if self.ShieldsNumber is None or self._force_update_shields:
                self.ShieldsNumber = self.get_shieldsnumber()
                self._force_update_shields = False
            self._current = self.ShieldsNumber

            nullvalue = self.waterdepth.nullvalue

        elif which==views_2D.CRITICAL_DIAMETER_SHIELDS:
            if self.critShields is None:
                self.critShields = self.get_critdiam(0)
            self._current = self.critShields

            nullvalue = self.waterdepth.nullvalue

        elif which==views_2D.CRITICAL_DIAMETER_IZBACH:
            if self.critIzbach is None:
                self.critIzbach = self.get_critdiam(1)
            self._current = self.critIzbach

            nullvalue = self.waterdepth.nullvalue

        elif which==views_2D.CRITICAL_DIAMETER_SUSPENSION_50:
            if self.critSusp50 is None:
                self.critSusp50 = self.get_critsusp(50)
            self._current = self.critSusp50

            nullvalue = self.waterdepth.nullvalue

        elif which==views_2D.CRITICAL_DIAMETER_SUSPENSION_100:
            if self.critSusp100 is None:
                self.critSusp100 = self.get_critsusp(100)
            self._current = self.critSusp100

            nullvalue = self.waterdepth.nullvalue


        self._current.linkedvec = self.linkedvec
        self._current.idx = self.idx
        self._current.nullvalue = nullvalue

    @property
    def min_field_size(self):
        return self._min_field_size

    @min_field_size.setter
    def min_field_size(self, value):
        self._min_field_size = value

    def get_norm_max(self):

        if self._which_current == views_2D.VECTOR_FIELD_Q:
            return (self._vec_field.min_size, self._vec_field.max_norm, np.max(self._current.array))
        elif self._which_current == views_2D.VECTOR_FIELD_U:
            return (self._vec_field.min_size, self._vec_field.max_norm, np.max(self._current.array))
        elif self._which_current == views_2D.QNORM_FIELD:
            return (self._vec_field.min_size, self._vec_field.max_norm, np.max(self._current.array))
        elif self._which_current == views_2D.UNORM_FIELD:
            return (self._vec_field.min_size, self._vec_field.max_norm, np.max(self._current.array))
        elif self._which_current == views_2D.WL_U:
            return (self._vec_field.min_size, self._vec_field.max_norm, np.max(((self.qx**2.+self.qy**2.)**.5/self.waterdepth).array))
        elif self._which_current == views_2D.WL_Q:
            return (self._vec_field.min_size, self._vec_field.max_norm, np.max(((self.qx**2.+self.qy**2.)**.5).array))
        elif self._which_current == views_2D.T_WL_Q:
            return (self._vec_field.min_size, self._vec_field.max_norm, np.max(((self.qx**2.+self.qy**2.)**.5).array))
        elif self._which_current == views_2D.T_WD_Q:
            return (self._vec_field.min_size, self._vec_field.max_norm, np.max(((self.qx**2.+self.qy**2.)**.5).array))
        elif self._which_current == views_2D.T_WD_U:
            return (self._vec_field.min_size, self._vec_field.max_norm, np.max(((self.qx**2.+self.qy**2.)**.5/self.waterdepth).array))

        return (0., 1.,1.)

    def update_zoom_2(self, newzoom):

        if self._vec_field is not None:
            self._vec_field.update_zoom_2(newzoom)

    def update_zoom_vectorfield(self,factor):

        if self._vec_field is not None:
            self._vec_field.update_zoom_factor(factor)

    def update_arrowpixelsize_vectorfield(self,factor):

        if self._vec_field is not None:
            self._vec_field.arrow_pixel_size += factor
            self._vec_field.arrow_pixel_size = max(1,self._vec_field.arrow_pixel_size)

    def update_pal(self, curpal:wolfpalette, graypal=None, bluepal=None):
        """
        Mise à jour de la palette

        :param curpal: palette courante
        :param graypal: palette grise
        :param bluepal: palette bleue
        """

        which = self._which_current

        self._current.mypal = curpal
        self._current.mypal.interval_cst = curpal.interval_cst
        self._current.rgb = curpal.get_rgba(self._current.array)
        self._current.rgb[self._current.array.mask] = [1., 1., 1., 1.]

        if which == 'wd_u':
            self._view.pals = [bluepal,curpal]
        elif which =='t_wl_q':
            self._view.pals = [graypal,curpal,None]
        elif which =='t_wd_q':
            self._view.pals = [graypal,bluepal,None]
        elif which =='t_wd_u':
            self._view.pals = [graypal,bluepal,None]

    def get_critdiam(self, which:int) -> WolfArray:
        """
        Calcul du dimètre critique

        :param which : 0 = Shields ; 1 = Izbach
        """

        def compute(which) -> WolfArray:
            ij = np.argwhere(self.waterdepth.array>0.)

            diamcrit = WolfArray(mold=self.waterdepth)
            qnorm = (self.qx**2.+self.qy**2.)**.5
            qnorm.array.mask=self.waterdepth.array.mask

            if which==0:
                diam = np.asarray([get_d_cr(qnorm.array[i,j],self.waterdepth.array[i,j],1./self.rough_n.array[i,j])[which] for i,j in ij])
            else:
                diam = np.asarray([izbach_d_cr(qnorm.array[i,j],self.waterdepth.array[i,j]) for i,j in ij])

            diamcrit.array[ij[:,0],ij[:,1]] = diam

            return diamcrit

        logging.info(_('Computing critical diameters'))

        diamcrit = compute(which)

        logging.info(_('End of computing critical diameters'))

        return diamcrit

    def get_shieldsnumber(self) -> WolfArray:
        """
        Calcul du nombre de Shields
        """

        def compute() -> WolfArray:

            ij = np.argwhere(self.waterdepth.array>0.)

            shields = WolfArray(mold=self.waterdepth)
            qnorm = (self.qx**2.+self.qy**2.)**.5
            qnorm.array.mask=self.waterdepth.array.mask

            _shields = np.asarray([get_Shields_2D_Manning(self.sediment_density,
                                                     self.sediment_diameter,
                                                     qnorm.array[i,j],
                                                     self.waterdepth.array[i,j],
                                                     self.rough_n.array.data[i,j]) for i,j in ij])

            shields.array[ij[:,0],ij[:,1]] = _shields

            return shields

        logging.info(_('Computing critical diameters'))
        shields = compute()
        logging.info(_('End of computing critical diameters'))

        return shields

    def get_critsusp(self, which:int = 50):

        logging.info(_('Computing critical diameters'))
        ij = np.argwhere(self.waterdepth.array>0.)

        diamcrit = WolfArray(mold=self.waterdepth)
        qnorm = (self.qx**2.+self.qy**2.)**.5
        qnorm.array.mask=self.waterdepth.array.mask

        diam = np.asarray([get_d_cr_susp(qnorm.array[i,j],self.waterdepth.array[i,j],1./self.rough_n.array[i,j],which=which) for i,j in ij])

        diamcrit.array[ij[:,0],ij[:,1]] = diam

    def plot(self, sx=None, sy=None, xmin=None, ymin=None, xmax=None, ymax=None):
        """ Affichage des résultats """

        if self._which_current in VIEWS_VECTOR_FIELD:
            self._vec_field.plot(sx, sy,xmin,ymin,xmax,ymax)
        elif self._which_current in VIEWS_COMPLEX:
            self._view.plot(sx, sy,xmin,ymin,xmax,ymax)
        else:
            self._current.plot(sx, sy,xmin,ymin,xmax,ymax)

    def get_values_labels(self, i:int, j:int):
        """ Récupération des valeurs et labels pour affichage """

        which = self._which_current

        mylab = [which.value]
        myval = [self._current.array[i,j]]

        if which in VIEWS_VECTOR_FIELD:
            if which == views_2D.VECTOR_FIELD_Q:
                mylab = [views_2D.QX.value,
                         views_2D.QY.value,
                         views_2D.QNORM.value]

                h  = self.waterdepth.array[i,j]
                qx = self.qx.array[i,j]
                qy = self.qy.array[i,j]
                qnorm = (qx**2.+qy**2.)**.5

                myval = [qx,
                         qy,
                         qnorm]

            elif which == views_2D.VECTOR_FIELD_U:
                mylab = [views_2D.UX.value,
                         views_2D.UY.value,
                         views_2D.UNORM.value]

                h  = self.waterdepth.array[i,j]
                qx = self.qx.array[i,j]
                qy = self.qy.array[i,j]

                ux = qx/h
                uy = qy/h

                unorm = (ux**2.+uy**2.)**.5

                myval = [ux,
                         uy,
                         unorm]

        if which in VIEWS_COMPLEX:

            mylab = [views_2D.TOPOGRAPHY.value,
                     views_2D.WATERDEPTH.value,
                     views_2D.WATERLEVEL.value,
                     views_2D.QX.value,
                     views_2D.QY.value,
                     views_2D.QNORM.value,
                     views_2D.UX.value,
                     views_2D.UY.value,
                     views_2D.UNORM.value,
                     views_2D.FROUDE.value]

            top = self.top.array[i,j]
            h  = self.waterdepth.array[i,j]

            sl = h+top

            qx = self.qx.array[i,j]
            qy = self.qy.array[i,j]
            qnorm = (qx**2.+qy**2.)**.5

            ux = qx/h
            uy = qy/h

            unorm = (ux**2.+uy**2.)**.5

            fr = unorm/(9.81*h)**.5
            myval = [top,
                     h,
                     sl,
                     qx,
                     qy,
                     qnorm,
                     ux,
                     uy,
                     unorm,
                     fr]

        return myval,mylab

class Wolfresults_2D(Element_To_Draw):
    """
    Manipulation des résultats d'un modèle WOLF2D en multiblocs

    La classe hérite de 'Element_To_Draw' afin d'être sûr de disposer des informations pour un éventuel affichage dans un viewer 'WolfMapViewer'

    ATTENTION :
     - la classe contient un dictionnaire 'myblocks' d'objets 'OneWolfResult'
     - les clés du dictionnaire sont de type 'block1', 'block2'... 'blockn' --> voir fonction 'getkeyblock'
     - les entrées ne sont PAS des matrices multiblocks 'WolfArrayMB' mais une classe 'OneWolfResult' contient plusieurs matrices pour chaque type de résultat (water depth, dischargeX, dischargeY, ...)

     - la classe se comporte donc un peu comme une généralisation d'une matrice 'WolfArrayMB' mais il ne s'agit pas d'une extension par polymorphisme
     - on retrouve cependant plusieurs routines similaires afin de faciliter l'intégration dans un viewer WX
    """

    myblocks:dict[str, OneWolfResult]
    head_blocks:dict[str, header_wolf]

    myparam:prev_parameters_simul
    myblocfile:bloc_file
    mymnap:WolfArrayMNAP

    def __init__(self,
                 fname:str = None,
                 mold = None, eps=0.,
                 idx: str = '',
                 plotted: bool = True,
                 mapviewer=None,
                 need_for_wx: bool = False,
                 loader=None) -> None:
        """
        Initialisation

        :param fname : nom du fichier de résultats
        :param mold : objet 'WolfArray' servant de moule pour les résultats
        :param eps : valeur de l'epsilon pour le masquage des données
        :param idx : identifiant de l'objet
        :param plotted : si True alors l'objet est prêt à être affiché
        :param mapviewer : objet 'WolfMapViewer' pour l'affichage
        :param need_for_wx : si True alors l'objet abesoin d'une app WX. Si elle n'existe pas, génération d'une erreur !
        :param loader : if True then we'll use this function rather than classic one.
                        This param was introduced because one cannot guess if one's loading GPU results
                        by just looking at the filename (GPU results come in directories).
        """
        super().__init__(idx, plotted, mapviewer, need_for_wx)

        self.filename=""
        self.filenamegen=self.filename

        self.linkedvec = None # vecteur d'exclusion de données

        self.epsilon = eps
        self._epsilon_default = self.epsilon

        self.loaded=True
        self.current_result = -1
        self.mypal = wolfpalette(None,'Colors')
        self.mypal.default16()
        self.mypal.automatic = True

        self.palgray = None
        self.palblue = None

        self.nbnotnull=99999

        self._which_current_view = views_2D.WATERDEPTH # _('Water depth [m]')

        self.translx=0.
        self.transly=0.

        self.head_blocks={}

        if fname is not None:

            if loader is not None:
                loader(fname)
            else:
                parts=splitext(fname)
                if len(parts)>1:
                    self.filename = parts[0]
                else:
                    self.filename = fname

                self.filenamegen=self.filename

                if exists(self.filename + '.trl'):
                    with open(self.filename + '.trl') as f:
                        trl=f.read().splitlines()
                        self.translx=float(trl[1])
                        self.transly=float(trl[2])

                self.myblocks={}
                self.read_param_simul()

                if exists(self.filename+'.head') or exists(join(dirname(self.filename),'bloc1.head')):
                    wolfpy.r2d_init(self.filename.ljust(255).encode('ansi'))
                    nb_blocks = wolfpy.r2d_nbblocks()

                    for i in range(nb_blocks):
                        curblock = OneWolfResult(i, parent=self)
                        self.myblocks[getkeyblock(i)] = curblock

                        nbx,nby,dx,dy,ox,oy,tx,ty = wolfpy.r2d_hblock(i+1)

                        curhead = self.head_blocks[getkeyblock(i)]=header_wolf()
                        curhead.nbx = nbx
                        curhead.nby = nby
                        curhead.origx = ox
                        curhead.origy = oy
                        curhead.dx = dx
                        curhead.dy = dy
                        curhead.translx = self.translx
                        curhead.transly = self.transly

                        self.myblocks[getkeyblock(i)].waterdepth.dx = dx
                        self.myblocks[getkeyblock(i)].waterdepth.dy = dy
                        self.myblocks[getkeyblock(i)].waterdepth.nbx = nbx
                        self.myblocks[getkeyblock(i)].waterdepth.nby = nby
                        self.myblocks[getkeyblock(i)].waterdepth.origx = ox
                        self.myblocks[getkeyblock(i)].waterdepth.origy = oy
                        self.myblocks[getkeyblock(i)].waterdepth.translx = self.translx
                        self.myblocks[getkeyblock(i)].waterdepth.transly = self.transly

                        self.myblocks[getkeyblock(i)].top.dx = dx
                        self.myblocks[getkeyblock(i)].top.dy = dy
                        self.myblocks[getkeyblock(i)].top.nbx = nbx
                        self.myblocks[getkeyblock(i)].top.nby = nby
                        self.myblocks[getkeyblock(i)].top.origx = ox
                        self.myblocks[getkeyblock(i)].top.origy = oy
                        self.myblocks[getkeyblock(i)].top.translx = self.translx
                        self.myblocks[getkeyblock(i)].top.transly = self.transly

                        self.myblocks[getkeyblock(i)].qx.dx = dx
                        self.myblocks[getkeyblock(i)].qx.dy = dy
                        self.myblocks[getkeyblock(i)].qx.nbx = nbx
                        self.myblocks[getkeyblock(i)].qx.nby = nby
                        self.myblocks[getkeyblock(i)].qx.origx = ox
                        self.myblocks[getkeyblock(i)].qx.origy = oy
                        self.myblocks[getkeyblock(i)].qx.translx = self.translx
                        self.myblocks[getkeyblock(i)].qx.transly = self.transly

                        self.myblocks[getkeyblock(i)].qy.dx = dx
                        self.myblocks[getkeyblock(i)].qy.dy = dy
                        self.myblocks[getkeyblock(i)].qy.nbx = nbx
                        self.myblocks[getkeyblock(i)].qy.nby = nby
                        self.myblocks[getkeyblock(i)].qy.origx = ox
                        self.myblocks[getkeyblock(i)].qy.origy = oy
                        self.myblocks[getkeyblock(i)].qy.translx = self.translx
                        self.myblocks[getkeyblock(i)].qy.transly = self.transly

                        self.myblocks[getkeyblock(i)].rough_n.dx = dx
                        self.myblocks[getkeyblock(i)].rough_n.dy = dy
                        self.myblocks[getkeyblock(i)].rough_n.nbx = nbx
                        self.myblocks[getkeyblock(i)].rough_n.nby = nby
                        self.myblocks[getkeyblock(i)].rough_n.origx = ox
                        self.myblocks[getkeyblock(i)].rough_n.origy = oy
                        self.myblocks[getkeyblock(i)].rough_n.translx = self.translx
                        self.myblocks[getkeyblock(i)].rough_n.transly = self.transly

                else:
                    nb_blocks = self.myblocfile.nb_blocks

                    for i in range(nb_blocks):
                        #print(f"Reading block {getkeyblock(i)}")
                        curblock = OneWolfResult(i, parent = self)
                        self.myblocks[getkeyblock(i)] = curblock
                        curblock.waterdepth.set_header(self.mymnap.head_blocks[getkeyblock(i)])
                        curblock.top.set_header(self.mymnap.head_blocks[getkeyblock(i)])
                        curblock.qx.set_header(self.mymnap.head_blocks[getkeyblock(i)])
                        curblock.qy.set_header(self.mymnap.head_blocks[getkeyblock(i)])
                        curblock.rough_n.set_header(self.mymnap.head_blocks[getkeyblock(i)])

                self.allocate_ressources()
                self.read_topography()
                self.read_ini_mb()

                self.loaded_rough = False
        else:
            self.myblocks={}

        self.nbx = 1
        self.nby = 1

        ox=9999999.
        oy=9999999.
        ex=-9999999.
        ey=-9999999.
        for curblock in self.myblocks.values():
            curhead=curblock.waterdepth.get_header(False)
            ox=min(ox,curhead.origx)
            oy=min(oy,curhead.origy)
            ex=max(ex,curhead.origx+float(curhead.nbx)*curhead.dx)
            ey=max(ey,curhead.origy+float(curhead.nby)*curhead.dy)
        self.dx = ex-ox
        self.dy = ey-oy
        self.origx = ox
        self.origy = oy

        self._nb_results = None
        self.timesteps = []
        self.times = []

        self.properties:Props_Res_2D = None
        self.set_properties()

        self.mngselection = SelectionData(self)
        self.mngselection.dx, self.mngselection.dy = self[0].dx, self[0].dy
        self.myops = None

    def get_bounds(self, abs=True):
        """
        Return bounds in coordinates

        :param abs = if True, add translation to (x, y) (coordinate to global space)
        :return : tuple of two lists of two floats - ([xmin, xmax],[ymin, ymax])
        """

        if abs:
            return ([self.origx + self.translx, self.origx + self.translx + float(self.nbx) * self.dx],
                    [self.origy + self.transly, self.origy + self.transly + float(self.nby) * self.dy])
        else:
            return ([self.origx, self.origx + float(self.nbx) * self.dx],
                    [self.origy, self.origy + float(self.nby) * self.dy])

    def check_bounds_ij(self, i:int, j:int):
        """Check if i and j are inside the array bounds"""

        x,y = self.get_xy_from_ij(i,j)
        return self.check_bounds_xy(x,y)

    def check_bounds_xy(self, x:float, y:float):
        """Check if i and j are inside the array bounds"""

        (xmin, xmax), (ymin, ymax) = self.get_bounds()

        return x>=xmin and x<=xmax and y>=ymin and y<=ymax

    @property
    def nullvalue(self):
        """ Get nullvalue from the first block """

        return self[0].nullvalue

    @nullvalue.setter
    def nullvalue(self, value):
        """ Set nullvalue for all blocks """

        for i in range(self.nb_blocks):
            self[i].nullvalue = value

    @property
    def alpha(self):
        return self[0].alpha

    @alpha.setter
    def alpha(self, value:float):
        for i in range(self.nb_blocks):
            self[i].alpha = value

    @property
    def shading(self):
        return self[0].shading

    @shading.setter
    def shading(self, value:bool):
        for i in range(self.nb_blocks):
            self[i].shading = value

    @property
    def altitudehill(self):
        return self[0].altitudehill

    @altitudehill.setter
    def altitudehill(self, value:bool):
        for i in range(self.nb_blocks):
            self[i].altitudehill = value

    @property
    def azimuthhill(self):
        return self[0].azimuthhill

    @azimuthhill.setter
    def azimuthhill(self, value:bool):
        for i in range(self.nb_blocks):
            self[i].azimuthhill = value

    @property
    def shaded(self):
        return self[0].shaded

    def show_properties(self):
        """ Affichage des propriétés de la matrice """

        if self.wx_exists and self.properties is not None:
            self.properties.SetTitle(_('Properties : ') + self.idx)
            self.properties.Show()

    def set_properties(self):
        """
        Create :
           - Props_Res_2D (GUI) if mapviewer is not None
        """

        if self.wx_exists and self.mapviewer is not None:
            self.properties = Props_Res_2D(self, self.mapviewer)
            self.properties.Hide()
        else:
            self.properties = None

    def get_header(self, abs=True) -> header_wolf:
        """ Récupération de l'entête de la matrice """

        curhead = header_wolf()

        curhead.origx = self.origx
        curhead.origy = self.origy

        curhead.dx = self.dx
        curhead.dy = self.dy

        curhead.nbx = self.nbx
        curhead.nby = self.nby

        curhead.translx = self.translx
        curhead.transly = self.transly

        curhead.head_blocks = self.head_blocks.copy()

        if abs:
            curhead.origx += curhead.translx
            curhead.origy += curhead.transly
            curhead.origz += curhead.translz

            curhead.translx = 0.
            curhead.transly = 0.
            curhead.translz = 0.

        return curhead

    def __getitem__(self, block_key:Union[int,str]) -> WolfArray:
        """Access a block's array of this multi-blocks Result"""

        if isinstance(block_key,int):
            _key = getkeyblock(block_key)
        else:
            _key = block_key

        if _key in self.myblocks.keys():
            return self.myblocks[_key].current
        else:
            return None

    """ Iterator """
    def __iter__(self):
        self._iter = 0
        return self[self._iter]

    def __next__(self):
        self._iter += 1
        return self[self._iter]
    """ End Iterator """

    def as_WolfArray(self, copyarray:bool=True) -> Union[WolfArray, WolfArrayMB]:
        """Récupération d'une matrice MB ou Mono sur base du résultat courant"""

        if self.nb_blocks>1:

            retarray = WolfArrayMB()
            retarray.set_header(self.get_header())
            for i in range(self.nb_blocks):
                retarray.add_block(self[i], copyarray=copyarray)
        else:
            if copyarray :
                retarray = WolfArray(mold=self[0])
            else:
                retarray = self[0]

        return retarray

    @property
    def nb_blocks(self):
        """ Nombre de blocs """

        return len(self.myblocks)

    @property
    def sediment_diameter(self):
        try:
            return self.myblocks[getkeyblock(0)].sediment_diameter
        except:
            return None

    @sediment_diameter.setter
    def sediment_diameter(self, value:float):
        for curblock in self.myblocks.values():
            force = curblock.sediment_diameter != value
            curblock.sediment_diameter = value
        # forcer la MAJ si nécessaire
        if self.get_currentview() == views_2D.SHIELDS_NUMBER and force:
            self.set_currentview()

    @property
    def sediment_density(self):
        try:
            return self.myblocks[getkeyblock(0)].sediment_density
        except:
            return None

    @sediment_density.setter
    def sediment_density(self, value:float):
        for curblock in self.myblocks.values():
            force = curblock.sediment_density != value
            curblock.sediment_density = value
        # forcer la MAJ si nécessaire
        if self.get_currentview() == views_2D.SHIELDS_NUMBER and force:
            self.set_currentview()

    def _gpu_loader(self, fname:str):

        # 2D GPU
        nb_blocks = 1
        self.myblocks = {}
        curblock = OneWolfResult(0, parent=self)
        self.myblocks[getkeyblock(0)] = curblock

        if exists(join(dirname(fname), 'simul.top')):
            curblock.top = WolfArray(join(dirname(fname), 'simul.top'), nullvalue=99999.)
            curblock.waterdepth = WolfArray(join(dirname(fname), 'simul.hbin'))
            curblock.qx = WolfArray(join(dirname(fname), 'simul.qxbin'))
            curblock.qy = WolfArray(join(dirname(fname), 'simul.qybin'))
            curblock.rough_n = WolfArray(join(dirname(fname), 'simul.frot'))
        elif exists(join(dirname(fname), 'bathymetry.npy')):
            curblock.top = WolfArray(join(dirname(fname), 'bathymetry.npy'), nullvalue=99999.)
            curblock.waterdepth = WolfArray(join(dirname(fname), 'h.npy'))
            curblock.qx = WolfArray(join(dirname(fname), 'qx.npy'))
            curblock.qy = WolfArray(join(dirname(fname), 'qy.npy'))
            curblock.rough_n = WolfArray(join(dirname(fname), 'manning.npy'))

            if exists(join(dirname(fname), 'parameters.json')):
                import json
                with open(join(dirname(fname), 'parameters.json'), 'r') as fp:

                    params = json.load(fp)

                    try:
                        curblock.top.dx = params["parameters"]["dx"]
                        curblock.top.dy = params["parameters"]["dy"]
                    except:
                        logging.error(_('No spatial resolution (dx,dy) in parameters.json -- Results will not be shown in viewer'))

                    try:
                        curblock.top.origx = params["parameters"]["base_coord_x"]
                        curblock.top.origy = params["parameters"]["base_coord_y"]
                    except:
                        logging.error(_('No spatial position (base_coord_x,base_coord_y) in parameters.json -- Results will not be spatially based'))

        self.loaded_rough = True

        to_check =[curblock.waterdepth, curblock.qx, curblock.qy, curblock.rough_n]
        check = False
        for curarray in to_check:
            check |= curarray.dx != curblock.top.dx
            check |= curarray.dy != curblock.top.dy
            check |= curarray.origx != curblock.top.origx
            check |= curarray.origy != curblock.top.origy
            check |= curarray.translx != curblock.top.translx
            check |= curarray.transly != curblock.top.transly

        if check:
            if exists(join(dirname(fname), 'simul.top')):
                logging.error(_("Inconsistent header file in .top, .qxbin, .qybin or .frot files"))
                logging.error(_("Forcing information into memory from the .top file -- May corrupt spatial positionning -- Please check your data !"))

            for curarray in to_check:
                curarray.dx    = curblock.top.dx
                curarray.dy    = curblock.top.dy
                curarray.origx = curblock.top.origx
                curarray.origy = curblock.top.origy
                curarray.translx = curblock.top.translx
                curarray.transly = curblock.top.transly

        if exists(join(dirname(fname), 'simul.trl')):
            with open(join(dirname(fname), 'simul.trl')) as f:
                trl=f.read().splitlines()
                self.translx=float(trl[1])
                self.transly=float(trl[2])

        curblock.set_current(views_2D.WATERDEPTH)

        self.myparam = None
        self.mymnap = None
        self.myblocfile = None

    def load_default_colormap(self, which:str):
        """
        Lecture d'une palette disponible dans le répertoire "models"
        """

        dir  = join(dirname(__file__), 'models')

        if exists(join(dir, which + '.pal')):
            try:
                self.mypal.readfile(join(dir, which + '.pal'))
                if which.endswith('_cst'):
                    self.mypal.interval_cst = True
                else:
                    self.mypal.interval_cst = False
            except:
                return
        else:
            logging.warning(_('Bad file - {}'.format(which)))
            return

    def get_times_steps(self, nb:int = None):
        """
        Récupération des temps réels et des pas de calcul de chaque résultat sur disque

        :param nb : nombre de résultats à lire
        """
        if nb is None:
            if self._nb_results is None:
                nb = self.get_nbresults()
            else:
                nb = self._nb_results
        if nb == 0:
            self.times, self.timesteps = [],[]
        else:
            wolfpy.r2d_init(self.filename.ljust(255).encode('ansi'))
            self.times, self.timesteps = wolfpy.get_times_steps(nb)

        return self.times, self.timesteps

    def find_minmax(self,update=False):
        """Find spatial bounds"""
        self.xmin = self.origx + self.translx
        self.xmax = self.origx + self.translx + float(self.nbx) * self.dx
        self.ymin = self.origy + self.transly
        self.ymax = self.origy + self.transly + float(self.nby) * self.dy

    def get_norm_max(self):
        """
        Retourne la norme maximale du champ de débit ou de vitesse
        """
        nmax=[]
        for curblock in self.myblocks.values():
            nmax.append(curblock.get_norm_max())

        return nmax

    def update_zoom_2(self, newzoom):

            for curblock in self.myblocks.values():

                curblock.update_zoom_2(newzoom)

    def update_zoom_factor(self):

        if self._which_current_view in VIEWS_VECTOR_FIELD or self._which_current_view in VIEWS_COMPLEX:
            nmax = self.get_norm_max()

            maxq        = np.max(np.asarray([cur[2] for cur in nmax]))
            maxq_rel    = np.max(np.asarray([cur[1] for cur in nmax]))
            size_min_rel= np.min(np.asarray([cur[0] for cur in nmax]))

            dmin = self.get_dxdy_min()

            for idx, curblock in enumerate(self.myblocks.values()):

                smin   = nmax[idx][0]
                qmax_r = nmax[idx][1]
                qmax   = nmax[idx][2]

                curblock.update_zoom_vectorfield(qmax / maxq * (1.-size_min_rel) + size_min_rel * 1.)

    def update_arrowpixelsize_vectorfield(self,factor):
        for curblock in self.myblocks.values():
            curblock.update_arrowpixelsize_vectorfield(factor)

    def get_dxdy_min(self):
        """Return the minimal size into blocks"""
        dmin=99999
        for curblock in self.myblocks.values():
            dmin = min(dmin,curblock.waterdepth.dx)
            dmin = min(dmin,curblock.waterdepth.dy)

        return dmin

    def get_dxdy_max(self):
        """Return the maximal size into blocks"""
        dmax=-99999
        for curblock in self.myblocks.values():
            dmax = max(dmax,curblock.waterdepth.dx)
            dmax = max(dmax,curblock.waterdepth.dy)

        return dmax

    def read_param_simul(self):
        """Read simulation parameters from files"""
        self.myparam = prev_parameters_simul(self)
        self.myparam.read_file(self.filename)

        self.myblocfile = bloc_file(self)
        self.myblocfile.read_file()

        self.mymnap = WolfArrayMNAP(self.filename)

    def get_currentview(self):
        """Return the current view"""
        return self._which_current_view

    def filter_inundation(self, eps:float=None, linkedvec:vector = None):
        """
        Apply filtering on array

        :param eps : mask data below eps
        :param linkedvec : mask data outside linkedvec
        """

        if eps is not None:
            self.epsilon = eps
        if linkedvec is not None:
            self.linkedvec = linkedvec

        self.mimic_plotdata()

        for curblock in self.myblocks.values():
            curblock.filter_inundation()

    def set_currentview(self, which=None, force_wx=False, force_updatepal:bool=False):
        """
        Set the current view --> see 'views_2D' for supported values

        :param which : view to set
        :param force_wx : if True, a wx dialog will be shown to set the minimum size of the vector field
        :param force_updatepal : if True, the palette will be updated

        """

        if which is None:
            which = self._which_current_view

        if self.wx_exists and force_wx:
            if which in VIEWS_VECTOR_FIELD or which in VIEWS_COMPLEX:
                dlg = wx.TextEntryDialog(None,_('Minimum size of the vector field (0 --> 1) -- 1 == equal size'),_('Size'), str(self.myblocks[getkeyblock(0)].min_field_size))

                ret = dlg.ShowModal()
                minsize = max(0,min(1,float(dlg.GetValue())))
                dlg.Destroy()
                for curblock in self.myblocks.values():
                    curblock.min_field_size = minsize

        if which in views_2D:
            # self.delete_lists()

            self._which_current_view = which

            self.plotting=True
            self.mimic_plotdata()

            if which in VIEWS_SEDIMENTARY:

                if not self.loaded_rough:
                    self.read_roughness_param()

            for curblock in self.myblocks.values():
                curblock.set_current(which)

            # Epsilon is set to 0. by default
            #  OK for all views except QX, QY, UX, UY
            if which in [views_2D.QX,
                         views_2D.QY,
                         views_2D.UX,
                         views_2D.UY]:
                self.epsilon = -999999.
            else:
                self.epsilon = self._epsilon_default

            self.filter_inundation()

            if which in VIEWS_VECTOR_FIELD or which in VIEWS_COMPLEX:
                self.update_zoom_factor()

            if force_updatepal:
                self.mypal.automatic = True
                self.updatepalette()
            else:
                self.link_palette()

            self.plotting=False
            self.mimic_plotdata()

            if self.mapviewer is not None:
                self.mapviewer.Refresh()

    def allocate_ressources(self):
        """Allocation de l'espace mémoire utile pour le stockage des résultats de chaque bloc"""
        for curblock in self.myblocks.values():
            curblock.waterdepth.allocate_ressources()
            curblock.top.allocate_ressources()
            curblock.qx.allocate_ressources()
            curblock.qy.allocate_ressources()

    def read_topography(self):
        """Lecture de la topographie de modélisation"""
        if exists(self.filename.strip() + '.topini'):
            with open(self.filename.strip() + '.topini','rb') as f:
                for i in range(self.nb_blocks):
                    nbx=self.myblocks[getkeyblock(i)].top.nbx
                    nby=self.myblocks[getkeyblock(i)].top.nby
                    nbbytes=nbx*nby*4
                    self.myblocks[getkeyblock(i)].top.array = ma.masked_equal(np.frombuffer(f.read(nbbytes),dtype=np.float32),0.)
                    self.myblocks[getkeyblock(i)].top.array = self.myblocks[getkeyblock(i)].top.array.reshape(nbx,nby,order='F')

    def read_ini_mb(self):
        """Lecture des conditions initiales"""
        if exists(self.filename.strip() + '.hbinb'):
            with open(self.filename.strip() + '.hbinb','rb') as f:
                for i in range(self.nb_blocks):
                    nbx=self.myblocks[getkeyblock(i)].waterdepth.nbx
                    nby=self.myblocks[getkeyblock(i)].waterdepth.nby
                    nbbytes=nbx*nby*4
                    self.myblocks[getkeyblock(i)].waterdepth.array = ma.masked_equal(np.frombuffer(f.read(nbbytes),dtype=np.float32),0.)
                    self.myblocks[getkeyblock(i)].waterdepth.array = self.myblocks[getkeyblock(i)].waterdepth.array.reshape(nbx,nby,order='F')

        if exists(self.filename.strip() + '.qxbinb'):
            with open(self.filename.strip() + '.qxbinb','rb') as f:
                for i in range(self.nb_blocks):
                    nbx=self.myblocks[getkeyblock(i)].qx.nbx
                    nby=self.myblocks[getkeyblock(i)].qx.nby
                    nbbytes=nbx*nby*4
                    self.myblocks[getkeyblock(i)].qx.array = ma.masked_equal(np.frombuffer(f.read(nbbytes),dtype=np.float32),0.)
                    self.myblocks[getkeyblock(i)].qx.array = self.myblocks[getkeyblock(i)].qx.array.reshape(nbx,nby,order='F')

        if exists(self.filename.strip() + '.qybinb'):
            with open(self.filename.strip() + '.qybinb','rb') as f:
                for i in range(self.nb_blocks):
                    nbx=self.myblocks[getkeyblock(i)].qy.nbx
                    nby=self.myblocks[getkeyblock(i)].qy.nby
                    nbbytes=nbx*nby*4
                    self.myblocks[getkeyblock(i)].qy.array = ma.masked_equal(np.frombuffer(f.read(nbbytes),dtype=np.float32),0.)
                    self.myblocks[getkeyblock(i)].qy.array = self.myblocks[getkeyblock(i)].qy.array.reshape(nbx,nby,order='F')

    def read_roughness_param(self):
        """Lecture du frottement de modélisation"""
        with open(self.filename.strip() + '.frotini','rb') as f:
            for i in range(self.nb_blocks):
                nbx=self.myblocks[getkeyblock(i)].rough_n.nbx
                nby=self.myblocks[getkeyblock(i)].rough_n.nby
                nbbytes=nbx*nby*4
                self.myblocks[getkeyblock(i)].rough_n.array = ma.masked_equal(np.frombuffer(f.read(nbbytes),dtype=np.float32),0.)
                self.myblocks[getkeyblock(i)].rough_n.array = self.myblocks[getkeyblock(i)].rough_n.array.reshape(nbx,nby,order='F')
        self.loaded_rough = True

    def get_nbresults(self, force_update_timessteps=True):
        """Récupération du nombre de pas sauvegardés --> utilisation de la librairie Fortran"""

        if exists(self.filename+'.head'):
            wolfpy.r2d_init(self.filename.ljust(255).encode('ansi'))
            nb = wolfpy.r2d_getnbresults()
            self._nb_results = nb

            if force_update_timessteps:
                self.get_times_steps(nb)
            return nb
        else:
            return 1

    def read_oneblockresult_withoutmask(self, which_step:int=-1,whichblock:int=-1):
        """
        Lecture d'un résultat pour un bloc spécifique --> utilisation de la librairie Fortran

        :param which_step : timestep ; 0-based; -1 == last one
        :param whichblock : block index
        """
        which_step = self._sanitize_result_step(which_step)

        if whichblock!=-1:
            block = self.myblocks[getkeyblock(whichblock,False)]
            nbx = block.waterdepth.nbx
            nby = block.waterdepth.nby

            # Fortran is 1-based --> which_step+1
            block.waterdepth.array, block.qx.array, block.qy.array = wolfpy.r2d_getresults(which_step+1, nbx, nby, whichblock)
            block.k.array, block.eps.array = wolfpy.r2d_getturbresults(which_step+1, nbx, nby, whichblock)
            block._force_update_shields = True

    def read_oneblockresult(self, which_step:int=-1, whichblock:int=-1):
        """
        Lecture d'un résultat pour un bloc spécifique et application d'un masque sur base d'nu epsilon de hauteur d'eau

        which_step: result number to read ; 0-based; -1 == last one
        whichblock : block index ; 1-based
        """

        which_step = self._sanitize_result_step(which_step)

        if whichblock!=-1:

            self.read_oneblockresult_withoutmask(which_step, whichblock)

            if self.epsilon > 0.:
                self.myblocks[getkeyblock(whichblock,False)].waterdepth.array=ma.masked_less_equal(self.myblocks[getkeyblock(whichblock,False)].waterdepth.array,self.epsilon)
            else:
                self.myblocks[getkeyblock(whichblock,False)].waterdepth.array=ma.masked_equal(self.myblocks[getkeyblock(whichblock,False)].waterdepth.array,0.)

            self.myblocks[getkeyblock(whichblock,False)].qx.array=ma.masked_where(self.myblocks[getkeyblock(whichblock,False)].waterdepth.array.mask,self.myblocks[getkeyblock(whichblock,False)].qx.array)
            self.myblocks[getkeyblock(whichblock,False)].qy.array=ma.masked_where(self.myblocks[getkeyblock(whichblock,False)].waterdepth.array.mask,self.myblocks[getkeyblock(whichblock,False)].qy.array)

            self.myblocks[getkeyblock(whichblock,False)].k.array=ma.masked_where(self.myblocks[getkeyblock(whichblock,False)].waterdepth.array.mask,self.myblocks[getkeyblock(whichblock,False)].k.array)
            self.myblocks[getkeyblock(whichblock,False)].eps.array=ma.masked_where(self.myblocks[getkeyblock(whichblock,False)].waterdepth.array.mask,self.myblocks[getkeyblock(whichblock,False)].eps.array)

            self.myblocks[getkeyblock(whichblock,False)].waterdepth.count()
            self.myblocks[getkeyblock(whichblock,False)].qx.count()
            self.myblocks[getkeyblock(whichblock,False)].qy.count()
            self.myblocks[getkeyblock(whichblock,False)].k.count()
            self.myblocks[getkeyblock(whichblock,False)].eps.count()

            self.myblocks[getkeyblock(whichblock,False)].waterdepth.set_nullvalue_in_mask()
            self.myblocks[getkeyblock(whichblock,False)].qx.set_nullvalue_in_mask()
            self.myblocks[getkeyblock(whichblock,False)].qy.set_nullvalue_in_mask()
            self.myblocks[getkeyblock(whichblock,False)].k.set_nullvalue_in_mask()
            self.myblocks[getkeyblock(whichblock,False)].eps.set_nullvalue_in_mask()

    def read_oneresult(self, which:int=-1):
        """
        Lecture d'un pas de sauvegarde

        which: result number to read; 0-based; -1 == last one
        """

        which = self._sanitize_result_step(which)

        if exists(self.filename+'.head'):
            logging.info(_('Reading from results - step :{}'.format(which+1)))
            wolfpy.r2d_init(self.filename.ljust(255).encode('ansi'))
            for i in range(self.nb_blocks):
                self.read_oneblockresult(which, i+1)
        else:
            logging.info(_('No ".head" file --> Initial Conditions'))

        self.current_result = which
        self.loaded=True

    def read_next(self):
        """
        Lecture du pas suivant
        """
        self.current_result += 1
        self._update_result_view()

    def _sanitize_result_step(self, which_step:int=-1):
        """ Sanitize result step index -- 0-based """
        nb = self.get_nbresults()
        while which_step<0:
            which_step += nb
        which_step = min(nb-1, which_step)
        which_step = max(0, which_step)

        return which_step

    def _update_result_view(self):

        self.current_result = self._sanitize_result_step(self.current_result)

        if exists(self.filename+'.head'):

            logging.info(_('Reading result step :{}'.format(self.current_result)))
            wolfpy.r2d_init(self.filename.ljust(255).encode('ansi'))

            for i in range(self.nb_blocks):
                self.read_oneblockresult(self.current_result, i+1)
        else:
            logging.info(_('No ".head" file --> Initial Conditions'))

        self.loaded=True

    def read_previous(self):
        """
        Lecture du pas suivant
        """
        # if self.current_result > 0:
        self.current_result -= 1
        self._update_result_view()

    def get_h_for_block(self, block: Union[int, str]) -> WolfArray:
        """
        Retourne la matrice de hauteur d'eau pour un bloc spécifique

        block : numéro du bloc; 1-based;
        """
        if isinstance(block,str):
            return self.myblocks[block].waterdepth
        else:
            return self.myblocks[getkeyblock(block,False)].waterdepth

    def get_qx_for_block(self, block: Union[int, str]) -> WolfArray:
        """
        Retourne la matrice de débit selon X pour un bloc spécifique

        block : numéro du bloc; 1-based;
        """
        if isinstance(block,str):
            return self.myblocks[block].qx
        else:
            return self.myblocks[getkeyblock(block,False)].qx

    def get_qy_for_block(self, block: Union[int, str]) -> WolfArray:
        """
        Retourne la matrice de débit selon Y pour un bloc spécifique

        block : numéro du bloc; 1-based;
        """
        if isinstance(block,str):
            return self.myblocks[block].qy
        else:
            return self.myblocks[getkeyblock(block,False)].qy

    def get_values_as_wolf(self, i:int, j:int, which_block:int=1):
        """
        Retourne les valeurs associées à des indices (i,j) et un numéro de block

        which_block : numéro du bloc; 1-based;

        ***
        ATTENTION :
            Les indices sont passés comme WOLF --> en numérotation Fortran (démarrage à 1 et non à 0)
        ***
        """
        h=-1
        qx=-1
        qy=-1
        vx=-1
        vy=-1
        vabs=-1
        fr=-1

        nbx = self.myblocks[getkeyblock(which_block,False)].waterdepth.nbx
        nby = self.myblocks[getkeyblock(which_block,False)].waterdepth.nby

        if(i>0 and i<=nbx and j>0 and j<=nby):
            h = self.myblocks[getkeyblock(which_block,False)].waterdepth.array[i-1,j-1]
            top = self.myblocks[getkeyblock(which_block,False)].top.array[i-1,j-1]
            qx = self.myblocks[getkeyblock(which_block,False)].qx.array[i-1,j-1]
            qy = self.myblocks[getkeyblock(which_block,False)].qy.array[i-1,j-1]
            if(h>0.):
                vx = qx/h
                vy = qy/h
                vabs=(vx**2.+vy**2.)**.5
                fr = vabs/(9.81*h)**.5

        return h,qx,qy,vx,vy,vabs,fr,h+top,top

    def get_values_turb_as_wolf(self, i:int, j:int, which_block:int=1):
        """
        Retourne les valeurs de turbulence associées à des indices (i,j) et un numéro de block

        which_block : numéro du bloc; 1-based;

        ATTENTION : Les indices sont passés comme WOLF --> en numérottaion Fortran (démarrage à 1 et non à 0)

        """
        k=-1
        e=-1
        nut=-1

        nbx = self.myblocks[getkeyblock(which_block,False)].waterdepth.nbx
        nby = self.myblocks[getkeyblock(which_block,False)].waterdepth.nby

        if(i>0 and i<=nbx and j>0 and j<=nby):
            k = self.myblocks[getkeyblock(which_block,False)].k.array[i-1,j-1]
            e = self.myblocks[getkeyblock(which_block,False)].eps.array[i-1,j-1]

            if e>0.:
                nut = 0.09*k**2./e

        return k,e,nut

    def get_header_block(self, which_block=1) -> header_wolf:
        """
        Obtention du header_wolf d'un block

        which_block : numéro du bloc; 1-based;
        """

        return self.head_blocks[getkeyblock(which_block,False)]

    def get_xy_infootprint_vect(self, myvect: vector, which_block=1) -> np.ndarray:

        """
        Returns:
            numpy array content les coordonnées xy des mailles dans l'empreinte du vecteur
        """

        myptsij = self.get_ij_infootprint_vect(myvect, which_block)
        mypts=np.asarray(myptsij.copy(),dtype=np.float64)

        lochead = self.get_header_block(which_block)

        mypts[:,0] = (mypts[:,0]+.5)*lochead.dx +lochead.origx +lochead.translx
        mypts[:,1] = (mypts[:,1]+.5)*lochead.dy +lochead.origy +lochead.transly

        return mypts,myptsij

    def get_ij_infootprint_vect(self, myvect: vector, which_block=1) -> np.ndarray:

        """
        Returns:
            numpy array content les indices ij des mailles dans l'empreinte du vecteur
        """

        lochead = self.get_header_block(which_block)
        nbx = lochead.nbx
        nby = lochead.nby

        i1, j1 = self.get_ij_from_xy(myvect.xmin, myvect.ymin, which_block)
        i2, j2 = self.get_ij_from_xy(myvect.xmax, myvect.ymax, which_block)
        i1 = max(i1,0)
        j1 = max(j1,0)
        i2 = min(i2,nbx-1)
        j2 = min(j2,nby-1)
        xv,yv = np.meshgrid(np.arange(i1,i2+1),np.arange(j1,j2+1))
        mypts = np.hstack((xv.flatten()[:,np.newaxis],yv.flatten()[:,np.newaxis]))

        return mypts

    def get_xy_inside_polygon(self, myvect: vector, usemask=True):
        """
        Obtention des coordonnées contenues dans un polygone
         usemask = restreint les éléments aux éléments non masqués de la matrice
        """

        myvect.find_minmax()

        mypointsxy={}

        myvert = myvect.asnparray()
        path = mpltPath.Path(myvert)

        for curblock in range(self.nb_blocks):
            locpointsxy,locpointsij = self.get_xy_infootprint_vect(myvect,curblock+1)
            inside = path.contains_points(locpointsxy)

            locpointsxy = locpointsxy[np.where(inside)]

            if usemask and len(locpointsxy)>0:
                locpointsij = locpointsij[np.where(inside)]
                mymask = np.logical_not(self.myblocks[getkeyblock(curblock)].current.array.mask[locpointsij[:, 0], locpointsij[:, 1]])
                locpointsxy = locpointsxy[np.where(mymask)]

            mypointsxy[getkeyblock(curblock)]=locpointsxy

        return mypointsxy

    def get_xy_under_polyline(self, myvect: vector) -> dict[str, (int,int)]:
        """
        Obtention des coordonnées (x,y) sous une polyligne avec séparation des points par bloc
         usemask = restreint les éléments aux éléments non masqués de la matrice
        """

        ds = self.get_dxdy_min()  # récupération de la taille la plus fine
        pts = myvect._refine2D(ds)# récupération des (x,y) selon le vecteur au pas le plus fin

        mypoints={}
        for idx in range(self.nb_blocks):
            mypoints[getkeyblock(idx)]=[]

        for curpt in pts:
            i,j,curblock = self.get_blockij_from_xy(curpt.x, curpt.y, aswolf=False)
            if curblock>-1:
                mypoints[getkeyblock(curblock)].append([curpt.x, curpt.y])

        return mypoints

    def get_values_insidepoly(self, myvect:vector, usemask:bool=True, agglo:bool=True, getxy:bool=False):
        """
        Retourne les valeurs des mailles contenues dans un polygone
        Traite la matrice courante et l'altitude de fond si on est en vue 'views_2D.WATERLEVEL'

        :param myvect : polygone
        :param usemask (optional) restreint les éléments aux éléments non masqués de la matrice
        :param agglo (optional) agglomère le résultat en une seule liste plutôt que d'avoir autant de liste que de blocs
        :param getxy (optional) retourne en plus les coordonnées des points

        :return myvalues : valeurs des mailles

        """
        myvalues={}
        myvaluesel={}
        mypoints = self.get_xy_inside_polygon(myvect, usemask)

        for curblock in range(self.nb_blocks):
            curkey = getkeyblock(curblock)
            if len(mypoints[curkey])>0:
                locval = np.asarray([self.get_value(cur[0], cur[1]) for cur in mypoints[curkey]])
                locel  = np.asarray([self.get_value_elevation(cur[0],cur[1]) for cur in mypoints[curkey]])

                locval=locval[np.where(locval!=-1)]
                locel =locel[np.where(locel!=-1)]

                myvalues[curkey]=locval
                myvaluesel[curkey]=locel
            else:
                myvalues[curkey]  =np.asarray([])
                myvaluesel[curkey]=np.asarray([])

        if agglo:
            myvalues   = np.concatenate([cur for cur in myvalues.values()])
            myvaluesel = np.concatenate([cur for cur in myvaluesel.values()])
            mypoints   = np.concatenate([cur for cur in mypoints.values()])

        if self._which_current_view == views_2D.WATERLEVEL:
            if getxy:
                return myvalues,myvaluesel,mypoints
            else:
                return myvalues,myvaluesel
        else:
            if getxy:
                return myvalues,None,mypoints
            else:
                return myvalues,None

    def get_all_values_insidepoly(self,myvect:vector, usemask=True, agglo=True, getxy=False):
        """
        Récupération de toutes les valeurs dans un polygone

        usemask (optional) restreint les éléments aux éléments non masqués de la matrice
        getxy (optional) retourne en plus les coordonnées des points
        """

        myvalues={}
        mypoints = self.get_xy_inside_polygon(myvect, usemask)

        for curblock in range(self.nb_blocks):
            if len(mypoints[getkeyblock(curblock)])>0:
                locval = np.asarray([self.get_values_from_xy(cur[0], cur[1]) for cur in mypoints[getkeyblock(curblock)]], dtype=object)

                locval=np.asarray([tuple(valloc) for valloc in locval if tuple(valloc)!=((-1,-1,-1,-1,-1,-1,-1),('-','-','-'))], dtype=object)

                myvalues[getkeyblock(curblock)]=locval
            else:
                myvalues[getkeyblock(curblock)]=np.empty([0,2])

        if agglo:
            myvalues   = np.concatenate([cur for cur in myvalues.values()])
            mypoints   = np.concatenate([cur for cur in mypoints.values()])

        if getxy:
            return myvalues,mypoints
        else:
            return myvalues

    def get_all_values_underpoly(self,myvect:vector, usemask=True, agglo=True, getxy=False, integrate_q = False):
        """
        Récupération de toutes les valeurs sous la polyligne
        Les valeurs retrounées sont identiques à la fonction "get_values_from_xy" soit (h,qx,qy,vx,vy,vabs,fr,h+top,top),(i+1,j+1,curblock.idx+1)

        usemask (optional) restreint les éléments aux éléments non masqués de la matrice
        getxy (optional) retourne en plus les coordonnées des points
        agglo (optional) agglomère le résultat en une seule liste plutôt que d'avoir autant de liste que de blocs
        """
        myvalues={}
        mypoints = self.get_xy_under_polyline(myvect)

        for curkey, ptsblock in mypoints.items():
            if len(ptsblock)>0:
                myvalues[curkey]=np.asarray([self.get_values_from_xy(cur[0], cur[1], integrate_q=integrate_q) for cur in ptsblock], dtype=object)
            else:
                myvalues[curkey]=np.empty([0,2])

        if agglo:

            loclist = [cur for cur in myvalues.values()]
            if len(loclist)>0:
                myvalues   = np.concatenate([cur for cur in myvalues.values()])
            else:
                myvalues = []

            if getxy:
                loclist = [cur for cur in mypoints.values() if len(cur)>0]
                if len(loclist)>0:
                    mypoints   = np.concatenate([cur for cur in mypoints.values() if len(cur)>0])
                else:
                    mypoints = np.asarray([])

        if getxy:
            return myvalues,mypoints
        else:
            return myvalues

    def get_q_alongpoly(self, myvect:vector, x_or_y:str = 'x', to_sum=True):
        """alias"""
        self.get_q_underpoly(myvect, x_or_y, to_sum)

    def get_q_underpoly(self, myvect:vector, x_or_y:str = 'x', to_sum=True):
        """
        Récupération du débit sous un vecteur

        to_sum pour sommer les valeurs et multiplier par la taille de maille
        """
        vals = self.get_all_values_underpoly(myvect, integrate_q=to_sum)

        if x_or_y.lower()=='x':
            idxq=1
        else:
            idxq=2

        q = np.asarray([cur[0][idxq] for cur in vals])

        if to_sum:
            return q.sum()
        else:
            return q

    def get_q_alongpoly_with_neighbor(self, myvect:vector, x_or_y:str = 'x', to_sum=True):
        """
        Récupération du débit sous un vecteur mais uniquement si un voisin existe dans la direction d'intégration

        to_sum pour sommer les valeurs et multiplier par la taille de maille
        """
        vals, xy = self.get_all_values_underpoly(myvect, integrate_q=to_sum, getxy=True)

        # ij = [self.get_ij_from_xy(x,y) for x,y in xy]
        if x_or_y.lower()=='x':
            # sommation de qx
            #  test du voisinage selon x -> i
            idxq=1
            dx = self[0].dx
            dy = 0.
        else:
            idxq=2
            dx = 0.
            dy = self[0].dy

        q = np.asarray([cur[0][idxq] for cur in vals])

        for idx, ((x,y), val) in enumerate(zip(xy, q)):
            if val > 0.:

                unk = self.get_values_from_xy(x+dx,y+dy)
                if unk[0][0] is np.ma.masked or unk[1][0] =='-':
                    q[idx] = 0.

            elif val < 0.:

                unk = self.get_values_from_xy(x-dx,y-dy)
                if unk[0][0] is np.ma.masked or unk[1][0] =='-':
                    q[idx] = 0.


        if to_sum:
            return q.sum()
        else:
            return q

    def get_q_alongpoly_raster_splitting(self, myvect:vector, to_sum=True, to_rasterize = True):
        """
        Récupération du débit sous un vecteur après avoir rasterisé selon les bords et appliqué le splitting WOLF aux flux

        Forcage préalable du vecteur slon la grille de calcul

        :param myvect : wolf polyline
        :param to_sum : pour sommer les valeurs et multiplier par la taille de maille
        :param to_rasterize : pour rasteriser le vecteur selon la grille de calcul
        """

        myhead = self.get_header_block(1)
        if to_rasterize:
            myvect = myhead.rasterize_vector(myvect)

        mynormals = myvect.get_normal_segments()
        xy_center = myvect.get_center_segments()

        norm_neigh = mynormals.copy()
        norm_neigh[:,0] = norm_neigh[:,0] * myhead.dx / 2.
        norm_neigh[:,1] = norm_neigh[:,1] * myhead.dy / 2.
        xy_left  = xy_center + norm_neigh
        xy_right = xy_center - norm_neigh
        values_left  = [self.get_values_from_xy(x, y, integrate_q=True) for x,y in xy_left]
        values_right = [self.get_values_from_xy(x, y, integrate_q=True) for x,y in xy_right]

        q=[]
        for curnorm, val_left, val_right in zip(mynormals, values_left, values_right):
            if not(outside_domain(val_left) or outside_domain(val_right)):
                if curnorm[0] != 0.:
                    q.append(q_splitting(val_left[0][1], val_left[0][1]) * curnorm[0])
                else:
                    q.append(q_splitting(val_left[0][2], val_left[0][2]) * curnorm[1])

        q = np.asarray(q)
        if to_sum:
            return q.sum()
        else:
            return q

    def _plot_one_q(self, vect:vector, x_or_y:str = 'x', absolute=True) -> float:

        qloc = self.get_q_alongpoly_with_neighbor(vect,x_or_y,True)
        if absolute:
            qloc = abs(qloc)

        return qloc

    def _plot_one_q_raster_splitting(self, vect:vector, absolute=True, to_rasterize = True) -> float:

        qloc = self.get_q_alongpoly_raster_splitting(vect, to_sum = True, to_rasterize = to_rasterize)
        if absolute:
            qloc = abs(qloc)

        return qloc

    def setup_cache(self, start_idx:int, end_idx:int = -1, only_h:bool = False):
        """
        Setup cache for results

        #FIXME : not implemented for général 2D results -- just for GPU
        Defined here for compatibility
        """
        self._cache = None

    def clear_cache(self):
        """
        Clear cache

        #FIXME : not implemented for général 2D results -- just for GPU
        Defined here for compatibility
        """
        self._cache = None

    #FIXME : rename 'x_or_y' to be more explicit
    def plot_q(self,
               vect:Union[vector, list[vector]],
               x_or_y:Union[str, list[str]] = 'x',
               toshow=False,
               absolute=True,
               figax = None):
        """
        Plot discharge along vector

        :param vector : wolf polyline -- will be splitted according to spatial step size
        :param x_or_y : 'x' for qx, 'y' for qy - integration axis or 'border' for q normal at border
        :param toshow : show the plot
        :param absolute : plot absolute value of discharge
        :param figax : tuple of matplotlib figure and axis

        """

        nb = self.get_nbresults()
        times, steps = self.times, self.timesteps

        if figax is None:
            fig, ax = plt.subplots()
        else:
            fig,ax = figax

        if isinstance(vect, vector):
            assert x_or_y in ['x', 'y', 'border'], 'x_or_y must be "x", "y" or "border"'

            q=[]
            for i in tqdm(range(nb)):
                self.read_oneresult(i)
                if x_or_y in ['x', 'y']:
                    q.append(self._plot_one_q(vect, x_or_y, absolute))
                elif x_or_y == 'border':
                    if i==0:
                        myhead = self.get_header_block(1)
                        vect_raster = myhead.rasterize_vector(vect)
                    q.append(self._plot_one_q_raster_splitting(vect_raster, absolute, to_rasterize = False))

            ax.plot(times,q, c='blue', label=vect.myname)

        else:

            assert len(vect) == len(x_or_y), 'Exepected same length for vect and x_or_y'
            for cur in x_or_y:
                assert cur in ['x', 'y', 'border'], 'x_or_y must be "x", "y" or "border"'

            q={int:list}
            vect_raster = []
            myhead = self.get_header_block(1)

            for i in range(len(vect)):
                q[i]= []
                if x_or_y[i] == 'border':
                    vect_raster.append(myhead.rasterize_vector(vect[i]))

            for i in tqdm(range(nb)):
                self.read_oneresult(i)

                for idx, (curvec, orient) in enumerate(zip(vect, x_or_y)):

                    if orient in ['x', 'y']:
                        q[idx].append(self._plot_one_q(curvec, orient, absolute))
                    elif orient == 'border':
                        cur_vect_raster = vect_raster[idx]
                        q[idx].append(self._plot_one_q_raster_splitting(cur_vect_raster, absolute, to_rasterize = False))

            for i in range(len(vect)):
                ax.plot(times,q[i], label=vect[i].myname)

        ax.set_xlabel(_('Time [s]'))
        ax.set_ylabel(_('Discharge/Flow rate [$m^3s^{-1}$]'))
        ax.legend(loc=2)

        fig.tight_layout()

        if toshow:
            fig.show()

        return fig,ax

    def plot_h(self, xy:Union[list[float], vector], h_or_z:Literal['h', 'z', 'head'], toshow=False, figax = None):
        """
        Plot water depth at one or multiple coordinates

        :param xy : list of coordinates
        :param h_or_z : 'h' for water depth, 'z' for bed elevation, 'head' for water head
        :param toshow : show the plot
        :param figax : tuple of matplotlib figure and axis

        """

        nb = self.get_nbresults(force_update_timessteps=True)
        times, steps = self.times, self.timesteps

        vals=[]
        if isinstance(xy, vector):
            label = xy.myname
            oldview = self.get_currentview()

            if h_or_z == 'h':
                curview = views_2D.WATERDEPTH
            elif h_or_z == 'z':
                curview = views_2D.WATERLEVEL
            elif h_or_z == 'head':
                curview = views_2D.HEAD

            label_y = curview.value

            for i in tqdm(range(nb)):
                self.read_oneresult(i)
                self.set_current(curview)
                vals.append(self.get_values_insidepoly(xy,)[0])

            self.set_currentview(oldview)

        else:
            label = _('Selected nodes')
            for i in tqdm(range(nb)):
                self.read_oneresult(i)

                values = [self.get_values_from_xy(x,y) for x,y in xy]

                which = 0
                if h_or_z =='h':
                    which = 0
                    values = np.asarray([valsloc[0][which] for valsloc in values])
                    label_y = _('Water depth [$m$]')

                elif h_or_z =='z':
                    which = 7
                    values = np.asarray([valsloc[0][which] for valsloc in values])
                    label_y = _('Water level [$m$]')

                elif h_or_z =='head':
                    values = np.asarray([valsloc[0][7]+valsloc[0][5]**2./2/9.81 for valsloc in values])
                    label_y = _('Water head [$m$]')

                vals.append(values)

        if figax is None:
            fig, ax = plt.subplots()
        else:
            fig, ax = figax

        means= []
        min = []
        max = []
        for curvals in vals:
            means.append(curvals.mean())
            min.append(curvals.min())
            max.append(curvals.max())

        ax.plot(times, means, label=_('Mean value - {}'.format(label)))
        ax.plot(times, min, label=_('Min value - {}'.format(label)))
        ax.plot(times, max, label=_('Max value - {}'.format(label)))

        ax.set_xlabel(_('Time [s]'))
        ax.set_ylabel(label_y)
        ax.legend(loc=2)
        fig.tight_layout()

        if toshow:
            fig.show()

        return fig,ax

    def get_values_from_xy(self, x:float, y:float, aswolf=True, integrate_q = False):
        """
        Retrouve les valeurs sur base de la coordonnée (x,y)

        aswolf : (optional) si True alors ajoute 1 à i et j pour se retrouver en numérotation VB6/Fortran
        """
        h=-1
        qx=-1
        qy=-1
        vx=-1
        vy=-1
        vabs=-1
        fr=-1

        exists=False
        for i,j,curblock in self.enum_block_xy(x,y):
            h = curblock.waterdepth.array[i,j]
            top = curblock.top.array[i,j]
            qx = curblock.qx.array[i,j]
            qy = curblock.qy.array[i,j]

            exists = top>0.

            if(h>0.):
                vx = qx/h
                vy = qy/h
                vabs=(vx**2.+vy**2.)**.5
                fr = vabs/(9.81*h)**.5
                exists=True

            if exists:
                if integrate_q:
                    qx *= curblock.qx.dy
                    qy *= curblock.qy.dx
                break

        if exists:
            if aswolf:
                return (h,qx,qy,vx,vy,vabs,fr,h+top,top),(i+1,j+1,curblock.blockindex+1)
            else:
                return (h,qx,qy,vx,vy,vabs,fr,h+top,top),(i,j,curblock.blockindex)
        else:
            return (-1,-1,-1,-1,-1,-1,-1),('-','-','-')

    def get_values_turb_from_xy(self, x:float, y:float, aswolf=True):
        """
        Retrouve les valeurs de turbulence sur base de la coordonnée (x,y)

        aswolf : (optional) si True alors ajoute 1 à i et j pour se retrouver en numérotation VB6/Fortran
        """
        h=-1
        k=-1
        e=-1
        nut=-1

        exists=False
        for i,j,curblock in self.enum_block_xy(x,y):
            h = curblock.waterdepth.array[i,j]
            k = curblock.k.array[i,j]
            e = curblock.eps.array[i,j]

            if(h>0. and e>0.):
                nut = 0.09*k**2./e
                exists=True

            if exists:
                break

        if exists:
            if aswolf:
                return (k,e,nut),(i+1,j+1,curblock.blockindex+1)
            else:
                return (k,e,nut),(i,j,curblock.blockindex)
        else:
            return (-1,-1,-1),('-','-','-')

    def get_value(self, x:float, y:float, nullvalue=-1):
        """
        Return the value of the current array at (X,Y) position
        """
        h=-1
        exists=False
        for i,j,curblock in self.enum_block_xy(x,y):
            h = curblock.waterdepth.array[i,j]
            val = curblock.current.array[i,j]

            if h is not np.nan:
                exists=np.abs(h)>0.
                if exists:
                    break

        if exists:
            return val
        else:
            return nullvalue

    def get_values_labels(self,x:float, y:float):
        """
        Return the values and labels of the current view at (X,Y) position
        """
        h=-1
        exists=False

        for i,j, curblock in self.enum_block_xy(x,y):
            h = curblock.waterdepth.array[i,j]

            if h is not np.nan:
                exists=np.abs(h)>0.
                if exists:
                    break

        if exists:
            vals,labs = curblock.get_values_labels(i,j)

            vals = [self.current_result+1]  + vals
            labs = ["Stored step (1-based)"] + labs

            vals = [self.times[self.current_result]]  + vals
            labs = ["Real Time [s]"] + labs

            if self.times[self.current_result]>3600:
                time_in_sec = self.times[self.current_result]
                vals = [str(timedelta(seconds=int(time_in_sec),
                                      milliseconds=int(time_in_sec-int(time_in_sec))*1000))]  + vals
                labs = ["Real Time [date]"] + labs


            vals = [self.timesteps[self.current_result]]  + vals
            labs = ["Step Time [iter]"] + labs

            return vals,labs
        else:
            return -1

    def get_value_elevation(self, x:float, y:float, nullvalue=-1):
        """Return the value of the bed elevation at (X,Y) position"""

        exists=False
        for i,j,curblock in self.enum_block_xy(x,y):
            h = curblock.waterdepth.array[i,j]
            val = curblock.top.array[i,j]

            if h is not np.nan:
                exists=np.abs(h)>0.
                if exists:
                    break

        if exists:
            return val
        else:
            return nullvalue

    def get_xy_from_ij(self, i:int, j:int, which_block:int=1, aswolf:bool=False, abs:bool=True):
        """
        Retourne les coordonnées (x,y) depuis les indices (i,j) et le numéro de block

        :param i: i index
        :param j: j index
        :param which_block: block number; 1-based;
        :param aswolf: True to add 1 to i and j to match the VB6/Fortran numbering format
        :param abs: True to return absolute coordinates
        """

        x,y = self.myblocks[getkeyblock(which_block,False)].waterdepth.get_xy_from_ij(i, j, aswolf=aswolf, abs=abs)
        return x,y

    def get_ij_from_xy(self, x:float, y:float, which_block:int = 1, aswolf=False, abs=True):
        """
        Retrouve les indices d'un point (x,y) dans un bloc spécifique

        Utilise la routine du même nom dans la martrice 'waterdepth'

        :param x: x coordinate
        :param y: y coordinate
        :param which_block: block number; 1-based;
        :param aswolf: True to add 1 to i and j to match the VB6/Fortran numbering format
        :param abs: True to return absolute coordinates
        """

        i,j = self.myblocks[getkeyblock(which_block, False)].waterdepth.get_ij_from_xy(x,y, aswolf=aswolf, abs=abs)

        return i,j # Par défaut en indices Python et non WOLF (VB6/Fortran)

    def _test_bounds_block(self, x:float, y:float, curblock:OneWolfResult):
        """
        Teste les bornes d'un bloc versus les coordonnées (x,y) d'un point
        """
        nbx = curblock.waterdepth.nbx
        nby = curblock.waterdepth.nby
        i,j = curblock.waterdepth.get_ij_from_xy(x, y, aswolf=False)

        if(i>=0 and i<nbx and j>=0 and j<nby):
            return True
        else:
            return False

    def enum_block_xy(self, x:float, y:float, aswolf=False, abs=True):
        """
        Enumération des blocs contenant la coordonnée (x,y)

        aswolf : True ajoute 1 à i et j pour corresppondre au format de numérotation VB6/Fortran
        """
        for curblock in self.myblocks.values():
            if self._test_bounds_block(x, y, curblock):

                i,j=curblock.waterdepth.get_ij_from_xy(x, y, aswolf=aswolf, abs=abs)

                yield i,j,curblock

    def get_blockij_from_xy(self, x:float, y:float, abs=True, aswolf=True):
        """
        Retourne les indices i,j et le numéro du block depuis les coordonnées (x,y)

        aswolf : True ajoute 1 à i et j pour corresppondre au format de numérotation VB6/Fortran
        """
        exists = False
        for i, j, curblock in self.enum_block_xy(x,y):
            if not curblock.waterdepth.array.mask[i, j]:
                exists = True
                break

        if exists:
            if aswolf:
                return i+1, j+1, curblock.blockindex+1
            else:
                return i, j, curblock.blockindex
        else:
            return -1, -1, -1

    def check_plot(self):
        """
        L'objet est coché/à traiter dans une fenêtre graphique 'WolfMapViewer'
        """
        self.plotted = True
        self.mimic_plotdata()

        if not self.loaded and self.filename!='':
            self.read_oneresult(self.current_result)
            self.reset_plot()

    def uncheck_plot(self, unload=False):
        """
        L'objet est décoché/pas à traiter dans une fenêtre graphique 'WolfMapViewer'
        """
        self.plotted = False
        self.mimic_plotdata()

    def link_palette(self):
        """
        Applique la même palette de couleur/colormap à tous les blocs
        """
        if (self.palgray is not None) and (self.palblue is not None):
            for curblock in self.myblocks.values():
                curblock.update_pal(self.mypal, self.palgray, self.palblue)
        else:
            for curblock in self.myblocks.values():
                curblock.update_pal(self.mypal)

    def get_min_max(self, which:Literal[views_2D.TOPOGRAPHY, views_2D.WATERDEPTH, 'current']):
        """
        Retourne la valeur min et max de la topo, de la hauteur d'eau ou de la matrice courante
        """
        if which == views_2D.TOPOGRAPHY:
            min = np.min([np.min(curblock.top.array) for curblock in self.myblocks.values()])
            max = np.max([np.max(curblock.top.array) for curblock in self.myblocks.values()])
        elif which == views_2D.WATERDEPTH:
            min = np.min([np.min(curblock.waterdepth.array) for curblock in self.myblocks.values()])
            max = np.max([np.max(curblock.waterdepth.array) for curblock in self.myblocks.values()])
        elif which == 'current':
            min = np.min([np.min(curblock.current.array) for curblock in self.myblocks.values()])
            max = np.max([np.max(curblock.current.array) for curblock in self.myblocks.values()])

        return min,max

    def get_working_array(self,onzoom=[]):
        """
        Délimitation d'une portion de matrice sur base de bornes

        onzoom : Liste Python de type [xmin, xmax, ymin, ymax]
        """

        if onzoom!=[]:
            allarrays=[]
            for curblock in self.myblocks.values():
                istart,jstart = curblock._current.get_ij_from_xy(onzoom[0],onzoom[2])
                iend,jend = curblock._current.get_ij_from_xy(onzoom[1],onzoom[3])

                istart= 0 if istart < 0 else istart
                jstart= 0 if jstart < 0 else jstart
                iend= curblock._current.nbx if iend > curblock._current.nbx else iend
                jend= curblock._current.nby if jend > curblock._current.nby else jend

                partarray=curblock._current.array[istart:iend,jstart:jend]
                partarray=partarray[partarray.mask==False]
                if len(partarray)>0:
                    allarrays.append(partarray.flatten())

            allarrays=np.concatenate(allarrays)
        else:
            allarrays = np.concatenate([curblock.current.array[curblock.current.array.mask==False].flatten() for curblock in self.myblocks.values()])

        self.nbnotnull = allarrays.count()

        return allarrays

    def updatepalette(self, which=0, onzoom=[]):
        """
        Mise à jour des palettes de couleur/colormaps

        palgray : niveaux de gris
        palblue : niveaux de bleu
        mypal   : coloration paramétrique

        :param which: 0
        :param onzoom: Liste Python de type [xmin, xmax, ymin, ymax]
        """
        self.palgray = wolfpalette()
        self.palblue = wolfpalette()

        self.palgray.defaultgray()
        self.palblue.defaultblue()

        self.palgray.values[0],self.palgray.values[-1] = self.get_min_max(views_2D.TOPOGRAPHY)
        self.palblue.values[0],self.palblue.values[-1] = self.get_min_max(views_2D.WATERDEPTH)

        if self.mypal.automatic:
            # self.mypal.default16()
            self.mypal.isopop(self.get_working_array(onzoom=onzoom),self.nbnotnull)

        self.link_palette()

        if self.properties is not None:
            # update GUI properties
            self.properties.update_palette()
            if self.mypal.automatic:
                self.properties._cm_auto.SetValue(1)
            else:
                self.properties._cm_auto.SetValue(0)

    def delete_lists(self):
        """
        Reset des listes OpenGL de la matrice courante
        """
        for curblock in self.myblocks.values():
            curblock._current.delete_lists()

    def mimic_plotdata(self, plotting=False):
        """
        Force la mise à jour de paramètres entre tous les blocs
        """
        self.plotting=plotting
        for curblock in self.myblocks.values():
            curblock._current.plotted = self.plotted
            curblock._current.plotting = self.plotting

            curblock.set_linkedvec(self.linkedvec)
            curblock.set_epsilon(self.epsilon)

    def plot(self, sx=None, sy=None,xmin=None,ymin=None,xmax=None,ymax=None, size=None):
        """Dessin OpenGL"""
        self.mimic_plotdata(True)

        for curblock in self.myblocks.values():
            curblock.plot(sx, sy,xmin,ymin,xmax,ymax)

        if self.myparam is not None:
            #conditions limites faibles
            self.myparam.weak_bc_x.myzones.plot()
            self.myparam.weak_bc_y.myzones.plot()

        # Plot selected nodes
        if self.mngselection is not None:
            self.mngselection.plot_selection()

        self.mimic_plotdata(False)

    def fillonecellgrid(self,curscale,loci,locj,force=False):
        """Dessin d'une fraction de la matrice pour tous les blocs"""
        for curblock in self.myblocks.values():
            curblock._current.fillonecellgrid(curscale,loci,locj,force)

    def set_current(self, which):
        """
        Change le type de résultat à présenter/traiter

        :param which: mode de visualisation --> see 'views_2D' for supported values"""

        if not which in views_2D:
            logging.error('Unknown view -- Check in views_2D')
            return

        for curblock in self.myblocks.values():
            curblock.set_current(which)

        self._which_current_view = which

    def next_result(self):
        """Lecture du pas suivant"""
        nb = self.get_nbresults()

        if self.current_result==-1:
            self.read_oneresult(-1)
        else:
            self.current_result+=1
            self.current_result = min(nb,self.current_result)
            self.read_oneresult(self.current_result)

            self.reset_plot()

    def reset_plot(self,whichpal=0):
        """Reset du dessin"""
        self.delete_lists()
        self.get_working_array()
        self.updatepalette(whichpal)

    def danger_map(self, start:int=0, end:int=-1, every:int=1) -> Union[tuple[WolfArray, WolfArray, WolfArray], tuple[WolfArrayMB, WolfArrayMB, WolfArrayMB]]:
        """
        Create Danger Maps
        """

        # Number of  time steps
        number_of_time_steps = self.get_nbresults()
        if end ==-1:
            end = number_of_time_steps

        # Init Danger Maps basde on results type
        #    If only one block --> WolfArray
        #    If only multiple blocks --> WolfArrayMB
        danger_map_matrix_h = self.as_WolfArray(copyarray=True)
        danger_map_matrix_v = self.as_WolfArray(copyarray=True)
        danger_map_matrix_mom = self.as_WolfArray(copyarray=True)

        # Reset data -> Set null values
        danger_map_matrix_h.reset()
        danger_map_matrix_v.reset()
        danger_map_matrix_mom.reset()

        danger_map_matrix_h.mask_reset()
        danger_map_matrix_v.mask_reset()
        danger_map_matrix_mom.mask_reset()

        danger = [danger_map_matrix_h, danger_map_matrix_v, danger_map_matrix_mom]

        for time_step in tqdm(range(start, end, every)):

            self.read_oneresult(time_step+1)

            if self.nb_blocks>1:
                for curblock in self.myblocks.keys():
                    # Get WolfArray
                    wd = self.get_h_for_block(curblock)
                    qx = self.get_qx_for_block(curblock)
                    qy = self.get_qy_for_block(curblock)

                    # Math operations are overloaded
                    v = (qx**2.+qy**2.)**.5/wd
                    mom = v*wd

                    comp = [wd, v, mom]

                    # Comparison
                    for curdanger, curcomp in zip(danger, comp):
                        i,j = np.where(curdanger.myblocks[curblock].array < curcomp.array)
                        curdanger.myblocks[curblock].array.data[i,j] = curcomp.array.data[i,j]

            else:
                curblock = getkeyblock(0)
                wd = self.get_h_for_block(curblock)
                qx = self.get_qx_for_block(curblock)
                qy = self.get_qy_for_block(curblock)

                v = (qx**2.+qy**2.)**.5/wd

                mom = v*wd

                comp = [wd, v, mom]

                # Comparison
                for curdanger, curcomp in zip(danger, comp):
                    i,j = np.where(curdanger.array < curcomp.array)
                    curdanger.array.data[i,j] = curcomp.array.data[i,j]

        danger_map_matrix_h.mask_lower(self.epsilon)
        if self.nb_blocks>1:
            for i in range(self.nb_blocks):
                danger_map_matrix_v[i].array.mask = danger_map_matrix_h[i].array.mask.copy()
                danger_map_matrix_mom[i].array.mask = danger_map_matrix_h[i].array.mask.copy()
        else:
            danger_map_matrix_v.array.mask = danger_map_matrix_h.array.mask.copy()
            danger_map_matrix_mom.array.mask = danger_map_matrix_h.array.mask.copy()


        return (danger_map_matrix_h, danger_map_matrix_v, danger_map_matrix_mom)
