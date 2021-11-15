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

This view shows a time series of the electricity production and consumption of the selected asset, as well as the running capacity.

"""

from com.artelys.platform.config import Constantes
execfile(Constantes.REP_SCRIPTS+'/results/kpis/imports/BaseKPI.py')
from java.awt import Color

ViewLabel = "Consumption vs production view (W)"


##############################
# INDEX DEFINITION & RANKING
##############################
electricityConsumptionIndex = 'Electricity consumption'
electricityGenerationIndex  = 'Electricity generation'
runningBoundIndex           = 'Running Bound'

stackIndexes    = [electricityConsumptionIndex, electricityGenerationIndex]
nonStackIndexes = [runningBoundIndex]

selectedData = stackIndexes + nonStackIndexes

##############################
# JYTHON FUNCTIONS
##############################
def get_indexing(context):
	return [
	getScopesIndexing(localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2),
	getTestCasesIndexing(context, localized=False, selectFirst=True, colorizeIndex=False, groupIndexAsGraphs=2),
	getAssetsIndexing(context, includedTechnologies=STORAGE_TYPES, localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2, indexName="Physical Assets"),
	BaseIndexDefault("Data",selectedData, False, False, True, 0)
	]

def getData(view):
	context = view.getContext()
	
	selectedScopes = getScopes()
	selectedTestCases = context.getTestCases()
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includedTechnologies=STORAGE_TYPES)
	
	electricity = Crystal.getEnergy(context, ELECTRICITY)
	
	ret = []
	for scope in selectedScopes:
		for testCase in selectedTestCases:
			results = Crystal.getComputationResults(context, scope, testCase)
			
			if results == None or (not results.isComputed()):
				print '[SCRIPT INFO] No results for ' + scope + ' ' + str(testCase)
				continue
			
			for asset in selectedAssetsByScope[scope]:
				assetName = asset.getName()
				if view.filter(scope, testCase, assetName):
					#Consumption
					if electricity in getConsumedEnergies(context, asset):
						electricityConsumption = results.getConsumption(asset, electricity)
						ret += [[[scope, testCase, assetName, electricityConsumptionIndex], electricityConsumption * MW_TO_W_CONVERSION]]
					#Production
					if electricity in getProducedEnergies(context, asset):
						electricityGeneration = results.getProduction(asset, electricity)
						ret += [[[scope, testCase, assetName, electricityGenerationIndex], electricityGeneration * MW_TO_W_CONVERSION]]
					#Cluster mode
					runningBound = getRunningBound(results, asset, electricity)
					if runningBound != None:
						#Running Bound
						ret += [[[scope, testCase, assetName, runningBoundIndex], runningBound * MW_TO_W_CONVERSION]]
	
	return ret

def getTimeContext(context):
	timeContext = [ context.getStartingDate() , context.getTimeStepDuration(), context.getTimeStepCount()]
	return timeContext 

##############################
# OPTIONNAL FUNCTIONS
# Default versions of this functions will be used if necessary
##############################
def isLineStacked(index):
	"""
	Returns true if the data identified by this (multi)index should be stacked when using the Graph option "Stacked chart" and "Line type:Script"
	"""
	return any(key in index for key in stackIndexes)

def colorizer(curve_label): 
	"""
	The function takes a label associated to a curve as an input and returns the color of the curve. 
	"""
	if electricityConsumptionIndex.lower() in curve_label.lower():
		return Color(38,196,236)
	elif electricityGenerationIndex.lower() in curve_label.lower():
		return Color(191,79,57)
	elif runningBoundIndex.lower() in curve_label.lower():
		return Color(128,0,0)
	return Color(0,0,0)




