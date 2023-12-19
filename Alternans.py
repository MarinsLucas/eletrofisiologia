import numpy as np
import matplotlib.pylab as plt
import pylab
from math import *
import ap_features as apf


def ms_model (BCL):
    dt = 0.1
    T = 4000
    N = int(T/dt)+1
    tau_in = 0.3
    tau_out = 6.0
    v_gate = 0.1
    tau_open = 20.0
    tau_closed = 150.0
    time= np.zeros(N)
    t=0
    i=0
    w = 1
    u = 0.
    voltage = np.zeros(N)
    duration = 2
    t_ini = 0
    Jstim = 0.1

    nbeats = 0
    CLinc = 5

    c = 0
    while(t<T):
        Jin   = (w*(u*u*(1.0-u)))/tau_in
        Jout  = -u/tau_out
        Jstim = 0.1 if t>=t_ini and t<=t_ini+duration else 0
        I_ion = Jin + Jout + Jstim
        d_dt_h = (1.0-w)/tau_open if (u < v_gate) else -w/tau_closed

        u = u + dt*I_ion
        w= w + dt*d_dt_h
        voltage[i] = u
        time[i] = t
        t = t+dt
        i+=1

        
        if t>t_ini+duration and c <= 8:
            t_ini += 350
            c+=1
        else:
            if t>t_ini+duration and c == 9:
                t_ini+=BCL
                c+=1
        


    return [voltage, time]

DI = []
APDs = []
BCL = 350
while (BCL >= 300 ):
    voltagem, time = ms_model(BCL)

    
    """ plt.plot(time, voltagem)
    plt.show()  """
    trace = apf.Beats(y=voltagem, t=time)
    # Get a list of beats
    beats = trace.beats
    # Pick out the last beat
    beat = beats[-1]
    beat_ = beats[-2]
    APDs.append(beat.apd(80))
    DI.append(BCL-beat_.apd(80))
    print(f"BCL: {BCL} - APD: {beat.apd(80)}")
    BCL -= 5

plt.plot(DI, APDs, '-o')
plt.xlabel("DI (ms)")
plt.ylabel("ADP (ms)")
plt.title("Curva de Restituição")
plt.show()

#Calcular a derivada nos pontos

dADP = []
for i in range(len(DI) -1):
    dADP.append((APDs[i+1] - APDs[i])/(DI[i+1] - DI[i]))

plt.plot(DI[:-1], dADP, '-o')
plt.xlabel("DI (ms)")
plt.ylabel("ADP' (ms)")
plt.title("Derivadas dos pontos da curva de resituição")
plt.show()