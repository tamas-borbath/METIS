########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Storage capacity (Wh)
---------------------------------------

Indexed by
	* scope
	* delivery point
	* energy (electricity, gas and water)
	* test case
	* technology
	* asset name
	
Return the storage capacity per delivery point, per energy and technology (in Wh).

"""


def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = indexFilter.filterIndexList(2, getEnergies(context, includedEnergies = {ELECTRICITY, GAS}))
	selectedTestCases      = indexFilter.filterIndexList(3, context.getTestCases())
	selectedTechnologies   = indexFilter.filterIndexList(4, getTechnologies(context, includedTechnologies=STORAGE_TYPES))
	selectedAssets         = indexFilter.filterIndexList(5, getAssets(context, includedTechnologies=STORAGE_TYPES))
	
	selectedAssetsByScope   = getAssetsByScope(context, selectedScopes, includedAssetsName=selectedAssets, includedTechnologies = selectedTechnologies)
	
	storageCapacityDict     = getStorageCapacityDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope, indexByAsset=True)

	for index in storageCapacityDict:
		kpiDict[index] = storageCapacityDict[index].getMeanValue() * MW_TO_W_CONVERSION
	
	return kpiDict

def get_indexing(context) :
	baseIndexList = [getScopesIndexing(), getDeliveryPointsIndexing(context), getEnergiesIndexing(context, includedEnergies = {ELECTRICITY, GAS}), getTestCasesIndexing(context), 
							getTechnologiesIndexing(context, includedTechnologies=STORAGE_TYPES),
							getAssetsIndexing(context, includedTechnologies=STORAGE_TYPES)]
	return baseIndexList

IndicatorLabel = "Storage capacity"
IndicatorUnit = "Wh"
IndicatorDeltaUnit = "Wh"
IndicatorDescription = "Storage capacity per energy and per delivery point"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Inputs>Production"
IndicatorTags = "Power System, Gas System, Power Markets"
