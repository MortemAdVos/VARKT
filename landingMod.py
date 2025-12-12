from math import pi, e, sin, cos, radians, sqrt, atan2, acos
from matplotlib import pyplot as plt
from pygame import Vector2, Vector3

print()
# если досрочно отделять ступень, скорость посадки 80, если не отделять - 162, странные дела, топливо как-то мало юзается

FUEL_MASS = 5 # масса единицы топлива или окислителя
G = 6.67e-11
P0 = 0.148438 # плотность воздуха при h=0
DT = 1/100
HConst = 4623 # разница между высотой от уровня моря и высотой от поверхности

def show(x :list[list], vals :list[list], xdesc :str = '', ydesc :str = '', colors :list[str] = ['red'], eq :bool = False):
    f = plt.figure()
    if eq:
        axes = f.gca()
        axes.set_aspect('equal')
    f.supxlabel(xdesc)
    f.supylabel(ydesc)
    for i in range(len(vals)):
        plt.plot(x[i%len(x)], vals[i], colors[i%len(colors)])

    plt.show()


class Planet:

    def __init__(self, r, m, mu, ad, p) -> None:
        self.r = r # радиус планеты
        self.m = m # масса планеты
        self.mu = mu # молекулярка атмосферы
        self.ad = ad # показатель адиабаты
        self.p = p # давление на уровне моря


class Stup:

    def __init__(self, dm: float, fm: float, trust: float, fu: float) -> None:
        self.dryMass = dm 
        self.fuelMass = fm 
        self.trust = trust 
        self.fu = fu # расход топлива
        self.S = pi*(2.5**2)/4
        self.Cd = 0.87 # условно продольный цилиндр
        self.SC = self.S*self.Cd

    def mass(self):
        return self.dryMass + self.fuelMass

    def burn(self, time: float, k :float = 1.0):
        if self.fuelMass > 0.1:
            self.fuelMass -= self.fu * FUEL_MASS * time * k

            if self.fuelMass < 0:
                self.fuelMass = 0
                return 0
            else:
                return 1
        else:
            return 0

class Parashute:

    def __init__(self, D, h, h0) -> None:
        self.Cd = 1.5
        self.S = pi*(D**2)/4
        self.h = h
        self.h0 = h0
        self.isopened = False

    def getSC(self, h):
        if self.h0 < h or not self.isopened:
            return 0
        if self.h >= h:
            return self.S*self.Cd
        if self.h < h:
            return self.S/4*self.Cd
        
        print("Error in getCS parashute, h = ", h)
        raise Exception


class Rocket:

    def __init__(self, H, speed, angle) -> None:
        self.T = 0
        self.stups = []
        self.stups.append(Stup(7402, 16000*0.477, 4*117500, 4*8.024))
        self.stups.append(Stup(8100, 4320, 212500, 13.702))
        self.parashutes = []
        self.pos = Vector2(-H-duna.r, 0)
        self.speed = Vector2(speed*sin(radians(angle)), -speed*cos(radians(angle)))
        self.T1 = True
        self.T2 = True
        self.parashutes.append(Parashute(11.76, 2050, 3200))
        for _ in range(3): self.parashutes.append(Parashute(4.64, 2600, 3200))
        for _ in range(2): self.parashutes.append(Parashute(2.34, 5000, 8000))
        
        self.helpAngle:list[float]   = []
        self.infoPos  :list[Vector2] = []
        self.infoSpd  :list[Vector2] = []
        self.infoAcc  :list[Vector2] = []
        self.infoMass :list[float]   = []
        self.infoSC   :list[float]   = []
        self.infoAs   :list[float]   = []
        self.infoAt   :list[float]   = []
        self.infoAg   :list[float]   = []
        self.infoH    :list[float]   = []
        self.infoDV   :list[float]   = []

    def sep(self):
        if len(self.stups) == 2:
            print("Time separation: ", self.T)
            self.stups.pop(0)
    
    def openParashutes(self):
        for p in self.parashutes:
            p.isopened = True

    def mass(self):
        """
        функция возвращает массу корабля в данный момент
        """
        return sum(s.mass() for s in self.stups)

    def getH(self):
        """
        функция возвращает высоту для корабля в данный момент
        """
        return self.pos.length() - duna.r 
    
    def getSC(self):
        return sum([p.getSC(self.getH()) for p in self.parashutes] + [self.stups[0].SC])

    def getA(self):
        pass
    
    def getG(self):
        """
        функция возвращает ускорение свободного падения для корабля в данный момент
        """
        return G*duna.m/(self.pos.length()**2)
    
    def getP(self, h):
        """
        функция возвращает плотность воздуха около корабля в данный момент
        """
        return  P0*e**((-1.325e-4)*(h))

    def update(self, dt):
        self.T += dt

        a = Vector2(0,0)
        Ft = 0
        self.helpAngle.append(atan2(self.pos.y, self.pos.x))

        if self.getH() < 45000 and self.T1 and self.speed.length() > 800:
            if self.stups[0].burn(dt, 0.75):
                Ft = self.stups[0].trust * 0.75
            else:
                self.sep()
                
        elif self.T1 and self.speed.length() < 800:
            self.T1 = False
        
        if self.getH() < 12000 and self.T2 and self.speed.length() > 600:
            if self.stups[0].burn(dt, 0.5):
                Ft = self.stups[0].trust * 0.5
            else:
                self.sep()
        elif self.T2 and self.speed.length() < 600:
            self.T2 = False

        elif self.getH() < 12000:
            self.sep()
            self.openParashutes()

        if self.getH() < 150 and self.speed.length() > 5:
            if self.stups[0].burn(dt, 0.5):
                Ft = self.stups[0].trust*0.5
            


        Ag = self.getG() * self.pos.normalize()
        As = self.getP(self.getH())/2*self.speed.length_squared()*self.getSC()/self.mass() * self.speed.normalize()
        At = Ft*self.speed.normalize()/self.mass()

        a -= (Ag + As + At)

        self.pos += self.speed*dt + a*dt*dt/2
        self.speed += a*dt

        self.infoPos.append(Vector2(self.pos.x, self.pos.y))
        self.infoSpd.append(Vector2(self.speed.x, self.speed.y))
        self.infoAcc.append(Vector2(a.x, a.y))
        self.infoMass.append(self.mass())
        self.infoSC.append(self.getSC())
        self.infoAs.append(As.length())
        self.infoAt.append(At.length())
        self.infoAg.append(Ag.length())
        self.infoH.append(self.getH())
        try:
            self.infoDV.append(abs(self.infoSpd[-2].length()-self.infoSpd[-2].length())/dt)
        except:
            self.infoDV.append(0)


