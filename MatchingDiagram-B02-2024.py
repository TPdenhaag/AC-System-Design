import matplotlib.pyplot as plt
import math as m

#List of Constants

class ConstantsClass:
#Known Values
    MachNum = 0.77
    ByPassRatio = 6
    CruiseSpeed = 228.3
    NumEngines = 2
    LandingLength = 1210
    TakeoffLength = 1296
    CVClimbGradient = 0.024

#Mass Ratios:
    MassRatio = 0.95
    MassRatioLanding = 0.845

#Variables that have been set as an example, but are not real!!
    ClCruise = 0.65
    ClClimb = 1.2
    Clfl = 0.6
    ClMax = 2.5
    ClLanding = 2.1
    Cd0 = 0.02
    #Mass Ratio is Beta
    AspectRatio = 9
    OswaldFactor = 0.8
    StallSpeed = 70
    LandingAltitude = 1600
    LandingDensity = 1.04759
    RateOfClimb = 15
    Kt = 0.85

#Less important constants
    SeaLevelTemperature = 288.15
    #Cruise Altitude: FL35000
    TemperatureAtCruise = 218.81
    PressureAtCruise = 23835.918
    DensityAtCruise = 0.3796
    #Climb Rate Altitude: 7400
    PressureAtClimb = 38800
    TemperatureAtClimb = 240
    DensityAtClimb = 0.563
    #Climb Gradient Altitude:1600m
    PressureAtClimbGrad = 83523.5
    TemperatureAtClimbGrad = 240
    DensityAtClimbGrad = 0.563

    #Climb Grad Requirements taken from CS-25 Certification Specifications * a safety factor (1.5)
    Cl25119 = 1.27
    Cd25119 = 0.059
    Oswald25119 = 0.868
    ClimbReq25119 = 0.038
    Cl25121a = 1.01
    Cd25121a = 0.0395
    Oswald25121a = 0.829
    ClimbReq25121a = 0.045
    Cl25121b = 1.013
    Cd25121b = 0.0395
    Oswald25121b = 0.829
    ClimbReq25121b = 0.036
    Cl25121c = 0.704
    Cd25121c = 0.02
    Oswald25121c = 0.79
    ClimbReq25121c = 0.018
    Cl25121d = 1.268
    Cd25121d = 0.059
    Oswald25121d = 0.829
    ClimbReq25121d = 0.0315
    
    CS25SafetyMargin = 1.5



    PressureAtTakeoff = 101325
    TemperatureAtTakeoff = 288.15
    DensityAtTakeoff = 1.225
    Gamma = 1.4

Constants = ConstantsClass()

#List of Functions 

#For CalcAlpha, an extra input is required: the lift coefficient for whatever scenario you're on (cruise, climb, etc...)
def CalcAlphaT(Input, Constants, ClUsed, PressureUsed, TempUsed, DensityUsed):
    SpeedForAlpha = m.sqrt(2 * Input * DensityUsed * ClUsed)
    MachNumberForAlpha = SpeedForAlpha/m.sqrt(Constants.Gamma * 287 * TempUsed)
    TotalPressure = PressureUsed * (1 + (Constants.Gamma - 1)/2 * MachNumberForAlpha**2)**(Constants.Gamma/(Constants.Gamma - 1))
    ConstantComponent = 1-(0.43 + 0.014*Constants.ByPassRatio)*m.sqrt(MachNumberForAlpha)
    SigmaT = TotalPressure/101325
    AlphaT = SigmaT * ConstantComponent
    return(AlphaT)

def CalcStallSpeed(Constants):
    return((1.225)/(2 * Constants.MassRatio)*((Constants.StallSpeed)/(1.23))**2 * Constants.ClMax)

def CalcLanding(Constants):
    #Pressure = 101325 * (1 + (-0.0065*Constants.LandingAltitude)/(Constants.SeaLevelTemperature))
    LandingFieldLength = Constants.Clfl * (Constants.StallSpeed)**2

    FinalOutput = 1/Constants.MassRatioLanding * (LandingFieldLength)/(Constants.Clfl) * Constants.LandingDensity * Constants.ClMax/2
    return(FinalOutput)

def CalcCruiseSpeed(Input, Constants):
    AlphaT = CalcAlphaT(Input, Constants, Constants.ClCruise, Constants.PressureAtCruise, Constants.TemperatureAtCruise, Constants.DensityAtCruise)
    #The calculation for cruise is Beta/AlphaT * 2 big blocks to the power or -1. These are Blocks 1 and 2
    Block1 = (Constants.Cd0 * 0.5 * Constants.DensityAtCruise * (Constants.CruiseSpeed)**2)/(Constants.MassRatio * Input)
    Block2 = (Constants.MassRatio * Input)/(m.pi * Constants.AspectRatio * Constants.OswaldFactor * 0.5 * Constants.DensityAtCruise * (Constants.CruiseSpeed)**2)
    return((Constants.MassRatio/AlphaT) * (Block1 + Block2))

def CalcClimb(Input, Constants):

    C = Constants.RateOfClimb

    AlphaT = CalcAlphaT(Input, Constants, Constants.ClClimb, Constants.PressureAtClimb, Constants.TemperatureAtClimb, Constants.DensityAtClimb)
    Block1 = (C**2)/(Constants.MassRatio * Input) * (Constants.DensityAtCruise)/(2) * m.sqrt(Constants.Cd0 * m.pi * Constants.AspectRatio * Constants.OswaldFactor)
    Block2 = Constants.Cd0/(m.pi * Constants.AspectRatio * Constants.OswaldFactor)
    return((Constants.MassRatio/AlphaT) * (m.sqrt(Block1) + 2 * m.sqrt(Block2)))

