########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

"""
This script is useful after computing optimal capacities with the capacity optimisation scope.
It will update the parameters 'Pmax' and 'Storage capacity' with optimization results.
The user can launch the simulation scope with the updated capacities afterwards.

"""

from com.artelys.CrystalEditor.scripting import Crystal
from com.artelys.platform.gui.dialogs import CrystalOptionDialog
from com.artelys.platform.config import Constantes
execfile(Constantes.getLibraryMappings("DefaultVar"))

def onExecute(action, event):
    ret = CrystalOptionDialog.showConfirmDialog(None, 
        "Are you sure you want to replace the parameters 'Pmax' and 'Storage capacity' with optimisation results? \nOld values will be lost.",
        "Replace parameters?", CrystalOptionDialog.YES_NO_OPTION)
    if ret != 0: return
    
    propagateCapacities(action, event)
    
def propagateCapacities(action, event):
    # Context retrieval -------------------------------------
    sourceContext = action.getSourceContext()
    destinationContext = action.getDestinationContext()
    if sourceContext == None:
        Crystal.showErrorDialog("Cannot execute script: source context cannot be None!")
        return
    if destinationContext == None:
        Crystal.showErrorDialog("Cannot execute script: destination context cannot be None!")
        return

    # Results retrieval -------------------------------------------
    results = None
    for testCase in sourceContext.getTestCases():
        results = Crystal.getComputationResults(sourceContext, testCase)
        if results != None:
            break
    if results == None or (not results.isComputed()):
        Crystal.showErrorDialog("Cannot execute script: there are no results to propagate !")
        return
    
    # Optimized parameters replacement --------------------------------
    CHANGE_PMAX_MESSAGE = "Change PMAX of asset: "
    CHANGE_STORAGE_CAPACITY_MESSAGE = "Change STORAGE CAPACITY of asset: "
    COST_KEY = "cost"
    
    if destinationContext == sourceContext:
        for physicalAsset in Crystal.listPhysicalAssets(sourceContext):
            physicalAssetName = physicalAsset.getName()
            for my_key in results.getAssetIndexedValuesIndexes(physicalAsset):
                foundPmaxKey = False
                foundStorageCapacityKey = False
                # Replacing the optimized Pmax, if there is one
                if OPTIMIZED_PMAX_VAR in my_key.toString().lower()  and not COST_KEY in my_key.toString().lower():
                    print CHANGE_PMAX_MESSAGE ,physicalAssetName
                    newPmax = results.getResult(my_key).getMeanValue()
                    physicalAsset.setData(PMAX, newPmax)
                # Replacing the optimized storage capacity, if there is one
                if OPTIMIZED_STORAGE_VAR in my_key.toString().lower() and not COST_KEY in my_key.toString().lower():
                    print CHANGE_STORAGE_CAPACITY_MESSAGE ,physicalAssetName
                    newStorageCapacity = results.getResult(my_key).getMeanValue()
                    physicalAsset.setData(STORAGE_CAPACITY, newStorageCapacity)
                # If all the parameters have been found
                if foundPmaxKey and foundStorageCapacityKey:
                    break #for my_key
    else:
        listAssetNotFound = []
        for sourcePhysicalAsset in Crystal.listPhysicalAssets(sourceContext):
            sourcePhysicalAssetName = sourcePhysicalAsset.getName()
            foundPmaxKey = False
            foundStorageCapacityKey = False
            for my_key in results.getAssetIndexedValuesIndexes(sourcePhysicalAsset):
                # Replacing the optimized Pmax, if there is one
                if OPTIMIZED_PMAX_VAR in my_key.toString().lower() and not COST_KEY in my_key.toString().lower():
                    foundPmaxKey = True
                    foundDestinationAsset = False
                    for destinationPhysicalAsset in Crystal.listPhysicalAssets(destinationContext):
                        if destinationPhysicalAsset.getName()== sourcePhysicalAssetName :
                            if sourcePhysicalAsset.getType() == destinationPhysicalAsset.getType() :
                                # Assets are considered identical
                                foundDestinationAsset = True
                                print CHANGE_PMAX_MESSAGE , destinationPhysicalAsset.getName()
                                newPmax = results.getResult(my_key).getMeanValue()
                                destinationPhysicalAsset.setData(PMAX, newPmax)
                                break #for destinationPhysicalAsset
                    if not foundDestinationAsset and not sourcePhysicalAssetName in listAssetNotFound:
                        listAssetNotFound.append(sourcePhysicalAssetName)
                # Replacing the optimized storage capacity, if there is one
                if OPTIMIZED_STORAGE_VAR in my_key.toString().lower() and not COST_KEY in my_key.toString().lower():
                    foundStorageCapacityKey = True
                    foundDestinationAsset = False
                    for destinationPhysicalAsset in Crystal.listPhysicalAssets(destinationContext):
                        if destinationPhysicalAsset.getName()== sourcePhysicalAssetName :
                            if sourcePhysicalAsset.getType() == destinationPhysicalAsset.getType() :
                                # Assets are considered identical
                                foundDestinationAsset = True
                                print CHANGE_STORAGE_CAPACITY_MESSAGE ,destinationPhysicalAsset.getName()
                                newStorageCapacity = results.getResult(my_key).getMeanValue()
                                destinationPhysicalAsset.setData(STORAGE_CAPACITY, newStorageCapacity)
                                break #for destinationPhysicalAsset
                    if not foundDestinationAsset and not sourcePhysicalAssetName in listAssetNotFound:
                        listAssetNotFound.append(sourcePhysicalAssetName)
                # If all the parameters have been found
                if foundPmaxKey and foundStorageCapacityKey:
                    break #for my_key
        
        if len(listAssetNotFound)>0:
            print "WARNING : Could not find the following assets in the destination context"
            print listAssetNotFound
	
askOnResults = False
askOnParametersChange = False
askOnDelete = False
askOnStructureChange = False