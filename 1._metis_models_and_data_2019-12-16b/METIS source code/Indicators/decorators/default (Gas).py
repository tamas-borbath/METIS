########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

"""

This view shows all the assets of the context, physical and financial, related to the gas market.
It also shows an arrow that is showing the flow between the assets and the relavant delivery point(s)

"""

from com.artelys.platform.config import Constantes

# This decorator exactly reflect what is done in "default(Power).py", but with GAS instead of ELECTRICITY

execfile(Constantes.REP_SCRIPTS+'/decorators/default (Power).py') 

USED_ENERGY = GAS