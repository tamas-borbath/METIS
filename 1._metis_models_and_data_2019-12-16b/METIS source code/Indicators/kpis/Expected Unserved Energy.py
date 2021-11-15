########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Expected Unserved Energy (Wh)
-----------------------------

Indexed by
	* scope
	* delivery point
	* energy
	* test case
	
The Expected Unserved Energy is the annual volume of energy (including reserves) that is not served, i.e. the annual volume of a given energy that is needed but is not delivered due to a lack of generation.

"""

def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	timeStepDuration = getTimeStepDurationInHours(context)
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = indexFilter.filterIndexList(2, getEnergies(context, includedEnergies = PRODUCED_ENERGIES))
	selectedTestCases      = indexFilter.filterIndexList(3, context.getResultsIndexSet())
	
	selectedAssetsByScope  = getAssetsByScope(context, selectedScopes, includeFinancialAssets=True, includedTechnologies=LOSS_OF_ENERGY_TYPES)
	
	lossOfLoadDict         = getProductionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope)
	
	for index in lossOfLoadDict:
		kpiDict[index] = lossOfLoadDict[index].getSumValue() * timeStepDuration * MW_TO_W_CONVERSION

	return kpiDict

def get_indexing(context) :
	baseIndexList = [getScopesIndexing(), getDeliveryPointsIndexing(context), getEnergiesIndexing(context, includedEnergies = PRODUCED_ENERGIES), getTestCasesIndexing(context)]
	return baseIndexList

IndicatorLabel = "Expected Unserved Energy"
IndicatorUnit = "Wh"
IndicatorDeltaUnit = "Wh"
IndicatorDescription = "Expected unserved energy per delivery point, for all energies and reserves"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Results>Loss of load"
IndicatorTags = "Power System, Gas System, Power Markets"