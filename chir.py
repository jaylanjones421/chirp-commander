# -*- coding: utf-8 -*-
#!/bin/sh
# ------------------------------------------------------------------------
#
#  This file is part of the Chirp Connect Python SDK.
#  For full information on usage and licensing, see https://chirp.io/
#
#  Copyright (c) 2011-2018, Asio Ltd.
#  All rights reserved.≈
#
# ------------------------------------------------------------------------
import argparse
import sys
import serial
import time
import os
# Importing kwikset controller
import kwikset
# Importing chirp 
from chirpsdk import ChirpConnect, CallbackSet, CHIRP_CONNECT_STATE
# Importing GPIO library
import RPi.GPIO as GPIO
# Importing time library for delay
import time
# DB related imports
import psycopg2
from config import config
# Importing web browsing modules
import webbrowser
import subprocess
import wave

# Defining THE unlock function
def unlock(hexData):
    strHexData=str(hexData)
    data = ""
    index = 0
    for i in strHexData:
        if(index%2 != 0):
            data += i
        index+=1
    timenow = time.asctime(time.localtime(time.time()))
    
    cur.execute("""SELECT * FROM users WHERE id=%s;""",[data])
    res = cur.fetchone()
    kwikset.unlock()
    cur.execute("""INSERT INTO entrances (user_id, time) VALUES (%s,%s);""",[data,timenow])
    print(" Welcome to Parkhub, " + res[1])
    wave.open('mlg-airhorn.wav')

class Callbacks(CallbackSet):

    def on_state_changed(self, previous_state, current_state):
        """ Called when the SDK's state has changed """
        print("State changed from {} to {}".format(
            CHIRP_CONNECT_STATE.get(previous_state),
            CHIRP_CONNECT_STATE.get(current_state)))

    def on_sending(self, payload, channel):
        """ Called when a chirp has started to be transmitted """
        print('Sending: ' + str(list(payload)))

    def on_sent(self, payload, channel):
        """ Called when the entire chirp has been sent """
        print('Sent data')
        print(list(payload))

    def on_receiving(self, channel):
        """ Called when a chirp frontdoor is detected """
        print('Receiving data')

    def on_received(self, payload, channel):
        """ Called when an entire chirp has been received.
        Note: A length of 0 indicates a failed decode.
        """
        if payload is None:
            print('Decode failed!')
        else:
	    # Printing time of unlock && unlock
            unlock(payload)

# Setting chirp.io dev variables
app_key = 'D10bF898f8C1eE22Ac4A7E3Dd'
app_secret = 'E4E90B62DC6fa5980c1b99b097B6EBbB6ddfe5CEb3BBe2CA3c'
app_config = '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'

# Setting up GPIO pins
kwikset.setup_serial()

# Read connection parameters for DB
params = config()

# Initialise ConnectSDK
sdk = ChirpConnect(app_key, app_secret, app_config)
print(str(sdk))

# Show audio channels
print(sdk.audio.query_devices())

# Configuring audio
sdk.audio.input_device = 2
sdk.audio.output_device = 0
sdk.audio.output_channels = 2
sdk.audio.sample_size = 'float32'
sdk.sample_rate = 48000

# Set callback functions
sdk.set_callbacks(Callbacks())

# Starting SDK
sdk.start(send=True, receive=True)

# connect to the PostgreSQL server
print('Connecting to the PostgreSQL database...')
conn = psycopg2.connect(**params)
conn.set_session(autocommit=True)

# create a cursor
cur = conn.cursor()


try:
    # Process audio streams
    while True:
        time.sleep(0.1)
        sys.stdout.write('.')
        sys.stdout.flush()
except KeyboardInterrupt:
    print('Exiting')

# Exit chirp.io SDK
sdk.stop()
sdk.close()