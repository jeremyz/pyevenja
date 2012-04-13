#/***************************************************************************
#                             fconfig.h
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


"""/** Class done to open or load and close or save the config in tree files
  (XML now, but nobody what's would be in the future, ex: LDAP).
  function : It is the access to a tree of information needed by the class which inheritate from Fconfig.
  This class can be modified if the datas are stored in another system than a file.
  The file can be a stream or every other input stream data (better in a tree like XML or LDAP).

  description :
  - Methods start and startNew will connect Fconfig to a tree (XML in this example, but can be a
     LDAP or other tree style).
  - Method end will enable to save the tree (not always needed).
  - Method resetCurrent will reset the current pointer to the node when last method start as been called.
  - Methods gotoNext, gotoPrev, gotoChildren, gotoParent enable to move inside the tree.
  - Methods Find and FindNext enable to search by name an tree Node.

  Fconfig is a generic caller for a tree access. This enable to change the type of supported tree XML,
    LDAP or others, without having to update the evenja kernel.

  *@author Fabian Padilla
  */"""

__all__ = ["Fconfig"]

try:
    import libxml2
except:
    print "libxml2 not available ... aborting !!"
    import sys
    sys.exit(1)

from flist import Flist
from fstringhash import FstringHash
import returncodes as RC
import evenjastrings as ES

class Fconfig(FstringHash):
    """ This class gives you the ability to walk around and through an XML document.
    This document can be created from sratch, read from a file, completed and modified, and so on.
    You can also execute some research queries... Everything seems to be safe /~\/~\."""

    def __init__(self):
        FstringHash.__init__(self)    # force contrustor
        self.fileName = None            # yeah, this is it !
        self.doc = None            # the document
        self.root = None        # the root node
        self.firstCurrent = None    # the first node of the tree
        self.current = None        # the current node
        self.stackCurrent = Flist()     # a stack used to push and pop self.current

    def __str__(self):
        return "\t"+FstringHash.__str__(self) +\
                " Fconfig - File : "+str(self.fileName)+\
                " - Current_Name : "+str(self.getName())+\
                " - Current_Content : "+str(self.getContent())+"\n"

    def startXml(self, param):
        """/** Read an XML tree, param may be a file name or an xmlNode. */"""
        if isinstance(param,str):
            # a filename is given, parse this file
            self.fileName = param
            try:
                self.doc = libxml2.parseFile(param)
            except:
                return RC.RET_CANNOTACCESS
            param = self.doc.children
        # a node is given or we have one now
        if not isinstance(param,libxml2.xmlNode):
            return RC.RET_CANNOTACCESS
        self.root = param.doc.children
        self.firstCurrent = param
        self.current = param
        if self.gotoChildren() != RC.RET_OK:
            return RC.RET_NOTEXIST
        # find <evenja_name> tag and put it's content in our FstringHash
        if self.Find(ES.XML_NAME, False) != RC.RET_OK:
            return RC.RET_NONAME
        string = self.getContent()
        if string == RC.RET_NONODESELECTED:        # don't need this ...
            return RC.RET_NONAME
        self.setString(string)
        self.resetCurrent()
        return RC.RET_OK

    def startNewXml(self, fileName = None):
        """/** Create a new XML tree. */"""
        if fileName:
            self.fileName = fileName
        else:
            self.fileName = None
        try:
            self.doc = libxml2.newDoc(ES.XML_VERSION)
            self.doc.newChild(None, ES.XML_XML, None)
        except:
            return RC.RET_CANNOTCREATE
        self.root = self.doc.children
        self.firstCurrent = self.root
        self.current = self.root
        self.setString(ES.TXT_NEW)
        return RC.RET_OK

    def endXml(self):
        """/** Close the XML tree. Save it if a file name exists. */"""
        if self.doc and self.fileName:
            if self.doc.saveFile(self.fileName) == -1:
                return RC.RET_CANNOTEND
        if self.doc:
            self.doc.freeDoc()
        self.doc = None
        self.root = None
        self.firstCurrent = None
        self.current = None
        self.fileName = None
        return RC.RET_OK

    def getCurrent(self):
        """/** Get the current node. */"""
        return self.current

