# -*- coding: utf-8 -*-

########################################################
# Copyright (c) 2013-2017 by Artelys S.A.S.            #
# All Rights Reserved.                                 #
#                                                      #
# This file is part of the Artelys Crystal Platform.   #
# Modifications are prohibited and could break the     #
# software features.                                   #
########################################################

___version___ = '1.2+'


###############################
# Scope id
###############################
SCOPE_SIMULATION = "SIMULATION"
SCOPE_OPTIMCAPA = "OPTIMCAPA"
###############################
# Behaviors id
###############################

# General
BH_GRADIENTS        = "GRADIENTS"

# Capacities optimization
BH_OPTIM_PMAX      = "OPTIM_PMAX"
BH_OPTIM_STOCK     = "OPTIM_STOCK"

# Stock type
BH_DISCHARGE_TIMES = "DISCHARGE_TIMES"

# Distinguish pmaxIn and pmaxOut
BH_USE_PMAX_IN = "USE_PMAX_IN"

# Cluster behavior
BH_CLUSTER = "CLUSTER"

# Unit behavior
BH_UNIT = "UNIT"

# DC load flow
BH_DCLF = "DCLF"

# Reserve behavior
BH_RESERVE           = "RESERVE"
BH_SYNC_RESERVE_UP   = "SYNC_RESERVE_UP"
BH_SYNC_RESERVE_DOWN = "SYNC_RESERVE_DOWN"
BH_MFRR_UP           = "MFRR_UP"
BH_MFRR_DOWN         = "MFRR_DOWN"

# Must run behavior
BH_MUST_RUN = "MUST_RUN"

# Fuel
BH_FUEL = "FUEL"

# Model objects behaviors
BH_EQUALITY      = "EQUALITY_CONSTRAINT"
BH_IMPORT_EXPORT = "WITH_IMPORT_EXPORT"

# Specific behaviors
BH_CONSTANT_VAR = "CONSTANT_VAR"
BH_USE_ENERGY_PRODUCTION = "USE_ENERGY_PRODUCTION"
BH_VOLUME_TARGET = "VOLUME_TARGET"
BH_GAS_BACKUP_HEATER = "GAS_BACKUP_HEATER"

###############################
# Physical Assets Parameters ID
###############################

#General Parameters
ENERGY_DELIVERY =   "PRODUCTION"
ENERGY_PICKUP   =   "CONSUMPTION"
FUEL_PICKUP     =   "FUEL_CONSUMPTION"
PRODUCTION_COST =   "_productionCost"
VARIABLE_COST   =   "_variableCost"
AVAILABILITY    =   "_availability"
INCENTIVE       =   "_incentive"

#For outages
OUTAGES = "_outages"

#For SimulationBehavior only
PMAX = "_pmax"

#For OPTIM_PMAX Behavior only
PMAXMAX =   "_pmaxmax"
PMAXMIN =   "_pmaxmin"
CAPEX   =   "_capex"
FOC     =   "_foc"

#For Transmissions
LOSSES           =   "_losses"
SUSCEPTANCE      =   "_susceptance"
CONSUMPTION_COST =   "_consumptionCost"

#For Hydro mixed pumping plants
PUMPING_COST     =   "_pumpingCost"

#For CO2Behavior
CO2_DELIVERY    =   "CO2"
##Without fuel
CO2_CONTENT     =   "_co2Content"
##With fuel
FUEL_CO2_CONTENT=   "_fuelCo2Content"

#For Gradients Behavior
GRADIENT_UP     =   "_gradientUp"
GRADIENT_DOWN   =   "_gradientDown"

#For Stock functions
ADD_TO_MODEL              =   "_addToModel" # Not an asset param. Option for the expert user
INITIAL_EQUALS_FINAL      =   "force initial stock = final stock" # Not an asset param. Option for the expert user

