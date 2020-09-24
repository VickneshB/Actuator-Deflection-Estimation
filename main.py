import numpy as np
import cv2
import sys
import argparse
import os

import matplotlib
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser() 
parser.add_argument("input", help="Input Video Path", type=str)
parser.add_argument("-o","--output", help="Prefered Output Video name \n(default: {Input}_Output.avi)", type=str)
args = parser.parse_args()


if args.output == None:
    args.output = os.path.splitext(args.input)[0] + "_Output.avi"

def main():
    
    originalSpecimenLength = 80 # mm
    video = cv2.VideoCapture(args.input)
    
    is_okay, bgr_image_input = video.read()
    
    if not is_okay:
        print("Cannot read video source")
        sys.exit()
    
    h1 = bgr_image_input.shape[0]
    w1 = bgr_image_input.shape[1]

    frameNo = 0
    
    fileObj = open("Deflection.csv","w+")
    
    try:
        fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
        fname = args.output
        fps = 30.0
        videoWriter = cv2.VideoWriter(fname, fourcc, fps, (w1, h1))
    except:
        print("Error: can't create output video: %s" % fname)
        sys.exit()
    
    frames = []
    deflections = []
    
    while True:
        
        is_okay, bgr_image_input = video.read()
    
        if not is_okay:
            print("End of Video")
            break
        
        frameNo = frameNo + 1
        
        
        gray_image = cv2.cvtColor(bgr_image_input, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray_image, 127,255,0)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            hull = cv2.convexHull(contour,returnPoints = False)
            defects = cv2.convexityDefects(contour,hull)

            if area > 20000 and area < 50000:            
                if defects is not None:
                    maxDeflection = 0
                    for i in range(defects.shape[0]):
                        s,e,f,d = defects[i,0]
                        start = tuple(contour[s][0])
                        end = tuple(contour[e][0])
                        far = tuple(contour[f][0])
                        
                        
                        distance = np.abs(((end[1] - start[1]) * far[0]) - ((end[0] - start[0]) * far[1]) + (end[0] * start[1]) - (end[1] * start[0]))\
                        /np.sqrt((end[1] - start[1])**2 + (end[0] - start[0])**2)
                        
                        
                        if distance > maxDeflection:
                            maxDeflection = distance
                            finalStart = start
                            finalEnd = end
                            finalFar = far
                    
                    if frameNo == 1:
                        specimanLength = np.sqrt((finalEnd[0] - finalStart[0])**2 + (finalEnd[1] - finalStart[1])**2)
                    
                    originalDeflection = (maxDeflection * originalSpecimenLength) / specimanLength
                        
                    print(str(frameNo) + ", " + str(originalDeflection) + " mm")   
                    frames.append(frameNo)
                    if len(deflections) > 0 and np.abs(originalDeflection-deflections[-1]) > 1:
                        deflections.append(deflections[-1])
                    else:
                        deflections.append(originalDeflection)
                    
                    fileObj.writelines([str(frameNo) +  ", " + str(originalDeflection) + "\n"])
                    
                    cv2.line(bgr_image_input,finalStart,finalEnd,[0,255,0],2)
                    cv2.circle(bgr_image_input,finalFar,5,[255,0,0],-1)

                bgr_image_input = cv2.drawContours(bgr_image_input, [contour], -1, (0,0,255), 3)
        
        cv2.imshow("Curvature", bgr_image_input)
        videoWriter.write(bgr_image_input)

        key_pressed = cv2.waitKey(1) & 0xFF
        if key_pressed == 27 or key_pressed == ord('q'):
            break
    
    fileObj.close()
    
    fig, ax = plt.subplots()
    ax.plot(frames, deflections)

    ax.set(xlabel='Frame Number', ylabel='Deflection (mm)',
           title='Deflection of the Specimen')
    ax.grid()

    fig.savefig("Deflection.png")
    plt.show()
        
        
if __name__ == '__main__':
    main()
