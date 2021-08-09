# %%
import sys
import json
import time
import argparse
import numpy as np
import matplotlib.pyplot as plt

import pygrib
from bullet import Bullet
from mpl_toolkits.basemap import Basemap
import cartopy.crs as ccr
import seaborn as sns
# %%選択肢の表示
def cli(msg, options):
	"""
	str msg : コマンドライン上に表示するメッセージ
	list[str] coptions :　コマンドライン上で選択する選択
	"""		
	cli = Bullet(
		prompt = msg,
		choices = options
	)
	return cli.launch()

#%%入力待ち
def input_param():
	try:
		line = sys.stdin.readline().rstrip()
		while(line):
			line = line.strip("\n")
			#print(line)
		line = sys.stdin.readline().rstrip()
	except BrokenPipeError:
		devnull = os.open(os.devnull, os.O_WRONLY)
		os.dup2(devnull, sys.stdout.fileno())
		sys.exit(1)
	return line

#%%
# %%パラメータの入力
def fig_setting(msg, mold):
	while(True):
		print(msg + "を指定してください : ")
		input = cliutils.input_param()
		#input = line = sys.stdin.readline().rstrip()
		#setting = input()
		if(len(input) == 0):
			print(msg + "をデフォルトに指定します.")
			break
		else:
			try:
				resolution = mold(input)
				print(msg,resolution,"に指定します。")	
				return resolution 
			except ValueError:
				print("入力が不正")

"""input()でErrorが出るのでsys.stdin.readlinで代替
fig_setting(msg, mold):    
	while(True):
        setting = input(msg + "を指定してください : ")
        if(len(setting) == 0):
            print(msg + "デフォルトに指定します.")
            break
        else:    
            try:
                resolution = mold(setting)
                print(msg,resolution,"に指定します。")
                break
            except ValueError:
                print("入力が不正")
"""
