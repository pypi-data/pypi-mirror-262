# Author: Scott Woods <scott.18.ansar@gmail.com.com>
# MIT License
#
# Copyright (c) 2017-2023 Scott Woods
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

import ansar.create as ar
from .socketry import *

__all__ = [
	'CONTACT_TYPE',
	'CONTACT_DEVICE',
	'EmailAddress',
	'PhoneNumber',
	'CloudLogin',
	'CloudAccount',
	'CloudDirectory',
	'CloudDirectoryAccess',
	'CloudAccess',
	'CloudLookup',
	'CloudRedirect',
	'CloudAssignment',
	'YourCloud',
	'RelayLookup',
	'RelayRedirect',
	'RelayAssignment',
	'YourRelay',
	'CloseRelay',
]

# Contact details.
CONTACT_TYPE = ar.Enumeration(PERSONAL=0, BUSINESS=1, HOME=2, OTHER=3)
CONTACT_DEVICE = ar.Enumeration(MOBILE=0, FIXED_LINE=1)

class EmailAddress(object):
	def __init__(self, email_type=None, email_address=None):
		self.email_type = email_type
		self.email_address = email_address

class PhoneNumber(object):
	def __init__(self, phone_type=None, phone_device=None, phone_number=None):
		self.phone_type = phone_type
		self.phone_device = phone_device
		self.phone_number = phone_number

# Cloud tables.
# Access to the cloud service.
class CloudLogin(object):
	def __init__(self, login_id=None, login_email=None, password=None,
			account_id=None, assigned_directory=None,
			family_name=None, given_name=None, nick_name=None, honorific=None):
		self.login_id = login_id
		self.login_email = login_email		# Unique key.
		self.password = password			# Creds.
		self.account_id = account_id		# Belong to this account.
		self.assigned_directory = assigned_directory or ar.default_set()	# Assigned use of.
		self.family_name = family_name
		self.given_name = given_name
		self.nick_name = nick_name
		self.honorific = honorific

# An account in the cloud.
# An organization with developers and directories.
class CloudAccount(object):
	def __init__(self, account_id=None,	login_id=None,
			organization_name=None, organization_location=None, technical_contact=None, financial_contact=None, administrative_contact=None,
			control_rules=None):
		self.account_id = account_id				# Unique key.
		self.login_id = login_id					# Owner of this account.
		self.organization_name = organization_name
		self.organization_location = organization_location
		self.technical_contact = technical_contact or ar.default_vector()
		self.financial_contact = financial_contact or ar.default_vector()
		self.administrative_contact = administrative_contact or ar.default_vector()
		# Payment
		# Invoices
		self.control_rules = control_rules or ar.default_map()

# A top-level directory providing global communications.
class CloudDirectory(object):
	def __init__(self, directory_id=None, account_id=None, directory_product=None, directory_instance=None, control_rules=None):
		self.directory_id = directory_id			# Unique key.
		self.account_id = account_id				# Belongs to account.
		self.directory_product = directory_product
		self.directory_instance = directory_instance
		self.control_rules = control_rules or ar.default_map()
		# Number of routes/relays
		# Message rate
		# Bytes rate

# A method of connection to one of the cloud directories.
class CloudDirectoryAccess(object):
	def __init__(self, access_id=None, directory_id=None, login_id=None, access_reason=None, control_rules=None):
		self.access_id = access_id			# Unique key.
		self.directory_id = directory_id	# Access to which directory.
		self.login_id = login_id			# Login that created this access.
		self.access_reason = access_reason
		self.control_rules = control_rules or ar.default_map()
		# Expiry
		# Number of concurrent accesses
		# Number of total accesses.

#
#
CLOUD_SCHEMA = {
	"password": ar.Unicode(),
	"assigned_directory": ar.SetOf(ar.UUID()),
	"family_name": ar.Unicode(),
	"given_name": ar.Unicode(),
	"nick_name": ar.Unicode(),
	"honorific": ar.Unicode(),
	"email_type": CONTACT_TYPE,
	"email_address": ar.Unicode(),
	"phone_type": CONTACT_TYPE,
	"phone_device": CONTACT_DEVICE,
	"phone_number": ar.Unicode(),
	"login_id": ar.UUID(),
	"login_email": ar.Unicode(),
	"organization_name": ar.Unicode(),
	"organization_location": ar.Unicode(),
	"technical_contact": ar.VectorOf(ar.Any()),
	"financial_contact": ar.VectorOf(ar.Any()),
	"administrative_contact": ar.VectorOf(ar.Any()),
	"account_id": ar.UUID(),
	"directory_product": ar.Unicode(),
	"directory_instance": ar.Unicode(),
	"access_id": ar.UUID(),
	"directory_id": ar.UUID(),
	"created_id": ar.UUID(),
	"access_reason": ar.Unicode(),
	"control_rules": ar.MapOf(ar.Unicode(), ar.Any()),
}