duna = Planet(320000, 4.515e21, 0.042, 1.2, 6755)
rocket = Rocket(90065-HConst, 825, -180-3.56)


while rocket.getH() > 3 and rocket.T < 1200:
    rocket.update(DT)

# print(rocket.T)

px = []
py = []
for i in range(len(rocket.infoPos)):
    a = rocket.infoPos[i].x
    b = rocket.infoPos[i].y
    px.append(a)
    py.append(b)

vx = []
vy = []
vm = []
for i in range(len(rocket.infoSpd)):
    a = rocket.infoSpd[i].x
    b = rocket.infoSpd[i].y
    vx.append(a*sin(rocket.helpAngle[i])+b*cos(rocket.helpAngle[i]))
    vy.append(a*cos(rocket.helpAngle[i])+b*sin(rocket.helpAngle[i]))
    vm.append(sqrt(a**2 + b**2))

ax = []
ay = []
am = []
for i in range(len(rocket.infoAcc)):
    a = rocket.infoAcc[i].x
    b = rocket.infoAcc[i].y
    ax.append(a*sin(rocket.helpAngle[i])+b*cos(rocket.helpAngle[i]))
    ay.append(a*cos(rocket.helpAngle[i])+b*sin(rocket.helpAngle[i]))
    am.append(sqrt(a**2 + b**2))

lT = [DT*i for i in range(len(px))]

PX = []
PY = []
I = 1000
for i in range(0, I):
    PX.append(sin(2*pi*i/I)*duna.r)
    PY.append(cos(2*pi*i/I)*duna.r)

HL = rocket.infoH
p2 = [rocket.getP(h+HConst) for h in HL]

data = [i.split(" ") for i in open("logs.txt", 'r').read().split("\n")[:-1]]
acL = []
vL = []
hL = []
pL = []
mL = []
asL = []
angleL = []
lonL = []
latL = []
scL = []
for i in data:
    # пока без массы, долготы и широты, потом пофикшу
    h, g, v, p, m, fs, an, lon, lat = map(float, i)
    # h, g, v, p, fs, an = map(float, i)
    hL.append(h-HConst)
    acL.append(g*9.81)
    vL.append(v)
    pL.append(p)
    mL.append(m)
    asL.append(fs/m)
    angleL.append(an)
    lonL.append(radians(lon))
    latL.append(radians(lat))
    scL.append(2*fs/v/v)

kt = (1004/len(data))

rT = [i*kt for i in range(len(data))]

xL = [rocket.infoPos[0].x]
yL = [rocket.infoPos[0].y]
aL = []

lonL, latL = latL, lonL

v1 = Vector3(cos(latL[0])*cos(lonL[0]), cos(latL[0])*sin(lonL[0]), sin(latL[0]))
for i in range(len(data)):
    v2 =  Vector3(cos(latL[i])*cos(lonL[i]), cos(latL[i])*sin(lonL[i]), sin(latL[i]))
    ang = acos(v1.x*v2.x + v1.y*v2.y +v1.z*v2.z)
    xL.append(-(hL[i]+duna.r)*cos(ang))
    yL.append((hL[i]+duna.r)*sin(ang))

# все фактические графики - фиолетовые

print("Скорость при контакте с грунтом: ", rocket.speed.length())

show([HL, hL], [p2, pL], "h","air density", colors=["red", "purple"])
show([px, xL, PX], [py, yL, PY], "px", "py", ["red", "purple", "black"], True)
show([lT, rT], [HL, hL], "t", "H", colors=["red", "purple"])
show([vm, vL], [HL, hL], "V", "H", colors=["red", 'purple'])
show([rocket.infoAs, asL], [HL, hL], "As", "H", colors=["red", "purple"])
show([rocket.infoAs, asL], [vm, vL], "As", "V", colors=["red", "purple"])
show([lT, rT], [vm, vL], "t", "speed", colors=["red", "purple"])
show([HL, hL], [rocket.infoAg, acL], "h", "g", colors=["red", "purple"])

show([lT, rT], [am, acL], "t","acceleration", colors=["red", "purple"])
show([HL, hL], [am, acL], "h","acceleration", colors=["red", "purple"])

show([lT, rT], [rocket.infoMass, mL], "t","mass, kg", colors=["red",  "purple"])
print()