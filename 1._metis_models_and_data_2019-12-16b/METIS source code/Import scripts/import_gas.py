########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

"""
A specific top-level import script has been created to import gas scenarios. It has exactly the same structure as the import_scenario_template.py script, but with some predefined parameter values that are used for gas model.

For instance, the granularity of simulation is daily, with a single optimization problem of one year, and the temporal DataBase paths are set to the specific folders used for gas temporal data.
"""

from java.io import File
from com.artelys.platform.config import Constantes
from com.artelys.crystal.aggregation.scripting import TemporalBase

#######################
# Context information #
#######################

# Choose the context name
contextName = 'GAS_CONTEXT_NAME'

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
timeStepDuration = 60*24 # in minutes

# Number of timeSteps of the simulation. The duration of the simulation is equal to timeStepDuration*numTimeSteps
numTimeSteps = 365

# Number of days of each optimization problem resolution.
tacticHorizon = 365 # in days

# Number of days for which decisions are kept from the optimization problem resolution.
# By definition, operational horizon is inferior to tactical horizon.
operationalHorizon = 365 # in days

###########################
##### Zone information ####
###########################

# Specify which zones to import from the scenario
# A list of string is expected, but it is also possible to use the wild card ALL meaning that no filtering is done
zoneList = ALL

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
Scenario = 'Gas - EUCO30_2030_market'

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
temporalDataPath = Constantes.REP_DATA + "TemporalData/BasicsGas"
temporalDataPathForDemandByUsage = Constantes.REP_DATA + "TemporalData/Demand/GasDemand"

# Version used in the DataBase ("Source" tag in the DB-Temporal.csv file)
version_DB = 'EUCO30_2030_daily'

# Imported test cases from the DataBase
testCaseList = ["Test case 37", "Test case 38", "Test case 46"]
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
###### Import script ######
###########################

execfile(Constantes.REP_SCRIPTS + "/user/scripts/execution_gas.py")
