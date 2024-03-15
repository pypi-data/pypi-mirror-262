from registration import register
from registration.default_ops import default_ops
from tifffile import imread, TiffFile, TiffWriter
import numpy as np
import math, time

time_start = time.time()
#Parameter settings
bins=100       #Num of frames in a bin
ops = default_ops()
# ops['nimg_init'] = 100
# ops['batch_size'] = 50
# ops['nonrigid'] = True

#Information loading
Image = imread(r'D:\SynologyDrive\LAB-share\Member-HuJiaHao\Astrocyte_morphorogy_iterationAverage\file_00009_ch1_deepcad_output.tif')
if np.min(Image)>32768:
    Image = Image-32768
Image = Image.astype(np.float32)
n_frames, Ly, Lx = Image.shape
reg_Image = np.zeros((n_frames, Ly, Lx))
Numofbins = math.ceil(n_frames/bins)
MidNum = round(Numofbins/2)
refImg=np.zeros((Numofbins,Ly,Lx))

#compute all reference Image
# for i in range(0,Numofbins-1):
#     Slice=Image[i*100:(i+1)*100-1,:,:]
#     refSlice = register.compute_reference(Slice, ops)
#     refImg[i,:,:]=refSlice
# Slice=Image[(Numofbins-1)*100:-1,:,:]
# refSlice = register.compute_reference(Slice, ops)
# refImg[Numofbins-1,:,:]=refSlice

#Registration of the mid bin of the frame
Slice = Image[(MidNum-1)*100:MidNum*100,:,:]
MidrefSlice = register.compute_reference(Slice,ops)
maskMul, maskOffset, cfRefImg, maskMulNR, maskOffsetNR, cfRefImgNR, blocks = register.compute_reference_masks(MidrefSlice, ops)
refAndMasks = [maskMul, maskOffset, cfRefImg, maskMulNR, maskOffsetNR, cfRefImgNR, blocks ]
reg_Slice, ymax , xmax , cmax, ymax1, xmax1, cmax1, nonsense = register.register_frames(refAndMasks, Slice, rmin=-np.inf, rmax=np.inf, bidiphase=0, ops=default_ops(), nZ=1)
reg_Image[(MidNum-1)*100:MidNum*100, :, :]=reg_Slice

#Registration of the second half of the frame
for i in range(MidNum,Numofbins-1):
    if i == MidNum:
        refSlice=MidrefSlice
    Slice = Image[i*100:(i+1)*100,:,:]
    maskMul, maskOffset, cfRefImg, maskMulNR, maskOffsetNR, cfRefImgNR, blocks = register.compute_reference_masks(
        refSlice, ops)
    refAndMasks = [maskMul, maskOffset, cfRefImg, maskMulNR, maskOffsetNR, cfRefImgNR, blocks]
    reg_Slice, ymax, xmax, cmax, ymax1, xmax1, cmax1, nonsense = register.register_frames(refAndMasks, Slice,
                                                                                          rmin=-np.inf, rmax=np.inf,
                                                                                          bidiphase=0,
                                                                                          ops=default_ops(), nZ=1)
    reg_Image[i*100:(i+1)*100,:,:] = reg_Slice
    refSlice = register.compute_reference(Slice, ops)

#Registration of the last bin of the frame
Slice=Image[(Numofbins-1)*100:,:,:]
maskMul, maskOffset, cfRefImg, maskMulNR, maskOffsetNR, cfRefImgNR, blocks = register.compute_reference_masks(refSlice,ops)
refAndMasks = [maskMul, maskOffset, cfRefImg, maskMulNR, maskOffsetNR, cfRefImgNR, blocks ]
reg_Slice, ymax , xmax , cmax, ymax1, xmax1, cmax1, nonsense = register.register_frames(refAndMasks, Slice, rmin=-np.inf, rmax=np.inf, bidiphase=0, ops=default_ops(), nZ=1)
reg_Image[(Numofbins-1)*100:,:,:]=reg_Slice

#Registration of the first half of the frame
for i in range(0,MidNum-1):
    if i == 0:
        refSlice=MidrefSlice
    Slice = Image[(MidNum-i-2)*100:(MidNum-i-1)*100,:,:]
    maskMul, maskOffset, cfRefImg, maskMulNR, maskOffsetNR, cfRefImgNR, blocks = register.compute_reference_masks(
        refSlice, ops)
    refAndMasks = [maskMul, maskOffset, cfRefImg, maskMulNR, maskOffsetNR, cfRefImgNR, blocks]
    reg_Slice, ymax, xmax, cmax, ymax1, xmax1, cmax1, nonsense = register.register_frames(refAndMasks, Slice,
                                                                                          rmin=-np.inf, rmax=np.inf,
                                                                                          bidiphase=0,
                                                                                          ops=default_ops(), nZ=1)
    reg_Image[(MidNum-i-2)*100:(MidNum-i-1)*100,:,:] = reg_Slice
    refSlice = register.compute_reference(Slice, ops)

with TiffWriter(r'D:\SynologyDrive\LAB-share\Member-HuJiaHao\Astrocyte_morphorogy_iterationAverage\reg.tif') as tif:
     tif.write(np.floor(reg_Image).astype(np.int16))

#Program run time
time_end = time.time()
time_sum = time_end - time_start
print(time_sum)