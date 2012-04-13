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


# TODO check int() and float() cast
# TODO tmp file usage for dumping xml in memory is really ugly !!!

"""/** Kernel of the evenja and evendoor technology => the DATA.
  Data is the only that know where they want to go. They can go to an
  evenDoor or evenBoard.
  THIS SCENARIO OF USE IS COVERED BY THE FPL Foundaion Public Licence.
  COPYRIGHT 1992-2004 Fabian Padilla.

  *@author Fabian Padilla
  */"""

__all__ = ["FevenData"]

try:
    import libxml2
except:
    print "libxml2 not available ... aborting !!"
    import sys
    sys.exit(1)

from time import time

from flist import Flist
from fconfig import Fconfig
from fposition import Fposition
from fstringhash import FstringHash

import evenjastrings as ES
import returncodes as RC

# TzurTcH - speed up ;))
PREF = ES.XML_DESTINATION + ES.TREE_SEPARATOR_STR
PREF_DESTCOUNT = PREF + ES.XML_DESTCOUNT
PREF_CURRENTDEST = PREF + ES.XML_CURRENTDEST
PREF_DESTNUMBER = PREF + ES.XML_DESTNUMBER


class FevenData(Fconfig):

    def __init__(self):
        Fconfig.__init__(self)        # force constructor
        self.source = Fposition()    # Where the evenData as been created
        self.startToUse = 0        # Date and time when this evenData as been sent from the evenDoor
        self.destination = Flist()    # Where the evenData want to go
        self.currentDestination = 0    # this is it
        self.activePort = None        # The Active actual port where the data will be sent
        self.linkFieldsNames = Flist()    # Name of the fields that link two evenData
        self.datas = None        # Pointer of the start of datas
        self.splitBuffer = None        # Used for string splitting actions
        self.xmlBuffer = None        # Pointersof the xmlBuffer when methods
                        # setDatasFromString and getDatasFromString are called
        self.evenDataB = None        # When a merge is done in the evenBoards it contains the other evenData
        self.initDatas()

    def __str__(self):
        """you want a trace of all processed messages : print data in fstarter.execute"""
        level = 0
        buff = self.getDatasToString()
        ret = ""
        for I in range(len(buff)):
            ret += buff[I]
            if buff[I] == '>':
                if buff[I-1] == '?':                # start
                    pass
                elif buff[-1] == '/' or buff[I:I+3] == '></':    # end of an empty attribute
                    ret += '\n'+level*'\t'
                elif buff[I+1] != '<':                # attribute
                    ret += '\n'+(level+1)*'\t'
                else:                        # new level
                    level += 1
                    ret += '\n'+level*'\t'
            if buff[I] =='<':
                if buff[I-1] == '\n':                # start
                    pass
                if buff[I-1] != '>' and buff[I-1] != '\n':    # end of an attribute
                    ret = ret[:-1]
                    ret += '\n'+level*'\t'+'<'
                if buff[I+1] == '/':                # end of a level
                    level -=1
        return "\t"+Fconfig.__str__(self)+ret

    def __del__(self):
        """/** I beleive this is for no use. */"""
        self.xmlBuffer = None    # should be ok like this
        self.reset()
        self.endXml()

    def initDatas(self):
        """/** Init the Datas Structure. */"""
        self.startNewXml()
        self.addChildren(ES.XML_DATAS,None)
        self.gotoChildren()
        self.Find(ES.XML_DATAS,False)
        self.datas = self.current
        self.setString(ES.TXT_NOVALUES)

    def getSplitted(self,separator,string = ES.TXT_NULL):
        """/** Split string using separator, returns first part, keeps the rest in splitBuffer. */"""
        if string:
            self.splitBuffer = string.split(separator)
        if self.splitBuffer:
            if len(self.splitBuffer) >=2:
                ret, self.splitBuffer = self.splitBuffer[0], self.splitBuffer[1:]
            else:
                ret, self.splitBuffer = self.splitBuffer[0], None
            return ret
        return None

    def gotoTagName(self,name,create = True,onlyDatas = True):
        """/** Access the right TAG name in the Tree, or create it */"""
        str = self.getSplitted(ES.TREE_SEPARATOR, name)
        if onlyDatas:
            self.current = self.datas
        else:
            self.current = self.root
        while str:
            ret = self.gotoChildren()
            if ret == RC.RET_NOTEXIST and create:        # no children, but can create
                self.addChildren(str,None)
                self.gotoChildren()

            elif ret == RC.RET_NOTEXIST and not create:    # no children and can't create, sorry
                return RC.RET_NOTFOUND

            ret = self.Find(str,False)            # search for str no deep search !!
            if ret == RC.RET_NOTFOUND and create:        # not found, but can create
                self.gotoParent()
                self.addChildren(str,None)
                self.gotoChildren()
                self.Find(str,False)            # go to this new node

            elif ret == RC.RET_NOTFOUND and not create:    # not found and can't create, sorry
                return RC.RET_NOTFOUND
            str = self.getSplitted(ES.TREE_SEPARATOR)        # next...
        return RC.RET_OK

    def setMetaEvenDatasToXml(self):
        """/** put META evenData => Source, Destination, startTime, etc... */"""

        def SETMETADATA(A,B):
            self.gotoTagName(A,True,False)
            self.setContent(str(B))

        SETMETADATA(ES.XML_SOURCE,self.source.getString())        # set source
        SETMETADATA(ES.XML_STARTTIME,self.startToUse)            # set startToUse
        self.gotoTagName(ES.XML_DESTINATION,True,False)
        SETMETADATA(PREF_DESTCOUNT,self.destination.getCount())        # nbDest
        SETMETADATA(PREF_CURRENTDEST,self.currentDestination)        # set currentDestination

        for I in range(self.destination.getCount()):            # set destinations
            SETMETADATA(PREF_DESTNUMBER%I,self.destination.get(I).getString())

        S = ""
        for I in range(self.linkFieldsNames.getCount()):        # set linkFieldsNames
            S += self.linkFieldsNames.get(I).getString() + ES.FIELD_SEPARATOR_STR
        if S:
            S = S[:-1]
        SETMETADATA(ES.XML_LINKFIELDS,S)

    def getMetaEvenDatasFromXml(self):
        """/** get META evenData => Source, Destination, startTime, etc... */"""
        nbDest = 0

        def GETMETADATA(A,B=None):
            ret = self.gotoTagName(A,False,False)
            if ret == RC.RET_OK:
                if B:
                    B(self.getContent())
                else:
                    return self.getContent()
            else:                            # TzurTcH - I hope never beeing there
                from sys import exit
                from sys import stderr
                stderr.write("ERRRROOORRRR\n")
                exit(1)

        GETMETADATA(ES.XML_SOURCE,self.setSource)            # get source
        self.startToUse = float(GETMETADATA(ES.XML_STARTTIME))        # get startToUse
        nbDest = int(GETMETADATA(PREF_DESTCOUNT))            # get nbDest
        self.currentDestination = int(GETMETADATA(PREF_CURRENTDEST))    # get currentDestination

        for I in range(nbDest):
            GETMETADATA(PREF_DESTNUMBER%I,self.addDestination)    # get destinations
        GETMETADATA(ES.XML_LINKFIELDS,self.setLinkFieldsNames)        # get linkFieldsNames

    def setDatasFromXXX(self,newDoc):
        """/** end the sequence of importing datas to the tree */"""
        ret = RC.RET_OK
        if newDoc:
            self.endXml()
            self.doc = newDoc
            ret = self.startXml(self.doc.children)
            self.resetCurrent()
            self.gotoChildren()
            self.Find(ES.XML_DATAS,False)
            self.datas = self.current
            self.getMetaEvenDatasFromXml()
            self.updateHashValue()
            return ret
        return RC.RET_CONNATACCESS

    def updateHashValue(self,fieldName = None):
        """/** Update the hashValue. Take Data in the tree and update HashValue of the evenData
        fieldname : name of the field (in the data tree updated) */"""
        update = False
        count = self.linkFieldsNames.getCount()
        if fieldName:
            for I in range(count):
                if self.linkFieldsNames.get(I).getString()==fieldName:
                    update = True
                    break
        else:
            update = True
        if update:
            bkpCurrent = self.current
            nbExists = 0
            str =""
            for I in range(count):
                value = self.getData(self.linkFieldsNames.get(I).getString())
                if value != RC.RET_NOTFOUND:
                    nbExists += 1
                    str += value
            if nbExists == count:
                self.setString(str)
            else:
                self.setString(ES.TXT_NULL)
            self.current = bkpCurrent

    def setSource(self,source):
        """/** Set the source position => from where the evenData comes. */"""
        return self.source.setPosition(source)

    def getSource(self):
        """/** Get the source position => from where the evenData comes. */"""
        return self.source

    def addDestination(self,destinationA):
        """/** Set the destination position => to where the evenData goes. */"""
        ret = RC.RET_OK
        str = self.getSplitted(ES.DESTINATION_SEPARATOR, destinationA)
        while str:
            pos = Fposition()
            pos.setPosition(str)
            ret = self.destination.add(pos)
            str = self.getSplitted(ES.TREE_SEPARATOR)
        return ret

    def getCurrentDestination(self):
        """/** Get the destination position => to where the evenData goes. */"""
        return self.destination.get(self.currentDestination)

    def selectNextDestination(self):
        """/** Select next destination, ex.: after a evenBoard this can be a evenPrg */"""
        if self.currentDestination+1 < self.destination.getCount():
            self.currentDestination += 1
            self.activePort = 0
            return RC.RET_OK
        else:
            return RC.RET_NOTEXIST

    def resetDestination(self):
        """/** Remove all the destinations from the list */"""
        for I in range(self.destination.getCount()):
            self.destination.remove(0)
        self.currentDestination = 0

    def setLinkFieldsNames(self,linkFieldsNamesString):
        """/** Name of the fields that represent the link between two evenDatas. */"""
        str = self.getSplitted(ES.FIELD_SEPARATOR, linkFieldsNamesString)
        if self.linkFieldsNames.getCount():
            self.resetLinkFieldsNames()
        while str:
            s = FstringHash()
            s.setString(str)
            self.linkFieldsNames.add(s)
            str = self.getSplitted(ES.TREE_SEPARATOR)
        self.updateHashValue()
        if self.evenDataB:
            evenDataB = None
        return RC.RET_OK

    def resetLinkFieldsNames(self):
        """/** Remove all the destinations from the list */"""
        for I in range(self.linkFieldsNames.getCount()):
            self.linkFieldsNames.remove(0)


    def reset(self):
        """/** Reset the datas ( erase all informations) */"""
        self.source.setString(ES.TXT_NULL)
        self.startToUse = time()
        self.resetDestination()
        self.resetLinkFieldsNames()
        self.endXml()
        self.initDatas()

    def getStartToUse(self):
        """/** When the evenData as entered for the first time into a room. */"""
        return self.startToUse

    def setEvenDataB(self,evenData):
        """/** Set the other evenData merged with this */"""
        self.evenDataB = evenData

    def getEvenDataB(self):
        """/** Get the other evenData merged with this ( and remove the pointer) */"""
        tmp = self.evenDataB
        self.evenDataB = None
        return tmp

    def setData(self,nodeName,value):
        """/** Set a "Value" in the datastree. */"""
        ret = self.gotoTagName(nodeName)
        if ret == RC.RET_OK:
            ret = self.setContent(value)
            self.updateHashValue(nodeName)
        return ret

    def getData(self,nodeName):
        """/** Get the "Value" of the nodeName in the datastree. */"""
        ret = self.gotoTagName(nodeName, False)
        if ret == RC.RET_OK:
            return self.getContent()
        return ret

    def setDataInt(self,nodeName,value):
        """/** Set a int "Value" in the datastree. */"""
        ret = self.gotoTagName(nodeName)
        if ret == RC.RET_OK:
            ret = self.setContent(str(value))
            self.updateHashValue(nodeName)
        return ret

    def getDataInt(self,nodeName):
        """/** Get the int "Value" of the nodeName in the datastree. */"""
        ret = self.gotoTagName(nodeName, False)
        if ret == RC.RET_OK:
            return int(self.getContent())
        return ret

    def setDatasFromString(self,string):
        """/** Set ALL the datas of the datastree. All this new datas replace the old datas. */"""
        return self.setDatasFromXXX(libxml2.parseMemory(string, len(string)))

    def setDatasFromFile(self,fileName):
        """/** Set ALL the datas of the datastree. From a File or a stream. */"""
        return self.setDatasFromXXX(libxml2.parseFile(fileName))

    def getDatasToString(self,):
        """/** Get ALL the datas to a string (ex.: XML format). */"""
        if self.xmlBuffer:
            self.xmlFree(self.xmlBuffer)
        self.setMetaEvenDatasToXml()
        # no xmlDocDumpMemory !!                        # TzurTcH !!!!! Achtung !!!!!
        f=file(".__temp__XML","w")
        self.doc.dump(f)
        f.close()
        f=file(".__temp__XML","r")
        S = f.read()
        f.close()
        return S

    def getDatasToFile(self,fileName):
        """/** Get ALL the datas To a File or a stream. */"""
        self.setMetaEvenDatasToXml()
        if self.doc.saveFile(fileName):
            return RC.RET_OK
        return RC.RET_CANNOTSAVE

    def copyFrom(self,data):
        """/** Copy all information from another evenData. */"""
        return self.setDatasFromString(data.getDatasToString())

    def setActivePort(self,port):
        """/** Set the active port */"""
        self.activePort = port

    def getActivePort(self):
        """/** Get the active port */"""
        return self.activePort

    def definePortAction(self,action,portName = None):
        """/** Do an action */"""
        str=""
        if portName:
            str += portName
        str += ":" + action
        self.addDestination(str)
        if self.destination.getCount():
            self.currentDestination = self.destination.getCount()-1
        else:
            self.currentDestination = 0
        return RC.RET_OK


    def DUMP(self):
        return self.doc.saveFile("dump.xml")


