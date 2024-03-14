"""
Module with units collections for each quantity
"""

import dataclasses

from dataclasses import dataclass

from . import units_types, errors


@dataclass(frozen=True)
class UnitsCollection:
    """
    Returns a collection of available units
    """

    def units_obj(self, units: str) -> units_types.ALL:
        """
        Return a units type object in a UnitsCollection
        from its string representation.
        :param units: The units string
        :return: The units type object
        """
        for field in dataclasses.fields(self):
            if field.name == units:
                return getattr(self, field.name)

        msg = f"Units ({units}) is not part of {self}."
        raise errors.QuantityUnitsError(msg)


# region Dimensionless
@dataclass(frozen=True)
class Dimensionless(UnitsCollection):
    """
    This units collection should be used for dimensionless quantities
    which cannot be derived from other quantities
    """

    dimensionless: units_types.Dimensionless = units_types.Dimensionless(
        "dimensionless"
    )


@dataclass(frozen=True)
class DimensionlessRatio(Dimensionless):
    """
    A units collection for dimensionless quantities with support for the "percent" units
    """

    percent: units_types.Dimensionless = units_types.Dimensionless("percent")


@dataclass(frozen=True)
class Share(DimensionlessRatio):
    """
    A units collection for dimensionless quantities with support for the "percent" units
    """

    pass


# endregion


# region Base Quantities
@dataclass(frozen=True)
class Length(UnitsCollection):
    m: units_types.Length = units_types.Length("m")
    km: units_types.Length = units_types.Length("km")
    dm: units_types.Length = units_types.Length("dm")
    cm: units_types.Length = units_types.Length("cm")
    mm: units_types.Length = units_types.Length("mm")


@dataclass(frozen=True)
class Mass(UnitsCollection):
    kg: units_types.Mass = units_types.Mass("kg")
    g: units_types.Mass = units_types.Mass("g")
    tonne: units_types.Mass = units_types.Mass("tonne")


@dataclass(frozen=True)
class Time(UnitsCollection):
    s: units_types.Time = units_types.Time("s")
    min: units_types.Time = units_types.Time("min")
    h: units_types.Time = units_types.Time("h")
    d: units_types.Time = units_types.Time("d")
    week: units_types.Time = units_types.Time("week")
    month: units_types.Time = units_types.Time("month")
    year: units_types.Time = units_types.Time("a")


@dataclass(frozen=True)
class Temperature(UnitsCollection):
    K: units_types.Temperature = units_types.Temperature("K")
    deg_C: units_types.Temperature = units_types.Temperature("°C")


@dataclass(frozen=True)
class Current(UnitsCollection):
    A: units_types.Current = units_types.Current("A")
    mA: units_types.Current = units_types.Current("mA")


# endregion


# region Base Derived Quantities
@dataclass(frozen=True)
class Volume(UnitsCollection):
    cm3: units_types.Volume = units_types.Volume("cm³")
    dm3: units_types.Volume = units_types.Volume("dm³")
    m3: units_types.Volume = units_types.Volume("m³")
    l: units_types.Volume = units_types.Volume("l")


@dataclass(frozen=True)
class Density(UnitsCollection):
    kg_per_m3: units_types.Density = units_types.Density("kg/m³")
    kg_per_l: units_types.Density = units_types.Density("kg/l")
    g_per_l: units_types.Density = units_types.Density("g/l")
    t_per_m3: units_types.Density = units_types.Density("t/m³")


@dataclass(frozen=True)
class Pressure(UnitsCollection):
    bar: units_types.Pressure = units_types.Pressure("bar")
    mbar: units_types.Pressure = units_types.Pressure("mbar")
    Pa: units_types.Pressure = units_types.Pressure("Pa")
    kPa: units_types.Pressure = units_types.Pressure("kPa")
    MPa: units_types.Pressure = units_types.Pressure("MPa")
    psi: units_types.Pressure = units_types.Pressure("psi")


# endregion


# region Time
@dataclass(frozen=True)
class Frequency(UnitsCollection):
    cycle_per_s: units_types.Frequency = units_types.Frequency("1/s")
    Hz: units_types.Frequency = units_types.Frequency("Hz")
    rpm: units_types.Frequency = units_types.Frequency("rpm")


