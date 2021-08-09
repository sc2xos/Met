#%%
import numpy as np
import random
import matplotlib.pyplot as plt
import json
import lorenz96
#%%
json_file = open("parameter.json","r")
json_data = json.load(json_file)
N = np.int(json_data["N"])
#%%
data = np.fromfile("spinup.bin",dtype=np.float32)
spinup = data.reshape(int(len(data)/N), N)
#%%
def main():
    read_shape = spinup.shape
    read_data = spinup.flatten()
    obs = []
    for i in range(len(read_data)):
        obs.append( read_data[i] + random.normalvariate(0, 1) )
    obs = np.array(obs,np.float32)
    obs = obs.reshape(read_shape)
    print("Observation Data shape : {}".format(obs.shape))
    #描画
    plt.title("True(X1) and Observation")
    plt.plot(spinup[0:200,0],  linestyle="solid", label="True")
    plt.plot(obs[0:200,0], linestyle="solid", label="Observation")
    plt.xlabel("Step")
    plt.legend()
    plt.savefig("obsmake.png", tight_layout=True, dpi=500)
    plt.plot()
    #出力
    if(os.path.isfile("obs.bin") == True):
        print("Remove already exist obs.bin")
        os.remove("obs.bin")
    obs.tofile("obs.bin")
    print("Complete output obs.bin")
# %%
if(__name__ == "__main__"):
    main()
#%%