# WALKING METHODS

    def resetCurrent(self, fromRoot = False):
        """/** Set current node to the root one if fromRoot, otherwise to the first one. */"""
        if fromRoot:
            self.current = self.root
        else:
            self.current = self.firstCurrent

    def gotoFirst(self):
        """/** Go to the first node of the current branch. */"""
        if not self.current:
            return RC.RET_NONODESELECTED
        self.current = self.current.parent.children
        if self.current.type != "element":
            return self.gotoNext()
        return RC.RET_OK

    def gotoLast(self):
        """/** Go to the last node of the current branch. */"""
        if not self.current:
            return RC.RET_NONODESELECTED
        self.current = self.current.parent.last
        if self.current.type != "element":
            return self.gotoPrev()
        return RC.RET_OK

    def gotoNext(self):
        """/** Go to the next node of the current branch. */"""
        if not self.current:
            return RC.RET_NONODESELECTED
        if not self.current.next:
            return RC.RET_NOTEXIST
        node = self.current.next
        while node.type != "element" and node.next:    # walk 'till you find
            node = node.next
        if node.type == "element":
            self.current = node
            return RC.RET_OK
        return RC.RET_NOTEXIST

    def gotoPrev(self):
        """/** Go to the previous node of the current branch. */"""
        if not self.current:
            return RC.RET_NONODESELECTED
        if not self.current.prev:
            return RC.RET_NOTEXIST
        node = self.current.prev
        while node.type != "element" and node.prev:    # walk 'till you find
            node = node.prev
        if node.type == "element":
            self.current = node
            return RC.RET_OK
        return RC.RET_NOTEXIST

    def gotoChildren(self):
        """/** Go to the children node of the current node. */"""
        if not self.current:
            return RC.RET_NONODESELECTED
        if not self.current.children:
            return RC.RET_NOTEXIST
        tmp = self.current
        self.current = self.current.children
        if self.current.type == "element":
            return RC.RET_OK
        ret = self.gotoNext()
        if ret == RC.RET_NOTEXIST:
            self.current = tmp
        return ret

    def gotoParent(self):
        """/** Go to the parent node of the current node. */"""
        if not self.current:
            return RC.RET_NONODESELECTED
        if not self.current.parent:
            return RC.RET_NOTEXIST
        tmp = self.current
        self.current = self.current.parent
        if self.current.type == "element":
            return RC.RET_OK
        ret = self.gotoPrev()
        if ret == RC.RET_NOTEXIST:
            self.current = tmp
        return ret

    def Search(self, name, subTree = True):
        """/** Find a name, with or without tree recusivity, using preorder path.
        self.current is saved from not_found case */"""
        if not self.current:
            return RC.RET_NONODESELECTED
        bkp = self.current                        # save self.current
        while True:
            if self.getName() == name:
                return RC.RET_OK
            if subTree and self.current.children:            # maybe deeper ??
                if self.gotoChildren() == RC.RET_OK:
                    if self.Search(name,subTree) == RC.RET_OK:
                        return RC.RET_OK
                    else:
                        self.gotoParent()
            if RC.RET_OK !=self.gotoNext():                # maybe further ??
                self.current = bkp                # recover self.current
                return RC.RET_NOTFOUND

    def Find(self, name, subTree = True):
        """/** Find a name from th etop of the tree, with or without tree recusivity. */"""
        ret = self.gotoFirst()
        if ret != RC.RET_OK:
            return ret
        return self.Search(name,subTree)

    def FindNext(self, name, subTree = True):
        """/** Find next name, with or without tree recusivity. */"""
        ret = self.gotoNext()
        if ret != RC.RET_OK:
            return ret
        return self.Search(name,subTree)


