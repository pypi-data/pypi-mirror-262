"""
Octree for searching for objects by coordinates
"""
import math

from cmlibs.maths.vectorops import sub, dot


class Octree:
    """
    Octree for searching for objects by coordinates
    """

    def __init__(self, tolerance=None):
        """
        :param tolerance: If supplied, tolerance to use, or None to compute as 1.0E-12.
        """
        self._tolerance = 1.0E-12 if tolerance is None else tolerance
        self._coordinates = None
        # Octree is either leaf with _object, or has 2**self._dimension children
        self._object = None
        # exactly 2^self._dimension children, cycling in lowest x index fastest
        self._children = None

    def _location_match(self, x):
        return all([math.fabs(x[i] - self._coordinates[i]) < self._tolerance for i in range(3)])

    def _child_index_lookup(self, x):
        switch = [0 if x[i] < self._coordinates[i] else 1 for i in range(3)]
        return switch[0] + 2 * switch[1] + 4 * switch[2]

    def _sq_distance(self, x):
        diff = sub(x, self._coordinates)
        return dot(diff, diff)

    def _find_object_by_coordinates(self, x, nearest=False):
        """
        Find the closest existing object with |x - ox| < tolerance.
        :param x: 3 coordinates in a list.
        :return: nearest distance, nearest object or None, None if none found.
        """
        if self._coordinates is not None and self._location_match(x):
            return 0.0, self._object

        if not nearest and self._children is None:
            return None, None

        if nearest and self._coordinates is None:
            return math.inf, None

        if nearest and self._children is None:
            return 0.0, self._object

        index = self._child_index_lookup(x)
        sq_distance_, object_ = self._children[index]._find_object_by_coordinates(x, nearest)

        if nearest:
            sq_distance = self._sq_distance(x)
            if sq_distance_ < sq_distance:
                return sq_distance_, object_
            else:
                return sq_distance, self._object

        return None, object_

    def tolerance(self):
        return self._tolerance

    def find_object_by_coordinates(self, x):
        """
        Find the closest existing object with |x - ox| < tolerance.
        :param x: 3 coordinates in a list.
        :return: nearest object or None if not found.
        """
        distance, nearest_object = self._find_object_by_coordinates(x)
        return nearest_object

    def find_nearest_object_by_coordinates(self, x):
        distance, nearest_object = self._find_object_by_coordinates(x, True)
        return nearest_object

    def insert_object_at_coordinates(self, x, obj):
        """
        Add object at coordinates to octree.

        :param x: 3 coordinates in a list.
        :param obj: object to store with coordinates.
        """
        if self._coordinates is None:
            self._coordinates = x
            self._object = obj
        else:
            if self._location_match(x):
                self._object = obj
            else:
                index = self._child_index_lookup(x)
                if self._children is None:
                    self._children = [Octree() for _ in range(8)]

                self._children[index].insert_object_at_coordinates(x, obj)

    def __repr__(self):
        if self._children is None:
            return f'\tleaf {self._coordinates}\n'

        return f'{self._coordinates} - \n' + ''.join([f'{c}' for c in self._children])
