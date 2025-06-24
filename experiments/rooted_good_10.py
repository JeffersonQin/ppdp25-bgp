from exp_import import *

if __name__ == "__main__":
    size = 10
    gadgets = (size - 1) * [GOOD_GADGET] + [GOOD_GADGET]
    run_rooted_experiment(*gadgets)