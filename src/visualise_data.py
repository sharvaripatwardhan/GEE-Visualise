import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


def plot_choropleth(gdf, year, column="NTL_mean", cmap="magma"):
    """
    Plot a metric by district for a given year
    
    Args:
        gdf : GeoDataFrame containing columns: 'year', 'district', metric column, and geometry
        year : Year to display (e.g., 2014-2024)
        column : Column name to plot (default: "NTL_mean")
        cmap : Matplotlib colormap name (default: "magma")
    
    Returns:
        fig, ax : matplotlib figure and axis objects
    """   
    # Filter data for selected year
    gdf_year = gdf[gdf["year"] == year].copy()
    
    if gdf_year.empty:
        print(f"No data available for year {year}")
        return None, None
    
    if column not in gdf_year.columns:
        print(f"Column '{column}' not found in GeoDataFrame")
        print(f"Available columns: {', '.join(gdf_year.columns)}")
        return None, None 
    print(f"Number of districts: {gdf_year['district'].nunique()}")
    
    # Create plot
    fig, ax = plt.subplots(figsize=(10, 10))
    gdf_year.plot(
        column=column,
        cmap=cmap,
        legend=True,
        edgecolor="black",
        linewidth=0.3,
        ax=ax
    )
    
    # Add district labels
    for idx, row in gdf_year.iterrows():
        centroid = row.geometry.centroid
        ax.text(
            centroid.x,
            centroid.y,
            row["district"],       
            fontsize=8,
            color="white",        
            ha="center",
            va="center"
        )
    
    ax.set_title(f"{column} by District — {year}", fontsize=14)
    ax.axis("off")
    plt.show()
    
    return fig, ax


def plot_choropleth_log(gdf, year, column="NTL_mean", cmap="magma"):
    """
    Plot a metric by district for a given year using logarithmic scale
    
    Args:
        gdf : GeoDataFrame containing columns: 'year', 'district', metric column, and geometry
        year : Year to display (e.g., 2014-2024)
        column : Column name to plot (default: "NTL_mean")
        cmap : Matplotlib colormap name (default: "magma")
    
    Returns:
        fig, ax : matplotlib figure and axis objects
    """   
    # Filter data for selected year
    gdf_year = gdf[gdf["year"] == year].copy()
    
    if gdf_year.empty:
        print(f"No data available for year {year}")
        return None, None
    
    if column not in gdf_year.columns:
        print(f"Column '{column}' not found in GeoDataFrame")
        print(f"Available columns: {', '.join(gdf_year.columns)}")
        return None, None
    
    print(f"Number of districts: {gdf_year['district'].nunique()}")
    
    # Create plot
    fig, ax = plt.subplots(figsize=(10, 10))
    gdf_year.plot(
        column=column,
        cmap=cmap,
        legend=True,
        edgecolor="black",
        linewidth=0.3,
        norm=LogNorm(),
        ax=ax
    )
    
    # Add district labels
    for idx, row in gdf_year.iterrows():
        centroid = row.geometry.centroid
        ax.text(
            centroid.x,
            centroid.y,
            row["district"],       
            fontsize=8,
            color="white",        
            ha="center",
            va="center"
        )
    
    ax.set_title(f"{column} (LogNorm) by District — {year}", fontsize=14)
    ax.axis("off")
    plt.show()
    
    return fig, ax    