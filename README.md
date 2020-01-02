# YUVtool
A tool for editing yuv video file, specific YUV420 4k 10bit file.
## Main functions:
`readyuv420(filename, bitdepth, W, H, startframe, totalframe, show=False)`
Read target yuv file with certain bitdepth , width , height and length(frame number),from any frame. Return np data in Y,U,V.


`reshapeyuv(Y,U,V,H,W,totalframe)` Using 3 np data as Y,U,V, and a target height and width. Return new np datas in y,u,v.


`saveyuv(targetfile,Y,U,V,totalframe)`Save a yuv file using np data Y,U,V. 

## For Video Compression 2019 :
Just run `PlanJia()` or `PlanYi()` to get the video. I personally recommend 30 frame only version thanks to faster speed.
Because of the format of data of YUV420, to let all 600 frame cut, all 600 frame with 4K resolution must be pre-loaded in this design.

All the output video shoud be succesfully played in YUVplayer which is provided in class with correct resolution and format setttings.
The tests of 320x240 ver are build with only 20 frames. I'm not sure if the program works fine with total 600 frames.

**Notes: `totalframe` can be actually replaced by reading `Y.shape[0]`.
Any PR for better design is welcome.** 
