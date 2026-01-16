import screen_brightness_control as sbc
import subprocess
import numpy as np

class SystemControl:
    def __init__(self):
        # Volume Initialization
        # macOS volume is 0-100
        self.minVol = 0
        self.maxVol = 100

    def set_volume(self, length):
        # Hand Range 50 - 300
        # Volume Range 0 - 100
        vol = np.interp(length, [50, 300], [self.minVol, self.maxVol])
        
        # Set volume using osascript
        cmd = f"osascript -e 'set volume output volume {int(vol)}'"
        subprocess.run(cmd, shell=True)
        
        return vol

    def get_volume_level(self):
        # Get volume using osascript
        cmd = "osascript -e 'output volume of (get volume settings)'"
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            current_vol = int(result.stdout.strip())
        except:
            current_vol = 50 # Default fallback
            
        volBar = np.interp(current_vol, [self.minVol, self.maxVol], [400, 150])
        volPer = np.interp(current_vol, [self.minVol, self.maxVol], [0, 100])
        return volBar, volPer

    def set_brightness(self, length):
        # Hand Range 50 - 300
        # Brightness Range 0 - 100
        brightness = np.interp(length, [50, 300], [0, 100])
        try:
            sbc.set_brightness(int(brightness))
        except:
            pass # Handle potential errors silently or log
        return brightness