STORAGE_CAPACITY          =   "_storageCapacity"
MAX_STORAGE_CAPACITY      =   "_maxStorageCapacity" #for storage optimization
MIN_STORAGE_CAPACITY      =   "_minStorageCapacity" #for storage optimization
INPUT_EFFICIENCY          =   "_inputEfficiency"
OUTPUT_EFFICIENCY         =   "_outputEfficiency"
INITIAL_STORAGE_LEVEL     =   "_initialStorageLevel"
MIN_INITIAL_STORAGE_LEVEL =   "_minInitialStorageLevel"
MAX_INITIAL_STORAGE_LEVEL =   "_maxInitialStorageLevel"
MIN_STORAGE_LEVEL         =   "_minStorageLevel"
STORAGE_CAPEX             =   "_storageCapex"
STORAGE_AVAILABILITY      =   "_storageAvailability"
STORAGE_LOSS_RATE         =   "_lossRate"
STORAGE_COST              =   "_storageCost"
BOUNDED_SUPPLY            =   "_boundedSupply"
PRORATA_SUPPLY            =   "_prorataSupply"
PRORATA_SUPPLY_COEF       =   "_prorataSupplyCoef" #Coef on prorata supply
FIXED_SUPPLY              =   "_fixedSupply"
FIXED_DEMAND              =   "_fixedDemand"

DISCHARGE_TIME            =   "_dischargeTime"
MAX_DISCHARGE_TIME        =   "_maxDischargeTime"
MIN_DISCHARGE_TIME        =   "_minDischargeTime"

PMAX_IN                   =   "_pmaxIn"
PMAX_IN_OUT_RATIO         =   "_pmaxInOutRatio" #For OPTIM_PMAX

WATER_STOCK_FILING_INCENTIVE   = "waterStockFilingIncentive" # just a key for the DEFVALUE dict
WATER_STOCK_PRODUCTION_PENALTY = "waterStockProductionPenalty" # just a key for the DEFVALUE dict

#Fleet models
FUEL_YIELD    = "_fuelYield"
MIN_LOAD      = "_minLoad"

#Cluster Behavior
MIN_OFF_TIME                  =   "_minOffTime"
CLUSTER_STARTING_COST         =   "_clusterStartingCost"
RUNNING_COST                  =   "_runningCost"
MODULATION_COST               =   "_modulationCost"
PRODUCTION_HEAT_RATE          =   "_productionHeatRate"
STARTUP_TIME                  =   "_startupTime"
RUNNING_CAPA_FUEL_CONSUMPTION =   "_runningCapaFuelConsumption"
CO2_CONTENT_RUNNING_BOUND     =   "_co2ContentRunningBound"
RUNNING_CAPACITY_MIN_LOAD     =   "_runningCapacityMinLoad"

#Unit Behavior
PMIN_ON          =   "_pminOn"
MIN_DURATION_ON  =   "_minDurationOn"
MIN_DURATION_OFF =   "_minDurationOff"
STARTING_COST    =   "_startingCost"
STOPPING_COST    =   "_stoppingCost"
STATE_OFF_NAME   =   "_stateOffName" # Not an asset param. Just to have a default value

#Reserve Behavior
##Asset
IS_QUICK_START        =   "_isQuickStart"       # Not an asset param, more like a tag.
IS_FLEET_MODE_ENABLED =   "_isFleetModeEnabled" # Not an asset param, more like a tag.
LOCAL_RESERVE         =   "_localReserve"      # For asset "minimum national reserve procurement"
##Energy pickup/delivery
E_SYNC_RESERVE_UP   =   "SYNC_RESERVE_UP"
E_SYNC_RESERVE_DOWN =   "SYNC_RESERVE_DOWN"
E_MFRR_UP           =   "MFRR_UP"
E_MFRR_DOWN         =   "MFRR_DOWN"

##Dictionnary to link each behavior to its relative reserve energy
ASSOCIATED_BEHAVIOR_FOR_RESERVE_ENERGY = {} 
ASSOCIATED_BEHAVIOR_FOR_RESERVE_ENERGY[E_SYNC_RESERVE_UP  ] = BH_SYNC_RESERVE_UP
ASSOCIATED_BEHAVIOR_FOR_RESERVE_ENERGY[E_SYNC_RESERVE_DOWN] = BH_SYNC_RESERVE_DOWN
ASSOCIATED_BEHAVIOR_FOR_RESERVE_ENERGY[E_MFRR_UP          ] = BH_MFRR_UP
ASSOCIATED_BEHAVIOR_FOR_RESERVE_ENERGY[E_MFRR_DOWN        ] = BH_MFRR_DOWN

