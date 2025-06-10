# Nepal Palika Finder

A fast, efficient Python tool to find the corresponding Nepali Gaupalika (Rural Municipality) or Nagarpalika (Municipality) from a given latitude and longitude coordinate.


## Installation

You can install this library directly from GitHub into your project using `pip`. This is the recommended way to use it as a dependency.


`
pip install git+https://github.com/konishon/nepal-palika-finder.git
`

## Usage

After installation, you can import and use the `PalikaLocator` in your own Python scripts. It works without any configuration.

```python
from nepal_palika_finder.locator import PalikaLocator

# 1. Create an instance of the locator.
print("Initializing Palika Locator...")
locator = PalikaLocator()
print("Initialization complete.")

# 2. Find the Palika for a given coordinate.
#    Coordinates for Kathmandu Durbar Square
ktm_coords = {"lat": 27.7041, "lon": 85.3074}

print(f"\nSearching for coordinates: {ktm_coords}")
result = locator.find_palika(latitude=ktm_coords["lat"], longitude=ktm_coords["lon"])

# 3. Print the results.
if result:
    properties = result.get('properties', {})
    palika_name = properties.get('PALIKA', properties.get('GaPa_NaPa', 'N/A'))
    district_name = properties.get('DISTRICT', properties.get('District', 'N/A'))
    
    print(f"✅ Found in: {palika_name}, {district_name} District.")
else:
    print("❌ Point not found in any Palika in the dataset.")

```
# Local Development
If you want to contribute to or modify the project itself, follow these steps.
## 1. Clone the Repository

```bash
git clone [https://github.com/konishon/nepal-palika-finder.git](https://github.com/konishon/nepal-palika-finder.git)
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
To run the example queries defined in main.py, execute:

```bash
poetry run python example.py
```

