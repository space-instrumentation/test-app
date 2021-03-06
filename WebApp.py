import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.integrate import odeint

st.write ("""
#  FOPDT Model Generator
""")

Tf = st.number_input('Feed Temperature:(Eg: 300 Kelvin)', 0, 1000, 300)
Caf = st.number_input('Feed Concentration:(Eg: 1 mol/lit)', 0, 100, 1)
q = st.number_input('Volumetric Flowrate:(Eg: 100 m^3/hr)', 0, 5000, 100)
V = st.number_input('Volume of Tank:(Eg: 100 m^3)', 0, 100, 100)

def run():
    # mixing model
    def mixer(x,t,Tf,Caf):
        # Inputs (2):
        # Tf = Feed Temperature (K)
        # Caf = Feed Concentration (mol/L)
        # States (2):
        # Concentration of A (mol/L)
        Ca = x[0]
        # Parameters:
        # Volumetric Flowrate (m^3/hr)
        #q = 100
        # Volume of CSTR (m^3)
        #V = 100
        # Calculate concentration derivative
        dCadt = q/V*(Caf - Ca)
        return dCadt

    # Initial Condition
    Ca0 = 0.0
    # Feed Temperature (K)
    #Tf = 300
    # Feed Concentration (mol/L)
    #Caf = 1
    # Time Interval (min)
    t = np.linspace(0,10,10000)

    # Simulate mixer
    Ca = odeint(mixer,Ca0,t,args=(Tf,Caf))
    data = np.vstack((t,Ca.T)) # vertical stack
    data = data.T     

    x = t
    y = Ca

    dc = 1

    t2q = 0.632 * dc
    t1q = 0.283 * dc

    distance = abs(t2q - x)
    minDistance = min(distance)
    np.where(distance == minDistance)
    a1 = data[np.where(distance == minDistance)]
    a1_split = np.hsplit(a1,2)
    t2 = a1_split[1]
    print('t2 (Time at 63.2% of Final Value) = {}'.format(t2[0]))

    distance1 = abs(t1q - x)       
    minDistance1 = min(distance1)
    np.where(distance1 == minDistance1)
    a2 = data[np.where(distance1 == minDistance1)]
    a2_split = np.hsplit(a2,2)
    t1 = a2_split[1]
    print('t1 (Time at 28.3% of Final Value) = {}'.format(t1[0]))

    tau = (t2 - t1) * 1.5
    print('Tau = {}'.format(round(tau[0][0],3)))
    L = t2 - t1
    f_L = round(L[0][0],3)
    f_tau = round(tau[0][0],3)
    st.subheader('FOPDT Model:')
    st.write('exp^{} * ({} / [{}s + 1])'.format(f_L,dc,f_tau))

    a = (dc*L)/tau
    Kp=0.95/a
    Ti=2.4*L
    Td=0.42*L
    Ki=Kp/Ti
    Kd=Kp*Td
    Kp = Kp[0][0]
    Ki = Ki[0][0]
    Kd = Kd[0][0]
    
    print('========Estimated Params.============')
    print('Kp = {}'.format(round(Kp,3)))
    print('Ki = {}'.format(round(Ki,3)))
    print('Kd = {}'.format(round(Kd,3)))
    print('===========MATLAB CODE===============')
    
    st.subheader('Initial Kp, Ki, Kd Values')
    st.write(round(Kp,3), round(Ki,3), round(Kd,3))
    st.info('*Copy the code given below and run in MATLAB. Upload the generated Dataset to PID-Tuner*')
    st.markdown("""
[PID Tuner](https://pid-tuner.herokuapp.com)
""")
    st.write('===================================')
    st.subheader('MATLAB CODE:')
    st.write('%Dataset Generation Code%') 
    st.write('Ki = 0;')
    st.write('Kp = 0;')
    st.write('Ki = {};'.format(round(Ki,3)))
    st.write('Kd = {};'.format(round(Kd,3)))
    st.write('for Kp = 0:0.01:{}'.format(round(Kp,3)))
    st.write("s = tf('s');")
    st.write('Ki_term = Ki*(1/s);')
    st.write('Kd_term = Kd*s;')
    st.write("C = Kp + Ki_Term + Kd_Term")
    st.write("Cl = feedback(C * P,1)")
    st.write('S = stepinfo(Cl);')
    st.write('I(n) = S.RiseTime;') 
    st.write('Q(n) = S.SettlingTime;')
    st.write('R(n) = S.Overshoot;')
    st.write('K(n) = Kp;')
    st.write('n = n + 1;')
    st.write('end')
    st.write('RiseTime = I(:);')
    st.write('SettlingTime = Q(:);')
    st.write('Overshoot = R(:);')
    st.write('KpValue = K(:);')
    st.write('Matrix = [KpValue RiseTime SettlingTime Overshoot]')
    
if st.button('Run'):
    st.markdown('Creating Model...')
    run()

else:
    st.info('Enter data and Run')
