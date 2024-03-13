import numpy as np
import numpy.ma as ma
from os import path
from pathlib import Path
from scipy.sparse import csr_array
from multiprocessing import Pool
from typing import Union
from tqdm import tqdm
import logging

from .PyTranslate import _
from .wolf_array import WolfArray
from .wolfresults_2D import Wolfresults_2D, views_2D, getkeyblock, OneWolfResult, vector, zone, Zones
from .PyVertex import wolfvertex
from .CpGrid import CpGrid
from .PyPalette import wolfpalette

try:
    from wolfgpu.results_store import ResultsStore, ResultType
except :
    logging.error(_("Unable to import wolfgpu.results_store.ResultsStore. Please install wolfgpu package or add a symlink to the wolfgpu package in the wolfhece directory"))

def _load_res(x) -> tuple[csr_array, csr_array, csr_array]:
    store:ResultsStore
    i:int

    store, i = x
    _, _, _, _, wd_np, qx_np, qy_np = store.get_result(i+1)

    if isinstance(wd_np, csr_array) and isinstance(qx_np, csr_array) and isinstance(qy_np, csr_array):
        return wd_np, qx_np, qy_np
    else:
        return csr_array(wd_np), csr_array(qx_np), csr_array(qy_np)

def _load_res_h(x) -> tuple[csr_array, csr_array, csr_array]:
    store:ResultsStore
    i:int

    store, i = x
    wd_np = store.get_named_result('h',i+1)

    if isinstance(wd_np, csr_array):
        return wd_np
    else:
        return csr_array(wd_np)

class Cache_Results2DGPU():
    """
    Gestion en mémoire de plusieurs résultats GPU
    Stockage CSR afin d'économiser la mémoire (Scipy CSR)
    """

    def __init__(self, fname:str, start_idx:int, end_idx:int = -1, only_h=False) -> None:
        """
        Chargement de résultats sur base du répertoire de sauvegarde de la simulation GPU

        Lecture des résultats depuis start_idx jusque end_idx

        only_h force la lecture de la hauteur d'eau seulement, sinon (h,qx,qy)

        :param fname: nom du répertoire de sauvegarde
        :param start_idx: index de départ (0-based)
        :param end_idx: index de fin (0-based)
        :param only_h: lecture de la hauteur d'eau seulement
        """

        self._results:Union[dict[str,tuple[csr_array, csr_array, csr_array]], dict[str,csr_array]] # typage

        # ResultsStore unique
        self._result_store = ResultsStore(Path(fname), mode='r')
        self._only_h = only_h

        if end_idx == -1:
            end_idx = self._result_store.nb_results

        if end_idx>start_idx:
            self.start_idx = int(max(start_idx,0))
            self.end_idx   = int(min(end_idx, self._result_store.nb_results))

            # Lecture en multiprocess des résultats
            if only_h:
                with Pool() as pool:
                    _results = pool.map(_load_res_h, [(self._result_store,i) for i in range(self.start_idx, self.end_idx)])
                    self._results = {i+1:res for i,res in enumerate(_results)}
            else:
                with Pool() as pool:
                    _results = pool.map(_load_res, [(self._result_store,i) for i in range(self.start_idx, self.end_idx)])
                    self._results = {i+1:res for i,res in enumerate(_results)}

    @property
    def only_h(self):
        return self._only_h

    def __getitem__(self,i:int):
        """Surcharge de l'opérateur []"""
        return self._results[i]

    def get_h(self, idx:int, dense:bool=True) -> Union[np.ndarray, csr_array]:
        """
        Retourne la matrice de hauteur d'eau de la position idx (0-based)
            - en CSR (Scipy CSR)
            - en dense (Numpy array)
        """
        if not self.only_h:
            return self._results[idx][0].toarray() if dense else self._results[idx][0]
        else:
            return self._results[idx].toarray() if dense else self._results[idx]

    def get_qx(self,idx:int, dense:bool=True) -> Union[np.ndarray, csr_array]:
        """
        Retourne la matrice de débit X d'eau de la position idx (0-based)
            - en CSR (Scipy CSR)
            - en dense (Numpy array)
        """

        if not self.only_h:
            return self._results[idx][1].toarray() if dense else self._results[idx][1]
        else:
            return None

    def get_qy(self,idx:int, dense:bool=True) -> Union[np.ndarray, csr_array]:
        """
        Retourne la matrice de débit Y d'eau de la position idx (0-based)
            - en CSR (Scipy CSR)
            - en dense (Numpy array)
        """

        if not self.only_h:
            return self._results[idx][2].toarray() if dense else self._results[idx][2]
        else:
            return None


