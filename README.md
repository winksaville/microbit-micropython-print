# microbit-print-via-usb-serial

Explore a way to print to the USB serial port for debugging

Turns out it's trivial use Python `print()`, but to use
utime you can't use integer in `ticks_diff` so using a
`deadline` with `ticks_add`, which can use an integer to
calculate the `deadline` you can then use `ticks_diff`.
This seems to work, maybe there are other techniques but
this is good enough for now.

```
from microbit import *

loop_number = 0
while True:
    loop_number = loop_number + 1
    print("Counter: " + str(loop_number));

    # We need to sleep as there appears to no handshake CTS/RTS
    # and if we don't slow things down the output can be garbaled
    # or possibly no output.
    sleep(2000)
```

## Build and Run

Use two terminals, in the one edit and use for editing
and flashing, via uflash. In the other one use `screen`
or other method to connect to the USB serial port.
See [Find serial port](#find-serial-port).

In one terminal start `screen` or other app capable of
using the serial port:
```
sudo screen /dev/ttyACM0 115200
```

Now in the other terminal be sure you've got a
[venv enabled](#activate-microbit-virtual-environment)
activated with `uflash` then run
`uflash print.py`, see [Install uflash](#install-uflash)
necessary.

```
(micro-bit-uflash) wink@fwlaptop 23-12-26T22:39:22.452Z:~/prgs/micro-bit/MicroPython/print
$ uflash print.py
Flashing print.py to: /run/media/wink/MICROBIT/micropython.hex
(micro-bit-uflash) wink@fwlaptop 23-12-26T22:39:49.977Z:~/prgs/micro-bit/MicroPython/print
$ 
```

In the other terminal you'll see `Counter: X`,
where X is the `loop_number`.
```
Counter: 1
Counter: 2
Counter: 3
Counter: 4
Counter: 5
```

Sometimes the serial port can get out of sync or
be slow and you'll see missing characters/lines or
weird characters. Exit out of `screen` by typing 2
characters; Ctr-A Ctrl-D. You can also reset the
microbot using the reset button on the "bottom" of
the board next to the USB port.

## Install uflash

Install using `pip install uflash`](https://pypi.org/project/uflash/). On my
Arch Linux system I needed to install via in a
[virtual environment](https://wiki.archlinux.org/title/Python/Virtual_environment).
I created `mkdir ~/venv` and then created `python -m venv/microbit ~/venv/`. To
then activate the microbit virtual environment `source ~/venv/microbit/bin/activate`.

## Activate microbit virtual environment

```
wink@fwlaptop 23-12-26T22:39:03.599Z:~/prgs/micro-bit/MicroPython/print
$ . ~/venv/micro-bit-uflash/bin/activate
(micro-bit-uflash) wink@fwlaptop 23-12-26T22:39:22.452Z:~/prgs/micro-bit/MicroPython/print
```

## Find serial port

To find which serial port you use `sudo dmesg -W` output
and then plug in the microbit USB and look for `tty`. Below
we see: `[24028.909939] cdc_acm 3-4:1.1: ttyACM0: USB ACM device`
so the device is `ttyACM0` on my computer.
``` 
$ sudo dmesg -W
[24019.655263] usb 3-4: USB disconnect, device number 15
[24019.667136] umount: attempt to access beyond end of device
               sda: rw=0, sector=0, nr_sectors = 1 limit=0
[24019.667141] FAT-fs (sda): unable to read boot sector to mark fs as dirty
[24028.483332] usb 3-4: new full-speed USB device number 16 using xhci_hcd
[24028.899761] usb 3-4: New USB device found, idVendor=0d28, idProduct=0204, bcdDevice=10.00
[24028.899770] usb 3-4: New USB device strings: Mfr=1, Product=2, SerialNumber=3
[24028.899773] usb 3-4: Product: "BBC micro:bit CMSIS-DAP"
[24028.899776] usb 3-4: Manufacturer: ARM
[24028.899778] usb 3-4: SerialNumber: 9904360261974e450034001100000036000000009796990b
[24028.907947] usb-storage 3-4:1.0: USB Mass Storage device detected
[24028.908835] scsi host0: usb-storage 3-4:1.0
[24028.909939] cdc_acm 3-4:1.1: ttyACM0: USB ACM device
[24028.912458] hid-generic 0003:0D28:0204.000D: hiddev97,hidraw4: USB HID v1.00 Device [ARM "BBC micro:bit CMSIS-DAP"] on usb-0000:00:14.0-4/input3
[24029.934668] scsi 0:0:0:0: Direct-Access     MBED     VFS              0.1  PQ: 0 ANSI: 2
[24029.935649] sd 0:0:0:0: [sda] 131200 512-byte logical blocks: (67.2 MB/64.1 MiB)
[24029.935890] sd 0:0:0:0: [sda] Write Protect is off
[24029.935894] sd 0:0:0:0: [sda] Mode Sense: 03 00 00 00
```

You can also "search" the output with grep if you've
already plugged in the device. Below we see I plugged in
the device twice.
```
$ sudo dmesg | grep tty
[sudo] password for wink: 
[23991.893674] cdc_acm 3-4:1.1: ttyACM0: USB ACM device
[24028.909939] cdc_acm 3-4:1.1: ttyACM0: USB ACM device
```

## License

Licensed under either of

- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE) or http:
```
or what I do is `ls /dev/tty*` and 
Plug in the microbit into the computers USB port.
```
uflash print.py
```

## License

Licensed under either of

- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE) or http://apache.org/licenses/LICENSE-2.0)
- MIT license ([LICENSE-MIT](LICENSE-MIT) or http://opensource.org/licenses/MIT)

### Contribution

Unless you explicitly state otherwise, any contribution intentionally submitted
for inclusion in the work by you, as defined in the Apache-2.0 license, shall
be dual licensed as above, without any additional terms or conditions.