##Max shares
SYNC_RESERVE_UP_MAX_SHARE     =   "_maxShareSyncReserveUp"
SYNC_RESERVE_DOWN_MAX_SHARE   =   "_maxShareSyncReserveDown"
MFRR_UP_MAX_SHARE           =   "_maxShareMfrrUp"
MFRR_DOWN_MAX_SHARE         =   "_maxShareMfrrDown"
##Demands
SYNC_UP_DEMAND   =   "_syncReserveUpDemand"
SYNC_DOWN_DEMAND =   "_syncReserveDownDemand"
MFRR_UP_DEMAND   =   "_mfrrUpDemand"
MFRR_DOWN_DEMAND =   "_mfrrDownDemand"
##Costs
SYNC_RESERVE_UP_COST   =   "_syncReserveUpCost"
SYNC_RESERVE_DOWN_COST =   "_syncReserveDownCost"
MFRR_UP_COST           =   "_mfrrUpCost"
MFRR_DOWN_COST         =   "_mfrrDownCost"
##Procurement costs
SYNC_RESERVE_PROCUREMENT_COST = "_syncReserveProcurementCost"
MFRR_PROCUREMENT_COST         = "_mfrrProcurementCost"
##Not running costs
MFRR_UP_NOT_RUNNING_COST   =   "_mfrrUpNotRunningCost"
## Generic ID --> # Not asset params. Used for LABELS
RESERVE_ENERGY           =   "reserveEnergy"
RESERVE_MAX_SHARE        =   "reserveMaxShare"
RESERVE_COST             =   "reserveCost"
RESERVE_IS_UP            =   "reserveIsUp"
RESERVE_DELAY            =   "reserveDelay"
RESERVE_NOT_RUNNING_COST =   "reserveNotRunningCost"
## List of reserve objects
RESERVE_LIST =   "Reserve object list"


###############################
# Financial Assets Parameters ID
###############################
PRICE        = "_price"
COST         = "_cost"
WATER_INFLOW = "_waterInflow"
DEMAND       = "_demand"
EXPORTS      = "_exports"
IMPORTS      = "_imports"
QUOTA        = "_quota"
IMPORT_PRICE = "_importPrice"

###############################
# Physical Assets Parameters DEFAULT VALUES
###############################
DEFVALUE = {}
#General Parameters
DEFVALUE[ENERGY_DELIVERY] =    ENERGY_DELIVERY
DEFVALUE[ENERGY_PICKUP  ] =    ENERGY_PICKUP
DEFVALUE[FUEL_PICKUP    ] =    FUEL_PICKUP
DEFVALUE[PRODUCTION_COST] =    PRODUCTION_COST
DEFVALUE[VARIABLE_COST  ] =    VARIABLE_COST
DEFVALUE[AVAILABILITY   ] =    AVAILABILITY
DEFVALUE[INCENTIVE      ] =    INCENTIVE
DEFVALUE[FUEL_YIELD     ] =    FUEL_YIELD

#For outages
DEFVALUE[OUTAGES] = OUTAGES

#For SimulationBehavior only
DEFVALUE[PMAX] =    PMAX

#For OPTIM_PMAX Behavior only
DEFVALUE[PMAXMAX] =    PMAXMAX
DEFVALUE[PMAXMIN] =    PMAXMIN
DEFVALUE[CAPEX  ] =    CAPEX
DEFVALUE[FOC    ] =    FOC

#For Transmissions
DEFVALUE[LOSSES          ] =    LOSSES
DEFVALUE[SUSCEPTANCE     ] =    SUSCEPTANCE
DEFVALUE[CONSUMPTION_COST] =    CONSUMPTION_COST

#For Hydro mixed pumping plants
DEFVALUE[PUMPING_COST] =   PUMPING_COST

#For CO2Behavior
DEFVALUE[CO2_DELIVERY   ] =    CO2_DELIVERY
##Without fuel
DEFVALUE[CO2_CONTENT    ] =    CO2_CONTENT
##With fuel
DEFVALUE[FUEL_CO2_CONTENT ] =    FUEL_CO2_CONTENT

