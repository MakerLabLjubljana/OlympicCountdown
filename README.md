# Olympic Countdown sculpture project

Olympic Countdown clock project aims towards creating a countdown display for the sculpture positioned in one of the largest shopping centreContribution in Slovenia. The timer will countdown to next Olympic Games and stand there as a reminder for all sport enthusiasts.   Contribution to visual appeal LED lights were put on the side of the sculpture.

This project was proposed by OKS (Olympic Committee Slovenia) to improve awareness that olympic games are coming. By putting a countdown timer as a heart of the sculpture Slovenia joined the global trend of establishing countdown sculptures in Main cities of many countries.

The sculpture also has an option to display different content as oppose to the clock. The ability to present moderated content from twitter and Facebook, there is also an option to present results for national accomplishments during the olympic games.


## Hardware

#### martix display

Panels used are used to make video walls on time square for example. Panels measure 16 by 32 pixels and can be chained together to create a video wall. They have bright LEDs aligned to the grid can display RGB colours. 12 digital pins drive the whole chain of displays (6 bit data and 6 bit control) using 5V up to 2A of power.

Panels are chained together to form a module with 2x3 panels on both sides. Wooden frame of the module also contains separate power supplies and separate RPIs to drive the displays. 
Display panels are connected in series with flat cables to Raspberry PI’s GPIO connector. Both panel sides have separate Raspberry driving it.

![Image of panel connections](https://rawgithub.com/MakerLabLjubljana/OlympicCountdown/master/Drawings/Matrix_panel_connections.svg =260x)  


Instructions on connecting RPI to the modules can be found on the instructions page of the library for displaying content. https://github.com/hzeller/rpi-rgb-led-matrix
For this project we chained all panels in series, and with that we also had to adjust the drivers to display the content correctly.

#### Side LED color bezel

We used Adafruit’s NeoPixel Digital RGB LED Strip - white to display the official olympic colours on side of the sculpture. Using ready to go Library to run the pixels, we started with one of the examples and changed it, so it displays the official Olympic colours (Red, Green, Blue, Yellow and Black). The Black colour can not be displayed, so we turned off all the piles from the strip at that sequence. 

Data connections are connected in parallel, because we solved synchronisation problem and saved some space in the module using only one arduino to tun the LEDs. Connecting ground pin to Arduino enables that the data voltage has a reference point.
Using a separate 150W power supply we protected Arduino from power spikes that may happen.

![NeoPixel lights connections](https://rawgithub.com/MakerLabLjubljana/OlympicCountdown/master/Drawings/NeoPixel_connections.svg  =200x)

Connecting the LED strip we followed the tutorial: 
https://learn.adafruit.com/adafruit-neopixel-uberguide/power

#### Weather protection

orong the system against weather influences is important, because it has to operate in all weather conditions for a long time period. Electrical devices don’t work in moist atmosphere, therefore a Acrylic mask was put over the module. And additional Moisture sensor was put into the sculpture to measure and notify us when the conditions get critical.

#### Power Supply

We installed 3x 150W power supply. There is some overhead capacity concerning power, but regarding that there will be upgrades this additional power will be useful. Animations that produce a lot of energy spikes can cause misbehaviour on power supplies. If there isn’t any overhead these spikes can damage the power supply and cause it to fail. Having a separate (4th) power supply to run RPIs and Arduino separates the logic from ‘dirty power’ and enables long term uninterrupted operation.

#### Network Connections

Connecting all devices to the network enabled us to control it remotely from our lab, avoiding loosing time to actually going to the site and program it in the cold winter days.
We used Ethernet cables to connect all devices to the Router inside the sculpture.

![Network connections](https://rawgithub.com/MakerLabLjubljana/OlympicCountdown/master/Drawings/Network_connections.svg  =200x)

## Software

#### Raspberry PI configuration
For this project we used Raspberry PI 2 to run the display. The configuration of RPIs enabled us to implement various functions:

##### SSH access
For enabling SSH connection we have to configure our RPI server first:
'''
sudo raspi-config
'''
navigate to '''ssh''' than Enter
and select Enable or disable ssh server


##### Git Tools

Git tools have to be installed to track all SW changes and update the libraries for the future 
install the tools with:
'''sudo apt-get install git'''

##### Python Configuration

'''
sudo apt-get install python-dev 
sudo pip install twython
mkdir git
cd git
git clone https://github.com/hzeller/rpi-rgb-led-matrix
git clone https://github.com/MakerLabLjubljana/OlympicCountdown
cd rpi-rgb-led-matrix
make 
make build-python
sudo make install-python
'''

##### Matrix display drivers

##### NTP - network time protocol

This program enables updating the time over the network. Every time the program is restarted it updates local time. We decided that refreshing local time should satisfy the need of having accurate time displayed.
Installing ntp can be done with:


##### Crontab

We used Cronjob to restart NTP every 37 minutes

Edit the cron table  using:

'''sudo crontab -e'''
and inserting the command at the end of the document

'''37 * * * * ntpd -gq''

When configuring crontab we used this tutorial: https://www.raspberrypi.org/documentation/linux/usage/cron.md

#### Arduino software

##### NEoPixel driver

LED lights on the side of the sculpture are programmed so the official colours of Olympic Games are displayed. Using smooth transitions from Red Blue Green Yellow and Black were created. All pixels are changing simultaneously with a small delay when a colour is displayed. Using the default library from Adafruit we used examples to greet the world and changed them so the colours were displayed correctly. Using a couple of FOR loops we enabled this function. We followed instructions on this page:  https://github.com/adafruit/Adafruit_NeoPixel

#### Programming Arduino Remotley

Not having enugh time before the oppening we decided to upload a simple program to drive the LED strips. Uploading updates to the code can be done esily through Raspberry using InoTool:
We followed this tutorial when installing this functionality
https://drive.google.com/file/d/0B6kXO9uUbKx2Snh3UEpBN1hLN0E/view?ts=56685186


#### Fonts

Coming close to 7 segment displays meant that we had to create our font. Using bitmap font editor: Fony, we created font adjusted to our matrix display.

#### Simulator

Developing new animations will be something we will do in the future, so we will build a simple simulator to display the pixels before deploying software onto the sculpture. Simulator is a simple Python script which enables the use of the display.

#### Web page

Administrative web page to change the text on the sculpture was also created. Using Javascript to simulate the display and the colours of the sculpture we can enable admins to change the content accordingly. Visitors can also observe the timer and use it to stream the view to public displays.

##### Team

Lab: MakerLab Ljubljana: http://maker.si
Faculty for Electrical engineering Ljubljana Slovenia
*Mentor : Luka Mali

*Martin Cimerman @CimeM
*Janez Cimerman @JanezCim
*Žiga Brinjšek @ZigaB
*Tim Kambrič @tkambic
*Nejc Jurkovič

This project was created with cooperation with Olympic Committee Slovenia (OCS)

