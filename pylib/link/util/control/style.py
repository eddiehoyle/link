from maya import cmds

class Style(object):
    """Point information for shapes"""

    def _style(self, array):
        """Return dict of curve data"""

        data = []
        for points in array:
            curve_data = dict(points=points,
                              knot=range(len(points)))
            data.append(curve_data)

        return data

    def exists(self, style):
        """Style data exists"""
        return hasattr(self, style)

    @property
    def square(self):
        points = [((-1, 0, 1,), (-1, 0, -1), (1, 0, -1), (1, 0, 1), (-1, 0, 1))]
        return self._style(points)

    @property
    def circle(self):
        points = [((6.123233995736766e-17, 2.2204460492503131e-16, 1.0), (-0.25881904510252068, 2.1447861848524059e-16, 0.96592582628906831), (-0.49999999999999989, 1.9229626863835641e-16, 0.86602540378443871), (-0.70710678118654746, 1.5700924586837752e-16, 0.70710678118654757), (-0.8660254037844386, 1.1102230246251568e-16, 0.50000000000000011), (-0.9659258262890682, 5.7469372616863126e-17, 0.25881904510252096), (-1.0, 6.2900117310782151e-32, 2.8327694488239898e-16), (-0.96592582628906842, -5.7469372616863015e-17, -0.25881904510252046), (-0.86602540378443893, -1.1102230246251559e-16, -0.49999999999999972), (-0.70710678118654791, -1.5700924586837747e-16, -0.70710678118654735), (-0.50000000000000044, -1.9229626863835638e-16, -0.8660254037844386), (-0.25881904510252129, -2.1447861848524059e-16, -0.96592582628906831), (-5.330771254230592e-16, -2.2204460492503136e-16, -1.0000000000000002), (0.2588190451025203, -2.1447861848524067e-16, -0.96592582628906865), (0.49999999999999961, -1.922962686383565e-16, -0.86602540378443915), (0.70710678118654735, -1.5700924586837764e-16, -0.70710678118654813), (0.8660254037844386, -1.110223024625158e-16, -0.50000000000000067), (0.96592582628906842, -5.7469372616863249e-17, -0.25881904510252152), (1.0000000000000004, -1.6150773046340863e-31, -7.273661547324616e-16), (0.96592582628906898, 5.7469372616862941e-17, 0.25881904510252013), (0.86602540378443948, 1.1102230246251556e-16, 0.49999999999999956), (0.70710678118654846, 1.5700924586837747e-16, 0.70710678118654735), (0.500000000000001, 1.9229626863835641e-16, 0.86602540378443871), (0.25881904510252179, 2.1447861848524064e-16, 0.96592582628906853), (9.49410759657493e-16, 2.2204460492503141e-16, 1.0000000000000004))]
        return self._style(points)

    @property
    def sphere(self):
        points = [((6.123233995736766e-17, 1.0, 0.0), (-0.25881904510252068, 0.96592582628906831, 0.0), (-0.49999999999999989, 0.86602540378443871, 0.0), (-0.70710678118654746, 0.70710678118654757, 0.0), (-0.8660254037844386, 0.50000000000000011, 0.0), (-0.9659258262890682, 0.25881904510252096, 0.0), (-1.0, 2.8327694488239898e-16, 0.0), (-0.96592582628906842, -0.25881904510252046, 0.0), (-0.86602540378443893, -0.49999999999999972, 0.0), (-0.70710678118654791, -0.70710678118654735, 0.0), (-0.50000000000000044, -0.8660254037844386, 0.0), (-0.25881904510252129, -0.96592582628906831, 0.0), (-5.330771254230592e-16, -1.0000000000000002, 0.0), (0.2588190451025203, -0.96592582628906865, 0.0), (0.49999999999999961, -0.86602540378443915, 0.0), (0.70710678118654735, -0.70710678118654813, 0.0), (0.8660254037844386, -0.50000000000000067, 0.0), (0.96592582628906842, -0.25881904510252152, 0.0), (1.0000000000000004, -7.273661547324616e-16, 0.0), (0.96592582628906898, 0.25881904510252013, 0.0), (0.86602540378443948, 0.49999999999999956, 0.0), (0.70710678118654846, 0.70710678118654735, 0.0), (0.500000000000001, 0.86602540378443871, 0.0), (0.25881904510252179, 0.96592582628906853, 0.0), (9.49410759657493e-16, 1.0000000000000004, 0.0)),
                  ((1.3596310734468911e-32, 1.0, -6.123233995736766e-17), (-5.7469372616863065e-17, 0.96592582628906831, 0.25881904510252068), (-1.1102230246251563e-16, 0.86602540378443871, 0.49999999999999989), (-1.5700924586837749e-16, 0.70710678118654757, 0.70710678118654746), (-1.9229626863835638e-16, 0.50000000000000011, 0.8660254037844386), (-2.1447861848524057e-16, 0.25881904510252096, 0.9659258262890682), (-2.2204460492503131e-16, 2.8327694488239898e-16, 1.0), (-2.1447861848524062e-16, -0.25881904510252046, 0.96592582628906842), (-1.9229626863835646e-16, -0.49999999999999972, 0.86602540378443893), (-1.5700924586837759e-16, -0.70710678118654735, 0.70710678118654791), (-1.1102230246251575e-16, -0.8660254037844386, 0.50000000000000044), (-5.74693726168632e-17, -0.96592582628906831, 0.25881904510252129), (-1.1836689970913454e-31, -1.0000000000000002, 5.330771254230592e-16), (5.7469372616862978e-17, -0.96592582628906865, -0.2588190451025203), (1.1102230246251557e-16, -0.86602540378443915, -0.49999999999999961), (1.5700924586837747e-16, -0.70710678118654813, -0.70710678118654735), (1.9229626863835638e-16, -0.50000000000000067, -0.8660254037844386), (2.1447861848524062e-16, -0.25881904510252152, -0.96592582628906842), (2.2204460492503141e-16, -7.273661547324616e-16, -1.0000000000000004), (2.1447861848524074e-16, 0.25881904510252013, -0.96592582628906898), (1.9229626863835658e-16, 0.49999999999999956, -0.86602540378443948), (1.5700924586837771e-16, 0.70710678118654735, -0.70710678118654846), (1.1102230246251588e-16, 0.86602540378443871, -0.500000000000001), (5.7469372616863311e-17, 0.96592582628906853, -0.25881904510252179), (2.1081153703972189e-31, 1.0000000000000004, -9.49410759657493e-16)),
                  ((6.123233995736766e-17, 2.2204460492503131e-16, 1.0), (-0.25881904510252068, 2.1447861848524059e-16, 0.96592582628906831), (-0.49999999999999989, 1.9229626863835641e-16, 0.86602540378443871), (-0.70710678118654746, 1.5700924586837752e-16, 0.70710678118654757), (-0.8660254037844386, 1.1102230246251568e-16, 0.50000000000000011), (-0.9659258262890682, 5.7469372616863126e-17, 0.25881904510252096), (-1.0, 6.2900117310782151e-32, 2.8327694488239898e-16), (-0.96592582628906842, -5.7469372616863015e-17, -0.25881904510252046), (-0.86602540378443893, -1.1102230246251559e-16, -0.49999999999999972), (-0.70710678118654791, -1.5700924586837747e-16, -0.70710678118654735), (-0.50000000000000044, -1.9229626863835638e-16, -0.8660254037844386), (-0.25881904510252129, -2.1447861848524059e-16, -0.96592582628906831), (-5.330771254230592e-16, -2.2204460492503136e-16, -1.0000000000000002), (0.2588190451025203, -2.1447861848524067e-16, -0.96592582628906865), (0.49999999999999961, -1.922962686383565e-16, -0.86602540378443915), (0.70710678118654735, -1.5700924586837764e-16, -0.70710678118654813), (0.8660254037844386, -1.110223024625158e-16, -0.50000000000000067), (0.96592582628906842, -5.7469372616863249e-17, -0.25881904510252152), (1.0000000000000004, -1.6150773046340863e-31, -7.273661547324616e-16), (0.96592582628906898, 5.7469372616862941e-17, 0.25881904510252013), (0.86602540378443948, 1.1102230246251556e-16, 0.49999999999999956), (0.70710678118654846, 1.5700924586837747e-16, 0.70710678118654735), (0.500000000000001, 1.9229626863835641e-16, 0.86602540378443871), (0.25881904510252179, 2.1447861848524064e-16, 0.96592582628906853), (9.49410759657493e-16, 2.2204460492503141e-16, 1.0000000000000004))]
        return self._style(points)

    @property
    def semi_circle(self):
        points = [[[6.123233995736766e-17, 2.2204460492503131e-16, 1.0], [-0.25881904510252068, 2.1447861848524059e-16, 0.96592582628906831], [-0.49999999999999989, 1.9229626863835641e-16, 0.86602540378443871], [-0.70710678118654746, 1.5700924586837752e-16, 0.70710678118654757], [-0.8660254037844386, 1.1102230246251568e-16, 0.50000000000000011], [-0.9659258262890682, 5.7469372616863126e-17, 0.25881904510252096], [-1.0, 6.2900117310782151e-32, 2.8327694488239898e-16], [-0.96592582628906842, -5.7469372616863015e-17, -0.25881904510252046], [-0.86602540378443893, -1.1102230246251559e-16, -0.49999999999999972], [-0.70710678118654791, -1.5700924586837747e-16, -0.70710678118654735], [-0.50000000000000044, -1.9229626863835638e-16, -0.8660254037844386], [-0.25881904510252129, -2.1447861848524059e-16, -0.96592582628906831], [-5.330771254230592e-16, -2.2204460492503136e-16, -1.0000000000000002]]]
        return self._style(points)

    @property
    def pyramid(self):
        points = [[[0.0, 0.53995001316070557, 0.0], [-1.0, -1.0, 1.0], [-1.0, -1.0, -1.0], [0.0, 0.53995001316070557, 0.0], [-1.0, -1.0, -1.0], [1.0, -1.0, -1.0], [0.0, 0.53995001316070557, 0.0], [1.0, -1.0, -1.0], [1.0, -1.0, 1.0], [0.0, 0.53995001316070557, 0.0], [1.0, -1.0, 1.0], [-1.0, -1.0, 1.0]]]
        return self._style(points)

    @property
    def cube(self):
        points = [[[-1.0, 1.0, -1.0], [1.0, 1.0, -1.0], [1.0, 1.0, 1.0], [-1.0, 1.0, 1.0], [-1.0, 1.0, -1.0], [-1.0, -1.0, -1.0], [1.0, -1.0, -1.0], [1.0, 1.0, -1.0], [1.0, -1.0, -1.0], [1.0, -1.0, 1.0], [1.0, 1.0, 1.0], [1.0, -1.0, 1.0], [-1.0, -1.0, 1.0], [-1.0, 1.0, 1.0], [-1.0, -1.0, 1.0], [-1.0, -1.0, -1.0]]]
        return self._style(points)

    @property
    def cross(self):
        points = [[[-0.33310534961812344, 0.0, 0.33310534961812344], [-0.99931604885437031, 0.0, 0.33310534961812344], [-0.99931604885437031, 0.0, -0.33310534961812344], [-0.33310534961812344, 0.0, -0.33310534961812344], [-0.33310534961812344, 0.0, -0.99931604885437031], [0.33310534961812344, 0.0, -0.99931604885437031], [0.33310534961812344, 0.0, -0.33310534961812344], [0.99931604885437031, 0.0, -0.33310534961812344], [0.99931604885437031, 0.0, 0.33310534961812344], [0.33310534961812344, 0.0, 0.33310534961812344], [0.33310534961812344, 0.0, 0.99931604885437031], [-0.33310534961812344, 0.0, 0.99931604885437031], [-0.33310534961812344, 0.0, 0.33310534961812344]]]
        return self._style(points)

    @property
    def arrow_single(self):
        points = [[[-1.0, 0.0, 1.0], [-1.0, 0.0, -1.0], [-2.0, 0.0, -1.0], [0.0, 0.0, -3.0], [2.0, 0.0, -1.0], [1.0, 0.0, -1.0], [1.0, 0.0, 1.0], [-1.0, 0.0, 1.0]]]
        return self._style(points)

    @property
    def arrow_double(self):
        points = [[[-1.0, 0.0, 2.0], [-1.0, 0.0, -1.0], [-2.0, 0.0, -1.0], [0.0, 0.0, -3.0], [2.0, 0.0, -1.0], [1.0, 0.0, -1.0], [1.0, 0.0, 2.0], [2.0, 0.0, 2.0], [0.0, 0.0, 4.0], [-2.0, 0.0, 2.0], [-1.0, 0.0, 2.0]]]
        return self._style(points)

    @property
    def arrow_triple(self):
        points = [[[-1.0, 0.0, 1.0], [-1.0, 0.0, 3.0], [-2.0, 0.0, 3.0], [0.0, 0.0, 5.0], [2.0, 0.0, 3.0], [1.0, 0.0, 3.0], [1.0, 0.0, -3.0], [2.0, 0.0, -3.0], [0.0, 0.0, -5.0], [-2.0, 0.0, -3.0], [-1.0, 0.0, -3.0], [-1.0, 0.0, -1.0], [-3.0, 0.0, -1.0], [-3.0, 0.0, -2.0], [-5.0, 0.0, 0.0], [-3.0, 0.0, 2.0], [-3.0, 0.0, 1.0], [-1.0, 0.0, 1.0]]]
        return self._style(points)

    @property
    def arrow_quad(self):
        points = [[[-1.0, 0.0, -1.0], [-1.0, 0.0, -3.0], [-2.0, 0.0, -3.0], [0.0, 0.0, -5.0], [2.0, 0.0, -3.0], [1.0, 0.0, -3.0], [1.0, 0.0, -1.0], [3.0, 0.0, -1.0], [3.0, 0.0, -2.0], [5.0, 0.0, 0.0], [3.0, 0.0, 2.0], [3.0, 0.0, 1.0], [1.0, 0.0, 1.0], [1.0, 0.0, 3.0], [2.0, 0.0, 3.0], [0.0, 0.0, 5.0], [-2.0, 0.0, 3.0], [-1.0, 0.0, 3.0], [-1.0, 0.0, 1.0], [-3.0, 0.0, 1.0], [-3.0, 0.0, 2.0], [-5.0, 0.0, 0.0], [-3.0, 0.0, -2.0], [-3.0, 0.0, -1.0], [-1.0, 0.0, -1.0]]]
        return self._style(points)

    def __getattr__(self, style):
        if hasattr(self, style):
            return getattr(self, style)
        else:
            raise AttributeError("No style information found: %s" % style)

    def __getitem__(self, style):
        return self.__getattr__(style)
