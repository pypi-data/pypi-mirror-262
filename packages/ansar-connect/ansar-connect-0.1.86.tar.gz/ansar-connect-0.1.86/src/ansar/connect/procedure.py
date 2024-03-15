# Author: Scott Woods <scott.18.ansar@gmail.com.com>
# MIT License
#
# Copyright (c) 2022, 2023 Scott Woods
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

""".

.
"""
__docformat__ = 'restructuredtext'

__all__ = [
	'NetworkSettings',
	'AccountSettings',
	'DeveloperSettings',
	'procedure_network',
	'procedure_signup',
	'procedure_login',
	'procedure_account',
	'procedure_developer',
]

import os
import getpass
import ansar.connect as ar
from ansar.encode.args import QUOTED_TYPE, SHIPMENT_WITH_QUOTES, SHIPMENT_WITHOUT_QUOTES
from ansar.create.procedure import DEFAULT_HOME, DEFAULT_GROUP, HOME, GROUP
from ansar.create.procedure import open_home, role_status
from ansar.connect.foh_if import *
from .directory_if import *

DEFAULT_ACCOUNT_ACTION = 'show'

# Per-command arguments as required.
# e.g. command-line parameters specific to create.
class NetworkSettings(object):
	def __init__(self, group_name=None, home_path=None, show_scopes=None, connect_scope=None, connect_file=None):
		self.group_name = group_name
		self.home_path = home_path
		self.show_scopes = show_scopes
		self.connect_scope = connect_scope
		self.connect_file = connect_file

NETWORK_SETTINGS_SCHEMA = {
	'group_name': ar.Unicode(),
	'home_path': ar.Unicode(),
	'show_scopes': ar.Boolean(),
	'connect_scope': ScopeOfService,
	'connect_file': ar.Unicode(),
}

ar.bind(NetworkSettings, object_schema=NETWORK_SETTINGS_SCHEMA)

#
#
def procedure_network(self, network, group, home):
	group = ar.word_argument_2(group, network.group_name, DEFAULT_GROUP, GROUP)
	home = ar.word_argument_2(home, network.home_path, DEFAULT_HOME, HOME)

	if '.' in group:
		e = ar.Rejected(group_name=(group, f'no-dots name'))
		raise ar.Incomplete(e)
	group_role = f'group.{group}'

	hb = open_home(home)

	_, running = role_status(self, hb, [group_role])
	if running:
		e = ar.Failed(group_start=(f'group "{group}" is already running', None))
		raise ar.Incomplete(e)

	settings = []
	if network.connect_scope:	# Assignment of new connection.
		if not network.connect_file:
			e = ar.Rejected(connect_with_no_file=('missing connection details', None))
			raise ar.Incomplete(e)
		s = ScopeOfService.to_name(network.connect_scope)
		p = os.path.abspath(network.connect_file)
		settings.append(f'--connect-scope={s}')
		settings.append(f'--connect-file={p}')

	else:
		settings.append(f'--show-scopes')

	try:
		a = self.create(ar.Process, 'ansar-group',	
					origin=ar.POINT_OF_ORIGIN.RUN_ORIGIN,
					home_path=hb.home_path, role_name=group_role, subrole=False,
					settings=settings)

		# Wait for Ack from new process to verify that
		# framework is operational.
		m = self.select(ar.Completed, ar.Stop)
		if isinstance(m, ar.Stop):
			# Honor the slim chance of a control-c before
			# the framework can respond.
			self.send(m, a)
			m = self.select(ar.Completed)

		# Process.
		def lfa_text(lfa):
			s = f'{lfa[0]}/{lfa[1]}/{lfa[2]}'
			return s

		value = m.value
		if isinstance(value, ar.Ack):	   # New instance established itself.
			pass
		elif isinstance(value, DirectoryAncestry):
			for d in reversed(value.lineage):
				scope = ScopeOfService.to_name(d.scope) if d.scope else '?'
				ipp = str(d.connecting_ipp) if d.connecting_ipp.host else 'DISABLED'
				method = d.method if d.connecting_ipp.host else '-'
				started = ar.world_to_text(d.started) if d.started else '-'
				connected = ar.world_to_text(d.connected) if d.connected else '-'
				sc = f'{started}'
				lfa = lfa_text(d.lfa)
				ar.output_line(f'{scope:6} {ipp:20} {method:26} {sc:26} {lfa}')
		elif isinstance(value, DirectoryReconnect):
			return value
		elif isinstance(value, ar.Faulted):
			raise ar.Incomplete(value)
		elif isinstance(value, ar.LockedOut):
			e = ar.Failed(role_lock=(None, f'"{group_role}" already running as <{value.pid}>'))
			raise ar.Incomplete(e)
		else:
			e = ar.Failed(role_execute=(value, f'unexpected response from "{group_role}" (ansar-group)'))
			raise ar.Incomplete(e)
	finally:
		pass

	return None

