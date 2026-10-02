import cv2
import numpy as np

def resize_for_ocr(img: np.ndarray, target_width: int = 900) -> np.ndarray:
    h,w=img.shape[:2]
    if w>=target_width: return img
    scale=target_width/max(w,1)
    return cv2.resize(img,(int(w*scale),int(h*scale)),interpolation=cv2.INTER_CUBIC)

def reduce_glare(gray: np.ndarray) -> np.ndarray:
    clipped=np.minimum(gray,245).astype(np.uint8)
    return cv2.GaussianBlur(clipped,(3,3),0)

def enhance_variants(crop: np.ndarray) -> list[np.ndarray]:
    gray=cv2.cvtColor(crop,cv2.COLOR_BGR2GRAY) if len(crop.shape)==3 else crop
    gray=resize_for_ocr(gray)
    den=cv2.fastNlMeansDenoising(gray,None,7,7,21)
    clahe=cv2.createCLAHE(clipLimit=2.2,tileGridSize=(8,8)).apply(den)
    glare=reduce_glare(clahe)
    blur=cv2.GaussianBlur(glare,(0,0),1.1)
    sharp=cv2.addWeighted(glare,1.6,blur,-0.6,0)
    adapt=cv2.adaptiveThreshold(sharp,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,31,7)
    otsu=cv2.threshold(sharp,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    return [gray,clahe,sharp,adapt,otsu]
