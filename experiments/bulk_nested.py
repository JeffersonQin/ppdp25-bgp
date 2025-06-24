from exp_import import *

if __name__ == "__main__":
    sizes = [2, 3]
    test_gadgets = [GOOD_GADGET, NAUGHTY_GADGET, DISAGREE_GADGET]

    for size in sizes:
        for test_gadget in test_gadgets:

            gadgets = [test_gadget] + (size - 1) * [GOOD_GADGET] 
            run_nested_experiment(*gadgets)