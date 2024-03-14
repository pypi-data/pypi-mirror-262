"""
Note: Most of the filters are simple wrappers of functions in either scikitimage or scipy.ndimage.
The filters can be run directly in these packages if the user desires, but the wrapping is done for
simplicity so that the Workspace class can be used, and the filter executions can be logged by the
workspace class in order to document the simulation workflows.

The C++ version of puma implements the filters directly. But for python, there's no reason to re-invent
the wheel when so many great packages exist for image manipulation
"""
from skimage.filters import gaussian
from scipy.ndimage import distance_transform_edt, median_filter
from scipy.ndimage import uniform_filter
from skimage.morphology import erosion, dilation, opening, closing, ball
from pumapy.utilities.workspace import Workspace
from pumapy.utilities.logger import print_warning
import numpy as np


def filter_median(ws, size):
    """ 3D Median filter

    :param ws: input workspace
    :type ws: Workspace
    :param size: size of window
    :type size: int

    :Example:
    >>> import pumapy as puma
    >>> ws = puma.import_3Dtiff(puma.path_to_example_file("100_fiberform.tif"), 1.3e-6)
    Importing .../100_fiberform.tif ... Done
    >>> ws_median = ws.copy()
    >>> puma.filter_median(ws_median, size=10)
    >>> # puma.compare_slices(ws, ws_median)  # to visualize it
    """
    if not isinstance(ws, Workspace):
        raise Exception("Workspace must be passed.")

    ws.log.log_section("Median Filter:")
    ws.log.log_line("Window Size: " + str(size))
    ws.log.write_log()

    ws.matrix = median_filter(ws.matrix, size)


def filter_gaussian(ws, sigma=1, apply_on_orientation=False):
    """ 3D Gaussian filter

    :param ws: input workspace
    :type ws: Workspace
    :param sigma: size of kernel
    :type sigma: int
    :param apply_on_orientation: specify whether to apply filter on orientation field
    :type apply_on_orientation: bool

    :Example:
    >>> import pumapy as puma
    >>> ws = puma.import_3Dtiff(puma.path_to_example_file("100_fiberform.tif"), 1.3e-6)
    Importing .../100_fiberform.tif ... Done
    >>> ws_gaussian = ws.copy()
    >>> puma.filter_gaussian(ws_gaussian, sigma=2, apply_on_orientation=False)
    >>> # puma.compare_slices(ws, ws_gaussian, 'z', index=1)  # to visualize it
    """
    if not isinstance(ws, Workspace):
        raise Exception("Workspace must be passed.")

    ws.log.log_section("Gaussian Filter:")
    ws.log.log_line("Sigma: " + str(sigma))
    ws.log.write_log()

    ws.matrix = gaussian(ws.matrix, sigma=sigma, preserve_range=True).astype(np.uint16)

    if apply_on_orientation:
        if ws.orientation.shape[:3] == ws.matrix.shape:
            unprocessed_orientation = ws.orientation.copy()
            ws.orientation = gaussian(ws.orientation, sigma=sigma, channel_axis=-1, preserve_range=True)
            # recreate unit vectors
            magnitude = np.linalg.norm(ws.orientation, axis=3)
            with np.errstate(divide='ignore', invalid='ignore'):  # temporarily ignore divide by 0 warnings
                ws.orientation = ws.orientation / magnitude[:, :, :, np.newaxis]
            ws.orientation[np.isnan(ws.orientation)] = unprocessed_orientation[np.isnan(ws.orientation)]
        else:
            print_warning("To apply filter on orientation field, it has to have same shape as ws.matrix.")


def filter_edt(ws, cutoff):
    """ 3D Exact euclidean distance transform.

        :param ws: input workspace
        :type ws: Workspace
        :param cutoff: cutoff to binarize image
        :type cutoff: (int, int)

        :Example:
        >>> import pumapy as puma
        >>> ws = puma.generate_tpms((100, 100, 100), (0.02, 0.05), 0.201, 0)  # generate tpms material
        Generating TPMS...
        >>> ws_edt = ws.copy()
        >>> puma.filter_edt(ws_edt, cutoff=(1, 1))
        >>> # puma.compare_slices(ws, ws_edt)  # to visualize it
    """
    if not isinstance(ws, Workspace):
        raise Exception("Workspace must be passed")

    ws.log.log_section("Euclidean Distance Transform Filter")
    ws.log.write_log()

    ws.matrix = distance_transform_edt(np.logical_and(ws.matrix >= cutoff[0], ws.matrix <= cutoff[1]))


