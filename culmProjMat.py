from pygame.locals import * # pygame stuff
from model import * # contains matrix stuff
import matplotlib.pyplot as plt # plotting stuff
import matplotlib.backends.backend_agg as agg # plt stuff
import pandas as pd # reading and processing csv
import numpy as np # matrix manipulation
import pygame as pog # you've seen this in the Unit 2 Culminating Project...
import pygame_widgets as pogW # sliders, buttons, and textboxes
import time, pylab, matplotlib # various stuff

matplotlib.use('Agg') # initialization stuff
bgCol = (255, 255, 255)
w, h = (1080, 720)
globalLb = 1.0
pastLb = globalLb 
globalN = 6
pastN = globalN
dataInd = 0

df = pd.read_csv('down_up.csv') # data cleaning from CSV
for i in df.columns:
  if 'Unnamed' in i or i == 'pic':
    del df[i]
data = df.values[:, 1:]
(p, m) = data.shape
data = data.reshape(p, m, 1)
X = np.arange(0, m)
X = X.reshape(X.shape[0], 1) # turning a 1D array into an m x 1 vector

def laText(weightV): # turn weightV (weight vector) from an array into a LaTeX-formatted string; weightV is an n x 1 vector
  ret = r'$\^{y}='

  ret += '{:.4}'.format(weightV[0][0])

  if weightV.shape[0] > 1:
    if weightV[1][0] > 0:
      ret += '+{:.4}x'.format(weightV[1][0])
    elif weightV[1][0] < 0:
      ret += '{:.4}x'.format(weightV[1][0])

  for i in range(2, weightV.shape[0]):
    roundVar = weightV[i][0]
    if roundVar > 0:
      ret += '+{:.4}x^'.format(roundVar) + '{' + str(i) + '}'
    elif roundVar < 0:
      ret += '{:.4}x^'.format(roundVar) + '{' + str(i) + '}'
  ret += '$'
  return ret, ret[7:-1] + ' (λ=1e{:.2}, Num. Features={}, Contestant={})'.format(float(lbSlider.getValue()) - 5, globalN, df['name'][dataInd]) # first return value is the latex-formatted string, the second value is the plain string for pasting into Desmos


def clickPlot(): # changes the plot when the 'Random Graph' button is pressed
  global dataInd, X, data
  dataInd = np.random.randint(0, data.shape[0])
  plotToScreen(X, data[dataInd], globalN)

def plotToScreen(x, y, n): # mostly copied code; plot the data, plot the curve of best fit, put the plt plot onto a screen in PyGame
  global surf, globalLb
  fig = pylab.figure(figsize=[6, 6], dpi=100) # figsize in inches
  ax = fig.gca()
  m = Model(x, y, n, globalLb) # plotting stuff and finding curve of best fit onto a plt plot, which is then rendered into a PyGame window
  m.normal()
  ax.plot(m.x, np.dot(m.acts, m.weightV))
  ax.plot(m.x, m.y)
  #ax.scatter(m.x, m.y)
  fmtTxt, plainText = laText(m.weightV) # we want both since we put the LaTeX formatted text on the window and the plain text in the terminal/command prompt

  # matplotlib doesn't do line wrapping well so I had to make some ugly line-breaking code so you can see the entire equation on the screen
  splitInd = 70 # amount of characters the first line will be before a line break
  try: # this breaks the line where a sign (+ or -) is found to make the equation look better in the window
    splitInd += fmtTxt[splitInd:].index('+')
  except:
    try:
      splitInd += fmtTxt[splitInd:].index('-')
    except:
      splitInd = -1 # if there is no sign after character 70, ignore line breaking

  if splitInd != -1:
    plt.figtext(0.5, 0.04, fmtTxt[:splitInd] + '$', wrap=False, horizontalalignment='center', fontsize=8)
    plt.figtext(0.5, 0.01, '$' + fmtTxt[splitInd:], wrap=False, horizontalalignment='center', fontsize=8)
  else:
    plt.figtext(0.5, 0.04, fmtTxt, wrap=False, horizontalalignment='center', fontsize=8)
  print(plainText)

  canvas = agg.FigureCanvasAgg(fig) # render plt plot
  canvas.draw()
  size = canvas.get_width_height()

  renderer = canvas.get_renderer() 
  raw_data = renderer.tostring_rgb()
  surf = pog.image.fromstring(raw_data, size, "RGB")
  plt.close('all')

pog.init() # pygame stuff

window = pog.display.set_mode((w, h), DOUBLEBUF)
screen = pog.display.get_surface()
screen = pog.display.set_mode((w, h))
titleText = pogW.TextBox(window, (1080-450)/2, 15, 450, 25, fontSize=15)
surf = None

lbSlider = pogW.Slider(window, 650, 150, 300, 10, min=0, max=10, step=0.1) # interactive sliders and stuff in the program
nSlider = pogW.Slider(window, 650, 250, 300, 10, min=0, max=10, step=1)
lbText = pogW.TextBox(window, 650, 110, 150, 25, fontSize=15) # lambda text
nText = pogW.TextBox(window, 650, 210, 200, 25, fontSize=15) # n text
pText = pogW.TextBox(window, 75, 77, 200, 25, fontSize=15) # player text
dataB = pogW.Button(window, 100, 650, 200, 50, text='Random Graph', margin=2, onClick=clickPlot)
pog.display.set_caption('aiyah bruh')
pog.display.flip()

plotToScreen(X, data[dataInd], globalN)

run = True
while run: # actions to run throughout the program: update the screen if lambda or num. features is changed or if the dataset is changed (basically when the user interacts with the window)
  if pastLb != globalLb or pastN != globalN: # window only does normal equation if the parameters update since normal equation is computationally expensive
    plotToScreen(X, data[dataInd], globalN)
    #frameNum = 0

  time.sleep(0.01) # max framerate is 100 FPS
  events = pog.event.get()
  screen.fill(bgCol) # white BG color
  screen.blit(surf, (0, 30)) # render plt plot on surface to PyGame window

  pastLb = globalLb
  globalLb = 10 ** (float(lbSlider.getValue()) - 5) # changing lambda based on lbSlider's position
  lbSlider.listen(events)
  lbSlider.draw()
  lbText.setText('Current λ: 1e{}'.format(round(float(lbSlider.getValue()) - 5, 2)))
  lbText.draw()

  pastN = globalN
  globalN = int(nSlider.getValue()) + 1 # changing number of features (n) based on nSlider's position
  nSlider.listen(events)
  nSlider.draw()
  nText.setText('Current polynomial order: {}'.format(globalN-1))
  nText.draw()

  pText.setText('Contestant; {}'.format(df['name'][dataInd])) # changes textbox above plt plot saying contestant name
  pText.draw()

  dataB.listen(events)
  dataB.draw()

  titleText.setText('    Salamilympics Pushup Curve Fitting Project (Matrices and stuff)') # title
  titleText.draw()
  pog.display.update() # show all of this garbage onto the real display

  for event in events:
    if event.type == pog.QUIT:
      run = False
      pog.quit()