# Keyboard input.
# Form/field filling.
def fill_field(name, t):
	if name == 'password':
		d = getpass.getpass(f'Password: ')
		return d

	ip = name.capitalize()
	ip = ip.replace('_', ' ')
	kb = input(f'{ip}: ')

	if isinstance(t, QUOTED_TYPE):
		sh = SHIPMENT_WITH_QUOTES % (kb,)
	else:
		sh = SHIPMENT_WITHOUT_QUOTES % (kb,)
	try:
		encoding = ar.CodecJson()
		d, _ = encoding.decode(sh, t)
	except ar.CodecFailed as e:
		f = ar.Faulted(f'cannot accept input for "{ip}"', str(e))
		raise ar.Incomplete(f)
	return d

def fill_form(self, form):
	schema = form.__art__.value
	for k, v in schema.items():
		d = fill_field(k, v)
		setattr(form, k, d)

#
#
class AccountSettings(object):
	def __init__(self, read=False, update=False, delete=False,
			add_developer=False, add_directory=False,
			update_developer=False, update_directory=False,
			delete_developer=False, delete_directory=False):
		self.read = read
		self.update = update
		self.delete = delete
		self.add_developer = add_developer
		self.add_directory = add_directory
		self.update_developer = update_developer
		self.update_directory = update_directory
		self.delete_developer = delete_developer
		self.delete_directory = delete_directory

ACCOUNT_SETTINGS_SCHEMA = {
	'read': ar.Boolean(),
	'update': ar.Boolean(),
	'delete': ar.Boolean(),
	'add_developer': ar.Boolean(),
	'add_directory': ar.Boolean(),
	'update_developer': ar.Boolean(),
	'update_directory': ar.Boolean(),
	'delete_developer': ar.Boolean(),
	'delete_directory': ar.Boolean(),
}

ar.bind(AccountSettings, object_schema=ACCOUNT_SETTINGS_SCHEMA)

#
#
def procedure_signup(self, account):
	settings = ar.object_custom_settings()
	cloud_ipp = ar.HostPort(settings.cloud_ip, 5022)

	ar.connect(self, cloud_ipp)
	m = self.select(ar.Connected, ar.NotConnected, ar.Stop)
	if isinstance(m, ar.Connected):
		session = self.return_address
	elif isinstance(m, ar.NotConnected):
		return m
	else:
		return ar.Aborted()

	try:
		return account_signup(self, session)	# Create account in cloud, clobber token.
	finally:
		self.send(ar.Close(), session)
		self.select(ar.Closed, ar.Stop)

#
#
def procedure_login(self, account):
	settings = ar.object_custom_settings()
	cloud_ipp = ar.HostPort(settings.cloud_ip, 5022)

	ar.connect(self, cloud_ipp)
	m = self.select(ar.Connected, ar.NotConnected, ar.Stop)
	if isinstance(m, ar.Connected):
		session = self.return_address
	elif isinstance(m, ar.NotConnected):
		return m
	else:
		return ar.Aborted()

	try:
		return account_login(self, session)		# Creds for existing account, update token.
	finally:
		self.send(ar.Close(), session)
		self.select(ar.Closed, ar.Stop)

#
#
def procedure_account(self, account):
	settings = ar.object_custom_settings()
	login_token = settings.login_token
	cloud_ipp = ar.HostPort(settings.cloud_ip, 5022)

	if login_token is None:
		if not account.signup and not account.login:
			f = ar.Faulted('not logged in', 'need to signup or login')
			return f

	ar.connect(self, cloud_ipp)
	m = self.select(ar.Connected, ar.NotConnected, ar.Stop)
	if isinstance(m, ar.Connected):
		session = self.return_address
	elif isinstance(m, ar.NotConnected):
		return m
	else:
		return ar.Aborted()

	try:
		self.send(OpenToken(login_token), session)
		m = self.select(TokenOpened, ar.Nak, ar.Faulted, ar.Abandoned, ar.Stop)
		if isinstance(m, ar.TokenOpened):
			pass
		elif isinstance(m, ar.Nak):
			f = ar.Faulted('not logged in', 'login expired? other change?')
			return f
		elif isinstance(m, ar.Faulted):
			return m
		elif isinstance(m, ar.Abandoned):
			f = ar.Faulted('remote abandoned connection', 'try later?')
			return f
		else:
			return ar.Aborted()

		if account.update:
			return account_update(self, m, session)
		elif account.delete:
			return account_delete(self, m, session)
		elif account.add_developer:
			return account_add_developer(self, m, session)
		elif account.add_directory:
			return account_add_directory(self, m, session)
		elif account.update_developer:
			return account_update_developer(self, m, session)
		elif account.update_directory:
			return account_update_directory(self, m, session)
		elif account.delete_developer:
			return account_delete_developer(self, m, session)
		elif account.delete_directory:
			return account_delete_directory(self, m, session)

		return account_read(self, m, session)
	finally:
		self.send(ar.Close(), session)
		self.select(ar.Closed, ar.Stop)

