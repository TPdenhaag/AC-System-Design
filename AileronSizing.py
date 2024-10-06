from Constants import Constants
from Wing import WingSpan, RootChord, S
import numpy as np
import matplotlib.pyplot as plt

#the constants that have to do with aircraft configuartion
span = WingSpan #m
root_chord = RootChord #m
qc_sweep = Constants.QuarterChordSweep #deg
taper_ratio = Constants.TaperRatio 
Cl_alpha_deg = 0.085
Cl_alpha_rad = 7.26
wing_area = S #m^2
C_d0 = Constants.Cd0
velocity = Constants.CruiseSpeed #m/s

#Now the aileron specs
aileron_efficiency = 0.32
aileron_chord_ratio = 0.15
aileron_end = span/2 - 0.5       #here, the end of the aileron is defined. Half a meter is left for the wing tip. 
angle_up = 15
angle_down = angle_up * 0.75
angle_avg = (angle_up + angle_down) / 2

#Now some constants are calculated
tip_chord = root_chord * taper_ratio

#chord as a function of y (c = ay + b)
a_chord = 2*(tip_chord-root_chord) / span
b_chord = root_chord

#Mission requirement
Prequired = 60 / 7 #deg/s

#two big numbers are calculated for the ADSEE method

Big_int_1 = (a_chord/4 * (span/2) ** 4 + b_chord/3 * (span/2) ** 3)
Clp = -((4 * (Cl_alpha_deg + C_d0)) / (wing_area * span**2)) * Big_int_1


#Here, a base function is defined for to calculate the roll performance based on the aileron specifics and size.
def Pcalc(b1):
    Big_int_2 = a_chord/3 * aileron_end**3 + b_chord/2 * aileron_end**2 - a_chord/3 * b1**3 - b_chord/2 * b1**2

    Clda = 2 * Cl_alpha_deg * aileron_efficiency * Big_int_2 / (wing_area * span)

    Pcalculated = -Clda / Clp * angle_avg * 2 * velocity / span
    return(Pcalculated)


    #unused
        #y1tab = []
        #y2tab = []
        #xtab = np.arange(10,12.7,resolution)

aileron_start = span / 2
resolution = 0.01
searching = True

#starting at the wing tip, the roll rate is calculated, and it is checked whether the aileron size complies. 
#This is done iteratively, until the aileron meets requirements. This is the critical length and is output.
 
while searching:
    Ptemp = Pcalc(aileron_start)
    aileron_start -= resolution
    if Ptemp >= Prequired:
        searching = False
            #y1tab.append(Ptemp)
            #y2tab.append(Prequired)

aileron_middle = aileron_end - ((aileron_end - aileron_start) / 2)
chord_length_middle = a_chord * aileron_middle + b_chord
aileron_length_middle = aileron_chord_ratio * chord_length_middle

print("The starting location along the span must be at " + str(round(aileron_start,2)) + " or fewer meters from the root chord.")
print("The aileron ends at " + str(aileron_end) + " meters from the root chord")
print("The aileron chord will be " + str(round(aileron_length_middle,2)) + " meters.")

        #plt.plot(xtab,y1tab)
        #plt.plot(xtab,y2tab)

        #plt.show()