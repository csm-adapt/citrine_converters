from __future__ import division

import numpy as np
import warnings
from matplotlib import pyplot as plt
from itertools import groupby
from scipy.signal import medfilt as median_filter
from scipy.ndimage import gaussian_filter
from scipy.stats import linregress
from scipy.ndimage.morphology import binary_dilation, binary_erosion
from ..tools import (
    linear_merge,
    Normalized,
    resample,
    HoughSpace,
    r_squared,
    remove_outliers,
    covariance)


ELASTIC_OFFSET=0.002


class MechanicalProperties(object):
    """
    Summary
    =======

    Determines the mechanical properties given a pd.DataFrame with
    keys "strain" (`epsilon`) and "stress" (`sigma`).

    The time at which stress and strain are recorded must by synchronized, e.g.
    stress data collected at time `t` must correspond to the strain data
    collected at that same time, `t`.

    The frequency of data collection need not match. Linear interpolation is
    used to register the stress and strain data. No extrapolation is allowed,
    so the only accessible times are the intersection of the time ranges of
    strain and stress data.

    Input
    =====
    :param epsilon, pd.DataFrame: Strain data that, at a minimum,
        must contain `time` and `strain` fields.
    :param sigma, pd.DataFrame: Stress data that, at a minimum, must
        contain `time` and `stress` fields.
    """
    def __init__(self, epsilon, sigma):
        # ##########
        # merge on time
        time, strain, stress = linear_merge(
            x1=epsilon['time'].values, y1=epsilon['strain'].values,
            x2=sigma['time'].values, y2=sigma['stress'].values)
        self.time   = time
        self.strain = strain
        self.stress = stress

    @property
    def elastic_modulus(self):
        return getattr(self, '_elastic_modulus', None)

    @elastic_modulus.setter
    def elastic_modulus(self, modulus):
        self._elastic_modulus = float(modulus)

    @property
    def elastic_onset(self):
        return getattr(self, '_elastic_onset', None)

    @elastic_onset.setter
    def elastic_onset(self, onset):
        self._elastic_onset = float(onset)

    @property
    def yield_stress(self):
        # elastic modulus has not been calculated first.
        modulus = self.elastic_modulus
        onset   = self.elastic_onset
        if modulus is None:
            msg = 'The elastic modulus must be set before yield ' \
                  'strength can be calculated.'
            raise ValueError(msg)
        if onset is None:
            msg = 'The elastic onset must be set before yield ' \
                  'strength can be calculated.'
            raise ValueError(msg)
        # calculate the yield strength
        #+ use strain values that are greater that 0.2% above
        #+ the elastic onset
        subset = (self.strain > onset)
        substrain = self.strain[subset]
        substress = self.stress[subset]
        #+ find the hypothetical elastic stress at each strain
        estress = modulus*(substrain - self.elastic_onset - ELASTIC_OFFSET)
        #+ when the hypothetical elastic stress is greater than
        #+ the measured stress, we have reached yield.
        mask   = (substress < estress)
        for i in reversed(range(len(mask)-1)):
            if not mask[i]:
                yield_stress = (substress[i] + substress[i+1])/2
                break
        return yield_stress

    @property
    def yield_strain(self):
        # elastic modulus has not been calculated first.
        modulus = self.elastic_modulus
        onset   = self.elastic_onset
        if modulus is None:
            msg = 'The elastic modulus must be set before the ' \
                  'strain at yield can be calculated.'
            raise ValueError(msg)
        if onset is None:
            msg = 'The elastic onset must be set before the ' \
                  'strain at yield can be calculated.'
            raise ValueError(msg)
        # calculate the strain at yield
        yield_stress = self.yield_stress
        yield_strain = yield_stress/modulus + ELASTIC_OFFSET
        return yield_strain

    @property
    def plastic_onset(self):
        return self.yield_strain

    @property
    def elastic_region(self):
        onset = self.elastic_onset
        if onset is None:
            msg = 'The elastic onset must be set before the ' \
                  'elastic region can be defined.'
            raise ValueError(msg)
        try:
            yield_strain = self.yield_strain
        except ValueError:
            msg = 'The elastic modulus must be set before the ' \
                  'elastic region can be defined.'
        strain = self.strain
        mask = (strain > onset) & (strain < yield_strain + onset)
        return self.strain[mask]

    @property
    def plastic_region(self):
        try:
            yield_strain = self.yield_strain
        except ValueError:
            msg = 'The elastic modulus must be set before the ' \
                  'elastic region can be defined.'
        strain = self.strain
        mask = (strain > yield_strain + onset)
        return self.strain[mask]

    @property
    def ultimate_stress(self):
        return self.stress.max()

    @property
    def necking_onset(self):
        i = np.where(self.stress == self.ultimate_stress)[0][0]
        return self.strain[i] - self.elastic_onset

    @property
    def fracture_stress(self):
        i = np.argmax(self.strain)
        return self.stress[i]

    @property
    def total_elongation(self):
        i = np.argmax(self.strain)
        return self.strain[i] - self.elastic_onset

    @property
    def ductility(self):
        """
        Returns the ductility, defined as the strain at failure
        (total elongation - recoverable elastic strain).
        """
        # erecov = recoverable strain at failure
        erecov = self.fracture_stress/self.elastic_modulus
        return (self.total_elongation - erecov)

    @property
    def toughness(self):
        """Uses simple quadrature to calculate the toughness."""
        strain = self.strain
        stress = self.stress
        mask = strain > self.elastic_onset
        return np.dot((stress[mask][1:] + stress[mask][:-1])/2.,
                      (strain[mask][1:] - strain[mask][:-1]))
