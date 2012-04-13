#/***************************************************************************
#                             frouter.h
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

"""/** function : Manage the entire routing of evenDatas between routers,
               evenDoor, evenBoard and evenPrg.

    description :

  *@author Fabian Padilla
  */"""

__all__ = ["Frouter"]

from fdoor_file import Fdoor_file
from fdoor_cout import Fdoor_cout
from fprg_concat import Fdoor_concat

from fport import Fport
from fconfig import Fconfig
from fevenboard import FevenBoard
from fevendata import FevenData
from fstringhash import FstringHash
from fportlisthash import FportListHash

from globalvars import gvActionEnd
from globalvars import gvActionError

import evenjastrings as ES
from returncodes import RET_OK
from returncodes import RET_NOINFOS
from returncodes import RET_NOTEXIST

class Frouter(FportListHash):

    def __init__(self):
        FportListHash.__init__(self)

    def __str__(self):
        return "\t"+FportListHash.__str__(self)+\
                "Frouter - (null)\n"

    def start(self,port,param):
        """/** Starts import the config file ( or other stream), and sets the parentrouter.
        If the port (evenDoor and evenBoard) need to send an evenData. */"""
        ret = Fport.start(self,port,param)
        if ret == RET_OK:
            return self.createRoom()
        return ret

    def getClassInfos(self,classInfo):
        """/** Get the informations concerning the creation of a port (room, evenprg, etc...) */"""
        ret = RET_OK
        self.pushCurrent()
        if self.gotoChildren() != RET_OK:
            return RET_NOTEXIST

        def search(string):
            if self.Find(string) == RET_OK:
                return self.getContent()
            return None

        classInfo['type'] = search(ES.XML_CLASS)
        classInfo['conf'] = search(ES.XML_CONF)
        classInfo['lib'] = search(ES.XML_LIB)
        classInfo['debug'] = search(ES.XML_DEBUG)

        self.popCurrent()
        return ret

    def getLinkInfos(self,linkInfo):
        """/** Get the informations concerning the cration of a port (room, evenprg, etc...) */"""
        ret = RET_OK
        self.pushCurrent()
        if self.gotoChildren() != RET_OK:
            return RET_NOTEXIST

        def search(string):
            if self.Find(string) == RET_OK:
                return self.getContent()
            return None

        linkInfo['source'] = search(ES.XML_LNKSOURCE)
        linkInfo['type'] = search(ES.XML_LNKTYPE)
        linkInfo['value'] = search(ES.XML_LNKVALUE)
        linkInfo['fields'] = search(ES.XML_LNKFIELDS)
        linkInfo['dest'] = search(ES.XML_LNKDEST)

        self.popCurrent()
        return ret

    def createRoom(self):
        """/** Create a room with a structure defined by the config or node in start method */"""
        classInfos = {  'type':None,\
                'conf':None,\
                'lib':None,\
                'debug':None}

        linkInfos = {   'source':None,\
                'type':None,\
                'value':None,\
                'fields':None,\
                'dest':None}
        strH = FstringHash()
        port = Fport

        # search for rooms, boards, doors and programms
        def IMPORT_PORTS(A,B,CLASS):
            if self.Find(A,False) == RET_OK:
                while True:
                    self.pushCurrent()
                    # read informations
                    self.getClassInfos(classInfos)
                    # let's build and start this
                    # if both are None or strcasecmp
                    # TODO  ugliest code in this library
                    if ((classInfos['type']==None and B==None) or \
                            (B <> None and classInfos['type'] <> None\
                            and (classInfos['type'].upper() == B.upper()))):
                        childRoom = CLASS()
                        if classInfos['conf'] <> None:
                            childRoom.start(self,classInfos['conf'])
                        else:
                            childRoom.start(self,self.current)
                        ptr = self.listHash.addOrGet(childRoom)
                        if ptr <> None:
                            ptr = None
                            return RET_PORTEXIST
                    self.popCurrent()
                    # search for a next one
                    if self.FindNext(A,False) != RET_OK:
                        break

        self.resetCurrent()
        if self.gotoChildren() != RET_OK:
            return RET_NOINFOS
        # search and build
        IMPORT_PORTS( ES.XML_ROOM,None,Frouter)
        IMPORT_PORTS( ES.XML_ROOM,"ROOM",Frouter)
        IMPORT_PORTS( ES.XML_BOARD,None,FevenBoard)
        IMPORT_PORTS( ES.XML_BOARD,"BOARD",FevenBoard)

        IMPORT_PORTS( ES.XML_DOOR, "file", Fdoor_file)
        IMPORT_PORTS( ES.XML_DOOR, "cout", Fdoor_cout)
        IMPORT_PORTS( ES.XML_PRG, "concat", Fdoor_concat)

        # seach for <envenja_link>, if dosen't exists, create an evendata and send it
        if self.Find(ES.XML_LNK, False) != RET_OK:
            return RET_OK
        while True:
            self.pushCurrent()
            self.getLinkInfos(linkInfos)
            if linkInfos['source'] <> None:
                strH.setString(linkInfos['source'])
                port = self.listHash.Search(strH)
                # if this source has been built, send a ACT_SYS_ADDDEST msg
                if port <> None:
                    data = self.getFreeEvenData()
                    data.setData( ES.XML_LNKTYPE, linkInfos['type'])
                    data.setData( ES.XML_LNKVALUE, linkInfos['value'])
                    data.setData( ES.XML_LNKFIELDS, linkInfos['fields'])
                    data.setData( ES.XML_LNKDEST, linkInfos['dest'])

                    data.definePortAction( ES.ACT_SYS_ADDDEST, linkInfos['source'])
                    self.sendEvenDataSys(data,port)
            self.popCurrent()
            if self.FindNext( ES.XML_LNK,False) != RET_OK:
                break
        return RET_OK

    def receive_evenData(self,evenData):
        """/** Receive the evenData to be routed to the right router or port. */"""
        port = self.listHash.Search(evenData.getCurrentDestination().getPort())
        if port <> None:
            #// ... then send to it the evenData
            #// Now it send the evenData by sndMsg, but normally this will change after the realeas of V3.0
            #//    sendEvenData( evenData, port);
            #//    return RET_OK;
            #// ...this will work well too, but it is another principle
            return port.justDoIt(evenData)
        evenData.definePortAction(ES.ACT_ERROR)
        return RET_OK

    def justDoIt(self,evenData):
        """/** Methods called by Fstarter */"""
        tmp = evenData.getCurrentDestination().getAction()
        if tmp.equals(gvActionEnd) or tmp.equals(gvActionError):
            self.setFreeEvenData(evenData)
            return RET_OK
        return Fport.justDoIt(self,evenData)

    def end(self):
        """/** Deploy the end() until the port. */"""
        for I in range(self.listHash.getCount()):
            self.listHash.get(I).end()
        return Fconfig.endXml(self)


if __name__ == '__main__':

    import unittest

    router1 = Frouter()
    router2 = Frouter()

    class FrouterTestCase(unittest.TestCase):

        def test1Name(self):
            self.assertEquals(router1.start( None, "testezlog.xml"),RET_OK)
            strH = FstringHash()
            strH.setString( "TEST00")

            #// TEST Name from file
            self.assertEquals(router1.equals( strH),True)

            #// TEST from node config
            conf = Fconfig()
            conf.startXml( "testezlog.xml")
            router2.start( None, conf.getCurrent())
            self.assertEquals(router2.equals( strH),True)
            router1.end()
            router2.end()


    unittest.main()
