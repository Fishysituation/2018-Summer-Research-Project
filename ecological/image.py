from PIL import Image

#load in data
runNo = 1    
gridSize = 100

targetSize = 1000

filein = 'runs/run' + str(runNo) + '.out'
fileout = "images/run" + str(runNo)

f = open(filein, 'r')


#colour code for mean to nice
colours = [
    (0,81,255),     # blue allC
    (255,26,0),     # red allD
    (227,255,0),    # yellow Random
    (0,255,4),      # green TFT
    (255,141,0),    # orange PAV
    
]

data = f.readlines()
splitData = []

temp = []
for line in data:
    if len(line) < gridSize:
        splitData.append(temp)
        temp = []
    else:
        temp.append(line)



for n in range(0, len(splitData)):
    img = Image.new('RGB', (gridSize, gridSize), "black")
    pixels = img.load() # create the pixel map

    for i in range(img.size[0]):    # for every col:
        for j in range(img.size[1]):    # For every row
            pixels[i,j] = colours[int(splitData[n][j][i])] # set the colour accordingly

    img = img.resize((targetSize, targetSize))

    img.show()
    #pause before doing next image
    input()
    img.save(fileout + str(n) + ".jpg")
