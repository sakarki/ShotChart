%matplotlib inline
import requests
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

shot_chart_url = 'http://stats.nba.com/stats/shotchartdetail?CFID=33&CFPAR;'\
                'AMS=2014-15&ContextFilter;=&ContextMeasure;=FGA&DateFrom;=&D;'\
                'ateTo=&GameID;=&GameSegment;=&LastNGames;=0&LeagueID;=00&Loca;'\
                'tion=&MeasureType;=Base&Month;=0&OpponentTeamID;=0&Outcome;=&'\
                'PaceAdjust=N&PerMode;=PerGame&Period;=0&PlayerID;=201935&Plu;'\
                'sMinus=N&Position;=&Rank;=N&RookieYear;=&Season;=2014-15&Seas;'\
                'onSegment=&SeasonType;=Regular+Season&TeamID;=0&VsConferenc;'\
                'e=&VsDivision;=&mode;=Advanced&showDetails;=0&showShots;=1&sh;'\
                'owZones=0'

#get the webpage containing the data
response = requests.get(shot_chart_url)
#grab the headers to be used as column headers for our data frame
headers = response.json()['resultsSets'][0]['headers']
#grab the shot chart data
shots = response.json()['resultsSets'][0]['rowSet']

shot_df = pd. DataFrame(shots, columns=headers)
#View the head of the DataFrame and all its columns
from IPython.display import display
with pd.option_context('display.max_columns', None): display(shot_df.head())

sns.set_style("white")
sns.set_color_codes()
plt.figure(figsize=(12,11))
plt.scatter(shot_df.LOC_X, shot_df.LOC_Y)
plt.show()

right = shot_df[shot_df.SHOT_ZONE_AREA == "Right Side(R)"]
plt.figure(figsize= (12,11))
plt.scatter(right.LOC_X, right.LOC_Y)
plt.xlim(-300,300)
plt.ylim(-100,500)
plt.show()

from matplotlib.patches import Circle, Rectangle, Arc

