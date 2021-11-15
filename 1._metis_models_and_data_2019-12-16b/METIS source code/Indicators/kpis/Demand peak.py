########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Demand peak (W)
----------------

Indexed by
	* scope
	* delivery point
	* test case
	* energy
	* demand type

Return the maximum value of the demand over the year, for a given scope, delivery point, energy, test case and the demand asset type.
NB : In case of flexible demand, we here consider realized demand (after optimization)

"""

TOTAL_LABEL = "Total of selected technologies"

def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	timeStepDuration = getTimeStepDurationInHours(context)
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = indexFilter.filterIndexList(2, getEnergies(context, includedEnergies = PRODUCED_ENERGIES))
	selectedTestCases      = indexFilter.filterIndexList(3, context.getTestCases()) #This differs from for testCase in context.getResultsIndexSet() which requires to have a computed solution!
	selectedTechnologies   = indexFilter.filterIndexList(4, getTechnologies(context, includeFinancialAssetTypes=True, includedTechnologies=DEMAND_TYPES) + [TOTAL_LABEL])

	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includeFinancialAssets=True, includedTechnologies = selectedTechnologies)

	demandDict = getDemandDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope)
	
	for index in demandDict:
		kpiDict[index] = demandDict[index].getMaxValue() * MW_TO_W_CONVERSION
	
	totalDict = defaultdict(lambda: getZeroTs(context))
	for index in demandDict:
		kpiDict[index] = demandDict[index].getMaxValue() * timeStepDuration * MW_TO_W_CONVERSION
		# Total demand
		scope, dpName, energy, testCase, techno = index
		indexTotal = (scope, dpName, energy, testCase, TOTAL_LABEL)
		totalDict[indexTotal] = totalDict[indexTotal] + demandDict[index]
	
	if TOTAL_LABEL in selectedTechnologies:
		for index in totalDict:
			kpiDict[index] = totalDict[index].getMaxValue() * timeStepDuration * MW_TO_W_CONVERSION
	
	return kpiDict

def get_indexing(context) :
	demandTechnologies = getTechnologies(context, includeFinancialAssetTypes=True, includedTechnologies=DEMAND_TYPES)
	selectedTechnologies = demandTechnologies + [TOTAL_LABEL]
	baseIndexList = [
			getScopesIndexing(), getDeliveryPointsIndexing(context), getEnergiesIndexing(context, includedEnergies=PRODUCED_ENERGIES), getTestCasesIndexing(context), 
			BaseIndexDefault("Data", selectedTechnologies, False, False, True, 0)]
	return baseIndexList

IndicatorLabel = "Demand peak"
IndicatorUnit = "W"
IndicatorDeltaUnit = "W"
IndicatorDescription = "Optimized demand peak (substracting load curtailment and V2G production)"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Inputs>Demand"
IndicatorTags = "Power System, Gas System, Power Markets"