@dataclass(frozen=True)
class DurationShare(Share):
    h_per_a: units_types.DurationShare = units_types.DurationShare("h/a")


@dataclass(frozen=True)
class ShareInPeriod(UnitsCollection):
    share_per_a: units_types.ShareInPeriod = units_types.ShareInPeriod("1/a")


# endregion


# region Geometry
@dataclass(frozen=True)
class Angle(UnitsCollection):
    rad: units_types.Angle = units_types.Angle("rad")
    deg: units_types.Angle = units_types.Angle("deg")
    arcmin: units_types.Angle = units_types.Angle("arcmin")
    arcsec: units_types.Angle = units_types.Angle("arcsec")


@dataclass(frozen=True)
class Area(UnitsCollection):
    m2: units_types.Area = units_types.Area("m²")
    km2: units_types.Area = units_types.Area("km²")
    mm2: units_types.Area = units_types.Area("mm²")
    ha: units_types.Area = units_types.Area("ha")


# endregion


# region Mechanics & Kinetics
@dataclass(frozen=True)
class Velocity(UnitsCollection):
    m_per_s: units_types.Velocity = units_types.Velocity("m/s")
    km_per_h: units_types.Velocity = units_types.Velocity("km/h")


@dataclass(frozen=True)
class Acceleration(UnitsCollection):
    m_per_s2: units_types.Acceleration = units_types.Acceleration("m/s²")


# endregion


# region Thermodynamics
@dataclass(frozen=True)
class TemperatureDifference(UnitsCollection):
    delta_deg_C: units_types.TemperatureDifference = (
        units_types.TemperatureDifference("delta_degC")
    )


@dataclass(frozen=True)
class Energy(UnitsCollection):
    Wh: units_types.Energy = units_types.Energy("Wh")
    kWh: units_types.Energy = units_types.Energy("kWh")
    MWh: units_types.Energy = units_types.Energy("MWh")
    GWh: units_types.Energy = units_types.Energy("GWh")
    J: units_types.Energy = units_types.Energy("J")
    kJ: units_types.Energy = units_types.Energy("kJ")
    MJ: units_types.Energy = units_types.Energy("MJ")
    GJ: units_types.Energy = units_types.Energy("GJ")


@dataclass(frozen=True)
class Enthalpy(UnitsCollection):
    J: units_types.Enthalpy = units_types.Enthalpy("J")
    kJ: units_types.Enthalpy = units_types.Enthalpy("kJ")
    MJ: units_types.Enthalpy = units_types.Enthalpy("MJ")
    GJ: units_types.Enthalpy = units_types.Enthalpy("GJ")
    cal: units_types.Enthalpy = units_types.Enthalpy("cal")
    kcal: units_types.Enthalpy = units_types.Enthalpy("kcal")


@dataclass(frozen=True)
class InternalEnergy(UnitsCollection):
    J: units_types.InternalEnergy = units_types.InternalEnergy("J")
    kJ: units_types.InternalEnergy = units_types.InternalEnergy("kJ")
    cal: units_types.InternalEnergy = units_types.InternalEnergy("cal")
    kcal: units_types.InternalEnergy = units_types.InternalEnergy("kcal")


@dataclass(frozen=True)
class MechanicalWork(UnitsCollection):
    J: units_types.MechanicalWork = units_types.MechanicalWork("J")
    kJ: units_types.MechanicalWork = units_types.MechanicalWork("kJ")


@dataclass(frozen=True)
class EnthalpyFlow(UnitsCollection):
    J_per_s: units_types.EnthalpyFlow = units_types.EnthalpyFlow("J/s")
    cal_per_s: units_types.EnthalpyFlow = units_types.EnthalpyFlow("cal/s")


@dataclass(frozen=True)
class Power(UnitsCollection):
    W: units_types.Power = units_types.Power("W")
    kW: units_types.Power = units_types.Power("kW")
    MW: units_types.Power = units_types.Power("MW")
    GW: units_types.Power = units_types.Power("GW")
    VA: units_types.Power = units_types.Power("VA")
    kVA: units_types.Power = units_types.Power("kVA")


