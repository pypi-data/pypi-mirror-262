#
# SHADOW3 Undulator preprocessors implemented in python
#
# this code replaces SHADOW3's undul_phot
#
# It calculates the undulator radiation as a function of energy, theta and phi. Phi is the polar angle.
#
# It uses SRW
#
# Available public functions:
#
#     undul_phot()   : like undul_phot of SHADOW but using SRW
#
#

# needed by srw

import array

try:
    import oasys_srw.srwlib as sl
except:
    try:
        import srwlib as sl
    except:
        raise ImportError("SRW not imported")


import numpy
import sys
from scipy import interpolate



def _srw_electron_beam(x=0., y=0., z=0., xp=0., yp=0., e=6.04, Iavg=0.2,
                       sigX=345e-6*1.e-20, sigY=23e-6*1.e-20, mixX=0.0, mixY=0.0,
                       sigXp=4.e-9*1.e-20/345e-6, sigYp=4.e-11*1.e-20/23e-6, sigE = 1.e-4):
  el_rest = 0.51099890221e-03
  eBeam = sl.SRWLPartBeam()
  eBeam.Iavg = Iavg
  eBeam.partStatMom1.x     =  x
  eBeam.partStatMom1.y     =  y
  eBeam.partStatMom1.z     =  z
  eBeam.partStatMom1.xp    =  xp
  eBeam.partStatMom1.yp    =  yp
  eBeam.partStatMom1.gamma =  e / el_rest
  eBeam.partStatMom1.relE0 =  1.0
  eBeam.partStatMom1.nq    = -1
  eBeam.arStatMom2[ 0] = sigX**2  #from here it is not necessary for Single Electron calculation, obviously....
  eBeam.arStatMom2[ 1] = mixX
  eBeam.arStatMom2[ 2] = sigXp**2
  eBeam.arStatMom2[ 3] = sigY**2
  eBeam.arStatMom2[ 4] = mixY
  eBeam.arStatMom2[ 5] = sigYp**2
  eBeam.arStatMom2[10] = sigE**2
  return eBeam

def _srw_drift_electron_beam(eBeam, und ):
  if isinstance(und, float):
    length = und
  elif isinstance(und, sl.SRWLMagFldU):    # Always defined in (0., 0., 0.) move the electron beam before the magnetic field.
    length = 0.0 - 0.55 * und.nPer * und.per - eBeam.partStatMom1.z
  elif isinstance(und, sl.SRWLMagFldC):
    if isinstance(und.arMagFld[0], sl.SRWLMagFldU):
      length = und.arZc[0] - 0.55 * und.arMagFld[0].nPer * und.arMagFld[0].per - eBeam.partStatMom1.z
    else: raise NameError
  else: raise NameError
  eBeam.partStatMom1.z += length
  eBeam.arStatMom2[0]  += 2 * length * eBeam.arStatMom2[1] + length**2 * eBeam.arStatMom2[2]
  eBeam.arStatMom2[1]  += length * eBeam.arStatMom2[2]
  eBeam.arStatMom2[3]  += 2 * length * eBeam.arStatMom2[4] + length**2 * eBeam.arStatMom2[5]
  eBeam.arStatMom2[4]  += length * eBeam.arStatMom2[5]
  eBeam.moved = length
  return eBeam

def _srw_simple_undulator(nPer=72, per=0.0228, B=0.120215, n=1, h_or_v='v'):
  harmB = sl.SRWLMagFldH(n, h_or_v, B)
  und = sl.SRWLMagFldU([harmB], per, nPer)
  return und

def _srw_undulators(und, Xc, Yc, Zc):#for the moment only one works
  cnt = sl.SRWLMagFldC([und], array.array('d', [Xc]), array.array('d', [Yc]), array.array('d', [Zc]))
  return cnt

def _srw_default_mesh():
    return sl.SRWLRadMesh(14718.4, 14718.4, 1, -15.e-6*50, 15e-6*50, 81, -15e-6*50, 15e-6*50, 81, 50.)

def _srw_default_mesh_bis():
    return sl.SRWLRadMesh(14718.4-1, 14718.4+1., 101, -15.e-6*50*3, 15e-6*50*3, 61, -15e-6*50*3, 15e-6*50*3, 61, 50.)