def account_signup(self, session):
	signup = AccountSignup()
	fill_form(self, signup)
	self.send(signup, session)
	m = self.select(TokenOpened, ar.Faulted, ar.Abandoned, ar.Stop)
	if isinstance(m, TokenOpened):
		pass
	elif isinstance(m, ar.Faulted):
		return m
	elif isinstance(m, ar.Abandoned):
		f = ar.Faulted('remote abandoned connection', 'try later?')
		return f
	else:
		return ar.Aborted()

	settings = ar.object_custom_settings()
	settings.login_token = m.login_token
	ar.store_settings(settings)
	return None

def account_login(self, session):
	login = AccountLogin()
	fill_form(self, login)
	self.send(login, session)
	m = self.select(TokenOpened, ar.Faulted, ar.Abandoned, ar.Stop)
	if isinstance(m, TokenOpened):
		pass
	elif isinstance(m, ar.Faulted):
		return m
	elif isinstance(m, ar.Abandoned):
		f = ar.Faulted('remote abandoned connection', 'try later?')
		return f
	else:
		return ar.Aborted()

	settings = ar.object_custom_settings()
	settings.login_token = m.login_token
	ar.store_settings(settings)
	return None

def account_read(self, opened, session):
	settings = ar.object_custom_settings()
	rd = AccountRead(login_token=opened.login_token, login_id=opened.login_id)
	self.send(rd, session)
	m = self.select(AccountPage, ar.Faulted, ar.Abandoned, ar.Stop)
	if isinstance(m, AccountPage):
		return m
	elif isinstance(m, ar.Faulted):
		return m
	elif isinstance(m, ar.Abandoned):
		f = ar.Faulted('remote abandoned connection', 'try later?')
		return f
	else:
		return ar.Aborted()

	# Print.
	return None

def account_update(self, opened, session):
	pass

def account_delete(self, opened, session):
	pass

def account_add_developer(self, opened, session):
	pass

def account_add_directory(self, opened, session):
	pass

def account_update_developer(self, opened, session):
	pass

def account_update_directory(self, opened, session):
	pass

def account_delete_developer(self, opened, session):
	pass

def account_delete_directory(self, opened, session):
	pass


#
#
class DeveloperSettings(object):
	def __init__(self, login=False, read=False, update=False):
		self.login = login
		self.read = read
		self.update = update

DEVELOPER_SETTINGS_SCHEMA = {
	'login': ar.Boolean(),
	'read': ar.Boolean(),
	'update': ar.Boolean(),
}

ar.bind(DeveloperSettings, object_schema=DEVELOPER_SETTINGS_SCHEMA)

#
#
def procedure_developer(self, developer):
	settings = ar.object_custom_settings()
	login_token = settings.login_token
	cloud_ipp = ar.HostPort(settings.cloud_ip, 5022)

	if login_token is None:
		f = ar.Faulted('not logged in', 'need to signup or login')
		return f

	ar.connect(self, cloud_ipp)
	m = self.select(ar.Connected, ar.NotConnected, ar.Stop)
	if isinstance(m, ar.Connected):
		session = self.return_address
	elif isinstance(m, ar.NotConnected):
		return m
	else:
		return ar.Aborted()

	try:
		self.send(OpenToken(login_token), session)
		m = self.select(ar.Ack, ar.Nak, ar.Stop)
		if isinstance(m, ar.Ack):
			pass
		elif isinstance(m, ar.Nak):
			f = ar.Faulted('not logged in', 'login expired? other change?')
			return f
		else:
			return ar.Aborted()

		if developer.add:
			return developer_add(self, session)

		return None
	finally:
		self.send(ar.Close(), session)
		self.select(ar.Closed, ar.Stop)

def developer_add(self, session):
	add = DeveloperAdd()
	self.send(add, session)
	m = self.select(ar.Ack, ar.Faulted, ar.Stop)
	if isinstance(m, ar.Ack):
		pass
	elif isinstance(m, ar.Faulted):
		return m
	else:
		return ar.Aborted()

	return None
