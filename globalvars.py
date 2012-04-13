#/***************************************************************************
#                             globalvars.h
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

from fstringhash import FstringHash
import evenjastrings as ES

#gvActionNormal = None
#gvActionDestination1Data = None
#gvActionDestination2Data = None
#gvActionFollowDestination = None
#gvActionWait = None

#gvActionAdd = None
#gvActionUpdate = None
#gvActionDelete = None
#gvActionGet = None
#gvActionFind = None

#gvActionEnd = None
#gvActionError = None

#// SYSTEM ACTIONS
#gvActionSysAddDest = None

#// PARAMETERS
#gvNoValues = None

#def initGlobalVars():
#	
#	global gvActionNormal
#	global gvActionDestination1Data
#	global gvActionDestination2Data
#	global gvActionFollowDestination
#	global gvActionWait
#	global gvActionAdd
#	global gvActionUpdate
#	global gvActionDelete
#	global gvActionGet
#	global gvActionFind
#	global gvActionEnd
#	global gvActionError
#	global gvActionSysAddDest
#	global gvNoValues
#	
gvActionNormal = FstringHash()
gvActionNormal.setString(ES.ACT_NORMAL)

gvActionDestination1Data = FstringHash()
gvActionDestination1Data.setString(ES.ACT_DESTINATION1DATA)

gvActionDestination2Data = FstringHash()
gvActionDestination2Data.setString(ES.ACT_DESTINATION2DATA)

gvActionFollowDestination = FstringHash()
gvActionFollowDestination.setString(ES.ACT_FOLLOWDESTINATION)

gvActionWait = FstringHash()
gvActionWait.setString(ES.ACT_WAIT)

gvActionAdd = FstringHash()
gvActionAdd.setString(ES.ACT_ADD)

gvActionUpdate = FstringHash()
gvActionUpdate.setString(ES.ACT_UPDATE)

gvActionDelete = FstringHash()
gvActionDelete.setString(ES.ACT_DELETE)

gvActionGet = FstringHash()
gvActionGet.setString(ES.ACT_GET)

gvActionFind = FstringHash()
gvActionFind.setString(ES.ACT_FIND)

gvActionEnd = FstringHash()
gvActionEnd.setString(ES.ACT_END)

gvActionError = FstringHash()
gvActionError.setString(ES.ACT_ERROR)

gvActionSysAddDest = FstringHash()
gvActionSysAddDest.setString(ES.ACT_SYS_ADDDEST)

gvNoValues = FstringHash()
gvNoValues.setString(ES.TXT_NOVALUES)


#if __name__ == '__main__':
#	
#	import unittest
#	D = dir()
#	L=[	ES.ACT_ADD,\
#		ES.ACT_DELETE,\
#		ES.ACT_DESTINATION1DATA,\
#		ES.ACT_DESTINATION2DATA,\
#		ES.ACT_END,\
#		ES.ACT_ERROR,\
#		ES.ACT_FIND,\
#		ES.ACT_FOLLOWDESTINATION,\
#		ES.ACT_GET,\
#		ES.ACT_NORMAL,\
#		ES.ACT_SYS_ADDDEST,\
#		ES.ACT_UPDATE,\
#		ES.ACT_WAIT,\
#		ES.TXT_NOVALUES]
#	
#	class globalvarsTestCase(unittest.TestCase):
#
#		def testInit(self):
#			initGlobalVars()
#			for I in D:
#				if I[:2]=="gv":
#					self.assertNotEquals(eval(D[D.index(I)]).getString(),D.index(I))
#	unittest.main()
