import Tkinter
import cPickle

def CreateImageArray(root, grid):
  RED = [255, 0, 0]
  BLUE = [0, 0, 255]
  WHITE = [255, 255, 255]

  imageArray = ''
  for rowData in grid:
    rowImageArray = '{'
    for value in rowData:
      if value == 1:
        (r, g, b) = RED
      elif value == 2:
        (r, g, b) = BLUE
      else:
        (r, g, b) = WHITE

      hexcode = "#%02x%02x%02x" % (r,g,b)
      rowImageArray += ' ' + hexcode
    rowImageArray += '}'
    imageArray += ' ' + rowImageArray

  return imageArray

if __name__ == '__main__':
  # Read in pickled data
  inputFile = open('grid.p', 'rb')
  grid = cPickle.load(inputFile)
  inputFile.close()

  # Create bitmap
  root = Tkinter.Tk()
  gridWidth = len(grid)
  gridHeight = len(grid[0])
  photo = Tkinter.PhotoImage(width=gridWidth, height=gridHeight)

  imageArray = CreateImageArray(root, grid)    
  photo.put(imageArray)

  label = Tkinter.Label(root, image=photo)
  label.grid()
  root.mainloop()
