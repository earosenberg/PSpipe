"""
This script computes the mode coupling matrices and the binning matrices Bbl
for the different surveys and arrays
"""

from pspy import so_map, so_mcm, pspy_utils, so_dict
import sys

d = so_dict.so_dict()
d.read_from_file(sys.argv[1])

window_dir = "windows"
mcm_dir = "mcms"
plot_dir = "plots/windows/"

pspy_utils.create_directory(mcm_dir)
pspy_utils.create_directory(window_dir)
pspy_utils.create_directory(plot_dir)

surveys = d["surveys"]
lmax = d["lmax"]

print("Computing mode coupling matrices:")

for id_sv1, sv1 in enumerate(surveys):
    arrays_1 = d["arrays_%s" % sv1]
    
    for id_ar1, ar1 in enumerate(arrays_1):
        l, bl1 = pspy_utils.read_beam_file(d["beam_%s_%s" % (sv1, ar1)])
        
        win1_T = so_map.read_map(d["window_T_%s_%s" % (sv1, ar1)])
        win1_pol = so_map.read_map(d["window_pol_%s_%s" % (sv1, ar1)])
        
        win1_T.write_map("%s/window_T_%s_%s.fits" % (window_dir, sv1, ar1))
        win1_T.plot(file_name="%s/window_T_%s_%s" % (plot_dir, sv1, ar1))
        win1_pol.write_map("%s/window_pol_%s_%s.fits" % (window_dir, sv1, ar1))
        win1_pol.plot(file_name="%s/window_pol_%s_%s" % (plot_dir, sv1, ar1))

        for id_sv2, sv2 in enumerate(surveys):
            arrays_2 = d["arrays_%s" % sv2]
            
            for id_ar2, ar2 in enumerate(arrays_2):
                # This ensures that we do not repeat redundant computations
                
                if  (id_sv1 == id_sv2) & (id_ar1 > id_ar2) : continue
                if  (id_sv1 > id_sv2) : continue
                
                print("%s_%s x %s_%s" % (sv1, ar1, sv2, ar2))
                l, bl2 = pspy_utils.read_beam_file(d["beam_%s_%s" % (sv2, ar2)])
                win2_T = so_map.read_map(d["window_T_%s_%s" % (sv2, ar2)])
                win2_pol = so_map.read_map(d["window_pol_%s_%s" % (sv2, ar2)])

                mbb_inv, Bbl = so_mcm.mcm_and_bbl_spin0and2(win1=(win1_T, win1_pol),
                                                            win2=(win2_T, win2_pol),
                                                            bl1=(bl1, bl1),
                                                            bl2=(bl2, bl2),
                                                            binning_file=d["binning_file"],
                                                            niter=d["niter"],
                                                            lmax=d["lmax"],
                                                            type=d["type"],
                                                            save_file="%s/%s_%sx%s_%s"%(mcm_dir, sv1, ar1, sv2, ar2))



