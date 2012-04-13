#/***************************************************************************
#                             fdoor_cout.h
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

__all__ = ["Fdoor_cout"]


from fevendoor import FevenDoor
from returncodes import RET_OK
from sys import stdout

class Fdoor_cout(FevenDoor):

    def __init__(self):
        FevenDoor.__init__(self)    # force constructor

    def __str__(self):
        return "\t"+FevenDoor.__str__(self)+\
                "Fdoor_cout - (null)\n"

    def receive_evenData(self,evenData):
        stdout.write("%s"%evenData.getData("TXT"))
        return RET_OK
