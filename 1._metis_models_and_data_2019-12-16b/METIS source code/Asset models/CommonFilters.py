########################################################
# Copyright (c) 2013-2017 by Artelys S.A.S.            #
# All Rights Reserved.                                 #
#                                                      #
# This file is part of the Artelys Crystal Platform.   #
# Modifications are prohibited and could break the     #
# software features.                                   #
########################################################


##############################
# ASSET TYPES
##############################
F_BIOMASS_FLEET                = "Biomass fleet"
F_BIOMASS_SUPPLY               = "Biomass supply"
F_CAES                         = "CAES fleet"
F_CCGT_FLEET                   = "CCGT fleet"
F_CLUSTER_COMMITMENT_PLAN      = "Cluster commitment plan"
F_CO2_EMISSIONS                = "CO2 emissions"
F_COAL_FLEET                   = "Coal fleet"
F_COAL_SUPPLY                  = "Coal supply"
F_CSP_FLEET                    = "CSP fleet"
F_DECENTRALIZED_THERMAL_FLEET  = "Decentralized thermal fleet"
F_DEMAND                       = "Demand"
F_DEMAND_RESPONSE              = "Demand-response"
F_DERIVED_GASSES_FLEET         = "Derived gasses fleet"
F_DSR                          = "DSR"
F_ELECTRIC_VEHICLES            = "Electric Vehicles"
F_HEAT_PUMP                    = "Heat Pump"
F_ELECTROLYSIS                 = "Electrolysis"
F_EXPORT_CONTRACT              = "Export contract"
F_GAS_CONSUMPTION              = "Gas consumption"
F_GAS_EXPORTS                  = "Gas exports"
F_GAS_IMPORTS                  = "Gas imports"
F_GAS_MARKET_CONSTANT_MARKUP   = "Gas Market Constant Markup"
F_GAS_PRODUCTION               = "Gas production"
F_GAS_STORAGE                  = "Gas storage"
F_GAS_SUPPLY                   = "Gas supply"
F_GENERIC_STORAGE              = "Generic Storage"
F_GEOTHERMAL_FLEET             = "Geothermal fleet"
F_H2_to_CH4                    = "H2 to CH4"
F_HYDRO_FLEET                  = "Hydro fleet"
F_HYDRO_ROR_FLEET              = "Hydro RoR fleet"
F_HYDROGEN_FLEET               = "Hydrogen fleet"
F_IMPORT_CONTRACT              = "Import contract"
F_IMPORT_PIPELINE              = "Import pipeline"
F_LI_ION_BATTERY               = "Lithium ion battery fleet"
F_LIGNITE_FLEET                = "Lignite fleet"
F_LIGNITE_SUPPLY               = "Lignite supply"
F_LNG_EXPORTS                  = "LNG exports"
F_LNG_IMPORTS                  = "LNG imports"
F_LNG_LIQUEFACTION_TRAIN       = "LNG liquefaction train"
F_LNG_TERMINAL                 = "LNG terminal"
F_LOSS_OF_LOAD                 = "Loss of load"
F_MIN_RESERVE_PROCUREMENT      = "Min reserve procurement"
F_NUCLEAR_FLEET                = "Nuclear fleet"
F_OCGT_FLEET                   = "OCGT fleet"
F_OIL_FLEET                    = "Oil fleet"
F_OIL_SUPPLY                   = "Oil supply"
F_OTHER_FLEET                  = "Other fleet"
F_OTHER_RENEWABLE_FLEET        = "Other renewable fleet"
F_OTHER_THERMAL_FLEET          = "Other thermal fleet"
F_PIPELINE_EQUALITY            = "Pipeline equality"
F_PIPELINE                     = "Pipeline"
F_POWER_DEMAND                 = "Power demand"
F_PUMPED_STORAGE_FLEET         = "Pumped storage fleet"
F_REGULATED_COAL_FLEET         = "Regulated Coal fleet"
F_REGULATED_OIL_FLEET          = "Regulated Oil fleet"
F_RESERVE_DEMAND               = "Reserve demand"
F_RESERVE_DIMENSIONING         = "Reserve Dimensioning"
F_RESERVE_SUPPLY               = "Reserve supply"
F_RESERVE_SYMMETRY_REQUIREMENT = "Reserve Symmetry Requirement"
F_SCENARIO                     = "Scenario"
F_SELL_CONTRACT                = "Sell contract"
F_SOLAR_FLEET                  = "Solar fleet"
F_SUPPLY_CONTRACT_WITH_BOUND   = "Supply contract with bound"
F_TRANSMISSION_EQUALITY        = "Transmission equality"
F_TRANSMISSION                 = "Transmission"
F_TRANSMISSIONSBEHAVIOR        = "TransmissionsBehavior"
F_WASTE_FLEET                  = "Waste fleet"
F_WELL                         = "Well"
F_WIND_OFFSHORE_FLEET          = "Wind offshore fleet"
F_WIND_ONSHORE_FLEET           = "Wind onshore fleet"

