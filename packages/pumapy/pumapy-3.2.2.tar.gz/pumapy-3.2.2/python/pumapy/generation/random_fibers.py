"""
The following function was copied and modified from the porespy project (distributed under the MIT License).
See https://github.com/PMEAL/porespy/blob/dev/porespy/generators/_imgen.py for more information.
See https://github.com/PMEAL/porespy/blob/dev/LICENSE for the license.
"""

from scipy.ndimage import distance_transform_edt as edt
from skimage.segmentation import watershed
import numpy as np
from pumapy.utilities.workspace import Workspace
from pumapy.utilities.logger import print_warning
from pumapy.filters.filters import filter_gaussian
import sys


def generate_random_fibers_isotropic(shape, radius, nfibers=None, porosity=None, length=None, max_iter=5,
                                     allow_intersect=True, segmented=True):
    """ Generates random isotropic fibers from number of fibers or porosity

        :param shape: the shape of the workspace to generate in (Nx, Ny, Nz) where N is the number of voxels.
        :type shape: (int, int, int)
        :param radius: the radius of the fibers in voxels
        :type radius: int
        :param nfibers: the number of fibers to add to the domain. Adjust this value to control the final porosity,
            which is not easily specified since cylinders overlap and intersect different fractions of the domain
        :type nfibers: int or None
        :param porosity: the target value for the porosity of the generated mat. The function uses an
            algorithm for predicting the number of required number of cylinder, and refines this over a certain number of
            fractional insertions (according to the 'iterations' input)
        :type porosity: float
        :param length: the length of the cylinders to add.  If ``None`` (default) then the cylinders will extend beyond the
            domain in both directions so no ends will exist. If a scalar value is given it will be interpreted as the
            Euclidean distance between the two ends of the cylinder.  Note that one or both of the ends *may* still lie
            outside the domain, depending on the randomly chosen center point of the cylinder
        :type length: float
        :param max_iter: the number of fractional fiber insertions used to target the requested porosity. By default a
            value of 3 is used (and this is typically effective in getting very close to the targeted porosity),
            but a greater number can be input to improve the achieved porosity
        :type max_iter: int
        :param allow_intersect: allow intersection betweem the fibers
        :type allow_intersect: bool
        :param segmented: return a domain that is already segmented (i.e. each fiber with unique ID) or
            with grayscales 0-255 with threshold=128 for the input diameter
        :type segmented: bool
        :return: random fibers domain
        :rtype: Workspace

        :Example:
        >>> import pumapy as puma
        >>> # specify porosity
        >>> ws_fibers = puma.generate_random_fibers_isotropic(shape=(100, 100, 100), radius=4, porosity=0.8, length=200, allow_intersect=True, segmented=True)
        Fibers created...
        >>> # puma.render_volume(ws_fibers, cutoff=(1, ws_fibers.max()), cmap='jet')  # to visualize it
        >>> # puma.render_orientation(ws_fibers)
        >>>
        >>> # specify number of fibers
        >>> ws_fibers = puma.generate_random_fibers_isotropic(shape=(100, 100, 100), radius=4, nfibers=100, length=200, allow_intersect=True, segmented=False)
        Fibers created...
        >>> # puma.render_volume(ws_fibers, cutoff=(1, ws_fibers.max()), cmap='jet')  # to visualize it
        >>> # puma.render_orientation(ws_fibers)
    """
    angle_type = 0 # isotropic
    variation = 0 # arbitrary
    direction = 'x' # arbitrary

    return generate_random_fibers_helper(shape, radius, nfibers, porosity, angle_type, variation, direction, length, max_iter,
                                         allow_intersect, segmented)

