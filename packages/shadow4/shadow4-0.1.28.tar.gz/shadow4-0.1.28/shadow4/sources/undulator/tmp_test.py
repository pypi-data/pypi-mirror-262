
# electron beam
from shadow4.sources.s4_electron_beam import S4ElectronBeam
electron_beam = S4ElectronBeam(energy_in_GeV=6,energy_spread=0.001,current=0.2)
electron_beam.set_sigmas_all(sigma_x=0,sigma_y=0,sigma_xp=0,sigma_yp=0)

# magnetic structure
from shadow4.sources.undulator.s4_undulator import S4Undulator
source = S4Undulator(
    K_vertical        = 1.341095, # syned Undulator parameter
    period_length     = 0.018, # syned Undulator parameter
    number_of_periods = 111.111, # syned Undulator parameter
    emin              = 90000.01790320012, # Photon energy scan from energy (in eV)
    emax              = 90000.01790320012, # Photon energy scan to energy (in eV)
    ng_e              = 1, # Photon energy scan number of points
    maxangle          = 5.432721424879363e-06, # Maximum radiation semiaperture in RADIANS
    ng_t              = 71, # Number of points in angle theta
    ng_p              = 11, # Number of points in angle phi
    ng_j              = 20, # Number of points in electron trajectory (per period) for internal calculation only
    code_undul_phot   = 'internal', # internal, pysru, srw
    flag_emittance    = 0, # when sampling rays: Use emittance (0=No, 1=Yes)
    flag_size         = 2, # when sampling rays: 0=point,1=Gaussian,2=FT(Divergences)
    distance          = 100.0, # distance to far field plane
    srw_range         = 0.05, # for SRW backpropagation, the range factor
    srw_resolution    = 50, # for SRW backpropagation, the resolution factor
    srw_semianalytical= 0, # for SRW backpropagation, use semianalytical treatement of phase
    magnification     = 0.025, # for internal/wofry backpropagation, the magnification factor
    flag_backprop_recalculate_source      = 1, # for internal or pysru/wofry backpropagation: source reused (0) or recalculated (1)
    flag_backprop_weight = 1, # for internal or pysru/wofry backpropagation: apply Gaussian weight to amplitudes
    weight_ratio         = 0.5, # for flag_backprop_recalculate_source=1, the ratio value sigma/window halfwidth
    flag_energy_spread   = 1, # for monochromatod sources, apply (1) or not (0) electron energy spread correction
    )


# light source
from shadow4.sources.undulator.s4_undulator_light_source import S4UndulatorLightSource
light_source = S4UndulatorLightSource(name='undulator', electron_beam=electron_beam, magnetic_structure=source,nrays=50000,seed=5676561)
beam = light_source.get_beam()

# test plot
from srxraylib.plot.gol import plot_scatter
rays = beam.get_rays()
plot_scatter(1e6 * rays[:, 0], 1e6 * rays[:, 2], title='(X,Z) in microns', show=0)

print(light_source.info())
# test plot
from srxraylib.plot.gol import plot_scatter
rays = beam.get_rays()
plot_scatter(1e6 * rays[:, 3], 1e6 * rays[:, 5], title='(Xp,Zp) ')