##############################
# ASSET TYPES SETS
# /!\ Use sets "{}", not lists "[]"
##############################
# TODO : update the below-defined lists that are not consitent with the current library
PRODUCTION_TYPES = {
		F_BIOMASS_FLEET,
		F_CAES,
		F_CCGT_FLEET,
		F_COAL_FLEET,
		F_DECENTRALIZED_THERMAL_FLEET,
		F_DERIVED_GASSES_FLEET,
		F_GAS_PRODUCTION,
		F_GAS_STORAGE,
		F_GENERIC_STORAGE,
		F_GEOTHERMAL_FLEET, 
		F_HYDRO_FLEET,
		F_HYDRO_ROR_FLEET,
		F_HYDROGEN_FLEET,
		F_LI_ION_BATTERY,
		F_LIGNITE_FLEET,
		F_LNG_LIQUEFACTION_TRAIN,
		F_LNG_TERMINAL,
		F_NUCLEAR_FLEET,
		F_OCGT_FLEET,
		F_OIL_FLEET,
		F_OTHER_FLEET,
		F_OTHER_RENEWABLE_FLEET,
		F_OTHER_THERMAL_FLEET,
		F_PUMPED_STORAGE_FLEET,
		F_REGULATED_COAL_FLEET,
		F_REGULATED_OIL_FLEET,
		F_SOLAR_FLEET,
		F_WASTE_FLEET,
		F_WIND_OFFSHORE_FLEET,
		F_WIND_ONSHORE_FLEET,
		F_ELECTROLYSIS,
		F_H2_to_CH4}

CO2_TYPES = {
		F_BIOMASS_FLEET,
		F_CAES,
		F_CCGT_FLEET,
		F_COAL_FLEET,
		F_DECENTRALIZED_THERMAL_FLEET,
		F_DERIVED_GASSES_FLEET,
		F_GAS_CONSUMPTION,
		F_GENERIC_STORAGE,
		F_GEOTHERMAL_FLEET,
		F_HYDROGEN_FLEET,
		F_LIGNITE_FLEET,
		F_NUCLEAR_FLEET,
		F_OCGT_FLEET,
		F_OIL_FLEET,
		F_REGULATED_COAL_FLEET,
		F_REGULATED_OIL_FLEET,
		F_WASTE_FLEET,
		F_HEAT_PUMP}

FLEXIBLE_RES_TYPES = {
		F_HYDRO_ROR_FLEET,
		F_SOLAR_FLEET,
		F_WIND_OFFSHORE_FLEET,
		F_WIND_ONSHORE_FLEET}

NON_FLEXIBLE_RES_TYPES = {
		F_GEOTHERMAL_FLEET,
		F_HYDRO_ROR_FLEET,
		F_HYDROGEN_FLEET,
		F_OTHER_FLEET,
		F_SOLAR_FLEET,
		F_WASTE_FLEET,
		F_WIND_OFFSHORE_FLEET,
		F_WIND_ONSHORE_FLEET}

STORAGE_TYPES = {
		F_CAES,
		F_CSP_FLEET,
		F_GAS_STORAGE,
		F_HYDRO_FLEET,
		F_GENERIC_STORAGE,
		F_LI_ION_BATTERY,
		F_LNG_TERMINAL,
		F_PUMPED_STORAGE_FLEET}

FUEL_SUPPLY_TYPES = {
		F_BIOMASS_SUPPLY,
		F_COAL_SUPPLY,
		F_GAS_SUPPLY,
		F_LIGNITE_SUPPLY,
		F_OIL_SUPPLY}

TRANSMISSION_TYPES = {
		F_TRANSMISSION,
		F_PIPELINE,
		F_IMPORT_PIPELINE}

FLEXIBLE_DEMAND_TYPES={
		F_DEMAND_RESPONSE,
		F_ELECTRIC_VEHICLES,
		F_HEAT_PUMP}

