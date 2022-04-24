import PySimpleGUI as sg
import cv2


layout = [[sg.Image(key='IMAGE')],
          [sg.Text('Recognized person(s): 0', key='RESULT',
                   expand_x=True, justification='c')]]
window = sg.Window('Face Recogniser', layout)
video = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")

while True:
    event, values = window.read(timeout=0)
    if event == sg.WIN_CLOSED:
        break
    # read src, get res
    _, frame = video.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(frame_gray,
                                          scaleFactor=1.2,
                                          minNeighbors=6,
                                          minSize=(50, 50))
    # rect
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # upd res
    img_bytes = cv2.imencode('.png', frame)[1].tobytes()
    window['IMAGE'].update(data=img_bytes)
    window['RESULT'].update(f'Recognized person(s): {len(faces)}')

window.close()

# face_cascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")
#
# img = cv2.imread('Resources/lena.png')
# imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
# faces = face_cascade.detectMultiScale(imgGray, 1.1, 4)
#
# for (x, y, w, h) in faces:
#     cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
#
#
# cv2.imshow("Result", img)
# cv2.waitKey(0)
