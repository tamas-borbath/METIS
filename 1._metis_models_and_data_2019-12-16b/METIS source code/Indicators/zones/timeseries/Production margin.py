########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

"""
Margin at each time step between available capacity and energy production for a given zone, for a given energy and a given technology:

.. math::
	\\small minMargin_{t, dp, techno, energy} = availability_{t, dp, techno, energy} \times pmax_{t, dp, techno, energy} - production_{t, dp, techno, energy}

"""

from com.artelys.platform.config import Constantes
execfile(Constantes.REP_SCRIPTS+'/results\kpis\imports\BaseKPI.py')

ViewLabel = "Production margin (W)"

indexValues = {}

def get_indexing(context) :
	return [
	getScopesIndexing(localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2),
	getZonesIndexing(context, localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2),
	getEnergiesIndexing(context, includedEnergies=PRODUCED_ENERGIES, localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2),
	getTestCasesIndexing(context, localized=False, selectFirst=True, colorizeIndex=False, groupIndexAsGraphs=2),
	getTechnologiesIndexing(context, includeFinancialAssetTypes = True, includedTechnologies = PRODUCTION_TYPES)
	]

def getData(view) :
	context = view.getContext()
	
	# Index filter
	selectedScopes         = view.filterIndexList(0, getScopes())
	selectedZones          = view.filterIndexList(1, getZones(context))
	selectedEnergies       = view.filterIndexList(2, getEnergies(context, includedEnergies=PRODUCED_ENERGIES))
	selectedTestCases      = view.filterIndexList(3, getTestCasesWithResults(context))
	selectedTechnologies   = view.filterIndexList(4, getTechnologies(context, includeFinancialAssetTypes = True, includedTechnologies = PRODUCTION_TYPES))
	
	selectedDeliveryPoints = getDpSetFromZoneList(context, selectedZones)
	
	# Compute data
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includedTechnologies = selectedTechnologies)
	
	availCapacitiesDict = getAvailableCapacityDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope)
	productionDict = getProductionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope)
	
	availCapacitiesDictZone = getZoneDictFromDpDict(context, availCapacitiesDict, 1)
	productionsDictZone     = getZoneDictFromDpDict(context, productionDict, 1)
	
	ret = []
	for index in availCapacitiesDictZone:
		# Note : index = (scope, deliveryPoint, energyName, testCase, technology)
		# NB : energyName of availCapacitiesDict is the main produced energy of the asset
		if index in productionsDictZone:
			resultTs = (availCapacitiesDictZone[index] - productionsDictZone[index]) * MW_TO_W_CONVERSION
			ret += [[list(index), resultTs]]

	return ret

def getTimeContext(context) :
	timeContext = [ context.getStartingDate() , context.getTimeStepDuration() , context.getTimeStepCount() ]
	return timeContext 