@dataclass(frozen=True)
class HeatFlow(UnitsCollection):
    W: units_types.HeatFlow = units_types.HeatFlow("W")
    kW: units_types.HeatFlow = units_types.HeatFlow("kW")
    MW: units_types.HeatFlow = units_types.HeatFlow("MW")
    GW: units_types.HeatFlow = units_types.HeatFlow("GW")
    J_per_s: units_types.HeatFlow = units_types.HeatFlow("J/s")


@dataclass(frozen=True)
class ThermalEfficiency(Share):
    W_per_W: units_types.ThermalEfficiency = units_types.ThermalEfficiency("W/W")
    kW_per_kW: units_types.ThermalEfficiency = units_types.ThermalEfficiency(
        "kW/kW"
    )
    MW_per_MW: units_types.ThermalEfficiency = units_types.ThermalEfficiency(
        "MW/MW"
    )


@dataclass(frozen=True)
class HeatFlowLossShare(Share):
    W_per_W: units_types.HeatFlowLossShare = units_types.HeatFlowLossShare("W/W")
    kW_per_kW: units_types.HeatFlowLossShare = units_types.HeatFlowLossShare(
        "kW/kW"
    )
    MW_per_MW: units_types.HeatFlowLossShare = units_types.HeatFlowLossShare(
        "MW/MW"
    )


@dataclass(frozen=True)
class HeatLossShare(Share):
    Wh_per_Wh: units_types.HeatLossShare = units_types.HeatLossShare("Wh/Wh")
    kWh_per_kWh: units_types.HeatLossShare = units_types.HeatLossShare("kWh/kWh")
    MWh_per_MWh: units_types.HeatLossShare = units_types.HeatLossShare("MWh/MWh")


@dataclass(frozen=True)
class SpecificHeatCapacity(UnitsCollection):
    J_per_kg_K: units_types.SpecificHeatCapacity = (
        units_types.SpecificHeatCapacity("J/(kg·K)")
    )
    kJ_per_kg_K: units_types.SpecificHeatCapacity = (
        units_types.SpecificHeatCapacity("kJ/(kg·K)")
    )


@dataclass(frozen=True)
class CarnotEfficiency(UnitsCollection):
    delta_K_per_K: units_types.CarnotEfficiency = units_types.CarnotEfficiency(
        "delta_K/K"
    )


@dataclass(frozen=True)
class FuelPerformance(UnitsCollection):
    W: units_types.FuelPerformance = units_types.FuelPerformance("W")
    kW: units_types.FuelPerformance = units_types.FuelPerformance("kW")
    MW: units_types.FuelPerformance = units_types.FuelPerformance("MW")
    GW: units_types.FuelPerformance = units_types.FuelPerformance("GW")


# endregion


# region Fluid Dynamics
@dataclass(frozen=True)
class VolumeFlow(UnitsCollection):
    m3_per_h: units_types.VolumeFlow = units_types.VolumeFlow("m³/h")
    l_per_min: units_types.VolumeFlow = units_types.VolumeFlow("l/min")
    m3_per_s: units_types.VolumeFlow = units_types.VolumeFlow("m³/s")
    l_per_s: units_types.VolumeFlow = units_types.VolumeFlow("l/s")


@dataclass(frozen=True)
class MassFlow(UnitsCollection):
    kg_per_s: units_types.MassFlow = units_types.MassFlow("kg/s")
    kg_per_min: units_types.MassFlow = units_types.MassFlow("kg/min")
    kg_per_h: units_types.MassFlow = units_types.MassFlow("kg/h")
    tonne_per_min: units_types.MassFlow = units_types.MassFlow("tonne/min")
    tonne_per_h: units_types.MassFlow = units_types.MassFlow("tonne/h")


@dataclass(frozen=True)
class DynamicViscosity(UnitsCollection):
    Pa_s: units_types.DynamicViscosity = units_types.DynamicViscosity("Pa·s")
    mPa_s: units_types.DynamicViscosity = units_types.DynamicViscosity("mPa·s")


@dataclass(frozen=True)
class KinematicViscosity(UnitsCollection):
    m2_per_s: units_types.KinematicViscosity = units_types.KinematicViscosity(
        "m²/s"
    )
    St: units_types.KinematicViscosity = units_types.KinematicViscosity("St")


# endregion


# region Heat and Mass Transfer
@dataclass(frozen=True)
class HeatCapacityRate(UnitsCollection):
    W_per_K: units_types.HeatCapacityRate = units_types.HeatCapacityRate("W/K")


