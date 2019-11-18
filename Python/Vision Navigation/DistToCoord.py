import math

def get_distance_meters(aLocation1, aLocation2):
	"""
	Returns the ground distance in metres between two LocationGlobal objects.
	This method is an approximation, and will not be accurate over large distances and close to the 
	earth's poles.
	"""
    
	dlat = aLocation2.lat - aLocation1.lat
	dlong = aLocation2.lon - aLocation1.lon
	return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5

def get_location_meters(original_location, dNorth, dEast, alt):
	"""
	Returns a LocationGlobal object containing the latitude/longitude `dNorth` and `dEast` metres from the 
	specified `original_location`. The returned Location has the same `alt` value
	as `original_location`.
	The function is useful when you want to move the vehicle around specifying locations relative to 
	the current vehicle position.
	The algorithm is relatively accurate over small distances (10m within 1km) except close to the poles.
	For more information see:
	http://gis.stackexchange.com/questions/2951/algorithm-for-offsetting-a-latitude-longitude-by-some-amount-of-meters
	"""
	earth_radius=6378137.0 #Radius of "spherical" earth
	#Coordinate offsets in radians
	dLat = dNorth/earth_radius
	dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))

	#New position in decimal degrees
	newlat = original_location.lat + (dLat * 180/math.pi)
	newlon = original_location.lon + (dLon * 180/math.pi)
	return LocationGlobalRelative(newlat, newlon, alt)