import cv2
import numpy as np
import glob
MIN_MATCH_COUNT=100

detector = cv2.xfeatures2d.SIFT_create()
note_name = ["100","100","200","200","10","10","500","500","20","20"]
FLANN_INDEX_KDITREE=0
flannParam=dict(algorithm=FLANN_INDEX_KDITREE,tree=5)
flann=cv2.FlannBasedMatcher(flannParam,{})
i = 0
#print(i)
#trainImg = [cv2.imread(file) for file in glob.glob('hund1.jpeg')]

while True:
    desti = "images/"+str(i)+".jpeg"
    #print("This is" +" "+note_name[i])
    print(desti)
    trainImg=cv2.imread(desti,0)

    trainKP,trainDesc=detector.detectAndCompute(trainImg,None)

    cam=cv2.VideoCapture(0)
    flag = 0
    ret, QueryImgBGR=cam.read()
    QueryImg=cv2.cvtColor(QueryImgBGR,cv2.COLOR_BGR2GRAY)
    queryKP,queryDesc=detector.detectAndCompute(QueryImg,None)
    matches=flann.knnMatch(queryDesc,trainDesc,k=2)

    goodMatch=[]
    for m,n in matches:
        if(m.distance<0.75*n.distance):
            goodMatch.append(m)
    if(len(goodMatch)>MIN_MATCH_COUNT):
        tp=[]
        qp=[]
        for m in goodMatch:
            tp.append(trainKP[m.trainIdx].pt)
            qp.append(queryKP[m.queryIdx].pt)
        tp,qp=np.float32((tp,qp))
        H,status=cv2.findHomography(tp,qp,cv2.RANSAC,3.0)
        h,w=trainImg.shape
        trainBorder=np.float32([[[0,0],[0,h-1],[w-1,h-1],[w-1,0]]])
        queryBorder=cv2.perspectiveTransform(trainBorder,H)
        cv2.polylines(QueryImgBGR,[np.int32(queryBorder)],True,(0,255,0),5)
    else:
        print ("Not Enough match found- %d/%d"%(len(goodMatch),MIN_MATCH_COUNT))
        if(len(goodMatch)>50):
            print("This is" +" "+note_name[i])
            i = i + 1
        else:
            print("Not Found")
            i = i + 1
            if(i is 10):
                i = 0
                
    
    cv2.imshow('result',QueryImgBGR)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break