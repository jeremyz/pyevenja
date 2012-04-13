#/***************************************************************************
#                             OSlinux.h
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

""" OS specifications """

__all__ = ["MAX_TREELEVEL","START_ELEMENTS","INC_ELEMENTS"]


MAX_TREELEVEL         = 8    # not used yet

# only used in flisthash.py tests
START_ELEMENTS          = 100   #/* Start with a list of 100 elements */
INC_ELEMENTS            = 50    #/* If list is full increment the size of 50 elements */
