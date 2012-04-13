#/***************************************************************************
#                             flist.h
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

"""/** List that manage a table of pointer.

  function : maintain a list of pointer.

  description : pointers (or other 32bit values) can be
  - added
  - returned by giving the idx in the list
  - returned by giving the idx in the list and removed from them
  - older returned and removed from the list, by FisrtInfirstOut order

  *@author Fabian Padilla
  */"""

__all__ = ["Flist"]

from returncodes import RET_NOTEXIST

class Flist:
	""" This class is just an other wrapper around the python builtin list.
	It dosen't use exceptions 'cause exceptions suck ! """
	def __init__(self):
		self.L = []

	def __str__(self):
		ret = ''
		for I in self.L:
			ret += str(I.__class__)+' : '+I.getString()+'  - '
		return 'Flist - '+ret

	def add(self, el):
		self.L.append(el)
		#return RET_OK				# TzurTcH - no need
		
	def get(self, idx):
		if idx<0 or idx>=len(self.L):
			return RET_NOTEXIST
		return self.L[idx]
	
	def remove(self, idx):
		if idx<0 or idx>=len(self.L):
			return RET_NOTEXIST
		tmp,self.L = self.L[idx], self.L[:idx]+self.L[idx+1:]
		return tmp
			
	def removeFifo(self):
		if len(self.L) == 0:
			return RET_NOTEXIST
		tmp, self.L = self.L[0], self.L[1:]
		return tmp
	
	def removeStack(self):
		if len(self.L) == 0:
			return RET_NOTEXIST
		return self.L.pop()
	
	def getCount(self):
		return len(self.L)
  

if __name__ == '__main__':

	import unittest

	
	class FlistTestCase(unittest.TestCase):

		def test1AddGetRemove(self):
			list = Flist()
			list.add("A")
			list.add("B")
			list.add("C")
			list.add("D")
			list.add("E")
			self.assertEquals(list.get(0),"A")
			self.assertEquals(list.get(1),"B")
			self.assertEquals(list.get(2),"C")
			self.assertEquals(list.get(3),"D")
			self.assertEquals(list.get(4),"E")
			self.assertEquals(list.remove(5),RET_NOTEXIST)
			self.assertEquals(list.remove(0),"A")
			self.assertEquals(list.remove(1),"C")
			self.assertEquals(list.remove(2),"E")
			self.assertEquals(list.remove(2),RET_NOTEXIST)
			self.assertEquals(list.remove(1),"D")
			self.assertEquals(list.remove(0),"B")
			self.assertEquals(list.remove(0),RET_NOTEXIST)
		
		def test2RemoveFifo(self):
			list = Flist()
			list.add("A")
			list.add("B")
			list.add("C")
			list.add("D")
			list.add("E")
			self.assertEquals(list.removeFifo(),"A")
			self.assertEquals(list.removeFifo(),"B")
			self.assertEquals(list.removeFifo(),"C")
			self.assertEquals(list.removeFifo(),"D")
			self.assertEquals(list.removeFifo(),"E")
			self.assertEquals(list.removeFifo(),RET_NOTEXIST)
		
		def test3RemoveStack(self):
			list = Flist()
			list.add("A")
			list.add("B")
			list.add("C")
			list.add("D")
			list.add("E")
			self.assertEquals(list.removeStack(),"E")
			self.assertEquals(list.removeStack(),"D")
			self.assertEquals(list.removeStack(),"C")
			self.assertEquals(list.removeStack(),"B")
			self.assertEquals(list.removeStack(),"A")
			self.assertEquals(list.removeStack(),RET_NOTEXIST)

		def test4GetCount(self):
			list = Flist()
			list.add("A")
			list.add("B")
			list.add("C")
			list.add("D")
			list.add("E")
			self.assertEquals(list.getCount(),5)

	unittest.main()
