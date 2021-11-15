########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Consumption peak (Wh)
----------------------

Indexed by
	* scope
	* delivery point
	* energy (including fuels)
	* technology
	* test case

Return the peak of energy demand for a given technology or contract.
We here consider the flexible demand after optimization (using the consumption of the corresponding assets).

"""

TOTAL_LABEL = "Total of selected technologies"

def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	timeStepDuration = getTimeStepDurationInHours(context)
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = indexFilter.filterIndexList(2, getEnergies(context, includedEnergies=PRODUCED_ENERGIES))
	selectedTestCases      = indexFilter.filterIndexList(3, context.getResultsIndexSet())
	selectedTechnologies   = indexFilter.filterIndexList(4, getTechnologies(context, includeFinancialAssetTypes = True, includedTechnologies=DEMAND_TYPES|PRODUCTION_TYPES|{F_GAS_CONSUMPTION}) + [TOTAL_LABEL])
	
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includeFinancialAssets=True, includedTechnologies = selectedTechnologies)
	
	consumptionDict = getConsumptionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope)
	
	totalDict = defaultdict(lambda: getZeroTs(context))
	for index in consumptionDict:
		kpiDict[index] = consumptionDict[index].getMaxValue() * timeStepDuration * MW_TO_W_CONVERSION
		# Total demand
		scope, dpName, energy, testCase, techno = index
		indexTotal = (scope, dpName, energy, testCase, TOTAL_LABEL)
		totalDict[indexTotal] = totalDict[indexTotal] + consumptionDict[index]
	
	if TOTAL_LABEL in selectedTechnologies:
		for index in totalDict:
			kpiDict[index] = totalDict[index].getMaxValue() * timeStepDuration * MW_TO_W_CONVERSION
	
	return kpiDict

def get_indexing(context) :
	demandTechnologies = getTechnologies(context, includeFinancialAssetTypes = True, includedTechnologies=DEMAND_TYPES|PRODUCTION_TYPES|{F_GAS_CONSUMPTION})
	selectedTechnologies = demandTechnologies + [TOTAL_LABEL]
	baseIndexList = [
			getScopesIndexing(), getDeliveryPointsIndexing(context), getEnergiesIndexing(context, includedEnergies=PRODUCED_ENERGIES), getTestCasesIndexing(context), 
			BaseIndexDefault("Data", selectedTechnologies, False, False, True, 0)]
	return baseIndexList

IndicatorLabel = "Consumption peak"
IndicatorUnit = "Wh"
IndicatorDeltaUnit = "Wh"
IndicatorDescription = "Consumption peak attached to a technology or a contract type"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Results"
IndicatorTags = " Power System, Gas System, Power Markets "