def _srw_single_electron_source(eBeam,
                                cnt,
                                mesh=None,
                                params=[1, 0.01, 0., 0., 20000, 1, 0],  # params: arPrecPar = [meth, relPrec,
                                                                        # zStartInteg, zEndInteg,
                                                                        # npTraj, useTermin, sampFactNxNyForProp]
                                ):

  if mesh is None:
      mesh = _srw_default_mesh_bis()
  wfr = sl.SRWLWfr()
  wfr.mesh = mesh
  wfr.partBeam = eBeam
  wfr.allocate(mesh.ne, mesh.nx, mesh.ny)
  eBeam = _srw_drift_electron_beam(eBeam, cnt)
  #srwl.CalcElecFieldSR(wfr1, partTraj, magFldCnt, arPrecPar)
  sl.srwl.CalcElecFieldSR(wfr, 0, cnt, params)
  stk = sl.SRWLStokes()
  stk.mesh = mesh
  stk.allocate(mesh.ne, mesh.nx, mesh.ny)
  eBeam = _srw_drift_electron_beam(eBeam, -eBeam.moved)
  wfr.calc_stokes(stk)
  return stk, eBeam

def _srw_multi_electron_source(eBeam,
                               und,
                               mesh=None,
                               params=[1, 9, 1.5, 1.5, 2]):
  if mesh is None:
      mesh = _srw_default_mesh()
  stk = sl.SRWLStokes()
  stk.mesh = mesh
  stk.allocate(mesh.ne, mesh.nx, mesh.ny)
  sl.srwl.CalcStokesUR(stk, eBeam, und, params)
  return stk, eBeam

def _srw_stokes0_to_arrays(stk):
  Shape = (4,stk.mesh.ny,stk.mesh.nx,stk.mesh.ne)
  data = numpy.ndarray(buffer=stk.arS, shape=Shape, dtype=stk.arS.typecode)
  data0 = data[0]
  data1 = data[1]
  x = numpy.linspace(stk.mesh.xStart, stk.mesh.xFin, stk.mesh.nx)
  y = numpy.linspace(stk.mesh.yStart, stk.mesh.yFin, stk.mesh.ny)
  e = numpy.linspace(stk.mesh.eStart, stk.mesh.eFin, stk.mesh.ne)
  Z2 = numpy.zeros((e.size, x.size, y.size))
  POL_DEG = numpy.zeros((e.size, x.size, y.size))
  for ie in range(e.size):
      for ix in range(x.size):
          for iy in range(y.size):
            Z2[ie, ix, iy] = data0[iy, ix, ie]
            # this is shadow definition, that uses POL_DEG = |Ex|/(|Ex|+|Ey|)
            Ex = numpy.sqrt(numpy.abs(0.5 * (data0[iy, ix, ie] + data1[iy, ix, ie])))
            Ey = numpy.sqrt(numpy.abs(0.5 * (data0[iy, ix, ie] - data1[iy, ix, ie])))
            POL_DEG[ie,ix,iy] = Ex / (Ex + Ey)
  return Z2, POL_DEG, e, x, y

def _srw_stokes0_to_spec(stk, fname="srw_xshundul.spec"):
  #
  # writes emission in a SPEC file (cartesian grid)
  #
  Shape = (4, stk.mesh.ny, stk.mesh.nx, stk.mesh.ne)
  data = numpy.ndarray(buffer=stk.arS, shape=Shape, dtype=stk.arS.typecode)
  data0 = data[0]
  x = numpy.linspace(stk.mesh.xStart, stk.mesh.xFin, stk.mesh.nx)
  y = numpy.linspace(stk.mesh.yStart, stk.mesh.yFin, stk.mesh.ny)
  e = numpy.linspace(stk.mesh.eStart, stk.mesh.eFin, stk.mesh.ne)
  f = open(fname,"w")
  for k in range(len(e)):
    f.write("#S %d intensity E= %f\n"%(k+1,e[k]))
    f.write("#N 3\n")
    f.write("#L X[m]  Y[m]  Intensity\n")
    for i in range(len(x)):
      for j in range(len(y)):
        f.write( "%e   %e   %e\n"%(x[i], y[j], data0[j,i,k]))
  f.close()
  sys.stdout.write('  file written: srw_xshundul.spec\n')

def _srw_interpol_object(x, y, z):
    #2d interpolation
    if numpy.iscomplex(z[0, 0]):
        tck_real = interpolate.RectBivariateSpline(x, y, numpy.real(z))
        tck_imag = interpolate.RectBivariateSpline(x, y, numpy.imag(z))
        return tck_real,tck_imag
    else:
        tck = interpolate.RectBivariateSpline(x, y, z)
        return tck

