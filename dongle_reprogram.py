"""
Script used for pairing of new devices with Turris Dongle.

Shows current content of memory first, then asks whether you want to clear
current memory of programmed devices.

Can be also used for adding new devices, just select that you don't want
to clear the current memory and then enter ID of first empty slot.

Auto-detects RC-86K and calculates its second address.

End with pressing Ctrl+C or by entering any non-number during programming.
"""

from device import Device

if __name__ == "__main__":
    device = Device(device="/dev/ttyUSB0")
    reader = device.gen_lines()

    # print current status
    for i in range(0, 32):
        device.send_command("GET SLOT:%02d" % i)
        print reader.next()

    slot_id = 0
    # optional erasing
    erase_all = raw_input("Erase all slots first? [y/N] ")
    if erase_all.lower() == "y":
        print "Erasing all slots..."
        device.send_command("ERASE ALL SLOTS")
        print reader.next()
    else:
        # custom first slot ID
        start = raw_input("Where do you want to start programming?\n"
                          "Enter number of the first slot or anything else "
                          "for programming from slot #00: ")
        try:
            slot_id = int(start)
            if slot_id <= 0 or slot_id >= 32:
                print "Error: slot number must be number from 0 to 31."
                exit(1)
        except ValueError:
            pass

    # the programming itself
    while True:
        device_addr = raw_input("Enter ID for device number #%02d: " % slot_id)
        try:
            device_addr = int(device_addr[-8:])
        except ValueError:
            break
        c = "SET SLOT:%02d [%08d]" % (slot_id, device_addr)
        print "SENDING:", c
        device.send_command(c)
        print "REPLY:", reader.next()
        slot_id += 1
        if 0x800000 <= device_addr <= 0x87FFFF:
            device_addr |= 1 << 20
            print "Programming second keypad's ID: %08d" % device_addr
            c = "SET SLOT:%02d [%08d]" % (slot_id, device_addr)
            print "SENDING:", c
            device.send_command(c)
            print "REPLY:", reader.next()
            slot_id += 1
