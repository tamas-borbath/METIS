########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

"""
A specific top-level import script has been created to import power system scenarios with power demand decomposed by end-use. It has a similar structure as the import_scenario_template.py, but with additional import parameters used to change some asset parameters before the context creation.

Thanks to these specific parameters, additional behaviors can be activated:

 - *useFuelModel*: Fuel consumption is explicitly modeled for power plants
 - *useReserveModel*: Activate the reserve production for all assets. Need to be set to True when power reserve is modelled
 - *useClusterModel*: Enable cluster model, allowing to take into account dynamic constraints and starting costs
 - *useGradients*: Enable gradient constraints for energy production
 - *useResMustRunModel*: Power renewable production is fatal, then RES assets always produce at their maximal available capacity
 - *usePmaxInPmaxOut*: Use distinct input and output capacities for hydro assets (*Hydro fleet* and *Pumped storage fleet*)

There is also a dedicated part for power demand assets:

- *useDemandModule*: If set to True, the power demand is decomposed by end-use
- *useFlexibleDemandAsset*: If set to True, all possible flexible end-uses are flexible (smart recharge for electric vehicles and sanitary hot water, smart thermal storage for heat pumps, ...)
"""

from java.io import File
from com.artelys.platform.config import Constantes
from com.artelys.crystal.aggregation.scripting import TemporalBase

# Uncomment the following line to cleanup the memory and force reload database
# Aggregation.flushTemporalBase()

#######################
# Context information #
#######################

# Choose the context name
contextName = 'CONTEXT_NAME'

# Target year of the context
targetYear = 2030

# Starting date of the simulation
# startDate : Java Data format : constructor Date(year, month, day)
#					- year : target year - 1900
#					- month : int from 0 to 11 
#					- day : int from 1 to 31 
startDate = Date(targetYear-1900,0,1) # Java date Date(year, month, day)

###########################
### Simulation horizons ###
###########################

# Duration in minutes of one time step of the simulation
timeStepDuration = 60 # in minutes

# Number of timeSteps of the simulation. The duration of the simulation is equal to timeStepDuration*numTimeSteps
numTimeSteps = 8760

# Number of days of each optimization problem resolution.
tacticHorizon = 15 # in days

# Number of days for which decisions are kept from the optimization problem resolution.
# By definition, operational horizon is inferior to tactical horizon.
operationalHorizon = 7 # in days

###########################
##### Zone information ####
###########################

# Specify which zones to import from the scenario
zoneList = ['BE','FR','BG','EE','DE','IT','GR','CZ','CH','AT','FI','HU','IE','ES','DK','NL','PT','NO','SI','LV','HR','LT','LU','SE','SK','PL','GB','RO','BA','ME','MK','RS','MT','CY']

# Path of the shapefile where zone shapes need to be extracted from
zoneFilePath = Constantes.REP_DATA + "/Shapefiles/CRENIT.shp"

# In a shapefile, each zone is indexed by an ID or several IDs.
# shapefileID is the name of the ID that should be used to filter zone in the shapefile
# Two shapefiles are mainly used in METIS:
#   - CRENIT.shp : For iso2 country codes. shapefileID : "ISO2"
#   - NUTS_RG_03M_2010.shp : For nuts2 geocode. shapefileID : "NUTS_ID"
shapefileID = "ISO2"

###########################
### Scenario information ##
###########################

# Scenario name
Scenario = 'Power - EUCO30_2030'

# Path to the asset Excel files for the given scenario
# If one of them is not necessary for the given context, the path variable should be set to None
assetFilePath        = Constantes.REP_DATA + 'Scenarios/' + Scenario + "/assets.xlsx"
contractFilePath     = Constantes.REP_DATA + 'Scenarios/' + Scenario + "/contracts.xlsx"
transmissionFilePath = Constantes.REP_DATA + 'Scenarios/' + Scenario + "/transmissions.xlsx"
modelObjectFilePath  = Constantes.REP_DATA + 'Scenarios/' + Scenario + "/modelObjects.xlsx"

###########################
### Temporal information ##
###########################

# Temporal DataBase path
temporalDataPath = Constantes.REP_DATA + "TemporalData/Basics"

# Version used in the DataBase ("Source" tag in the DB-Temporal.csv file)
version_DB = 'EUCO30_2030'

# Imported test cases from the DataBase
# testCaseList = ["Test case 42", "Test case 43"]
testCaseList = ["Test case 37"]
TemporalBase.getInstance().setTestCases(testCaseList)

###########################
##### Zone aggregation ####
###########################

# Specify how zones should be aggregated together.
# zoneAggregationMap is dictionary, whose keys are the new zone names and its elements are the corresponding aggregated zones
# 					e.g. {'Iberia': ['ES','PT'], 'NordPool': ['NO','FI','SE'] }
# The new aggregated zones (e.g 'Iberia', 'NordPool') should not contain any underscore " _ " in their name.
zoneAggregationMap = {}

###########################
####### Asset groups ######
###########################

useFuelModel     = True
usePmaxInPmaxOut = True
useReserveModel = False
useClusterModel = True
useGradients = False
useResMustRunModel = False

############################
####### Demand module ######
############################

# Set to True to use the power demand decomposition by end-use
# Only available for REF16_2030, EUCO30_2030 and EUCO30_2050
useDemandModule = True

# All demand asset are flexible if set to True
useFlexibleDemandAsset = True

if useDemandModule:
	# Path to the temporal database for demand by usage
	temporalDataPathForDemandByUsage = Constantes.REP_DATA + "TemporalData/Demand/PowerDemand"

	# Path to the temporal database for temperatures
	temporalDataPathForTemperature = Constantes.REP_DATA + "TemporalData/Demand/Temperature"

	# Path to the temporal database for additional parameters (arrivals/departures for electric vehicles, heating demand for HP, etc.)
	temporalDataPathForOtherData = Constantes.REP_DATA + "TemporalData/Demand/Other"

	# Path to demand assets
	assetDemandFilePath    = Constantes.REP_DATA + 'Scenarios/' + Scenario + "/powerDemandDecomposition/assets_powerDemandDecomposition.xlsx"
	contractDemandFilePath = Constantes.REP_DATA + 'Scenarios/' + Scenario + "/powerDemandDecomposition/contracts_powerDemandDecomposition.xlsx"


#######################################################################
#######  KPI groups file path (ex of groups: EU28, EU30, ...)   #######
#######################################################################

# If no kpi groups need to be imported, the variable should be set at None
kpiGroupsFilePath = Constantes.REP_DATA + "/kpi_groups_definition.csv"

###########################
###### Import script ######
###########################

execfile(Constantes.REP_SCRIPTS + "/user/scripts/execution_power_system_with_demand_decomposition_by_end-use.py")
