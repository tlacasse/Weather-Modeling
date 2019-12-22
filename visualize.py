from weather.source import build_dataset, RIVERS
import cv2
import numpy as np

# FTTV, SBWS, CTTV, BBBB
data = build_dataset()

pos = {r.code: (r.lat_coord(), r.long_coord()) for r in RIVERS.values()}
print(pos)
pos = {k: [int((70 - v[0] - 6)), int((70 - v[1] - 19))] for k, v in pos.items()}
# pos = {k: [int((70 - v[1] - 8)), int((70 - v[0] - 20))] for k, v in pos.items()}

maxs = {r: max(data[r]) for r in RIVERS.keys()}

def dist(x1, y1, x2, y2):
   # return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return np.abs(x2 - x1) + np.abs(y2 - y1)

def build_kernel(size):
    mid = int(np.floor(size / 2))
    kernel = np.zeros((size, size), dtype='double')
    for i in range(kernel.shape[0]):
        for j in range(kernel.shape[1]):
            kernel[i][j] = size - dist(i, j, mid, mid)
    return kernel
            
kernel = build_kernel(5)
#kernel = np.ones((5, 5))
print(kernel)

for i in range(len(data['FTTV'])):
    #img = np.zeros((13, 23), dtype='uint8')
    size = (16, 26)
    img = np.zeros(size, dtype='double')
    
    for r in RIVERS.keys():
        for x in range(-5, 6, 1):
            for y in range(-5, 6, 1):
                img[pos[r][0]+x, pos[r][1]+y] += min(int((data[r][i] / maxs[r]) * 300), 255)
                
    #img = cv2.resize(img, (1150, 650), interpolation=cv2.INTER_NEAREST)#
    #kernel = np.ones((5, 5))
    #img = cv2.GaussianBlur(img, (25, 25), 10)
    #img[:, :] *= 10
    #img = cv2.GaussianBlur(img, (5, 5), 500)
    #img = cv2.filter2D(img.astype(np.float32), -1, kernel)
    img = img.astype(dtype='uint8')
    img = cv2.resize(img, (size[1]*30, size[0]*30), interpolation=cv2.INTER_NEAREST)
    
    
    cv2.imshow('GageHeight', img)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
    