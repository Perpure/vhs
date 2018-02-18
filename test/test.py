from PIL import Image, ImageDraw 
rezolutionx=16
rezolutiony=9

source= Image.open('source.jpg')
image = Image.open('test.jpg')
width = image.size[0]
height = image.size[1]	
pix = image.load()
color = (255, 255, 255)
color2 = (0,0,0)
firstx=0
firsty=0
lastx=0
lasty=0
source=source.resize((width,height))
rez = Image.new('RGB', (width, height), color)
draw = ImageDraw.Draw(rez)
for i in range(width):
    for j in range(height):
        a = pix[i, j][0]
        b = pix[i, j][1]
        c = pix[i, j][2]
        if a>150:
            if not(firstx):
                firstx=i
                firsty=j
            lastx=i
            lasty=j
x=lastx-firstx+1
y=lasty-firsty+1
print(x/y)
if (x/y)>(rezolutionx/rezolutiony):
    e=(x/y)-(rezolutionx/rezolutiony)
    w=x
    h=y
    w1=0
    h1=0
    while True:
        w-=1
        if (w/h)<=(rezolutionx/rezolutiony):
            if (rezolutionx/rezolutiony)-(w/h)<((w+1)/h)-(rezolutionx/rezolutiony):
                e=(rezolutionx/rezolutiony)-(w/h)
                w1=w
                h1=h
                break
            else:
                e=(rezolutionx/rezolutiony)-((w+1)/h)
                w1=w+1
                h1=h
                break
    w=x
    h=y
    while True:
        h+=1
        if (w/h)<=(rezolutionx/rezolutiony):
            if (rezolutionx/rezolutiony)-(w/h)<(w/(h-1))-(rezolutionx/rezolutiony):
                if ((rezolutionx/rezolutiony)-(w/h))<e:
                    w1=w
                    h1=h
                break
            else:
                if ((rezolutionx/rezolutiony)-(w/(h-1)))<e:
                    w1=w
                    h1=h-1
                break
else:
    e=(rezolutionx/rezolutiony)-(x/y)
    w=x
    h=y
    w1=0
    h1=0
    while True:
        w+=1
        if (w/h)<=(rezolutionx/rezolutiony):
            if (rezolutionx/rezolutiony)-(w/h)<((w-1)/h)-(rezolutionx/rezolutiony):
                e=(rezolutionx/rezolutiony)-(w/h)
                w1=w
                h1=h
                break
            else:
                e=(rezolutionx/rezolutiony)-((w-1)/h)
                w1=w-1
                h1=h
                break
    w=x
    h=y
    while True:
        h-=1
        if (w/h)<=(rezolutionx/rezolutiony):
            if (rezolutionx/rezolutiony)-(w/h)<(w/(h+1))-(rezolutionx/rezolutiony):
                if ((rezolutionx/rezolutiony)-(w/h))<e:
                    w1=w
                    h1=h
                break
            else:
                if ((rezolutionx/rezolutiony)-(w/(h+1)))<e:
                    w1=w
                    h1=h+1
                break
lastx=firstx+w1-1
lasty=firsty+h1-1
print(w1/h1)
cropped = source.crop((firstx, firsty, lastx, lasty))
if w1>h1:
    cropped=cropped.rotate(90,expand=True)
for i in range(firstx,lastx):
    for j in range(firsty,lasty):
        draw.point((i, j), color2)
cropped = cropped.resize((1080,1920))
rez.save("rez.png")
source.save("source2.jpg")
cropped.save("cropped.jpg")
