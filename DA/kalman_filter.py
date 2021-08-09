#%%
import numpy as np
import matplotlib.pyplot as plt
import lorenz96 as l96
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
#%%
def kalman_filter(Xa, Pa, obs, delta=0.1, H=np.identity(N), R=np.identity(N)):
    #予報
    Xf = l96.short_run(Xa)
    #カルマンゲインの計算
    M = jacobian(Xa)
    Pf = ( 1 + delta ) * M @ Pa @ M.T
    K = Pf @ H.T @ np.linalg.inv(H @ Pf @ H.T +R)
    #解析値の計算
    Xa = Xf + K @ (obs - H @ Xf)
    Pa = (np.identity(N) - K @ H) @ Pf
    return Xa, Pa

#%%
def exec():
    Pa0 = np.identity(N) + 1e+1
    Xa0 = control[0,:]
    pa = Pa0
    xa = Xa0
    Xa = []
    Pa = []
    for t in range(int((YEAR/2) * 365 * (24/AW))-1):
        print("Time Step {}".format(t))
        Xa.append(xa)
        Pa.append(pa)
        xa, pa= kalman_filter(xa, pa, obs[t+1, :])
    Xa = np.array(Xa)
    Pa = np.array(Pa)
    print(" Fnish Calculate Xa : ", Xa.shape)
    print(" Fnish Calculate Pa : ", Pa.shape)
    return Xa, Pa

Xa, Pa = exec()
#%%
plt.title("X1")
plt.plot(control[0:200,0],label="Control")
plt.plot(Xa[0:200,0],label="Analysis")
plt.plot(true[0:200,0],label="True")
plt.plot(obs[0:200,0])
plt.xlabel("Step ( /6h)")
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
plt.xlabel("Step ( /6h )")
plt.legend()
plt.savefig("non_delta.png",tight_layout=True, dpi=500)
#%%
"""
if(__name__ == "__main__"):
    start = time.time()
    main()
    elapsed = time.time() - start
    print("Elapsed Time : ",elapsed)
"""
# %%
