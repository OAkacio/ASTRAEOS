#
# * ============================================
# * Bibliotecas
# * ============================================
import os
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import *
from tqdm import tqdm
try:
    from .pytools import system as sy
    from .pytools import graphs as gp
    from .pytools import saveload as sl
except:
    import pytools.system as sy
    import pytools.graphs as gp
    import pytools.saveload as sl
from juliacall import Main as jl

# ? --- Chamando Função jl ---
jl.include("src/astraeos_core/integrator.jl")
