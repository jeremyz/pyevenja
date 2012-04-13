#/***************************************************************************
#                             fposition.h
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


"""/** Define the position ( source OR destination) of the evenData.
  function : maintain the stringHashs for the computer, rooms, port, action.
  Format example : www.revena.com/room1/room2/port:normal

  description : method "setPosition" set all position informations this mean
  - compute
  - room tree
  - port
  - action.
  Then these informations are retrieved with getComputer, getRoom, getPort,
  getAction methods.

  *@author Fabian Padilla
  */"""

__all__ =["Fposition"]

from flist import Flist
from fstringhash import FstringHash

from returncodes import RET_OK
from evenjastrings import ACT_WAIT_NOTHING
from evenjastrings import ACT_NORMAL
from evenjastrings import TXT_NULL

class Fposition(FstringHash):
    """This class keeps informations on  the computer / a list of rooms / a port /an action / and time"""

    def __init__(self):
        FstringHash.__init__(self)    # force constructor
        self.computer = FstringHash()    # /** computer destination or source. */
        self.rooms = Flist()        # /** room destination or source. */
        self.nbLevel = 0
        self.port = FstringHash()    # /** port destination or source. */
        self.action = FstringHash()    # /** action to do at the position (source or destination). */
        self.waitTime = 0        # /** wait time in the action */
        #/** waitTime unit (ex.: y(year), n(month), d(day), h(hour), m(minute), s(seconde) or x(milliseconde))*/
        self.unitWaitTime = ACT_WAIT_NOTHING
        self.positionActived = False

    def __del__(self):
        """I belive this is for no use"""
        self.resetPosition()

    def __str__(self):
        return "\t"+FstringHash.__str__(self)+\
                "Fposition - computer : "+str(self.computer)+\
                " - rooms : "+str(self.rooms)+\
                " - nbLevel : "+str(self.nbLevel)+\
                " - port : "+str(self.port)+\
                " - action : "+str(self.action)+\
                " - waitTime : "+str(self.waitTime)+\
                " - unitWaitTime : "+str(self.unitWaitTime)+\
                " - positionAtived : "+str(self.positionActived)+"\n"

    def resetPosition(self):
        """/** reset position (erase datas) */"""
        if self.positionActived:
            self.computer.setString(TXT_NULL)
            # delete rooms
            for I in range(self.nbLevel):
                self.rooms.remove(0)            # TzurTcH - no self.getRoom()
            self.nbLevel = 0
            self.port.setString(TXT_NULL)
            self.action.setString(TXT_NULL)
            self.waitTime = 0
            self.unitWaitTime = ACT_WAIT_NOTHING
            self.positionActived = False

    def setPosition(self, position):
        """/** Set the source or the destination of an evenData. */"""
        self.resetPosition()
        self.nbLevel = 0
        self.setString(position)

        # search for - computer/rooms<F2>
        buffer = position.split("/")
        if len(buffer) > 1:
            # computer name ?
            ret = None
            try:
                ret = buffer[0].index(".")
            except:
                None
            if ret:
                self.computer.setString(buffer[0])
                buffer = buffer[1:]
            # import rooms
            bufferRooms=""
            for I in buffer[:-1]:
                self.rooms.add( FstringHash())
                if self.nbLevel:
                    bufferRooms += "/"
                bufferRooms += I
                self.rooms.get(self.nbLevel).setString(bufferRooms)
                self.nbLevel += 1
        # search for - port:action
        buffer = buffer[-1].split(":")
        self.port.setString(buffer[0])
        if len(buffer) > 1:
            # search for - action,time
            buffer = buffer[1].split(",")
            self.action.setString(buffer[0])
            if len(buffer) > 1:
                self.waitTime = int(buffer[1][:-1])
                self.unitWaitTime = buffer[1][-1]
            else:
                self.waitTime = 0
                self.unitWaitTime = ACT_WAIT_NOTHING
        else:
            self.action.setString(ACT_NORMAL)
            self.waitTime = 0
            self.unitWaitTime = ACT_WAIT_NOTHING
        self.positionActived = True
        return RET_OK

    def getComputer(self):
        """/** Get the computer name. If the evenData needs to go to another computer. */"""
        return self.computer

    def getRoom(self, level = 0):
        """/** Get the room for destination or source. */"""
        if level < self.nbLevel:
            return self.rooms.get(level)
        else:
            return None

    def getNbLevel(self):
        """/** Number of levels in the rooms routing tree. */"""
        return self.nbLevel

    def getPort(self):
        """/** Get the port of the position (source or destination). This means an evenDoor or a evenBoard. */"""
        return self.port

    def getAction(self):
        """/** Get the action of the position (source or destination). */"""
        return self.action

    def getWaitTime(self):
        """/** Get the amount of waiting time (unity is another get function) */"""
        return self.waitTime

    def getUnitWaitTime(self):
        """/** Get the unity time y,n,d,h,m,s or x */"""
        return self.unitWaitTime

    def copyFrom(self, pos):
        """/** Copy a position From another Fposition class */"""
        self.resetPosition()
        self.computer.copyFrom(pos.getComputer())

        for I in range(pos.getNbLevel()):
            new = FstringHash()
            new.copyFrom(pos.getRoom(I))
            self.rooms.add(new)
        self.nbLevel = pos.getNbLevel()
        self.port.copyFrom(pos.getPort())
        self.action.copyFrom(pos.getAction())
        self.waitTime = pos.getWaitTime()
        self.unitWaitTime = pos.getUnitWaitTime()
        self.positionActived = True