def _srw_interpol(x, y, z, x1, y1):
    #2d interpolation
    if numpy.iscomplex(z[0, 0]):
        tck_real, tck_imag = _srw_interpol_object(x, y, z)
        z1_real = tck_real(numpy.real(x1), numpy.real(y1))
        z1_imag = tck_imag(numpy.imag(x1), numpy.imag(y1))
        return (z1_real + 1j * z1_imag)
    else:
        tck = _srw_interpol_object(x, y, z)
        z1 = tck(x1, y1)
        return z1

def _undul_phot_SRW(E_ENERGY, INTENSITY, LAMBDAU, NPERIODS, K, EMIN, EMAX, NG_E, MAXANGLE, NG_T, NG_P,
                    number_of_trajectory_points=100):
    lambdau = LAMBDAU
    k = K
    e_energy = E_ENERGY
    nperiods = NPERIODS
    emin = EMIN
    emax = EMAX
    intensity = INTENSITY
    maxangle = MAXANGLE
    sx = 0.0 # h['SX']   #  do not use emittance at this stage
    sz = 0.0 # h['SZ']   #  do not use emittance at this stage
    ex = 0.0 # h['EX']   #  do not use emittance at this stage
    ez = 0.0 # h['EZ']   #  do not use emittance at this stage
    # nrays = h['NRAYS']
    nx = 2*NG_T - 1
    nz = nx
    ne = NG_E # int(ne)

    print ("lambdau = ",lambdau)
    print ("k = ",k)
    print ("e_energy = ",e_energy)
    print ("nperiods = ",nperiods)
    print ("intensity = ",intensity)
    print ("maxangle=%d rad, (%d x %d points) "%(maxangle,nx,nz))
    print ("sx = ",sx)
    print ("sz = ",sz)
    print ("ex = ",ex)
    print ("ez = ",ez)
    print ("emin =%g, emax=%g, ne=%d "%(emin,emax,ne))

    #
    # define additional parameters needed by SRW
    #
    B = k / 93.4 / lambdau
    slit_distance = 100.0
    method = "SE" # single-electron  "ME" multi-electron
    sE = 1e-9 # 0.89e-3

    #
    # prepare inputs
    #

    # convert cm to m

    # sx *= 1.0e-2
    # sz *= 1.0e-2
    # ex *= 1.0e-2
    # ez *= 1.0e-2

    if sx != 0.0:
      sxp = ex / sx
    else:
      sxp = 0.0

    if sz != 0.0:
      szp = ez / sz
    else:
      szp = 0.0

    xxp = 0.0
    zzp = 0.0

    paramSE = [1, 0.01, 0, 0, 50000, 1, 0]
    paramME = [1, 9, 1.5, 1.5, 2]

    #
    #
    if nx==1 and nz==1: paramME[4] = 1
    params = paramSE if method=="SE" else paramME

    slit_xmin = -maxangle*slit_distance
    slit_xmax =  maxangle*slit_distance
    slit_zmin = -maxangle*slit_distance
    slit_zmax =  maxangle*slit_distance

    #
    # calculations
    #
    print("nperiods: %d, lambdau: %f, B: %f)" % (nperiods, lambdau, B))

    und = _srw_simple_undulator(nperiods, lambdau, B)
    print("e=%f, Iavg=%f, sigX=%f, sigY=%f, mixX=%f, mixY=%f, sigXp=%f, sigYp=%f, sigE=%f" %
          (e_energy, intensity, sx, sz, xxp, zzp, sxp, szp, sE) )
    eBeam = _srw_electron_beam(e=e_energy, Iavg=intensity,
                               sigX=sx, sigY=sz, mixX=xxp, mixY=zzp, sigXp=sxp, sigYp=szp, sigE=sE)


    cnt = _srw_undulators(und, 0., 0., 0.)
    sys.stdout.flush()

    mesh = sl.SRWLRadMesh(emin, emax, ne, slit_xmin, slit_xmax, nx,slit_zmin, slit_zmax, nz, slit_distance)
    if (method == 'SE'):
        print ("Calculating SE...")
        stkSE, eBeam = _srw_single_electron_source(eBeam, cnt, mesh, params)
        sys.stdout.write('  done\n')
        sys.stdout.write('  saving SE Stokes...'); sys.stdout.flush()
        stk = stkSE
    else:
        print ("Calculating ME...")
        stkME, eBeam = _srw_multi_electron_source(eBeam, und) # cnt, mesh, params)
        sys.stdout.write('  done\n')
        sys.stdout.write('  saving SE Stokes...'); sys.stdout.flush()
        stk = stkME

    #
    # dump file with radiation on cartesian grid
    #
    # _srw_stokes0_to_spec(stk,fname="srw_xshundul.spec")

    #
    # interpolate for polar grid
    #

    # polar grid
    theta = numpy.linspace(0, MAXANGLE, NG_T)
    phi = numpy.linspace(0, numpy.pi / 2, NG_P)
    Z2 = numpy.zeros((NG_E, NG_T, NG_P))
    POL_DEG = numpy.zeros((NG_E, NG_T, NG_P))

    # interpolate on polar grid
    radiation, pol_deg, e, x, y = _srw_stokes0_to_arrays(stk)
    for ie in range(e.size):
      tck = _srw_interpol_object(x,y,radiation[ie])
      tck_pol_deg = _srw_interpol_object(x, y, pol_deg[ie])
      for itheta in range(theta.size):
        for iphi in range(phi.size):
          R = slit_distance / numpy.cos(theta[itheta])
          r = R * numpy.sin(theta[itheta])
          X = r * numpy.cos(phi[iphi])
          Y = r * numpy.sin(phi[iphi])
          tmp = tck(X, Y)

          #  Conversion from SRW units (photons/mm^2/0.1%bw) to SHADOW units (photons/rad^2/eV)
          tmp *= (slit_distance * 1e3)**2 # photons/mm^2 -> photons/rad^2
          tmp /= 1e-3 * e[ie] # photons/o.1%bw -> photons/eV

          Z2[ie, itheta, iphi] = tmp
          POL_DEG[ie, itheta, iphi] = tck_pol_deg(X, Y)

    # !C SHADOW defines the degree of polarization by |E| instead of |E|^2
    # !C i.e.  P = |Ex|/(|Ex|+|Ey|)   instead of   |Ex|^2/(|Ex|^2+|Ey|^2)
    # POL_DEG = numpy.sqrt(POL_DEG2)/(numpy.sqrt(POL_DEG2)+numpy.sqrt(1.0-POL_DEG2))

    # we use, however, POL_DEG = |Ex|^2/(|Ex|^2+|Ey|^2)

    return {'radiation':Z2, 'polarization':POL_DEG, 'photon_energy':e, 'theta':theta, 'phi':phi, 'trajectory':None}

