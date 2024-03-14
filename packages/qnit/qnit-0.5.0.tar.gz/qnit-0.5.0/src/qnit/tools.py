"""
Module with interim function to compensate missing Pint functionality
"""

import pint
import pint_pandas
import numpy as np
import pandas as pd

from scipy import interpolate  # type: ignore
from typing import Optional, Union

from . import PintQuantity, errors, data_types


class Series:
    """
    A class with static methods for pandas.Series that
    extends the pint-pandas functionality.
    """

    @staticmethod
    def round(series: pd.Series, units: str, decimals: int = 0) -> pd.Series:
        """
        This function is a workaround for the missing `pd.Series.round()`
        functionality of `PintArray`s.
        See https://github.com/hgrecco/pint-pandas/issues/144
        :param series: Pint-series including the data to round.
        :param units: String including the units.
        :param decimals: Decimals to round.
        :return: Pint-series with rounded numbers.
        """
        series = series.pint.m_as(units)
        series = series.round(decimals=decimals)
        return pd.Series(series, dtype=f"pint[{units}]")


class InterpolationQuantity:
    """
    Class including an interpolation by argument in []
    """

    def __init__(self, y: pd.Series, x: Optional[pd.Series] = None, **kwargs):
        """
        :param y: Series with PintQuantities for y-axis in any units
        :param x: Series with PintQuantities for x-axis in interpolation.
            If None, the index of y is used.
        :param kwargs: kwargs passed to interpolation function
        """
        if x is None:
            x = pd.Series(data=y.index, dtype=y.index.dtype)
        self.xUnits = x.pint.units
        self.yUnits = y.pint.units
        self.interpolationQuantity = (
            InterpolationQuantity.__quantity_interpolation(
                x=x.pint.magnitude, y=y.pint.magnitude, **kwargs
            )
        )

    @staticmethod
    def __quantity_interpolation(x, y, **kwargs):
        """
        Internal interpolation function
        :param x: x values
        :param y: y values
        :param kwargs: kwargs passed to interp1d function
        """
        return interpolate.interp1d(x=x, y=y, **kwargs)

    def __getitem__(self, item: Union[data_types.PintQuantity, pd.Series]):
        """
        :param item: X-value as PintQuantity for the interpolation
        :return: Y-value of the interpolation in PintQuantity
        """
        if isinstance(item, pd.Series):
            x = item.pint.to(self.xUnits).pint.magnitude  # type: ignore[attr-defined]
            return_series = True
        else:
            x = item.to(self.xUnits).magnitude
            return_series = False
        with np.errstate(invalid="ignore"):
            y = self.interpolationQuantity(x)
        if return_series:
            return pd.Series(data=y, dtype=f"pint[{self.yUnits}]", index=x.index)
        else:
            return PintQuantity(y, self.yUnits)


def to(units_aware: Union[pint.Quantity, pd.Series], units: str):
    """
    Convert the units of a pint Quantity or a pint-extended pandas Series
    to target units
    :param units_aware: PintQuantity or pint-extended pandas Series
    :param units: Target units
    :return:
    """
    if isinstance(units_aware, pd.Series):
        if pint_pandas.pint_array.is_pint_type(units_aware):
            return units_aware.pint.to(units)  # type: ignore[attr-defined]
        else:
            raise errors.BaseError(
                f"Cannot convert units of units-naive {repr(units_aware)}."
            )
    else:
        return units_aware.to(units)
