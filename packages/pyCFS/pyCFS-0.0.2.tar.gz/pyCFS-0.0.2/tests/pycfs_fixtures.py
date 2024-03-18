import pytest
import numpy as np
from dataclasses import dataclass
from typing import List, Callable, Optional
from pyCFS import pyCFS


DEFAULT_PROJECT = "default_project"
DEFAULT_CFS_DIR = "default_install_dir/"
DEFAULT_PARAMS = np.array([], dtype=np.float64)
DEFAULT_TEMPLATES_PATH = "./templates/"
DEFAULT_RESULTS_HDF_PATH = "./results_hdf5/"
DEFAULT_LOGS_PATH = "./logs/"
DEFAULT_HISTORY_PATH = "./history/"
CFS_EXT = "cfs"
XML_EXT = "xml"
JOU_EXT = "jou"
CDB_EXT = "cdb"


@dataclass
class pyCFSArguments:
    project_name: str = ("",)
    cfs_install_dir: str = ("",)
    init_params = (DEFAULT_PARAMS,)
    cfs_params_names: List[str] = ([],)
    material_params_names: List[str] = ([],)
    trelis_params_names: List[str] = ([],)
    trelis_version: str = ("trelis",)
    cfs_proj_path: str = ("./",)
    templates_path: str = ("./templates",)
    init_file_extension: str = ("init",)
    mat_file_name: str = ("mat",)
    result_type: str = ("hdf5",)
    n_threads: int = (1,)
    res_manip_fun: Optional[Callable[["pyCFS"], None]] = (None,)
    quiet_mode: bool = (False,)
    detail_mode: bool = (False,)
    clean_finish: bool = (False,)
    save_hdf_results: bool = (False,)
    array_fill_value = (np.nan,)
    parallelize: bool = (False,)
    remeshing_on: bool = (False,)
    n_jobs_max: int = (1000,)
    testing: bool = (False,)


@pytest.fixture
def default_params() -> pyCFSArguments:

    args = pyCFSArguments()

    args.project_name = DEFAULT_PROJECT
    args.cfs_install_dir = DEFAULT_CFS_DIR
    args.init_params = DEFAULT_PARAMS
    args.cfs_params_names = []
    args.material_params_names = []
    args.trelis_params_names = []
    args.trelis_version = "trelis"
    args.cfs_proj_path = "./"
    args.templates_path = "./templates"
    args.init_file_extension = "init"
    args.mat_file_name = "mat"
    args.result_type = "hdf5"
    args.n_threads = 1
    args.res_manip_fun = None
    args.quiet_mode = False
    args.detail_mode = False
    args.clean_finish = False
    args.save_hdf_results = False
    args.array_fill_value = np.nan
    args.parallelize = False
    args.remeshing_on = False
    args.n_jobs_max = 1000
    args.testing = True # only exception !

    return args


@pytest.fixture
def dummy_params() -> pyCFSArguments:

    args = pyCFSArguments()

    args.project_name = "my_project"
    args.cfs_path = "/home/cfs/bin/"
    args.init_params = np.array([0.0, 0.0, 0.0])
    args.cfs_params_names = ["a", "b"]
    args.material_params_names = ["c"]
    args.trelis_params_names = []
    args.trelis_version = "trelis"
    args.cfs_proj_path = "./"
    args.templates_path = "./templates"
    args.init_file_extension = "init"
    args.mat_file_name = "mat"
    args.result_type = "hdf5"
    args.n_threads = 1
    args.res_manip_fun = None
    args.quiet_mode = False
    args.detail_mode = False
    args.clean_finish = False
    args.save_hdf_results = False
    args.array_fill_value = 200.0
    args.parallelize = False
    args.remeshing_on = True
    args.n_jobs_max = 1000
    args.testing = True

    return args


@pytest.fixture
def default_pycfs_obj() -> pyCFS:
    return pyCFS(
        DEFAULT_PROJECT,
        DEFAULT_CFS_DIR,
        DEFAULT_PARAMS,
        testing=True, # only exception !
    )


@pytest.fixture
def dummy_pycfs_obj(dummy_params) -> pyCFS:
    return pyCFS(
        dummy_params.project_name,
        dummy_params.cfs_path,
        dummy_params.init_params,
        cfs_params_names=dummy_params.cfs_params_names,
        material_params_names=dummy_params.material_params_names,
        trelis_params_names=dummy_params.trelis_params_names,
        trelis_version=dummy_params.trelis_version,
        cfs_proj_path=dummy_params.cfs_proj_path,
        templates_path=dummy_params.templates_path,
        init_file_extension=dummy_params.init_file_extension,
        mat_file_name=dummy_params.mat_file_name,
        result_type=dummy_params.result_type,
        n_threads=dummy_params.n_threads,
        res_manip_fun=dummy_params.res_manip_fun,
        quiet_mode=dummy_params.quiet_mode,
        detail_mode=dummy_params.detail_mode,
        clean_finish=dummy_params.clean_finish,
        save_hdf_results=dummy_params.save_hdf_results,
        array_fill_value=dummy_params.array_fill_value,
        parallelize=dummy_params.parallelize,
        remeshing_on=dummy_params.remeshing_on,
        n_jobs_max=dummy_params.n_jobs_max,
        testing=dummy_params.testing,
    )
