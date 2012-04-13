#/***************************************************************************
#                             fportlist.h
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

"""/** Inherited from Fport to add a listHash.

  function : maintain a list in
             FevenDoor : 

  description : work as Fport.

  *@author Fabian Padilla
  */"""

__all__ = ["FportList"]

from fport import Fport
from flist import Flist


class FportList(Fport):
	"""This class is nothing but a fport with a flist as atribute"""

	def __init__(self):
		Fport.__init__(self)	# force constructor
		self.list = Flist	#/** List of inherited class from FstringHash ( found them faster). */

	def __str__(self):
		return "\t"+Fport.__str__(self)+\
				"FportList - list : "+str(self.list)+"\n"
