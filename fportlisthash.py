#/***************************************************************************
#                             fevendata.h
#                             -----------
#    begin                : sam nov 2 2002
#    copyright            : (C) 1992-2004 by Fabian Padilla
#    email                : fp@bridgethink.com
# ***************************************************************************/
# /***************************************************************************
#
#                              fportlisthash.py
#                              -------------------
#     begin                : tue mar 09 2004
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

"""/** Inherited from Fport to add a listHash.

  function : maintain a list of single evenDatas ( single by the linkValue) in
             FevenBoard : to merge and or maintain a list of evenDatas
             Frouter : to send the evenDatas to the right destinations

  description : work as Fport.

  *@author Fabian Padilla
  */"""

__all__ = ["FportListHash"]
  
from fport import Fport
from flisthash import FlistHash


class FportListHash(Fport):
	""" This is a Fport with Flist attribute"""

	def __init__(self):
		Fport.__init__(self)		# force constructor
		self.listHash = FlistHash()	#/** List of inherited class from FstringHash ( found them faster). */
	
	def __str__(self):
		return "\t"+Fport.__str__(self)+\
				"FportListHash - list : "+str(self.listHash)+"\n"
