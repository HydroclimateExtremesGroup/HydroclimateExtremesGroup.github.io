# Rainfall Polygon Analysis Tool

A Python tool for analyzing gridded rainfall data within specified polygon boundaries. This tool is designed for hydrological research and can extract rainfall statistics from NetCDF files within watershed or administrative boundaries.

## Features

- **NetCDF Data Support**: Load and analyze gridded rainfall data in NetCDF format
- **Polygon Masking**: Extract data within specified polygon boundaries (shapefile format)
- **Comprehensive Statistics**: Calculate total, mean, maximum, minimum, and standard deviation of rainfall
- **Area-Weighted Analysis**: Account for latitude-dependent grid cell areas
- **Temporal Analysis**: Analyze time series data when available
- **Visualization**: Generate maps and time series plots
- **Export Results**: Save statistics and time series data to CSV files

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from rainfall_polygon_analysis import RainfallPolygonAnalyzer

# Initialize analyzer
analyzer = RainfallPolygonAnalyzer(
    netcdf_path="path/to/rainfall_data.nc",
    shapefile_path="path/to/polygon.shp"
)

# Load and analyze data
analyzer.load_data()
stats = analyzer.calculate_rainfall_stats()
analyzer.plot_results()
```

### Command Line Usage

```bash
python rainfall-polygon-analysis.py
```

## Input Data

### NetCDF Rainfall Data
The tool expects NetCDF files with:
- Longitude and latitude coordinates
- Rainfall/precipitation data variable
- Optional time dimension for temporal analysis

### Polygon Shapefile
- Standard shapefile format (.shp, .shx, .dbf, .prj)
- Any coordinate reference system (will be reprojected as needed)
- Single or multiple polygon features

## Output

The tool generates:
1. **Statistics Summary**: Total, mean, max, min, and standard deviation of rainfall
2. **Visualization**: Maps showing original data, masked data, and time series
3. **CSV Files**: Detailed results and time series data
4. **Console Output**: Real-time analysis progress and results

## Example Output

```
RAINFALL ANALYSIS RESULTS
==================================================
total_precipitation: 1250.45
mean_precipitation: 2.34
max_precipitation: 15.67
min_precipitation: 0.0
std_precipitation: 3.21
area_weighted_mean: 2.41
```

## Applications

- **Watershed Analysis**: Calculate rainfall within watershed boundaries
- **Flood Risk Assessment**: Analyze precipitation patterns in flood-prone areas
- **Climate Research**: Study rainfall variability across different regions
- **Water Resource Management**: Assess water availability in specific areas
- **Urban Planning**: Analyze rainfall patterns in urban areas

## Technical Details

- **Coordinate Systems**: Automatically handles different CRS and reprojects as needed
- **Memory Efficient**: Uses xarray for efficient handling of large NetCDF files
- **Spatial Operations**: Uses GeoPandas and Shapely for robust geometric operations
- **Visualization**: Cartopy for publication-quality maps

## Requirements

- Python 3.7+
- See requirements.txt for specific package versions

## Author

Hydroclimate Extremes Research Group  
University of Wisconsin-Madison  
Civil and Environmental Engineering

## License

This project is part of the open-source research tools developed by the Hydroclimate Extremes Research Group.