#end 'class MechanicalProperties(object):'


def approximate_elastic_regime_from_hough(mechprop, **kwds):
    r"""
    Construct a Hough space from the strain and stress data, then
    analyze this Hough space to approximate the slope and intercept
    of the linear elastic region of the stress-strain curve.

    Given the equation

    $$
        ax + by + c = 0,\, a = \sin \phi,\, b = \cos \phi
    $$

    from above, and

    $$
        d = |a x + b y + c|
    $$

    then $c = \pm d$ so that

    $$
        \begin{align*}
            y &= \tan(-\phi) x \pm \frac{d}{\cos(-\phi)} \\
              &= \tan(\pi - \phi) x \mp \frac{d}{\cos(\pi - \phi)} \\
            y &= \tan(\theta) x \mp \frac{d}{\cos(\theta)}
        \end{align*}
    $$

    Then for linear segments in the set `(x, y)`, with `x` and
    `y` potentially normalized, a maximum in the Hough space
    occurs at a $(\theta, r)$ corresponding to the line that
    contains colinear points. In a stress-strain curve, this
    occurs close to the origin and near 90 degrees. Intuitively,
    one would look for the elastic region in this area.

    ## Moving back from scaled to unscaled coordinates

    As mentioned above, the Hough transform is performed on the scaled
    data to eliminate data compression due to disparate axes scales.
    We must return to an unscaled data now to eliminate the dimensional
    expansion from the scaled Hough transform.

    $$
        \begin{align*}
            y_s &= x_s \tan (\theta) - d \sec (\theta) \\
            \frac{y - y_{min}}{y_{max} - y_{min}} &= \frac{x - x_{min}}{x_{max} - x_{min}} \tan(\theta) - d \sec(\theta) \\
            y &= \left( \frac{x - x_{min}}{x_{max} - x_{min}} \tan(\theta) - d \sec(\theta) \right)(y_{max} - y_{min}) + y_{min} \\
              &= x \tan(\theta)\left( \frac{y_{max} - y_{min}}{x_{max} - x_{min}} \right) - x_{min} \tan(\theta) \left( \frac{y_{max} - y_{min}}{x_{max} - x_{min}} \right) - d (y_{max} - y_{min}) \sec(\theta) + y_{min}
        \end{align*}
    $$

    From which the elastic modulus is
    $E = \tan(\theta)(y_{max} - y_{min})/(x_{max} - x_{min})$ and the yield
    strength is defined as the intersection of the stress strain curve and

    $$
        y = (x-ELASTIC_OFFSET) \tan(\theta) \left( \frac{y_{max} - y_{min}}{x_{max} - x_{min}} \right) - x_{min} \tan(\theta)\left( \frac{y_{max} - y_{min}}{x_{max} - x_{min}} \right) - d (y_{max} - y_{min}) \sec(\theta) + y_{min}
    $$

    Input
    =====
    :mechprop, MechanicalProperties: Mechanical properties object from
        which the elastic properties are to be approximated.

    Options
    =======
    :lower, float: lower angle in which to look for the modulus (in degrees).
        Default: 60 degrees.
    :upper, float: upper angle in which to look for the modulus (in degrees).
        Default: 90 degrees.
    Passed through to the construction of a HoughSpace object. See
    HoughSpace for a description of these options.

    Output
    ======
    Dictionary of predicted values:
        {
            'elastic modulus' : m,
            'elastic onset'   : -b/m,
            'elastic strain'  : x[mask],
            'elastic stress'  : y[mask],
            'resampled'       : resampled,
            'hough'           : hough }
    where
    :elastic modulus, float: slope of the elastic region (Young's modulus)
    :elastic onset, float: Onset of elasticity.
    :elastic strain, array: slice of the strain vector lying inside
        the elastic region.
    :elastic stress, array: slice of the stress vector lying inside
        the elastic region.
    :resampled, 2D numpy.ndarray: resampled hough space
    :hough, HoughSpace: hough transform of stress-strain data.
    """
    # handle keywords
    qlo = kwds.get('lower', 60)
    qhi = kwds.get('upper', 90)

    # The Hough space will result in a curve that forms a "V" shape
    # near 90 degrees. The stress-strain curve have significantly
    # different ranges: 0-1000 MPa and 0-0.4 strain, respectively.
    # Normalize stress and strain so both are in the range [0-1].
    strain = Normalized(mechprop.strain)
    stress = Normalized(mechprop.stress)
    hough = HoughSpace(strain, stress, **kwds)

    # resample Hough space
    resampled = resample(hough)

    # smooth the resampled data to eliminate noise
    resampled[:] = gaussian_filter(resampled, 3)
    resampled[:] = gaussian_filter(resampled, 3)
    resampled[:] = gaussian_filter(resampled, 3)

    # look in the 60-90 degree range for the elastic region
    qlo = int(qlo/180*hough.nq)
    qhi = int(qhi/180*hough.nq)
    sub = resampled[qlo:qhi]
    pos = np.mean(np.argwhere(sub == sub.max()), axis=0) + [qlo, 0]
    theta, distance = hough.theta_distance(*pos)

    # move from scaled to unscaled coordinates (see doc string)
    x, y = strain.unscaled, stress.unscaled
    xs, ys = strain, stress
    xmin, xmax = x.min(), x.max()
    ymin, ymax = y.min(), y.max()
    dy = ymax - ymin
    dx = xmax - xmin
    dydx = dy/dx
    tanq = np.tan(theta)
    secq = 1./np.cos(theta)

    # y = m*x + b
    m = tanq*dydx
    b = -xmin*m - distance*dy*secq + ymin

    # find the plastic region (lies below `y = m*(x - ELASTIC_OFFSET) + b` line)
    plastic = (y < (m*(x - ELASTIC_OFFSET) + b))
    for i in reversed(range(plastic.size)):
        if not plastic[i]:
            plastic[:i] = False
            break

    # find the compliance region, if it exists
    compliance = np.zeros_like(plastic, dtype=bool)
    #compliance = (strain < -b/m)

    # a first approximation to the elastic region is the region
    # that is not compliance and not plastic.
    mask = ((~compliance) & (~plastic))
    return {
        'elastic modulus': m,
        'elastic onset': -b/m,
        'elastic strain': x[mask],
        'elastic stress': y[mask],
        'resampled': resampled,
        'hough': hough
    }


