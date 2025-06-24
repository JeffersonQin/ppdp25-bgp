from exp_import import *

if __name__ == "__main__":
    size = 2
    gadgets = [NAUGHTY_GADGET] + (size - 1) * [GOOD_GADGET] 
    run_nested_experiment(*gadgets)