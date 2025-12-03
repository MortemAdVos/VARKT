def munaManeur(ap, conn, control, pericenter, apocenter, alt, rocket, speed, met, tmd):
    print("start Muna maneur")
    dV = 835
    dT = 100

    control.throttle = 0
    ap.target_pitch_and_heading(-18,90)

    while met() < tmd-dT:
        pass

    orbspeed = speed()
    control.throttle = 1
    while orbspeed + dV > speed():
        ta = -17*(1-(speed()-orbspeed)/dV)
        ap.target_pitch = ta
    control.throttle = 0
    print('end muna maneur')
    print()