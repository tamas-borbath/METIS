########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Average production at peak demand (Wh)
---------------------------------------

Indexed by
	* scope
	* delivery point
	* energy
	* test case
	* technology

Average peak Production per delivery point and technology for a given energy

.. math::

	\\small production_{dp, techno, energy} = \\sum_{t \\in peak period} production_{t, dp, techno, energy}

"""

import operator as op 

HOUR_NB_LIST = ['10','100','300', '800']

def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	timeStepDuration = getTimeStepDurationInHours(context)
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = indexFilter.filterIndexList(2, getEnergies(context, includedEnergies = PRODUCED_ENERGIES))
	selectedTestCases      = indexFilter.filterIndexList(3, context.getResultsIndexSet())
	selectedTechnologies   = indexFilter.filterIndexList(4, getTechnologies(context, includeFinancialAssetTypes = True))
	selectedHourNb         = indexFilter.filterIndexList(5, HOUR_NB_LIST)
	selectedAssetsByScope  = getAssetsByScope(context, selectedScopes, includedTechnologies = selectedTechnologies,includeFinancialAssets=True)
	
	productionAssetByScope  = getAssetsByScope(context, selectedScopes, includedTechnologies = PRODUCTION_TYPES, includeFinancialAssets=True)
	consumptionAssetByScope = getAssetsByScope(context, selectedScopes, includedTechnologies = DEMAND_TYPES,     includeFinancialAssets=True)
	ENRAssetByScope         = getAssetsByScope(context, selectedScopes, includedTechnologies = NON_FLEXIBLE_RES_TYPES)

	netDemand = {}
	indexHours = {}
	consumptionDict =  getDemandDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, consumptionAssetByScope, True)
	productionDict  =   getProductionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope)
	ENRProduction   =   getProductionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, ENRAssetByScope, True)

	# HOURS OF PEAK
	# They are computed on net production [from non-flexible RES technologies)
	for index in consumptionDict :
		netDemand[index] = (consumptionDict[index] - ENRProduction[index])
		currentDemand = netDemand[index].getValues()
		## Detect hours with maximum 
		for hourNb in selectedHourNb:
			indexHour = tuple(list(index) + [hourNb])
			indexHours[indexHour] = [x[0] for x in sorted(enumerate(currentDemand, 0), key = lambda x: x[1])[-int(hourNb):]]
	
	# PRODUCTION
	for index in productionDict:
		production  = productionDict[index].getValues()
		indexForHour = list(index)[:-1] # peaks hours does not take technology as index of course
		for hourNb in selectedHourNb:
			idx = tuple(indexForHour + [hourNb])
			if idx not in indexHours:
				continue
			peakProduction = [production[i] for i in indexHours[idx]]
			averagePeakProduction = sum(peakProduction)/len(peakProduction)
			
			kpiIdx = tuple(list(index) + [hourNb])
			kpiDict[kpiIdx] = averagePeakProduction * timeStepDuration * MW_TO_W_CONVERSION

	return kpiDict

def get_indexing(context):
	baseIndexList = [getScopesIndexing(), getDeliveryPointsIndexing(context), getEnergiesIndexing(context, includedEnergies = PRODUCED_ENERGIES), getTestCasesIndexing(context), 
							getTechnologiesIndexing(context, includedTechnologies= PRODUCTION_TYPES),
							BaseIndexDefault("Peak time step considered", HOUR_NB_LIST, False, False, True, 0)]
	return baseIndexList

IndicatorLabel = "Average production at peak demand"
IndicatorUnit = "Wh"
IndicatorDeltaUnit = "Wh"
IndicatorDescription = "Average production at peak demand per delivery point and technology"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Results>Production"
IndicatorTags = "Power System, Gas System, Power Markets"
