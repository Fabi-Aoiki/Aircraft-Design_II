from PIL import Image

xMin = 0.21
xMax = 0.69
xVal = 0.689
yMin = 10
yMax = 29

DiaPath = "Aircraft-Design_II/ChartReaderFolder/bitmap.jpg"

def AutoChartReader(DiaPath, xMin, xMax, xVal, yMin, yMax, IsLog = False): 
    Img = Image.open(DiaPath)
    ImgWidth, ImgHeight = Img.size

    xValPix = ImgWidth * (xVal-xMin) / (xMax-xMin)
    ListBlackPix = []

    for y in range(1, ImgHeight):
        r, g, b = Img.getpixel((xValPix, y))
        if r + g + b == 0:
            ListBlackPix.append(y)

    yValPix = round(sum(ListBlackPix) / len(ListBlackPix))  
    ResultValue = (ImgHeight-yValPix) / ImgHeight * (yMax-yMin) + yMin
    return(ResultValue)

# res = AutoChartReader(DiaPath, xMin, xMax, xVal, yMin, yMax)
# print(res)