def interactive_approximator(mechprop, **kwds) :
    """
    Raise an interactive matplotlib window for the user to select two
    points in the elastic region.

    :param mechprop, MechanicalPproperties: The object that contains the
        stress-strain data.

    Options
    =======
    :param rtol, float: "Width" of the line used to determine if a point should
        be included in the linear region. If not specified, the selected points
        define the upper and lower bounds along the strain axis.

    :return: Dictionary of predicted values:
        {
            'elastic modulus' : m,
            'elastic onset'   : -b/m,
            'elastic strain'  : x[mask],
            'elastic stress'  : y[mask],
            'resampled'       : resampled,
            'hough'           : hough }
    where
    :elastic modulus, float: slope of the elastic region (Young's modulus)
    :elastic onset, float: Onset of elasticity.
    :elastic strain, array: slice of the strain vector lying inside
        the elastic region.
    :elastic stress, array: slice of the stress vector lying inside
        the elastic region.
    :resampled, 2D array: Carry-over from a poor initial implementation.
    :hough, 2D array: Carry-over from a poor initial implementation.
    """
    stress = mechprop.stress
    strain = mechprop.strain

    class DraggableLine:
        lock = None  # only one can be animated at a time

        def __init__(self, line):
            self.cidpress = None
            # self.cidrelease = None
            self.cidmotion = None
            self.line = line
            self.selected, = line.axes.plot([], [], 'ro')
            self.guide, = line.axes.plot([], [], 'r--')
            self.first = None
            self.second = None

        def connect(self):
            'connect to all the events we need'
            self.cidpress = self.line.figure.canvas.mpl_connect(
                'button_press_event', self.on_press)
            # self.cidrelease = self.line.figure.canvas.mpl_connect(
            #     'button_release_event', self.on_release)
            self.cidmotion = self.line.figure.canvas.mpl_connect(
                'motion_notify_event', self.on_motion)

        def get_line_limits(self, x1, x2, y1, y2):
            xlo, xhi = self.line.axes.get_xlim()
            ylo, yhi = self.line.axes.get_ylim()
            dy = y2 - y1
            dx = x2 - x1
            if np.isclose(dx, 0):
                xmin = x1
                xmax = x1
                ymin = ylo
                ymax = yhi
            elif np.isclose(dy, 0):
                xmin = xlo
                xmax = xhi
                ymin = y1
                ymax = y1
            else:
                m = dy / dx
                xmin = xlo
                xmax = xhi
                ymin = m * (xlo - x1) + y1
                ymax = m * (xhi - x1) + y1
            return ([xmin, xmax], [ymin, ymax])

        def on_press(self, event):
            'on button press we will see if the mouse is over us and store some data'
            if DraggableLine.lock is not None:
                return self.on_second(event)
            if event.inaxes != self.line.axes: return
            contains, attrd = self.line.contains(event)
            if not contains: return
            xdata = self.line.get_xdata()
            ydata = self.line.get_ydata()
            ind = np.argmin((xdata - event.xdata)**2 + (ydata - event.ydata)**2)
            x0, y0 = xdata[ind], ydata[ind]
            self.first = x0, y0
            DraggableLine.lock = self

            # now redraw the selected points
            self.selected.set_xdata([x0])
            self.selected.set_ydata([y0])

            # draw everything but the selected lines and store the pixel buffer
            canvas = self.line.figure.canvas
            axes = self.line.axes
            self.guide.set_animated(True)
            axes.draw_artist(self.selected)
            canvas.draw()
            self.background = canvas.copy_from_bbox(self.line.axes.bbox)

            # now redraw the guide line
            x, y = self.get_line_limits(x0, event.xdata, y0, event.ydata)
            self.guide.set_xdata(x)
            self.guide.set_ydata(y)
            axes.draw_artist(self.guide)

            # and blit just the redrawn area
            canvas.blit(axes.bbox)

        def on_motion(self, event):
            'on motion we will move the rect if the mouse is over us'
            if DraggableLine.lock is not self:
                return
            if event.inaxes != self.line.axes: return
            x1, y1 = self.first
            x2, y2 = event.xdata, event.ydata
            x, y = self.get_line_limits(x1, x2, y1, y2)
            self.guide.set_xdata(x)
            self.guide.set_ydata(y)

            canvas = self.line.figure.canvas
            axes = self.line.axes
            # restore the background region
            canvas.restore_region(self.background)

            # redraw just the current rectangle
            axes.draw_artist(self.guide)

            # blit just the redrawn area
            canvas.blit(axes.bbox)

        def on_second(self, event):
            'on release we reset the press data'
            if DraggableLine.lock is not self: return
            if event.inaxes != self.line.axes: return
            contains, attrd = self.line.contains(event)
            if not contains: return
            xdata = self.line.get_xdata()
            ydata = self.line.get_ydata()
            ind = np.argmin((xdata - event.xdata)**2 + (ydata - event.ydata)**2)
            x0, y0 = xdata[ind], ydata[ind]
            self.second = x0, y0

            # set the data for the selected points
            x1, y1 = self.first
            x2, y2 = self.second
            self.selected.set_xdata([x1, x2])
            self.selected.set_ydata([y1, y2])

            # release the lock
            DraggableLine.lock = None

            # turn off the rect animation property and reset the background
            self.guide.set_animated(False)
            self.background = None

            # redraw the full figure
            # axes = self.line.axes
            # axes.draw_artist(self.)
            self.line.figure.canvas.draw()

        def disconnect(self):
            'disconnect all the stored connection ids'
            self.line.figure.canvas.mpl_disconnect(self.cidpress)
            # self.line.figure.canvas.mpl_disconnect(self.cidrelease)
            self.line.figure.canvas.mpl_disconnect(self.cidmotion)

    fig, ax = plt.subplots(1, 1)
    line, = ax.plot(strain, stress, 'k:', picker=5)
    dl = DraggableLine(line)
    dl.connect()
    plt.show(block=True)
    xlo, ylo = dl.first
    xhi, yhi = dl.second
    if xhi < xlo:
        xlo, xhi = xhi, xlo
        ylo, yhi = yhi, ylo
    m = (yhi-ylo)/(xhi-xlo)
    b = ylo - m*xlo
    # which points are close to this line?
    if "rtol" in kwds:
        mask = np.isclose(stress - m*strain, b, rtol=kwds['rtol'])
    else:
        mask = ((strain >= xlo) & (strain <= xhi))
    # a.x = b
    a = np.stack((np.where(mask)[0].astype(float), strain[mask]), axis=-1)
    b = stress[mask]
    ((b, m), residuals, rank, singularValues) = np.linalg.lstsq(a, b, rcond=None)
    return {
        'elastic modulus': m,
        'elastic onset': -b/m,
        'elastic strain': strain[mask],
        'elastic stress': stress[mask],
        'resampled': np.array([[]]),
        'hough': np.array([[]])
    }


