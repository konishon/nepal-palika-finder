from src.nepal_palika_finder.locator import PalikaLocator
import json

def run_query_example():
    """
    Demonstrates how to use the PalikaLocator, which automatically finds
    and loads its own bundled data file.
    """
    try:
        locator = PalikaLocator()
    except Exception as e:
        print(f"Error initializing locator: {e}")
        print("Please ensure the 'local_levels.fgb' file is located in 'src/nepal_palika_finder/data/'.")
        return

    # --- Step 2: Run Example Queries ---
    print("\n--- Testing with coordinates from various locations in Nepal ---")

    points_to_test = {
        "Kathmandu (Pashupatinath)": {"lat": 27.7107, "lon": 85.3484},
        "Pokhara (Peace Pagoda)": {"lat": 28.2045, "lon": 83.9470},
        "Lumbini (World Peace Pagoda)": {"lat": 27.4962, "lon": 83.2766},
        "Mount Everest Summit": {"lat": 27.9881, "lon": 86.9250}
    }

    for name, coords in points_to_test.items():
        lat, lon = coords["lat"], coords["lon"]
        print(f"\nQuerying for: {name} (Lat: {lat}, Lon: {lon})")

        containing_feature = locator.find_palika(latitude=lat, longitude=lon)

        if containing_feature:
            properties = containing_feature.get('properties', {})
            palika_name = properties.get('PALIKA', properties.get('GaPa_NaPa', 'N/A'))
            district_name = properties.get('DISTRICT', properties.get('District', 'N/A'))

            print(f"  ✅  Result: Found in {palika_name}, {district_name} District.")
        else:
            print("  ❌  Result: Point is not within any Gaupalika/Nagarpalika in the dataset.")

    # --- Step 3: Get Geometry as GeoJSON ---
    print("\n\n--- Testing geometry retrieval as GeoJSON ---")
    
    biratnagar_coords = {"lat": 26.4525, "lon": 87.2718}
    print(f"\nQuerying for geometry of: Biratnagar (Lat: {biratnagar_coords['lat']}, Lon: {biratnagar_coords['lon']})")

    geometry_geojson = locator.get_palika_geometry(latitude=biratnagar_coords["lat"], longitude=biratnagar_coords["lon"])

    if geometry_geojson:
        print(f"  ✅  Result: Found geometry. Type: {geometry_geojson.get('type')}")
        # To avoid printing a massive object, let's just show a snippet.
        geometry_str = json.dumps(geometry_geojson)
        print(f"     GeoJSON (first 100 chars): {geometry_str[:100]}...")
    else:
        print("  ❌  Result: Geometry not found for the given point.")


if __name__ == "__main__":
    run_query_example()