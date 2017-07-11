import ctypes

'''Finds the width and height of the screen,
as well as the ratio of the width and height to 1920 and 1080 respectively'''
def screen_metrics():
    ctypes.windll.user32.SetProcessDPIAware()
    user32 = ctypes.windll.user32
    width = int(user32.GetSystemMetrics(0))
    height = int(user32.GetSystemMetrics(1))
    wto1920 = width/1920
    hto1080 = height/1080
    metrics = [width, height, wto1920, hto1080]
    return metrics


# Create new load function that bipasses pygame.error