def CalcTakeoff(Input, Constants):
    V2 = m.sqrt(Input * 2/Constants.DensityAtTakeoff * 1/Constants.ClMax)
    Cl2 = (Constants.StallSpeed/V2)**2 * Constants.ClMax
    AlphaT = CalcAlphaT(Input, Constants, Cl2, Constants.PressureAtTakeoff, Constants.TemperatureAtTakeoff, Constants.DensityAtTakeoff)
    H2 = 11
    Lto = Constants.TakeoffLength
    Ne = (Constants.NumEngines)/(Constants.NumEngines - 1)
    return(1.15 * AlphaT * m.sqrt(Ne * Input/(Lto * Constants.Kt * Constants.DensityAtTakeoff * 9.80665 * m.pi * Constants.AspectRatio * Constants.OswaldFactor)) + Ne * (4 * H2)/(Lto))

def CalcClimbGradient(Input, Constants, MassRatio, Cl, Cd0, Oswald, Ne, ClimbRequirement):
    AlphaT = CalcAlphaT(Input, Constants, Cl, Constants.PressureAtClimbGrad, Constants.TemperatureAtClimbGrad, Constants.DensityAtClimbGrad)
    return(Ne * MassRatio/AlphaT * (ClimbRequirement + 2*m.sqrt(Cd0/(m.pi * Constants.AspectRatio * Oswald))))

WingLoading = [100*x for x in range(0, 91)]
#WingLoading is W/S, and forms the X axis of the plot


StallVar = CalcStallSpeed(Constants)
LandVar = CalcLanding(Constants)
print(LandVar)
CruiseList = []
ClimbList = []
TakeoffList = []
CgList = []
Cg25119 = []
Cg25121a = []
Cg25121b = []
Cg25121c = []
Cg25121d = []

for i in range(len(WingLoading)):
    if WingLoading[i] > 500:
        TakeoffList.append(CalcTakeoff(WingLoading[i], Constants))
        CruiseList.append(CalcCruiseSpeed(WingLoading[i], Constants))
        ClimbList.append(CalcClimb(WingLoading[i], Constants))
        CgList.append(CalcClimbGradient(WingLoading[i], Constants, Constants.MassRatio, Constants.ClClimb, Constants.Cd0, Constants.OswaldFactor, 2, Constants.CVClimbGradient))
        Cg25119.append(CalcClimbGradient(WingLoading[i], Constants, Constants.MassRatio, Constants.Cl25119, Constants.Cd25119, Constants.Oswald25119, 2, Constants.ClimbReq25119))
        Cg25121a.append(CalcClimbGradient(WingLoading[i], Constants, Constants.MassRatio, Constants.Cl25121a, Constants.Cd25121a, Constants.Oswald25121a, 1, Constants.ClimbReq25121a))
        Cg25121b.append(CalcClimbGradient(WingLoading[i], Constants, Constants.MassRatio, Constants.Cl25121b, Constants.Cd25121b, Constants.Oswald25121b, 1, Constants.ClimbReq25121b))
        Cg25121c.append(CalcClimbGradient(WingLoading[i], Constants, Constants.MassRatio, Constants.Cl25121c, Constants.Cd25121c, Constants.Oswald25121c, 1, Constants.ClimbReq25121c))
        Cg25121d.append(CalcClimbGradient(WingLoading[i], Constants, Constants.MassRatio, Constants.Cl25121d, Constants.Cd25121d, Constants.Oswald25121d, 1, Constants.ClimbReq25121d))

plt.axvline(StallVar, c = "blue", label = "Stall Speed")
plt.axvline(LandVar, c = "red", label = "Landing Field")
plt.plot([100*x for x in range(6, 91)], ClimbList, c = (0.9, 0.9, 0), label = "Climb Rate")
plt.plot([100*x for x in range(6, 91)], CruiseList, c = "purple", label = "Cruise Speed")
plt.plot([100*x for x in range(6, 91)], TakeoffList, c = (0.8, 0.3, 0.6), label = "Takeoff")
plt.plot([100*x for x in range(6, 91)], CgList, c = (0.6, 0.6, 0.3), label = "Climb Gradient")
plt.plot([100*x for x in range(6, 91)], Cg25119, c = (0.4, 0.6, 0.7), label = "Cg: 25119")
plt.plot([100*x for x in range(6, 91)], Cg25121a, c = (0, 0, 0.3), label = "Cg: 25121a")
plt.plot([100*x for x in range(6, 91)], Cg25121b, c = (0, 0.25, 0.3), label = "Cg: 25121b")
plt.plot([100*x for x in range(6, 91)], Cg25121c, c = (0, 0.5, 0.3), label = "Cg: 25121c")
plt.plot([100*x for x in range(6, 91)], Cg25121d, c = (0, 0.9, 0.4), label = "Cg: 25121d")
plt.plot(5220.47, 0.43632, marker = "x", markersize = 10, markeredgecolor = "red")
plt.legend(loc="upper right")
plt.ylim(0, 1)
plt.xlabel("W/S")
plt.ylabel("T/W")
plt.show()