from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np
from numba import jit
import json
#%%
json_file = open("parameter.json","r")
json_data = json.load(json_file)
N = np.int(json_data["N"])  # Number of variables
F = np.int(json_data["F"])  # Forcing
dt = np.float(json_data["dt"])
AW = np.int(json_data["AW"])           #Assimilation Window
ADAY = np.float(json_data["ADAY"])    # / day
YEAR = np.int(json_data["YEAR"])      # Integration year
x0 = F * np.ones(N)
x0[19] += 0.01
#%%
@jit
def lorenz96(x):
    """Lorenz 96 model."""
    # Compute state derivatives
    d = np.zeros(N)
    # First the 3 edge cases: i=1,2,N
    d[0] = (x[1] - x[N-2]) * x[N-1] - x[0] + F
    d[1] = (x[2] - x[N-1]) * x[0] - x[1] + F
    d[N-1] = (x[0] - x[N-3]) * x[N-2] - x[N-1] + F
    # Then the general case
    for i in range(2, N-1):
        d[i] = (x[i+1] - x[i-2]) * x[i-1] - x[i] + F
    # Return the state derivatives
    return d
#%%
@jit
def RK4(xin):
    k1 = lorenz96(xin) * dt
    k2 = lorenz96(xin + k1/2) * dt
    k3 = lorenz96(xin + k2/2) * dt
    k4 = lorenz96(xin + k3) * dt
    xout = xin + ( k1 + 2*k2 + 2*k3 + k4 ) / 6 
    return xout
#%%6時間積分
@jit
def short_run(prev_x):
    x = prev_x
    interval = int(ADAY / (24/AW) / dt ) 
    result = []
    for t in range(interval):
        x = RK4(x)
    output = np.array(x, dtype=np.float32)
    #print("Spinup Data shape : {}".format(output.shape))
    return output

#%%