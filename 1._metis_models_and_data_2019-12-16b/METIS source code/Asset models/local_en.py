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
Crystal = Crystal.Instance()
Crystal.importAndExecute("DefaultVar.py")

#############################################
# Default parameters names for getAssetData
#############################################

###############################
# Assets Parameters LABELS
###############################
LABELS = {}

#### PHYSICAL ASSETS ####
#General Parameters
LABELS[ENERGY_DELIVERY] =    "PRODUCTION"
LABELS[ENERGY_PICKUP  ] =    "CONSUMPTION"
LABELS[PRODUCTION_COST] =    "Production cost"
LABELS[VARIABLE_COST  ] =    "Variable cost"
LABELS[AVAILABILITY   ] =    "Availability"
LABELS[FUEL_YIELD     ] =    "Fuel yield"

#For outages
DEFVALUE[OUTAGES] = "Unplanned outages"

#For SimulationBehavior only
LABELS[PMAX] = "Pmax"

#For OPTIM_PMAX Behavior only
LABELS[PMAXMAX] =   "Pmaxmax"
LABELS[PMAXMIN] =   "Pmaxmin"
LABELS[CAPEX  ] =   "CAPEX"
LABELS[FOC    ] =   "FOC"
LABELS[PMAX_IN_OUT_RATIO] =   "OptimPmax In Out ratio"

#For Transmissions
LABELS[LOSSES          ] =   "Losses"
LABELS[SUSCEPTANCE     ] =   "Susceptance"
LABELS[CONSUMPTION_COST] =   "Consumption cost"

#For Hydro mixed pumping plants
LABELS[PUMPING_COST] =   "Pumping cost"

#For CO2Behavior
LABELS[CO2_DELIVERY   ] =   "CO2"
##Without fuel
LABELS[CO2_CONTENT    ] =   "CO2 content"
##With fuel
LABELS[FUEL_CO2_CONTENT ] =   "Fuel CO2 content"

#For Gradients Behavior
LABELS[GRADIENT_UP    ] =   "Gradient up"
LABELS[GRADIENT_DOWN  ] =   "Gradient down"

#For Stock functions
LABELS[ADD_TO_MODEL         ] =   "addToModel" # Not an asset param. Option for the expert user
LABELS[STORAGE_CAPACITY     ] =   "Storage capacity"
LABELS[MAX_STORAGE_CAPACITY ] =   "Max storage capacity" # For storage optimization
LABELS[MIN_STORAGE_CAPACITY ] =   "Min storage capacity" # For storage optimization
LABELS[INPUT_EFFICIENCY     ] =   "Input efficiency"
LABELS[OUTPUT_EFFICIENCY    ] =   "Output efficiency"
LABELS[INITIAL_STORAGE_LEVEL] =   "Initial storage level"
LABELS[MIN_STORAGE_LEVEL    ] =   "Minimal storage level"
LABELS[STORAGE_CAPEX        ] =   "Storage CAPEX"
LABELS[STORAGE_AVAILABILITY ] =   "Storage availability"
LABELS[STORAGE_LOSS_RATE    ] =   "Loss rate"
LABELS[STORAGE_COST         ] =   "Cost on storage level at each time step"
LABELS[BOUNDED_SUPPLY       ] =   "Bounded supply added to storage"
LABELS[PRORATA_SUPPLY       ] =   "Pro-rata supply added to storage"
LABELS[PRORATA_SUPPLY_COEF  ] =   "Ratio PmaxSolar/PmaxTurbine"
LABELS[FIXED_SUPPLY         ] =   "Fixed supply added to storage"
LABELS[FIXED_DEMAND         ] =   "Fixed demand added to storage"

LABELS[MIN_INITIAL_STORAGE_LEVEL] =   "Minimal initial storage level"
LABELS[MAX_INITIAL_STORAGE_LEVEL] =   "Maximal initial storage level"

LABELS[DISCHARGE_TIME      ] =   "Discharge time"
LABELS[MAX_DISCHARGE_TIME  ] =   "Max discharge time"
LABELS[MIN_DISCHARGE_TIME  ] =   "Min discharge time"

LABELS[PMAX_IN]       = "Pmax In"