if __name__ == '__main__':

    import unittest

    def getLinkFieldsNames(self):
        return self.linkFieldsNames

    FILE = "testezlog_save.xml"

    class FevendataTestCase(unittest.TestCase):


        def test1Source(self):
            data1 = FevenData()
            data1.setSource( "MySQL")
            self.assertEquals("MySQL",data1.getSource().getString())

        def test2Destination(self):
            data1 = FevenData()
            data1.addDestination( "gateUI")
            self.assertEquals(data1.getCurrentDestination().getPort().getString(),"gateUI")
            self.assertEquals(data1.selectNextDestination(),RC.RET_NOTEXIST)

            data1.resetDestination()

            data1.addDestination( "boardUI1")
            data1.addDestination( "prgUI1")
            data1.addDestination( "boardUI2")
            data1.addDestination( "prgUI2")

            self.assertEquals( data1.getCurrentDestination().getPort().getString(),"boardUI1")
            self.assertEquals( data1.selectNextDestination(),RC.RET_OK)
            self.assertEquals( data1.getCurrentDestination().getPort().getString(),"prgUI1")
            self.assertEquals( data1.selectNextDestination(),RC.RET_OK)
            self.assertEquals( data1.getCurrentDestination().getPort().getString(),"boardUI2")
            self.assertEquals( data1.selectNextDestination(),RC.RET_OK)
            self.assertEquals( data1.getCurrentDestination().getPort().getString(),"prgUI2")
            self.assertEquals( data1.selectNextDestination(),RC.RET_NOTEXIST)

            data1.resetDestination()

            data1.addDestination( "boardUI1;prgUI1;boardUI2;prgUI2");

            self.assertEquals( data1.getCurrentDestination().getPort().getString(),"boardUI1")
            self.assertEquals( data1.selectNextDestination(),RC.RET_OK)
            self.assertEquals( data1.getCurrentDestination().getPort().getString(),"prgUI1")
            self.assertEquals( data1.selectNextDestination(),RC.RET_OK)
            self.assertEquals( data1.getCurrentDestination().getPort().getString(),"boardUI2")
            self.assertEquals( data1.selectNextDestination(),RC.RET_OK)
            self.assertEquals( data1.getCurrentDestination().getPort().getString(),"prgUI2")
            self.assertEquals( data1.selectNextDestination(),RC.RET_NOTEXIST)

        def test3LnkFieldsname(self):
            data2 = FevenData()
            data2.setLinkFieldsNames( "Client/Address/Name,Client/AccountNumber")
            LINK2=data2.__dict__['linkFieldsNames']

            self.assertEquals( "Client/Address/Name",LINK2.get(0).getString())
            self.assertEquals( "Client/AccountNumber", LINK2.get(1).getString())

            #// Check a change of the linkFieldsNames directly without creating a new evenData
            data2.setLinkFieldsNames( "Ref1/Ref2/Ref3,Val1/Val2,Data1")

            self.assertEquals( "Ref1/Ref2/Ref3",LINK2.get( 0).getString())
            self.assertEquals( "Val1/Val2",LINK2.get(1).getString())
            self.assertEquals( "Data1", LINK2.get(2).getString())

        def test4Timer(self):
            data1 = FevenData()
            T = time()
            data1.reset()
            T1 = data1.getStartToUse()
            self.assertEquals( abs(T - T1) < 2,True)

        def test5SetAndGetDatas(self):
            data1 = FevenData()
            data1.setData( "Name", "Dupont")
            self.assertEquals( data1.getData( "Name"),"Dupont")
            data1.setData( "Account/Number", "012345678901234567")
            data1.setData( "Account/Name", "BANK Dupond")
            data1.setData( "Account/Devises/Rate/CHF", "1,234")
            data1.setData( "Account/Devises/Rate/DM", "1,2")
            self.assertEquals( data1.getData( "Account/Number"),"012345678901234567")
            self.assertEquals( data1.getData( "Account/Name"),"BANK Dupond")
            self.assertEquals( data1.getData( "Account/Devises/Rate/CHF"),"1,234")
            self.assertEquals( data1.getData( "Account/Devises/Rate/DM"),"1,2")

        def test6SetAndGetDatasInt(self):
            data1 = FevenData()
            data1.setDataInt( "Name", 10)
            self.assertEquals( data1.getDataInt( "Name"),10)
            data1.setDataInt( "Account/Number", 123)
            data1.setDataInt( "Account/Name", 200)
            data1.setDataInt( "Account/Devises/Rate/CHF", -176)
            data1.setDataInt( "Account/Devises/Rate/DM", 182)
            self.assertEquals( data1.getDataInt( "Account/Number"),123)
            self.assertEquals( data1.getDataInt( "Account/Name") ,200)
            self.assertEquals( data1.getDataInt( "Account/Devises/Rate/CHF"), -176)
            self.assertEquals( data1.getDataInt( "Account/Devises/Rate/DM"), 182)

        def test7SaveDatasFile(self):
            data1 = FevenData()
            data1 = FevenData()
            data1.setSource( "MySQL")

            data1.addDestination( "boardUI1")
            data1.addDestination( "prgUI1")
            data1.addDestination( "boardUI2")
            data1.addDestination( "prgUI2")
            data1.setLinkFieldsNames( "Client/Address/Name,Client/AccountNumber")

            data1.setData( "Account/Number", "123")
            data1.setData( "Account/Name", "200")
            data1.setDataInt( "Account/Devises/Rate/CHF", 176)
            data1.setDataInt( "Account/Devises/Rate/DM", 182)

            data1.getDatasToFile(FILE)

            S = "<?xml version=\"1.0\"?>\n<XML><evendata_datas><Account><Number>123</Number><Name>200</Name><Devises><Rate><CHF>176</CHF><DM>182</DM></Rate></Devises></Account></evendata_datas><evendata_source>MySQL</evendata_source><evendata_starttime>0</evendata_starttime><evendata_destination><evendata_destcount>4</evendata_destcount><evendata_currentdest>0</evendata_currentdest><evendata_dest0>boardUI1</evendata_dest0><evendata_dest1>prgUI1</evendata_dest1><evendata_dest2>boardUI2</evendata_dest2><evendata_dest3>prgUI2</evendata_dest3></evendata_destination><evendata_linkfields>Client/Address/Name,Client/AccountNumber</evendata_linkfields></XML>\n"
            self.assertEquals(S,file(FILE, "r").read())

        def test8LoadDatasFile(self):
            data2 = FevenData()
            LINK2=data2.__dict__['linkFieldsNames']
            data2.setDatasFromFile(FILE)
            self.assertEquals( data2.getSource().getString(),"MySQL")
            self.assertEquals( data2.getCurrentDestination().getString(),"boardUI1")
            data2.selectNextDestination()
            self.assertEquals( data2.getCurrentDestination().getString(),"prgUI1")
            data2.selectNextDestination()
            self.assertEquals( data2.getCurrentDestination().getString(),"boardUI2")
            data2.selectNextDestination()
            self.assertEquals( data2.getCurrentDestination().getString(),"prgUI2")
            self.assertEquals(data2.selectNextDestination(), RC.RET_NOTEXIST)

            self.assertEquals( "Client/Address/Name", LINK2.get(0).getString())
            self.assertEquals( "Client/AccountNumber", LINK2.get(1).getString())

            self.assertEquals( data2.getData( "Account/Number"),"123")
            self.assertEquals( data2.getData( "Account/Name"),"200")
            self.assertEquals( data2.getDataInt( "Account/Devises/Rate/CHF"), 176)
            self.assertEquals( data2.getDataInt( "Account/Devises/Rate/DM"), 182)

        def test9SaveDatasMemory(self):
            data1 = FevenData()
            data1.setSource( "MySQL")
            data1.addDestination( "boardUI1")
            data1.addDestination( "prgUI1")
            data1.addDestination( "boardUI2")
            data1.addDestination( "prgUI2")
            data1.setLinkFieldsNames( "Client/Address/Name,Client/AccountNumber")


            data1.setData( "Account/Number", "123")
            data1.setData( "Account/Name", "200")
            data1.setDataInt( "Account/Devises/Rate/CHF", 176)
            data1.setDataInt( "Account/Devises/Rate/DM", 182)

            global buff
            buff = data1.getDatasToString()

            S = "<?xml version=\"1.0\"?>\n<XML><evendata_datas><Account><Number>123</Number><Name>200</Name><Devises><Rate><CHF>176</CHF><DM>182</DM></Rate></Devises></Account></evendata_datas><evendata_source>MySQL</evendata_source><evendata_starttime>0</evendata_starttime><evendata_destination><evendata_destcount>4</evendata_destcount><evendata_currentdest>0</evendata_currentdest><evendata_dest0>boardUI1</evendata_dest0><evendata_dest1>prgUI1</evendata_dest1><evendata_dest2>boardUI2</evendata_dest2><evendata_dest3>prgUI2</evendata_dest3></evendata_destination><evendata_linkfields>Client/Address/Name,Client/AccountNumber</evendata_linkfields></XML>\n"

            self.assertEquals(S,buff)

        def test10LoadDatasMemory(self):
            data2 = FevenData()
            self.test9SaveDatasMemory()
            data2.setDatasFromString( buff)
            LINK2=data2.__dict__['linkFieldsNames']

            self.assertEquals(data2.getSource().getString(),"MySQL")
            self.assertEquals( data2.getCurrentDestination().getString(),"boardUI1")
            data2.selectNextDestination()
            self.assertEquals( data2.getCurrentDestination().getString(),"prgUI1")
            data2.selectNextDestination()
            self.assertEquals( data2.getCurrentDestination().getString(),"boardUI2")
            data2.selectNextDestination()
            self.assertEquals( data2.getCurrentDestination().getString(),"prgUI2")
            self.assertEquals( data2.selectNextDestination(), RC.RET_NOTEXIST)

            self.assertEquals( "Client/Address/Name", LINK2.get(0).getString())
            self.assertEquals( "Client/AccountNumber", LINK2.get(1).getString())

            self.assertEquals( data2.getData( "Account/Number"), "123")
            self.assertEquals( data2.getData( "Account/Name"), "200")
            self.assertEquals( data2.getDataInt( "Account/Devises/Rate/CHF"), 176)
            self.assertEquals( data2.getDataInt( "Account/Devises/Rate/DM"), 182)

        def test11HashValue(self):
            return
            data1.setLinkFieldsNames( "Client/Address/Name,Client/AccountNumber")
            data1.setData( "Client/Address/Name", "Dupont")
            data1.setData( "Client/AccountNumber", "200")

            strH = FstringHash()
            strH.setString( "Dupont200")
            self.assertEquals(strH.equals( data1),True)

            strH.setString( "Dupont201")
            self.assertEquals(strH.equals( data1),False)

        def test12CopyFrom(self):
            return
            data1.setDatasFromFile("testezlog_save.xml")
            data1.setLinkFieldsNames( "Client/Address/Name,Client/AccountNumber")
            data1.setData( "Client/Address/Name", "Dupont")
            data1.setData( "Client/AccountNumber", "200")

            data2.copyFrom( data1)

            self.assertEquals(data1.equals( data2),True)

            buff1 = data1.getDatasToString()
            buff2 = data2.getDatasToString()
            self.asserEquals(len(buff1),len(buff2))
            self.asserEquals(buff1,buff2)


    unittest.main()
