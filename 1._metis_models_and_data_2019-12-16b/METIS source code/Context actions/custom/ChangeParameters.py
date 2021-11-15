########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

"""
This action imports parameter values for a list of assets in the current context.
Parameters must be defined in the changeParameters.csv file in the client/Standard/data folder.

"""
from com.artelys.CrystalEditor.scripting import Crystal
from com.artelys.platform.gui.dialogs import CrystalOptionDialog
from com.artelys.platform.config import Constantes
import csv
import os
execfile(Constantes.REP_SCRIPTS+'/CommonUtils.py')

def onExecute(action, event):  
    changeParameters(action, event)

def changeParameters(action, event):
    # Context retrieval -------------------------------------
    sourceContext = action.getSourceContext()
    energy = Crystal.getEnergy("electricity")
    GWtoMW = 1000

    #open csvfile
    csvFileName = Constantes.REP_DATA + 'changeParameters.csv'
    CrystalOptionDialog.showConfirmDialog(None, "Changing parameters according to data from " + csvFileName +
        "\nPlease note that csv delimiter must be ';' and decimal mark must be ','" +
        "\nThe csv must start with a header line, and then each line should be as follows:" +
        "\n  zone | parameter1 | parameter2 | parameter3 | etc...", "", CrystalOptionDialog.CLOSED_OPTION)

    with open(csvFileName, 'rb') as csvfile:
        csvReader = csv.reader(csvfile,  delimiter=';')
        assetNameList = []
        paramIndex = {}
        parameterDict = {}

        firstLine = True
        for row in csvReader:
            if firstLine:
                for i in range(1,len(row)):
                    parameterDict[row[i]] = {}
                    paramIndex[i] = row[i]
                firstLine = False
                continue

            assetName = row[0]
            assetNameList.append(assetName)
            for i in range(1,len(row)):
                if row[i] == '':
                    continue
                else:
                    print row[i]
                    parameterDict[paramIndex[i]][assetName] = float(row[i].replace(',', '.'))

        countAsset = 0
        countParam = 0
        for assetName in assetNameList:
            asset = sourceContext.getPhysicalAsset(assetName)
            if asset != None:
                countAsset += 1
                for param in paramIndex.values():
                    if param in parameterDict:
                        countParam += 1
                        newParam = parameterDict[param][assetName] 
                        asset.setData(param, newParam)
                    # changedTransmissionsList.append(zoneIn + "->" + zoneOut + " : " + str(newPmax) + " MW")
            else:
                print "WARNING: the asset " + assetName + " has not been found in the context"

        CrystalOptionDialog.showConfirmDialog(None, str(countParam) + " parameter values have been changed for a total of " + str(countAsset) + " assets", "", CrystalOptionDialog.CLOSED_OPTION)

askOnResults = False
askOnParametersChange = False
askOnDelete = False
askOnStructureChange = False