def generate_random_fibers_transverseisotropic(shape, radius, nfibers=None, porosity=None, direction='z', variation=0, length=None, max_iter=5,
                                               allow_intersect=True, segmented=True):
    """ Generates random transverse isotropic fibers from number of fibers or porosity

        :param shape: the shape of the workspace to generate in (Nx, Ny, Nz) where N is the number of voxels.
        :type shape: (int, int, int)
        :param radius: the radius of the fibers in voxels
        :type radius: int
        :param nfibers: the number of fibers to add to the domain. Adjust this value to control the final porosity,
            which is not easily specified since cylinders overlap and intersect different fractions of the domain
        :type nfibers: int or None
        :param porosity: the target value for the porosity of the generated mat. The function uses an
            algorithm for predicting the number of required number of cylinder, and refines this over a certain number of
            fractional insertions (according to the 'iterations' input)
        :type porosity: float
        :param direction: Either 'x', 'y', or 'z'. The direction orthogonal to the plane of the fibers. Example: for fibers
            oreinted in XY, put 'z'
        :type direction: string
        :param variation: The angle variation in the orthogonal direction. 0 for no variation, 90 for full variation.
        :type variation: float
        :param length: the length of the cylinders to add.  If ``None`` (default) then the cylinders will extend beyond the
            domain in both directions so no ends will exist. If a scalar value is given it will be interpreted as the
            Euclidean distance between the two ends of the cylinder.  Note that one or both of the ends *may* still lie
            outside the domain, depending on the randomly chosen center point of the cylinder
        :type length: float
        :param max_iter: the number of fractional fiber insertions used to target the requested porosity. By default a
            value of 3 is used (and this is typically effective in getting very close to the targeted porosity),
            but a greater number can be input to improve the achieved porosity
        :type max_iter: int
        :param allow_intersect: allow intersection betweem the fibers
        :type allow_intersect: bool
        :param segmented: return a domain that is already segmented (i.e. each fiber with unique ID) or
            with grayscales 0-255 with threshold=128 for the input diameter
        :type segmented: bool
        :return: random fibers domain
        :rtype: Workspace

        :Example:
        >>> import pumapy as puma
        >>> # specify porosity
        >>> ws_fibers = puma.generate_random_fibers_transverseisotropic(shape=(100, 100, 100), radius=4, porosity=0.8, direction='x', variation=15, length=200, allow_intersect=True, segmented=True)
        Fibers created...
        >>> # puma.render_volume(ws_fibers, cutoff=(1, ws_fibers.max()), cmap='jet')  # to visualize it
        >>> # puma.render_orientation(ws_fibers)
        >>>
        >>> # specify number of fibers
        >>> ws_fibers = puma.generate_random_fibers_transverseisotropic(shape=(100, 100, 100), radius=4, nfibers=100, direction='y', variation=0, length=200, allow_intersect=True, segmented=False)
        Fibers created...
        >>> # puma.render_volume(ws_fibers, cutoff=(1, ws_fibers.max()), cmap='jet')  # to visualize it
        >>> # puma.render_orientation(ws_fibers)
        >>>
        >>> # don't allow intersection between fibers
        >>> ws_fibers = puma.generate_random_fibers_transverseisotropic(shape=(100, 100, 100), radius=4, porosity=0.9, direction='z', variation=30, length=200, allow_intersect=False, segmented=True)
        Fibers created...
        >>> # puma.render_volume(ws_fibers, cutoff=(1, ws_fibers.max()), cmap='jet')  # to visualize it
        >>> # puma.render_orientation(ws_fibers)
    """
    angle_type = 1 # transverse isotropic
    return generate_random_fibers_helper(shape, radius, nfibers, porosity, angle_type, variation, direction, length, max_iter,
                                         allow_intersect, segmented)

