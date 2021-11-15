########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

"""

This view shows the zones of the context, without showing the different assets

"""

from com.artelys.platform.config import Constantes
execfile(Constantes.REP_SCRIPTS+'/decoratorUtils.py')

def configureZoneRenderable(renderable,zone):
	# Shows the zone shapes 
	# Without a label because its becomes inaesthetic when several decorators are supperposed
	# (+ it's useless : the map already provides country names)
	setZoneShape(renderable,zone)
	renderable.setDisplayAnnotation(zone.getName())

def getDisplayPriority():
	# Should be lower than any other decorator
	return 1
