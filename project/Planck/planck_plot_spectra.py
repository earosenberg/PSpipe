import numpy as np
import pylab as plt
from pspy import so_dict, so_spectra
import sys

d = so_dict.so_dict()
d.read_from_file(sys.argv[1])

freqs = d["freqs"]
spectra = ["TT", "TE", "TB", "ET", "BT", "EE", "EB", "BE", "BB"]

spectra_dir = "spectra"
plot_dir = "plots"

pspy_utils.create_directory(plot_dir)

pol_efficiency= {}
pol_efficiency["100"] = 0.9995
pol_efficiency["143"] = 0.999
pol_efficiency["217"] = 0.999

for freq in freqs:
    spec_name = "Planck_%sxPlanck_%s-%sx%s" % (freq, freq, "hm1", "hm2")
    file_name = "%s/spectra_%s.dat" % (spectra_dir, spec_name)
    lb, ps_dict = so_spectra.read_ps(file_name, spectra=spectra)
    
    for spec in ["TT", "TE", "EE"]:
        planck_name = "%s_%sx%s" % (spec, freq, freq)
        l, cl, error = np.loadtxt("data/planck_data/spectrum_" + planck_name + ".dat", unpack=True)
        id = np.where((lb >= l[0]) & (lb <= l[-1]))
        lb_sel = lb.copy()
        lb_sel = lb_sel[id]

        if spec == "TE":
            Db_dict["TE"] = (Db_dict["TE"] + Db_dict["ET"]) / 2
            Db_dict["TE"] *= pol_efficiency[freq]
    
        if spec == "EE":
            Db_dict["EE"] *= pol_efficiency[freq]**2
        
        Db_dict[spec] = Db_dict[spec][id]

        plt.figure(figsize=(14, 7))
        plt.subplot(2, 1, 1)
        plt.errorbar(lb_sel, ps_dict[spec]*lb_sel**2/(2*np.pi), label="planck pspy %s GHz" % freq, color="black")
        plt.errorbar(l, cl*l**2/(2*np.pi), error*l**2/(2*np.pi), fmt=".", label="planck %s GHz" % freq, color="red")
        plt.xlabel(r"$\ell$", fontsize=22)
        plt.ylabel(r"$\ell^2 C_\ell/(2 \pi)$", fontsize=22)
        plt.legend()
        plt.subplot(2, 1, 2)
        plt.plot(lb_sel, lb_sel*0, color="black")
        plt.errorbar(lb_sel, (ps_dict[spec]-cl)/error, label="frac %s" % freq, color="red")
        plt.xlabel(r"$\ell$", fontsize=22)
        plt.ylabel(r"$\Delta C_\ell/\sigma_{\ell} $", fontsize=22)
        plt.ylim(-0.5, 0.5)
        plt.legend()
        plt.savefig("%s/redo_planck_%s_%s.png"%(plot_dir,spec,freq))
        plt.clf()
        plt.close()


