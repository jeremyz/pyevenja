#/***************************************************************************
#                             fevenprg.h
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

"""/** evenPrg do the modification on the evenData or many evenDatas.

  function : Interface for all evenPrg.

  description : Must contain only the behavior to modify datas and "if" concerning the
                modification of datas. Do not implement in a evenPrg "if" about end user
                functionnalities. See the withepaper.pdf at www.evenja.org.
  
  *@author Fabian Padilla
  */"""


__all__ = ["FevenPrg"]


from fportbkpevendata import FportBkpEvenData
from evenjastrings import ACT_ERROR

class FevenPrg(FportBkpEvenData):
	""" This class is the interface for all evenPrg"""

	def __init__(self):
		FportBkpEvenData.__init__(self)	# force constructor
		self.evenDataB = None		#/** Backup of the evenDatas that need to be sends by sendEvenData */
	
	def __str__(self):
		return "\t"+FportBkpEvenData.__str__(self)+\
				"FevenPrg - evenDataB : "+str(self.evenDataB)+"\n"
	
	def justDoIt(self,evenData):
		"""/** Methods called by Fstarter */"""
		self.evenDataB = evenData.getEvenDataB()
		if self.evenDataB <> None:
			evenData.setEvenDataB(self.evenDataB)
		ret = FportBkpEvenData.justDoIt(self,evenData)
		if self.evenDataB <> None:
			self.evenDataB.definePortAction(ACT_ERROR)
			self.sendEvenData(self.evenDataB)
		return ret
	
	def sendEvenData(self,evenData):
		"""/** Methods to enable all ports to sends evenDatas to a port */"""
		if self.evenDataB == evenData:
			self.evenDataB = None
		FportBkpEvenData.sendEvenData(self,evenData)
	
	def sendEvenDataSys(self,evenData):
		"""/** Methods to enable all ports to sends evenDatas to a port */"""
		if self.evenDataB == evenData:
			self.evenDataB = None
		FportBkpEvenData.sendEvenDataSys(self,evenData)
	
