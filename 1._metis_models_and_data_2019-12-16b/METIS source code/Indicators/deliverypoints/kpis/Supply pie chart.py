########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

"""

This view shows, for each energy, a pie chart of the different supply types in the context, with their proportions.

"""

from com.artelys.platform.config import Constantes
execfile(Constantes.REP_SCRIPTS+'/results\kpis\imports\BaseKPI.py')


def get_indexing(context):
	return [
	getScopesIndexing(localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2),
	getDeliveryPointsIndexing(context, localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2),
	getEnergiesIndexing(context, includedEnergies=PRODUCED_ENERGIES, localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2),
	getTestCasesIndexing(context, localized=False, selectFirst=True, colorizeIndex=False, groupIndexAsGraphs=2),
	getTechnologiesIndexing(context, includedTechnologies=PRODUCTION_TYPES, localized=False, selectFirst=False, colorizeIndex=True, groupIndexAsGraphs=3)
	]

def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	timeStepDuration = getTimeStepDurationInHours(context)
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = indexFilter.filterIndexList(2, getEnergies(context, includedEnergies=PRODUCED_ENERGIES))
	selectedTestCases      = indexFilter.filterIndexList(3, context.getResultsIndexSet())
	selectedTechnologies   = indexFilter.filterIndexList(4, getTechnologies(context, includedTechnologies=PRODUCTION_TYPES))
	
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includedTechnologies = selectedTechnologies)

	productionsDict = getProductionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope, aggregation=False)
	
	for index in productionsDict:
		kpiDict[index]  = productionsDict[index].getSumValue() * timeStepDuration * MW_TO_W_CONVERSION
	
	return kpiDict

IndicatorLabel = "Supply pie chart (Wh)"
IndicatorUnit = "Wh"
IndicatorDeltaUnit = "Wh"
IndicatorDescription = "Total supply attached to a technology or a contract type"
# IndicatorParameters = []
# IndicatorIcon = "./gfx/energies/co2.png"
# IndicatorCategory = "Results>Technical>Production"
# IndicatorTags = ""