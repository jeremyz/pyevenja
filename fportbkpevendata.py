#/***************************************************************************
#                             fportbkpevendata.h
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

  function : secure the use of evenData send to evenPrg or evebDoor.

  description : work as Fport.

  *@author Fabian Padilla
  */"""

__all__ = ["FportBkpEvenData"]

from fport import Fport
from evenjastrings import ACT_ERROR

class FportBkpEvenData(Fport):
    """This class is a wrapper arounf Fport class for security purpose"""

    def __init__(self):
        Fport.__init__(self)    # force constructor
        self.evenDataA = None    #/** Backup of the evenDatas that need to be sends by sendEvenData */

    def __str__(self):
        return "\t"+Fport.__str__(self)+\
                "FportBkpEvenData - evenDataA : "+str(self.evenDataA)+"\n"

    def justDoIt(self,evenData):
        """/** Methods called by Fstarter */"""
        self.evenDataA = evenData
        ret = Fport.justDoIt(self,evenData)
        if self.evenDataA:
            self.evenDataA.definePortAction(ACT_ERROR)
            self.sendEvenData(self.evenDataA)
        return ret

    def sendEvenData(self,evenData,portDestination = None):
        """/** Methods to enable all ports to sends evenDatas to a port */"""
        if (self.evenDataA == evenData):
            self.evenDataA = None
        Fport.sendEvenData(self,evenData,portDestination)

    def sendEvenDataSys(self,evenData,portDestination = None):
        """/** Methods to enable all ports to sends evenDatas to a port */"""
        if (self.evenDataA == evenData):
            self.evenDataA = None
        Fport.sendEvenDataSys(self,evenData,portDestination)