class wolfres2DGPU(Wolfresults_2D):
    """
    Gestion des résultats du code GPU 2D
    Surcharge de "Wolfresults_2D"
    """

    def __init__(self,
                 fname:str,
                 eps=0.,
                 idx: str = '',
                 plotted: bool = True,
                 mapviewer=None,
                 store = None):

        super().__init__(fname = str(Path(fname)), eps=eps, idx=idx, plotted=plotted, mapviewer=mapviewer, loader=self._loader)

        # MERGE Inheriting is a bad idea in general because it allows
        # classes to look inside others, and induces hard
        # coupling. It's better to connect with instances and use
        # their functions so that the provider can better enforce what
        # is available to class's users.

        if store is None:
            self._result_store = ResultsStore(sim_path = Path(fname), mode='r')
        else:
            self._result_store = store

        self._cache = None

    def setup_cache(self, start_idx:int=0, end_idx:int = -1, only_h:bool = False):
        """
        Setup cache from start_idx result to end_idx result

        if only_h is True, only waterdepth is loaded into memory

        :param start_idx: start index (0-based)
        :param end_idx: end index (0-based)
        :param only_h: only waterdepth is loaded into memory
        """
        self._cache = Cache_Results2DGPU(self.filename, start_idx, end_idx, only_h= only_h)

    def clear_cache(self):
        """
        Clear cache
        """
        self._cache = None

    def _loader(self, fname:str):
        # 2D GPU

        self.filename = fname
        sim_path = Path(fname).parent

        nb_blocks = 1
        self.myblocks = {}
        curblock = OneWolfResult(0, parent=self)
        self.myblocks[getkeyblock(0)] = curblock

        if path.exists(path.join(sim_path, 'simul.top')):

            curblock.top = WolfArray(path.join(sim_path, 'simul.top'), nullvalue=99999.)
            curblock.waterdepth = WolfArray(path.join(sim_path, 'simul.hbin'))
            curblock.qx = WolfArray(path.join(sim_path, 'simul.qxbin'))
            curblock.qy = WolfArray(path.join(sim_path, 'simul.qybin'))
            curblock.rough_n = WolfArray(path.join(sim_path, 'simul.frot'))

        elif path.exists(path.join(sim_path, 'bathymetry.npy')):
            curblock.top = WolfArray(path.join(sim_path, 'bathymetry.npy'))
            curblock.waterdepth = WolfArray(path.join(sim_path, 'h.npy'))
            curblock.qx = WolfArray(path.join(sim_path, 'qx.npy'))
            curblock.qy = WolfArray(path.join(sim_path, 'qy.npy'))
            curblock.rough_n = WolfArray(path.join(sim_path, 'manning.npy'))

            if path.exists(path.join(sim_path, 'parameters.json')):

                import json
                with open(path.join(sim_path, 'parameters.json'), 'r') as fp:

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

        # Force nullvalue to zero because it will influence the size of the arrow in vector field views
        curblock.qx.nullvalue = 0.
        curblock.qy.nullvalue = 0.

        self.loaded_rough = True

        self.head_blocks[getkeyblock(0)] = curblock.top.get_header()

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
            if path.exists(path.join(sim_path, 'simul.top')):
                logging.error(_("Inconsistent header file in .top, .qxbin, .qybin or .frot files"))
                logging.error(_("Forcing information into memory from the .top file -- May corrupt spatial positionning -- Please check your data !"))

            for curarray in to_check:
                curarray.dx    = curblock.top.dx
                curarray.dy    = curblock.top.dy
                curarray.origx = curblock.top.origx
                curarray.origy = curblock.top.origy
                curarray.translx = curblock.top.translx
                curarray.transly = curblock.top.transly

        if path.exists(path.join(sim_path, 'simul.trl')):
            with open(path.join(sim_path, 'simul.trl')) as f:
                trl=f.read().splitlines()
                self.translx=float(trl[1])
                self.transly=float(trl[2])

        curblock.set_current(views_2D.WATERDEPTH)

        self.myparam = None
        self.mymnap = None
        self.myblocfile = None

    def get_nbresults(self, force_update_timessteps=True):
        """
        Récupération du nombre de résultats

        Lecture du fichier de tracking afin de permettre une mise à jour en cours de calcul
        """
        self._result_store.reload()
        if force_update_timessteps:
            self.get_times_steps()

        self._nb_results = self._result_store.nb_results
        return self._result_store.nb_results

    def read_oneresult(self, which:int=-1):
        """
        Lecture d'un pas de sauvegarde

        which: result number to read; 0-based; -1 == last one
        """

        which = self._sanitize_result_step(which)

        # stored result files are 1-based -> which+1
        if self._cache is not None:
            if (which >= self._cache.start_idx and which < self._cache.end_idx) and (not self._cache.only_h):
                wd_np = self._cache.get_h(which+1, True)
                qx_np = self._cache.get_qx(which+1, True)
                qy_np = self._cache.get_qy(which+1, True)
            else:
                _, _, _, _, wd_np, qx_np, qy_np = self._result_store.get_result(which+1)
        else:
            _, _, _, _, wd_np, qx_np, qy_np = self._result_store.get_result(which+1)

        curblock = self.myblocks[getkeyblock(1,False)]
        if self.epsilon > 0.:
            curblock.waterdepth.array=ma.masked_less_equal(wd_np.astype(np.float32).T, self.epsilon)
        else:
            curblock.waterdepth.array=ma.masked_equal(wd_np.astype(np.float32).T, 0.)

        curblock.qx.array=ma.masked_where(curblock.waterdepth.array.mask,qx_np.astype(np.float32).T)
        curblock.qy.array=ma.masked_where(curblock.waterdepth.array.mask,qy_np.astype(np.float32).T)

        curblock.waterdepth.count()
        curblock.qx.count()
        curblock.qy.count()

        curblock.waterdepth.set_nullvalue_in_mask()
        curblock.qx.set_nullvalue_in_mask()
        curblock.qy.set_nullvalue_in_mask()

        self.current_result = which
        self.loaded=True

    def _update_result_view(self):
        """
        Procédure interne de mise à jour du pas

        Etapes partagées par read_next et read_previous
        """
        self.current_result = self._sanitize_result_step(self.current_result)
        self.read_oneresult(self.current_result)

    def read_next(self):
        """
        Lecture du pas suivant
        """
        self.current_result+=1
        self._update_result_view()

    def get_times_steps(self, nb:int = None):
        """
        Récupération des temps réels et les pas de calcul de chaque résultat sur disque

        :param nb : nombre de résultats à lire

        """
        self.times = [time[ResultType.T.value] for time in self._result_store._sim_times]
        self.timesteps = [time[ResultType.STEP_NUM.value] for time in self._result_store._sim_times]

        if nb is None:
            return self.times, self.timesteps
        elif nb == 0:
            self.times, self.timesteps = [],[]
            return self.times, self.timesteps
        else:
            if nb <= len(self.times):
                return self.times[:nb], self.timesteps[:nb]
            else:
                return self.times, self.timesteps

    def read_previous(self):
        """
        Lecture du pas suivant
        """
        self.current_result -= 1
        self._update_result_view()

    def get_cached_h(self, idx):
        """ Return cached water depth according to WOLF convention """

        if self._cache is not None:
            return self._cache.get_h(idx+1, True).T
        else:
            return None

    def get_cached_qx(self, idx):
        """ Return cached specific discharge along X according to WOLF convention """

        if self._cache is not None:
            return self._cache.get_qx(idx+1, True).T
        else:
            return None

    def get_cached_qy(self, idx):
        """ Return cached specific discharge along Y according to WOLF convention """

        if self._cache is not None:
            return self._cache.get_qy(idx+1, True).T
        else:
            return None

    def show_tiles(self):
        """ Show tiles in mapviewer """

        if self.mapviewer is None:
            logging.error(_("No mapviewer available"))
            return

        grid_tiles = Zones()

        ox = self.origx
        oy = self.origy

        tile_size = 16

        dx_tiles = self[0].dx * tile_size
        dy_tiles = self[0].dy * tile_size

        nbx = int(self[0].nbx // tile_size + (1 if np.mod(self[0].nbx, tile_size) else 0))
        nby = int(self[0].nby // tile_size + (1 if np.mod(self[0].nby, tile_size) else 0))

        tiles_zone = zone(name = 'Tiles', parent = grid_tiles)
        grid_tiles.add_zone(tiles_zone)

        grid_x = vector(name = 'tiles_x', parentzone=tiles_zone)
        grid_y = vector(name = 'tiles_y', parentzone=tiles_zone)
        tiles_zone.add_vector(grid_x)
        tiles_zone.add_vector(grid_y)

        for i in range(nbx+1):
            if np.mod(i, 2) == 0:
                grid_x.add_vertex(wolfvertex(ox + i * dx_tiles, oy))
                grid_x.add_vertex(wolfvertex(ox + i * dx_tiles, oy + nby * dy_tiles))
            else:
                grid_x.add_vertex(wolfvertex(ox + i * dx_tiles, oy + nby * dy_tiles))
                grid_x.add_vertex(wolfvertex(ox + i * dx_tiles, oy))

        for j in range(nby+1):
            if np.mod(j, 2) == 0:
                grid_y.add_vertex(wolfvertex(ox, oy + j * dy_tiles))
                grid_y.add_vertex(wolfvertex(ox + nbx * dx_tiles, oy + j * dy_tiles))
            else:
                grid_y.add_vertex(wolfvertex(ox + nbx * dx_tiles, oy + j * dy_tiles))
                grid_y.add_vertex(wolfvertex(ox, oy + j * dy_tiles))


        self.mapviewer.add_object('vector', newobj = grid_tiles, id = 'Tiles')
class Sim_2D_GPU():
    """ Simulation 2D GPU -- Interface """

    def __init__(self, fname:Union[str,Path] = '') -> None:

        try:
            from wolfgpu.simple_simulation import SimpleSimulation
        except:
            logging.error(_("Unable to import wolfgpu.simple_simulation.SimpleSimulation. Please install wolfgpu package or add a symlink to the wolfgpu package in the wolfhece directory"))

        self.filename = Path(fname)
        self.loaded = False

        if self.filename.exists():
            self.sim = SimpleSimulation()
            self.sim.load(self.filename)
            self.loaded = True

        pass