def set_elastic(mechprop, **kwds):
    """
    Sets the elastic properties for the provided MechanicalProperties
    object.

    Input
    =====
    :mechprop, MechanicalProperties: mechanical properties object into
        which the elastic properties will be stored.

    Options
    =======
    :approximator, f(strain, stress): Function to approximate the
        "elastic onset" and "elastic modulus", returned as keys in
        a dictionary.
    :maxiter, int: maximum number of iterations. Default: 20.
    :covariance, bool: optimize on covariance. Default.
    :rsquared, bool: optimize on $R^2$. Supercedes covariance.
    :error, float: strain gage measurement error. Default: 0.00005.

    Output
    ======
    Returns best performance metrics. Modulus and offset stored in
    `mechprop`.
    """
    # ########################
    # handle keyword arguments
    interactive = kwds.get('interactive', True)
    if interactive:
        approximator = interactive_approximator
    else:
        approximator = approximate_elastic_regime_from_hough

    # # maximum number of iterations
    # maxiter = kwds.get('maxiter', 20)
    #
    # # set the target optimization (This is a minimization.)
    # if 'rsq' in kwds:
    #     target = lambda cov, rsq : 1. - rsq
    # else:
    #     # by default, optimize on the covariance
    #     target = lambda cov, rsq : cov
    #
    # # error in the strain gage measurement
    # # error = np.abs(kwds.get('error', 0.00005))
    # error = np.abs(kwds.get('error', 0.00005))

    # ########################
    # strain = mechprop.strain
    # stress = mechprop.stress
    approx = approximator(mechprop)
    epsilon = approx['elastic strain']
    sigma = approx['elastic stress']

    # ########################
    regression = calculate_modulus(epsilon, sigma)

    modulus = regression['modulus']
    intercept = -regression['elastic onset']*modulus
    rsq = regression['coefficient of determination']
    cov = regression['coefficient of variation']
    ses = regression['standard error in the slope']

    # ########################
    # update the mechanical properties
    mechprop.elastic_modulus = modulus
    mechprop.elastic_onset = regression['elastic onset']

    # ########################
    # save the best
    return {
        'param': [intercept, modulus],
        'SE modulus': ses,
        'cov': cov,
        'rsq': rsq,
        'residual strain': epsilon - sigma/modulus,
        'elastic strain': epsilon,
        'elastic stress': sigma,
        'mask': np.ones_like(epsilon),
        'hough': approx['hough'],
        'resampled': approx['resampled']
    }

    # # ########################
    # # sigma = E epsilon + offset
    # # epsilon = e_calc = (sigma - offset)/E
    # # s.t.
    # # residual strain = e_measured - e_calc
    # predicted_strain = lambda s, E, b: (s - b)/E
    # residual_strain = lambda e, s, E, b: e - predicted_strain(s, E, b)
    #
    # # ########################
    # # use residual strain to minimize RMS residual strain
    # residual = residual_strain(epsilon, sigma, modulus, intercept)
    # # residual = residual_strain(epsilon-approx['elastic onset'], sigma, modulus)
    # # DEBUGGING #
    # # import sys
    # # from matplotlib import pyplot as plt
    # # plt.plot(residual, sigma)
    # # plt.show(block=True)
    # # sys.exit(1)
    # # END DEBUGGING #
    # mask = (np.abs(residual) < error)
    # # lower bound (end of compliance region)
    # for i in range(len(mask)):
    #     if mask[i]:
    #         lower = i
    #         break
    # # upper bound (end of linear elastic region)
    # for i in reversed(range(len(mask))):
    #     if mask[i]:
    #         upper = i
    #         break
    # mask[lower:upper] = True
    #
    # # ########################
    # # exclude outliers (to help with noisy data) using IQR
    # # this should remove both outliers and the compliance region
    # # print "Iteration:",
    # # i = 0
    # for _ in range(len(epsilon)):
    #     # i += 1
    #     # print i,
    #     previous = mask.copy()
    #     modulus, intercept, corrcoeff, pvalue, SE_slope = \
    #         linregress(epsilon[mask], sigma[mask])
    #     residual = residual_strain(epsilon, sigma, modulus, intercept)
    #     mask[mask] = remove_outliers(residual[mask])
    #     # print "({} changed),".format(np.sum(np.logical_xor(mask, previous))),
    #     if np.all(previous == mask):
    #         # print ""
    #         break
    # print("Number points used in fit: {}/{}".format(np.sum(mask), len(mask)))
    #
    # # DEBUGGING #
    # from matplotlib import pyplot as plt
    # fig, ax = plt.subplots(1, 1)
    # colors = [('darkgreen' if b else 'darkblue') for b in mask]
    # ax.scatter(residual, sigma, c=colors)
    # ax.axvline(-error, ls='--', color='r')
    # ax.axvline(error, ls='--', color='r')
    # plt.show()
    # # # END DEBUGGING #
    #
    # # ########################
    # # save the best
    # best = {
    #     'param': [intercept, modulus],
    #     'SE modulus': SE_slope,
    #     'cov': covariance(epsilon[mask], predicted_strain(sigma[mask], modulus, intercept)),
    #     'rsq': r_squared(epsilon[mask], predicted_strain(sigma[mask], modulus, intercept)),
    #     'residual strain': residual,
    #     'elastic strain': epsilon,
    #     'elastic stress': sigma,
    #     'mask': mask,
    #     'hough': approx['hough'],
    #     'resampled': approx['resampled']
    # }
    #
    # # ########################
    # # update the modulus of the mechanical properties
    # intercept, modulus = best['param']
    # mechprop.elastic_modulus = modulus
    # mechprop.elastic_onset = -intercept / modulus
    #
    # # done -- no iteration
    # return best


