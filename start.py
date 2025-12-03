

def start(ap, conn, control, pericenter, apocenter, alt, rocket, ts_fuel):

    target_alt = 102_000
    ap_pr = False

    fs_sep = True
    ss_sep = True
    ts_sep = True

    fst = rocket.resources_in_decouple_stage(stage=8, cumulative=False)
    sst = rocket.resources_in_decouple_stage(stage=6, cumulative=False)
    fs_fuel = conn.add_stream(fst.amount, 'LiquidFuel')
    ss_fuel = conn.add_stream(sst.amount, 'LiquidFuel')

    ap.engage()
    ap.target_pitch_and_heading(90,90)
    
    control.throttle = 1    
    control.activate_next_stage()

    while pericenter() < target_alt:
        if apocenter() > target_alt and pericenter() < target_alt:

            if apocenter()-75 < alt() and not ap_pr:
                print('ap was')
                ap_pr = True


            if ap_pr:
                ta = 5
            else:
                ta = 0
            ap.target_pitch = ta    

            if alt()+20000>target_alt:
                control.throttle = 1
            else:   
                control.throttle = 0

        elif apocenter() > target_alt and pericenter() > target_alt:
            control.throttle = 0

            ta = 0
            ap.target_pitch = ta

            break

        else:
            if alt() > 13000:
                control.throttle = 1
                ta = 90-(alt()-13000)/1000*2.4
                ta = max(ta, 0)
                ap.target_pitch = ta
            else:
                ap.target_pitch_and_heading(90,90)

        
        if fs_sep and fs_fuel() < 0.1:
            print(fs_fuel(), ss_fuel(), ts_fuel())
            control.throttle = 0
            control.activate_next_stage()
            control.activate_next_stage()
            control.throttle = 1
            fs_sep = False
            print("drop stage")
        if ss_sep and ss_fuel() < 0.1:
            print(fs_fuel(), ss_fuel(), ts_fuel())
            control.throttle = 0
            control.activate_next_stage()
            control.activate_next_stage()
            control.throttle = 1
            ss_sep = False
            print("drop stage")

    control.throttle = 0
    print("circle orbit finished")
    print()