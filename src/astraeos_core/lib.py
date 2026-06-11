#
# * ========================================================================================
# * Importações
# * ========================================================================================
# ? --- Bibliotecas Padrão e Científicas ---
import os
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import *
import time
from astropy import constants as const
from astropy import units as u

# ? --- Módulos Locais (pytools) ---
try:
    from .pytools import system as sy
    from .pytools import graphs as gp
    from .pytools import saveload as sl
except ImportError:
    import pytools.system as sy
    import pytools.graphs as gp
    import pytools.saveload as sl

# ? --- Integração com Julia ---
from juliacall import Main as jl

# * ========================================================================================
# * Início
# * ========================================================================================
# ? --- Execução do Core ---
jl.include("src/astraeos_core/integrator.jl")
