from pumapy.material_properties.volume_fraction import compute_volume_fraction
from pumapy.physics_models.utils.property_maps import IsotropicConductivityMap
from pumapy.physics_models.finite_volume.isotropic_conductivity import IsotropicConductivity


def compute_continuum_tortuosity(workspace, cutoff, direction, side_bc='p', prescribed_bc=None,
                                 tolerance=1e-4, maxiter=10000, solver_type='cg', display_iter=True, matrix_free=True):
    """ Compute the tortuosity modelling the local conductivity as isotropic

        :param workspace: domain
        :type workspace: pumapy.Workspace
        :param cutoff: cutoff to binarize domain specifying the void phase
        :type cutoff: (int, int)
        :param direction: direction for solve ('x','y', or 'z')
        :type direction: string
        :param side_bc: side boundary conditions (string) can be symmetric ('s'), periodic ('p') or dirichlet ('d')
        :type side_bc: string
        :param prescribed_bc: 3D array holding dirichlet BC
        :type prescribed_bc: pumapy.IsotropicConductivityBC or None
        :param tolerance: tolerance for iterative solver
        :type tolerance: float
        :param maxiter: maximum Iterations for solver
        :type maxiter: int
        :param solver_type: solver type, options: 'cg' (default), 'bicgstab', 'direct'
        :type solver_type: string
        :param display_iter: display iterations and residual
        :type display_iter: bool
        :param matrix_free: if True, then use matrix-free method
        :type matrix_free: bool
        :return: tortuosity, diffusivity, porosity, concentration field
        :rtype: ((float, float, float), float, float, numpy.ndarray)
        :Example:
        >>> import pumapy as puma
        >>> ws_fiberform = puma.import_3Dtiff(puma.path_to_example_file("200_fiberform.tif"), 1.3e-6)
        Importing ...
        >>> n_eff_x, Deff_x, poro, C_x = puma.compute_continuum_tortuosity(ws_fiberform, (0, 89), 'x', side_bc='s', tolerance=1e-4)
        Approximate memory requirement for simulation...
    """

    cond_map = IsotropicConductivityMap()
    cond_map.add_material(cutoff, 1)  # assigning void k=1

    if cutoff[0] > 0:  # assigning the solid k=0
        cond_map.add_material((0, cutoff[0]-1),0)
    cond_map.add_material((cutoff[1]+1,32000),0)

    solver = IsotropicConductivity(workspace, cond_map, direction, side_bc, prescribed_bc,
                                   tolerance, maxiter, solver_type, display_iter, matrix_free)

    solver.error_check()

    solver.log_input()
    solver.compute()
    solver.log_output()

    porosity = compute_volume_fraction(workspace, cutoff)
    eta = [divide_zero(porosity,solver.keff[0]), divide_zero(porosity, solver.keff[1]), divide_zero(porosity , solver.keff[2])]

    return eta, solver.keff, porosity, solver.T


def divide_zero(x,y):
    try:
        return x/y
    except ZeroDivisionError:
        return 0