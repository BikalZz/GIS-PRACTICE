import geopandas as gpd
from shapely.geometry import LineString, Point
import numpy as np
import matplotlib.pyplot as plt

# Create roads data (LineStrings)
roads_data = [
    {'name': 'Road 1', 'geometry': LineString([(0, 0), (3, 3)])},
    {'name': 'Road 2', 'geometry': LineString([(0, 3), (3, 0)])}
]
roads_gdf = gpd.GeoDataFrame(roads_data, geometry='geometry')

# Create cities data (Points)
cities_data = [
    {'name': 'City A', 'geometry': Point(0.5, 0.3)},
    {'name': 'City B', 'geometry': Point(2.5, 1.2)},
    {'name': 'City C', 'geometry': Point(1.8,1.8)}
]
cities_gdf = gpd.GeoDataFrame(cities_data, geometry='geometry')

# Save to shapefiles (optional)
roads_gdf.to_file(r'session 3/roads.shp')
cities_gdf.to_file(r'session 3/cities.shp')
print("Shapefiles saved successfully.")

def find_nearest_road(city_point, roads_gdf):
    min_distance = np.inf
    nearest_road = None
    closest_point = None
    for _, road in roads_gdf.iterrows():
        print(road)
        distance = city_point.distance(road.geometry)
        print(distance)
        if distance < min_distance:
            min_distance = distance
            nearest_road = road.geometry
            # Find the closest point on the road to the city
            projected = road.geometry.project(city_point)
            closest_point = road.geometry.interpolate(projected)
    return (nearest_road, closest_point, min_distance)

# Apply the function to each city
results = cities_gdf.geometry.apply(lambda p: find_nearest_road(p, roads_gdf))
print(results)

cities_gdf['nearest_road'], cities_gdf['closest_point'], cities_gdf['distance_to_road'] = zip(*results)

print("\nCities GeoDataFrame with nearest roads:")
print(cities_gdf)

# Plotting
fig, ax = plt.subplots(figsize=(8, 6))

# Plot roads
roads_gdf.plot(ax=ax, color='blue', linewidth=2, label='Roads')

# Plot cities
cities_gdf.plot(ax=ax, marker='o', color='red', markersize=50, label='Cities')

# Plot connections to closest points
for _, city in cities_gdf.iterrows():
    ax.plot([city.geometry.x, city.closest_point.x],
            [city.geometry.y, city.closest_point.y],
            color='green', linestyle='--', linewidth=1.5)

# Add labels and legend
ax.set_title("Network of Roads and Cities with Nearest Connections")
ax.set_xlabel("X Coordinate")
ax.set_ylabel("Y Coordinate")
ax.legend()

plt.grid(True, linestyle=':')
plt.show()