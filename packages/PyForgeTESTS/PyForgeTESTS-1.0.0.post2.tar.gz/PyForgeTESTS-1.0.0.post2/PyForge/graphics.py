#  PyForge ©️
#  2023-2024 Izaiyah Stokes <setoichi.dev@gmail.com>
#
#  This software is provided 'as-is', without any express or implied
#  warranty.  In no event will the authors be held liable for any damages
#  arising from the use of this software.
#
#  Permission is granted to anyone to use this software for any purpose,
#  including commercial applications, and to alter it and redistribute it
#  freely, subject to the following restrictions:
#
#  1. The origin of this software must not be misrepresented; you must not
#     claim that you wrote the original software. If you use this software
#     in a product, an acknowledgment in the product documentation would be
#     appreciated but is not required.
#  2. Altered source versions must be plainly marked as such, and must not be
#     misrepresented as being the original software.
#  3. This notice may not be removed or altered from any source distribution.

import random
from screeninfo import get_monitors
from PyForge.const import *
from PyForge.utils import naturalKey
from PyForge.core import pg, os, __versionTag__, gw



def createWindow(windowSize:list|Vector2=Vector2(800,600), FLAG:list|int=[]) -> pg.Surface:
    return pg.display.set_mode((windowSize[0],windowSize[1]), *FLAG)

def setTitle(title:str=f"{__versionTag__}") -> None:
    pg.display.set_caption(title)

def setWindowPos(windowTitle:str, x:int, y:int) -> None:
    try:
        window = gw.getWindowsWithTitle(windowTitle)[0]
        window.moveTo(x, y)
    except IndexError:
        print("Window not found!")

def getMonitorSize() -> Vector2:
    [monitor := m for m in get_monitors()]
    return Vector2(monitor.width,monitor.height)

def getMonitorInfo() -> list:
    info = []
    [info.append(m) for m in get_monitors()]
    return info

def randomColor() -> list:
    r = random.randint(1,255)
    g = random.randint(1,255)
    b = random.randint(1,255)
    return [r,g,b]

def fillSurface(surf:pg.Surface, color:tuple|list=randomColor()) -> bool:
    if (surf.fill(color)):
        return True;
    return False;

def blit(destSurf:pg.Surface, toBlit:pg.Surface, position:Vector2) -> None:
    if not position: destSurf.blit(toBlit, toBlit.get_rect())
    else: destSurf.blit(toBlit, (position[0], position[1]))

def loadSurface(path: str) -> pg.Surface:
    canonicalizedPath = path.replace('/', os.sep).replace('\\', os.sep)
    image = pg.image.load(canonicalizedPath).convert_alpha()
    return image

def loadSurfaceDir(path: str) -> list:
    surfaceList = []
    for _, __, imageFiles in os.walk(path):
        sortedFiles = sorted(imageFiles, key=naturalKey)
        for image in sortedFiles:
            fullPath = path + '/' + image
            imageSurface = loadSurface(fullPath)
            surfaceList.append(imageSurface)

    return surfaceList

def loadSurfaceDirNum(path: str) -> list:
    surfaceList = []
    fileList = []
    for _, __, imageFiles in os.walk(path):
        for index, image in enumerate(imageFiles):
            fileList.append(image)
        # sort images based on numerical values in the image names: run1.png will always come before run12.png as walk doesnt sort files returned.
        fileList.sort(key=lambda image: int(
            ''.join(filter(str.isdigit, image))))
        for index, image in enumerate(fileList):
            fullPath = path + '/' + image
            imageSurface = loadSurface(fullPath).convert_alpha()
            imageSurface.set_colorkey([0, 0, 0])
            surfaceList.append(imageSurface)
    return surfaceList

def scaleSurface(surf:pg.Surface, size:list|tuple) -> pg.Surface:
    return pg.transform.scale(surface=surf,size=size)

def scaleSurfaces(surfs: list, size: tuple) -> list:
    scaled_images = []
    for surf in surfs:
        scaled_images.append(scaleSurface(surf, size))
    return scaled_images

def surfaceCutout(surf: pg.Surface, cutSize: int) -> list:
    surface = surf
    surfNumX = int(surface.get_size()[0] / cutSize)
    surfNumY = int(surface.get_size()[1] / cutSize)

    cutSurfs = []
    for row in range(surfNumY):
        for col in range(surfNumX):
            x = col * cutSize
            y = row * cutSize
            newSurf = pg.Surface(
                (cutSize, cutSize), flags=pg.SRCALPHA)
            newSurf.blit(surface, (0, 0), pg.Rect(
                x, y, cutSize, cutSize))
            cutSurfs.append(newSurf)

    return cutSurfs

def loadSurfaceCutout(path: str, cutSize: int) -> list:
    surface = loadSurface(path)
    surfNumX = int(surface.get_size()[0] / cutSize)
    surfNumY = int(surface.get_size()[1] / cutSize)
    cutSurfs = []
    for row in range(surfNumY):
        for col in range(surfNumX):
            x = col * cutSize
            y = row * cutSize
            newSurf = pg.Surface((cutSize, cutSize), flags=pg.SRCALPHA).convert_alpha()
            newSurf.blit(surface, (0, 0), pg.Rect(x, y, cutSize, cutSize))
            cutSurfs.append(newSurf)
    return cutSurfs

def setIcon(iconPath:str) -> None:
    try:
        icon = loadSurface(iconPath)
        pg.display.set_icon(icon)
    except (TypeError):
        print("ERROR SETTING ICON!!!\n")

TEXT_LIB= {}
def renderText(surf:pg.Surface, ttfPath:str=None, text:str="text", position:pg.math.Vector2=pg.math.Vector2, size:int=30, color:list|tuple=(255,255,255), bgColor=None, center=True) -> None:
    textSurf = TEXT_LIB.get(f"{text}{color}{size}")
    if textSurf is None:
        if ttfPath != None:
            font = pg.font.Font(ttfPath, size)
        else:
            font = pg.font.Font(None, size)
        textSurf = font.render(text, True, color, bgColor)
        TEXT_LIB[f"{text}{color}{size}"] = textSurf
    x, y = position
    if center:
        surf.blit(textSurf, (x - (textSurf.get_width() // 2), y - (textSurf.get_height() // 2)))
    else:
        surf.blit(textSurf, (x, y))

def sendFrame() -> None:
    pg.display.flip()

def drawRect(destSurf:pg.Surface, rect:pg.Rect, color:list, width:int=1) -> pg.Rect:
    pg.draw.rect(surface=destSurf, color=color, rect=rect, width=width)

def createRect(position:list|Vector2=[0,0], size:list|Vector2=[16,16]) -> pg.Rect:
    return pg.Rect(position,size)
