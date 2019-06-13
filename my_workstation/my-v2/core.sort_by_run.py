from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
###############
from local.core import L

# ### Sorting objects from before/after
# %% markdown
# Transforms and callbacks will have run_after/run_before attributes,
# this function will sort them to respect those requirements
# (if it's possible). Also, sometimes we want a tranform/callback to be run
# at the end, but still be able to use run_after/run_before behaviors.
# For those, the function checks for a toward_end attribute
# (that needs to be True).



def _is_instance(f, gs):
    """
    oneliner:
    whether `f` is an instance to or the same to any of `gs`.

    purpose:
    1. yes, we have `isinstance(o, cls)` to check on class and instance
        1.1 but it requies both instance and class available to work
        1.2 what if we only have a list of objects and funcs instead `cls`
    2. also it leaves out the case `test_eq(o, p)`,
        2.1 sometimes we need to check whether `o` and `p` are same type
        2.2 or the same func,
    3. why not have both above dealt with a single func?
        3.1 loop through the list of objects/funcs
        3.2 and distinguish them to be either (type, 'function') or class
        3.3 put them into a list and loop through the list
        3.4 check whether `f` is instance of or just equal to `g`, each item in the list `tst`
    4. return: T or F
        4.1 as long as one `g` match with (instance or equal) `f`, return True
        4.2 otherwise, False
    """
    tst = [g if type(g) in [type, 'function'] else g.__class__ for g in gs]
    for g in tst:
        if isinstance(f, g) or f==g: return True
    return False


def _is_first(f, gs):
    """
    oneliner:
    1. whether `f` is the first func to run among `gs` (a list of funcs)
    2. based on `run_after` and `run_before` of `gs`

    purpose:
    1. among many tranform funcs, it is important to figure out which run first
    2. each func may have attributes like `run_after`, `run_before` to order
    3. how can we figure out which func is first with their attributes above?
        3.1 if `f` run_after `o`, and `o` is among `gs`, then `f` can't be first
        3.2 say `g` run before `o`, and `f` _is_instance to `o`,
                then `f` can't be first.
        3.3 otherwise, yes, `f` is first
    """
    for o in L(getattr(f, 'run_after', None)):
        if _is_instance(o, gs): return False
    for g in gs:
        if _is_instance(f, L(getattr(g, 'run_before', None))): return False
    return True


###################
# `sort_by_run(fs)`
# = rank funcs into a list based on their execution order
# logic:
    # `end` = index of `gs` which has `toward_end` attribute
    # `inp, res` = the full fs, and empty list
    # loop through all funcs, test which is the first func
    # get the first func into `res` the list

def sort_by_run(fs):
    """
    oneliner:
    1. sort `fs` from first to last to run
    2. based on their attrs such as `toward_end`, `run_after`, `run_before`

    purpose:
    1. `_is_instance`, `_is_first` help us figure out whether `f` is first among `fs`
    2. but in the end we want `fs` to be sorted by execution order
    3. `sort_by_run` does it for us
        3.1 'toward_end' help us find the last func in `fs`, put it at the end of `inp`, keep the rest funcs before it.
        3.2 loop through the rest funcs `inp`, use `_is_first` to find the actual first func to run, and pop it out of `inp`, and into `res`
        3.3 again loop through the remaining funcs `inp`, and do the previous step, until `inp` is empty
    4. return res
    """
    end = L(getattr(f, 'toward_end', False) for f in fs)
    inp,res = L(fs)[~end] + L(fs)[end], []
    while len(inp) > 0:
        for i,o in enumerate(inp):
            if _is_first(o, inp):
                res.append(inp.pop(i))
                break
        else: raise Exception("Impossible to sort")
    return res

show_doc(sort_by_run)
class Tst(): pass
class Tst1():
    run_before=[Tst]
class Tst2():
    run_before=Tst
    run_after=Tst1
tsts = [Tst(), Tst1(), Tst2()]
sort_by_run(tsts)
test_eq(sort_by_run(tsts), [tsts[1], tsts[2], tsts[0]])

# the following contradict with `Tst1.run_before=[Tst]``
Tst2.run_before,Tst2.run_after = Tst1,Tst
test_fail(lambda: sort_by_run([Tst(), Tst1(), Tst2()]))

def tst1(x): return x
tst1.run_before = Tst
test_eq(sort_by_run([tsts[0], tst1]), [tst1, tsts[0]])

# how position, run_before, toward_end work together
class Tst1():
    toward_end=True
class Tst2():
    toward_end=True
    run_before=Tst1
tsts = [Tst(), Tst1(), Tst2()]
test_eq(sort_by_run(tsts), [tsts[0], tsts[2], tsts[1]])
