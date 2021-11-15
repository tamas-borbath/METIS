########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

from java.io import File
from com.artelys.platform.config import Constantes
from com.artelys.crystal.aggregation.scripting import TemporalBase

execfile(Constantes.REP_SCRIPTS + "/user/tools/importUtils.py")
execfile(Constantes.REP_SCRIPTS + "/user/tools/crystal.py")
execfile(Constantes.REP_SCRIPTS + "/user/tools/aggregationMethodology.py")
execfile(Constantes.REP_SCRIPTS + "/user/tools/aggregationUtils.py")
execfile(Constantes.REP_SCRIPTS + "/user/tools/DefaultVar.py")
execfile(Constantes.REP_SCRIPTS + "/user/tools/CommonFilters.py")

######################################
#### Fetch data from the database ####
######################################

# Load temporal data (timeSeries)
temporalInfos = loadTemporalData(temporalDataPath, targetYear)
demandTemporalInfos = loadTemporalData(temporalDataPathForDemandByUsage, targetYear)
temporalInfos = mergeInfos(temporalInfos, demandTemporalInfos)

# Create the mapping for temporal data, according to the target Year, the test case list and the Source
temporalDataMapping = createTemporalDataMapping(testCaseList, targetYear, version_DB)

# Load zones from a shapeFile
zonesInfos = loadZones(zoneFilePath, shapefileID, zoneList)

# Load assets, contracts, transmissions and model object from Excel files
# [WARNING] : only one single temporalInfos should be used for all asset/contract/transmission/modelObject infos
#             since the final mapping is done with a single temporalInfos file in StudyContext(..)
assetsInfos        = loadScenarioAssets(assetFilePath, ALL, zoneList, ALL, temporalInfos)
contractsInfos     = loadScenarioContracts(contractFilePath, ALL, zoneList, ALL, temporalInfos)
transmissionsInfos = loadScenarioTransmissions(transmissionFilePath, ALL, zoneList, ALL, temporalInfos)
modelObjectInfos   = loadModelObjects(modelObjectFilePath, ALL, ALL)


######################################
####### Change data parameters #######
######################################


######################################
######### Perform aggregation ########
######################################

# Perform aggregation
if zoneAggregationMap != {}:
	[assetsInfos, contractsInfos, transmissionsInfos, zonesInfos] = completeAggregation(assetsInfos, contractsInfos, transmissionsInfos, zonesInfos, zoneAggregationMap, temporalInfos, ALL, ALL, ALL, {})

######################################
######### Create the context #########
######################################

# Reorganize assets in a circle around the center of their corresponding zone
Aggregation.centerAroundZones(assetsInfos,contractsInfos,zonesInfos)

# Create the context
createContext(contextName, assetsInfos, contractsInfos, transmissionsInfos, modelObjectInfos, zonesInfos, temporalInfos, temporalDataMapping, startDate, numTimeSteps, timeStepDuration, operationalHorizon, tacticHorizon, timeZone="Etc/GMT-1")
