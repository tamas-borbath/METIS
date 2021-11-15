########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

"""

Indexed by
	* scope
	* test case
	* asset
	* data

This view shows a time series of the gas consumption of the asset

"""

from com.artelys.platform.config import Constantes
execfile(Constantes.REP_SCRIPTS+'/results/kpis/imports/BaseKPI.py')
from java.awt import Color

ViewLabel = "Consumption view (Gas) (W)"


##############################
# INDEX DEFINITION & RANKING
##############################
stackIndexesRanking = {GAS:1}

##############################
# JYTHON FUNCTIONS
##############################
def get_indexing(context):
	selectedData = [energy.getName() for energy in getEnergies(context, includedEnergies = [GAS])]
	return [
	getScopesIndexing(localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2),
	getTestCasesIndexing(context, localized=False, selectFirst=True, colorizeIndex=False, groupIndexAsGraphs=2),
	getAssetsIndexing(context, excludedTechnologies=TRANSMISSION_TYPES, consumedEnergies=[GAS], localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2, indexName="Physical Assets"),
	BaseIndexDefault("Data",selectedData, False, False, True, 0)
	]

def getData(view) :
	context = view.getContext()
	
	selectedScopes = getScopes()
	selectedEnergies = getEnergies(context, includedEnergies = [GAS])
	selectedTestCases = context.getTestCases()
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, excludedTechnologies=TRANSMISSION_TYPES)
	
	ret = []
	
	for scope in selectedScopes:
		for testCase in selectedTestCases:
			results = Crystal.getComputationResults(context, scope, testCase)
			if results == None or (not results.isComputed()):
				print '[SCRIPT INFO] No results for ' + scope + ' ' + str(testCase)
				continue
			
			for asset in selectedAssetsByScope[scope]:
				assetName = asset.getName()
				if not view.filter(scope, testCase, assetName):
					continue # Not selected
				for energy in getConsumedEnergies(context, asset):
					if energy in selectedEnergies:
						# Consumption
						consumptionTs = getConsumption(results, context, scope, asset, energy, testCase)
						ret += [[[scope, testCase, assetName, energy.getName()], consumptionTs * MW_TO_W_CONVERSION]]
	
	return ret

def getTimeContext(context) :
	timeContext = [context.getStartingDate(), context.getTimeStepDuration(), context.getTimeStepCount()]
	return timeContext

##############################
# OPTIONNAL FUNCTIONS
# Default versions of this functions will be used if necessary
##############################

def isLineStacked(index) :
	"""
	Returns true if the data identified by this (multi)index should be stacked when using the Graph option "Stacked chart" and "Line type:Script"
	"""
	return True

def indexCompare(numIndex,indexValue1,indexValue2):
	"""
	Comparator used to order indexes by comparing them two by two (when using the scripted order on this index type)
	numIndex is the index type ID (Scopes are 0, Test cases are 1,... eg)
	indexValue1 and indexValue2 are two index of the same type (two energies, or two technologies eg)
	"""
	if indexValue1 in stackIndexesRanking.keys() and indexValue2 in stackIndexesRanking.keys():
		return stackIndexesRanking[indexValue1] - stackIndexesRanking[indexValue2]
	else:
		return 0 # No order defined, all indexes are at the same level --> return 0

def colorizer(curve_label): 
	"""
	The function takes a label associated to a curve as an input and returns the color of the curve. 
	"""
	if ELECTRICITY.lower() == curve_label.lower() or GAS.lower() == curve_label.lower(): 
		return Color(191,79,57)
	return Color(0,0,0)