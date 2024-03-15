import matplotlib.pyplot as plt
import numpy as np

import context

import simim.lightcone as lc
from simim.galprops import galprops, sfr, co, densegas, farinfrared
from imsim.lc_props import sfr_behroozi,sfr_behroozi_plot
from imsim.lc_luminosity import lco_li, lco_lidz, lco_copss, l_delooze, l_uzgil, l_spinoglio

def check_behroozi():
    from imsim.lc_props import sfr_behroozi
    from simim.galprops.sfr import behroozi13

    x = np.array([np.logspace(8,13) for i in range(25)]).flatten()
    plt.loglog(x,sfr_behroozi(2.5,x,scatter=True),ls='',marker='.')
    plt.loglog(x,behroozi13(2.5,x),ls='',marker='.')
    plt.show()

check_behroozi()

def check_sfr():
    print(sfr.behroozi13(1,1e10,scatter=False))
    print(sfr_behroozi(1,1e10,scatter=False))

    print(sfr.tngcorrections(10,1))
    print(sfr.tngcorrections(10,2))
    print(sfr.tngcorrections(10,3))

    sfr_behroozi_plot()
    sfr.behroozi13.plot()

def test_properties():
    def masstest(mass):
        return mass

    testprop1 = galprops.prop(prop_name='Test1',
                               prop_function=masstest,
                               kwargs=['mass'],
                               give_args_in_h_units=False,
                               function_return_in_h_units=False,
                               h_dependence=-1)
    testprop2 = galprops.prop(prop_name='Test2',
                               prop_function=masstest,
                               kwargs=['mass'],
                               give_args_in_h_units=True,
                               function_return_in_h_units=False,
                               h_dependence=-1)
    testprop3 = galprops.prop(prop_name='Test3',
                               prop_function=masstest,
                               kwargs=['mass'],
                               give_args_in_h_units=True,
                               function_return_in_h_units=True,
                               h_dependence=-1)

    handler = lc.handler.lightcone('TNG100-3','test1',0)

    handler.make_property(testprop1)
    handler.make_property(testprop2)
    handler.make_property(testprop3)
    print("y value should be ~.7 times x value")
    handler.plot('Test1','Test2',axkws={'xscale':'log','yscale':'log'})
    print("y value should equal x value")
    handler.plot('Test1','Test3',axkws={'xscale':'log','yscale':'log'})


def test_luminosity():
    handler = lc.handler.lightcone('TNG100-3','test1',0)

    print(co.li16(10,scatter_lco=False),lco_li(10,scatter_lco=False,scatter_sfr=False))
    handler.make_property(galprops.prop_li_co,rename=['Li'])
    handler.make_property(galprops.prop_co_sled)
    handler.plot('Li','L10',axkws={'xscale':'log','yscale':'log'})
    handler.plot('Li','L98',axkws={'xscale':'log','yscale':'log'})

    # print(co.lidz11(1e10,rand_f_duty=False),lco_lidz(1e10,rand_f_duty=False))
    # handler.make_property(galprops.prop_lidz_co,rename=['Lidz'])
    #
    # handler.make_property(galprops.prop_pullen_co,rename=['Pullen'])
    #
    # print(co.keating16(1e10,scatter_lco=False),lco_copss(np.array([1e10],ndmin=1),scatter=False))
    # handler.make_property(galprops.prop_keating_co,rename=['Keating'])
    #
    # handler.plot('Li','Lidz',axkws={'xscale':'log','yscale':'log'})
    # handler.plot('Li','Pullen',axkws={'xscale':'log','yscale':'log'})
    # handler.plot('Li','Keating',axkws={'xscale':'log','yscale':'log'})
    #
    # handler.make_property(galprops.prop_gao_hcn,rename=['Gao'])
    # handler.make_property(galprops.prop_breysse_hcn,rename=['Breysse'])
    # handler.plot('Gao','Breysse',axkws={'xscale':'log','yscale':'log'})
    #
    # print(farinfrared.delooze14(10**5,scatter=False))
    # print(farinfrared.delooze14(10,scatter=False),l_delooze(10,scatter=False,scatter_sfr=False))
    # print(farinfrared.uzgil14(10,scatter=False),l_uzgil(10,scatter=False,scatter_sfr=False))
    # print(farinfrared.spinoglio12(10,scatter=False),l_spinoglio(10,scatter=False,scatter_sfr=False))
    # handler.make_property(galprops.prop_delooze_cii,rename=['Delooze'])
    # handler.make_property(galprops.prop_uzgil_cii,rename=['Uzgil'])
    # handler.make_property(galprops.prop_spinoglio_cii,rename=['Spinoglio'])
    # handler.plot('Delooze','sfr',axkws={'xscale':'log','yscale':'log'})
    # handler.plot('Delooze','Uzgil',axkws={'xscale':'log','yscale':'log'})
    # handler.plot('Delooze','Spinoglio',axkws={'xscale':'log','yscale':'log'})


# check_sfr()
# test_properties()
# test_luminosity()