@dataclass(frozen=True)
class HeatTransferCoefficient(UnitsCollection):
    W_per_m2_K: units_types.HeatTransferCoefficient = (
        units_types.HeatTransferCoefficient("W/(m²·K)")
    )


@dataclass(frozen=True)
class ThermalConductivity(UnitsCollection):
    W_per_m_K: units_types.ThermalConductivity = units_types.ThermalConductivity(
        "W/(m·K)"
    )


@dataclass(frozen=True)
class QuadraticHeatTransferCoefficient(UnitsCollection):
    W_per_m2_K2: units_types.QuadraticHeatTransferCoefficient = (
        units_types.QuadraticHeatTransferCoefficient("W/(m²·K²)")
    )


# endregion


# region Financial
@dataclass(frozen=True)
class Currency(UnitsCollection):
    EUR: units_types.Currency = units_types.Currency("EUR")
    ct: units_types.Currency = units_types.Currency("ct")
    USD: units_types.Currency = units_types.Currency("USD")


@dataclass(frozen=True)
class HourlyCosts(UnitsCollection):
    EUR_per_h: units_types.HourlyCosts = units_types.HourlyCosts("EUR/h")


@dataclass(frozen=True)
class EnergyCosts(UnitsCollection):
    EUR_per_MWh: units_types.EnergyCosts = units_types.EnergyCosts("EUR/MWh")
    ct_per_kWh: units_types.EnergyCosts = units_types.EnergyCosts("ct/kWh")
    EUR_per_kWh: units_types.EnergyCosts = units_types.EnergyCosts("EUR/kWh")


# endregion


# region Energy Engineering
@dataclass(frozen=True)
class EnergyYield(UnitsCollection):
    kWh_per_a: units_types.EnergyYield = units_types.EnergyYield("kWh/a")
    MWh_per_a: units_types.EnergyYield = units_types.EnergyYield("MWh/a")
    GWh_per_a: units_types.EnergyYield = units_types.EnergyYield("GWh/a")


@dataclass(frozen=True)
class PowerAreaRatio(UnitsCollection):
    W_per_m2: units_types.PowerAreaRatio = units_types.PowerAreaRatio("W/m²")
    kW_per_m2: units_types.PowerAreaRatio = units_types.PowerAreaRatio("kW/m²")
    MW_per_m2: units_types.PowerAreaRatio = units_types.PowerAreaRatio("MW/m²")
    W_per_cm2: units_types.PowerAreaRatio = units_types.PowerAreaRatio("W/cm²")


@dataclass(frozen=True)
class GeothermalProdIndex(UnitsCollection):
    m3_per_s_Pa: units_types.GeothermalProdIndex = (
        units_types.GeothermalProdIndex("m³/(s·Pa)")
    )


@dataclass(frozen=True)
class LinearPressure(UnitsCollection):
    Pa_s_per_l: units_types.LinearPressure = units_types.LinearPressure(
        "(Pa·s)/l"
    )


@dataclass(frozen=True)
class QuadraticPressure(UnitsCollection):
    Pa_s2_per_l2: units_types.QuadraticPressure = units_types.QuadraticPressure(
        "(Pa·s²)/l²"
    )


@dataclass(frozen=True)
class TemperatureCorrection(UnitsCollection):
    inverse_K: units_types.TemperatureCorrection = (
        units_types.TemperatureCorrection("1/K")
    )


@dataclass(frozen=True)
class MinRelativePower(Share):
    W_per_W: units_types.MinRelativePower = units_types.MinRelativePower("W/W")
    kW_per_kW: units_types.MinRelativePower = units_types.MinRelativePower(
        "kW/kW"
    )
    MW_per_MW: units_types.MinRelativePower = units_types.MinRelativePower(
        "MW/MW"
    )


@dataclass(frozen=True)
class MinRelativeHeatFlow(Share):
    W_per_W: units_types.MinRelativeHeatFlow = units_types.MinRelativeHeatFlow(
        "W/W"
    )
    kW_per_kW: units_types.MinRelativeHeatFlow = units_types.MinRelativeHeatFlow(
        "kW/kW"
    )
    MW_per_MW: units_types.MinRelativeHeatFlow = units_types.MinRelativeHeatFlow(
        "MW/MW"
    )


# endregion
