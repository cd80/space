import ctypes
import ctypes.wintypes
import time
import time
# https://stackoverflow.com/questions/38461335/python-2-x-queryperformancecounter-on-windows
kernel32             = ctypes.WinDLL('kernel32', use_last_error=True)

starting_time        = ctypes.wintypes.LARGE_INTEGER()
ending_time          = ctypes.wintypes.LARGE_INTEGER()
elapsed_microseconds = ctypes.wintypes.LARGE_INTEGER()
frequency            = ctypes.wintypes.LARGE_INTEGER()

kernel32.QueryPerformanceCounter(ctypes.byref(starting_time))
class TimingData():
    def __init__(self):
        self.frameNumber = 0
        self.lastFrameTimeStamp = 0
        self.lastFrameDuration = 0
        self.lastFrameClockstamp = 0
        self.lastFrameClockTicks = 0
        self.isPaused = False
        self.averageFrameDuration = 0
        self.fps = 0
        self.timingData = 0
    def init(self):
        self.initTime()
        self.timingData = TimingData()
        
        self.timingData.frameNumber = 0

        self.timingData.lastFrameTimestamp = self.systemTime()
        self.timingData.lastFrameDuration = 0

        self.timingData.lastFrameClockstamp = self.getClock()
        self.timingData.lastFrameClockTicks = 0

        self.timingData.isPaused = False

        self.timingData.averageFrameDuration = 0
        self.timingData.fps = 0
    def initTime(self):
        time = ctypes.wintypes.LARGE_INTEGER()
        self.qpcFlag =  kernel32.QueryPerformanceFrequency(ctypes.byref(time)) > 0
        if self.qpcFlag:
            self.qpcFrequency = 1000.0 / time.value

    def systemTime(self):
        if self.qpcFlag:
            qpcMillisPerTick = ctypes.wintypes.LARGE_INTEGER()
            kernel32.QueryPerformanceCounter(ctypes.byref(qpcMillisPerTick))
            return qpcMillisPerTick.value * self.qpcFrequency
        else:
            return kernel32.timeGetTime()


    def getClock(self):
        return time.clock()


    def get(self):
        return self.timingData

    def update(self):
        if not self.timingData:
            return

        if not self.timingData.isPaused:
            self.timingData.frameNumber += 1

        thisTime = self.systemTime()
        self.timingData.lastFrameDuration = thisTime - self.timingData.lastFrameTimeStamp
        self.timingData.lastFrameTimeStamp = thisTime

        thisClock = self.getClock()
        self.timingData.lastFrameClockTics = thisClock - self.timingData.lastFrameClockstamp
        self.timingData.lastFrameClockstamp = thisClock

        if self.timingData.frameNumber > 1:
            if self.timingData.averageFrameDuration <= 0:
                self.timingData.averageFrameDuration = self.timingData.lastFrameDuration

            else:
                self.timingData.averageFrameDuration *= 0.99
                self.timingData.averageFrameDuration += 0.01 * self.timingData.lastFrameDuration

                self.timingData.fps = 1000.0 / self.timingData.averageFrameDuration


