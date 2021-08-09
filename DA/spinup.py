#%%
from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np
import json
import time
from numba import jit
import lorenz96 as l96
#%%
json_file = open("parameter.json","r")
json_data = json.load(json_file)
N = np.int(json_data["N"])  # Number of variables
F = np.int(json_data["F"])  # Forcing
dt = np.float(json_data["dt"])
AW = np.int(json_data["AW"])           #Assimilation Window
ADAY = np.float(json_data["ADAY"])    # / day
YEAR = np.int(json_data["YEAR"])      # Integration year
#%%
def main():
    x0 = F * np.ones(N)
    x0[19] += 0.01
    x = x0
    result = []
    for t in range(int(YEAR * 365 * (24/AW))):
        result.append(x)
        x = l96.short_run(x)
    spinup = np.array(result,dtype=np.float32)
    print("Spinup Data shape : ",spinup.shape)
    
    #3変数
    fig = plt.figure(figsize=(5,8))
    ax1 = fig.add_subplot(2, 1, 1, projection='3d')
    ax1.set_title("X1,X2,X3")
    ax1.plot(spinup[:, 0], spinup[:, 1], spinup[:, 2])
    ax1.set_xlabel('$x_1$')
    ax1.set_ylabel('$x_2$')
    ax1.set_zlabel('$x_3$')

    ax2 = fig.add_subplot(2, 1, 2)
    ax2.imshow(spinup[-40:-1, :],cmap="jet")
    ax2.set_xlabel("Step")
    ax2.set_ylabel("X")
    fig.suptitle("F = {}".format(F))
    plt.legend()
    plt.savefig("spinup_F{}.png".format(F), tight_layout=True, dpi=500)
    plt.show()

    #%%後半1年分を出力
    if(os.path.isfile("spinup.bin") == True):
        print("Remove alredy exist Data")
        os.remove("spinup.bin")
    output = spinup[int(len(spinup[:,0])/2):int(len(spinup[:,0])), :]
    print("Output Data shape : ",output.shape )
    output.tofile("spinup.bin")
    print("Complete output spinup.bin")

    return spinup
#%%
if(__name__ == "__main__"):
    start = time.time()
    spinup = main()
    elapsed = time.time() - start
    print("Elapsed Time : ",elapsed)
#%%
