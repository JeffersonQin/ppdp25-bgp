### Setup

Clone the repository using 

`git clone https://github.com/JeffersonQin/ppdp25-bgp.git`

Change directory:

`cd ppdp25-bgp`

Create a virtual environment using 

`python3 -m venv .venv`

If on Windows/Powershell activate virtual environment using:

`.venv\Scripts\Activate.ps1`

If on Windows/CMD activate virtual environment using:

`.venv\Scripts\activate.bat`

If on Posix/bash activate virtual environment using:

`source .venv/bin/activate`

Install packages using:

`python3 -m pip install -r requirements.txt`



### Experiments

Scripts for running the experiments are located in experiments/
There are scripts that will run a single experiment in the form `{type}_{test_gadget}.py` or `{type}_{test_gadget}_{size}.py`
Where: 
`type` is the operator used to create the gadget: base, rooted, or nested 
`test_gadget` is one of the gadgets: Good Gadget, Naughty Gadget, or Disagree Gadget
`size` is the number of gadgets used in the combined gadget for the experiment

Combined gadgets (when `type` is rooted or nested) use `size-1` Good Gadgets and 1 `test_gadget` in their construction
When the `type` is base the size is equal to 1 and just the `test_gadget` itself is used in the experiment

There are also scripts to run the experiments in bulk: `bulk_base.py`, `bulk_rooted.py`, and `bulk_nested.py`
Each script will run all the experiments for the corresponding type.

For example running:

`python3 experiments/rooted_disagree_5.py`

will run the experiment for a rooted combination on 4 Good Gadgets and 1 Disagree Gadget.

Running:

`python3 experiments/bulk_base.py`

will run all the experiments for the base type, corresponding to the 3 gadgets; Good Gadget, Naughty Gadget, and Disagree Gadget.







