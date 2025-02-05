# Copyright (c) 2025, Sarvadhi and Contributors
# See license.txt

# import frappe
from frappe.tests import IntegrationTestCase, UnitTestCase


# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]


class UnitTestBooking_History(UnitTestCase):
	"""
	Unit tests for Booking_History.
	Use this class for testing individual functions and methods.
	"""

	pass


class IntegrationTestBooking_History(IntegrationTestCase):
	"""
	Integration tests for Booking_History.
	Use this class for testing interactions between multiple components.
	"""

	pass
