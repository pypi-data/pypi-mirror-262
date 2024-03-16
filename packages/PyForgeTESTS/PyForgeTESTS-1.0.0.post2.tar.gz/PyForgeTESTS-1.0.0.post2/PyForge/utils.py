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

from PyForge.core import *
from PyForge.const import *


def createClock() -> pg.time.Clock:
    return pg.time.Clock()

def tickGetDeltaTime(clock:pg.time.Clock, FPS:int|float=144):
    return clock.tick(FPS)/1000.0

def naturalKey(string_) -> int|str:
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]

def getMousePosition() -> Vector2:
    return Vector2(*pg.mouse.get_pos())

def sineWaveValue() -> int:
    value = math.sin(pg.time.get_ticks())
    if value >= 0:
        return 255
    else:
        return 0

def clamp(num: int, minValue: int, maxValue: int) -> int:
    return max(min(num, maxValue), minValue)

def distTo(originVector, targetVector) -> Vector2:
    deltaX = targetVector.x - originVector.x
    deltaY = targetVector.y - originVector.y
    return Vector2((deltaX), (deltaY))

def getKeyState() -> tuple|pg.key.ScancodeWrapper:
    return pg.key.get_pressed()

def getMousePosition() -> Vector2:
    return Vector2(pg.mouse.get_pos())

def getMousePositionWZ(zoom) -> Vector2:
    return  Vector2(pg.mouse.get_pos()[0]/zoom,pg.mouse.get_pos()[1]/zoom)

class FPSMonitor:
    def __init__(self) -> None:
        """
        Initializes the FPSMonitor object.

        Attributes:
            peak_fps (float): The highest FPS value reached.
            total_frames (int): The total number of frames that have been rendered.
            total_fps (float): The sum of all FPS values, used to calculate the average FPS.
        """
        self.peakFps = 0.0
        self.totalFrames = 0
        self.totalFps = 0.0

    def update(self, currentFps:float) -> None:
        """
        Updates the FPS values with the current FPS.

        Args:
            current_fps (float): The current FPS value from pg.time.Clock().get_fps().
        """
        # Update the peak FPS if the current FPS is higher than the previously recorded peak
        self.peakFps = max(self.peakFps, currentFps)

        # Increment the total frames and add the current FPS to the total_fps
        self.totalFrames += 1
        self.totalFps += currentFps

    def getCurrentFps(self, clock) -> float:
        """
        Retrieves the current FPS from the provided frame clock.

        Args:
            clock (pg.time.Clock): The frame clock object.

        Returns:
            float: The current FPS value.
        """
        return clock.get_fps()

    def getPeakFps(self) -> float:
        """
        Returns the peak FPS value.

        Returns:
            float: The highest FPS value reached.
        """
        return self.peakFps

    def getAverageFps(self) -> float:
        """
        Calculates and returns the average FPS value.

        Returns:
            float: The average FPS value.
        """
        return self.totalFps / self.totalFrames if self.totalFrames > 0 else 0.0

    def getFpsData(self, clock) -> str:
        """
        Returns the current, peak, and average FPS values.

        Args:
            clock (pg.time.Clock): The frame clock object.

        Returns:
            str: A string containing the current FPS, peak FPS, and average FPS.
        """
        currentFps = self.getCurrentFps(clock)
        self.update(currentFps)
        peakFps = self.getPeakFps()
        averageFps = self.getAverageFps()
        return f"FPS | current | {int(currentFps)} | peak | {int(peakFps)} | avg. | {int(averageFps)}"

class DebugInterface:
    def __init__(self, displaySurface:pg.Surface, position:Vector2, gameClock:pg.time.Clock, interfaceSize:Vector2=(180,80), fontSize:int=24, bgColor:list=None, textColor:list=None) -> None:
        self.scope = []
        self.bgColor = bgColor
        self.fontSize = fontSize
        self.textColor = textColor
        self.displaySurface = displaySurface
        self.font = pg.font.Font(size=fontSize)
        self.interfaceRect = pg.Rect((position.x, position.y), interfaceSize)
        self._monitor = FPSMonitor()
        self._clock = gameClock

    def addToInterface(self, Info) -> None:
        if Info not in self.scope:
            self.scope.append(str(Info))

    def setFontSize(self, fontSize:int=24):
        self.fontSize = fontSize
        self.font = pg.font.Font(size=fontSize)

    def visualOutput(self) -> None:
        self.addToInterface(self._monitor.getFpsData(self._clock))
        for i,j in enumerate(self.scope):
            if (self.bgColor): debugInfo = self.font.render(str(j), antialias=True, color=self.textColor, bgcolor=self.bgColor)
            else: debugInfo = self.font.render(str(j), antialias=True, color=self.textColor, bgcolor=self.bgColor)
            self.displaySurface.blit(debugInfo,(self.interfaceRect.x,self.interfaceRect.y+(i*(debugInfo.get_height() + 4))))
        self.scope.clear()
