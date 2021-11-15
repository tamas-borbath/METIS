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

This view shows the time series of the production cost of the selected asset, as a stacked chart that cumulates the following costs:
- CO2 emission cost
- Consumption cost
- Fuel consumption cost
- MFFR downward reserve cost
- MFFR up not running cost
- MFFR upward reserve cost
- Production cost
- Running cost
- Start up cost
- Storage cost 
- Synchronized downward reserve cost
- Synchronized upward reserve cost

"""

from com.artelys.platform.config import Constantes
execfile(Constantes.REP_SCRIPTS+'//results//kpis//imports//BaseKPI.py')

ViewLabel = u"Production cost view (\u20ac)"

#Stacks
# NB : THIS LABELS ARE GLOBAL CONSTANTS (imported from CommonFilters)
stackIndexesRanking = {LABEL_PROD_COST:2, LABEL_CONSUMPTION_COST:3, LABEL_STORAGE_COST:100, LABEL_RUNNING_BOUND_COST: 1, LABEL_STARTUP_COST:9, LABEL_SYNC_RESERVE_UP_COST:8, LABEL_SYNC_RESERVE_DOWN_COST:8,\
LABEL_MFRR_UP_COST:8, LABEL_MFRR_DOWN_COST: 8, LABEL_MFRR_UP_NOT_RUNNING_COST:8, LABEL_FUEL_COST:5, LABEL_CO2_COST:6}

#Lines
totalCostIndex = "Total cost"
nonStackIndexesRanking = {totalCostIndex:10}

#All
selectedData = stackIndexesRanking.keys()
selectedData.extend(nonStackIndexesRanking.keys())

indexesRanking = stackIndexesRanking.copy()
indexesRanking.update(nonStackIndexesRanking)


def get_indexing(context) :
	return [
	getScopesIndexing(localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2),
	getTestCasesIndexing(context, localized=False, selectFirst=True, colorizeIndex=False, groupIndexAsGraphs=2),
	getAssetsIndexing(context, includedTechnologies=PRODUCTION_TYPES, localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2, indexName="Physical Assets"),
	BaseIndexDefault("Data",selectedData, False, False, True, 0)
	]

def getData(view) :
	context = view.getContext()
	portfolioInterface = context.getPortfolioInterface()
	timeStepDurationInHours = context.getTimeStepDuration()/60 # in hours
	
	selectedScopes = getScopes()
	selectedTestCases = context.getResultsIndexSet()
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includedTechnologies=PRODUCTION_TYPES)
	
	ret = []
	for scope in selectedScopes:
		for testCase in selectedTestCases:
			results = Crystal.getComputationResults(context, scope, testCase)
			
			if results == None:
				print '[SCRIPT INFO] No results for ' + scope + ' ' + str(testCase)
				continue
			
			for asset in selectedAssetsByScope[scope]:
				assetName = asset.getName()
				if view.filter(scope, testCase, assetName):
					totalCost = getZeroTs(context)
					
					# Asset costs
					# This function returns directly a dict by type of cost
					assetCostDict = getAssetCostByType(results, context, scope, asset, testCase)
					for index in assetCostDict:
						totalCost = totalCost + (assetCostDict[index])
						ret += [[[scope, testCase, assetName, index], assetCostDict[index]]]
					
					# Total cost
					ret += [[[scope, testCase, assetName, totalCostIndex], totalCost]]
	
	return ret

def getTimeContext(context) :
	timeContext = [ context.getStartingDate() , context.getTimeStepDuration() , context.getTimeStepCount() ]
	return timeContext 

def isLineStacked(index) :
	# index may contains several keys
	# data type is only one key among several (scope, testCase, assetName, ...)
	return any(key in index for key in stackIndexesRanking)

def indexCompare(numIndex,indexValue1,indexValue2):
	if indexValue1 in indexesRanking and indexValue2 in indexesRanking:
		return indexesRanking[indexValue1] - indexesRanking[indexValue2]
	else:
		return 0


def colorizer(curve_label): 
	"""
	The function takes a label associated to a curve as an input and returns the color of the curve. 
	"""
	if LABEL_PROD_COST.lower() == curve_label.lower():
		return Color(255,153,153)
	elif LABEL_RUNNING_BOUND_COST.lower() == curve_label.lower():
		return Color(102,178,255)
	elif LABEL_STARTUP_COST.lower() == curve_label.lower():
		return Color(102,204,0)
	elif LABEL_MFRR_UP_NOT_RUNNING_COST.lower() == curve_label.lower():
		return Color(0,0,0)
	elif LABEL_FUEL_COST.lower() == curve_label.lower():
		return Color(255,178,102)
	elif LABEL_CO2_COST.lower() == curve_label.lower():
		return Color(192,192,192)
	elif totalCostIndex.lower() == curve_label.lower():
		return Color(255,51,51)
	elif LABEL_CONSUMPTION_COST.lower() == curve_label.lower():
		return Color(228, 191, 252)
	elif LABEL_STORAGE_COST.lower() == curve_label.lower():
		return Color(193, 255, 255)
	elif LABEL_MFRR_UP_NOT_RUNNING_COST.lower() in curve_label.lower(): 
		return Color(191,79,57)
	elif LABEL_MFRR_DOWN_COST.lower() in curve_label.lower():
		return Color(133,182,134)
	elif LABEL_SYNC_RESERVE_DOWN_COST.lower() in curve_label.lower():
		return Color(72,120,73)
	elif LABEL_SYNC_RESERVE_UP_COST.lower() in curve_label.lower():
		return Color(0,128,192)
	elif LABEL_MFRR_UP_COST.lower() in curve_label.lower():
		return Color(85,200,255)
	
	return Color(0,0,0)




