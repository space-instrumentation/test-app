import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

uploaded_file1 = st.sidebar.file_uploader(
                        label="Upload Dataset",
                         type=['csv', 'xlsx'])

st.sidebar.markdown("""
[Train Dataset](https://pid-tuner.herokuapp.com)
""")

st.write ("""
# FOPDT Generator and Z-N Tuner App
""")


def run():

    # Extract data into X and y
    print('Original Dataset')
    print(data1)
    data = data1[:].values
    x = data1['Time']
    x = x[:].values
    print('Time Array')
    print(x)
    
    y = data1[['Output']]
    y = y[:].values
    print('Output Array')
    print(y)

    dc = 1

    t2q = 0.632 * dc
    print('t2q = {}'.format(t2q))
    t1q = 0.283 * dc
    print('t1q = {}'.format(t1q))

    distance = abs(t2q - x)
    print('distance = {}'.format(distance))
    minDistance = min(distance)
    print('minDistance = {}'.format(minDistance))
    print(np.where(distance == minDistance))
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
    j = t2 - t1
    print(j)
    
    L = t2 - t1
    print('L = {}'.format(round(L[0][0],3)))

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


    
    cols = st.beta_columns(2)
    cols[0].subheader('Dataset')
    cols[0].write(data1)
    cols[1].subheader('FOPDT Parameters')
    cols[1].write('L = {}'.format(round(L[0][0],3)))
    cols[1].write('tau = {}'.format(round(tau[0][0],3)))

    st.subheader('ZN Tuned Parameters: (Kp - Ki - Kd)')
    cols = st.beta_columns(3)
    cols[0].write(round(Kp,3))
    cols[1].write(round(Ki,3))
    cols[2].write(round(Kd,3))
    
    
    
    

if uploaded_file1 is not None:
    data1 = pd.read_csv(uploaded_file1)
    #st.write(data1)
    run()
else:
    st.info('Awaiting for CSV file to be uploaded.')
    