def filter_mean(ws, size=5):
    """ 3D Mean filter.

        :param ws: input workspace
        :type ws: Workspace
        :param size: size of window
        :type size: int

        :Example:
        >>> import pumapy as puma
        >>> ws = puma.import_3Dtiff(puma.path_to_example_file("100_fiberform.tif"), 1.3e-6)
        Importing .../100_fiberform.tif ... Done
        >>> ws_mean = ws.copy()
        >>> puma.filter_mean(ws_mean, size=10)
        >>> # puma.compare_slices(ws, ws_mean)  # to visualize it
    """
    if not isinstance(ws, Workspace):
        raise Exception("Workspace must be passed")

    ws.log.log_section("Mean Filter")
    ws.log.log_line("Window Size: " + str(size))
    ws.log.write_log()

    ws.matrix = uniform_filter(ws.matrix, size)


def filter_erode(ws, cutoff, size=5):
    """ 3D morphological erosion filter.

        :param ws: input workspace
        :type ws: Workspace
        :param cutoff: cutoff to binarize image
        :type cutoff: (int, int)
        :param size: size of the spherical windows used
        :type size: int

        :Example:
        >>> import pumapy as puma
        >>> ws = puma.generate_tpms((100, 100, 100), (0.02, 0.05), 0.201, 0)  # generate tpms material
        Generating TPMS ...
        >>> ws_erode = ws.copy()
        >>> puma.filter_erode(ws_erode, (1, 1))  # eroding the copy
        >>> # puma.compare_slices(ws, ws_erode)  # to visualize it
    """
    if not isinstance(ws, Workspace):
        raise Exception("Workspace must be passed")

    ws.log.log_section("Erode Filter")
    ws.log.log_line("Spherical Window Size: " + str(size))
    ws.log.write_log()

    ws.binarize_range(cutoff)

    ws.matrix = erosion(ws.matrix, ball(size))


def filter_dilate(ws, cutoff, size=5):
    """ 3D morphological dilation filter.

        :param ws: input workspace
        :type ws: Workspace
        :param cutoff: cutoff to binarize image
        :type cutoff: (int, int)
        :param size: size of the spherical windows used
        :type size: int

        :Example:
        >>> import pumapy as puma
        >>> ws = puma.generate_tpms((100, 100, 100), (0.02, 0.05), 0.201, 0)  # generate tpms material
        Generating TPMS ...
        >>> ws_dilate = ws.copy()
        >>> puma.filter_dilate(ws_dilate, cutoff=(1, 1), size=5)  # dilating the copy
        >>> # puma.compare_slices(ws, ws_dilate)  # to visualize it
    """
    if not isinstance(ws, Workspace):
        raise Exception("Workspace must be passed")

    ws.log.log_section("Dilation Filter")
    ws.log.log_line("Spherical Window Size: " + str(size))
    ws.log.write_log()

    ws.binarize_range(cutoff)

    ws.matrix = dilation(ws.matrix, ball(size))


def filter_opening(ws, cutoff, size=5):
    """ 3D morphological opening filter (i.e. dilation first and then erosion).

        :param ws: input workspace
        :type ws: Workspace
        :param cutoff: cutoff to binarize image
        :type cutoff: (int, int)
        :param size: size of the spherical windows used
        :type size: int

        :Example:
        >>> import pumapy as puma
        >>> ws = puma.import_3Dtiff(puma.path_to_example_file("100_fiberform.tif"), 1.3e-6)
        Importing .../100_fiberform.tif ... Done
        >>> ws_opening = ws.copy()
        >>> puma.filter_opening(ws_opening, cutoff=(90, 255), size=3)
        >>> ws_binary = ws.copy()
        >>> ws_binary.binarize_range((90, 255))
        >>> # puma.compare_slices(ws_binary, ws_opening, 'z', index=1)  # to visualize it
    """
    if not isinstance(ws, Workspace):
        raise Exception("Workspace must be passed")

    ws.log.log_section("Opening Filter")
    ws.log.log_line("Spherical Window Size: " + str(size))
    ws.log.write_log()

    ws.binarize_range(cutoff)

    ws.matrix = opening(ws.matrix, ball(size))


def filter_closing(ws, cutoff, size=5):
    """ 3D morphological closing filter (i.e. erosion first and then dilation).

        :param ws: input workspace
        :type ws: Workspace
        :param cutoff: cutoff to binarize image
        :type cutoff: (int, int)
        :param size: size of the spherical windows used
        :type size: int

        :Example:
        >>> import pumapy as puma
        >>> ws = puma.import_3Dtiff(puma.path_to_example_file("100_fiberform.tif"), 1.3e-6)
        Importing .../100_fiberform.tif ... Done
        >>> ws_closing = ws.copy()
        >>> puma.filter_closing(ws_closing, cutoff=(90, 255), size=3)
        >>> ws_binary = ws.copy()
        >>> ws_binary.binarize_range((90, 255))
        >>> # puma.compare_slices(ws_binary, ws_closing, 'z', index=1)  # to visualize it
    """
    if not isinstance(ws, Workspace):
        raise Exception("Workspace must be passed")

    ws.log.log_section("Closing Filter")
    ws.log.log_line("Spherical Window Size: " + str(size))
    ws.log.write_log()

    ws.binarize_range(cutoff)

    ws.matrix = closing(ws.matrix, ball(size))
