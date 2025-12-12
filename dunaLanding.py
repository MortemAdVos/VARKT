from time import time, sleep
from math import sqrt


def length(a):
    return sqrt(sum(i**2 for i in a))


def landing(ap, conn, control, rocket):


    def logging():
        g = flightInfo().g_force
        malt = flightInfo().mean_altitude
        v = rocket.orbit.speed
        p = flightInfo().atmosphere_density
        m = rocket.mass
        Fs = length(flightInfo().aerodynamic_force)
        angle = flightInfo().pitch
        longitude = flightInfo().longitude
        latitude = flightInfo().latitude

        file.write(f"{malt} {g} {v} {p} {m} {Fs} {angle} {longitude} {latitude}\n")

    print("start landing")
    control.throttle = 0
    control.sas = True
    sleep(1)
    control.sas_mode = conn.space_center.SASMode.retrograde
    alt = conn.add_stream(getattr, rocket.flight(),'surface_altitude')
    legs = rocket.parts.with_tag("sh")
    flightInfo = rocket.flight


    with open("logs.txt", "a+", encoding="UTF-8") as file:

        while alt() > 45000:
            logging()

        if rocket.orbit.speed > 800:
            control.throttle = 0.75

        while rocket.orbit.speed > 800:
            logging()

        control.throttle = 0

        while alt() > 12000:
            logging()

        if rocket.orbit.speed > 600:
            control.throttle = 0.5

        while rocket.orbit.speed > 600:
            logging()

        control.throttle = 0
        logging()
        sleep(2)
        logging()

        control.activate_next_stage()
        logging()
        control.activate_next_stage()
        logging()
        sleep(1)
        logging()

        control.activate_next_stage()
        for l in legs:
            l.leg.deployed = True
        
        logging()
        
        while alt() > 120:
            logging()

        while alt() > 8:
            logging()
            if rocket.orbit.speed > 5:
                control.throttle = 0.2
            else:
                control.throttle = 0
        control.throttle = 0
        logging()
        print("landing finished")


def cirlcing(ap, conn, control, alt, rocket):

    ap.disengage()
    control.rcs = True
    pericenter = conn.add_stream(getattr, rocket.orbit, 'periapsis_altitude')

    print("start duna cirlce maneur")

    control.throttle = 0
    control.sas = True
    sleep(1)
    control.sas_mode = conn.space_center.SASMode.retrograde

    if rocket.orbit.time_to_periapsis > 80:
        conn.space_center.warp_to(conn.space_center.ut+rocket.orbit.time_to_periapsis - 70)
    
    while rocket.orbit.time_to_periapsis > 60000:
        pass
    
    sleep(5)

    control.throttle = 1
    while pericenter() > 25000:
        pass
    control.throttle = 0

    print('end Duna cirlcing maneur')
    print()