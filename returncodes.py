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

"""/** This header includes the retrurn codes for the evenja, evendoor, starter and evenRouter packages. */"""


#// If all is OK ( most of the time ?? ;) )
RET_OK =  0
RET_KO = -1

#// Standard return problems (memory, timeout, etc...)
RET_MEMORYSPACE = -10

#// developpement errors
RET_NOTIMPLEMENTED = -1001			#/* Method not already implmented*/
RET_NOTIMPLEMENTED_TXT = "NOT IMPLEMENTED"	#/* Text version */

#// Erros which can be generated at start of the application (before the rooms are working)
RET_NOPARAMS = -2001	#// The parameter is not available

#// Returns in normal usage of the evenja and evendoor technology need to be managed by the class
RET_INTERNAL        = -10000
#RET_FILENAME2LONG   = RET_INTERNAL - 1  #/* The FileName is too long > MAX_PATH */
#RET_STRING2LONG     = RET_INTERNAL - 2  #/* String is too long */
RET_PORTEXIST       = RET_INTERNAL - 3  #/* A router exist with the same name */
RET_NONAME          = RET_INTERNAL - 4  #/* No name exist for this port */
RET_NOINFOS         = RET_INTERNAL - 5  #/* No informations */

#// Returns in normal usage of the tree or ldap used for configuration or data storage
RET_TREE            = -11000
RET_CANNOTACCESS    = RET_TREE - 1  #/* Cannot access the stream (file or other) */
RET_CANNOTCREATE    = RET_TREE - 2  #/* The creation of the document is not possible */
RET_CANNOTEND       = RET_TREE - 3  #/* Cannot end the stream (save file or other save datas) */
RET_NONODESELECTED  = RET_TREE - 4  #/* Current = 0 */
RET_NOTEXIST        = RET_TREE - 5  #/* {Next,Prev,Children or Parent} Node not exist and cannot be set as the current */
RET_NOTFOUND        = RET_TREE - 6  #/* Nothing found, in the search */

RET_CANNOTSAVE      = RET_TREE - 7  #/* Cannot save the file */
#RET_		    = ""

