#/***************************************************************************
#                             fprg_concat.h
#                             -----------
#    begin                : sam nov 2 2002
#    copyright            : (C) 1992-2004 by Fabian Padilla
#    email                : fp@bridgethink.com
# ***************************************************************************/

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

""" doc """

__all__ = ["Fdoor_concat"]

from fevenprg import FevenPrg

from returncodes import RET_OK
from evenjastrings import ACT_END

class Fdoor_concat(FevenPrg):

	def __init__(self):
		FevenPrg.__init__(self)		# force construstor

	def __str__(self):
		return "\t"+FevenPrg.__str__(self)+\
				"Fdoor_concat - (null)\n"

	def receive_evenData(self,evenData):
		evenDataB = evenData.getEvenDataB()
		
		str = evenData.getData("TXT")
		str += evenDataB.getData("TXT")
		evenData.setData("TXT",str)
		evenData.resetDestination()
		evenData.addDestination("printf")
		self.sendEvenData(evenData)

		evenDataB.definePortAction(ACT_END)
		self.sendEvenData(evenDataB)
		
		return RET_OK
