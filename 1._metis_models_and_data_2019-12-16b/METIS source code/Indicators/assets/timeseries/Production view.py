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

This view shows a combination of time series as stacks and lines

Stacks:
 - Non reserved generation
 - Downward MFRR
 - Downward Synchronized Reserve
 - Upward Synchronized Reserve
 - Upward MFRR

Lines:
 - Generation capacity
 - Available capacity
 - Running Bound
 - Generation level
 - Minimal Generation level

"""

from com.artelys.platform.config import Constantes

execfile(Constantes.REP_SCRIPTS+'/results/kpis/imports/BaseKPI.py')
from java.awt import Color

ViewLabel = "Production view (W)"


##############################
# INDEX DEFINITION & RANKING
##############################
#Stacks
nonReservedGenerationIndex = 'Non reserved generation'
mfrrResDownGenerationIndex = 'Downward MFRR'
syncResDownGenerationIndex = 'Downward Synchronized Reserve'
syncResUpGenerationIndex   = 'Upward Synchronized Reserve'
mfrrResUpGenerationIndex   = 'Upward MFRR'
stackIndexesRanking = {nonReservedGenerationIndex:1, mfrrResDownGenerationIndex:2, syncResDownGenerationIndex:3, syncResUpGenerationIndex:4, mfrrResUpGenerationIndex:5}

#Lines
pmaxIndex = 'Pmax'
availableCapacityIndex = 'Available Capacity'
runningBoundIndex      = 'Running Bound'
mainGenerationIndex    = 'Generation'
minimalGenerationIndex = 'Minimal Generation'
nonStackIndexesRanking = {pmaxIndex:11, availableCapacityIndex:12, runningBoundIndex:13, mainGenerationIndex:14, minimalGenerationIndex:15}

#All
selectedData = stackIndexesRanking.keys()
selectedData.extend(nonStackIndexesRanking.keys())

indexesRanking = stackIndexesRanking.copy()
indexesRanking.update(nonStackIndexesRanking)

##############################
# JYTHON FUNCTIONS
##############################

def get_indexing(context):
	return [
	getScopesIndexing(localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2),
	getTestCasesIndexing(context, localized=False, selectFirst=True, colorizeIndex=False, groupIndexAsGraphs=2),
	getAssetsIndexing(context, includedTechnologies=PRODUCTION_TYPES, localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2, indexName="Physical Assets"),
	BaseIndexDefault("Data",selectedData, False, False, True, 0)
	]

def getData(view) :
	context = view.getContext()
	zeroTs = getZeroTs(context)
	
	selectedScopes = getScopes()
	selectedTestCases = context.getTestCases()
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includedTechnologies=PRODUCTION_TYPES)
	
	mfrrResDown = Crystal.getEnergy(context, MFRR_DOWN)
	syncResDown = Crystal.getEnergy(context, SYNC_RESERVE_DOWN)
	syncResUp   = Crystal.getEnergy(context, SYNC_RESERVE_UP)
	mfrrResUp   = Crystal.getEnergy(context, MFRR_UP)
	
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
					continue # Indexes not selected
				
				#Getting the real energy produced by this asset
				mainProducedEnergy = asset.getEnergyForParameter(ENERGY_DELIVERY, context)
				
				#Production
				mainGeneration = results.getProduction(asset, mainProducedEnergy)
				mfrrResDownGeneration = results.getProduction(asset, mfrrResDown)
				syncResDownGeneration = results.getProduction(asset, syncResDown)
				syncResUpGeneration   = results.getProduction(asset, syncResUp)
				mfrrResUpGeneration   = results.getProduction(asset, mfrrResUp)
				if mainGeneration != None:
					#Electricity Generation
					ret += [[[scope, testCase,assetName,mainGenerationIndex], mainGeneration * MW_TO_W_CONVERSION]]
					#Non Reserved Generation
					nonReservableGeneration = mainGeneration
					if syncResDownGeneration != None:
						nonReservableGeneration = nonReservableGeneration - syncResDownGeneration
					if mfrrResDownGeneration != None:
						nonReservableGeneration = nonReservableGeneration - mfrrResDownGeneration
					ret += [[[scope, testCase,assetName,nonReservedGenerationIndex], nonReservableGeneration * MW_TO_W_CONVERSION]]
				if mfrrResDownGeneration != None:
					#MFRR RES DOWN
					ret += [[[scope, testCase,assetName,mfrrResDownGenerationIndex], mfrrResDownGeneration * MW_TO_W_CONVERSION]]
				if syncResDownGeneration != None:
					#SYNC RES DOWN
					ret += [[[scope, testCase,assetName,syncResDownGenerationIndex], syncResDownGeneration * MW_TO_W_CONVERSION]]
				if syncResUpGeneration != None:
					#SYNC RES UP
					ret += [[[scope, testCase,assetName,syncResUpGenerationIndex], syncResUpGeneration * MW_TO_W_CONVERSION]]
				if mfrrResUpGeneration != None:
					#MFRR UP
					ret += [[[scope, testCase,assetName,mfrrResUpGenerationIndex], mfrrResUpGeneration * MW_TO_W_CONVERSION]]
				#Data Value
				#Pmax
				pmax = getInstalledCapacity(context, scope, asset, testCase, results)
				if pmax != None:
					ret += [[[scope, testCase,assetName,pmaxIndex], pmax * MW_TO_W_CONVERSION + zeroTs]]
				
				#Available Capacity
				availableCapacity = getAvailableCapacity(context, scope, asset, testCase, results)
				if availableCapacity != None:
					ret += [[[scope, testCase,assetName,availableCapacityIndex], availableCapacity * MW_TO_W_CONVERSION + zeroTs]]
				
				#Cluster mode
				if asset.isActiveBehavior(BH_CLUSTER, scope):
					#Running Bound
					runningBound = getRunningBound(results, asset, mainProducedEnergy)
					if runningBound != None:
						ret += [[[scope, testCase,assetName,runningBoundIndex], runningBound * MW_TO_W_CONVERSION]]
					
					#Minimal generation
					minimalGeneration = getRunningMinLoadBound(context, scope, asset, testCase, results)
					if minimalGeneration != None:
						ret += [[[scope, testCase,assetName,minimalGenerationIndex], minimalGeneration * MW_TO_W_CONVERSION + zeroTs]]
				#Fleet mode
				else:
					#Minimal generation
					minimalGeneration = getMinLoadBound(context, scope, asset, testCase, results)
					if minimalGeneration != None:
						ret += [[[scope, testCase,assetName,minimalGenerationIndex], minimalGeneration * MW_TO_W_CONVERSION + zeroTs]]

	return ret

def getTimeContext(context) :
	timeContext = [ context.getStartingDate() , context.getTimeStepDuration() , context.getTimeStepCount()]
	return timeContext 


##############################
# OPTIONNAL FUNCTIONS
# Default versions of this functions will be used if necessary
##############################

def isLineStacked(index) :
	"""
	Returns true if the data identified by this (multi)index should be stacked when using the Graph option "Stacked chart" and "Line type:Script"
	"""
	return any(key in index for key in stackIndexesRanking)

def indexCompare(numIndex,indexValue1,indexValue2):
	"""
	Comparator used to order indexes by comparing them two by two (when using the scripted order on this index type)
	numIndex is the index type ID (Scopes are 0, Test cases are 1,... eg)
	indexValue1 and indexValue2 are two index of the same type (two energies, or two technologies eg)
	"""
	if indexValue1 in indexesRanking and indexValue2 in indexesRanking:
		# Using the indexesRanking dict to order data types
		return indexesRanking[indexValue1] - indexesRanking[indexValue2]
	else:
		return 0 # No order defined, all indexes are at the same level --> return 0

def colorizer(curve_label): 
	"""
	The function takes a label associated to a curve as an input and returns the color of the curve. 
	"""
	if nonReservedGenerationIndex.lower() in curve_label.lower(): 
		return Color(191,119,57)
	elif mfrrResDownGenerationIndex.lower() in curve_label.lower():
		return Color(133,182,134)
	elif syncResDownGenerationIndex.lower() in curve_label.lower():
		return Color(72,120,73)
	elif syncResUpGenerationIndex.lower() in curve_label.lower():
		return Color(0,128,192)
	elif mfrrResUpGenerationIndex.lower() in curve_label.lower():
		return Color(85,200,255)
	elif pmaxIndex.lower() in curve_label.lower():
		return Color(0,0,0)
	elif availableCapacityIndex.lower() in curve_label.lower():
		return Color(98,0,196)
	elif runningBoundIndex.lower() in curve_label.lower():
		return Color(128,0,0)
	elif minimalGenerationIndex.lower() in curve_label.lower():
		return Color(239,239,239)
	elif mainGenerationIndex.lower() in curve_label.lower():
		return Color(191,79,57)
	return Color(0,0,0)
