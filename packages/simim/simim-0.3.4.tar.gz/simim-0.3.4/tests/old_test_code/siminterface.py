import context

import numpy as np
import matplotlib.pyplot as plt

import simim.siminterface as sim
from simim.setupsimim import create_paths
from simim.galprops.galprops import prop_li_co

def test_load():
    handler = sim.SimHandler(simname)
    print(handler.extract_snap_keys())
    print(handler.get_mass_index(1e15,99))
    print(handler.get_mass_index(1e14,99))
    print(handler.get_mass_index(1e13,99))
    print(handler.get_mass_index(1e12,99))
    print(handler.get_mass_index(1e11,99))
    print(handler.get_mass_index(1e10,99))
    print(handler.get_mass_index(1e9,99))
    print(handler.get_mass_index(1e8,99))

    print(handler.key_units)
    print("done")

def check_snap_meta():
    handler = sim.SimHandler(simname)
    for i in handler.snap_meta['index']:
        stuff = handler.extract_snap_meta(i)
        dmin = handler.cosmo.comoving_distance(stuff['redshift_min']).value*handler.h
        dmid = handler.cosmo.comoving_distance(stuff['redshift']).value*handler.h
        dmax = handler.cosmo.comoving_distance(stuff['redshift_max']).value*handler.h
        print(i,dmax,stuff['distance_max'])

def test_stats():

    handler = sim.SimHandler(simname)

    def sfrmean(sfr):
        return np.mean(sfr)
    def sfrdensity(sfr):
        return np.sum(sfr)/(handler.metadata['box_edge']/handler.h)**3

    val,z = handler.snap_stat(sfrmean,['sfr'])
    plt.plot(z,val)
    plt.show()

    val,z = handler.snap_stat(sfrdensity,['sfr'])
    plt.plot(z,val)
    plt.show()

def test_properties():
    print("\n\nDo first time:")
    handler = sim.SimHandler(simname,init_snaps=True)
    handler.make_property(prop_li_co, rename='Lco_Li', overwrite=False)

    print("\n\nDo second time + write:")
    handler = sim.SimHandler(simname,init_snaps=True)
    handler.make_property(prop_li_co, rename='Lco_Li', overwrite=False, write=True)

    print("\n\nDo third third + write + delete:")
    handler = sim.SimHandler(simname,init_snaps=True)
    handler.make_property(prop_li_co, rename='Lco_Li', overwrite=True, write=True)
    handler.delete_property('Lco_Li')

    print("\n\nDo fourth time + write + delete:")
    handler = sim.SimHandler(simname,init_snaps=True)
    handler.make_property(prop_li_co, rename='Lco_Li', overwrite=True, write=True)
    handler.delete_property('Lco_Li')


# test_illustris_download()
# test_illustris_meta()
# test_illustris_format()
# test_load()
# check_snap_meta()
# test_stats()
test_properties()
