from MatchingDiagram import Constants, DesignPointX, StallVar
import math as m

WingLoading = DesignPointX
S = 404691/WingLoading
WingSpan = m.sqrt(Constants.AspectRatio*S)
RootChord = 2 * S/((1 + Constants.TaperRatio) * WingSpan)
MAC = 2 * RootChord * (1 + Constants.TaperRatio + Constants.TaperRatio**2)/(3 * (1 + Constants.TaperRatio))
yMAC = WingSpan * (1 + 2*Constants.TaperRatio)/(6 * (1 + Constants.TaperRatio))
HalfChordSweep = m.atan(2 * (m.tan(m.radians(Constants.QuarterChordSweep)) * 0.5 * WingSpan - 0.25 * RootChord + 0.25 * RootChord * Constants.TaperRatio)/(WingSpan))
ThicknessToChord = (m.cos(HalfChordSweep)**3 * (0.935 - (Constants.MachNum + 0.03)*m.cos(HalfChordSweep)) - 0.115*(Constants.ClCruise)**1.5)/(m.cos(HalfChordSweep)**2)
OswaldFactor = 2/(2 - Constants.AspectRatio + m.sqrt(4 + Constants.AspectRatio**2 * (1 + m.tan(HalfChordSweep)**2)))
def CalcDifferentSweep(CalcRatio):
   return(m.atan(m.tan(m.radians(Constants.QuarterChordSweep)) -4*((CalcRatio - 0.25)*(1 - Constants.TaperRatio)/(1 + Constants.TaperRatio))/Constants.AspectRatio))
CLMaxWing = Constants.ClMaxRatio * Constants.ClMaxAirfoil
HingeLineSweep = CalcDifferentSweep(0.7)
SwF = (Constants.ClMaxEstimate - CLMaxWing)/(0.9*Constants.dClMaxAirfoil * m.cos(HingeLineSweep)) * S

print("LES" + str(m.degrees(CalcDifferentSweep(0))))

#Dihedral = 
#dCLMaxWing = 
#dCl

print(S)
print(SwF)
print(RootChord)
print(WingSpan)
print(MAC)
print(yMAC)
print(ThicknessToChord)