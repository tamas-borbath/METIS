# -*- coding: utf-8 -*-

########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

from java.io import File
from com.artelys.platform.config import Constantes
from com.artelys.crystal.aggregation.scripting import TemporalBase
import time

execfile(Constantes.REP_SCRIPTS + "/user/tools/importUtils.py")
execfile(Constantes.REP_SCRIPTS + "/user/tools/metisUtils.py")
execfile(Constantes.REP_SCRIPTS + "/user/tools/crystal.py")
execfile(Constantes.REP_SCRIPTS + "/user/tools/aggregationMethodology.py")
execfile(Constantes.REP_SCRIPTS + "/user/tools/aggregationUtils.py")
execfile(Constantes.REP_SCRIPTS + "/user/tools/DefaultVar.py")
execfile(Constantes.REP_SCRIPTS + "/user/tools/CommonFilters.py")

######################################
######## Create assets groups ########
######################################

useFuelModelAssetList     = [F_BIOMASS_FLEET,F_CCGT_FLEET,F_COAL_FLEET,F_LIGNITE_FLEET,F_OCGT_FLEET,F_OIL_FLEET] if useFuelModel else []

usePmaxInPmaxOutAssetList = [F_PUMPED_STORAGE_FLEET, F_HYDRO_FLEET] if usePmaxInPmaxOut else []

clusterAssetList = [F_BIOMASS_FLEET,F_CCGT_FLEET,F_COAL_FLEET,F_HYDRO_FLEET,F_LIGNITE_FLEET,F_OCGT_FLEET,F_OIL_FLEET,F_PUMPED_STORAGE_FLEET] if useClusterModel else []

gradientAssetList = ALL if useGradients else []

mustRunAssetList = [F_DERIVED_GASSES_FLEET,F_GEOTHERMAL_FLEET,F_HYDROGEN_FLEET,F_OTHER_RENEWABLE_FLEET,F_OTHER_THERMAL_FLEET] 
mustRunAssetList += [F_SOLAR_FLEET,F_WIND_ONSHORE_FLEET,F_WIND_OFFSHORE_FLEET,F_HYDRO_ROR_FLEET,F_WASTE_FLEET] if useResMustRunModel else []

if useDemandModule:
	if not useFlexibleDemandAsset:
		notFlexibleAssetList = [asset for asset in FLEXIBLE_DEMAND_TYPES]
	else:
		notFlexibleAssetList = []

if useReserveModel:
	reserveAssetList = [F_BIOMASS_FLEET,F_NUCLEAR_FLEET,F_COAL_FLEET,F_LIGNITE_FLEET,F_CCGT_FLEET,F_OCGT_FLEET,F_OIL_FLEET,F_HYDRO_FLEET,F_PUMPED_STORAGE_FLEET,F_DSR]
	if not useResMustRunModel: # Add RES asset only if they are not in must-run
		reserveAssetList += [F_SOLAR_FLEET,F_WIND_ONSHORE_FLEET,F_WIND_OFFSHORE_FLEET,F_HYDRO_ROR_FLEET,F_WASTE_FLEET]
else:
	reserveAssetList = []

# Remove specific reserve assets if useReserveModel is set to False
if useReserveModel:
	assetsTypesFilter = ALL
	contractsTypesFilter = ALL
	contractsNamesFilter = ALL
	modelObjectsTypesFilter = ALL
else:
	removedAssetsTypes = [F_DSR]
	removedContractsTypes = [F_RESERVE_DEMAND]
	removedContractsNames = ["(?i)"+resType +"(?-i)" for resType in RESERVE_ENERGIES] # remove contracts whose name includes a reserve energy name (case insensitive)
	removedElecModelObjectsTypes = [F_MIN_RESERVE_PROCUREMENT,F_RESERVE_DIMENSIONING,F_RESERVE_SUPPLY,F_RESERVE_SYMMETRY_REQUIREMENT]

	# remove demand assets if demand module is used
	if useDemandModule:
		removedContractsTypes.append(F_POWER_DEMAND)

	assetsTypesFilter = allButFilter(removedAssetsTypes)
	contractsTypesFilter = allButFilter(removedContractsTypes)
	contractsNamesFilter = allButFilter(removedContractsNames, False)
	modelObjectsTypesFilter = allButFilter(removedElecModelObjectsTypes)


######################################
#### Fetch data from the database ####
######################################

# Load temporal data (timeSeries)
temporalInfos = loadTemporalData(temporalDataPath, targetYear)

