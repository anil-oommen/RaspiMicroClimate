import lirc

'''
GPIO Infra Red Reciever ,  tsop38238
Module to read and understand the different IR Codes so i can map to AC Remote
http://www.instructables.com/id/How-To-Useemulate-remotes-with-Arduino-and-Raspber/step8/Reading-IR-using-Raspberry-Pi/
Hardware Connection
    PINS
    Vcc to 3V3 / 5 V
    GROUND CENTER
    DATA GPIO18
Rasberry Steps
    # get latest
    sudo apt-get update
    sudo apt-get upgrade
        -- wow full upgrade ???
    sudo rpi-update
    sudo reboot
    sudo apt-get install lirc


    sudo nano /etc/modules
    added
    lirc_dev
    lirc_rpi gpio_in_pin=18 gpio_out_pin=17


    sudo nano /etc/lirc/hardware.conf
    changed
    DRIVER="default"
    DEVICE="/dev/lirc0"
    MODULES="lirc_rpi"

    sudo reboot

    sudo /etc/init.d/lirc stop
    sudo /etc/init.d/lirc status
    sudo /etc/init.d/lirc start

    Debug here
    http://www.jamesrobertson.eu/blog/2013/may/19/2326hrs.txt

    # Stop LIRC and run command to and point and test remote/ reboot once done
    # sudo /etc/init.d/lirc stop
    mode2 -d /dev/lirc0


    # List of all Available Actions
    irrecord --list-namespace
    #Start Mapping Signals to Action in a local file.
    irrecord -d /dev/lirc0 ~/lircd.conf
    #and move to the registered location
    sudo mv lircd.conf.conf /etc/lirc/lircd.conf


    #################################
    #SOLUTION 1 : Mapping Buttons to Commands , can be use for Simple
    #Buttons , but for AC each action sends the complete state and so cannot be used

    # Get your libs for Python to talk
    https://pypi.python.org/pypi/python-lirc/
    #Install Python LIRC Connect
    sudo apt-get install python3-lirc

    #create your new config for py-lirc
    #default location  ~/.lircrc : I am using "lircrc_button_to_app.conf"


    # And then you can use in python as
    import lirc
    sockid = lirc.init("myprogram")
    or for another config file
    sockid = lirc.init("myprogram", "mylircrc")

    #########

    #################################
    #SOLUTION 2 : This is Experimental
    # To understand States.








'''

sockid = lirc.init("pylirc_webservice", "lircrc_button_to_app.conf")
#sockid = lirc.init("pylirc_webservice", blocking = False)
#sockid = lirc.init("pylirc_webservice", blocking = False)

while(1) :
    codeIR = lirc.nextcode()
    print(codeIR)

lirc.deinit()