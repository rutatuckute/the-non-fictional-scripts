import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

class SarajevoLocations:

    def __init__(self, roads, water, locations):
        
        self.roads = roads
        self.water = water
        self.locations = locations
        self.loc_number = len(self.locations)
        
    def plot_map(self, positions, images, icons):
        
        self.fig, self.ax = plt.subplots(1, figsize=(25,20))
        self.fig.set_facecolor('black')
        
        self.roads.plot(color='#FBBB62', ax=self.ax)
        self.water.plot(color='#40E0D0', ax=self.ax)
        self.locations.plot(kind='scatter',
                            x='Longitude',
                            y='Latitude',
                            ax=self.ax,
                            color='#DE3163',
                            s=90)
        
        index = 0
        for loc, img, ic in zip(positions, images, icons):
            self.annotate_location(index, loc, ic, img)
            index += 1
        
        # Sarajevo coordinates
        self.ax.set_xlim(18.3967, 18.4517)
        self.ax.set_ylim(43.8376, 43.8751)
        self.ax.set_aspect('equal')
        
        self.ax.axis('off')
        
    def load_image(self, image_path):
        
        arr_image = plt.imread(image_path, format='png')
        imagebox_icon = OffsetImage(arr_image, zoom=0.1)
        
        return imagebox_icon
        
    def annotate_location(self, index, text_position, 
                          image, image_position):
        
        self.ax.annotate(
            text = self.locations['Name'][index],
            xy=(self.locations['Longitude'][index], 
                self.locations['Latitude'][index]),
            xytext=text_position,
            textcoords='offset points',
            ha='center',
            color='white',
            backgroundcolor='black',
            bbox=dict(boxstyle='round', fc='black', ec='white', pad=1),
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="angle,angleA=0,angleB=90,rad=3",
                            color='white'),
            fontweight='bold'
        )
        
        self.ax.add_artist(AnnotationBbox(
            offsetbox=image,
            xy=(self.locations['Longitude'][index], 
                 self.locations['Latitude'][index]),
            xybox=image_position,
            xycoords='data',
            boxcoords="offset points",
            pad=0)
        )