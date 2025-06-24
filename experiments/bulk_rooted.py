from exp_import import *

if __name__ == "__main__":
    sizes = [2, 5, 10, 50, 100]
    test_gadgets = [GOOD_GADGET, NAUGHTY_GADGET, DISAGREE_GADGET]

    for size in sizes:
        for test_gadget in test_gadgets:

            gadgets = (size - 1) * [GOOD_GADGET] + [test_gadget]
            run_rooted_experiment(*gadgets)