if __name__ == '__main__':

    import unittest
    from evenjastrings import *

    pos1 = Fposition()
    pos2 = Fposition()

    class FpositionTestCase(unittest.TestCase):

        def test1Splitting(self):
            pos1.setPosition( "WWW.TEST.ORG/room1/room2/port")
            self.assertEquals(pos1.getNbLevel(),2)
            self.assertEquals("WWW.TEST.ORG",pos1.getComputer().getString())
            self.assertEquals("room1",pos1.getRoom(0).getString())
            self.assertEquals("room1/room2",pos1.getRoom(1).getString())
            self.assertEquals("port",pos1.getPort().getString())
            self.assertEquals(ACT_NORMAL,pos1.getAction().getString())

            pos1.setPosition("room1/room2/port:destination1Data")
            self.assertEquals(pos1.getNbLevel(),2)
            self.assertEquals(TXT_NULL,pos1.getComputer().getString())
            self.assertEquals("room1",pos1.getRoom(0).getString())
            self.assertEquals("room1/room2",pos1.getRoom(1).getString())
            self.assertEquals("port",pos1.getPort().getString())
            self.assertEquals(ACT_DESTINATION1DATA,pos1.getAction().getString())

            pos1.setPosition( "port:wait,5s")
            self.assertEquals(pos1.getNbLevel(),0)
            self.assertEquals(TXT_NULL,pos1.getComputer().getString())
            self.assertEquals(pos1.getRoom(0),None)
            self.assertEquals("port",pos1.getPort().getString())
            self.assertEquals(ACT_WAIT,pos1.getAction().getString())
            self.assertEquals(pos1.getWaitTime(),5)
            self.assertEquals( pos1.getUnitWaitTime(),ACT_WAIT_SECOND)

            pos1.setPosition( ":wait,5d")
            self.assertEquals(pos1.getNbLevel(),0)
            self.assertEquals(TXT_NULL,pos1.getComputer().getString())
            self.assertEquals(pos1.getRoom(0),None)
            self.assertEquals(TXT_NULL,pos1.getPort().getString())
            self.assertEquals(ACT_WAIT,pos1.getAction().getString())
            self.assertEquals(pos1.getWaitTime(),5)
            self.assertEquals(pos1.getUnitWaitTime(),ACT_WAIT_DAY)

            pos1.setPosition( ":end")
            self.assertEquals(pos1.getNbLevel(),0)
            self.assertEquals(TXT_NULL,pos1.getComputer().getString())
            self.assertEquals(pos1.getRoom(0),None)
            self.assertEquals(TXT_NULL,pos1.getPort().getString())
            self.assertEquals(ACT_END,pos1.getAction().getString())

        def test2Copy(self):
            pos1.setPosition( "WWW.TEST.ORG/room1/room2/port:wait,1d")
            pos2.copyFrom( pos1)
            self.assertEquals(pos1.getComputer().equals( pos2.getComputer()),True)
            self.assertEquals(pos1.getRoom(0).equals(pos2.getRoom(0)),True)
            self.assertEquals(pos1.getRoom( 1).equals( pos2.getRoom( 1)),True)
            self.assertEquals(pos1.getPort().equals( pos2.getPort()),True)
            self.assertEquals(pos1.getAction().equals( pos2.getAction()),True)
            self.assertEquals(pos1.getWaitTime(),pos2.getWaitTime())
            self.assertEquals(pos1.getUnitWaitTime(),pos2.getUnitWaitTime())

    unittest.main()
