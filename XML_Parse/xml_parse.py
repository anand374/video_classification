#!/usr/bin/python
import xml.etree.ElementTree as ET
import cv2
from imutils import paths
import numpy as np
import argparse
import glob


'''
NOTE-------------------
We used the PASCAL Challenge VOC2010 dataset.
The annonations for the images were stored as XML files.
THe annonations included data for where the person is located in an image, and where his body parts are located.
The data format was different for 2007-08 and 2009-10, modifications were done accordingly.
'''
person_path='dpm_database/persons/'
head_path='dpm_database/head/'
hand_path='dpm_database/hand/'
foot_path='dpm_database/foot/'

'''
xmlPath1="trash/"

imgPath="~/mount/VOC2010PersonParts/VOCdevkit/person_Parts_Only/Final/JPEGImages/"
'''

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True, help="path to images directory")
ap.add_argument("-x", "--xml", required=True, help="path to xml directory")
args = vars(ap.parse_args())
xmlPaths=glob.glob(args["xml"]+"/*")
#xmlPaths=glob.glob(xmlPath1+"/*")

i=0
j=0
for xmlPath in xmlPaths:
   tree = ET.parse(xmlPath)
   root = tree.getroot()

   for obj in root.iter('object'):
      if(obj[0].text=='person'):
         #i+=1
         imgPath=args["images"]+"/"+xmlPath[len(xmlPath)-15:len(xmlPath)-4]+'.jpg'
         img=cv2.imread(imgPath)
         if img is None:
            j+=1
            print "Failed %d times." % (j)
            continue
         bckup=np.copy(img)
         '''
         size=obj.find('bndbox')
         pers_min=(int(size[1].text),int(size[3].text))
         pers_max=(int(size[0].text),int(size[2].text))
         roi=bckup[pers_min[1]:pers_max[1],pers_min[0]:pers_max[0]]
         cv2.rectangle(img,pers_min,pers_max,(0,255,0),3)
         imgWritePath=person_path+str(i)+"09-10.jpg"

         cv2.imwrite(imgWritePath,roi)
         '''
         #print "Person bound box (xy_min,xy_max): ((%d,%d),(%d,%d))" % (pers_min[0],pers_min[1],pers_max[0],pers_max[1])
         

         #Convention- Blue for head, Green for hands, Red for foot
         for part in obj.iter('part'):
            part_min = (int(part[1][0].text),int(part[1][1].text))
            part_max = (int(part[1][2].text),int(part[1][3].text))
            part_name = part[0].text
            #print "%s bound box: ((%d,%d),(%d,%d))" % (part_name,part_min[0],part_min[1],part_max[0],part_max[1])
            roi=bckup[part_min[1]:part_max[1],part_min[0]:part_max[0]]
            i+=1
            if(part_name=='head'):
               cv2.rectangle(img,part_min,part_max,(255,0,0),3)
               imgWritePath=head_path+str(i)+"09-10.jpg"
               cv2.imwrite(imgWritePath,roi)

            elif(part_name=='hand'):
               cv2.rectangle(img,part_min,part_max,(0,255,0),3)
               imgWritePath=hand_path+str(i)+"09-10.jpg"
               cv2.imwrite(imgWritePath,roi)
            
            elif(part_name=='foot'):
               cv2.rectangle(img,part_min,part_max,(0,0,255),3)
               imgWritePath=foot_path+str(i)+"09-10.jpg"
               cv2.imwrite(imgWritePath,roi)
            print imgWritePath
         #while(1):
         cv2.imshow("Person", img)
         k=cv2.waitKey(1)
         if k & 0xFF==ord('q'):
            break
         elif k==27:
            cv2.destroyAllWindows()
            exit()


cv2.destroyAllWindows()