# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: t -*-
# vi: set ft=python sts=4 ts=4 sw=4 noet :

# This file is part of Fail2Ban.
#
# Fail2Ban is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Fail2Ban is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Fail2Ban; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

# Fail2Ban developers

__copyright__ = "Copyright (c) 2012 Yaroslav Halchenko"
__license__ = "GPL"

from threading import Lock

from ..server.jail import Jail
from ..server.actions import Actions


class DummyActions(Actions):
	def checkBan(self):
		return self._Actions__checkBan()


class DummyJail(Jail):
	"""A simple 'jail' to suck in all the tickets generated by Filter's
	"""
	def __init__(self, name='DummyJail', backend=None):
		self.lock = Lock()
		self.queue = []
		super(DummyJail, self).__init__(name=name, backend=backend)
		self.__actions = DummyActions(self)

	def __len__(self):
		with self.lock:
			return len(self.queue)

	def isEmpty(self):
		with self.lock:
			return not self.queue

	def isFilled(self):
		with self.lock:
			return bool(self.queue)

	def putFailTicket(self, ticket):
		with self.lock:
			self.queue.append(ticket)

	def getFailTicket(self):
		with self.lock:
			try:
				return self.queue.pop()
			except IndexError:
				return False

	@property
	def idle(self):
		return False;
	
	@idle.setter
	def idle(self, value):
		pass

	@property
	def actions(self):
		return self.__actions;

	def isAlive(self):
		return True;