def generate_random_fibers_1D(shape, radius, nfibers=None, porosity=None, direction='z', length=None, max_iter=5,
                              allow_intersect=True, segmented=True):
    """ Generates random 1D fibers from number of fibers or porosity

        :param shape: the shape of the workspace to generate in (Nx, Ny, Nz) where N is the number of voxels.
        :type shape: (int, int, int)
        :param radius: the radius of the fibers in voxels
        :type radius: int
        :param nfibers: the number of fibers to add to the domain. Adjust this value to control the final porosity,
            which is not easily specified since cylinders overlap and intersect different fractions of the domain
        :type nfibers: int or None
        :param porosity: the target value for the porosity of the generated mat. The function uses an
            algorithm for predicting the number of required number of cylinder, and refines this over a certain number of
            fractional insertions (according to the 'iterations' input)
        :type porosity: float
        :param direction: Either 'x', 'y', or 'z'. The direction of the 1D fibers
        :type direction: string
        :param length: the length of the cylinders to add.  If ``None`` (default) then the cylinders will extend beyond the
            domain in both directions so no ends will exist. If a scalar value is given it will be interpreted as the
            Euclidean distance between the two ends of the cylinder.  Note that one or both of the ends *may* still lie
            outside the domain, depending on the randomly chosen center point of the cylinder
        :type length: float
        :param max_iter: the number of fractional fiber insertions used to target the requested porosity. By default a
            value of 3 is used (and this is typically effective in getting very close to the targeted porosity),
            but a greater number can be input to improve the achieved porosity
        :type max_iter: int
        :param allow_intersect: allow intersection betweem the fibers
        :type allow_intersect: bool
        :param segmented: return a domain that is already segmented (i.e. each fiber with unique ID) or
            with grayscales 0-255 with threshold=128 for the input diameter
        :type segmented: bool
        :return: random fibers domain
        :rtype: Workspace

        :Example:
        >>> import pumapy as puma
        >>> # specify porosity
        >>> ws_fibers = puma.generate_random_fibers_1D(shape=(100, 100, 100), radius=4, porosity=0.8, direction='x', length=200, allow_intersect=True, segmented=True)
        Fibers created...
        >>> # puma.render_volume(ws_fibers, cutoff=(1, ws_fibers.max()), cmap='jet')  # to visualize it
        >>> # puma.render_orientation(ws_fibers)
        >>>
        >>> # specify number of fibers
        >>> ws_fibers = puma.generate_random_fibers_1D(shape=(100, 100, 100), radius=4, nfibers=100, direction='y', length=200, allow_intersect=True, segmented=False)
        Fibers created...
        >>> # puma.render_volume(ws_fibers, cutoff=(1, ws_fibers.max()), cmap='jet')  # to visualize it
        >>> # puma.render_orientation(ws_fibers)
        >>>
        >>> # don't allow intersection between fibers
        >>> ws_fibers = puma.generate_random_fibers_1D(shape=(100, 100, 100), radius=4, porosity=0.9, direction='z', length=200, allow_intersect=False, segmented=True)
        Fibers created...
        >>> # puma.render_volume(ws_fibers, cutoff=(1, ws_fibers.max()), cmap='jet')  # to visualize it
        >>> # puma.render_orientation(ws_fibers)
    """
    angle_type = 2 # transverse isotropic
    variation = 0 # arbitrary
    return generate_random_fibers_helper(shape, radius, nfibers, porosity, angle_type, variation, direction, length, max_iter,
                                         allow_intersect, segmented)