#For Gradients Behavior
DEFVALUE[GRADIENT_UP    ] =    GRADIENT_UP
DEFVALUE[GRADIENT_DOWN  ] =    GRADIENT_DOWN

#For Stock functions
DEFVALUE[ADD_TO_MODEL             ] =    True # Not an asset param. Option for the expert user
DEFVALUE[STORAGE_CAPACITY         ] =    STORAGE_CAPACITY
DEFVALUE[MAX_STORAGE_CAPACITY     ] =    MAX_STORAGE_CAPACITY
DEFVALUE[MIN_STORAGE_CAPACITY     ] =    MIN_STORAGE_CAPACITY
DEFVALUE[INPUT_EFFICIENCY         ] =    1.0
DEFVALUE[OUTPUT_EFFICIENCY        ] =    1.0
DEFVALUE[INITIAL_STORAGE_LEVEL    ]=     0
DEFVALUE[MIN_INITIAL_STORAGE_LEVEL] =    None
DEFVALUE[MAX_INITIAL_STORAGE_LEVEL] =    None
DEFVALUE[MIN_STORAGE_LEVEL        ] =    None
DEFVALUE[STORAGE_CAPEX            ] =    STORAGE_CAPEX
DEFVALUE[STORAGE_AVAILABILITY     ] =    1.0
DEFVALUE[STORAGE_LOSS_RATE        ] =    STORAGE_LOSS_RATE
DEFVALUE[STORAGE_COST             ] =    STORAGE_COST
DEFVALUE[BOUNDED_SUPPLY           ] =    BOUNDED_SUPPLY
DEFVALUE[PRORATA_SUPPLY           ] =    PRORATA_SUPPLY
DEFVALUE[PRORATA_SUPPLY_COEF      ] =    PRORATA_SUPPLY_COEF
DEFVALUE[FIXED_SUPPLY             ] =    FIXED_SUPPLY
DEFVALUE[FIXED_DEMAND             ] =    FIXED_DEMAND

DEFVALUE[DISCHARGE_TIME           ] =    DISCHARGE_TIME
DEFVALUE[MAX_DISCHARGE_TIME       ] =    MAX_DISCHARGE_TIME
DEFVALUE[MIN_DISCHARGE_TIME       ] =    MIN_DISCHARGE_TIME
DEFVALUE[INITIAL_EQUALS_FINAL     ] =    False

DEFVALUE[PMAX_IN]  = PMAX_IN
DEFVALUE[PMAX_IN_OUT_RATIO] =    1


#Fleet models
DEFVALUE[FUEL_YIELD    ] = FUEL_YIELD
DEFVALUE[MIN_LOAD      ] = MIN_LOAD

#Cluster Behavior
DEFVALUE[MIN_OFF_TIME                  ] =    MIN_OFF_TIME
DEFVALUE[CLUSTER_STARTING_COST         ] =    CLUSTER_STARTING_COST
DEFVALUE[RUNNING_COST                  ] =    RUNNING_COST
DEFVALUE[MODULATION_COST               ] =    MODULATION_COST
DEFVALUE[PRODUCTION_HEAT_RATE          ] =    PRODUCTION_HEAT_RATE
DEFVALUE[RUNNING_CAPA_FUEL_CONSUMPTION ] =    RUNNING_CAPA_FUEL_CONSUMPTION
DEFVALUE[STARTUP_TIME                  ] =    STARTUP_TIME
DEFVALUE[CO2_CONTENT_RUNNING_BOUND     ] =    CO2_CONTENT_RUNNING_BOUND
DEFVALUE[RUNNING_CAPACITY_MIN_LOAD     ] =    RUNNING_CAPACITY_MIN_LOAD

#UnitBehavior
DEFVALUE[PMIN_ON         ] =    PMIN_ON
DEFVALUE[MIN_DURATION_ON ] =    MIN_DURATION_ON
DEFVALUE[MIN_DURATION_OFF] =    MIN_DURATION_OFF
DEFVALUE[STARTING_COST   ] =    STARTING_COST
DEFVALUE[STOPPING_COST   ] =    None 
DEFVALUE[STATE_OFF_NAME  ] =    "OFF"


