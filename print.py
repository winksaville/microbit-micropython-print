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