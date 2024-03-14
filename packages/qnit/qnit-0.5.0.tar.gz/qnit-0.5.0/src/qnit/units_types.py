"""
This module provides typing classes for the units types.
"""

from typing import Union, TypeVar


class BaseUnitsType(str):
    """
    Base class for all the units types
    """

    pass


class NoUnits(BaseUnitsType):
    pass


"""
Please add every new units type to `ALL`
"""


# region Dimensionless
class Dimensionless(BaseUnitsType):
    """
    This units type should be used for the dimensionless quantities,
    which cannot be derived from other quantities
    """

    pass


# endregion


# region Base Quantities
class Length(BaseUnitsType):
    pass


class Mass(BaseUnitsType):
    pass


class Time(BaseUnitsType):
    pass


class Temperature(BaseUnitsType):
    pass


class Current(BaseUnitsType):
    pass


# endregion


# region Base Derived Quantities
class Volume(BaseUnitsType):
    pass


class Density(BaseUnitsType):
    pass


class Pressure(BaseUnitsType):
    pass


# endregion


# region Time
class Frequency(BaseUnitsType):
    pass


class DurationShare(Dimensionless):
    pass


class ShareInPeriod(BaseUnitsType):
    pass


# endregion


# region Geometry
class Angle(BaseUnitsType):
    pass


class Area(BaseUnitsType):
    pass


# endregion


# region Mechanics & Kinetics
class Velocity(BaseUnitsType):
    pass


class Acceleration(BaseUnitsType):
    pass


# endregion


# region Thermodynamics
class TemperatureDifference(BaseUnitsType):
    pass


class Energy(BaseUnitsType):
    pass


class Enthalpy(Energy):
    pass


class InternalEnergy(Energy):
    pass


class Work(Energy):
    pass


class MechanicalWork(Work):
    pass


class EnergyFlow(BaseUnitsType):
    pass


class EnthalpyFlow(EnergyFlow):
    pass


class Power(EnergyFlow):
    pass


class HeatFlow(EnergyFlow):
    pass


class EnergyFlowShare(Dimensionless):
    pass


class HeatFlowShare(EnergyFlowShare):
    pass


class ThermalEfficiency(HeatFlowShare):
    pass


class HeatFlowLossShare(HeatFlowShare):
    pass


class SpecificHeatCapacity(BaseUnitsType):
    pass


class EnergyShare(Dimensionless):
    pass


class PowerShare(EnergyFlowShare):
    pass


class HeatLossShare(EnergyShare):
    pass


class CarnotEfficiency(BaseUnitsType):
    pass


class FuelPerformance(EnergyFlow):
    pass


# endregion


# region Fluid Dynamics
class VolumeFlow(BaseUnitsType):
    pass


class MassFlow(BaseUnitsType):
    pass


class DynamicViscosity(BaseUnitsType):
    pass


class KinematicViscosity(BaseUnitsType):
    pass


# endregion


# region Heat and Mass Transfer
class HeatCapacityRate(BaseUnitsType):
    pass


class HeatTransferCoefficient(BaseUnitsType):
    pass


class ThermalConductivity(BaseUnitsType):
    pass


class QuadraticHeatTransferCoefficient(BaseUnitsType):
    pass


# endregion


# region Financial
class Currency(BaseUnitsType):
    pass


class HourlyCosts(BaseUnitsType):
    pass


class EnergyCosts(BaseUnitsType):
    pass


# endregion


# region Energy Engineering
class EnergyYield(BaseUnitsType):
    pass


class PowerAreaRatio(BaseUnitsType):
    pass


class GeothermalProdIndex(BaseUnitsType):
    pass


class LinearPressure(BaseUnitsType):
    pass


class QuadraticPressure(BaseUnitsType):
    pass


class TemperatureCorrection(BaseUnitsType):
    pass


class MinRelativePower(PowerShare):
    pass


class MinRelativeHeatFlow(HeatFlowShare):
    pass


# endregion


"""
Please add every new units type to `ALL`
"""

ALL = Union[
    Acceleration,
    Angle,
    Area,
    CarnotEfficiency,
    Currency,
    Current,
    Density,
    Dimensionless,
    DurationShare,
    DynamicViscosity,
    Energy,
    EnergyCosts,
    EnergyYield,
    Enthalpy,
    EnthalpyFlow,
    FuelPerformance,
    Frequency,
    GeothermalProdIndex,
    HeatCapacityRate,
    HeatFlow,
    HeatFlowLossShare,
    HeatTransferCoefficient,
    HourlyCosts,
    InternalEnergy,
    KinematicViscosity,
    Length,
    LinearPressure,
    Mass,
    MechanicalWork,
    MinRelativePower,
    MinRelativeHeatFlow,
    NoUnits,
    PowerAreaRatio,
    Power,
    Pressure,
    QuadraticHeatTransferCoefficient,
    QuadraticPressure,
    ShareInPeriod,
    SpecificHeatCapacity,
    Temperature,
    TemperatureCorrection,
    TemperatureDifference,
    ThermalConductivity,
    ThermalEfficiency,
    Time,
    Velocity,
    Volume,
    VolumeFlow,
    MassFlow,
]
UnitsT = TypeVar("UnitsT", bound=BaseUnitsType)
