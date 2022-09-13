import cv2
__all__ = [cv2]

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture('landscape-video.mp4')
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
fps = cap.get(cv2.CAP_PROP_FPS)
width_crop = round(height/1.7778)
height_crop = height
video_writer = cv2.VideoWriter('follow.avi', cv2.VideoWriter_fourcc('P','I','M','1'), fps, (width, height))
videoCrop_writer = cv2.VideoWriter('follow_crop.avi', cv2.VideoWriter_fourcc('P','I','M','1'), fps, (width_crop, height_crop))
last_faces = [(width/2-200/2, height/2-200/2, 200, 200)]
for frame_idx in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))):
    ret, frame = cap.read()
    img = frame.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(200, 200))
    if len(faces) == 0:
        faces = last_faces
    (face_x, face_y, face_w, face_h) = faces[0]
    (lface_x, lface_y, lface_w, lface_h) = last_faces[0]
    if frame_idx != 0:
        (kface_x, kface_y, kface_w, kface_h) = keep_faces[0]
        marge = 26
        marge_incrementation = .5
        if face_x > kface_x + marge:
            keep_faces = [(int(kface_x + marge_incrementation), kface_y, int(kface_w + marge_incrementation), kface_h)]
            print('JUMPCUT RIGHT #'+str(frame_idx))
            print('face_x='+str(face_x)+' kface_x='+str(kface_x)+' in_kface_x='+str(int(kface_x + marge_incrementation)))
        elif face_x < kface_x - marge:
            keep_faces = [(int(kface_x - marge_incrementation), kface_y, int(kface_w - marge_incrementation), kface_h)]
            print('JUMPCUT LEFT #'+str(frame_idx))
            print('face_x=' + str(face_x) + ' kface_x=' + str(kface_x)+' in_kface_x='+str(int(kface_x - marge_incrementation)))
        else:
            keep_faces = faces
    else:
        keep_faces = faces
# skip_frames = 2
    # if frame_idx % skip_frames == 0 or frame_idx == 0:
        # print(frame_idx)
        # keep_faces = faces
    last_faces = faces
    for (x, y, w, h) in keep_faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    (kface_x, kface_y, kface_w, kface_h) = keep_faces[0]
    img_x_out = round(height/1.7778)
    if kface_w < height:
        img_x_in = round(kface_x-(height/1.7778-kface_w)/2)
    else:
        img_x_in = kface_x
    img_y_in = 0
    img_y_out = height
    cv2.rectangle(img, (img_x_in, img_y_in), (img_x_in + img_x_out, img_y_in + img_y_out), (0, 0, 0), 2)
    # print([img_x_in, img_x_out, img_y_in, img_y_out])
    img_cropped = frame[img_y_in:img_y_in + img_y_out, img_x_in:img_x_in + img_x_out]
    video_writer.write(img)
    videoCrop_writer.write(img_cropped)
    cv2.imshow('Video Follow', img)
    cv2.imshow('Video Cropped', img_cropped)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
video_writer.release()
cv2.destroyAllWindows()