import time 

def goman(ap, conn, control, rocket, speed, met, tmd):
    print("start goman maneur")
    dV = 880
    dT = abs(dV)/(rocket.max_vacuum_thrust/rocket.mass)
    print("engine burn time: ", dT)

    ap.disengage()
    control.rcs = True
    control.throttle = 0
    control.sas = True
    time.sleep(1)
    control.sas_mode = conn.space_center.SASMode.prograde

    while met() < tmd-dT:
        pass

    orbspeed = speed()
    print('engine on')
    control.throttle = 1
    while orbspeed + dV > speed():
        pass
    control.throttle = 0

    print('end goman maneur')
    print()