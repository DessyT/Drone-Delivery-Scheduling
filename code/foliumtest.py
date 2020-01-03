# import folium package
import folium

map = folium.Map(location = [57.151954, -2.091723], width=750, height=500, zoom_start=15)

folium.Marker([57.151954, -2.091723], popup="Depot").add_to(map)
folium.Marker([57.152437, -2.095494], popup="Morrisons").add_to(map)

folium.PolyLine(locations = [(57.151954, -2.091723), (57.152437, -2.095494)],
                line_opacity = 0.5).add_to(map)

map.save("maps/my_map1.html")
