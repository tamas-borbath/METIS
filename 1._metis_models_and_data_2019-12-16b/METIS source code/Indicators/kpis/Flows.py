########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Flow (Wh)
------------------

Indexed by
	* scope
	* energy (electricity or gas)
	* test case
	* transmission
	
Return the annual volumes flowing through a considered transmission line (monodirectionnal)
	

"""

def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	timeStepDuration = getTimeStepDurationInHours(context)
	
	selectedScopes        = indexFilter.filterIndexList(0, getScopes())
	selectedEnergies      = indexFilter.filterIndexList(1, getEnergies(context, includedEnergies = {ELECTRICITY, GAS}))
	selectedTestCases     = indexFilter.filterIndexList(2, context.getResultsIndexSet())
	selectedAssets        = indexFilter.filterIndexList(3, getAssets(context, includedTechnologies = TRANSMISSION_TYPES))

	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includedAssetsName = selectedAssets)

	transmissionDict = getTransmittedEnergy(context, selectedScopes, selectedTestCases, selectedEnergies, selectedAssetsByScope)

	for index in transmissionDict:
		kpiDict[index] = transmissionDict[index].getSumValue() * MW_TO_W_CONVERSION * timeStepDuration 

	return kpiDict

def get_indexing(context):
	baseIndexList = [getScopesIndexing(), getEnergiesIndexing(context, includedEnergies = {ELECTRICITY, GAS}), getTestCasesIndexing(context), getAssetsIndexing(context, includedTechnologies = TRANSMISSION_TYPES)]
	return baseIndexList

IndicatorLabel = "Flow"
IndicatorUnit = "Wh"
IndicatorDeltaUnit = "Wh"
IndicatorDescription = "Annual energy flow going through a transmissions line"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Results>Transmission"
IndicatorTags = "Power System, Gas System, Power Markets"