DEMAND_TYPES = FLEXIBLE_DEMAND_TYPES|{
		F_DEMAND,
		F_POWER_DEMAND,
		F_RESERVE_DEMAND,
		F_GAS_CONSUMPTION}

DEMAND_FOR_RESERVE_SIZING_TYPES = {
		F_DEMAND,
		F_POWER_DEMAND,
		F_DEMAND_RESPONSE}

LOSS_OF_ENERGY_TYPES = {F_LOSS_OF_LOAD}

CURTAILABLE_TYPES = {F_WELL}

FLEXIBLE_EXPORT_TYPES = {
		F_GAS_EXPORTS,
		F_LNG_EXPORTS}

FLEXIBLE_IMPORT_TYPES = {
		F_GAS_IMPORTS,
		F_LNG_IMPORTS}

NON_FLEXIBLE_EXPORT_TYPES = {F_EXPORT_CONTRACT}

NON_FLEXIBLE_IMPORT_TYPES = {F_IMPORT_CONTRACT}

EXPORT_TYPES = FLEXIBLE_EXPORT_TYPES|NON_FLEXIBLE_EXPORT_TYPES

IMPORT_TYPES = FLEXIBLE_IMPORT_TYPES|NON_FLEXIBLE_IMPORT_TYPES

CYCLE_STORAGE_TYPES = {
		F_CAES,
		F_GAS_STORAGE,
		F_PUMPED_STORAGE_FLEET,
		F_GENERIC_STORAGE,
		F_LI_ION_BATTERY}

REVERSE_SURPLUS = {F_LNG_LIQUEFACTION_TRAIN}

THERMALGAP_TYPES = {
		F_CCGT_FLEET, 
		F_OCGT_FLEET,
		F_COAL_FLEET,
		F_OIL_FLEET,
		F_LIGNITE_FLEET,
		F_REGULATED_COAL_FLEET,
		F_REGULATED_OIL_FLEET}

##############################
# ENERGY TYPES SETS
##############################

RESERVE_ENERGIES = {
			SYNC_RESERVE_UP,
			SYNC_RESERVE_DOWN,
			MFRR_UP,
			MFRR_DOWN}

PRODUCED_ENERGIES = {
				ELECTRICITY,
				SYNC_RESERVE_UP,
				SYNC_RESERVE_DOWN,
				MFRR_UP,
				MFRR_DOWN,
				GAS}

CONSUMED_ENERGIES = {
				ELECTRICITY,
				SYNC_RESERVE_UP,
				SYNC_RESERVE_DOWN,
				MFRR_UP,
				MFRR_DOWN,
				GAS,
				OIL,
				BIOMASS,
				LIGNITE,
				COAL,
				LNG}

##############################
# INTERFACE TUPLES
##############################
INTERFACE_SPEC_LIST= { #(interfaceName, isAPrimaryInterface, isInput)
					(ENERGY_DELIVERY     , True , False),
					(ENERGY_PICKUP       , True , True),
					(CO2_DELIVERY        , False, False),
					(FUEL_PICKUP         , False, True),
					(E_SYNC_RESERVE_UP   , True , False),
					(E_SYNC_RESERVE_DOWN , True , False),
					(E_MFRR_UP           , True , False),
					(E_MFRR_DOWN         , True , False),}

##############################
# CONSTANT FOR KPI
##############################
# Asset view : Production cost view
LABEL_PROD_COST                = "Production cost"
LABEL_CONSUMPTION_COST         = "Consumption cost"
LABEL_STORAGE_COST             = "Storage cost"
LABEL_FUEL_COST                = "Fuel cost"
LABEL_CO2_COST                 = "CO2 cost"
LABEL_RUNNING_BOUND_COST       = "Running bound cost"
LABEL_STARTUP_COST             = "Start up cost"
LABEL_SYNC_RESERVE_UP_COST     = "Synchronized upward reserve cost"
LABEL_SYNC_RESERVE_DOWN_COST   = "Synchronized downward reserve cost"
LABEL_MFRR_UP_COST             = "MFRR upward reserve cost"
LABEL_MFRR_DOWN_COST           = "MFRR downward reserve cost"
LABEL_MFRR_UP_NOT_RUNNING_COST = "MFRR up not running cost"
LABEL_ENERGY_SHEDDING_COST     = "Load shedding cost"

