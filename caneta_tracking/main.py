from ultralytics import YOLO
import cv2 
#load model

model= YOLO('C:/Users/usuário/Desktop/caneta_tracking/train2/weights/best.pt')

#load video
video_path='./test.mp4'
cap=cv2.VideoCapture(video_path)

ret=True

# Get video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

#----
output_video_path = 'output_tracking_video.mp4'
output_video = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

#read frames
while ret:
    ret,frame=cap.read()
    if ret:

        #detect objects
        #track objects
        results= model.track(frame,persist=True)
        #plot results
        frame_= results[0].plot()

        output_video.write(frame_)
        #visualize
        #cv2.imshow('frame',frame_)
        #if cv2.waitKey(25) & 0xFF == ord('q'):
            #break

cap.release()
cv2.destroyAllWindows()
output_video.release()
