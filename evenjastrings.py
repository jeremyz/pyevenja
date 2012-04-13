#/***************************************************************************
#                             evenjastrings.h
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

"""strings of the evenja kernel"""

#/** xml strings (names of xml tags) for config files*/
XML_XML         = "XML"               #/** XML tag to define XML definition */

#/** Tags for the first level of the XML config tree */
XML_SERVER      = "evenja_server"     #/** XML tag to define if the software is a server (wait until an end signal) */
XML_ROOM        = "evenja_room"       #/** XML tag to define a room */
XML_DOOR        = "evenja_door"       #/** XML tag to define a door */
XML_BOARD       = "evenja_board"      #/** XML tag to define a board */
XML_PRG         = "evenja_prg"        #/** XML tag to define a prg */
XML_INIT        = "evenja_init"       #/** XML tag to start a evenPrg that initialise something
                                            #    for some enduser functionnalities */
#/** Tags for the second level of the XML config tree */
XML_NAME        = "evenja_name"       #/** XML tag containing the Name of a room, door, board and prg */
XML_DOC         = "evenja_doc"        #/** XML tag to contain documentation about room, door, board and prg */
XML_CLASS       = "evenja_class"      #/** XML tag to have the name of the class */
XML_CONF        = "evenja_conf"       #/** XML tag to have the name of the physical configuration file (ex: "hello.xml" */
XML_LIB         = "evenja_lib"        #/** XML tag to have the name of the physical library (ex: "hello.so" or "hello.dll") */
XML_DEBUG       = "evenja_debug"      #/** XML tag to enable the viewer to be connected to the port */
XML_LNK         = "evenja_link"       #/** XML tag Parameters to link an evenData to port */

#/** Tags for the third level of the XML config tree */
XML_LNKSOURCE   = "evenja_linksource" #/** XML tag Source of the evenDtata to link with ??? */
XML_LNKTYPE     = "evenja_linktype"   #/** XML tag Name of the fields that determine the type */
XML_LNKVALUE    = "evenja_linkvalue"  #/** XML tag Value corresponding to the type */
XML_LNKFIELDS   = "evenja_linkfields" #/** XML tag to contain the list of the fields names to make the right link */
XML_LNKDEST     = "evenja_linkdest"   #/** XML tag Destination of the evenData after link checked ok */

#/** xml strings ( names of xml tags) for evendatas files */
XML_DATAS       = "evendata_datas"        #/** XML tag to define a datas */
XML_SOURCE      = "evendata_source"       #/** Source of the data */
XML_STARTTIME   = "evendata_starttime"    #/** Time when the data as start */
XML_DESTINATION = "evendata_destination"  #/** List of all destinations */
XML_DESTCOUNT   = "evendata_destcount"    #/** Number of destinations */
XML_CURRENTDEST = "evendata_currentdest"  #/** Actual destination number */
XML_DESTNUMBER  = "evendata_dest%d"       #/** Destination number (completed by software */
XML_LINKFIELDS  = "evendata_linkfields"   #/** List of all fields to do the right link */

#// -------------------------------------------------------------------------
#// -------------------------------------------------------------------------
#// ACTIONS strings
#// ---------------

#// -------------------------------------------------------------------------
#/** evenja SYSTEM ACTIONS
#  evenDoor, evenBoard and evenPrg actions */
ACT_SYS_START       = "SYS_START"     #/** Start a port, after creation */
ACT_SYS_UPDATE      = "SYS_UPDATE"    #/** Update a port */
ACT_SYS_END         = "SYS_END"       #/** End a port, before deletion */
ACT_SYS_STOP        = "SYS_STOP"      #/** Stop the work inside the port */
ACT_SYS_CONTINUE    = "SYS_CONTINUE"  #/** Continue the work inside the port (after a stop) */
ACT_SYS_ADDDEST     = "SYS_ADDDEST"   #/** Add a special destination to an evenDoor */
ACT_SYS_REMDEST     = "SYS_REMDEST"   #/** Remove a special destination to an evenDoor */
ACT_SYS_TESTMODE    = "SYS_TESTMODE"  #/** Enable the check of a port with the configuration of them, at runtime */

