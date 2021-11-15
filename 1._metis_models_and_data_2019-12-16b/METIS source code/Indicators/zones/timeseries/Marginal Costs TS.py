########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

"""

This view shows a time series, for each energy, of the marginal cost of generation of this energy at the selected zone.

"""

from com.artelys.platform.config import Constantes
execfile(Constantes.REP_SCRIPTS+'/results\kpis\imports\BaseKPI.py')

ViewLabel = u"Marginal costs TS (\u20ac/MWh)"

def get_indexing(context):
	return [
	getScopesIndexing(localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2),
	getZonesIndexing(context, localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2),
	getEnergiesIndexing(context, includedEnergies = PRODUCED_ENERGIES, localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2),
	getTestCasesIndexing(context, localized=False, selectFirst=True, colorizeIndex=True, groupIndexAsGraphs=0)
	]

def getData(view):

	context = view.getContext()
	timeStepDuration = getTimeStepDurationInHours(context)

	tempSelectedScopes       = getScopes()
	tempSelectedZones        = getZones(context)
	tempSelectedEnergies     = getEnergies(context, includedEnergies=PRODUCED_ENERGIES)
	tempSelectedTestCases    = context.getResultsIndexSet()

	includedScopes = set()
	includedZones = set()
	includedEnergies = set()
	includedTestCases = set()
	
	for scope in tempSelectedScopes:
		if view.filter(scope):
			for zone in tempSelectedZones:
				if view.filter(scope, zone):
					for energy in tempSelectedEnergies:
						if view.filter(scope, zone, energy.getName()):
							for testCase in tempSelectedTestCases:
								if view.filter(scope, zone, energy.getName(), testCase):
									includedScopes.add(scope)
									includedZones.add(zone)
									includedEnergies.add(energy.getName())
									includedTestCases.add(testCase)
	
	includedScopes = list(includedScopes)
	includedZones = list(includedZones)
	includedEnergies = list(includedEnergies)
	includedTestCases = list(includedTestCases)
	########################
	
	selectedScopes       		= getScopes(includedScopes=includedScopes)
	selectedZones      			= getZones(context, includedZones=includedZones)
	selectedEnergies     		= getEnergies(context, includedEnergies=includedEnergies)
	selectedTestCases    		= getTestCasesWithResults(context, includedTestCases=includedTestCases)

	selectedDeliveryPoints = getDpSetFromZoneList(context, selectedZones)

	marginalCostDict = getMarginalCostDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints)

	tempDict = getZoneDictFromDpDict(context, marginalCostDict, 1)

	ret = []
	for index in tempDict:
		ret += [[list(index), tempDict[index] / timeStepDuration]]

	return ret

def getTimeContext(context):
	timeContext = [context.getStartingDate(), context.getTimeStepDuration(), context.getTimeStepCount()]
	return timeContext 

