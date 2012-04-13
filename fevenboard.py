#/***************************************************************************
#                             fevenboard.h
#                             -----------
#    begin                : sam nov 2 2002
#    copyright            : (C) 1992-2004 by Fabian Padilla
#    email                : fp@bridgethink.com
# ***************************************************************************/
# /***************************************************************************
#
#                              fevenboard.py
#                              -------------------
#     begin                : wed mar 10 2004
#     copyright            : (C) 2004 by Jeremy Zurcher
#     email                : tzurtch@bluemail.ch
#
#  ***************************************************************************/

# /***************************************************************************
#  *                                                                         *
#  *   This program is free software; you can redistribute it and/or modify  *
#  *   it under the terms of the Foundation Public License as published by   *
#  *   bridgethink sarl; either version 2 of the License, or                 *
#  *   (at your option) any later version.                                   *
#  *                                                                         *
#  ***************************************************************************/

#
#  from C++ to python by Jeremy Zurcher <jeremy@asynk.ch>
#

"""/** evenData will wait for another evenData in this evenBoard.

  function : merge informations having the same linkValue.

  description : receive an evenData and check if another evenData with the same linkValue
                is already in the list. Then Apply the ACTION to marge them together
                and send to somewhere.

  *@author Fabian Padilla
  */"""

__all__ = ["FevenBoard"]

from fportlisthash import FportListHash

from returncodes import RET_OK
from evenjastrings import ACT_ERROR

from globalvars import gvActionWait
from globalvars import gvActionDestination1Data
from globalvars import gvActionFollowDestination

class FevenBoard(FportListHash):

	def __init__(self):
		FportListHash.__init__(self)	# force contrustor

	def __str__(self):
		return "\t"+FportListHash.__str__(self)+\
				"FevenBoard - (null)\n"
	
	def receive_evenData(self,evenData):
		"""/** Receive the evenData and apply the action to know what to do with */"""
		action = evenData.getCurrentDestination().getAction()

		if action.equals(gvActionDestination1Data):
			if evenData.selectNextDestination() != RET_OK:
				evenData.definePortAction(ACT_ERROR)
		else:
			dataPresent = self.listHash.addOrRemove(evenData)
			if dataPresent <> None:
				if action.equals(gvActionFollowDestination):
					provData = dataPresent
					dataPresent = evenData
					evenData = provData
				evenData.setEvenDataB(dataPresent)
				if evenData.selectNextDestination() != RET_OK:
					evenData.definePortAction(ACT_ERROR)
				self.sendEvenData(evenData)
			else:
				if action.equals(gvActionWait):
					print "NOT IMPLEMENTED YET"
		return RET_OK
						
