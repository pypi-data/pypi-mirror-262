from __future__ import annotations
import os
import imutils, imutils.paths
import json
import xml.etree.ElementTree as ET
import uuid
import cv2
import numpy as np
import shutil
from tqdm import tqdm
import random
from tabulate import tabulate

from shapely.geometry import Point, Polygon, LineString
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import (
    HuberRegressor,
    LinearRegression,
    RANSACRegressor,
    TheilSenRegressor,
)

class autils:
    def __init__(self):
        
        pass

    def printTable(self, table_heads, info_dict):
        #table_header = ["class", "iou"]
        exp_table = [
            (str(k), str(v))
            for k, v in info_dict.items()
        ]
        
        print(tabulate(exp_table,headers=table_heads,tablefmt="fancy_grid"))

    def getImgPaths(self, imgs_dir):
        if not os.path.exists(imgs_dir):
            raise ValueError("{} doesn't exist!".format(imgs_dir))
        img_paths = list(imutils.paths.list_files(imgs_dir))
        return img_paths

    def imgsDict(self, imgs_dir):
        img_paths = self.getImgPaths(imgs_dir)
        imgs_dict = {}
        for img_path in img_paths:
            base_name = os.path.basename(img_path)[:-4]
            imgs_dict[base_name] = img_path
        return imgs_dict
    
    def getJsonPaths(self, jsons_dir):
        if not os.path.exists(jsons_dir):
            raise ValueError("{} doesn't exist!".format(jsons_dir))
        json_paths = list(imutils.paths.list_files(jsons_dir, validExts=".json"))
        return json_paths

    def fileBasename(self, file_path, format=".json"):
        if format in [".json"]:
            base_name = os.path.basename(file_path)[:-5]
        elif format in [".jpg", ".png", ".bmp", ".txt"]:
            base_name = os.path.basename(file_path)[:-4]
        else:
            raise ValueError("Format don't support!")

        return base_name

    def readJsonFile(self, json_path):
        if not os.path.exists(json_path):
            return None
        try:
            with open(json_path, 'r', encoding="utf-8") as f:
                js_data = json.load(f)
        except:
            return None
        return js_data

    def readXMLFile(self, xml_path):
        """
        #get node values
        for annot in root.iter('image'):
            img_id = annot.get("name")
            id = int(annot.get("id"))
        """
        assert os.path.exists(xml_path)
        tree = ET.parse(xml_path)
        root_node = tree.getroot()

        return root_node

    def checkDir(self, dir_path):
        if not os.path.exists(dir_path):
            return False
        else:
            return True
    
    def mkDir(self, dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def rmDir(self, dir_path):
        shutil.rmtree(dir_path)
    
    def genUUID(self,):
        return str(uuid.uuid4().hex)

    def shuffleList(src_list):
        random.shuffle(src_list)

    def saveJsonData(self, js_data, save_path):
        with open(save_path, "w", encoding='utf-8') as f:
            json.dump(js_data, f, indent=4, ensure_ascii=False)

    def selectImgs(self, src_imgs_dir, dst_imgs_dir, show_size=(480,270)):
        assert self.checkDir(src_imgs_dir), "Source image directory invalid!"
        img_paths = list(imutils.paths.list_images(src_imgs_dir))
        assert  len(img_paths) > 0, "Image number is zero!"
        self.mkDir(dst_imgs_dir)

        for img_path in tqdm(img_paths):
            img = cv2.imread(img_path)
            if img is None: continue
            h,w = img.shape[:2]
            if show_size is not None:
                assert isinstance(show_size, tuple), "show size invalid"
                assert show_size[0] > 50 and show_size[1] > 50
                img = cv2.resize(img, (show_size[0], show_size[1]))
            
            cv2.imshow("img", img)

            key = cv2.waitKey(100000)
            if key == 102: # "f"
                print("Forward...")
                continue
            elif key == 13: # "Enter"
                img_name = os.path.basename(img_path)
                save_path = os.path.join(dst_imgs_dir, img_name)
                shutil.copy2(img_path, save_path)
                print("Copyed:{} ".format(save_path))
                continue
            elif key == 32: #"space" (pause)
                print("pause!")
                cv2.waitKey(0)
            elif key == 113: #"q" (quit):
                print("exit!")
                break
            else:
                print("Invalid key!")
                continue

    #------annot formats
    def decodePolyline(self, polyline):
        pts = []
        label = polyline.get("label")
        points = polyline.get("points")
        points = points.split(";")
        for pt in points:
            x, y = pt.split(",")
            pts.append([float(x),float(y)])
            #pts.append({"x": x, "y":y})
        return label, pts

    def getCVATannots(self, xml_path):
        if not os.path.exists(xml_path):
            raise ValueError("{} does't exist!".format(xml_path))
       
        root_node = self.readXMLFile(xml_path)
        if root_node is None:
            raise ValueError("xml root node invalid!")

        all_annots = []
        for annot in root_node.iter('image'):
            img_id = annot.get("name")
            file_name = img_id.split(os.path.sep)[-1]
            width = int(float(annot.get("width")))
            height= int(float(annot.get("height")))

            lines_info = {}
            lines_info["file_name"] = file_name
            lines_info["imageHeight"] = height
            lines_info["imageWidth"] = width
            lines_info["annots"] = []
            for polyline in annot.iter('polyline'):
                label, pts = self.decodePolyline(polyline)
                lines_info["annots"].append(dict(label=label, pts=pts))

            all_annots.append(lines_info)

        return all_annots

    def createLabelmeProto(self,):
        "create common format labelme proto"
        labelme_annot = {}
        labelme_annot["shapes"] = []
        #labelme_annot["version"] = "5.0.2"
        labelme_annot["version"] = "3.16.7"
        labelme_annot["flags"] = {}
        labelme_annot["imagePath"] = ""
        labelme_annot["imageHeight"] = -1
        labelme_annot["imageWidth"] = -1
        labelme_annot["imageData"] = None
        labelme_annot["relations"] = None
        labelme_annot["lineColor"]=[0,255,0,128]
        labelme_annot["fillColor"]=[255,0,0,128]

        return labelme_annot

    def createLabelmeShapeProto(self,):
        "create common labelme single shape proto"
        line_annot = {}
        line_annot["label"] = ""
        line_annot["line_color"] = None,
        line_annot["fill_color"] = None,
        line_annot["points"] = []
        line_annot["uuid"] = ""
        line_annot["shape_type"] = "linestrip"
        line_annot["flags"] = {}
        line_annot["group_id"] =  None
        line_annot["in_freespace"] = None

        return line_annot

    #-----math
    def twoPtsDist(self,p1, p2):
        return  np.linalg.norm(np.array(p1)-np.array(p2))

    def lineLength(self,pts):
        length = 0.0
        for i in range(len(pts) - 1):
            length += self.twoPtsDist(pts[i], pts[i+1])

        return length

    def calImgBoarderPtOnLine(self,pt1, pt2, img_size):
        #计算由两点确定的直线的向图像底部的延伸线与图像边缘的交点
        """
        ax + by = c   // 线性方程
        由两点（x1,y1）,（x2,y2）确认参数
        a=(y2−y1)
        b=(x1−x2)
        c=ax1+by1
        ==> x = (c - by) / a 
        ==> y = (c - ax) / b
        """
        assert pt1[1] > pt2[1]  # pt1.y > pt2.y

        x1, y1 = pt1
        x2, y2 = pt2
        img_h, img_w = img_size
        a = y2 - y1
        b = x1 - x2
        c = a*x1 + b*y1

        if a == 0:
            return [(x1, img_h-2),(x1, 1)] # 竖直线：返回位于直线上的图像底部及顶部边缘点
        if b == 0:
            return [(1, y1), (img_w-2, y1)] # 水平线：返回位于直线上的图像左右边缘点

        x = (c - b * (img_h-1)) / a
        if x >=0 and x < img_w:
            return [(x, img_h-1)] # 返回位于直线上图像底部的边缘点
        y = (c - a * 0) / b
        if y > y1 and y < img_h:
            return [(0, y)] # 返回位于直线上图像左边缘点
        y = (c - a * (img_w-1))/b
        if y > y1 and y < img_h:
            return [(img_h-1, y)] # 返回位于直线上图像右边缘点

        return None

    def pt2LineDist(self,p1, p2, p):
        # distance of pt to the line (p1, p2)
        p1, p2, p = np.array(p1), np.array(p2), np.array(p)
        return np.abs(np.linalg.norm(np.cross(p2-p1, p1-p)))/np.linalg.norm(p2-p1)

    def isPtNearImgBoarder(self, pt,img_size,near_thres=5):
        ##判断点与图像的左，右，上，下四个边缘是否靠近

        h, w = img_size
        boarder_polygon = [[0,0],[0,h-1],[w-1,h-1], [w-1,0]]
        # right_line = [[w-1,0],[w-1,h-1]]
        # bot_line = [[0,h-1],[w-1,h-1]]
        dst_pt = Point(pt)
        boarder_region =  Polygon(boarder_polygon)

        return boarder_region.exterior.distance(dst_pt) <= near_thres

    def lineSlop(self, xs, ys):
        if xs[0] == xs[1]:
            return 0
        else:
            slope = np.polyfit(xs,ys,1)[0]
        return slope

    def lineAngle(self, xs, ys):
        angle = np.rad2deg(np.arctan2(ys[-1] - ys[0], xs[-1] - xs[0]))
        return angle

    def interp1d(self,ys,xs, fit_order):
        #y: samll -> large
        #以y为自变量拟合x
        assert ys[1] > ys[0], "ys[1] must larger than ys[0]"
        fit_param = np.polyfit(ys, xs,fit_order)
        fit_xy = np.poly1d(fit_param)
        pts = []
        for y in range(int(ys[0]),int(ys[-1]) , 1):
            pts.append((fit_xy(y), y))

        return pts

    def refineLine(self,line, poly_factor, fit_method="RANSAC"):
        """
        poly_facotr: 1,2,3...
        fit_method: "RANSAC", "HuberRegressor","Theil_Sen","OLS"
        """
        line = np.array(line).astype(float)
        xs,ys = line[:,0], line[:,1]
        ys_fit = ys[:,np.newaxis]
        estimators = [
            ("RANSAC", RANSACRegressor(random_state=42)),
            ("HuberRegressor", HuberRegressor()),
            ("Theil_Sen", TheilSenRegressor(random_state=42)),
            ("OLS", LinearRegression())
        ]
        # poly_factor = 1 if fit_type.get("line") else 2
        fit_types = dict(RANSAC=0, HuberRegressor=1,Theil_Sen=2,OLS=3)
        estimator_type = fit_types.get(fit_method)
        assert estimator_type is not None
            
        model = make_pipeline(PolynomialFeatures(poly_factor), estimators[estimator_type][1])
        model.fit(ys_fit, xs)
        xs_fit = model.predict(ys_fit)

        fit_line = np.concatenate((xs_fit[:,np.newaxis],ys_fit), axis=-1)
        return fit_line

    #---image    
    def imgs2video(self, imgs_dir, video_path, reset_imgsize=False, fps=30):
        assert self.checkDir(imgs_dir)
        img_paths = list(imutils.paths.list_images(imgs_dir))
        if len(img_paths) < 1:
            print('Image directory have nothing!')
            return 

        if reset_imgsize:
            h, w = reset_imgsize
        else:
            img = cv2.imread(img_paths[0])
            h, w = img.shape[:2]

        fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
        writer = cv2.VideoWriter(video_path, fourcc, fps, (w,h))
        
        img_paths = sorted(img_paths, key=lambda k: os.path.basename(k)[:-4])
        for img_path in tqdm(img_paths):
            img = cv2.imread(img_path)
            img = cv2.resize(img, (w,h))
            writer.write(img)

        writer.release()

    def putTextOnPillowImg(self,img, pos:tuple, color, text, text_size=30):
        pil_font = ImageFont.truetype("font/arial.ttf", text_size)
        # img = Image.open(img_path)
        draw = ImageDraw.Draw(img)
        draw.text(pos,text,color,font=pil_font)
        draw.text(pos,text,color,font=pil_font)

        return img

    def cv2AddChinaText(self, img, text, pos, color=(0, 0, 255), text_size=20):
        if isinstance(img, np.ndarray):
            img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("font/simsun.ttc", text_size, encoding='utf-8')
        draw.text(pos, text, color, font=font)
        return cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

    def randColor(self,):
        b = random.randint(0,255)
        g = random.randint(0,255)
        r = random.randint(0,255)
        return (b,g,r)

    def concateImgs(self, imgs_dir1, imgs_dir2, save_dir, concate_type="hconcate"):
        #---concate images with same basename from two directory
        assert self.checkDir(imgs_dir1) and self.checkDir(imgs_dir2)
        img_paths1 = list(imutils.paths.list_images(imgs_dir1))
        assert len(img_paths1) > 0

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        for path1 in img_paths1:
            file_name = os.path.basename(path1)
            path2 = os.path.join(imgs_dir2, file_name)

            if not  os.path.exists(path2):
                continue
            
            img1 = cv2.imread(path1)
            img2 = cv2.imread(path2)
            if img1 is None or img2 is None:continue

            if concate_type == "hconcate":
                img = cv2.hconcat((img1, img2))
            elif concate_type == "vconcate":
                img = cv2.vconcat((img1, img2))
            else:
                raise ValueError("Invalid concate type!")

            save_path = os.path.join(save_dir, file_name)
            cv2.imwrite(save_path, img)
