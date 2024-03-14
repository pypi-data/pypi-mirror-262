"""
Module with models for calculating melt Fe-Mg partition coefficients between olivine and melt as:

 (Fe\ :sup:`2+` / Mg)\ :sub:`ol` / (Fe\ :sup:`2+` / Mg)\ :sub:`melt`
"""

from .Kds import *
from .models import FeMg_blundy, FeMg_Toplis, Kd_models
