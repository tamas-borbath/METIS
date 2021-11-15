########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Investment costs (euro)
---------------------------------------

Indexed by
	* scope
	* delivery point
	* energy (electricity or gas)
	* test case
	* technology
	* asset name

Return the investment costs per technology, i.e. the cost associated to building a given technology. It is equal to the technology installed capacity times the sum of the CAPEX and Fixed Operating Cost (FOC):

.. math:: \\small investmentCosts_{technology, energy} = installedCapacity^{technology, energy}*(CAPEX^{technology, energy} + FOC^{technology, energy})
	
"""

def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):

	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = indexFilter.filterIndexList(2, getEnergies(context, includedEnergies={ELECTRICITY, GAS}))
	selectedTestCases      = indexFilter.filterIndexList(3, context.getTestCases()) #This differs from for testCase in context.getResultsIndexSet() which requires to have a computed solution!
	selectedTechnologies   = indexFilter.filterIndexList(4, getTechnologies(context, includedTechnologies = PRODUCTION_TYPES))
	selectedAssets         = indexFilter.filterIndexList(5, getAssets(context, includedTechnologies = PRODUCTION_TYPES))
	
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includedAssetsName=selectedAssets, includedTechnologies=selectedTechnologies)

	capexDict = getCapexDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope, aggregation = False, indexByAsset=True)
	focDict   = getFocDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope, aggregation = False, indexByAsset=True)

	for index in capexDict:
		kpiDict[index] = (capexDict[index] + focDict[index]).getMeanValue()
	return kpiDict

def get_indexing(context) :
	baseIndexList = [getScopesIndexing(), context.getDeliveryPointsIndexing(), getEnergiesIndexing(context, includedEnergies={ELECTRICITY, GAS}), getTestCasesIndexing(context), 
							getTechnologiesIndexing(context, includedTechnologies = PRODUCTION_TYPES),
							getAssetsIndexing(context, includedTechnologies = PRODUCTION_TYPES)]
	return baseIndexList

IndicatorLabel = "Investment costs"
IndicatorUnit = u"\u20ac"
IndicatorDeltaUnit = u"\u20ac"
IndicatorDescription = "Investment costs per technology per delivery point"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Inputs"
IndicatorTags = "Power System, Gas System, Power Markets"