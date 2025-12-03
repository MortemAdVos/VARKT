import time 

def landing(ap, conn, control, rocket):

    print("start landing")
    control.throttle = 0
    control.sas = True
    time.sleep(1)
    control.sas_mode = conn.space_center.SASMode.retrograde
    alt = conn.add_stream(getattr, rocket.flight(),'surface_altitude')
    legs = rocket.parts.with_tag("sh")

    while alt() > 45000:
        pass
    if rocket.orbit.speed > 800:
        control.throttle = 0.75
    while rocket.orbit.speed > 800:
        pass
    control.throttle = 0

    while alt() > 12000:
        pass
    if rocket.orbit.speed > 600:
        control.throttle = 0.5
    while rocket.orbit.speed > 600:
        pass
    
    time.sleep(2)

    control.activate_next_stage()
    control.activate_next_stage()

    time.sleep(1)

    control.activate_next_stage()
    for l in legs:
        l.leg.deployed = True
    
    while alt() > 100:
        pass

    while alt() > 10:
        if rocket.orbit.speed > 5:
            control.throttle = 0.2
        else:
            control.throttle = 0
    control.throttle = 0
    print("landing finished")


def cirlcing(ap, conn, control, alt, rocket):

    ap.disengage()
    control.rcs = True
    pericenter = conn.add_stream(getattr, rocket.orbit, 'periapsis_altitude')

    print("start duna cirlce maneur")

    control.throttle = 0
    control.sas = True
    time.sleep(1)
    control.sas_mode = conn.space_center.SASMode.retrograde

    if rocket.orbit.time_to_periapsis > 80:
        conn.space_center.warp_to(conn.space_center.ut+rocket.orbit.time_to_periapsis - 70)
    
    while rocket.orbit.time_to_periapsis > 60000:
        pass
    
    time.sleep(5)

    control.throttle = 1
    while pericenter() > 25000:
        pass
    control.throttle = 0

    print('end Duna cirlcing maneur')
    print()