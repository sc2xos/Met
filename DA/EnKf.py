#%%
import numpy as np
import matplotlib.pyplot as plt
import lorenz96 as l96
import random
import json 
#%%
json_file = open("parameter.json","r")
json_data = json.load(json_file)
N = np.int(json_data["N"])  # Number of variables
F = np.int(json_data["F"])  # Forcing
AW = np.float(json_data["AW"])
ADAY = np.float(json_data["ADAY"])
YEAR = np.int(json_data["YEAR"])
#%%
#時間発展の線形性を利用して近似的に求める
def jacobian(x):
    d = 1e-4
    Jacob = np.zeros((N, N))
    xb = l96.short_run(x)
    for i in range(N):
        xe = np.zeros(N)
        xe[:] = x[:]
        xe[i] = x[i] + d
        xa = l96.short_run(xe)    #誤差あり
        Jacob[:, i] = (xa[:] - xb[:]) / d
    return Jacob
#%%
def read_data():
    obs = np.fromfile("obs.bin",dtype=np.float32)
    obs = obs.reshape(int(len(obs)/N), N)
    print("##### Read Observation Data #####")
    print("Observation Data shape : ",obs.shape)
    control = np.fromfile("control.bin",dtype=np.float32)
    control = control.reshape(int(len(control)/N), N)
    print("##### Read Control Run Data #####")
    print("Control Run Data shape : ",obs.shape)
    true = np.fromfile("spinup.bin",dtype=np.float32)
    true = true.reshape(int(len(true)/N), N)
    print("##### Read True Value Data #####")
    print("True Value Data shape : ",obs.shape)
    return obs, control, true
obs, control, true = read_data()
#%%Kalman Filter
initial_Pa = np.identity(N) * 1e+1
#観測に欠損値はないので観測演算子は単位行列でOK
def EnKF(prev_Xa, prev_Pa, obs):
    delta = 0.1
    member = 40
    H = np.identity(N)      
    R = np.identity(N)
    #予報
    Xfk = []
    for m in range(member):
        #print("Member : {}".format(m))
        prev_Xak = prev_Xa + random.normalvariate(0,1)
        Xf = l96.short_run(prev_Xak)
        Xfk.append(Xf)
    #カルマンゲインの計算
    Xfk = np.array(Xfk)
    Xf_mean = np.mean(Xfk, axis=0)
    print("xf_mean.shape",Xf_mean.shape)
    print("Xfk",(np.array(Xfk)).shape)
    ##############################
    dXf = []
    for m in range(member):
        dXfk = Xfk[m,:] - Xf_mean
        dXf.append(dXfk)
    dXf = np.array(dXf)
    print("dXf.shape",dXf.shape)
    ##############################
    dYf = []
    for m in range(member):
        dyfk = H @ Xfk[m,:] - H @ Xf_mean
        dYf.append(dyfk)
    dYf = np.array(dYf)
    print("dYf.shape",dYf.shape)
    ####################
    K = dXf @ dYf.T @ np.linalg.inv( dYf @ dYf.T + (member - 1 )*R) 
    #解析値の計算
    Xak = Xfk + K @ (obs - H @ Xfk)
    print("Xak.shape",Xak.shape)
    #Pa = (np.identity(N) - K @ H) @ Pf
    #Print
    """
    print("Xf.shape : ", Xf.shape)
    print("M.shape : ",M.shape)
    print("Pf.shape : ", Pf.shape)
    print("H.shape : ", H.shape)
    print("R.shape : ", R.shape)
    print("K.shape : ", K.shape)
    print("Pa.shape : ", Pa.shape)
    print("Xa.shape : ", Xa.shape)
    """
    #Rの推定
    #d_ob = obs - H @ Xf
    #d_oa = obs - H @ Xa 
    #R = cal_R(d_oa, d_ob)
    
    return Xak
#Xak.shape = [40, 40]

#%%
def exec():
    Pa0 = np.identity(N) + 1e+1
    Xa0 = control[0,:]
    pa = Pa0
    xa = Xa0
    Xa = []
    Pa = []
    #for t in range(1):
    for t in range(int((YEAR/2) * 365 * (24/AW))-1):
        print("Time Step {}".format(t))
        Xa.append(xa)
        Pa.append(pa)
        xa = EnKF(xa, pa, obs[t+1, :])
        xa = np.mean(xa,axis=0)
    Xa = np.array(Xa)
    Pa = np.array(Pa)
    print(" Fnish Calculate Xa : ", Xa.shape)
    print(" Fnish Calculate Pa : ", Pa.shape)
    return Xa

Xa  = exec()
#%%
plt.plot(control[0:200,0],label="Control")
plt.plot(Xa[0:200,0],label="Xa")
plt.plot(true[0:200,0],label="True")
plt.legend()
#plt.plot(obs[:,0])
#%%
def calc_rmse(data1, data2):
    RMSE = []
    for i in range(len(data1[:,0])):
        rmse = np.sqrt(np.mean((data1[i,:] - data2[i,:]) ** 2))
        RMSE.append(rmse)
    return RMSE
#%%
RMSE1 = calc_rmse(control, true)
RMSE2 = calc_rmse(Xa, true)
RMSE3 = calc_rmse(obs, true)
plt.title("RMSE (vs True)")
plt.plot(RMSE1, label="Control")
plt.plot(RMSE2, label="Anlysis")
plt.plot(RMSE3, label="Observation")
plt.legend()
plt.savefig("non_delta.png")
#%%
"""
if(__name__ == "__main__"):
    start = time.time()
    main()
    elapsed = time.time() - start
    print("Elapsed Time : ",elapsed)
"""
# %%