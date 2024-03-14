"""
Module with predefined quantity types
"""

import dataclasses

from dataclasses import dataclass
from typing import Type, Generic, Optional

from . import units_collections, units_types, errors
from .units_types import UnitsT


@dataclass(frozen=True)
class QuantityType(Generic[UnitsT]):
    """
    Class for meta information of a quantity.
    Implemented as dataclass for simple definition of child-classes.
    """

    # Type of the units e.g., units_types.Energy
    units_type: Type[UnitsT]
    # The internal units e.g., units_collections.Energy.J
    internal_units: UnitsT
    # Collection of available units e.g., units_collections.Energy()
    available_units: units_collections.UnitsCollection
    # Default display units e.g., units_collections.Energy.MWh
    default_display_units: Optional[UnitsT] = None

    def __post_init__(self):
        """
        Check the compatibility of the given units
        """
        # Check if type of internal units matches the declared units type
        if not isinstance(self.internal_units, self.units_type):
            msg = (
                f"Type of internal_units ({type(self.internal_units)}) "
                f"does not match the specified units type ({self.units_type})"
            )
            raise errors.QuantityUnitsError(msg)

        # Check if type of display units matches the declared units type
        if self.default_display_units is not None:
            if not isinstance(self.default_display_units, self.units_type):
                msg = (
                    "Type of default_display_units"
                    f" ({type(self.default_display_units)}) does not match the"
                    f" specified units type ({self.units_type})"
                )
                raise errors.QuantityUnitsError(msg)

        # Check if type of all fields of the units collection
        # match the declared units type
        for units_field in dataclasses.fields(self.available_units):
            field_object = getattr(self.available_units, units_field.name)
            if not issubclass(self.units_type, type(field_object)):
                msg = (
                    f"The type ({type(field_object)}) "
                    f" of the field '{units_field.name}' (and maybe others)"
                    f" from the available_units ({self.available_units})"
                    f" do not match the specified units type ({self.units_type})"
                )
                raise errors.QuantityUnitsError(msg)


# region Dimensionless
Dimensionless = QuantityType(
    units_type=units_types.Dimensionless,
    internal_units=units_collections.Dimensionless.dimensionless,
    default_display_units=units_collections.Dimensionless.dimensionless,
    available_units=units_collections.Dimensionless(),
)
# endregion


# region Base Quantities
Length = QuantityType(
    units_type=units_types.Length,
    internal_units=units_collections.Length.m,
    default_display_units=units_collections.Length.m,
    available_units=units_collections.Length(),
)


Mass = QuantityType(
    units_type=units_types.Mass,
    internal_units=units_collections.Mass.kg,
    default_display_units=units_collections.Mass.kg,
    available_units=units_collections.Mass(),
)


Time = QuantityType(
    units_type=units_types.Time,
    internal_units=units_collections.Time.s,
    default_display_units=units_collections.Time.h,
    available_units=units_collections.Time(),
)


Temperature = QuantityType(
    units_type=units_types.Temperature,
    internal_units=units_collections.Temperature.K,
    default_display_units=units_collections.Temperature.deg_C,
    available_units=units_collections.Temperature(),
)


Current = QuantityType(
    units_type=units_types.Current,
    internal_units=units_collections.Current.A,
    default_display_units=units_collections.Current.A,
    available_units=units_collections.Current(),
)
# endregion


# region Base Derived Quantities
Volume = QuantityType(
    units_type=units_types.Volume,
    internal_units=units_collections.Volume.m3,
    default_display_units=units_collections.Volume.m3,
    available_units=units_collections.Volume(),
)


Density = QuantityType(
    units_type=units_types.Density,
    internal_units=units_collections.Density.kg_per_m3,
    default_display_units=units_collections.Density.kg_per_m3,
    available_units=units_collections.Density(),
)


Pressure = QuantityType(
    units_type=units_types.Pressure,
    internal_units=units_collections.Pressure.Pa,
    default_display_units=units_collections.Pressure.bar,
    available_units=units_collections.Pressure(),
)
# endregion


# region Time
Frequency = QuantityType(
    units_type=units_types.Frequency,
    internal_units=units_collections.Frequency.Hz,
    default_display_units=units_collections.Frequency.Hz,
    available_units=units_collections.Frequency(),
)


DurationShare = QuantityType(
    units_type=units_types.DurationShare,
    internal_units=units_collections.DurationShare.h_per_a,
    default_display_units=units_collections.DurationShare.h_per_a,
    available_units=units_collections.DurationShare(),
)


ShareInPeriod = QuantityType(
    units_type=units_types.ShareInPeriod,
    internal_units=units_collections.ShareInPeriod.share_per_a,
    default_display_units=units_collections.ShareInPeriod.share_per_a,
    available_units=units_collections.ShareInPeriod(),
)
# endregion


# region Geometry
Angle = QuantityType(
    units_type=units_types.Angle,
    internal_units=units_collections.Angle.rad,
    default_display_units=units_collections.Angle.deg,
    available_units=units_collections.Angle(),
)


