import pandas as pd
import geopandas as gpd
import json
from shapely.geometry import shape
from typing import Optional, Union, Dict, Any


def keep_columns(dataframe, columns):
    """ 
    Returns a new DataFrame containing only the specified columns
    
    Args:
        dataframe (pd.DataFrame): The input DataFrame
        columns (List[str]): List of column names to keep

    Returns:
        pd.DataFrame: A new DataFrame with only the specified columns
    """
    existing_cols = [col for col in columns if col in dataframe.columns]
    return dataframe[existing_cols].copy()


def std_cols(dataframe, columns):
    """
    Standarsizes text in columns: strips whitespace, replaces multiple spaces with one, and converts all text to lowercase
    
    Args:
        dataframe (pd.DataFrame): The input DataFrame
        columns (List[str]): List of column names to standardize

    Returns:
        pd.DataFrame: DataFrame with standardized columns
    """
    df = dataframe.copy()
    for col in columns:
        if col in df.columns:
            df[col] = (df[col].astype(str)
                             .str.strip()
                             .str.lower()  
                             .str.replace(r"\s+", " ", regex=True))
    return df


def make_numeric(dataframe, columns, dtype):
    """
    Changes column type to numeric 

    Args:
        dataframe (pd.DataFrame): The input DataFrame
        columns (List[str]): List of column names to convert to numeric
        dtype (type): The target numeric type (e.g., float, int, 'Int64'). Defaults to float.

    Returns:
        pd.DataFrame: DataFrame with the specified columns converted to numeric
    """
    df = dataframe.copy()
    for col in columns:
        if col in df.columns:
            series = pd.to_numeric(df[col], errors="coerce")
            
            # Apply the specific dtype if needed 
            if dtype == 'Int64' or dtype == pd.Int64Dtype:
                 df[col] = series.astype('Int64')
            elif dtype == int:
                 df[col] = series.astype(int, errors='ignore')
            else:
                 df[col] = series
                 
    return df


def geo_to_geom(x: Union[str, Dict[str, Any], float]) -> Optional[shape]:
    """
    Helper function to robustly convert a GeoJSON string, dict, or NaN 
    from the '.geo' column into a Shapely geometry object
    """
    if pd.isna(x):
        return None
        
    # If the entry is already a dictionary 
    if isinstance(x, dict):
        try:
            return shape(x)
        except Exception:
            return None
            
    # If the entry is a string (GeoJSON string)
    if isinstance(x, str):
        try:
            return shape(json.loads(x))
        except Exception:
            return None
            
    return None 


def create_geo_df(dataframe, geo_column = ".geo", crs = "EPSG:4326", area_crs = "EPSG:6933"):
    """
    Converts a standard DataFrame with a GeoJSON column into a GeoDataFrame,
    assigns a CRS, and calculates the area in square kilometers

    Args:
        dataframe (pd.DataFrame): The input DataFrame containing GeoJSON data.
        geo_column (str): The name of the column containing GeoJSON strings/dicts (default: '.geo')
        crs (str): The coordinate reference system of the GeoJSON data (default: 'EPSG:4326')
        area_crs (str): The equal-area CRS to use for area calculation (default: 'EPSG:6933')

    Returns:
        gpd.GeoDataFrame: The resulting GeoDataFrame with a 'geometry' column and an 'area_sqkm' column
    """
    df = dataframe.copy()
    geo_column = ".geo"

    if geo_column not in df.columns:
        raise RuntimeError(f"Required column '{geo_column}' not found in the dataset.")
        
    df["geometry"] = df[geo_column].apply(geo_to_geom)  # Apply GeoJSON parsing function  
    gdf = gpd.GeoDataFrame(df, geometry="geometry", crs=crs)  # Create the GeoDataFrame and assign CRS    
    gdf = gdf.set_geometry("geometry")  # Set the geometry column

    print(f"GeoDataFrame created with CRS: {gdf.crs}")
    return gdf


def weighted_mean(series, weight_series):
    """
    Calculates the weighted mean of a series
    """
    series = series.astype('float64')
    weight_series = weight_series.astype('float64')
    
    if weight_series.sum() == 0 or weight_series.isna().all():
        return np.nan
    return (series * weight_series).sum() / weight_series.sum()
