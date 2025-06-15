
# Nepal Palika Finder

A fast, efficient Python tool to find the corresponding Nepali Gaupalika (Rural Municipality) or Nagarpalika (Municipality) from a given latitude and longitude coordinate or by its name.


## Installation

You can install this library directly from GitHub into your project using `pip`. This is the recommended way to use it as a dependency.


`
pip install git+https://github.com/konishon/nepal-palika-finder.git
`

## Usage

After installation, you can import and use the `PalikaLocator` in your own Python scripts. It works without any configuration.

```python
from nepal_palika_finder.locator import PalikaLocator

# 1. Create an instance of the locator. This takes a few seconds
#    as it builds spatial and name indexes in memory.
print("Initializing Palika Locator...")
locator = PalikaLocator()
print("Initialization complete.")
```

### 1. Find Palika by Coordinates

You can find the properties of a Palika that contains a specific geographic point.

```python
# Coordinates for Kathmandu Durbar Square
ktm_coords = {"lat": 27.7041, "lon": 85.3074}

result = locator.find_palika(latitude=ktm_coords["lat"], longitude=ktm_coords["lon"])

if result:
    properties = result.get('properties', {})
    palika_name = properties.get('PALIKA', 'N/A')
    district_name = properties.get('DISTRICT', 'N/A')
    print(f"✅ Found in: {palika_name}, {district_name} District.")
else:
    print("❌ Point not found in any Palika in the dataset.")
```

### 2. Search Palikas by Name (for Autocomplete)

Use `search_palikas_by_name` to get a list of potential matches for a partial name. This is ideal for user interface autocomplete fields.

```python
search_query = "pata"
results = locator.search_palikas_by_name(search_query, limit=5)

print(f"Found {len(results)} Palikas starting with '{search_query}':")
for properties in results:
    palika_name = properties.get('PALIKA', 'N/A')
    district_name = properties.get('DISTRICT', 'N/A')
    print(f"  - {palika_name}, {district_name}")

```

### 3. Get Palika Geometry

You can retrieve the raw GeoJSON geometry of a Palika using either coordinates or its name.

#### By Coordinates
```python
# Coordinates for Biratnagar
biratnagar_coords = {"lat": 26.4525, "lon": 87.2718}

geometry = locator.get_palika_geometry(
    latitude=biratnagar_coords["lat"], 
    longitude=biratnagar_coords["lon"]
)

if geometry:
    print(f"✅ Found geometry for point. Type: {geometry.get('type')}")
```

#### By Name
Since some Palika names are not unique across Nepal, you can provide an optional `district_name` to ensure you get the correct one.

```python
import json

# Find geometry for 'Bhimdatta' in 'Kanchanpur' district
palika_name = "Bhimdatta"
district_name = "Kanchanpur"

geometry = locator.get_palika_geometry_by_name(palika_name, district_name=district_name)

if geometry:
    print(f"✅ Found geometry for {palika_name}, {district_name}.")
    # The result is a Python dictionary representing the GeoJSON geometry
    print(f"   GeoJSON (partial): {json.dumps(geometry)[:100]}...")
else:
    print(f"❌ Geometry not found for {palika_name} in {district_name}.")
```

# Local Development
If you want to contribute to or modify the project itself, follow these steps.
## 1. Clone the Repository

```bash
git clone https://github.com/konishon/nepal-palika-finder.git
cd nepal-palika-finder
```

## 2. Project Structure
```bash

nepal-palika-finder/
└── src/
    └── nepal_palika_finder/
        ├── data/
        │   └── local_levels.fgb  
        ├── __init__.py
        ├── data_loader.py
        └── locator.py
```

## 3. Install Dependencies with Poetry

```bash
poetry install
```

This will create a virtual environment and install all necessary libraries for development.

## 4. Run the Example
To run the example queries defined in example.py, execute:

```bash
poetry run python example.py
```