def calculate_undulator_emission_SRW(
                     electron_energy              = 6.0,
                     electron_current             = 0.2,
                     undulator_period             = 0.018,
                     undulator_nperiods           = 100,
                     K                            = 1.0,
                     photon_energy                = 2000.0,
                     EMAX                         = 20000.0,
                     NG_E                         = 10,
                     MAXANGLE                     = 0.1,
                     number_of_points             = 100,
                     NG_P                         = 100,
                     number_of_trajectory_points  = 100):
    return _undul_phot_SRW(
                        electron_energy,
                        electron_current,
                        undulator_period,
                        undulator_nperiods,
                        K,
                        photon_energy,
                        EMAX,
                        NG_E,
                        MAXANGLE,
                        number_of_points,
                        NG_P,
                        number_of_trajectory_points=number_of_trajectory_points,
                        )
if __name__ == "__main__":
    dict1 = calculate_undulator_emission_SRW(
                     electron_energy              = 6.0,
                     electron_current             = 0.2,
                     undulator_period             = 0.025,
                     undulator_nperiods           = 188.0,
                     K                            = 1.681183,
                     photon_energy                = 5591.0,
                     EMAX                         = 5700.0,
                     NG_E                         = 11,
                     MAXANGLE                     = 2e-5,
                     number_of_points             = 51,
                     NG_P                         = 11,
                     number_of_trajectory_points  = 51)

    from srxraylib.plot.gol import plot_image
    plot_image(dict1['radiation'][0], dict1['theta'], dict1['phi'], aspect='auto',  title="first", show=0)
    plot_image(dict1['radiation'][-1], dict1['theta'], dict1['phi'], aspect='auto', title="last", show=1)

    plot_image(dict1['CART_radiation'][0], 1e6 * dict1['CART_x'], 1e6 * dict1['CART_y'], aspect='auto', title="first", show=0)
    plot_image(dict1['CART_radiation'][-1], 1e6 * dict1['CART_x'], 1e6 * dict1['CART_y'], aspect='auto', title="last", show=1)