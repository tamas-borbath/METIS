########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Supply (Wh)
-----------

Indexed by
	* scope
	* delivery point
	* energy (any energy, fuel and reserve type)
	* test case
	* technology

Return for a given delivery point, the annual volumes of production per technology, as well as the imports to the delivery point through the transmissions and the fuel supply.
It is similar to the KPI 'Production (detailed)' but it also includes imports and fuel supply.

The KPI is particularly adapted for gas models as national gas demand is in large parts satisfied by imports.
"""

def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	timeStepDuration = getTimeStepDurationInHours(context)
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = indexFilter.filterIndexList(2, getEnergies(context, includedEnergies=Crystal.listEnergyIDs(context)))
	selectedTestCases      = indexFilter.filterIndexList(3, context.getResultsIndexSet())
	selectedTechnologies   = indexFilter.filterIndexList(4, getTechnologies(context, includeFinancialAssetTypes = True, excludedTechnologies = DEMAND_TYPES))
	
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includeFinancialAssets=True, includedTechnologies = selectedTechnologies)
	
	productionsDict = getProductionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope)
	
	for index in productionsDict.keys():
		kpiDict[index] = productionsDict[index].getSumValue() * timeStepDuration * MW_TO_W_CONVERSION
	
	return kpiDict

def get_indexing(context) :
	baseIndexList = [getScopesIndexing(), getDeliveryPointsIndexing(context), getEnergiesIndexing(context, includedEnergies=Crystal.listEnergyIDs(context)), getTestCasesIndexing(context), getTechnologiesIndexing(context, includeFinancialAssetTypes = True, excludedTechnologies = DEMAND_TYPES)]
	return baseIndexList

IndicatorLabel = "Supply"
IndicatorUnit = "Wh"
IndicatorDeltaUnit = "Wh"
IndicatorDescription = "Total supply attached to a technology or a contract type"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Results>Production"
IndicatorTags = "Power System, Gas System, Power Markets"