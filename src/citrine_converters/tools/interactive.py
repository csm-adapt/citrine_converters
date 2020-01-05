import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import LassoSelector
from matplotlib.path import Path


class DraggableLine:
    lock = None  # only one can be animated at a time

    def __init__(self, ax, line):
        self.cidpress = None
        self.cidmotion = None
        self.ax = ax
        self.line = line
        self.selected, = line.axes.plot([], [], 'ro')
        self.guide, = line.axes.plot([], [], 'r--')
        self.first = None
        self.second = None
        self.connect()

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.ax.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidmotion = self.ax.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def get_line_limits(self, x1, x2, y1, y2):
        xlo, xhi = self.ax.get_xlim()
        ylo, yhi = self.ax.get_ylim()
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
        if event.inaxes != self.ax: return
        contains, attrd = self.line.contains(event)
        if not contains: return
        xdata = self.line.get_xdata()
        ydata = self.line.get_ydata()
        ind = np.argmin((xdata - event.xdata) ** 2 + (ydata - event.ydata) ** 2)
        x0, y0 = xdata[ind], ydata[ind]
        self.first = x0, y0
        DraggableLine.lock = self

        # now redraw the selected points
        self.selected.set_xdata([x0])
        self.selected.set_ydata([y0])

        # draw everything but the selected lines and store the pixel buffer
        canvas = self.ax.figure.canvas
        axes = self.ax
        self.guide.set_animated(True)
        axes.draw_artist(self.selected)
        canvas.draw()
        self.background = canvas.copy_from_bbox(self.ax.bbox)

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
        if event.inaxes != self.ax: return
        x1, y1 = self.first
        x2, y2 = event.xdata, event.ydata
        x, y = self.get_line_limits(x1, x2, y1, y2)
        self.guide.set_xdata(x)
        self.guide.set_ydata(y)

        canvas = self.ax.figure.canvas
        axes = self.ax
        # restore the background region
        canvas.restore_region(self.background)

        # redraw just the current rectangle
        axes.draw_artist(self.guide)

        # blit just the redrawn area
        canvas.blit(axes.bbox)

    def on_second(self, event):
        'on release we reset the press data'
        if DraggableLine.lock is not self: return
        if event.inaxes != self.ax: return
        contains, attrd = self.line.contains(event)
        if not contains: return
        xdata = self.line.get_xdata()
        ydata = self.line.get_ydata()
        ind = np.argmin((xdata - event.xdata) ** 2 + (ydata - event.ydata) ** 2)
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
        self.ax.figure.canvas.draw()

    def disconnect(self):
        'disconnect all the stored connection ids'
        self.ax.figure.canvas.mpl_disconnect(self.cidpress)
        self.ax.figure.canvas.mpl_disconnect(self.cidmotion)


class SelectFromCollection:
    """Select indices from a matplotlib collection using `LassoSelector`.

    Whether a point is selected is toggled when the point is selected. By
    default, all points are selected.

    This tool fades out the points that are not part of the selection
    (i.e., reduces their alpha values). If your collection has alpha < 1,
    this tool will permanently alter the alpha values.

    Note that this tool selects collection objects based on their *origins*
    (i.e., `offsets`).

    Parameters
    ----------
    ax : :class:`~matplotlib.axes.Axes`
        Axes to interact with.

    alpha : :class:`matplotlib.collections.Collection` subclass
        Collection you want to select from.

    selected : bool
        Whether all points are selected by default (True, default) or
        unselected (False).

    alpha_other : 0 <= float <= 1
        To highlight a selection, this tool sets all selected points to an
        alpha value of 1 and non-selected points to `alpha_other`.
    """

    def __init__(self, ax, artist, selected=True, alpha_other=0.3):
        if isinstance(artist, plt.Line2D):
            collection = ax.scatter(artist.get_xdata(), artist.get_ydata(),
                                    c=artist.get_color(), alpha=0)
            artist.set_alpha(alpha_other)
            ax.add_artist(collection)
        else:
            collection = artist
        self.canvas = ax.figure.canvas
        self.collection = collection
        self.alpha_other = alpha_other

        self.xys = collection.get_offsets()
        self.Npts = len(self.xys)

        # Ensure that we have separate colors for each object
        self.fc = collection.get_facecolors()
        if len(self.fc) == 0:
            raise ValueError('Collection must have a facecolor')
        elif len(self.fc) == 1:
            self.fc = np.tile(self.fc, (self.Npts, 1))

        self.lasso = LassoSelector(ax, onselect=self.onselect)
        self.mask = np.ndarray((self.Npts,), dtype=bool)
        self.mask.fill(selected)

    def onselect(self, verts):
        # 0010101110 (initial)
        # 0110110000 (selected)
        # 0100011110 (xor)
        path = Path(verts)
        mask = path.contains_points(self.xys)
        np.logical_xor(mask, self.mask, out=mask)
        self.mask = mask
        self.fc[:, -1] = self.alpha_other
        self.fc[self.mask, -1] = 1
        self.collection.set_facecolors(self.fc)
        self.canvas.draw_idle()

    def disconnect(self):
        self.lasso.disconnect_events()
        self.fc[:, -1] = 1
        self.collection.set_facecolors(self.fc)
        self.canvas.draw_idle()


def trim(x, y, **scatter_kwds):
    """
    Interactively trims data from a plot of (x, y).

    :param x:
    :param y:
    :param scatter_kwds: keywords to pass to the scatter plot.
    :return:
    """
    fig, ax = plt.subplots()
    pts = ax.scatter(x, y, **scatter_kwds)
    selector = SelectFromCollection(ax, pts)

    def accept(event):
        if event.key == 'enter':
            selector.disconnect()
            plt.close(fig)

    fig.canvas.mpl_connect("key_press_event", accept)
    ax.set_title("Press enter to accept selected points.")
    plt.show(block=True)

    return selector.mask.copy()