Area = QuantityType(
    units_type=units_types.Area,
    internal_units=units_collections.Area.m2,
    default_display_units=units_collections.Area.m2,
    available_units=units_collections.Area(),
)
# endregion


# region Mechanics & Kinetics
Velocity = QuantityType(
    units_type=units_types.Velocity,
    internal_units=units_collections.Velocity.m_per_s,
    default_display_units=units_collections.Velocity.m_per_s,
    available_units=units_collections.Velocity(),
)


Acceleration = QuantityType(
    units_type=units_types.Acceleration,
    internal_units=units_collections.Acceleration.m_per_s2,
    default_display_units=units_collections.Acceleration.m_per_s2,
    available_units=units_collections.Acceleration(),
)
# endregion


# region Thermodynamics
TemperatureDifference = QuantityType(
    units_type=units_types.TemperatureDifference,
    internal_units=units_collections.TemperatureDifference.delta_deg_C,
    default_display_units=units_collections.TemperatureDifference.delta_deg_C,
    available_units=units_collections.TemperatureDifference(),
)


Energy = QuantityType(
    units_type=units_types.Energy,
    internal_units=units_collections.Energy.J,
    default_display_units=units_collections.Energy.MWh,
    available_units=units_collections.Energy(),
)


Enthalpy = QuantityType(
    units_type=units_types.Enthalpy,
    internal_units=units_collections.Enthalpy.J,
    default_display_units=units_collections.Enthalpy.kJ,
    available_units=units_collections.Enthalpy(),
)


InternalEnergy = QuantityType(
    units_type=units_types.InternalEnergy,
    internal_units=units_collections.InternalEnergy.J,
    default_display_units=units_collections.InternalEnergy.kJ,
    available_units=units_collections.InternalEnergy(),
)


MechanicalWork = QuantityType(
    units_type=units_types.MechanicalWork,
    internal_units=units_collections.MechanicalWork.J,
    default_display_units=units_collections.MechanicalWork.kJ,
    available_units=units_collections.MechanicalWork(),
)


EnthalpyFlow = QuantityType(
    units_type=units_types.EnthalpyFlow,
    internal_units=units_collections.EnthalpyFlow.J_per_s,
    default_display_units=units_collections.EnthalpyFlow.J_per_s,
    available_units=units_collections.EnthalpyFlow(),
)


Power = QuantityType(
    units_type=units_types.Power,
    internal_units=units_collections.Power.W,
    default_display_units=units_collections.Power.kW,
    available_units=units_collections.Power(),
)


HeatFlow = QuantityType(
    units_type=units_types.HeatFlow,
    internal_units=units_collections.HeatFlow.W,
    default_display_units=units_collections.HeatFlow.kW,
    available_units=units_collections.HeatFlow(),
)


ThermalEfficiency = QuantityType(
    units_type=units_types.ThermalEfficiency,
    internal_units=units_collections.ThermalEfficiency.W_per_W,
    default_display_units=units_collections.ThermalEfficiency.kW_per_kW,
    available_units=units_collections.ThermalEfficiency(),
)

HeatFlowLossShare = QuantityType(
    units_type=units_types.HeatFlowLossShare,
    internal_units=units_collections.HeatFlowLossShare.W_per_W,
    default_display_units=units_collections.HeatFlowLossShare.kW_per_kW,
    available_units=units_collections.HeatFlowLossShare(),
)


HeatLossShare = QuantityType(
    units_type=units_types.HeatLossShare,
    internal_units=units_collections.HeatLossShare.Wh_per_Wh,
    default_display_units=units_collections.HeatLossShare.kWh_per_kWh,
    available_units=units_collections.HeatLossShare(),
)


SpecificHeatCapacity = QuantityType(
    units_type=units_types.SpecificHeatCapacity,
    internal_units=units_collections.SpecificHeatCapacity.J_per_kg_K,
    default_display_units=units_collections.SpecificHeatCapacity.J_per_kg_K,
    available_units=units_collections.SpecificHeatCapacity(),
)


CarnotEfficiency = QuantityType(
    units_type=units_types.CarnotEfficiency,
    internal_units=units_collections.CarnotEfficiency.delta_K_per_K,
    default_display_units=units_collections.CarnotEfficiency.delta_K_per_K,
    available_units=units_collections.CarnotEfficiency(),
)


FuelPerformance = QuantityType(
    units_type=units_types.FuelPerformance,
    internal_units=units_collections.FuelPerformance.W,
    default_display_units=units_collections.FuelPerformance.kW,
    available_units=units_collections.FuelPerformance(),
)
# endregion


# region Fluid Dynamics
VolumeFlow = QuantityType(
    units_type=units_types.VolumeFlow,
    internal_units=units_collections.VolumeFlow.m3_per_h,
    default_display_units=units_collections.VolumeFlow.l_per_min,
    available_units=units_collections.VolumeFlow(),
)