# RETRIEVE INFORMATIONS

    def getName(self):
        """/** Get the Name of the current Node. */"""
        if self.current:
            return self.current.name
        return RC.RET_NONODESELECTED

    def setName(self, name):
        """/** Set the Name of the current Node. */"""
        if not self.current:
            return RC.RET_NONODESELECTED
        self.current.setName(name)
        return RC.RET_OK

    def getContent(self):
        """/** Get the Content of the current Node. */"""
        if not self.current:
            return RC.RET_NONODESELECTED
        currentA = self.current.children
        if currentA:
            return currentA.content
        return ES.TXT_NULL

    def setContent(self, content):
        """/** Set the Content of the current Node. */"""
        if not self.current:
            return RC.RET_NONODESELECTED
        if content <> None:
            self.current.setContent(content)
        else:
            self.current.setContent(ES.TXT_NULL)
        return RC.RET_OK

# CREATE ADN DELETE NODES

    def addChildren(self, name, content = None):
        """/** Create a new node (the current node is the parent). */"""
        if not self.current:
            return RC.RET_NONODESELECTED
        self.current.newChild(None,name,content)
        if self.doc and not self.root:
            self.root = self.doc.children
            self.firstCurrent = self.root
            self.current = self.root
        return RC.RET_OK

    def removeCurrent(self):
        """/** Remove the current node (recursively).
        After remove operation, goto the previous node if exists or to the next, or the parent*/"""
        str = self.getName()
        if str == RC.RET_NONODESELECTED or str is None:
            return RC.RET_NONODESELECTED
        if str.upper() == ES.XML_XML.upper():            # TzurTcH - case insensitive should be ok
            return RC.RET_OK
        toRemove = self.current
        if self.current.prev:
            self.gotoPrev()
        elif self.current.next:
            self.gotoNext()
        elif self.current.parent:
            self.gotoParent()
        # maybe it will empty this tree ...
        if self.root == toRemove or self.firstCurrent == toRemove or self.root.doc.children == toRemove:
            self.root = None
            self.firstCurrent = None
            self.current = None
        toRemove.unlinkNode()
        toRemove.freeNode()
        return RC.RET_OK

# STACK MEMORY CAPABILITIES

    def pushCurrent(self):
        """/** Push the Current position to the stack. */"""
        self.stackCurrent.add(self.current)

    def popCurrent(self):
        """/** Pop the Current position from the stack. */"""
        if self.stackCurrent.getCount():
            self.current = self.stackCurrent.removeStack()

