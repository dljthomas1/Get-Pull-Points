def get_pull_points(poly, n, plot_map = False, plot_legend = False):

    '''
    This function will take a polygon, and try to segment it into an n approximately equally
    sized sections, returning the centre points of each section.
    
    If your polygon is bounday of a pyshical place (eg a city, town, etc) you should first 
    convert the coordinate reference system (CRS) to a local metric projection. See the Jupyter
 	 notebook on my Github profile as an example.

    poly            Polgon on which you wish to generate 'pull points'.
    n (int)         The number of sections you wish to split the polygon up into
    plot_map        True/False. Do you want to plot a map of the results
    plot legend    Do you want to plot the legend of the map?
    '''

    # Import required modules
    import matplotlib.cm as cm
    from sklearn.cluster import KMeans
    import matplotlib.pyplot as plt
    plt.style.use('ggplot')
    from shapely.geometry import Point
    from shapely.geometry import Polygon
    import geopandas as gpd
    import numpy as np

    # Function to create uniform points throughout the polygon
    def get_uniform_points(poly, num_points):
        min_x, min_y, max_x, max_y =poly.bounds
        x = (np.linspace(min_x,max_x,num_points))
        y=  (np.linspace(min_y,max_y,num_points))
        xx,yy = np.meshgrid(x,y,sparse=True)
        xx = xx.reshape((np.prod(xx.shape),))
        yy = yy.reshape((np.prod(yy.shape),))
        points = []

        for x in xx:
          for y in yy:
            random_point = Point([x, y])
            if (random_point.within(poly)):
              points.append(list(random_point.coords))
        return points

    uniform_points = get_uniform_points(poly,20) 

    # Creates a pandas GeoDataFrame of the uniform points.
    df = gpd.GeoDataFrame(uniform_points, columns = ['geometry'])
    df.geometry = df.geometry.apply(lambda x: Point(x))

    # Set up Kmeans clustering to create approximately n equally sized clusters
    from sklearn.cluster import KMeans
    df['x'] = df.geometry.apply(lambda x: x.x)
    df['y'] = df.geometry.apply(lambda x: x.y)
    X = df[['y','x']].values

    # Carry out clustering 
    kmean = KMeans(n_clusters = n).fit(X)
    df['pull_point'] = kmean.predict(X).tolist()

    # Find the centre point of each cluster
    pull_points = df.groupby(['pull_point']).mean().reset_index()
    pull_points = gpd.GeoDataFrame(pull_points,geometry = gpd.points_from_xy(pull_points.x, pull_points.y))

    if plot_map == True:

        # Set up colour iterations
        color=iter(cm.rainbow(np.linspace(0,1,n))) 

        # Map out our clustering
        fig, ax = plt.subplots(figsize = (10,10))
        gpd.GeoSeries(poly).plot(ax = ax, alpha = 0.5) # Plot the polygon

        # Go through each colour and plot it
        for i in range(n):
            c = next(color)
            temp = df[df.pull_point == i]
            temp.plot(ax = ax, color = c, alpha = 0.95, markersize = 4, label = 'grid point: %s' % (temp.pull_point.unique()[0]))

        # Plot the 
        pull_points.plot(ax = ax, color = 'black', markersize = 35 , label = 'pull points')

        if plot_legend == True:
          plt.legend()
        plt.show()

    return pull_points
