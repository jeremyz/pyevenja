#/***************************************************************************
#                             fevendata.h
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


"""/** Door of the room.

  function : evenDoor of the room. Connect the room to external world.
             To a specific prototcol and data format.

  description : evenDoor would convert a specific data format to the internal
                evenData format and the evenData format to the external data format.

  *@author Fabian Padilla
  */"""

__all__ = ["FevenDoor"]

from flist import Flist
from fstringhash import FstringHash
from globalvars import gvActionSysAddDest
from fportbkpevendata import FportBkpEvenData

from returncodes import RET_OK
from returncodes import RET_NOTEXIST

from evenjastrings import XML_LNKTYPE
from evenjastrings import XML_LNKVALUE
from evenjastrings import XML_LNKFIELDS
from evenjastrings import XML_LNKDEST
from evenjastrings import TXT_NULL

class FspecialDestination:
    """ """

    def __init__(self, linkTypesNames, valueA, linkFieldsNames, linkDest):
        self.type = FstringHash()
        self.value = FstringHash()
        self.fields = FstringHash()
        self.dest = FstringHash()

        self.type.setString(linkTypesNames)
        self.value.setString(valueA)
        self.fields.setString(linkFieldsNames)
        self.dest.setString(linkDest)


class FevenDoor(FportBkpEvenData):
    """ """
    def __init__(self):
        FportBkpEvenData.__init__(self)        # force constructor
        self.list = Flist()            #/** List of special destination */a

    def __del__(self):
        """I believe this is for no use."""
        while self.list.getCount():
                self.list.remove(0)

    def __str__(self):
        return "\t"+FportBkpEvenData.__str__(self)+\
                "FevenDoor - list : "+str(self.list)+"\n"

    def justDoItSys(self,evenData):
        """/** Methods called by Fstarter. */"""
        ret = RET_OK
        if evenData.getCurrentDestination().getAction().equals(gvActionSysAddDest):
            ret = self.list.add( FspecialDestination(evenData.getData(XML_LNKTYPE),\
                                 evenData.getData(XML_LNKVALUE),\
                                 evenData.getData(XML_LNKFIELDS),\
                                 evenData.getData(XML_LNKDEST)))
        self.setFreeEvenData(evenData)
        return ret

    def sendEvenData(self,evenData):
        """/** Methods to enable all ports to sends evenDatas to a port. */"""
        spDestToDo = None
        if evenData.getCurrentDestination() != RET_NOTEXIST:
            return FportBkpEvenData.sendEvenData(self,evenData)
        for I in range(self.list.getCount()):
            spDest = self.list.get(I)
            spDestString = spDest.type.getString()
            if spDestString != TXT_NULL:                # if we got a destination
                evenData.setLinkFieldsNames(spDestString)
            if spDestString == TXT_NULL or evenData.equals(spDest.value):
                if spDestToDo <> None:
                    evenDataToDo = getFreeEvenData()
                    evenDataToDo = copyFrom(evenData)
                    evenDataToDo.setSource(self.getString())
                    evenDataToDo.setLinkFieldsNames(spDestToDo.fields.getString())
                    evenDataToDo.resetDestination()
                    evenDataToDo.addDestinatio(spDestToDo.dest.getString())
                    FportBkpEvenData.sendEvenData(self,evenDataToDo)
                spDestToDo = spDest
        if spDestToDo:    # something to send
            evenData.setSource(self.getString())
            evenData.setLinkFieldsNames(spDestToDo.fields.getString())
            evenData.resetDestination()
            evenData.addDestination(spDestToDo.dest.getString())
            FportBkpEvenData.sendEvenData(self,evenData)
        else:
            self.parent.setFreeEvenData(evenData)

    def getFreeEvenData(self):
        """/** Get a new evenData. */"""
        return self.parent.getFreeEvenData()
