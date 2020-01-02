
# -*- coding: utf-8 -*-
 
import math
from functools import partial
import numpy as np
import matplotlib.pyplot as plt
 
 
def readyuv420(filename, bitdepth, W, H, startframe, totalframe, show=False):
    uv_H = H // 2
    uv_W = W // 2
 
    if bitdepth == 8:
        Y = np.zeros((totalframe, H, W), np.uint8)
        U = np.zeros((totalframe, uv_H, uv_W), np.uint8)
        V = np.zeros((totalframe, uv_H, uv_W), np.uint8)
    elif bitdepth == 10:
        Y = np.zeros((totalframe, H, W), np.uint16)
        U = np.zeros((totalframe, uv_H, uv_W), np.uint16)
        V = np.zeros((totalframe, uv_H, uv_W), np.uint16)
 
    plt.ion()
 
    bytes2num = partial(int.from_bytes, byteorder='little', signed=False)
    #num2bytes = partial(int.to_bytes,2,byteorder='little', signed=False)
 
    bytesPerPixel = math.ceil(bitdepth / 8)
    seekPixels = startframe * H * W * 3 // 2
    fp = open(filename, 'rb')
    fp.seek(bytesPerPixel * seekPixels)
    
    print("bytesPerpixel:",bytesPerPixel)
    print("seekPixels:",seekPixels)
 
    for i in range(totalframe):
 
        for m in range(H):
            for n in range(W):
                if bitdepth == 8:
                    pel = bytes2num(fp.read(1))
           
                    Y[i, m, n] = np.uint8(pel)
                elif bitdepth == 10:
                    pel = bytes2num(fp.read(2))
                   
                    Y[i, m, n] = np.uint16(pel)
               
                    
 
        for m in range(uv_H):
            for n in range(uv_W):
                if bitdepth == 8:
                    pel = bytes2num(fp.read(1))
                    U[i, m, n] = np.uint8(pel)
                elif bitdepth == 10:
                    pel = bytes2num(fp.read(2))
                    
                    U[i, m, n] = np.uint16(pel)
 
        for m in range(uv_H):
            for n in range(uv_W):
                if bitdepth == 8:
                    pel = bytes2num(fp.read(1))
                  
                    V[i, m, n] = np.uint8(pel)
                elif bitdepth == 10:
                    pel = bytes2num(fp.read(2))
                    
                    V[i, m, n] = np.uint16(pel)
        print('No.',i,'frame is read')
        if show:
            print(i)
            plt.subplot(131)
            plt.imshow(Y[i, :, :], cmap='gray')
            plt.subplot(132)
            plt.imshow(U[i, :, :], cmap='gray')
            plt.subplot(133)
            plt.imshow(V[i, :, :], cmap='gray')
            plt.show()
            plt.pause(1)
            
    if totalframe==1:
        return Y[0], U[0], V[0] #this will ruin other function,if you do need single frame, please take care of the dimension when rewriting.
    else:
        return Y,U,V
def reshapeyuv(Y,U,V,H,W,totalframe):#convert 4k into target H W
    uv_H=H//2
    uv_W=W//2
    
    y = np.zeros((totalframe, H, W), np.uint16)
    u = np.zeros((totalframe, uv_H, uv_W), np.uint16)
    v = np.zeros((totalframe, uv_H, uv_W), np.uint16)

    #to move the window, extra offsets can be add in these 4 values below:
    ystartpoint_w=3840//2-W//2
    ystartpoint_h=2160//2-H//2
    uvstartpoint_w=1920//2-uv_H//2 
    uvstartpoint_h=1080//2-uv_W//2

    for i in range(totalframe):
        for m in range(H):
            for n in range(W):
                ms=m+ystartpoint_h
                ns=n+ystartpoint_w
               # print(ms,ns,i,m,n)
                y[i, m, n]=Y[i,ms,ns]
        for m in range(uv_H):
            for n in range(uv_W):
                ms=m+uvstartpoint_h
                ns=n+uvstartpoint_w
                u[i,m,n]=U[i,ms,ns]
        for m in range(uv_H):
            for n in range(uv_W):
                ms=m+uvstartpoint_h
                ns=n+uvstartpoint_w
                v[i,m,n]=V[i,ms,ns]
        print('No.',i,"frame is reshaped")
    return y,u,v

def saveyuv(targetfile,Y,U,V,totalframe):
    H=Y.shape[1]
    W=Y.shape[2]
    print('save as ',Y.shape[2],'x',Y.shape[1])
    fs=open(targetfile,'wb')
    uv_H=H//2
    uv_W=W//2
    for i in range(totalframe):
        for m in range(H):
            for n in range(W):
                pel=int(Y[i, m, n]).to_bytes(2,byteorder='little', signed=False); 
                fs.write(pel)
        for m in range(uv_H):
            for n in range(uv_W):
                pel=int(U[i, m, n]).to_bytes(2,byteorder='little', signed=False); 
                fs.write(pel)
        for m in range(uv_H):
            for n in range(uv_W):
                pel=int(V[i, m, n]).to_bytes(2,byteorder='little', signed=False); 
                fs.write(pel)
        print("No.",i,"frame is saved")
    fs.close()
    print('procedure done')

def PlanJia():
    Y,U,V=readyuv420(r'Campfire_3840x2160_30fps_bt709_420_videoRange.yuv',10, 3840,2160, 0, 600,False)
    y,u,v=reshapeyuv(Y,U,V,240,320,600)
    saveyuv('Campfire_320x240.yuv',y,u,v,600)

def PlanYi():
    Y,U,V=readyuv420(r'Campfire_3840x2160_30fps_bt709_420_videoRange.yuv',10, 3840,2160, 0, 30,False)
    print(Y.shape,U.shape,V.shape)
    saveyuv('first_30_of_Campfire_3840x2160.yuv',Y,U,V,30)

if __name__ == '__main__':
    PlanJia()
    #PlanYi()

