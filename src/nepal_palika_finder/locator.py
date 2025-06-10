import fiona
from pathlib import Path
from shapely.geometry import shape, Point
from shapely.strtree import STRtree
from .data_loader import get_fgb_path # Import the new helper

class PalikaLocator:
    """
    A fast locator to find the Nepalese Gaupalika/Nagarpalika for a given point.
    Data is bundled directly with the package.
    """
    def __init__(self):
        """
        Initializes the locator by loading the bundled FlatGeobuf data
        and building a high-performance spatial index.
        """
        fgb_file = get_fgb_path()

        print("Loading Nepal local level data and building spatial index...")
        with fiona.open(fgb_file, 'r') as collection:
            self.features = list(collection)
            geometries = [shape(feature['geometry']) for feature in self.features]

        self.tree = STRtree(geometries)
        print(f"Index built successfully with {len(self.features)} Palikas. Ready for queries.")

    def find_palika(self, latitude: float, longitude: float):
        """
        Finds the Gaupalika/Nagarpalika feature that contains the given coordinates.
        """
        point = Point(longitude, latitude)
        possible_matches_indices = self.tree.query(point)

        for idx in possible_matches_indices:
            candidate_geometry = shape(self.features[idx]['geometry'])
            if candidate_geometry.contains(point):
                return self.features[idx]

        return None
