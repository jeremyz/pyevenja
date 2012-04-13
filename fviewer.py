#/***************************************************************************
#                             fviewer.h
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

"""/** Debugger class.
  function : receive information about :
    - Configuration of a port (evenDoor or evenBoard)
    - Data waiting inside the port (evenDoor or evenBoard)

  description : This class cannot be different inside the same room,
                because all ports (evenDoor and evenBoard)
                need to be able to
                access the head information :
                - source
                - destination
                and access the data information.
                WITHOUT HAVING TO DO A VERSIONNING.

  *@author Fabian Padilla
  */"""

__all__ = ["Fviewer"]

from fport import Fport
from fevendata import FevenData

class Fviewer(Fport):
    """This class is form debugging purpose """
    def __init__(self):
        Fport.__init__(self)        # force constructor

    def __str__(self):
        return "\t"+Fport.__str__(self)+\
                "Fviewer - (null)\n"
