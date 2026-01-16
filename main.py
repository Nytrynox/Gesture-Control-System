import cv2
import time
import numpy as np
from hand_tracking import HandDetector
from system_control import SystemControl
from gui import App
import threading

def main():
    # Initialize Modules
    detector = HandDetector(detectionCon=0.7, maxHands=1)
    sys_control = SystemControl()
    
    # Initialize GUI
    app = App()
    
    # Camera Setup
    cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
    cap.set(3, 640)
    cap.set(4, 480)

    def video_loop():
        while True:
            success, img = cap.read()
            if not success:
                break

            # Hand Tracking
            img = detector.findHands(img)
            lmList, bbox = detector.findPosition(img, draw=True)

            vol_per = 0
            bright_per = 0

            if len(lmList) != 0:
                # Gesture Recognition
                
                # Filter based on size (distance to camera)
                area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) // 100
                
                if 250 < area < 1000:
                    # Find Distance between Index and Thumb
                    length, img, lineInfo = detector.findDistance(4, 8, img)
                    
                    # Convert Volume
                    # Volume Control (Index and Thumb)
                    # Smoothness could be added here
                    
                    # Check which fingers are up
                    fingers = detector.fingersUp()
                    
                    # If Pinky is down, set volume
                    if not fingers[4]:
                        vol = sys_control.set_volume(length)
                        
                        if length < 50:
                            cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                    
                    # If Pinky is up, set brightness (using same pinch for demo simplicity, or use different fingers)
                    # Let's use Index and Middle finger distance for brightness for better separation
                    # Or just use a mode switch based on hand.
                    # For simplicity: 
                    # Index+Thumb Pinch = Volume
                    # Index+Middle Pinch = Brightness (Let's implement this)
                    
                    length2, img, lineInfo2 = detector.findDistance(8, 12, img)
                    if length2 < 50: # Mode switch or just brightness?
                         # Let's stick to the user request: "fingers i have to control laptop a-z volume brightness"
                         # Let's use:
                         # Index+Thumb = Volume
                         # Thumb+Pinky = Brightness (A bit hard)
                         # Let's use: Left hand vs Right hand? No, usually one hand.
                         # Let's use: Index+Thumb = Volume. 
                         # Middle+Thumb = Brightness.
                         pass

                    length_bright, img, lineInfo_bright = detector.findDistance(4, 12, img)
                    if not fingers[3]: # Ring finger down
                         bright = sys_control.set_brightness(length_bright)


            # Get Status
            vol_bar, vol_per = sys_control.get_volume_level()
            # Brightness reading might be slow, so maybe just use the set value or read occasionally
            # For now, let's just update GUI with what we have
            
            # Update GUI
            # We need to be careful updating GUI from another thread
            # CustomTkinter is not thread safe for direct updates usually, but let's try scheduling
            # or just updating variables that the GUI polls.
            # Actually, better to run this loop IN the GUI update cycle.
            
            pass
    
    # Refactoring to use GUI's main loop for video processing to avoid threading issues
    def update():
        success, img = cap.read()
        if success:
            img = detector.findHands(img)
            lmList, bbox = detector.findPosition(img, draw=True)
            
            vol_per = 0
            bright_per = 0

            if len(lmList) != 0:
                # Filter based on size
                area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) // 100
                
                if 250 < area < 1000:
                    # Volume: Thumb + Index
                    length, img, _ = detector.findDistance(4, 8, img)
                    
                    # Brightness: Thumb + Middle
                    length_bright, img, _ = detector.findDistance(4, 12, img)

                    # Fingers Up
                    fingers = detector.fingersUp()
                    
                    # Logic:
                    # If Index and Thumb are close, control volume.
                    # If Middle and Thumb are close, control brightness.
                    # To avoid conflict, check which one is active or use a "Mode" gesture.
                    # Simple approach: 
                    # If Pinky is DOWN -> Volume Mode
                    # If Pinky is UP -> Brightness Mode
                    
                    if not fingers[4]: # Pinky Down -> Volume
                        sys_control.set_volume(length)
                        cv2.putText(img, "Volume Mode", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)
                    else: # Pinky Up -> Brightness
                        sys_control.set_brightness(length)
                        cv2.putText(img, "Brightness Mode", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

            # Update GUI Image
            app.update_video(img)
            
            # Update Status Labels
            # Get current volume/brightness to display
            # This might be resource intensive to query every frame, so maybe optimize later
            try:
                vol_bar, vol_per = sys_control.get_volume_level()
                # Brightness read is not implemented in sys_control efficiently, let's just use the last set value or skip for now
                # Assuming sys_control.set_brightness returns the value
                bright_per = 0 # Placeholder
            except:
                vol_per = 0
            
            app.update_status(vol_per, bright_per)

        app.after(10, update)

    update()
    app.mainloop()

if __name__ == "__main__":
    main()
