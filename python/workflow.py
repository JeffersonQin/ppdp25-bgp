import sys
from gadget import Gadget
from metarouting import check_convergence
from divergence import get_sp_links, maude_search

from cvc5.pythonic import sat
import multiprocessing as mp

from datetime import datetime, timedelta
import time

from functools import partial

print = partial(print, flush=True)


def work(gadget: Gadget, sp_links=None, sp_recur_size=None, timeout=None):
    links = sp_links
    if links is None:
        rsat, solver = check_convergence(gadget)


        if rsat == sat:
            print(f"{gadget.name} converges.")
            return

        print(f"{gadget.name} diverges.")
        print(f"Computing links leading to divergence:")

        links = get_sp_links(solver)
        print(links, flush=True)

    if sp_recur_size is None:
        recur_sizes = [3, 4, 5, 6, 7]
    else:
        recur_sizes = sp_recur_size
    manager = mp.Manager()
    shared_data = manager.list()

    jobs = []

    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=timeout) if timeout is not None else None

    for size in recur_sizes:
        p = mp.Process(target=maude_search, args=((gadget, links, size, shared_data)), name=f"SEARCH {size}")
        p.start()
        print(f"Started process {p.name} with id {p.pid}", flush=True)
        jobs.append(p)



    finished_process = None
    ecode = 0
    while not finished_process and (timeout is None or datetime.now() < end_time):
        for job in jobs:
            if not job.is_alive() and job.exitcode == 0:
                finished_process = job
                
                break

            if not job.is_alive() and job.exitcode != 0:
                print(f"SEARCH {job.name} terminated on its own with exitcode {job.exitcode}", flush=True)
                jobs.remove(job)
        
        time.sleep(0.1)

    if finished_process is None:
        print("No solution found.")
        #return False
    
    else:
        print(f"Process {finished_process.name} ({finished_process.exitcode}) finished first")
        print(f"Process {finished_process.name} ({finished_process.exitcode}) finished first", file=sys.stderr)
        #index = recur_sizes[jobs.index(finished_process)]

        size, output1, output2 = shared_data[0]
        print(f"size: {size}")
        print(f"size: {size}", file=sys.stderr)

        #except KeyboardInterrupt:
        #print(f"Interrupted, terminating spawned processes.", flush=True)
        #manager.shutdown()
        #ecode = 130


    #Terminate remaining processes
    for job in jobs:
        if job.is_alive():
            print(f"Attempting to terminate {job.name}", flush=True)
            #time.sleep(1)
            job.terminate()
            job.join()
            print(f"Process {job.name} ({job.exitcode}) terminated", flush=True)

    return finished_process is not None

        
def work_single(gadget: Gadget, sp_recur_size: int, sp_links=None, timeout=None, name=None):
    links = sp_links
    smt_total_time = None
    if sp_links is None:
        smt_start_time = time.time()
        rsat, solver = check_convergence(gadget)
        smt_end_time = time.time()

        smt_total_time = round(smt_end_time-smt_start_time, 3)

        if rsat == sat:
            print(f"{gadget.name} converges.")
            return True, set(), sp_recur_size, smt_total_time, None

        print(f"{gadget.name} diverges.")
        print()
        print(f"Computing links leading to divergence:")

        links = get_sp_links(solver) if sp_links is None else sp_links
        print(links, flush=True)


    manager = mp.Manager()
    shared_data = manager.list()


    p = mp.Process(target=maude_search, args=((gadget, links, sp_recur_size, shared_data)), name=f"SEARCH {sp_recur_size}")
    maude_start_time = time.time()
    p.start()
    
    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=timeout) if timeout is not None else None

    result = False
    while p.is_alive() and (timeout is None or datetime.now() < end_time):
        p.join(0.1)

    maude_end_time = time.time()
    maude_total_time = round(maude_end_time - maude_start_time, 3)
    
    if p.is_alive():
        p.terminate()
        result = None

    return result, links, sp_recur_size, smt_total_time, maude_total_time
    

