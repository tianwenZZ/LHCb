import subprocess, os
import time
import argparse

time_start = time.time()    # time start
print('INFO: time start:', time.asctime(time.localtime(time_start)))
parser = argparse.ArgumentParser()
parser.add_argument('--request-IDs', nargs='+',
                    help='Request IDs, split by space')
parser.add_argument("--wg", help='Name of working group')
parser.add_argument("--dir", help='Name of directory')
args = parser.parse_args()

#dirname = "MCStats_B2DstKpi"
#wg = "B2OpenCharm"
dirname = args.dir
requestIDs = args.request_IDs
wg = args.wg


# Get production IDs
command = 'python dirac-get-productionID.py '
for rid in requestIDs:
    command = command + rid + ' '
getProdIDs = subprocess.run(
    command,
    stdout=subprocess.PIPE,
    shell=True)
#exit_code = getProdIDs.wait()
#if exit_code:  # exit_code=0 means successfully exit
#    print("Error: Failed to get prodIDs !")
#    exit()
ProdIDs = getProdIDs.stdout.decode('utf-8')[:-1].split(',')
#print(ProdIDs)

# Generate stat files
ps_prepare = subprocess.run(f"mkdir {dirname}", shell=True)
#print(ps_prepare.wait())
#if ps_prepare.wait():
#    print(f"Error: cannot get in dir {dirname}! Exiting...")
#    exit()
pids= ''
i = 0
while True:
    if i>=len(ProdIDs): break
    # generate stat files every 8 production IDs
    if i + 8 < len(ProdIDs):
        pids= ','.join(ProdIDs[i:i + 8])
    else: 
        pids= ','.join(ProdIDs[i:])
    command = f"cd {dirname} && python ../scripts/DownloadAndBuildStat.py {pids} -w {wg}"
    ps_download = subprocess.Popen(command, shell=True)
    ps_download.wait()
    i+=8
ps_mv = subprocess.Popen(f"cp -r {dirname} ~/public/MCStatTools",
        shell=True)
ps_mv.wait()
print("Generation of {0} statistics tables is done!".format(dirname))



time_end = time.time()  # time end
print('INFO: time end:', time.asctime(time.localtime(time_end)))
time_sum = time_end - time_start  # time cost, unit: second
print('INFO: the program cost: {} min.'.format(round(time_sum/60, 2)))