if __name__ == '__main__':

    import unittest
    from evenjastrings import *

    conf =  Fconfig()

    class FconfigTestCase(unittest.TestCase):

        def test1FileName(self):
            self.assertEquals(conf.startXml( "testezlog.xml"),RC.RET_OK)
            self.assertEquals(conf.endXml(),RC.RET_OK)

        def test2NewTree(self):
            self.assertEquals(conf.startNewXml(),RC.RET_OK)
            self.assertEquals(conf.endXml(),RC.RET_OK)
            self.assertEquals(conf.startNewXml( "testezlog_addnode.xml"),RC.RET_OK)
            self.assertEquals(conf.endXml(),RC.RET_OK)

        def test3StartNode(self):
            self.assertEquals(conf.startXml( "testezlog.xml"),RC.RET_OK)
            conf1 = Fconfig()
            conf1.startXml( conf.getCurrent())
            conf1.gotoChildren()
            self.assertEquals(ES.XML_NAME.upper(),conf1.getName().upper())
            conf1.endXml()
            self.assertEquals(conf.endXml(),RC.RET_OK)

        def test4Node(self):
            self.assertEquals(conf.startXml( "testezlog.xml"),RC.RET_OK)
            conf.gotoChildren()
            self.assertEquals(ES.XML_NAME, conf.getName())
            self.assertEquals("TEST00", conf.getContent())
            conf.gotoNext()
            self.assertEquals(ES.XML_ROOM, conf.getName())
            conf.gotoChildren()
            self.assertEquals(ES.XML_NAME, conf.getName())
            self.assertEquals("Room1", conf.getContent())
            conf.gotoNext()
            self.assertEquals(ES.XML_DOC, conf.getName())
            self.assertEquals("FirstRoom", conf.getContent())
            conf.gotoNext()
            conf.gotoPrev()
            self.assertEquals(ES.XML_DOC, conf.getName())
            self.assertEquals("FirstRoom", conf.getContent())
            conf.gotoPrev()
            conf.gotoNext()
            self.assertEquals(ES.XML_DOC, conf.getName())
            self.assertEquals("FirstRoom", conf.getContent())
            self.assertEquals(conf.endXml(),RC.RET_OK)

        def test5ParentChildren(self):
            self.assertEquals(conf.startXml( "testezlog.xml"),RC.RET_OK)
            self.assertEquals(ES.XML_XML.upper(), conf.getName().upper())
            self.assertEquals(conf.gotoChildren(),RC.RET_OK)

            self.assertEquals(ES.XML_NAME, conf.getName())
            self.assertEquals("TEST00", conf.getContent())
            self.assertEquals(conf.gotoChildren(),RC.RET_NOTEXIST)
            self.assertEquals(ES.XML_NAME, conf.getName())
            self.assertEquals("TEST00", conf.getContent())

            self.assertEquals(conf.gotoParent(),RC.RET_OK)
            self.assertEquals(ES.XML_XML.upper(), conf.getName().upper())
            self.assertEquals(conf.gotoParent(),RC.RET_NOTEXIST)

            conf.resetCurrent()
            self.assertEquals(conf.gotoChildren(),RC.RET_OK)
            self.assertEquals(ES.XML_NAME, conf.getName())
            self.assertEquals(conf.endXml(),RC.RET_OK)

        def test6FirstLast(self):
            self.assertEquals(conf.startXml( "testezlog.xml"),RC.RET_OK)
            conf.gotoChildren()
            conf.gotoNext()
            conf.gotoChildren()
            conf.gotoLast()
            self.assertEquals(ES.XML_CONF, conf.getName())
            self.assertEquals(conf.gotoNext(),RC.RET_NOTEXIST)
            conf.gotoFirst()
            self.assertEquals(ES.XML_NAME, conf.getName())
            self.assertEquals(conf.gotoPrev(),RC.RET_NOTEXIST)
            conf.gotoNext()
            self.assertEquals(ES.XML_DOC, conf.getName())
            self.assertEquals(conf.endXml(),RC.RET_OK)

        def test7Find(self):
            self.assertEquals(conf.startXml( "testezlog.xml"),RC.RET_OK)
            if conf.Find(ES.XML_NAME):
                self.assertEquals(ES.XML_NAME, conf.getName())
                self.assertEquals("Room1", conf.getContent())
                conf.pushCurrent()
                conf.FindNext(ES.XML_DOC)
                self.assertEquals(ES.XML_DOC, conf.getName())
                self.assertEquals("FirstRoom", conf.getContent())
                conf.popCurrent()
                conf.FindNext(ES.XML_DOC, false)
            self.assertEquals(conf.Find(ES.TXT_NULL),RC.RET_NOTFOUND)
            self.assertEquals(conf.endXml(),RC.RET_OK)

        def test8NewNode(self):
            self.assertEquals(conf.startNewXml( "testezlog_addnode.xml"),RC.RET_OK)
            conf.addChildren( ES.XML_NAME, "Room1")
            conf.addChildren( ES.XML_DOC, "FirstRoom")
            conf.addChildren( ES.XML_CONF, "REMOVETEST")

            conf.gotoChildren()
            conf.gotoLast()
            self.assertEquals(ES.XML_CONF, conf.getName())
            conf.removeCurrent()
            self.assertEquals(ES.XML_DOC, conf.getName())
            self.assertEquals("FirstRoom", conf.getContent())

            conf.gotoParent()    # XML
            self.assertEquals(ES.XML_XML, conf.getName())
            conf.addChildren(ES.XML_CONF, "REMOVETEST")
            conf.gotoChildren()
            conf.gotoLast()
            conf.gotoPrev()
            self.assertEquals(ES.XML_DOC, conf.getName())
            self.assertEquals("FirstRoom", conf.getContent())
            conf.removeCurrent()
            self.assertEquals(ES.XML_NAME, conf.getName())
            self.assertEquals("Room1", conf.getContent())

            conf.gotoParent()
            conf.addChildren(ES.XML_DOC, "FirstRoom")
            conf.gotoChildren()
            conf.removeCurrent()
            self.assertEquals(ES.XML_CONF, conf.getName())
            self.assertEquals("REMOVETEST", conf.getContent())

            self.assertEquals(conf.endXml(),RC.RET_OK)

        def testBigBuild(self):
            """TzurTcH's test suite"""
            self.assertEquals(conf.startNewXml( "DEEP.xml"),RC.RET_OK)
            self.assertEquals(conf.getName(),XML_XML)
            self.assertEquals(conf.addChildren( ES.XML_NAME, "Room1"),RC.RET_OK)
            self.assertEquals(conf.addChildren( ES.XML_NAME, "Room2"),RC.RET_OK)
            self.assertEquals(conf.addChildren( ES.XML_NAME, "Room3"),RC.RET_OK)
            self.assertEquals(conf.addChildren( ES.XML_NAME, "Room4"),RC.RET_OK)
            self.assertEquals(conf.addChildren( ES.XML_NAME, "Room5"),RC.RET_OK)
            self.assertEquals(conf.gotoChildren(),RC.RET_OK)
            self.assertEquals(conf.getContent(),"Room1")

            self.assertEquals(conf.gotoLast(),RC.RET_OK)
            self.assertEquals(conf.getContent(),"Room5")
            self.assertEquals(conf.gotoLast(),RC.RET_OK)
            self.assertEquals(conf.getContent(),"Room5")

            self.assertEquals(conf.addChildren( ES.XML_DOC, "child_of_5"),RC.RET_OK)
            self.assertEquals(conf.gotoNext(),RC.RET_NOTEXIST)
            self.assertEquals(conf.getContent(),"Room5")

            self.assertEquals(conf.addChildren( ES.XML_DOC, "child_of_5_two"),RC.RET_OK)
            self.assertEquals(conf.addChildren( ES.XML_DOC, "child_of_5_three"),RC.RET_OK)
            self.assertEquals(conf.getContent(),"Room5")

            self.assertEquals(conf.gotoFirst(),RC.RET_OK)
            self.assertEquals(conf.getContent(),"Room1")
            self.assertEquals(conf.gotoFirst(),RC.RET_OK)
            self.assertEquals(conf.getContent(),"Room1")
            self.assertEquals(conf.addChildren( ES.XML_DOC, "child_of_1"),RC.RET_OK)
            self.assertEquals(conf.gotoPrev(),RC.RET_NOTEXIST)
            self.assertEquals(conf.getContent(),"Room1")

            self.assertEquals(conf.addChildren( ES.XML_DOC, "child_of_1_two"),RC.RET_OK)
            self.assertEquals(conf.getContent(),"Room1")
            self.assertEquals(conf.addChildren( ES.XML_DOC, "child_of_1_three"),RC.RET_OK)

            self.assertEquals(conf.gotoNext(),RC.RET_OK)
            self.assertEquals(conf.getContent(),"Room2")
            self.assertEquals(conf.gotoNext(),RC.RET_OK)
            self.assertEquals(conf.getContent(),"Room3")
            self.assertEquals(conf.gotoNext(),RC.RET_OK)
            self.assertEquals(conf.getContent(),"Room4")
            self.assertEquals(conf.addChildren( ES.XML_DOC, "child_of_4"),RC.RET_OK)
            self.assertEquals(conf.gotoPrev(),RC.RET_OK)
            self.assertEquals(conf.getContent(),"Room3")
            self.assertEquals(conf.gotoPrev(),RC.RET_OK)
            self.assertEquals(conf.getContent(),"Room2")
            self.assertEquals(conf.addChildren( ES.XML_DOC, "child_of_2"),RC.RET_OK)
            self.assertEquals(conf.gotoNext(),RC.RET_OK)
            self.assertEquals(conf.getContent(),"Room3")

            self.assertEquals(conf.addChildren( ES.XML_DOC, "child_of_3"),RC.RET_OK)
            self.assertEquals(conf.addChildren( "SEARCH", "child_of_3_two"),RC.RET_OK)

            conf.pushCurrent()
            self.assertEquals(conf.getContent(),"Room3")
            conf.resetCurrent(False)
            self.assertEquals(conf.getName(),XML_XML)
            self.assertEquals(conf.Find("SEARCH"),RC.RET_OK)
            conf.popCurrent()

            self.assertEquals(conf.addChildren( ES.XML_DOC, "child_of_3_three"),RC.RET_OK)
            self.assertEquals(conf.getContent(),"Room3")
            self.assertEquals(conf.gotoChildren(),RC.RET_OK)
            self.assertEquals(conf.getContent(),"child_of_3")
            self.assertEquals(conf.gotoLast(),RC.RET_OK)
            self.assertEquals(conf.getContent(),"child_of_3_three")
            self.assertEquals(conf.gotoChildren(),RC.RET_NOTEXIST)
            self.assertEquals(conf.getContent(),"child_of_3_three")

            self.assertEquals(conf.gotoParent(),RC.RET_OK)
            self.assertEquals(conf.getContent(),"Room3")
            self.assertEquals(conf.gotoParent(),RC.RET_OK)
            self.assertEquals(conf.gotoChildren(),RC.RET_OK)
            self.assertEquals(conf.getContent(),"Room1")

            self.assertEquals(conf.gotoParent(),RC.RET_OK)
            self.assertEquals(conf.getName(),ES.XML_XML)
            self.assertEquals(conf.gotoParent(),RC.RET_NOTEXIST)
            self.assertEquals(conf.gotoParent(),RC.RET_NOTEXIST)
            self.assertEquals(conf.getName(),ES.XML_XML)
            self.assertEquals(conf.removeCurrent(),RC.RET_OK)

            self.assertEquals(conf.gotoChildren(),RC.RET_OK)
            self.assertEquals(conf.getContent(),"Room1")
            self.assertEquals(conf.gotoChildren(),RC.RET_OK)
            self.assertEquals(conf.getContent(),"child_of_1")
            self.assertEquals(conf.gotoParent(),RC.RET_OK)
            self.assertEquals(conf.removeCurrent(),RC.RET_OK)
            self.assertEquals(conf.getContent(),"Room2")
            self.assertEquals(conf.Find("NOTHING"),RC.RET_NOTFOUND)
            self.assertEquals(conf.getContent(),"Room2")
            self.assertEquals(conf.FindNext("NOTHING"),RC.RET_NOTFOUND)
            self.assertEquals(conf.getContent(),"Room3")

            self.assertEquals(conf.gotoPrev(),RC.RET_OK)
            self.assertEquals(conf.FindNext("SEARCH"),RC.RET_OK)
            self.assertEquals(conf.getContent(),"child_of_3_two")
            self.assertEquals(conf.gotoParent(),RC.RET_OK)
            self.assertEquals(conf.FindNext("SEARCH"),RC.RET_NOTFOUND)
            self.assertEquals(conf.getContent(),"Room4")
            self.assertEquals(conf.getName(),ES.XML_NAME)
            self.assertEquals(conf.gotoNext(),RC.RET_OK)
            self.assertEquals(conf.getContent(),"Room5")

            self.assertEquals(conf.gotoParent(),RC.RET_OK)
            self.assertEquals(conf.getName(),XML_XML)
            self.assertEquals(conf.endXml(),RC.RET_OK)


    unittest.main()
