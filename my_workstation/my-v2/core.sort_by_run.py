from local.test import *
from local.imports import *
from local.notebook.showdoc import show_doc
###############
from local.core import L

# ### Sorting objects from before/after
# %% markdown
# Transforms and callbacks will have run_after/run_before attributes, this function will sort them to respect those requirements (if it's possible). Also, sometimes we want a tranform/callback to be run at the end, but still be able to use run_after/run_before behaviors. For those, the function checks for a toward_end attribute (that needs to be True).

####################
# = check if `f` is an instance of any `g` from `gs`

def _is_instance(f, gs):
    tst = [g if type(g) in [type, 'function'] else g.__class__ for g in gs]
    for g in tst:
        if isinstance(f, g) or f==g: return True
    return False

#####################
# `_is_first(f, gs)`
# > if `f.run_after` is an instance of any g in gs, or
# > if `f` is an instance of any `g.run_before`,
# > then `f` is not first to `gs`

def _is_first(f, gs):
    for o in L(getattr(f, 'run_after', None)):
        if _is_instance(o, gs): return False
    for g in gs:
        if _is_instance(f, L(getattr(g, 'run_before', None))): return False
    return True


###################
# `sort_by_run(fs)`
# = rank funcs into a list based on their execution order

def sort_by_run(fs):
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
test_eq(sort_by_run(tsts), [tsts[1], tsts[2], tsts[0]])

# the following contradict with `Tst1.run_before=[Tst]``
Tst2.run_before,Tst2.run_after = Tst1,Tst
sort_by_run([Tst(), Tst1(), Tst2()])

# nb
test_fail(lambda: sort_by_run([Tst(), Tst1(), Tst2()]))

def tst1(x): return x
tst1.run_before = Tst
test_eq(sort_by_run([tsts[0], tst1]), [tst1, tsts[0]])

class Tst1():
    toward_end=True
class Tst2():
    toward_end=True
    run_before=Tst1
tsts = [Tst(), Tst1(), Tst2()]
test_eq(sort_by_run(tsts), [tsts[0], tsts[2], tsts[1]])
