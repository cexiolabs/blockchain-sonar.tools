#!/usr/bin/env python
#
# You may run this script inside docker (if you does not have python locally)
#
# 	docker run --rm --tty --interactive --volume $PWD:/workdir --workdir=/workdir --entrypoint /bin/bash python:3.7
# 	pip install requests
# 	cat addresses.csv | ./address-balance-btc.py
#
# Input CSV format (addresses.csv in above example):
#
# 	<address>[,<user_data_1>,<user_data_1>,<user_data_N>]
#
# Output CSV format:
# 	<address>[,<user_data_1>,<user_data_1>,<user_data_N>],<balance in blockchain>
#

import requests
import sys
from time import sleep
from datetime import datetime, timezone

class CommunicationException(Exception):
	def __init__(self, message):
		self.message = message



for inputLine in sys.stdin:
	inputRow = inputLine.rstrip()
	inputTokens = [x.strip() for x in inputRow.split(',')]
	address = inputTokens[0]

	while True:
		try:
			sleep(0.5)
			# https://sochain.com/api#get-balance
			getAddressBalanceUrl="https://sochain.com//api/v2/get_address_balance/BTC/%s" % (address);
			getAddressBalanceResponse = requests.get(getAddressBalanceUrl)
			if getAddressBalanceResponse.status_code != 200:
				raise CommunicationException("Unexpected response status code: %s" % getAddressBalanceResponse.status_code)
			getAddressBalanceResponseContent = getAddressBalanceResponse.json()
			addressBalanceStr = getAddressBalanceResponseContent['data']['confirmed_balance']


			print("%s,%s" % (inputRow, addressBalanceStr))
			sys.stdout.flush()
			break
		except Exception as ex:
#			raise ex
			print("Attempt failure. {0}".format(ex), file=sys.stderr)
			sleep(5)
