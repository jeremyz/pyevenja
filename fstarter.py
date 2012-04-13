#/***************************************************************************
#                             fstarter.h
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

"""/** First class of evenja and evendoor to be created.
  This class will ask the firstRouter to create the first level of classes.

  *@author Fabian Padilla
  */"""


__all__ = ["Fstarter"]


from frouter import Frouter
from fevendata import FevenData
from fstringhash import FstringHash

from returncodes import RET_OK
from evenjastrings import XML_SERVER

class Fstarter(Frouter):
    """This is the main dispather, it receives all messages"""

    def __init__(self):
        Frouter.__init__(self)        # force constructor
        #/** Is the software a server (deamon) or a normal software.
        # A Server or deamon software wait until a signal ask for the end
        # A normal software wil end when nothing is to do (at the end) */
        self.server = False
        self.exit = False

    def __str__(self):
        return "\t"+Frouter.__str__(self)+\
                "Fstarter - (null)\n"

    def setExit(self):
        """/** Kill the application */"""
        self.exit = True

    def start(self,FileName):
        """/** Open the config file and transmit the first level of the rooms to the firstRouter. */"""
        ret = Frouter.start(self,None,FileName)        # set None as parent router
        if ret == RET_OK:
            self.pushCurrent()
            self.server = not self.Find(XML_SERVER)
            self.popCurrent()
        return ret

    def execute(self,trace):
        """/** Method called by the "main" of the application.
        It send an evenData to all evenBoard and then to all evenDoor to really start the work of the rooms.
        And wait until a TERM signal arrives from theself.__class__. OS. */"""

        if trace:
            while True:
                while self.listMsgSys.getCount() or self.listMsg.getCount():
                    if self.listMsgSys.getCount():
                        data = self.listMsgSys.removeFifo()
                        print '<?xml version="1.0"?>'
                        print '< *** SYS MSG *** />'
                        print data
                        data.getActivePort().justDoItSys(data)
                    else:
                        data = self.listMsg.removeFifo()
                        print '<?xml version="1.0"?>'
                        print '< *** MSG *** />'
                        print data
                        data.getActivePort().justDoIt(data)
                    if self.exit:
                        break
                if not self.server or self.exit:
                    break
                # TODO a small time out maybe ???

        else:
            while True:
                while self.listMsgSys.getCount() or self.listMsg.getCount():
                    if self.listMsgSys.getCount():
                        data = self.listMsgSys.removeFifo()
                        data.getActivePort().justDoItSys(data)
                    else:
                        data = self.listMsg.removeFifo()
                        data.getActivePort().justDoIt(data)
                    if self.exit:
                        break
                if not self.server or self.exit:
                    break
                # TODO a small time out maybe ???

        return RET_OK

    def end(self):
        """/** Manage if Fstarter saves the config file ( in a dinamyc configuration of rooms).
        Or if it is not needed because it is a static configuration. */"""
        return Frouter.end(self)




if __name__ == '__main__':

    import unittest

    starter1 = Fstarter();
    starter2 = Fstarter();

    class FstarterTestCase(unittest.TestCase):

        def test1Name(self):
            self.assertEquals(starter1.start( "testezlog.xml"),RET_OK)

            strH = FstringHash()
            strH.setString( "TEST00")

            #// TEST Name from file
            self.assertEquals(starter1.equals( strH),True)

            starter1.end()

    unittest.main()
