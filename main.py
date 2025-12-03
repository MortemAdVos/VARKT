import krpc
import math
from time import time, sleep

from start import start
from munaManeur import munaManeur
from goman import goman
from normalCorrect import normalCorrect
from radialCorrect import radialCorrect
from dunaOrbit import dunaOrbit
from dunaLanding import landing, cirlcing

M1 = 1835

def inputTime(txt :str):
    return int(float(input(txt)))

print("start conn")
conn = krpc.connect()
print("conn sucsesfull")
rocket = conn.space_center.active_vessel
flightInfo = rocket.flight()
ap = rocket.auto_pilot
control = rocket.control

alt = conn.add_stream(getattr, rocket.flight(),'mean_altitude')
pericenter = conn.add_stream(getattr, rocket.orbit, 'periapsis_altitude')
apocenter = conn.add_stream(getattr, rocket.orbit, 'apoapsis_altitude')
speed = conn.add_stream(getattr, rocket.orbit, 'speed')
met = conn.add_stream(getattr, rocket, 'met')
panels = rocket.parts.with_tag("sol")
antens = rocket.parts.with_tag("ant")


tst = rocket.resources_in_decouple_stage(stage=4, cumulative=False)
ts_fuel = conn.add_stream(tst.amount, 'LiquidFuel')

control.rcs = True

control.sas = True

print("start processing")
conn.space_center.warp_to(1460)
while conn.space_center.ut < 1480:
    pass

startTime = conn.space_center.ut
print("StartTime: ", startTime)

start(ap, conn, control, pericenter, apocenter, alt, rocket, ts_fuel)
conn.space_center.warp_to(startTime+M1-222)

for p in panels:
    p.solar_panel.deployed = True
for a in antens:
    a.antenna.deployed = True

munaManeur(ap, conn, control, pericenter, apocenter, alt, rocket, speed, met, M1)

dv = float(input("dV in Muna correct: "))
if dv != 0:
    t = inputTime("time Muna correct maneur: ")
    conn.space_center.warp_to(t-150)
    radialCorrect(ap, conn, control, rocket, met, t-startTime, dv) 

dv = float(input("dV on normal axis: "))
if dv != 0:
    t = inputTime("time normal maneur: ")
    conn.space_center.warp_to(t-150)
    normalCorrect(ap, conn, control, rocket, speed, met, t-startTime, dv) 

tmd = inputTime('Goman maneur time input: ')-startTime
conn.space_center.warp_to(startTime+tmd-150)
goman(ap, conn, control, rocket, speed, met, tmd)


dv = float(input("dV in radial correct maneur: "))
if dv != 0:
    t = inputTime("time radial correct maneur: ")
    conn.space_center.warp_to(t-90)
    radialCorrect(ap, conn, control, rocket, met, t-startTime, dv) 

tmd = inputTime('Dune stop time input: ')-startTime
conn.space_center.warp_to(startTime+tmd-150)
dunaOrbit(ap, conn, control, rocket)

for p in panels:
    p.solar_panel.deployed = False
for a in antens:
    a.antenna.deployed = False

cirlcing(ap, conn, control, alt, rocket)

landing(ap, conn, control, rocket)

for p in panels:
    p.solar_panel.deployed = True
for a in antens:
    a.antenna.deployed = True

control.rcs = False