#! /bin/env python

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

"""This is the main entry point for all evenja applications"""

from fstarter import Fstarter

from returncodes import RET_OK
from returncodes import RET_MEMORYSPACE
from returncodes import RET_NOPARAMS

#----------------------------------------------------------------------------

import sys, getopt, os.path, string


shorts = 'hvtc'
longs = ['help','version','trace','compile']
vers = '0.0.9'


#----------------------------------------------------------------------------
def usage(name):
    print 'usage :'+name+' ['+shorts+'] xml_file'
    print ' h - help'
    print ' v - version'
    print ' t - trace\tfstarter.execute() will print all received messages'
    print ' c - compile\tclean and rebuild files'


#----------------------------------------------------------------------------
def version(name):
    print(name+', version '+str(vers))
    print 'written by jeremy zurcher tzurtch@bluemail.ch'
    print 'stolen from evenja-2.9.72-beta1, written by Fabian Padilla fp@bridgethink.com'
    print '''\nthis version should be ok, but isn't written in "pure" python style ;))'''
    print 'the work is in progress ...'


#----------------------------------------------------------------------------
def main():
    path,name=os.path.split(sys.argv[0])
    trace = False
    try:
        opts,args = getopt.getopt(sys.argv[1:],shorts,longs)
    except getopt.GetoptError:
        print('try '+name+' --help')
        sys.exit(0)

    for opt,arg in opts:
        if opt in ('-'+shorts[0],'--'+longs[0]):
            usage(name)
            sys.exit(0)
        if opt in ('-'+shorts[1],'--'+longs[1]):
            version(name)
            sys.exit(0)
        if opt in ('-'+shorts[2],'--'+longs[2]):
            trace = True
        if opt in ('-'+shorts[3],'--'+longs[3]):
            L=[    'OSconfig.py',\
                'OSlinux.py',\
                'evenjastrings.py',\
                'fconfig.py',\
                'fdoor_cout.py',\
                'fdoor_file.py',\
                'fevendoor.py',\
                'fevenboard.py',\
                'fevendata.py',\
                'fevenprg.py',\
                'flist.py',\
                'flisthash.py',\
                'fport.py',\
                'fportbkpevendata.py',\
                'fportlist.py',\
                'fportlisthash.py',\
                'fposition.py',\
                'fprg_concat.py',\
                'frouter.py',\
                'fstarter.py',\
                'fstringhash.py',\
                'fviewer.py',\
                'globalvars.py',\
                'returncodes.py']
            if sys.platform != 'linux2':
                print "Would you please install an acceptable OS, thanks."
            os.system('rm *.pyc *.pyo 2>/dev/null')
            for I in L:
                print 'python -O -W all '+I
                os.system('python -O -W all '+I)
            sys.exit(0)

    if not args:
        usage(name)
        sys.exit(1)

    # here we go ... with this buggy verion ...

    starter = Fstarter()

    if starter:
        ret = starter.start(args[0])
        if ret == RET_OK:
            starter.execute(trace)    # launch the stuff
            ret = starter.end()     # for dynamc configuration
        else:
            print "can't start the starter *sigh*"
            sys.exit(-1)
    else:
        print "can't instanciate the starter ... really bad !!!!"
        sys.exit(-1)
    sys.exit(0)


#----------------------------------------------------------------------------
if __name__=='__main__':
    main()