def generate_random_fibers(shape, radius, nfibers=None, porosity=None, phi=90., theta=90., length=None, max_iter=5,
                           allow_intersect=True, segmented=True):
    """ Generates random fibers from number of fibers or porosity

        :param shape: the shape of the workspace to generate in (Nx, Ny, Nz) where N is the number of voxels.
        :type shape: (int, int, int)
        :param radius: the radius of the fibers in voxels
        :type radius: int
        :param nfibers: the number of fibers to add to the domain. Adjust this value to control the final porosity,
            which is not easily specified since cylinders overlap and intersect different fractions of the domain
        :type nfibers: int or None
        :param porosity: the target value for the porosity of the generated mat. The function uses an
            algorithm for predicting the number of required number of cylinder, and refines this over a certain number of
            fractional insertions (according to the 'iterations' input)
        :type porosity: float
        :param phi: a value between 0 and 90 that controls the amount that the fibers lie *out of* the XY plane,
            with 0 meaning all fibers lie in the XY plane, and 90 meaning that cylinders are randomly oriented out of the
            plane by as much as +/- 90 degrees
        :type phi: float
        :param theta: a value between 0 and 90 that controls the amount of rotation *in the* XY plane,
            with 0 meaning all fibers point in the X-direction, and 90 meaning they are randomly rotated about the
            Z axis by as much as +/- 90 degrees
        :type theta: float
        :param length: the length of the cylinders to add.  If ``None`` (default) then the cylinders will extend beyond the
            domain in both directions so no ends will exist. If a scalar value is given it will be interpreted as the
            Euclidean distance between the two ends of the cylinder.  Note that one or both of the ends *may* still lie
            outside the domain, depending on the randomly chosen center point of the cylinder
        :type length: float
        :param max_iter: the number of fractional fiber insertions used to target the requested porosity. By default a
            value of 3 is used (and this is typically effective in getting very close to the targeted porosity),
            but a greater number can be input to improve the achieved porosity
        :type max_iter: int
        :param allow_intersect: allow intersection betweem the fibers
        :type allow_intersect: bool
        :param segmented: return a domain that is already segmented (i.e. each fiber with unique ID) or
            with grayscales 0-255 with threshold=128 for the input diameter
        :type segmented: bool
        :return: random fibers domain
        :rtype: Workspace
    """

    print_warning("Deprecated API for fiber generation. New API has function calls for isotropic, transverse isotropic, and 1D fibers rather than specifying phi and theta. This function call will be removed in a future version")

    if phi == 90 and theta == 90:
        print_warning("based on phi and theta input, generating isotropic fibers")
        angle_type = 0
        variation = 0
        direction = 'x'
    elif phi == 90 and theta != 0:
        print_warning("based on phi and theta input, generating transverse isotropic fibers in XY plane, with variation of " + str(theta) + " degrees")
        angle_type = 1
        variation = theta
        direction = 'z'
    elif phi == 90 and theta == 0:
        print_warning("based on phi and theta input, generating 1d fibers in the z direction")
        angle_type = 2
        variation = 0
        direction = 'z'
    else:
        print_warning("non-standard values of phi and theta. Defaulting to isotropic fibers. Use new fiber generation API")
        angle_type = 0
        variation = 0
        direction = 'x'

    return generate_random_fibers_helper(shape, radius, nfibers, porosity, angle_type, variation, direction, length, max_iter,
                                         allow_intersect, segmented)


