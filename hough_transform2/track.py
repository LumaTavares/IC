import cv2 as cv
import numpy as np



# Carregar video
video=cv.VideoCapture('video3.mp4')

#making output video
frame_width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
fps = video.get(cv.CAP_PROP_FPS)

output_video_path = 'output_tracking_video.mp4'
output_video = cv.VideoWriter(output_video_path, cv.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

  
while True:
    ret,frame=video.read()
    if not ret:
        video= cv.VideoCapture(video)
        continue


    hsv=cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    #masks----
    lower_color = np.array([ 56, 54, 134])  # Ajuste conforme necessário
    upper_color = np.array([ 76, 74, 214])
    mask = cv.inRange(hsv, lower_color, upper_color)

    #-----
    edges= cv.Canny(mask, 55,200)
    #desenha as linhas
    lines=cv.HoughLinesP(edges,1,np.pi/180,5,maxLineGap=50)
    if lines is not None:   #linhas para videos -saber se ainda existe alguma linha
        for line in lines:
            x1,y1,x2,y2=line[0]
            cv.line(frame,(x1,y1),(x2,y2),(0,255,0),5)

    output_video.write(frame)#making the frames

    #cv.imshow('frame',frame)#mostra o frame
    
    key=cv.waitKey(25)
    if cv.waitKey(25) & 0xFF == ord('q'):
        break
video.release()
cv.destroyAllWindows()
output_video.release()
        
    