def calculate_modulus(strain, stress):
    """
    Calculates the modulus based on the ASTM E111.

    The Young's modulus, :math:`E` is calculated from strain (:math:`X`) and
    stress (:math:`Y`) data. The total number of points is :math:`N`

    .. math::

        E = \frac{\sum XY - N\overline{X}\overline{Y}}{\sum X^2 - N\overline{X}^2}

    The coefficient of determination, :math:`r^2`, is given by

    .. math::

        r^2 = \frac{\left[ \sum XY - \frac{\sum X \sum Y}{N} \right]^2}{\left[ \sum X^2 - \left(\sum X\right)^2/N \right]\left[ \sum Y^2 - \left( \sum Y \right)^2/N \right]}

    The coefficient of variation of the slope, :math:`V_1` is

    .. math::

        V_1 = 100 \sqrt{\frac{\frac{1}{r^2} - 1}{N - 2}}

    The coefficient of variation of te slope should be lower than 2%. Values as
    low as 0.5% have been achieved in aluminum. The confidence interval for the
    regression, :math:`I`,

    .. math::

        \pm I = t V_1

    :math:`t` is the t-statistic from standard tables at N-2 degrees of freedom.

    :param strain:
    :param stress:
    :return:
    """
    x, y = np.asarray(strain), np.asarray(stress)
    assert x.shape == y.shape, \
        "The number of stress and strain observations must match."
    N = len(x)
    xbar, ybar = x.mean(), y.mean()

    a = np.stack((np.ones_like(strain).astype(float), strain), axis=-1)
    b = stress
    ((b, m), residuals, rank, SV) = np.linalg.lstsq(a, b, rcond=None)

    modulus = ((x*y).sum() - N*xbar*ybar) / \
              ((x**2).sum() - N*xbar**2)
    rsq = ((x*y).sum() - (xbar*ybar)/N) / \
          (((x**2).sum() - xbar**2/N)*(y**2).sum() - ybar**2/N)

    cov = 100*np.sqrt((1/rsq - 1)/(N - 2))

    ses = np.sqrt((((y - ybar)**2).sum()) / \
                  (((x - xbar)**2).sum()*(N-2)))

    return {
        'modulus': modulus,
        'elastic onset': -b/modulus,
        'coefficient of determination': rsq,
        'coefficient of variation': cov,
        'standard error in the slope': ses
    }