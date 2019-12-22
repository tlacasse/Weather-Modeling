import cv2
import numpy as np

def distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

class Projection:
    
    def __init__(self, reference_points, width, padding=0.1):
        self.reference_points = reference_points
        self.width = width
        self.padding = padding
        self._calc()
        
    def _calc(self):
        self.ref_lat_list = [abs(lat) for lat, long in self.reference_points]
        self.ref_long_list = [abs(long) for lat, long in self.reference_points]
        self.lat_bnd = (min(self.ref_lat_list), max(self.ref_lat_list))
        self.long_bnd = (min(self.ref_long_list), max(self.ref_long_list))
        self.lat_range = self.lat_bnd[1] - self.lat_bnd[0]
        self.long_range = self.long_bnd[1] - self.long_bnd[0]
        self.height = self.width * (self.lat_range / self.long_range)
        self.width_border = self.width * self.padding
        self.height_border = self.height * self.padding
        self.width_use = self.width - self.width_border - self.width_border
        self.height_use = self.height - self.height_border - self.height_border
        
    def get_dim(self):
        return int(round(self.height)), int(round(self.width))
        
    def on_points(self, latlong_list):
        def map_lat(l):
            l = (l - self.lat_bnd[0]) / self.lat_range
            l = self.height - (l * self.height_use) - self.height_border
            return int(round(l))
        def map_long(l):
            l = (l - self.long_bnd[0]) / self.long_range
            l = self.width - (l * self.width_use) - self.width_border
            return int(round(l))
        return [(map_lat(abs(lat)), map_long(abs(long))) for lat, long in latlong_list]   

def display_loop(iterable, func):
    for i in iterable:
        img = func(i)
        cv2.imshow('', img)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()
    
class RiverMapper:
    
    def __init__(self, size, kernel_size, weight):
        self.size = size
        self.kernel_size = kernel_size
        self.weight = weight
        self.kernel = self._build_kernel()
        
    def map_to_grid(self, data):
        img = np.zeros(self.size, dtype='double')
        for y, x, d in data:
            img[y, x] += d
            
        img = cv2.filter2D(img, -1, self.kernel)
        
        length = len(data)
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                # average and limit
                img[i, j] = min(img[i, j] / length, 255)
                
        return img.astype(dtype='uint8')
        
    def _build_kernel(self):
        mid = self.kernel_size // 2
        k = np.empty((self.kernel_size, self.kernel_size), dtype='double')
        for i in range(self.kernel_size):
            for j in range(self.kernel_size):
                k[i, j] = (2 + mid - distance(i, j, mid, mid)) * self.weight
        return k

def square_circle(size):
    points = []
    for i in range(size):
        for j in range(size):
            points.append((i, j))
    mid = size // 2
    points.sort(key=lambda p: distance(p[0], p[1], mid, mid))
    return points

class CloudCell:
    
    def __init__(self, i, j, sc, num=5):
        self.i = i
        self.j = j
        self.sc = sc
        self.clouds = []
        
        frac = num * 2
        border = self.sc / frac
        useable = self.sc - border - border
        for a, b in square_circle(num):
            self.clouds.append(Cloud(i, j, sc, 
                                     border + ((a/(num-1))*useable), 
                                     border + ((b/(num-1))*useable), 
                                     frac))
        interval = (num * num) / 4   
        self.conditions = {}
        self.conditions[5] = self.clouds
        self.conditions[4] = self.clouds
        self.conditions[3] = self._sublist(self.clouds, round(interval * 3))
        self.conditions[2] = self._sublist(self.conditions[3], round(interval * 2))
        self.conditions[1] = self._sublist(self.conditions[2], round(interval))
        self.conditions[0] = []
        
    def _sublist(self, a, size):
        return a[:size]
        
    def draw(self, img, cloud, direction, speed):
        for c in self.conditions[cloud]:
            c.draw(img, cloud, direction, speed)
        return img
    
    def _i(self, a=0):
        return (self.i + a) * self.sc
    
    def _j(self, a=0):
        return (self.j + a) * self.sc
    
class Cloud:
    
    def __init__(self, i, j, sc, pi, pj, frac):
        self.i = i
        self.j = j
        self.sc = sc
        self.pi = pi
        self.pj = pj
        self.frac = frac
        
    def draw(self, img, cloud, direction, speed):
        # 0 is "calm" wind
        if direction == 0:
            speed = 0
        direction -= 90 # orient correctly
        speed /= 4 # reduce to reasonable speed
        self.pi += speed * np.sin(np.deg2rad(direction))
        self.pj += speed * np.cos(np.deg2rad(direction))
        self.pi = self._wrap(self.pi)
        self.pj = self._wrap(self.pj)
        cv2.circle(img, (self._j(), self._i()), int(round((self.sc * 1.1) / self.frac)), 255, thickness=-1)
        return img
    
    def _i(self):
        return (self.i * self.sc) + int(round(self.pi))
    
    def _j(self):
        return (self.j * self.sc) + int(round(self.pj))
    
    def _wrap(self, val):
        if val < 0:
            val += self.sc
        if val >= self.sc:
            val -= self.sc
        return val
