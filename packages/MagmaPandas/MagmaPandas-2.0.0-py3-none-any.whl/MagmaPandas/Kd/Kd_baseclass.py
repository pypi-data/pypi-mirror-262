from abc import ABC, abstractmethod


class Kd_model(ABC):
    @abstractmethod
    def calculate_Kd(
        cls, Melt_mol_fractions, forsterite_initial, T_K, P_bar, *args, **kwargs
    ):
        pass

    @abstractmethod
    def get_error(cls, *args, **kwargs):
        pass

    @abstractmethod
    def get_offset_parameters(cls, n: int, *args, **kwargs):
        pass

    @abstractmethod
    def get_offset(cls, melt_composition, offset_parameters, *args, **kwargs):
        pass
