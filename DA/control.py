#%%
import numpy as np
import matplotlib.pyplot as plt
import random
import json
import time
import lorenz96
#%%
json_file = open("parameter.json","r")
json_data = json.load(json_file)
N = np.int(json_data["N"])  # Number of variables
AW = np.int(json_data["AW"])
ADAY = np.float(json_data["ADAY"])
YEAR = np.int(json_data["YEAR"])
#%%
def read_data():
    data = np.fromfile("spinup.bin",dtype=np.float32)
    true = data.reshape(int(len(data)/N), N)
    data = np.fromfile("obs.bin",dtype=np.float32)
    obs = data.reshape(int(len(data)/N), N)
    return true, obs
true, obs = read_data()
#%%
def cal_rmse(data0, data1):
    rmse = []
    for i in range(len(data0[:,0])):
        rmse.append(np.sqrt(np.mean( (data0[i, :] - data1[i, :]) ** 2 )))
    return rmse
#%%
def main():    
    x = true[0,:] + random.normalvariate(0,0.01)      #Make Initial State
    result = []
    for t in range(int((YEAR/2) * 365 * (24/AW))):
        result.append(x)
        x = l96.short_run(x)
    control = np.array(result, dtype=np.float32)
    print("Control Run Data shape : {}".format(control.shape))
    #描画
    fig = plt.figure(figsize=(10,5))
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)
    #誤差の拡大
    ax1.set_title("X1")
    ax1.plot(control[0:200,0], label="Control")
    ax1.plot(true[0:200,0], label="True")
    ax1.set_xlabel("Step ( /6h )")
    ax1.legend()
    #RMSE描画
    rmse = cal_rmse(control, true)
    ax2.set_title("RMSE")
    ax2.plot(rmse[0:9], label="Control vs True")
    ax2.set_xlabel("Step ( /6h )")
    ax2.legend()
    fig.tight_layout()
    plt.savefig("Control.png",tight_layout=True, dpi=500)
    plt.show()
    #出力
    if(os.path.isfile("control.bin") == True):
        os.remove("control.bin")
    control.tofile("control.bin")
#%%
if(__name__ == "__main__"):
    start = time.time()
    main()
    elapsed = time.time() - start
    print("Elapsed Time : ",elapsed)
#%%