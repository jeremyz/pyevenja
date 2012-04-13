#/***************************************************************************
#                             fport.h
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

"""/**Origin class for all part of the software that receive data in evenja concept.

  function: Abstract class for ALL ports : FevenPrg, FevenDoor, FevenBoard, Frouter.

  description : Implement only the behavior with the viewer.

  ***********
  IMPORTANT :
  ***********
  In the method receive_evenData each inherited class need to call the parent
  method first , with : Fport::receive_evenData( evenData);

  *@author Fabian Padilla
  */"""

__all__ =["Fport"]
  
from flist import Flist
from fconfig import Fconfig
from fevendata import FevenData
from flisthash import FlistHash
from returncodes import RET_OK
from returncodes import RET_NOTIMPLEMENTED
from evenjastrings import XML_NAME


class Fport(Fconfig):
	"""This is the abstract class for all kind of port.
	It manages viewer and got some generic and high level data manipulation methods"""
	
	# class attribute
	listMsg = Flist()		#/** List of all waiting envenData to be send to a port */
	listMsgSys = Flist()	#/** List of all wainting envenData with system datas to be send to a port */
	
	def __init__(self):
		Fconfig.__init__(self)		# force constructor
		self.parent = None		#/** Router this port is connected to and receives from */
		self.viewer = None		#/** Enable to view the datas inside the port (evenDoor or evenBoard). */
		self.freeEvenData = FlistHash()	#/** List of Free and Available evenDatas (faster than new and delete ;) */

	def __str__(self):
		return "\t"+Fconfig.__str__(self)+\
				" Fport - parent : "+str(self.parent)+\
				" - Viewer : "+str(self.viewer)+\
				" - freeEvenData : "+str(self.freeEvenData.getCount())+"\n"
	
	def start(self,port,config):
		"""/** Starts import the config file ( or other stream), and sets the parent
		router. If the port (evenDoor and evenBoard) need to send an evenData. */"""
		self.parent = port
		return self.startXml(config)	# TzurTcH ??
		#if ret == RET_OK:		# we found the <evenja_name> tag and get it's content
		#	self.pushCurrent()	# so why look for it another time and expect not to find it ???
		#	self.gotoChildren()
		#	ret = self.Find(XML_NAME,False)
		#	if ret != RET_OK:
		#		self.setString(self.getContent())
		#	self.popCurrent()
		#return ret
	
	def receive_evenData(self,evenData):
		"""/** Work in all ports => router, evenPrg, evenDoor or evenBoard are only
		done inside this overload method.
		If it is a evenDoor the surcharged method will receive an evenData
		that needs to be exported from the room to the external format of the evenDoor.
		If it is a evenBoard the surcharged method will receive an evenData
		and modify or wait for another evenData. */"""
		print "This method MUST be overriden !!"
		from sys import exit
		exit(1)
	
	def end(self):
		"""/** To force futur developer to implement the right behavior for evenDoor and evenBoard */"""
		return self.endXml()
	
	def setViewer(self,viewer):
		"""/** Set the debug viewer. Where all incoming evenDatas are displayed with the config of the port. */"""
		self.viewer = viewer
		#return RET_OK								# TzurTcH - no need
	
	def justDoIt(self,evenData):
		"""/** Methods called by Fstarter */"""
		ret = RET_OK
		if self.viewer:
			ret = self.viewer.receive_evenData(evenData)
		if ret == RET_OK:
			ret = self.receive_evenData(evenData)
		return ret
	
	def justDoItSys(self,evenData):
		"""/** Methods called by Fstarter */"""
		self.setFreeEvenData(evenData)
		#return RET_OK								# TzurTcH - ne need
	
	def sendEvenData(self,evenData,portDestination = None):
		"""/** Methods to enable all ports to sends evenDatas to a port */"""
		if portDestination:
			evenData.setActivePort(portDestination)
		elif self.parent:
			evenData.setActivePort(self.parent)
		else:
			evenData.setActivePort(self)
		self.listMsg.add(evenData)
	
	def sendEvenDataSys(self,evenData,portDestination = None):
		"""/** Methods to enable all ports to sends evenDatas to a port */"""
		if portDestination:
			evenData.setActivePort(portDestination)
		elif self.parent:
			evenData.setActivePort(self.parent)
		else:
			evenData.setActivePort(self)
		self.listMsgSys.add(evenData)
	
	
	def setFreeEvenData(self, evenData):
		"""/** set an evenData free */"""
		self.freeEvenData.add(evenData)
	
	def getFreeEvenData(self):
		"""/** Get an evenData free */"""
		if self.freeEvenData.getCount():
			data = self.freeEvenData.remove(0)
		else:
			data = FevenData()
		data.reset()
		return data

	def evendoor_condition(self,evenData,port):
		"""/** USED BY THE EVENDOOR LIBRARY. FUTUR IMPLEMENTATION. */"""
		return RET_NOTIMPLEMENTED

