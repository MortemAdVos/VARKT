import time
def normalCorrect(ap, conn, control, rocket, speed, met, tmd, dv):
    print("start normal correcting")
    dT = abs(dv)/(rocket.max_vacuum_thrust/rocket.mass)
    print("engine burn time: ", dT)
    ap.disengage()
    control.rcs = True
    control.throttle = 0
    control.sas = True
    time.sleep(1)
    if dv > 0:
        control.sas_mode = conn.space_center.SASMode.normal
    else:
        control.sas_mode = conn.space_center.SASMode.anti_normal

    p= int(met())
    while met() < tmd-dT:
        if int(met())%10==0 and p != int(met()): 
            p = int(met())
    if abs(dv) < 20:
        k = 0.1
    elif abs(dv) < 70:
        k = 0.5
    elif abs(dv) < 100:
        k = 0.75
    else:
        k = 1
    
    control.throttle = k
    time.sleep(round(dT,1))
    control.throttle = 0

    control.sas = False

    print('finished normal correcting')
    print()