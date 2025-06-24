from exp_import import *

if __name__ == "__main__":
    size = 3
    gadgets = [DISAGREE_GADGET] + (size - 1) * [GOOD_GADGET] 
    run_nested_experiment(*gadgets)