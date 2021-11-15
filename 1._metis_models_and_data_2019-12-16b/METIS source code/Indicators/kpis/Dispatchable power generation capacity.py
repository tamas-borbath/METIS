########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Dispatchable power generation capacity (W)
-------------------------------------------

Indexed by
	* scope
	* delivery point
	* energy (electricity and gas)
	* test case
	* technology

Return the annual mean dispatchable capacity per delivery point and technology, i.e. the mean capacity of assets that can be switched on at will (i.e. the mean capacity of assets other than "must-run" assets). 
The mean dispatchable capacity is calculated as the sum over the dispatchable assets, of the installed capacity times the mean availability:

.. math:: \\small meanDispatchCapa_{dp} = \\sum_{asset} installedCapa_{asset}^{dp}*mean_t(availability_{t, asset})

Where :math:`\\small meanDispatchCapa_{dp}` is the mean dispatchable capacity for a given dp and :math:`\\small installedCapa_{asset}^{dp}` is the installed capacity of a dispatchable asset.

"""

def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = indexFilter.filterIndexList(2, getEnergies(context, includedEnergies = {ELECTRICITY, GAS}))
	selectedTestCases      = indexFilter.filterIndexList(3, context.getTestCases()) #This differs from for testCase in context.getResultsIndexSet() which requires to have a computed solution!
	selectedTechnologies   = indexFilter.filterIndexList(4, getTechnologies(context, includedTechnologies = PRODUCTION_TYPES))
	
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includedTechnologies = selectedTechnologies, excludedBehaviors = {BH_MUST_RUN})
	
	availableCapacityDict = getAvailableCapacityDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope, aggregation = False)

	for index in availableCapacityDict:
			kpiDict[index] = (availableCapacityDict[index]).getMeanValue() * MW_TO_W_CONVERSION
	
	return kpiDict

def get_indexing(context) :
	baseIndexList = [getScopesIndexing(includedScopes={SCOPE_SIMULATION}), getDeliveryPointsIndexing(context), getEnergiesIndexing(context, includedEnergies = {ELECTRICITY, GAS}), getTestCasesIndexing(context), getTechnologiesIndexing(context, includedTechnologies = PRODUCTION_TYPES)]
	return baseIndexList

IndicatorLabel = "Dispatchable power generation capacity"
IndicatorUnit = "W"
IndicatorDeltaUnit = "W"
IndicatorDescription = "Dispatchable power generation capacity per delivery point detailled by technology"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Inputs>Production"
IndicatorTags = "Power System"