ar.bind(EmailAddress, object_schema=CLOUD_SCHEMA)
ar.bind(PhoneNumber, object_schema=CLOUD_SCHEMA)
ar.bind(CloudLogin, object_schema=CLOUD_SCHEMA)
ar.bind(CloudAccount, object_schema=CLOUD_SCHEMA)
ar.bind(CloudDirectory, object_schema=CLOUD_SCHEMA)
ar.bind(CloudDirectoryAccess, object_schema=CLOUD_SCHEMA)

# Protocol between a connecting directory and
# a cloud directory.
class CloudAccess(object):
	def __init__(self, access_ipp=None, account_id=None, directory_id=None):
		self.access_ipp = access_ipp or HostPort()
		self.account_id = account_id
		self.directory_id = directory_id

class CloudLookup(object):
	def __init__(self, account_id=None, directory_id=None):
		self.account_id = account_id
		self.directory_id = directory_id

class CloudRedirect(object):
	def __init__(self, redirect_ipp=None, directory_id=None, assignment_token=None):
		self.redirect_ipp = redirect_ipp or HostPort()
		self.directory_id = directory_id
		self.assignment_token = assignment_token

class CloudAssignment(object):
	def __init__(self, directory_id=None, assignment_token=None):
		self.directory_id = directory_id
		self.assignment_token = assignment_token

class YourCloud(object):
	def __init__(self, address=None):
		self.address = address

DIRECTORY_SCHEMA = {
	"access_ipp": ar.UserDefined(HostPort),
	"account_id": ar.UUID(),
	"directory_id": ar.UUID(),
	"redirect_ipp": ar.UserDefined(HostPort),
	"assignment_token": ar.UUID(),
	"address": ar.Address(),
}

ar.bind(CloudAccess, object_schema=DIRECTORY_SCHEMA)
ar.bind(CloudLookup, object_schema=DIRECTORY_SCHEMA)
ar.bind(CloudRedirect, object_schema=DIRECTORY_SCHEMA)
ar.bind(CloudAssignment, object_schema=DIRECTORY_SCHEMA)
ar.bind(YourCloud, object_schema=DIRECTORY_SCHEMA)

# Protocol between a routing/looping subscriber and
# a publisher.
class RelayLookup(object):
	def __init__(self, relay_id=None, directory_id=None):
		self.relay_id = relay_id
		self.directory_id = directory_id

class RelayRedirect(object):
	def __init__(self, redirect_ipp=None, relay_id=None, assignment_token=None):
		self.redirect_ipp = redirect_ipp or HostPort()
		self.relay_id = relay_id
		self.assignment_token = assignment_token

class RelayAssignment(object):
	def __init__(self, relay_id=None, assignment_token=None):
		self.relay_id = relay_id
		self.assignment_token = assignment_token

class YourRelay(object):
	def __init__(self, address=None):
		self.address = address

class CloseRelay(object):
	def __init__(self, redirect=None):
		self.redirect = redirect or RelayRedirect()

RELAY_SCHEMA = {
	"relay_id": ar.UUID(),
	"directory_id": ar.UUID(),
	"redirect_ipp": ar.UserDefined(HostPort),
	"assignment_token": ar.UUID(),
	"address": ar.Address(),
	"account_id": ar.UUID(),
}

ar.bind(RelayLookup, object_schema=RELAY_SCHEMA)
ar.bind(RelayRedirect, object_schema=RELAY_SCHEMA)
ar.bind(RelayAssignment, object_schema=RELAY_SCHEMA)
ar.bind(YourRelay, object_schema=RELAY_SCHEMA)

#
#
class CloseRelay(object):
	def __init__(self, redirect=None):
		self.redirect = redirect or RelayRedirect()

CLOSE_SCHEMA = {
	"redirect": ar.UserDefined(RelayRedirect),
}

ar.bind(CloseRelay, object_schema=CLOSE_SCHEMA)
