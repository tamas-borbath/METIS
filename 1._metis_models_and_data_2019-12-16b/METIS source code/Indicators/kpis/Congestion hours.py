########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Congestion hours (h)
---------------------

Indexed by
	* scope
	* energy (electricity or gas)
	* test case
	* transmission

The number of congestion hours corresponds to the number of hours over the year during which an interconnection is saturated with respect to its available capacity.
An interconnection is considered saturated when it reaches 99.99% of its available capacity.

"""

def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	timeStepDuration = getTimeStepDurationInHours(context)
	
	selectedScopes    = indexFilter.filterIndexList(0, getScopes())
	selectedEnergies  = indexFilter.filterIndexList(1, getEnergies(context, includedEnergies = {ELECTRICITY, GAS}))
	selectedTestCases = indexFilter.filterIndexList(2, context.getResultsIndexSet())
	selectedAssets    = indexFilter.filterIndexList(3, getAssets(context, includedTechnologies = TRANSMISSION_TYPES))
	
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includedAssetsName = selectedAssets)

	capacitiesDict     = getTransmissionCapacity(context, selectedScopes, selectedTestCases, selectedEnergies, selectedAssetsByScope)
	availabilitiesDict = getTransmissionAvailability(context, selectedScopes, selectedTestCases, selectedEnergies, selectedAssetsByScope)
	transmissionDict   = getTransmittedEnergy(context, selectedScopes, selectedTestCases, selectedEnergies, selectedAssetsByScope)

	for index in capacitiesDict:
		if (capacitiesDict[index]*availabilitiesDict[index]).getSumValue() > 0:
			kpiDict[index] = ((capacitiesDict[index] * availabilitiesDict[index]) - transmissionDict[index]).getValue().countBelow(0.0001)*timeStepDuration
	
	return kpiDict

def get_indexing(context) :
	baseIndexList = [getScopesIndexing(), getEnergiesIndexing(context, includedEnergies = {ELECTRICITY, GAS}), getTestCasesIndexing(context), getAssetsIndexing(context, includedTechnologies = TRANSMISSION_TYPES)]
	return baseIndexList

IndicatorLabel = "Congestion hours"
IndicatorUnit = "h"
IndicatorDeltaUnit = "h"
IndicatorDescription = "Hours during which the flow is close to the maximal capacity"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Results>Transmission"
IndicatorTags = " Power System, Gas System, Power Markets "