MassFlow = QuantityType(
    units_type=units_types.MassFlow,
    internal_units=units_collections.MassFlow.kg_per_s,
    default_display_units=units_collections.MassFlow.kg_per_min,
    available_units=units_collections.MassFlow(),
)


DynamicViscosity = QuantityType(
    units_type=units_types.DynamicViscosity,
    internal_units=units_collections.DynamicViscosity.Pa_s,
    default_display_units=units_collections.DynamicViscosity.Pa_s,
    available_units=units_collections.DynamicViscosity(),
)


KinematicViscosity = QuantityType(
    units_type=units_types.KinematicViscosity,
    internal_units=units_collections.KinematicViscosity.m2_per_s,
    default_display_units=units_collections.KinematicViscosity.m2_per_s,
    available_units=units_collections.KinematicViscosity(),
)
# endregion


# region Heat and Mass Transfer
HeatCapacityRate = QuantityType(
    units_type=units_types.HeatCapacityRate,
    internal_units=units_collections.HeatCapacityRate.W_per_K,
    default_display_units=units_collections.HeatCapacityRate.W_per_K,
    available_units=units_collections.HeatCapacityRate(),
)


HeatTransferCoefficient = QuantityType(
    units_type=units_types.HeatTransferCoefficient,
    internal_units=units_collections.HeatTransferCoefficient.W_per_m2_K,
    default_display_units=units_collections.HeatTransferCoefficient.W_per_m2_K,
    available_units=units_collections.HeatTransferCoefficient(),
)


ThermalConductivity = QuantityType(
    units_type=units_types.ThermalConductivity,
    internal_units=units_collections.ThermalConductivity.W_per_m_K,
    default_display_units=units_collections.ThermalConductivity.W_per_m_K,
    available_units=units_collections.ThermalConductivity(),
)


QuadraticHeatTransferCoefficient = QuantityType(
    units_type=units_types.QuadraticHeatTransferCoefficient,
    internal_units=(
        units_collections.QuadraticHeatTransferCoefficient.W_per_m2_K2
    ),
    default_display_units=(
        units_collections.QuadraticHeatTransferCoefficient.W_per_m2_K2
    ),
    available_units=units_collections.QuadraticHeatTransferCoefficient(),
)
# endregion


# region Financial
Currency = QuantityType(
    units_type=units_types.Currency,
    internal_units=units_collections.Currency.EUR,
    default_display_units=units_collections.Currency.EUR,
    available_units=units_collections.Currency(),
)


HourlyCosts = QuantityType(
    units_type=units_types.HourlyCosts,
    internal_units=units_collections.HourlyCosts.EUR_per_h,
    default_display_units=units_collections.HourlyCosts.EUR_per_h,
    available_units=units_collections.HourlyCosts(),
)


EnergyCosts = QuantityType(
    units_type=units_types.EnergyCosts,
    internal_units=units_collections.EnergyCosts.EUR_per_MWh,
    default_display_units=units_collections.EnergyCosts.EUR_per_MWh,
    available_units=units_collections.EnergyCosts(),
)
# endregion


# region Energy Engineering
EnergyYield = QuantityType(
    units_type=units_types.EnergyYield,
    internal_units=units_collections.EnergyYield.MWh_per_a,
    default_display_units=units_collections.EnergyYield.MWh_per_a,
    available_units=units_collections.EnergyYield(),
)


PowerAreaRatio = QuantityType(
    units_type=units_types.PowerAreaRatio,
    internal_units=units_collections.PowerAreaRatio.W_per_m2,
    default_display_units=units_collections.PowerAreaRatio.W_per_m2,
    available_units=units_collections.PowerAreaRatio(),
)


GeothermalProdIndex = QuantityType(
    units_type=units_types.GeothermalProdIndex,
    internal_units=units_collections.GeothermalProdIndex.m3_per_s_Pa,
    default_display_units=units_collections.GeothermalProdIndex.m3_per_s_Pa,
    available_units=units_collections.GeothermalProdIndex(),
)


LinearPressure = QuantityType(
    units_type=units_types.LinearPressure,
    internal_units=units_collections.LinearPressure.Pa_s_per_l,
    default_display_units=units_collections.LinearPressure.Pa_s_per_l,
    available_units=units_collections.LinearPressure(),
)


QuadraticPressure = QuantityType(
    units_type=units_types.QuadraticPressure,
    internal_units=units_collections.QuadraticPressure.Pa_s2_per_l2,
    default_display_units=units_collections.QuadraticPressure.Pa_s2_per_l2,
    available_units=units_collections.QuadraticPressure(),
)


TemperatureCorrection = QuantityType(
    units_type=units_types.TemperatureCorrection,
    internal_units=units_collections.TemperatureCorrection.inverse_K,
    default_display_units=units_collections.TemperatureCorrection.inverse_K,
    available_units=units_collections.TemperatureCorrection(),
)
# endregion
