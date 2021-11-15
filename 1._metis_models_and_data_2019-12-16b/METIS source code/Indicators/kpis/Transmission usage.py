########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Transmission usage (%)
----------------------

Indexed by
	* scope
	* delivery point (dummy)
	* energy
	* test case
	* transmission 

The instant transmission usage of an interconnection is the ratio of electricity or gas flowing through the transmission over its capacity.
The KPI computes the yearly average value of instant transmission usage, for a given transmission:

.. math:: transmissionUsage_{transmission} = \\small \\frac{mean(instantTransmissionUsage^{transmission})}{installedCapacity^{transmission}} (\\%)

"""

def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	timeStepDuration = getTimeStepDurationInHours(context)
	
	selectedScopes        = indexFilter.filterIndexList(0, getScopes())
	selectedEnergies      = indexFilter.filterIndexList(1, getEnergies(context, includedEnergies = {ELECTRICITY, GAS}))
	selectedTestCases     = indexFilter.filterIndexList(2, context.getResultsIndexSet())
	selectedAssets        = indexFilter.filterIndexList(3, getAssets(context, includedTechnologies = TRANSMISSION_TYPES))

	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includedAssetsName = selectedAssets)
	
	capacitiesDict   = getTransmissionCapacity(context, selectedScopes, selectedTestCases, selectedEnergies, selectedAssetsByScope)
	transmissionDict = getTransmittedEnergy(context, selectedScopes, selectedTestCases, selectedEnergies, selectedAssetsByScope)

	for index in capacitiesDict:
		totalCapacity = capacitiesDict[index].getSumValue()
		if totalCapacity != 0:
			kpiDict[index] = 100 * transmissionDict[index].getSumValue() / totalCapacity

	return kpiDict

def get_indexing(context):
	baseIndexList = [getScopesIndexing(), getEnergiesIndexing(context, includedEnergies = {ELECTRICITY, GAS}), getTestCasesIndexing(context), getAssetsIndexing(context, includedTechnologies = TRANSMISSION_TYPES)]
	return baseIndexList

IndicatorLabel = "Transmission usage"
IndicatorUnit = "%"
IndicatorDeltaUnit = "%"
IndicatorDescription = "Usage of a transmission"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Results>Transmission"
IndicatorTags = "Power System, Gas System, Power Markets"