#ReserveBehaviour
##Asset
DEFVALUE[IS_QUICK_START       ] =    False
DEFVALUE[IS_FLEET_MODE_ENABLED] =    False
DEFVALUE[LOCAL_RESERVE        ] =    LOCAL_RESERVE

##Reserve objects
class Reserve:
    """ /!\ TODO """
    def __init__(self, energy, isUp, isManual, maxShare, cost, delay, notRunningCost):
        self.energy         = energy
        self.isUp           = isUp
        self.isManual       = isManual # Manual reserve like the mffr is opposed to automatic reserves by a longer delay which enables some technologies to start up their units to answer it
        self.maxShare       = maxShare
        self.cost           = cost        
        self.delay          = delay # /!\ In hours
        self.notRunningCost = notRunningCost

##Constants
SYNC_RESERVE_DELAY = 0.083
MFRR_RESERVE_DELAY = 0.25

##Reserves
# Synchronized reserve
R_SYNC_RESERVE_UP   =    Reserve(E_SYNC_RESERVE_UP,   True,  False, SYNC_RESERVE_UP_MAX_SHARE,   SYNC_RESERVE_UP_COST,   SYNC_RESERVE_DELAY, notRunningCost=None)
R_SYNC_RESERVE_DOWN =    Reserve(E_SYNC_RESERVE_DOWN, False, False, SYNC_RESERVE_DOWN_MAX_SHARE, SYNC_RESERVE_DOWN_COST, SYNC_RESERVE_DELAY, notRunningCost=None)
# Manual Frequency Restoration Reserve (mFRR)
R_MFRR_UP           =    Reserve(E_MFRR_UP,           True,  True,  MFRR_UP_MAX_SHARE,           MFRR_UP_COST,           MFRR_RESERVE_DELAY, notRunningCost=MFRR_UP_NOT_RUNNING_COST)
R_MFRR_DOWN         =    Reserve(E_MFRR_DOWN,         False, True,  MFRR_DOWN_MAX_SHARE,         MFRR_DOWN_COST,         MFRR_RESERVE_DELAY, notRunningCost=None)
##Reserve list
DEFVALUE[RESERVE_LIST ] =    [R_SYNC_RESERVE_UP, R_SYNC_RESERVE_DOWN, R_MFRR_UP, R_MFRR_DOWN]

###############################
# Financial Assets Parameters DEFAULT VALUES
###############################
DEFVALUE[PRICE       ] =  PRICE
DEFVALUE[COST        ] =  COST
DEFVALUE[WATER_INFLOW] =  WATER_INFLOW
DEFVALUE[DEMAND      ] =  DEMAND
DEFVALUE[EXPORTS     ] =  EXPORTS
DEFVALUE[IMPORTS     ] =  IMPORTS
DEFVALUE[QUOTA       ] =  QUOTA
DEFVALUE[IMPORT_PRICE] =  IMPORT_PRICE

###############################
# ENERGIES
###############################
ELECTRICITY         = "electricity"
SYNC_RESERVE_UP     = "syncResUp"
SYNC_RESERVE_DOWN   = "syncResDown"
MFRR_UP             = "mfrrResUp"
MFRR_DOWN           = "mfrrResDown"

CO2              = "co2"

GAS              = "gas"
OIL              = "oil"
COAL             = "coal"
LIGNITE          = "lignite"
BIOMASS          = "biomass"
LNG              = "lng"


###############################
# Results names
# /!\ DO NOT CHANGE !! Those are standard COE result names.
# Used in XML & KPI
###############################

OPTIMIZED_PMAX_VAR     = 'varupperbound'
OLD_OPTIMIZED_STORAGE_VAR  =  'varstockbound'
OPTIMIZED_STORAGE_VAR  = 'maxStock' # new COE format with old-result-format = false
#Cluster
RUNNING_BOUND_RESULT   = 'runningBound'
RUNNING_COST_RESULT    = 'runningBoundCost'
RUNNING_STORAGE_RESULT = 'runningStock'
STARTING_COST_RESULT   = 'startUpCost'
#Electric vehicles (non-standard)
RAW_DEMAND_LABEL = 'Raw demand'

###############################
# CONSTANT
###############################
KWH_TO_MWH = 1e-3
