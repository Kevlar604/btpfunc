import vapoursynth as vs
core = vs.get_core()
import functools
def FrameTypeDeband(n,clip,y1,y2,y3,cr1,cr2,cr3,cb1,cb2,cb3,gy1,gy2,gy3,gc1,gc2,gc3,dynamic_grain):
	if clip.get_frame(n).props._PictType.decode() == "B":
		return core.neo_f3kdb.Deband(clip, y=y1, cr=cr1, cb=cb1, grainy=gy1, grainc=gc1,keep_tv_range=True, dynamic_grain=dynamic_grain)
	elif clip.get_frame(n).props._PictType.decode() == "P":
		return core.neo_f3kdb(clip, y=y2, cr=cr2, cb=cb2, grainy=gy2, grainc=gc2,keep_tv_range=True, dynamic_grain=dynamic_grain)
	else:
		return core.neo_f3kdb(clip, y=y3, cr=cr3, cb=cb3, grainy=gy3, grainc=gc3,keep_tv_range=True, dynamic_grain=dynamic_grain)
		
def ConditionalDeband(clip,y1,y2,y3,cr1,cr2,cr3,cb1,cb2,cb3,gy1,gy2,gy3,gc1,gc2,gc3,dynamic_grain):
	return core.std.FrameEval(src, functools.partial(FrameTypeDeband,clip=clip,y1=y1,y2=y2,y3=y3,cr1=cr1,cr2=cr2,cr3=cr3,cb1=cb1,cb2=cb2,cb3=cb3,gy1=gy1,gy2=gy2,gy3=gy3,gc1=gc1,gc2=gc2,gc3=gc3,dynamic_grain=dynamic


def hablehdr10tosdr(clip, source_peak=1200, ldr_nits=100, tFormat=vs.YUV420P8, tMatrix="709", tRange="limited", color_loc="center"):
  core = vs.get_core()
  clip=core.resize.Bilinear(clip=clip, format=vs.YUV444PS,range_in_s="limited", range_s="full",chromaloc_in_s=color_loc,dither_type="none")
  clip=core.resize.Bilinear(clip=clip, format=vs.RGBS, matrix_in_s="2020ncl", range_in_s="full",dither_type="none")
  clip=core.resize.Bilinear(clip=clip, format=vs.RGBS, transfer_in_s="st2084", transfer_s="linear",dither_type="none", nominal_luminance=source_peak)
  exposure_bias=(source_peak/ldr_nits) #set 150 or 200 for lowering the brightness

  #hable tone mapping
  #["A"] = 0.22
  #["B"] = 0.3
  #["C"] = 0.1
  #["D"] = 0.2
  #["E"] = 0.01
  #["F"] = 0.3
  #["W"] = 11.2
  #((x * (A*x + C*B) + D*E) / (x * (A*x+B) + D*F)) - E/F"   
  tm = core.std.Expr(clip, expr="x    {exposure_bias} * 0.22 x    {exposure_bias} * * 0.03 + * 0.002 +    x   {exposure_bias} * 0.22 x   {exposure_bias} * * 0.3 + * 0.06 + / 0.01 0.30 / -  ".format(exposure_bias=exposure_bias),format=vs.RGBS)#12=1200 nits / 100 nits
  
  w = core.std.Expr(clip, expr="{exposure_bias} 0.15 {exposure_bias} * 0.05 + * 0.004 + {exposure_bias} 0.15 {exposure_bias} * 0.50 + * 0.06 + / 0.02 0.30 / -  ".format(exposure_bias=exposure_bias),format=vs.RGBS)#  

  clip = core.std.Expr(clips=[tm,w], expr=" x  1 y  / *  ",format=vs.RGBS)
  clip=core.resize.Bilinear(clip=clip, format=vs.RGBS, primaries_in_s="2020", primaries_s=tMatrix,dither_type="none")
  clip=core.resize.Bilinear(clip=clip, format=vs.RGBS, transfer_in_s="linear", transfer_s=tMatrix,dither_type="none")

  if format != vs.RGBS:
    clip=core.resize.Bilinear(clip=clip, format=tFormat, matrix_s=tMatrix, range_in_s="full",range_s=tRange,chromaloc_in_s=color_loc)
  return clip
