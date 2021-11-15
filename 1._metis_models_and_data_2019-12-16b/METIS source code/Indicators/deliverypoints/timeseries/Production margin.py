########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

"""
Margin at each time step between available capacity and energy production for a given delivery point, for a given energy and a given technology:

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
	getDeliveryPointsIndexing(context, localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2),
	getEnergiesIndexing(context, includedEnergies=PRODUCED_ENERGIES, localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2),
	getTestCasesIndexing(context, localized=False, selectFirst=True, colorizeIndex=False, groupIndexAsGraphs=2),
	getTechnologiesIndexing(context, includeFinancialAssetTypes = True, includedTechnologies = PRODUCTION_TYPES)
	]

def getData(view) :
	context = view.getContext()
	
	# Index filter
	selectedScopes         = view.filterIndexList(0, getScopes())
	selectedDeliveryPoints = view.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = view.filterIndexList(2, getEnergies(context, includedEnergies=PRODUCED_ENERGIES))
	selectedTestCases      = view.filterIndexList(3, getTestCasesWithResults(context))
	selectedTechnologies   = view.filterIndexList(4, getTechnologies(context, includeFinancialAssetTypes = True, includedTechnologies = PRODUCTION_TYPES))
	
	# Compute data
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includedTechnologies = selectedTechnologies)
	
	availCapacitiesDict = getAvailableCapacityDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope)
	productionDict = getProductionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope)
	
	ret = []
	for index in availCapacitiesDict:
		# Note : index = (scope, deliveryPoint, energyName, testCase, technology)
		# NB : energyName of availCapacitiesDict is the main produced energy of the asset
		if index in productionDict:
			resultTs = (availCapacitiesDict[index] - productionDict[index]) * MW_TO_W_CONVERSION
			ret += [[list(index), resultTs]]

	return ret

def getTimeContext(context) :
	timeContext = [ context.getStartingDate() , context.getTimeStepDuration() , context.getTimeStepCount() ]
	return timeContext 