#Fleet model
LABELS[FUEL_YIELD ] =   "Fuel yield"
LABELS[MIN_LOAD   ] =   "Min load"

#Cluster Behavior
LABELS[MIN_OFF_TIME                        ] =   "Min off time"
LABELS[CLUSTER_STARTING_COST               ] =   "Starting cost"
LABELS[RUNNING_COST                        ] =   "Running cost"
LABELS[MODULATION_COST                     ] =   "Modulation cost"
LABELS[PRODUCTION_HEAT_RATE                ] =   "Heat rate"
LABELS[RUNNING_CAPA_FUEL_CONSUMPTION       ] =   "Running capacity fuel consumption"
LABELS[STARTUP_TIME                        ] =   "Startup time"
LABELS[CO2_CONTENT_RUNNING_BOUND           ] =   "CO2 content for the running bound"
LABELS[RUNNING_CAPACITY_MIN_LOAD           ] =   "Running capacity min load"

#UnitBehavior
LABELS[PMIN_ON         ] =   "Pmin On"
LABELS[MIN_DURATION_ON ] =   "Min duration On"
LABELS[MIN_DURATION_OFF] =   "Min duration Off"
LABELS[STARTING_COST   ] =   "Starting cost"
LABELS[STOPPING_COST   ] =   "Stopping cost"
LABELS[STATE_OFF_NAME  ] =   "State Off Name" # Not an asset param. Just to have a default value

#ReserveBehavior
##Asset
LABELS[LOCAL_RESERVE  ] =   "National procurement minimum (w.r.t the total requirement)"
##Energy pickup/delivery
LABELS[E_SYNC_RESERVE_UP  ] =   "Synchronized upward reserve energy"
LABELS[E_SYNC_RESERVE_DOWN] =   "Synchronized downward reserve energy"
LABELS[E_MFRR_UP          ] =   "mFFR upward reserve energy"
LABELS[E_MFRR_DOWN        ] =   "mFFR upward reserve energy"
##Max shares
LABELS[SYNC_RESERVE_UP_MAX_SHARE  ] =   "Synchronized upward reserve max share"
LABELS[SYNC_RESERVE_DOWN_MAX_SHARE] =   "Synchronized downward reserve max share"
LABELS[MFRR_UP_MAX_SHARE          ] =   "mFFR and synchronized upward reserve max share"
LABELS[MFRR_DOWN_MAX_SHARE        ] =   "mFFR and synchronized downward reserve max share"
##Costs
LABELS[SYNC_RESERVE_UP_COST  ] =   "Synchronized upward reserve cost"
LABELS[SYNC_RESERVE_DOWN_COST] =   "Synchronized downward reserve cost"
LABELS[MFRR_UP_COST          ] =   "mFFR upward reserve cost"
LABELS[MFRR_DOWN_COST        ] =   "mFFR upward reserve cost"
##Procurement costs
LABELS[SYNC_RESERVE_PROCUREMENT_COST  ] =   "Synchronized reserve procurement cost"
LABELS[MFRR_PROCUREMENT_COST          ] =   "mFRR reserve procurement cost"
## Generic ID --> # Not asset params. Used for LABELS
LABELS[RESERVE_ENERGY   ] =   "Reserve Energy"
LABELS[RESERVE_MAX_SHARE] =   "Reserve Max Share"
LABELS[RESERVE_COST     ] =   "Reserve Cost"
LABELS[RESERVE_IS_UP    ] =   "Reserve IsUp"
LABELS[RESERVE_DELAY    ] =   "Reserve Delay"
LABELS[RESERVE_NOT_RUNNING_COST ] =   "Reserve Not Running Cost"
## List of reserve objects
LABELS[RESERVE_LIST] =   "Reserve object list"


#### FINANCIAL ASSETS ####
LABELS[PRICE       ] = "Price"
LABELS[COST        ] = "Cost"
LABELS[WATER_INFLOW] = "Water inflow"
LABELS[DEMAND      ] = "Demand"
LABELS[EXPORTS     ] = "Exports"
LABELS[IMPORTS     ] = "Imports"
LABELS[QUOTA       ] = "Quota"

#############################################
# Constraints names for user constraints
#############################################

