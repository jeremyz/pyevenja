#/***************************************************************************
#                             flisthash.h
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

# TODO it could maybe be a D={}, sounds faster and easier....

"""/** Special list that manage the link between Hash value and the evenData pointer.

  function : maintain a list of SINGLE FstringHash ( single is define by HashValue)

  description :
  - search : search for an existing FstringHash with the same hashValue
  - addOrGet and addOrRemove only add methods available. Then only single hashValue exist.

  *@author Fabian Padilla
  */"""

__all__ = ["FlistHash"]

from flist import Flist
from fstringhash import FstringHash

class FlistHash(Flist):
	""" This class is a wrapper arounf the flist class, providing some search capabilities"""

	def __init__(self):
		Flist.__init__(self)		# force constructor

	def __str__(self):
		return "\t"+Flist.__str__(self)+\
				"FlistHash - (null)\n"
	
	#def SearchPos(self,fstringHash):
	#	"""/** Search the position of the stringhash name.
	#	Return the position in the list or None if not found. */"""
	#	ret = None
	#	print self.L
	#	for I in self.L:
	#		if I.equals(fstringHash):
	#			return self.L.index(I)
	#	return ret
		
	
	def Search(self,fstringHash):
		"""/** Search if same name (stringhash) exist */"""
		for I in self.L:
			if I.equals(fstringHash):
				return I
		return None
	
	def addOrGet(self,fstringHash):
		"""/** If the same name exist in the list then get it from the list.
		If not, add stringhash in the list then return None. */"""
		pos = self.Search(fstringHash)
		if pos <> None:
			return pos
		self.add(fstringHash)
		return None
	
	def addOrRemove(self,fstringHash):
		"""/** If the same name exist in the list, then removes and return it.
		If not, then add to the list and return None. */"""
		pos = self.Search(fstringHash)
		if pos <> None:
			self.L.remove(pos)
			return pos
		self.add(fstringHash)
		return None
  

if __name__ == '__main__':

	import unittest
	from OSconfig import START_ELEMENTS
	
	List = FlistHash()
	
	str=[FstringHash(),FstringHash(),FstringHash(),FstringHash(),FstringHash()]
	STR=["TEST", "TEST1", "TEST", "TEST1", "TEST2"]
	str[0].setString(STR[0])
	str[1].setString(STR[1])
	str[2].setString(STR[2])
	str[3].setString(STR[3])
	str[4].setString(STR[4])
	
	class FlistHashTestCase(unittest.TestCase):
	
		def test1HashAddOrGet(self):
			self.assertEquals(List.addOrGet(str[0]),None)
			self.assertEquals(List.addOrGet(str[1]),None)
			self.assertEquals(List.addOrGet(str[2]).equals(str[2]),True)
			self.assertEquals(List.addOrGet(str[3]).equals(str[3]),True)
			self.assertEquals(List.addOrGet(str[4]),None)
		
		def test2HashAddOrRemove(self):
			self.assertEquals(List.addOrRemove(str[0]).equals(str[0]),True)
			self.assertEquals(List.addOrRemove(str[1]).equals(str[1]),True)
			self.assertEquals(List.addOrRemove(str[2]),None)
			self.assertEquals(List.addOrRemove(str[3]),None)
			self.assertEquals(List.addOrRemove(str[4]).equals(str[4]),True)
			self.assertEquals(List.addOrRemove(str[2]).equals(str[2]),True)
			self.assertEquals(List.addOrRemove(str[3]).equals(str[3]),True)
		
		def test3HashSearch(self):
			for I in range (START_ELEMENTS+10):
				buffer = "TEST%d"%I
				str1 = FstringHash()
				str1.setString(buffer)
				self.assertEquals(List.addOrGet( str1),None)
			buffer = "TEST%d"%(START_ELEMENTS-10)
			str1 = FstringHash()
			str1.setString(buffer)
			self.assertEquals(List.Search(str1).getString(),"TEST%d"%(START_ELEMENTS-10))

			
	unittest.main()
