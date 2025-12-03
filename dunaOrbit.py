import time

def dunaOrbit(ap, conn, control, rocket):
    print("start Duna maneur")

    ap.disengage()
    control.rcs = True
    control.throttle = 0

    control.sas = True
    time.sleep(1)
    control.sas_mode = conn.space_center.SASMode.retrograde
    pericenter = conn.add_stream(getattr, rocket.orbit, 'periapsis_altitude')

    tst = rocket.resources_in_decouple_stage(stage=4, cumulative=False)
    ts_fuel = conn.add_stream(tst.amount, 'LiquidFuel')
    ts_sep = True

    time.sleep(5)

    
    k = 0.75
    while pericenter() > 90000:
        control.throttle = k
        if pericenter() < 250000:
            k = 0.25
        elif pericenter() < 500000:
            k = 0.5
        if ts_sep and ts_fuel() < 0.1:
            control.activate_next_stage()
            control.activate_next_stage()
            ts_sep = False
            print("drop stage")
    control.throttle = 0
    print('end Duna maneur')
    print()