#// -------------------------------------------------------------------------
#/** SOFTWARE ACTIONS.
#    Standard actions implemented in the evenja kernel.
#    Actions for evenPorts */
ACT_NORMAL      = "normal"      #/** No specific action, each Fport have is own "normal" action */


# /** Action for evenBoard */

#/** no special action, no link with another evenData (with the linkValue). Used in the evenPrg. */
ACT_DESTINATION1DATA  = "destination1Data"

#/** it waits until another evenData arrives in the same evenBoard (with the same linkValue) and
#follows the Destination of them. */
ACT_DESTINATION2DATA  = "destination2Data"

#/** if another evenData with the same linkValue is waiting in the evenBoard, then follows the destination of that evenData.
#If no evenData with the same linkValue isn't waiting, then it wait inside the evenBoard for another evenData. */
ACT_FOLLOWDESTINATION = "followDestination"

#/** it works like "destination2Data" if another evenData with the same linkValue is already inside the evenBoard.
#If no evenData with the same linkValue is inside the evenBoard,
#then it waits a time defined after the Action (ex: wait,100s). */
ACT_WAIT              = "wait"


#/** Actions for evenDoor */

#/** Add the evenData to Fport ( ex.: if it is an evenDoor of a DB then Add the datas to the Database) */
ACT_ADD               = "add"

#/** Update the evenData to Fport ( ex.: if it is an evenDoor of a DB then Update the record of the Database) */
ACT_UPDATE            = "update"

#/** Delete the evenData to Fport ( ex.: if it is an evenDoor of a DB then Delete the record of the Database) */
ACT_DELETE            = "delete"

#/** Get an evenData from a Port ( ex.: if is is an evenDoor of a file, get the next line) */
ACT_GET               = "get"

#/** Find the evenData to Fport (ex.: if it is a evenDoor of a DB then Find the record of the Database) */
ACT_FIND              = "find"

#/** special Action for some evenDoors that will receive informations in the evenData.
#The evenDoor does the request corresponding to this information and sends the evenData to the next point of the list
#of destinations. Ex. : evenDoor does a" SELECT" in a SQL database and puts the result inside the evenData. */
ACT_CALLBACK          = "callback"

#/** The evenData goes to a list of freeEvenDatas inside the nearest router, to be used as soon as possible */
ACT_END               = "end"

#/** The evenData goes to a specific evenPort where all errors are sents. Like a log, but it can be each evenPort inherited. */
ACT_ERROR             = "error"

#/** Format of the wait time when ACT_WAIT is used */
ACT_WAIT_NOTHING      = ' '                   #/** In fact, don't wait */
ACT_WAIT_YEAR         = 'y'
ACT_WAIT_MONTH        = 'n'
ACT_WAIT_DAY          = 'd'
ACT_WAIT_HOUR         = 'h'
ACT_WAIT_MINUTE       = 'm'
ACT_WAIT_SECOND       = 's'
ACT_WAIT_MILLISEC     = 'x'

#// -------------------------------------------------------------------------
#/** Internal Names
#    Just for fun and coherence */
XML_VERSION   = "1.0"           #/** Version of XML (compatible) */
TXT_NEW       = "NEW"           #/** Name of a new tree */
TXT_NULL      = ""              #/** Null string */
FIELD_SEPARATOR     = ','           #/** Separator of fields */
FIELD_SEPARATOR_STR = ","           #/** Separator of fields */
TREE_SEPARATOR      = '/'           #/** Separator of the XML TREE TAG NAME */
TREE_SEPARATOR_STR  = "/"           #/** Separator of the XML TREE TAG NAME */
DESTINATION_SEPARATOR     = ';'     #/** Separator of destination */
DESTINATION_SEPARATOR_STR = ";"     #/** Separator of destination */
TXT_NOVALUES        = "NOVALUES"    #/** Value that tke an evenData when no values are alreadyin the data tree */

#// -------------------------------------------------------------------------

