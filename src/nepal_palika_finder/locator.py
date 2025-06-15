import fiona
from pathlib import Path
from shapely.geometry import shape, Point
from shapely.strtree import STRtree
from .data_loader import get_fgb_path # Import the new helper
import warnings

class PalikaLocator:
    """
    A fast locator to find the Nepalese Gaupalika/Nagarpalika for a given point or by name.
    Data is bundled directly with the package.
    """
    def __init__(self):
        """
        Initializes the locator by loading the bundled FlatGeobuf data,
        building a high-performance spatial index, and creating a name index for text search.
        """
        fgb_file = get_fgb_path()

        print("Loading Nepal local level data...")
        with fiona.open(fgb_file, 'r') as collection:
            self.features = list(collection)
        
        print("Building spatial index...")
        geometries = [shape(feature['geometry']) for feature in self.features]
        self.tree = STRtree(geometries)
        print(f"Spatial index built successfully with {len(self.features)} Palikas.")

        print("Building name index for text-based search...")
        self.name_index = []
        for idx, feature in enumerate(self.features):
            properties = feature.get('properties', {})
            palika_name = properties.get('PALIKA') or properties.get('GaPa_NaPa')
            district_name = properties.get('DISTRICT') or properties.get('District')
            
            if palika_name and district_name:
                self.name_index.append({
                    'name_lower': palika_name.lower(),
                    'district_lower': district_name.lower(),
                    'original_properties': properties,
                    'feature_index': idx
                })
        print("Name index built. Ready for queries.")

    def find_palika(self, latitude: float, longitude: float):
        """
        Finds the Gaupalika/Nagarpalika feature that contains the given coordinates.

        Returns:
            dict: The full feature dictionary from the underlying data source, or None.
        """
        point = Point(longitude, latitude)
        possible_matches_indices = self.tree.query(point)

        for idx in possible_matches_indices:
            candidate_geometry = shape(self.features[idx]['geometry'])
            if candidate_geometry.contains(point):
                return self.features[idx]

        return None

    def get_palika_geometry(self, latitude: float, longitude: float):
        """
        Finds the Gaupalika/Nagarpalika for the given coordinates and returns its
        geometry as a GeoJSON dictionary.

        Returns:
            dict: A GeoJSON dictionary representing the geometry of the found Palika,
                  or None if no Palika is found.
        """
        containing_feature = self.find_palika(latitude, longitude)

        if containing_feature and 'geometry' in containing_feature:
            return containing_feature['geometry']

        return None

    def search_palikas_by_name(self, query: str, limit: int = 10):
        """
        Searches for Palikas where the name starts with the given query string.
        This is ideal for implementing autocomplete features. Search is case-insensitive.

        Args:
            query (str): The partial or full name of the Palika to search for.
            limit (int): The maximum number of results to return.

        Returns:
            list[dict]: A list of Palika property dictionaries that match the query.
        """
        if not query:
            return []
            
        lower_query = query.lower()
        results = []
        for item in self.name_index:
            if item['name_lower'].startswith(lower_query):
                results.append(item['original_properties'])
                if len(results) >= limit:
                    break
        return results

    def get_palika_geometry_by_name(self, palika_name: str, district_name: str = None):
        """
        Finds a Palika by its exact name and returns its geometry. Since Palika names
        can be duplicated across districts, providing a district name is recommended for accuracy.

        Args:
            palika_name (str): The exact, case-insensitive name of the Palika.
            district_name (str, optional): The exact, case-insensitive name of the District
                                           to resolve ambiguities. Defaults to None.

        Returns:
            dict: A GeoJSON dictionary of the Palika's geometry, or None if not found or ambiguous.
        """
        lower_palika_name = palika_name.lower()
        
        candidates = [
            item for item in self.name_index if item['name_lower'] == lower_palika_name
        ]
        
        if not candidates:
            return None

        if len(candidates) > 1 and district_name:
            lower_district_name = district_name.lower()
            candidates = [
                item for item in candidates if item['district_lower'] == lower_district_name
            ]

        if len(candidates) == 1:
            feature_index = candidates[0]['feature_index']
            return self.features[feature_index]['geometry']
        
        if len(candidates) > 1:
            districts = [c['original_properties'].get('DISTRICT') for c in candidates]
            warnings.warn(
                f"Ambiguous Palika name '{palika_name}'. "
                f"Found in multiple districts: {districts}. "
                "Please specify a district_name to get a unique result."
            )

        return None