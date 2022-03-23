import sys

sys.path.append("..")
import unittest
import os
from spherical2images.utils import get_mapillary_points_bbox, build_mapillary_sequence, write_geojson


class Test_points(unittest.TestCase):
    def test_points(self):
        """Test the returned points"""
        access_token = os.environ.get("MAPILLARY_ACCESS_TOKEN")
        if access_token is not None:
            bbox = [-83.2263319287, 42.3489816308, -83.2230326577, 42.3507715447]
            fc_points = get_mapillary_points_bbox(bbox)
            write_geojson("tests/fixtures/points.geojson",fc_points)
            fc_lines = build_mapillary_sequence(fc_points)
            write_geojson("tests/fixtures/sequences.geojson",fc_lines)
            # fc_points=[]
            # fc_lines=[]
            num_point = len(fc_points)
            self.assertGreater(num_point, 0, f"Function got {num_point} points, ok")
            num_lines = len(fc_lines)
            self.assertGreater(
                num_lines, 0, f"Function got {num_lines} lineStrings, ok"
            )
