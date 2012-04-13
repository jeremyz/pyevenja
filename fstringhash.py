#/***************************************************************************
#                             fstringhash.h
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

# TODO method equals should be __eq__ for the beauty ...
# TODO  do we really need this, as python allready provides it's hash value technology in PyObject [ obj.__hash__() ]
#
#    ob_sval == char*
#    ob_size == strlen()
#
# int
# _PyString_Eq(PyObject *o1, PyObject *o2)
# {
#    PyStringObject *a, *b;
#    a = (PyStringObject*)o1;
#    b = (PyStringObject*)o2;
#        return a->ob_size == b->ob_size
#          && *a->ob_sval == *b->ob_sval
#          && memcmp(a->ob_sval, b->ob_sval, a->ob_size) == 0;
# }
#
# static long
# string_hash(PyStringObject *a)
# {
#       register int len;
#    register unsigned char *p;
#    register long x;
#
#    if (a->ob_shash != -1)
#        return a->ob_shash;
#    len = a->ob_size;
#    p = (unsigned char *) a->ob_sval;
#    x = *p << 7;
#    while (--len >= 0)
#        x = (1000003*x) ^ *p++;
#    x ^= a->ob_size;
#    if (x == -1)
#        x = -2;
#    a->ob_shash = x;
#    return x;
# }




"""/** To speed up the process of comparaison between values, we use a hash technology.
  function : hash a string and show hashvalue and string.

  description : the method "setString" is used to set the the value of the stringhash.
          Then  the hash value is available.
        This will speedup the comparaison between the different "string" in evenja rooms.
        ( it is faster to compare two int than  complete string).

  *@author Fabian Padilla
  */"""

__all__ =["FstringHash"]

try:
    import hashlib
except:
    print "no MD5 capabilities ... aborting"
    import sys
    sys.exit(1)


class FstringHash:
    """This class is wrapper around the python builtin string providing an extra (virtual) hash function"""
    def __init__(self):
        self.string = None
        self.hashValue = None

    def __str__(self):
        return "FstringHash : "+str(self.string)+"\n"

    def __hash(self):
        """ default hash function, may be overriden """
        return hashlib.md5(self.string).hexdigest()

    def setString(self,string):
        self.string = string
        if string is None:
            self.hashValue = None
        else:
            self.hashValue = self.__hash()

    def getString(self):
        return self.string

    def getHashValue(self):
        return self.hashValue

    def copyFrom(self,other):
        """copy my attributes from other"""
        self.string = other.string
        self.hashValue = other.hashValue

    #def __eq__(self,other):
    def equals(self,other):
        return self.string == other.string and self.hashValue == other.hashValue


if __name__ == '__main__':

    import unittest

    str1 = FstringHash()
    str2 = FstringHash()

    class FstringHashTestCase(unittest.TestCase):

        def test1Equal(self):
            str1.setString("WWW.TEST.ORG")
            str2.setString("WWW.TEST.ORG")
            self.assertEquals(str1.equals(str2),1)

        def test2NotEqual(self):
            str1.setString("WWW.TEST.ORG")
            str2.setString("WWW.NOTEST.ORG")
            self.assertEquals(str1.equals(str2),0)

        def test3Copy(self):
            str1.setString("WWW.TEST.ORG")
            str2.copyFrom(str1)
            self.assertEquals(str1.equals(str2),1)

        def test4Hash(self):
            str1.setString("WWW.TEST.ORG")
            self.assertEquals(hashlib.md5("WWW.TEST.ORG").hexdigest(),str1.getHashValue())

        def test5None(self):
            str1.setString("WWW.TEST.ORG")
            str1.setString(None)
            self.assertEquals(str1.getHashValue(),None)
            self.assertEquals(str1.getString(),None)



    unittest.main()