# For gradients
CONSTRAINT_GRADIENT_UB  = "GradientUp "
CONSTRAINT_GRADIENT_LB  = "GradientDown "

# For Stock functions
CONSTRAINT_MIN_STORAGE_CAPACITY         = "OptimStorageLB "
CONSTRAINT_DISCHSTOCK_VALUE             = "DischargeTime "
CONSTRAINT_INITIAL_STORAGE_LEVEL        = "InitialStorageLevel "
CONSTRAINT_MIN_STORAGE_LEVEL            = "MinStorageLevel "
CONSTRAINT_STORAGE_AVAILABILITY         = "StorageAvailability "
CONSTRAINT_CLUSTER_OPTIM_PMAX           = "OptimPmaxBoundOnPbar "
CONSTRAINT_PRORATA_SUPPLY               = "ProrataSupplyBound"
CONSTRAINT_PRORATA_SUPPLY_INI           = "ProrataSupplyBoundIni"

# Specific storage constraints
CONSTRAINT_VARIABLE_INJECTION_CAPACITY  = "variableStorageInjectionCapacity"
CONSTRAINT_VARIABLE_WITHDRAWAL_CAPACITY = "variableStorageWithdrawalCapacity"
CONSTRAINT_FORCE_INITIAL_EQUAL_FINAL    = "ForceInitialLevelEqualsFinal"
CONSTRAINT_ADD_MIN_INIT_STORAGE_BOUND   = "AddMinInitStorageBound"
CONSTRAINT_ADD_MAX_INIT_STORAGE_BOUND   = "AddMaxInitStorageBound"

# For Production
CONSTRAINT_MUST_RUN_PROD = "MustRunProd"
CONSTRAINT_MIN_USAGE     = "MinLoad"
CONSTRAINT_CO2_CLUSTER_NO_FUEL = "co2ClusterNoFuel"

# For Consumption
CONSTRAINT_CONSUMPTION_PMAX         = "ConsumUpperBoundWithOptimPmax "
CONSTRAINT_UNIT_FUEL_CONSUMPTION    = "UnitFuelConsum "
CONSTRAINT_CLUSTER_FUEL_CONSUMPTION = "ClusterFuelConsum "

# For Reserve functions
CONSTRAINT_RUNNING_NOT_RUNNING_RESERVE_DEFINITION = "RunningAndNotRunningReserveDefinition "
CONSTRAINT_MAX_OVERALL_RESERVE_RATIO              = "MaxOverallReserveRatio " # + reserveName
CONSTRAINT_MAX_RUNNING_RESERVE_RATIO              = "MaxRunningReserveRatio " # + reserveName
CONSTRAINT_UP_RESERVE_OVERALL_CAPACITY            = "UpReserveOverallCapa "
CONSTRAINT_UP_RESERVE_RUNNING_CAPACITY            = "UpReserveRunningCapa "
CONSTRAINT_DOWN_RESERVE_OVERALL_CAPACITY          = "DownReserveOverallCapa "
CONSTRAINT_DOWN_RESERVE_RUNNING_CAPACITY          = "DownReserveRunningCapa "
CONSTRAINT_MIN_LOAD_RESERVE                       = "MinLoadReserve "
CONSTRAINT_UP_RESERVE_DSR_CAPACITY                = "UpReserveDsrCapa "
CONSTRAINT_DOWN_RESERVE_DSR_CAPACITY              = "DownReserveDsrCapa "
CONSTRAINT_UP_RESERVE_TRANSMISSION_CAPACITY       = "UpReserveTransmissionCapa "
CONSTRAINT_DOWN_RESERVE_TRANSMISSION_CAPACITY     = "DownReserveTransmissionCapa "
CONSTRAINT_UP_RESERVE_STORAGE_LIMIT               = "UpResStorageLimit "
CONSTRAINT_DOWN_RESERVE_STORAGE_LIMIT             = "DownResStorageLimit "
CONSTRAINT_FLEET_RESERVE_RUNNING_CAPACITY         = "FleetReserveRunningCapacity"

# For generic constraints
CONSTRAINT_FORCE_CONSTANT = "VariableForcedConstant"
CONSTRAINT_REVERSE_FLOW = "ReverseFlowInequality"