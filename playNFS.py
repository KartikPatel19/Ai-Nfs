import numpy as np
from PIL import ImageGrab
import cv2
import pyautogui
import time
from directKeys import ReleaseKey, PressKey, W, A, S, D

def drawLines(img, lines):
	try:
		for line in lines:
			coords = line[0]
			cv2.line(img, (coords[0],coords[1]), (coords[2],coords[3]), [255,255,255], 3)
	except:
		pass

def roi(img, vertices):
	mask = np.zeros_like(img)
	cv2.fillPoly(mask,vertices,255)
	masked = cv2.bitwise_and(img, mask)
	return masked


def processImg(originalImage):
	processedImg = cv2.cvtColor(originalImage,cv2.COLOR_BGR2GRAY)
	processedImg = cv2.Canny(processedImg,threshold1=300,threshold2=400)
	processedImg = cv2.GaussianBlur(processedImg, (5,5),0)
	verticies = np.array([[10,500],[10,300],[300,200],[500,200],[800,300],[800,400]])
	processedImg = roi(processedImg,[verticies])

	lines = cv2.HoughLinesP(processedImg, 1, np.pi/180, 180, 20, 15)
	drawLines(processedImg,lines)

	return processedImg


def main():

	lastTime = time.time()
	while(True):
	    screen = np.array(ImageGrab.grab(bbox=(0,40,800,640)))
	    newScreen = processImg(screen)

	    print('Loop took {} seconds'.format(time.time()-lastTime))
	    lastTime = time.time()
	    cv2.imshow('window',newScreen)

	   # cv2.imshow('window',cv2.cvtColor(screen,cv2.COLOR_BGR2RGB))
	    if cv2.waitKey(25) & 0xFF == ord('q'):
	        cv2.destroyAllWindows()
	        break

main()