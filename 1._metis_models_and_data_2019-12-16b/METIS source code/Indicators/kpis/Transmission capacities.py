########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Transmission capacities (W)
---------------------------------------

Indexed by
	* scope
	* delivery point
	* energy (electricity or gas)
	* test case
	* transmission
	
Return the capacity of each single transmission.
		
"""

def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	selectedScopes    = indexFilter.filterIndexList(0, getScopes())
	selectedEnergies  = indexFilter.filterIndexList(1, getEnergies(context, includedEnergies = {ELECTRICITY, GAS}))
	selectedTestCases = indexFilter.filterIndexList(2, context.getTestCases()) #This differs from for testCase in context.getResultsIndexSet() which requires to have a computed solution!
	selectedAssets    = indexFilter.filterIndexList(3, getAssets(context, includedTechnologies = TRANSMISSION_TYPES))
	
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includedAssetsName = selectedAssets)

	capacitiesDict = getTransmissionCapacity(context, selectedScopes, selectedTestCases, selectedEnergies, selectedAssetsByScope)
	
	for index in capacitiesDict:
		kpiDict[index] = capacitiesDict[index].getMeanValue() * MW_TO_W_CONVERSION
	
	return kpiDict

def get_indexing(context):
	baseIndexList = [getScopesIndexing(), getEnergiesIndexing(context, includedEnergies = {ELECTRICITY, GAS}), getTestCasesIndexing(context), getAssetsIndexing(context, includedTechnologies = TRANSMISSION_TYPES)]
	return baseIndexList

IndicatorLabel = "Transmission capacities"
IndicatorUnit = "W"
IndicatorDeltaUnit = "W"
IndicatorDescription = "Interconnection capacities"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Inputs>Transmission"
IndicatorTags = "Power System, Gas System, Power Markets"