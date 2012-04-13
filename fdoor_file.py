#/***************************************************************************
#                             fdoor_file.h
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

__all__ = ["Fdoor_file"]

from fport import Fport
from fevendoor import FevenDoor

from globalvars import gvActionGet

from evenjastrings import ACT_GET
from returncodes import RET_OK
from returncodes import RET_CANNOTACCESS
from returncodes import RET_CANNOTSAVE

class Fdoor_file(FevenDoor):

    def __init__(self):
        FevenDoor.__init__(self)    # force constructor
        self.file = None

    def __str__(self):
        return "\t"+FevenDoor.__str__(self)+\
                "Fdoor_file - file : "+str(self.file)+"\n"

    def start(self,port,node):
        ret = Fport.start(self,port,node)
        if ret == RET_OK:
            self.gotoChildren()
            if self.Find("filename",False) == RET_OK:
                str = self.getContent()
                try:
                    self.file = file(str,"rw")
                except:
                    return RET_CANNOTACCESS
                self.filename = str
            if file <> None:
                data = self.getFreeEvenData()
                data.definePortAction(ACT_GET,self.getString())
                self.sendEvenData(data)
            else:
                return RET_CANNOTACCESS
        return ret

    def receive_evenData(self,evenData):
        if evenData.getCurrentDestination().getAction().equals(gvActionGet):
            line = self.file.readline()
            if line:
                # send line
                evenData.reset()
                evenData.setData("filename",self.filename)
                evenData.setData("TXT",line)
                self.sendEvenData(evenData)

                # say "I got more"
                data = self.getFreeEvenData()
                data.definePortAction(ACT_GET, self.getString())
                self.sendEvenData(data)
        return RET_OK


    def end(self):
        ret = Fport.end(self)
        if ret == RET_OK and self.file <> None:
            try:
                self.file.close()
            except:
                return RET_CANNOTSAVE
        return ret