def draw_court(ax=None, color='black', lw=2, outer_lines=False):
    #If an axes object isn't provided to plot onto, just get current one
    if ax is None:
        ax = plt.gca()

    #Creating the various parts of an Nba basketball court

    #Creating the basketball hoop
    #1 foot = 10 points/pixels
    #Diameter of a hoop is 18" so it has a radius of 9", which is a value 7.5 in our coordinate system
    hoop = Circle((0,0), radius=7.5, linewidth=lw, color=color, fill=False)

    #creating backboard
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

    #The paint
    #creating the outer box of the plain, width=16ft, height=19ft
    outer_box = Rectangle((-80,-47.5), 160, 190, linewidth=lw, color=color, fill=False)

    #creating the inner box of the paint, width = 12ft, height = 19ft
    inner_box = Rectangle((-60,-47.5), 120, 190, linewidth=lw, color=color, fill=False)

    #freethrow top and bottom arc
    top_free_throw = Arc((0,142.5), 120, 120, theta1=0, theta2=180)

    bottom_free_throw = Arc((0,142.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color, linestyle='dashed')

    #Restricted zone
    restricted = Arc((0,0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)

    #3pt line
    #creating the side 3pt lines, they are 14ft long before they begin to arc
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw, color=color)

    corner_three_b = Rectangle ((220, -47.5), 0, 140, linewidth = lw, color=color)

    #3pt arc
    three_arc = Arc((0,0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)

    #Center court
    center_outer_arc = Arc((0,422.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color)
    center_inner_arc = Arc((0,422.5), 40, 40, theta1=180, theta2=0, linewidth=lw, color=color)

    #List of court elements to be plotted on the axes
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                      bottom_free_throw, restricted, corner_three_a,
                      corner_three_b, three_arc, center_outer_arc,
                      center_inner_arc]

    if outer_lines:
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw, color=color, fill=False)
        court_elements.append(outer_lines)
        #This draws the half court line, baseline, and the out of bound lines on the sides

    #adding court elemts onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax

#drawing the court
plt.figure(figsize=(12,11))
draw_court(outer_lines=true)
plt.xlim(300,-300)
plt.show()

plt.figure(figsize=(12,11))
plt.scatter(shot_df.LOC_X, shot_df.LOC_Y)
draw_court()
# Adjust plot limits to just fit in half court
plt.xlim(-250,250)
# Descending values along th y axis from bottom to top
# in order to place the hoop by the top of plot
plt.ylim(422.5, -47.5)
# get rid of axis tick labels
# plt.tick_params(labelbottom=False, labelleft=False)
plt.show()

# create our jointplot
joint_shot_chart = sns.jointplot(shot_df.LOC_X, shot_df.LOC_Y, stat_func=None,
                                 kind='scatter', space=0, alpha=0.5)

joint_shot_chart.fig.set_size_inches(12,11)

# A joint plot has 3 Axes, the first one called ax_joint
# is the one we want to draw our court onto and adjust some other settings
ax = joint_shot_chart.ax_joint
draw_court(ax)

# Adjust the axis limits and orientation of the plot in order
# to plot half court, with the hoop by the top of the plot
ax.set_xlim(-250,250)
ax.set_ylim(422.5, -47.5)

# Get rid of axis labels and tick marks
ax.set_xlabel('')
ax.set_ylabel('')
ax.tick_params(labelbottom='off', labelleft='off')

# Add a title
ax.set_title('James Harden FGA \n2014-15 Reg. Season',
             y=1.2, fontsize=18)

# Add Data Scource and Author
ax.text(-250,445,'Data Source: stats.nba.com'
        '\nAuthor: Savvas Tjortjoglou (savvastjortjoglou.com)',
        fontsize=12)

plt.show()

import urllib.request
# we pass in the link to the image as the 1st argument
# the 2nd argument tells urlretrieve what we want to scrape
pic = urllib.request.urlretrieve("http://stats.nba.com/media/players/230x185/201935.png",
                                    "201935.png")

# urlretrieve returns a tuple with our image as the first
# element and imread reads in the image as a
# mutlidimensional numpy array so matplotlib can plot it
harden_pic = plt.imread(pic[0])

# plot the image
plt.imshow(harden_pic)
plt.show()

from matplotlib.offsetbox import  OffsetImage

# create our jointplot

# get our colormap for the main kde plot
# Note we can extract a color from cmap to use for
# the plots that lie on the side and top axes
cmap=plt.cm.YlOrRd_r

# n_levels sets the number of contour lines for the main kde plot
joint_shot_chart = sns.jointplot(shot_df.LOC_X, shot_df.LOC_Y, stat_func=None,
                                 kind='kde', space=0, color=cmap(0.1),
                                 cmap=cmap, n_levels=50)

joint_shot_chart.fig.set_size_inches(12,11)

# A joint plot has 3 Axes, the first one called ax_joint
# is the one we want to draw our court onto and adjust some other settings
ax = joint_shot_chart.ax_joint
draw_court(ax)

# Adjust the axis limits and orientation of the plot in order
# to plot half court, with the hoop by the top of the plot
ax.set_xlim(-250,250)
ax.set_ylim(422.5, -47.5)

# Get rid of axis labels and tick marks
ax.set_xlabel('')
ax.set_ylabel('')
ax.tick_params(labelbottom='off', labelleft='off')

# Add a title
ax.set_title('James Harden FGA \n2014-15 Reg. Season',
             y=1.2, fontsize=18)

# Add Data Scource and Author
ax.text(-250,445,'Data Source: stats.nba.com'
        '\nAuthor: Savvas Tjortjoglou (savvastjortjoglou.com)',
        fontsize=12)

# Add Harden's image to the top right
# First create our OffSetImage by passing in our image
# and set the zoom level to make the image small enough
# to fit on our plot
img = OffsetImage(harden_pic, zoom=0.6)
# Pass in a tuple of x,y coordinates to set_offset
# to place the plot where you want, I just played around
# with the values until I found a spot where I wanted
# the image to be
img.set_offset((625,621))
# add the image
ax.add_artist(img)

plt.show()

#print systemn versions
import sys
print('Python version:', sys.version_info)
import IPython
print('IPython version:', IPython.__version__)
print('Requests verstion', requests.__version__)
print('Urllib.requests version', urllib.request.__version__)
import matplotlib as mpl
print('Matplotlib version:', mpl.__version__)
print('Seaborn version:', sns.__version__)
print('Pandas version:', pd.__version__)