# Load demand timeseries if useDemandModule is set to true
if useDemandModule:
	demandTemporalInfos = loadTemporalData(temporalDataPathForDemandByUsage, targetYear)
	temperatureTemporalInfos = loadTemporalData(temporalDataPathForTemperature, targetYear)
	otherDataInfos = loadTemporalData(temporalDataPathForOtherData, targetYear)
	temporalInfos = mergeInfos(temporalInfos, demandTemporalInfos)
	temporalInfos = mergeInfos(temporalInfos, temperatureTemporalInfos)
	temporalInfos = mergeInfos(temporalInfos, otherDataInfos)

# Create the mapping for temporal data, according to the target Year, the test case list and the Source
temporalDataMapping = createTemporalDataMapping(testCaseList, targetYear, version_DB)

# Load zones from a shapeFile
zonesInfos = loadZones(zoneFilePath, shapefileID, zoneList)

# Load assets, contracts, transmissions and model object from Excel files
# [WARNING] : only one single temporalInfos should be used for all asset/contract/transmission/modelObject infos
#             since the final mapping is done with a single temporalInfos file in StudyContext(..) 
assetsInfos        = loadScenarioAssets(assetFilePath, ALL, zoneList, assetsTypesFilter, temporalInfos)
contractsInfos     = loadScenarioContracts(contractFilePath, contractsNamesFilter, zoneList, contractsTypesFilter, temporalInfos)
transmissionsInfos = loadScenarioTransmissions(transmissionFilePath, ALL, zoneList, ALL, temporalInfos)
modelObjectInfos   = loadModelObjects(modelObjectFilePath, ALL, modelObjectsTypesFilter)

# Load demand asset if useDemandModule is set to true
if useDemandModule:
	assetsDemandInfos        = loadScenarioAssets(assetDemandFilePath, ALL, zoneList, assetsTypesFilter, temporalInfos)
	contractsDemandInfos     = loadScenarioContracts(contractDemandFilePath, ALL, zoneList, ALL, temporalInfos)

	# Merge infos
	assetsInfos    = mergeInfos(assetsInfos, assetsDemandInfos)
	contractsInfos = mergeInfos(contractsInfos, contractsDemandInfos)

######################################
####### Change data parameters #######
######################################

# AddBehaviors
for scope in Crystal.getScopes():
	addBehaviors(scope, BH_RESERVE    , assetsInfos, reserveAssetList         )
	addBehaviors(scope, BH_CLUSTER    , assetsInfos, clusterAssetList         )
	addBehaviors(scope, BH_GRADIENTS  , assetsInfos, gradientAssetList        )
	addBehaviors(scope, BH_MUST_RUN   , assetsInfos, mustRunAssetList         )
	addBehaviors(scope, BH_USE_PMAX_IN, assetsInfos, usePmaxInPmaxOutAssetList)
	addBehaviors(scope, BH_FUEL       , assetsInfos, useFuelModelAssetList    )
	# All non flexible demand assets are forced to be must-run, ie. non flexible
	if useDemandModule:
		addBehaviors(scope, BH_MUST_RUN   , assetsInfos   , notFlexibleAssetList )
		addBehaviors(scope, BH_MUST_RUN   , contractsInfos, notFlexibleAssetList )

######################################
######### Perform aggregation ########
######################################

# save scenario data (used in reserve sizing)
mo = saveScenarioData(modelObjectInfos, zoneList, zoneAggregationMap, assetsInfos, contractsInfos, temporalInfos, testCaseList, targetYear, version_DB)
modelObjectInfos.add(mo)

# Perform aggregation
if zoneAggregationMap != {}:
	# Categories for thermal units
	agePatternList = ["old", "medium", "young"]
	aggregationTypesToSeparate = {
		F_CCGT_FLEET : agePatternList,
		F_COAL_FLEET : agePatternList,
		F_LIGNITE_FLEET : agePatternList,
		F_OCGT_FLEET : agePatternList
		}

	if useReserveModel: # Extra categories need to be created for  DSR assets
		aggregationTypesToSeparate.update({F_DSR: ['Process Technology','Other','Storage']})

	[assetsInfos, contractsInfos, transmissionsInfos, zonesInfos] = completeAggregation(assetsInfos, contractsInfos, transmissionsInfos, zonesInfos, zoneAggregationMap, temporalInfos, ALL, ALL, ALL, aggregationTypesToSeparate)

######################################
######### Create the context #########
######################################

# Reorganize assets in a circle around the center of their corresponding zone
Aggregation.centerAroundZones(assetsInfos,contractsInfos,zonesInfos)

# Create the context
createContext(contextName, assetsInfos, contractsInfos, transmissionsInfos, modelObjectInfos, zonesInfos, temporalInfos, temporalDataMapping, startDate, numTimeSteps, timeStepDuration, operationalHorizon, tacticHorizon, timeZone="Etc/GMT-1")

# Import KPI groups
if kpiGroupsFilePath is not None:
	importKpiGroups(kpiGroupsFilePath)

print "Import Done !"