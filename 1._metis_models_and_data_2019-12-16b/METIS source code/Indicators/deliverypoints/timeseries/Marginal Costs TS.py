########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

"""

This view shows a time series, for each energy, of the marginal cost of generation of this energy at the selected delivery point.

"""

from com.artelys.platform.config import Constantes
execfile(Constantes.REP_SCRIPTS+'/results\kpis\imports\BaseKPI.py')

ViewLabel = u"Marginal costs TS (\u20ac/MWh)"


def get_indexing(context):
	return [
	getScopesIndexing(localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2),
	getDeliveryPointsIndexing(context, localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2),
	getEnergiesIndexing(context, includedEnergies = PRODUCED_ENERGIES, localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2),
	getTestCasesIndexing(context, localized=False, selectFirst=True, colorizeIndex=True, groupIndexAsGraphs=0)
	]

def getData(view):
	context = view.getContext()
	timeStepDuration = getTimeStepDurationInHours(context)
	
	###### Filter Index ######
	tempSelectedScopes       		= getScopes()
	tempSelectedDeliveryPoints      = getDeliveryPoints(context)
	tempSelectedEnergies     		= getEnergies(context, includedEnergies=PRODUCED_ENERGIES)
	tempSelectedTestCases			= getTestCasesWithResults(context)
	
	includedScopes = set()
	includedDeliveryPoints = set()
	includedEnergies = set()
	includedTestCases = set()
	
	for scope in tempSelectedScopes:
		if view.filter(scope):
			for deliveryPoint in tempSelectedDeliveryPoints:
				if view.filter(scope, deliveryPoint):
					for energy in tempSelectedEnergies:
						if view.filter(scope, deliveryPoint, energy.getName()):
							for testCase in tempSelectedTestCases:
								if view.filter(scope, deliveryPoint, energy.getName(), testCase):
									includedScopes.add(scope)
									includedDeliveryPoints.add(deliveryPoint)
									includedEnergies.add(energy.getName())
									includedTestCases.add(testCase)
	
	includedScopes = list(includedScopes)
	includedDeliveryPoints = list(includedDeliveryPoints)
	includedEnergies = list(includedEnergies)
	includedTestCases = list(includedTestCases)
	########################
	
	selectedScopes       		= getScopes(includedScopes=includedScopes)
	selectedDeliveryPoints      = getDeliveryPoints(context, includedDeliveryPoints=includedDeliveryPoints)
	selectedEnergies     		= getEnergies(context, includedEnergies=includedEnergies)
	selectedTestCases    		= getTestCasesWithResults(context, includedTestCases=includedTestCases)
	
	marginalCostDict = getMarginalCostDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints)
	
	ret = []
	for index in marginalCostDict:
		ret += [[list(index), marginalCostDict[index] / timeStepDuration]]
	
	return ret

def getTimeContext(context):
	timeContext = [context.getStartingDate(), context.getTimeStepDuration(), context.getTimeStepCount()]
	return timeContext 

