########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Import capacity (W)
-------------------

Indexed by
	* scope
	* delivery point
	* energy (electricity or gas)
	* test case

This KPI will return No data on power contexts and gas contexts without import or export contracts as it only applies to gas import and export contracts.

Return the import capacity of a given delivery point for a given energy and a given test case.

"""

def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = indexFilter.filterIndexList(2, getEnergies(context, includedEnergies = {ELECTRICITY, GAS}))
	selectedTestCases      = indexFilter.filterIndexList(3, context.getTestCases()) #This differs from for testCase in context.getResultsIndexSet() which requires to have a computed solution!
	
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includedTechnologies = IMPORT_TYPES)
	
	importCapacitiesDict = getInstalledCapacityDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope, aggregation = True)
	
	for index in importCapacitiesDict:
		kpiDict[index] = importCapacitiesDict[index].getMeanValue() * MW_TO_W_CONVERSION
	
	return kpiDict

def get_indexing(context):
	baseIndexList = [getScopesIndexing(), getDeliveryPointsIndexing(context), getEnergiesIndexing(context, includedEnergies = {ELECTRICITY, GAS}), getTestCasesIndexing(context)]
	return baseIndexList

IndicatorLabel = "Import capacity"
IndicatorUnit = "W"
IndicatorDeltaUnit = "W"
IndicatorDescription = "Import capacity per delivery point"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Inputs>Exchanges"
IndicatorTags = "Power System, Gas System, Power Markets"