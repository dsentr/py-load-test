from flask import Flask, request
from functools import wraps
import subprocess 
from subprocess import PIPE, run
import logging

logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

app = Flask(__name__)

def stress_kill(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        killstring="kill -9 $(pidof of stress)"
        subprocess.run(killstring, shell=True, stdout=PIPE)
        logging.info("killing all stress tool processes")
        return func(*args, **kwargs)
    return wrapper

#Only accepts GET methods by default
#smoke test route
@app.route("/home")
@app.route('/') 
def health_check():
    logging.info("returned health check status: up!")
    return 'health check status: up!'

@app.route('/stress/kill')
@stress_kill
def kill_only():
    return "<p>killed all stress processes</p>", 200   

@app.route('/stress/cpu/<int:stresscpu>', methods=["GET"]) 
@stress_kill # decorator on bottom gets executed first
def stress_cpu_test(stresscpu):
    '''Uses stress tool to load test CPU'''
    cpu_options=[1,2]
    if stresscpu not in cpu_options:
        return "<p>cpu options are 1 or 2</p>", 404
    else:
        command='stress -c {} -i 1 -m 1 --vm-bytes 128M'.format(stresscpu)
        subprocess.Popen(command.split()) #popen is non-blocking, so don't need to wait for process to finish
        logging.info("starting memory stress test with %s CPU", stresscpu)
        return "<p>running stress test on cpu</p>", 201


@app.route('/stress/memory/<int:stressmem>', methods=["GET"])
@stress_kill
def stress_mem_test(stressmem):
    '''Uses stress tool to load test memory'''
    mem_options=[128,256,512]
    if stressmem not in mem_options:
        return "<p>memory options are 128, 256, or 512</p>", 404
    else:
        command='stress -c 1 -i 1 -m 1 --vm-bytes {}M'.format(stressmem)
        subprocess.Popen(command.split())
        logging.info("starting memory stress test with %s MB", stressmem)
        return "<p>running stress test on memory</p>", 201
   

if __name__ == '__main__':
    app.run()