def generate_random_fibers_helper(shape, radius, nfibers, porosity, angle_type, variation, direction, length, max_iter,
                                  allow_intersect=True, segmented=True):
    # error checks and warnings
    if max_iter < 3:
        raise Exception("Iterations must be >= 3")
    if nfibers is None and porosity is None:
        raise Exception("'nfibers' and 'porosity' can't be both None")
    if nfibers is not None and porosity is not None:
        print_warning("'nfibers' and 'porosity' have both been provided: only nfibers used.")

    # logging
    ws = Workspace()
    ws.log.log_section("Generating Random Fiber Domain")
    ws.log.log_value("Domain Shape: ", shape)
    ws.log.log_value("Fiber radius: ", radius)
    ws.log.log_line(f"Porosity: {porosity}" if nfibers is None else f"Number of fibers: {nfibers}")
    ws.log.log_line(f"Angle Type: ({angle_type})")
    ws.log.log_line(f"Angle Variation: ({variation})")
    ws.log.log_line(f"Direction: ({direction})")
    ws.log.log_line(f"Fiber length: {length}")
    ws.log.log_line(f"Allow intersections: {allow_intersect}")
    ws.log.write_log()

    ids_orient_dict = {}
    fiber_count = 0

    img = np.zeros(shape, dtype=int)

    # run solver for provided number of fibers
    if nfibers is not None:
        if allow_intersect:
            img, _ = _generate_fibers(shape=shape, radius=radius, nfibers=nfibers, n_fibers_total=nfibers,
                                      fiber_count=fiber_count, ids_orient_dict=ids_orient_dict,
                                      allow_intersect=allow_intersect, angle_type=angle_type, variation=variation, direction=direction, length=length)
        else:
            _generate_fibers(shape=shape, radius=radius, nfibers=nfibers, n_fibers_total=nfibers,
                             fiber_count=fiber_count, ids_orient_dict=ids_orient_dict,
                             allow_intersect=allow_intersect, angle_type=angle_type, variation=variation, direction=direction, length=length, existing_img=img)

    else:  # porosity provided
        vol_total = float(np.prod(shape))

        length_estimate = vol_total ** (1 / 3) if length is None else length

        vol_fiber = length_estimate * np.pi * radius * radius
        n_pixels_to_add = -np.log(porosity) * vol_total

        subdif = 0.8 / np.sum(np.arange(1, max_iter) ** 2)
        fractions = [0.2]
        for i in range(1, max_iter):
            fractions.append(fractions[i - 1] + (max_iter - i) ** 2 * subdif)

        img = np.zeros(shape, dtype=int)
        current_porosity = 1.
        for i, frac in enumerate(fractions):
            n_fibers_total = n_pixels_to_add / vol_fiber
            n_fibers = int(np.ceil(frac * n_fibers_total) - fiber_count)
            if current_porosity < porosity:
                break

            if allow_intersect:
                new_fibers, mask = _generate_fibers(shape, radius, nfibers=n_fibers, n_fibers_total=int(round(n_fibers_total)),
                                                    fiber_count=fiber_count, ids_orient_dict=ids_orient_dict, allow_intersect=allow_intersect,
                                                    angle_type=angle_type, variation=variation, direction=direction, length=length)
                new_fibers = new_fibers[mask]
                img[mask] = new_fibers
            else:
                _generate_fibers(shape, radius, nfibers=n_fibers,
                                 n_fibers_total=int(round(n_fibers_total)),
                                 fiber_count=fiber_count, ids_orient_dict=ids_orient_dict,
                                 allow_intersect=allow_intersect,
                                 angle_type=angle_type, variation=variation, direction=direction, length=length, existing_img=img)

            fiber_count = np.unique(img).shape[0]

            if i != max_iter - 1:  # update target for next iteration
                porosity = np.sum(img == 0) / img.size
                vol_added = -np.log(porosity) * vol_total
                vol_fiber = vol_added / fiber_count

    ws.matrix = img.astype(np.uint16)

    print("\nAssigning orientations ... ", end='')
    k = np.array(list(ids_orient_dict.keys()))
    v = np.array(list(ids_orient_dict.values()))
    mapping_ar = np.zeros((k.max() + 1, 3), dtype=v.dtype)
    mapping_ar[k] = v
    ws.orientation = mapping_ar[ws.matrix]
    print("Done")

    if not segmented:  # add grayscale gradients with Gaussian
        ws.binarize(1)
        ws.matrix *= 255
        filter_gaussian(ws, sigma=int(round((radius//2-1))))
        porosity = ws.porosity(cutoff=(0, 127))
    else:
        porosity = ws.porosity()
    print("Generated random fibers domain with porosity: {}".format(porosity))
    ws.log.log_section("Finished Random Fiber Generation")
    ws.log.write_log()
    return ws


def _generate_fibers(shape, radius, nfibers, n_fibers_total, fiber_count, ids_orient_dict, allow_intersect,
                     angle_type, variation, direction, length=None, existing_img=None):
    """ Generates random fibers given nfibers"""

    # error checks
    shape = np.array(shape)
    if np.size(shape) == 1:
        shape = np.full((3, ), int(shape))
    elif np.size(shape) == 2:
        raise Exception("Shape can only be 3D")

    H = np.sqrt(np.sum(np.square(shape))).astype(int)
    if length is None:
        length = 2 * H
    R = min(int(length / 2), 2 * H)

    if (angle_type < 0) or (angle_type > 2):
        raise Exception('angle type must be 0 (isotropic) , 1 (transverse isotropic), or 2 (1D fibers)')
    if (variation > 90) or (variation < 0):
        raise Exception('angle variation for transverse isotropic fibers must be between 0 and 90')
    if not ( direction == 'x' or direction == 'y' or direction == 'z'):
        raise Exception('direction must be either x, y, or z')

    n = 0  # current iteration number of fibers
    L = min(H, R)

    if not allow_intersect:
        mask = np.ones(shape, dtype=bool)
    else:
        im = np.zeros(shape, dtype=int)

    # maximum unsuccessful attempts of inserting a fiber
    max_attempts = 100000
    attempt_num = 0

    while n < nfibers:

        if attempt_num > max_attempts:
            raise Exception(f"While loop did not converge after {max_attempts} iterations.")
        else:
            attempt_num += 1

        x = np.random.rand(3) * (shape + 2 * L)

        if angle_type == 0: # isotropic
            theta_rand = np.random.rand() * 2 * np.pi
            phi_rand = np.arccos(1. - 2. * np.random.rand())
            unit_vector = np.array([np.sin(phi_rand) * np.cos(theta_rand),
                                    np.sin(phi_rand) * np.sin(theta_rand),
                                    np.cos(phi_rand)])
        elif angle_type == 1: # transverse isotropic
            theta_rand = np.random.rand() * 2 * np.pi

            if variation <= 0.5:
                phi_rand = np.pi / 2.
            else:
                phi_rand = np.arccos(1. - 2. * np.random.rand())
                while np.abs( np.pi / 2. - phi_rand ) > variation * np.pi / 180. :
                    phi_rand = np.arccos(1. - 2. * np.random.rand())

            temp_vector = np.array([np.sin(phi_rand) * np.cos(theta_rand),
                                    np.sin(phi_rand) * np.sin(theta_rand),
                                    np.cos(phi_rand)])

            if direction == 'x':
                unit_vector = np.array([temp_vector[2], temp_vector[1], temp_vector[0]])
            elif direction == 'y':
                unit_vector = np.array([temp_vector[0], temp_vector[2], temp_vector[1]])
            else:
                unit_vector = np.array([temp_vector[0], temp_vector[1], temp_vector[2]])

        elif angle_type == 2: # 1D
            if direction == 'x':
                unit_vector = np.array([1, 0, 0])
            elif direction == 'y':
                unit_vector = np.array([0, 1, 0])
            else:
                unit_vector = np.array([0, 0, 1])

        x0 = R * unit_vector
        [x0, x1] = [x + x0, x - x0]

        x0 = np.around(x0).astype(int)
        x1 = np.around(x1).astype(int)
        L = np.amax(np.absolute([[x1[0] - x0[0]], [x1[1] - x0[1]], [x1[2] - x0[2]]])) + 1
        crds = [np.rint(np.linspace(x0[0], x1[0], L)).astype(int),
                np.rint(np.linspace(x0[1], x1[1], L)).astype(int),
                np.rint(np.linspace(x0[2], x1[2], L)).astype(int)]

        lower = ~np.any(np.vstack(crds).T < [L, L, L], axis=1)
        upper = ~np.any(np.vstack(crds).T >= shape + L, axis=1)
        valid = upper * lower
        if np.any(valid):
            if not allow_intersect:
                mask[crds[0][valid] - L, crds[1][valid] - L, crds[2][valid] - L] = 0
                mask = edt(mask) < radius
                if existing_img[mask].max() == 0:
                    fiber_count += 1
                    existing_img[mask] = fiber_count
                    ids_orient_dict[fiber_count] = unit_vector
                    n += 1
                    attempt_num = 0
                mask.fill(1)
            else:
                fiber_count += 1
                ids_orient_dict[fiber_count] = unit_vector
                im[crds[0][valid] - L, crds[1][valid] - L, crds[2][valid] - L] = fiber_count
                n += 1
                attempt_num = 0  # restart counter if change happens
            sys.stdout.write("\rFibers created: {} --> approximate target: {} ".format(fiber_count, n_fibers_total))

    if allow_intersect:
        distance_map = edt(im == 0)
        mask = distance_map < radius
        return watershed(distance_map, im, mask=mask), mask
