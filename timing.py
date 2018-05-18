import ctypes
import ctypes.wintypes
import time

# https://stackoverflow.com/questions/38461335/python-2-x-queryperformancecounter-on-windows
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)


class TimingData:
    def __init__(self):
        self.frameNumber = 0
        self.lastFrameTimeStamp = 0
        self.lastFrameDuration = 0
        self.lastFrameClockstamp = 0
        self.lastFrameClockTicks = 0
        self.isPaused = False
        self.averageFrameDuration = 0
        self.fps = 0
        self.timingData = None
        self.qpcFlag = 0
        self.qpcFrequency = 0

    def init(self):
        self.init_time()
        self.timingData = TimingData()
        
        self.timingData.frameNumber = 0

        self.timingData.lastFrameTimestamp = self.system_time()
        self.timingData.lastFrameDuration = 0

        self.timingData.lastFrameClockstamp = self.get_clock()
        self.timingData.lastFrameClockTicks = 0

        self.timingData.isPaused = False

        self.timingData.averageFrameDuration = 0
        self.timingData.fps = 0

    def init_time(self):
        cur_time = ctypes.wintypes.LARGE_INTEGER()
        self.qpcFlag = kernel32.QueryPerformanceFrequency(ctypes.byref(cur_time)) > 0
        if self.qpcFlag:
            self.qpcFrequency = 1000.0 / cur_time.value

    def system_time(self):
        if self.qpcFlag:
            qpc_mills_per_tick = ctypes.wintypes.LARGE_INTEGER()
            kernel32.QueryPerformanceCounter(ctypes.byref(qpc_mills_per_tick))
            return qpc_mills_per_tick.value * self.qpcFrequency
        else:
            return kernel32.timeGetTime()

    def get_clock(self):
        return time.clock()

    def get(self):
        return self.timingData

    def update(self):
        if not self.timingData:
            return

        if not self.timingData.isPaused:
            self.timingData.frameNumber += 1

        this_time = self.system_time()
        self.timingData.lastFrameDuration = this_time - self.timingData.lastFrameTimeStamp
        self.timingData.lastFrameTimeStamp = this_time

        this_clock = self.get_clock()
        self.timingData.lastFrameClockTics = this_clock - self.timingData.lastFrameClockstamp
        self.timingData.lastFrameClockstamp = this_clock

        if self.timingData.frameNumber > 1:
            if self.timingData.averageFrameDuration <= 0:
                self.timingData.averageFrameDuration = self.timingData.lastFrameDuration

            else:
                self.timingData.averageFrameDuration *= 0.99
                self.timingData.averageFrameDuration += 0.01 * self.timingData.lastFrameDuration

                self.timingData.fps = 1000.0 / self.timingData.averageFrameDuration


