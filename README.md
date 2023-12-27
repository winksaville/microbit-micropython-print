# microbit-print-via-usb-serial

Explore a way to print to the USB serial port for debugging

Turns out it's trivial use Python `print()`, but to use
utime you can't use integer in `ticks_diff` so using a
`deadline` with `ticks_add`, which can use an integer to
calculate the `deadline` you can then use `ticks_diff`.
This seems to work, maybe there are other techniques but
this is good enough for now.

```
import utime
from microbit import *

# Initial Globals
loop_number = 0
deadline_duration = 2 * 1_000_000
sleep_time = 0

# Delay start so there is time to sync with `screen`
utime.sleep_us(deadline_duration)

# Previous start_tick used to calculate actual duration
prev_start_tick = 0

# Loop
while True:
    # Record the time the loop starts
    start_tick = utime.ticks_us()

    # Bump loop_number
    loop_number = loop_number + 1

    # Calcuate the deadline so we can calculate how much time to sleep
    # Note: We can't use a constant in utime.ticks_diff so we determine
    #       the deadline and then use ticks_diff() to determine sleep_time.
    deadline = utime.ticks_add(start_tick, deadline_duration)

    # Display the current loop counter, we don't need to wait
    # since we've got a deadline and will be waiting at the bottom
    # Of course if this takes longer than the deadline the output
    # will not be correct. Setting the delay to 100 speeds up scrolling
    # so it's less likely to take a long time.
    display.scroll(loop_number, wait = True, delay = 100)

    duration1_ticks = utime.ticks_us()
    duration1 = utime.ticks_diff(duration1_ticks, start_tick)

    # the first time through print duration as 0
    if prev_start_tick == 0:
        prev_duration = 0
    else:
        prev_duration = start_tick - prev_start_tick

    # Print some debug
    print("Counter: " + str(loop_number) +
          " start_tick: " + str(start_tick) +
          " prev duration: " + str(prev_duration) +
          " prev sleep_time: " + str(sleep_time) +
          " duration1: " + str(duration1))

    duration2 = utime.ticks_diff(utime.ticks_us(), duration1_ticks)
    print("duration2: " + str(duration2));

    # Calculate time to sleep and sleep. Note
    # as we print more digits we won't sleep
    # because it takes longer to scroll through
    # the digits on the microbit display!
    sleep_time = utime.ticks_diff(deadline, utime.ticks_us())
    if sleep_time > 0:
        utime.sleep_us(sleep_time)

    prev_start_tick = start_tick
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

