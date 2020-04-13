from Game.YOLO.video_control import player_tracker 
import time

    
def test_tracking():
    # testing yolo module
    yolo_obj = player_tracker()
    yolo_obj.start()


test_tracking()
