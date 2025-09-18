#!/usr/bin/env python3
"""
Rainfall Polygon Analysis Tool
==============================

This script analyzes gridded rainfall data (NetCDF format) within a specified polygon boundary.
It calculates various rainfall statistics including total precipitation, maximum values, and
temporal patterns within the polygon area.

Author: Hydroclimate Extremes Research Group
University of Wisconsin-Madison
"""

import xarray as xr
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from shapely.geometry import Point
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class RainfallPolygonAnalyzer:
    """
    A class to analyze rainfall data within polygon boundaries.
    """
    
    def __init__(self, netcdf_path, shapefile_path):
        """
        Initialize the analyzer with data file paths.
        
        Parameters:
        -----------
        netcdf_path : str
            Path to the NetCDF rainfall data file
        shapefile_path : str
            Path to the polygon shapefile
        """
        self.netcdf_path = netcdf_path
        self.shapefile_path = shapefile_path
        self.rainfall_data = None
        self.polygon = None
        self.masked_data = None
        
    def load_data(self):
        """Load NetCDF rainfall data and polygon shapefile."""
        print("Loading rainfall data...")
        self.rainfall_data = xr.open_dataset(self.netcdf_path)
        print(f"Rainfall data loaded: {self.rainfall_data}")
        
        print("Loading polygon data...")
        self.polygon = gpd.read_file(self.shapefile_path)
        print(f"Polygon loaded: {self.polygon.shape[0]} features")
        print(f"CRS: {self.polygon.crs}")
        
    def inspect_data(self):
        """Display information about the loaded datasets."""
        print("\n" + "="*50)
        print("RAINFALL DATA INSPECTION")
        print("="*50)
        print(f"Dimensions: {dict(self.rainfall_data.dims)}")
        print(f"Data variables: {list(self.rainfall_data.data_vars)}")
        print(f"Coordinates: {list(self.rainfall_data.coords)}")
        
        # Print data variable details
        for var in self.rainfall_data.data_vars:
            print(f"\n{var}:")
            print(f"  Shape: {self.rainfall_data[var].shape}")
            print(f"  Attributes: {dict(self.rainfall_data[var].attrs)}")
        
        print("\n" + "="*50)
        print("POLYGON DATA INSPECTION")
        print("="*50)
        print(f"Columns: {list(self.polygon.columns)}")
        print(f"Bounds: {self.polygon.total_bounds}")
        print(f"CRS: {self.polygon.crs}")
        
    def create_mask(self):
        """Create a boolean mask for grid points within the polygon."""
        print("Creating spatial mask...")
        
        # Get coordinate arrays
        if 'longitude' in self.rainfall_data.coords:
            lons = self.rainfall_data.longitude.values
            lats = self.rainfall_data.latitude.values
        elif 'lon' in self.rainfall_data.coords:
            lons = self.rainfall_data.lon.values
            lats = self.rainfall_data.lat.values
        else:
            # Try to find coordinate variables
            coord_vars = [var for var in self.rainfall_data.coords if 'lon' in var.lower() or 'lat' in var.lower()]
            print(f"Available coordinate variables: {coord_vars}")
            raise ValueError("Could not find longitude/latitude coordinates")
        
        # Create meshgrid
        lon_grid, lat_grid = np.meshgrid(lons, lats)
        
        # Convert to points
        points = [Point(lon, lat) for lon, lat in zip(lon_grid.ravel(), lat_grid.ravel())]
        
        # Create GeoDataFrame of points
        points_gdf = gpd.GeoDataFrame(geometry=points, crs='EPSG:4326')
        
        # Ensure both datasets have the same CRS
        if self.polygon.crs != points_gdf.crs:
            self.polygon = self.polygon.to_crs(points_gdf.crs)
        
        # Perform spatial join to find points within polygon
        points_in_polygon = gpd.sjoin(points_gdf, self.polygon, how='inner', predicate='within')
        
        # Create boolean mask
        mask = np.zeros(lon_grid.shape, dtype=bool)
        for idx in points_in_polygon.index:
            i, j = np.unravel_index(idx, lon_grid.shape)
            mask[i, j] = True
        
        print(f"Found {np.sum(mask)} grid points within polygon")
        return mask
    
    def calculate_rainfall_stats(self, variable_name=None):
        """Calculate rainfall statistics within the polygon."""
        print("Calculating rainfall statistics...")
        
        # Create mask
        mask = self.create_mask()
        
        # Find the main rainfall variable if not specified
        if variable_name is None:
            # Look for common rainfall variable names
            rainfall_vars = [var for var in self.rainfall_data.data_vars 
                           if any(keyword in var.lower() for keyword in ['rain', 'precip', 'prcp', 'rainfall'])]
            if rainfall_vars:
                variable_name = rainfall_vars[0]
                print(f"Using rainfall variable: {variable_name}")
            else:
                print("Available variables:", list(self.rainfall_data.data_vars))
                variable_name = input("Please specify the rainfall variable name: ")
        
        # Get rainfall data
        rainfall = self.rainfall_data[variable_name]
        
        # Apply mask to all time steps
        masked_rainfall = rainfall.where(mask)
        
        # Calculate statistics
        stats = {}
        
        # Spatial statistics (across all time)
        stats['total_precipitation'] = float(masked_rainfall.sum().values)
        stats['mean_precipitation'] = float(masked_rainfall.mean().values)
        stats['max_precipitation'] = float(masked_rainfall.max().values)
        stats['min_precipitation'] = float(masked_rainfall.min().values)
        stats['std_precipitation'] = float(masked_rainfall.std().values)
        
        # Temporal statistics (if time dimension exists)
        if 'time' in rainfall.dims:
            stats['total_time_steps'] = int(rainfall.sizes['time'])
            stats['time_series_mean'] = float(masked_rainfall.mean(dim=['latitude', 'longitude']).mean().values)
            stats['max_instantaneous'] = float(masked_rainfall.max(dim=['latitude', 'longitude']).max().values)
            
            # Time series data
            time_series = masked_rainfall.mean(dim=['latitude', 'longitude'])
            stats['time_series'] = time_series.to_pandas()
        
        # Area-weighted statistics
        if 'latitude' in rainfall.coords:
            # Calculate area weights (approximate)
            lat_weights = np.cos(np.radians(rainfall.latitude))
            area_weights = lat_weights * mask
            area_weights = area_weights / area_weights.sum()
            
            area_weighted_mean = (rainfall * area_weights).sum().values
            stats['area_weighted_mean'] = float(area_weighted_mean)
        
        self.masked_data = masked_rainfall
        return stats
    
    def plot_results(self, variable_name=None, save_path=None):
        """Create visualization of the analysis results."""
        print("Creating visualization...")
        
        if variable_name is None:
            rainfall_vars = [var for var in self.rainfall_data.data_vars 
                           if any(keyword in var.lower() for keyword in ['rain', 'precip', 'prcp', 'rainfall'])]
            variable_name = rainfall_vars[0] if rainfall_vars else list(self.rainfall_data.data_vars)[0]
        
        rainfall = self.rainfall_data[variable_name]
        
        # Create figure with subplots
        fig = plt.figure(figsize=(15, 10))
        
        # Plot 1: Original data (first time step if available)
        ax1 = plt.subplot(2, 2, 1, projection=ccrs.PlateCarree())
        if 'time' in rainfall.dims:
            data_to_plot = rainfall.isel(time=0)
        else:
            data_to_plot = rainfall
        
        im1 = data_to_plot.plot(ax=ax1, transform=ccrs.PlateCarree(), 
                               cmap='Blues', add_colorbar=False)
        self.polygon.boundary.plot(ax=ax1, color='red', linewidth=2, transform=ccrs.PlateCarree())
        ax1.set_title('Original Rainfall Data')
        ax1.coastlines()
        ax1.add_feature(cfeature.BORDERS)
        ax1.gridlines()
        
        # Plot 2: Masked data
        ax2 = plt.subplot(2, 2, 2, projection=ccrs.PlateCarree())
        if self.masked_data is not None:
            if 'time' in self.masked_data.dims:
                masked_to_plot = self.masked_data.isel(time=0)
            else:
                masked_to_plot = self.masked_data
            im2 = masked_to_plot.plot(ax=ax2, transform=ccrs.PlateCarree(), 
                                     cmap='Blues', add_colorbar=False)
        self.polygon.boundary.plot(ax=ax2, color='red', linewidth=2, transform=ccrs.PlateCarree())
        ax2.set_title('Masked Rainfall Data')
        ax2.coastlines()
        ax2.add_feature(cfeature.BORDERS)
        ax2.gridlines()
        
        # Plot 3: Time series (if available)
        if 'time' in rainfall.dims and self.masked_data is not None:
            ax3 = plt.subplot(2, 2, 3)
            time_series = self.masked_data.mean(dim=['latitude', 'longitude'])
            time_series.plot(ax=ax3)
            ax3.set_title('Time Series (Area Average)')
            ax3.set_xlabel('Time')
            ax3.set_ylabel('Precipitation')
            ax3.grid(True)
        else:
            ax3 = plt.subplot(2, 2, 3)
            ax3.text(0.5, 0.5, 'No time dimension found', 
                    ha='center', va='center', transform=ax3.transAxes)
            ax3.set_title('Time Series (Not Available)')
        
        # Plot 4: Statistics summary
        ax4 = plt.subplot(2, 2, 4)
        ax4.axis('off')
        
        # Add statistics text
        stats_text = f"""
        Rainfall Statistics Summary
        =========================
        
        Total Precipitation: {self.stats.get('total_precipitation', 'N/A'):.2f}
        Mean Precipitation: {self.stats.get('mean_precipitation', 'N/A'):.2f}
        Max Precipitation: {self.stats.get('max_precipitation', 'N/A'):.2f}
        Min Precipitation: {self.stats.get('min_precipitation', 'N/A'):.2f}
        Std Precipitation: {self.stats.get('std_precipitation', 'N/A'):.2f}
        
        Area Weighted Mean: {self.stats.get('area_weighted_mean', 'N/A'):.2f}
        """
        
        ax4.text(0.1, 0.9, stats_text, transform=ax4.transAxes, 
                fontsize=10, verticalalignment='top', fontfamily='monospace')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to: {save_path}")
        
        plt.show()
    
    def save_results(self, output_path):
        """Save analysis results to CSV file."""
        print(f"Saving results to: {output_path}")
        
        # Convert stats to DataFrame
        results_df = pd.DataFrame([self.stats])
        
        # Add metadata
        results_df['analysis_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        results_df['netcdf_file'] = self.netcdf_path
        results_df['shapefile'] = self.shapefile_path
        
        # Save to CSV
        results_df.to_csv(output_path, index=False)
        print("Results saved successfully!")
        
        # Save time series if available
        if 'time_series' in self.stats and self.stats['time_series'] is not None:
            ts_path = output_path.replace('.csv', '_timeseries.csv')
            self.stats['time_series'].to_csv(ts_path)
            print(f"Time series saved to: {ts_path}")

def main():
    """Main function to run the rainfall polygon analysis."""
    
    # File paths
    netcdf_path = "/Users/daniel/Documents/RainyDay/Milwaukee_2025/NEXRAD_DPR_data/NEXRAD_update/GriddedDPR20250811_corrected_wct461.nc"
    shapefile_path = "/Users/daniel/Documents/RainyDay/Milwaukee_2025/MMSD-Planning-Area-Outline-WGS84.shp"
    
    # Initialize analyzer
    analyzer = RainfallPolygonAnalyzer(netcdf_path, shapefile_path)
    
    try:
        # Load data
        analyzer.load_data()
        
        # Inspect data
        analyzer.inspect_data()
        
        # Calculate statistics
        analyzer.stats = analyzer.calculate_rainfall_stats()
        
        # Print results
        print("\n" + "="*50)
        print("RAINFALL ANALYSIS RESULTS")
        print("="*50)
        for key, value in analyzer.stats.items():
            if key != 'time_series':  # Skip time series in printout
                print(f"{key}: {value}")
        
        # Create visualization
        analyzer.plot_results(save_path="rainfall_analysis_results.png")
        
        # Save results
        analyzer.save_results("rainfall_analysis_results.csv")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

