from src.nepal_palika_finder.locator import PalikaLocator
import json
import warnings

def run_query_example():
    """
    Demonstrates how to use the PalikaLocator, which automatically finds
    and loads its own bundled data file.
    """
    try:
        # Suppress the ambiguity warning for the demonstration
        warnings.filterwarnings("ignore", message="Ambiguous Palika name*")
        locator = PalikaLocator()
        warnings.resetwarnings() # Reset warnings for other parts of a larger app
    except Exception as e:
        print(f"Error initializing locator: {e}")
        print("Please ensure the 'local_levels.fgb' file is located in 'src/nepal_palika_finder/data/'.")
        return

    # --- Step 2: Run Example Queries by Coordinate ---
    print("\n\n--- Testing with coordinates from various locations in Nepal ---")

    points_to_test = {
        "Kathmandu (Pashupatinath)": {"lat": 27.7107, "lon": 85.3484},
        "Pokhara (Peace Pagoda)": {"lat": 28.2045, "lon": 83.9470},
    }

    for name, coords in points_to_test.items():
        lat, lon = coords["lat"], coords["lon"]
        print(f"\nQuerying for: {name} (Lat: {lat}, Lon: {lon})")

        containing_feature = locator.find_palika(latitude=lat, longitude=lon)

        if containing_feature:
            properties = containing_feature.get('properties', {})
            palika_name = properties.get('PALIKA') or properties.get('GaPa_NaPa', 'N/A')
            district_name = properties.get('DISTRICT') or properties.get('District', 'N/A')

            print(f"  ✅  Result: Found in {palika_name}, {district_name} District.")
        else:
            print("  ❌  Result: Point is not within any Gaupalika/Nagarpalika in the dataset.")

    # --- Step 3: Search for Palikas by Name (Autocomplete) ---
    print("\n\n--- Testing Palika search by name (for autocomplete) ---")
    search_query = "pata"
    print(f"\nSearching for Palikas starting with '{search_query}'...")
    search_results = locator.search_palikas_by_name(search_query)

    if search_results:
        print(f"  ✅  Found {len(search_results)} results:")
        for props in search_results:
            palika = props.get('PALIKA') or props.get('GaPa_NaPa', 'N/A')
            district = props.get('DISTRICT') or props.get('District', 'N/A')
            print(f"    - {palika}, {district}")
    else:
        print(f"  ❌  No results found for '{search_query}'.")

    # --- Step 4: Get Geometry by Name ---
    print("\n\n--- Testing geometry retrieval by name ---")
    
    palika_to_find = "Kathmandu"
    print(f"\nQuerying for geometry of: '{palika_to_find}'")
    geometry = locator.get_palika_geometry_by_name(palika_to_find)
    if geometry:
        print(f"  ✅  Result: Found geometry for {palika_to_find}. Type: {geometry.get('type')}")
    else:
        print(f"  ❌  Result: Could not find geometry for {palika_to_find}.")
        
    # --- Step 5: Get a list of all Palikas ---
    print("\n\n--- Testing retrieval of all Palikas ---")

    # Example 1: Get properties only (default)
    all_palikas_properties = locator.get_all_palikas()
    print(f"\nFound {len(all_palikas_properties)} Palikas (properties only).")
    print("  ✅  Example of first 3:")
    for props in all_palikas_properties[:3]:
        palika = props.get('PALIKA') or props.get('GaPa_NaPa', 'N/A')
        district = props.get('DISTRICT') or props.get('District', 'N/A')
        print(f"    - {palika}, {district}")

    # Example 2: Get full features with geometry
    all_palikas_features = locator.get_all_palikas(include_geometry=True)
    print(f"\nFound {len(all_palikas_features)} Palikas (with geometry).")
    if all_palikas_features:
        first_feature = all_palikas_features[0]
        print(f"  ✅  Example of first feature keys: {list(first_feature.keys())}")
        print(f"  ✅  It has properties: {first_feature.get('properties')}")
        print(f"  ✅  And a geometry of type: '{first_feature.get('geometry', {}).get('type')}'")


if __name__ == "__main__":
    run_query_example()