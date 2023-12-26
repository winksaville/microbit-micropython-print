from microbit import *

loop_number = 0
while True:
    loop_number = loop_number + 1
    print("Counter: " + str(loop_number));

    # We need to sleep as there appears to no handshake CTS/RTS
    # and if we don't slow things down the output can be garbaled
    # or possibly no output.
    sleep(500)

