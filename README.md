# RPiParticle ![build status](https://api.travis-ci.org/FriskByBergen/RPiParticle.svg?branch=master "TravisCI Build Status")

## Overview

This is a small code to sample dust readings from a SDS011 sensor and
post the measurements to a webserver. The executable script will
regularly query the webserver for updates, and if a new version has
been configured the script will invoke git to download a new version
and restart itself.

## Usage

### Installation

1. Install the required dependencies. The friskby_client is heavily
   based on git - and you must have installed that with:

      sudo apt-get install git

   before proceeding with the installation and configuration of the
   friskby client.


2. Log in to the Raspberry PI and download the code with:

     cd /tmp
     
     git clone https://github.com/FriskByBergen/RPiParticle

   Observe that the code downloaded with this git clone command is
   *not* the code which will eventually run on the client, it is
   therefor important that the git clone commands is performed in a
   temporary location in the filesystem.


3. Run the bin/install-deps.sh script, this will install the
   non-standard Python packages reuired by the friskby client. This
   script should only be run once:

     cd RPiParticle/bin

     sudo ./install-deps.sh
   
   The install-deps.sh script will also install the network time client ntpdate.  

4. Before you can proceed with step 4 you must make sure you have an account and can log in on 
   the web-admin: https://friskby.herokuapp.com/admin/. Log in to the web-admin interface and 
   make sure to enter the following information.

   a) Configure your Device in the Devices table.

   b) Configure two sensors attached to your device - these sensor
      must have the name of your device, suffix "_PM10" and "_PM25"
      respectively.

   c) Make sure the "Locked" checkbox on your device is
      *unchecked*. Observe that this will automatically be relocked after
      you have run the bin/initrpi script - so if you run repeatedly you
      must repeat the unlock step.



4. Run the bin/initrpi script:

     cd RPiParticle/bin
     
     sudo ./initrpi

    The initrpi script consist of three different parts:

      a) It will optionally configure WiFi on the Raspberry PI.

      b) It will query the user for a device ID and then query the
         Webserver for configuration of that device ID, download and
         test the code, and install it.

      c) It will install the client code as a systemd service (make
         sure to answer yes on the last question).
 
    It is perfectly OK to run the bin/initrpi script repeatedly.
     

### Manual restart

It should not be necessary to manually restart the friskby client, but
if things go wrong for some reason, log in to the raspberry pi and
follow these steps:

1. Stop the current client with: "sudo systemctl stop friskby"

2. Make sure the device is unlocked and has the correct client version
   on the webserver.

3. Essentially repeat the installation procedure.





