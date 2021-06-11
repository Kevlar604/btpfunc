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


def tm_hable(clip="",source_peak=1000 ) :
	core = vs.get_core()
    	c=clip

    	source_peak=source_peak 
    	LDR_nits=100     
    	exposure_bias=source_peak/LDR_nits
    	o=c
    	c=core.std.Limiter(c, 0)     
    	r=core.std.ShufflePlanes(c, planes=[0], colorfamily=vs.GRAY)
    	g=core.std.ShufflePlanes(c, planes=[1], colorfamily=vs.GRAY)
    	b=core.std.ShufflePlanes(c, planes=[2], colorfamily=vs.GRAY)
    	lum = core.std.Expr(clips=[r,g,b], expr="0.216 x * 0.715 y * + 0.0722 z * +")
    	lum=core.std.Limiter(lum, 0)
    	lum=core.std.ShufflePlanes(lum, planes=[0], colorfamily=vs.RGB)



    
    	rr="x  {exposure_bias} * 0.15 x  {exposure_bias} * * 0.05 + * 0.004 + x  {exposure_bias} * 0.15 x  {exposure_bias} * * 0.50 + * 0.06 + / 0.02 0.30 / - 1 {exposure_bias} 0.15 {exposure_bias} * 0.05 + * 0.004 + {exposure_bias} 0.15 {exposure_bias} * 0.50 + * 0.06 + / 0.02 0.30 / - / * ".format(exposure_bias=exposure_bias)
    	gg="y  {exposure_bias} * 0.15 y  {exposure_bias} * * 0.05 + * 0.004 + y  {exposure_bias} * 0.15 y  {exposure_bias} * * 0.50 + * 0.06 + / 0.02 0.30 / - 1 {exposure_bias} 0.15 {exposure_bias} * 0.05 + * 0.004 + {exposure_bias} 0.15 {exposure_bias} * 0.50 + * 0.06 + / 0.02 0.30 / - / * ".format(exposure_bias=exposure_bias)
    	bb="z {exposure_bias} * 0.15 z  {exposure_bias} * * 0.05 + * 0.004 + z  {exposure_bias} * 0.15 z  {exposure_bias} * * 0.50 + * 0.06 + / 0.02 0.30 / - 1 {exposure_bias} 0.15 {exposure_bias} * 0.05 + * 0.004 + {exposure_bias} 0.15 {exposure_bias} * 0.50 + * 0.06 + / 0.02 0.30 / - / * ".format(exposure_bias=exposure_bias)


    	r1 = core.std.Expr(clips=[r,g,b], expr="x y >=   y z > {rr}   z x > x y - z y - / {bb} {gg} - * {gg} +     z y > {rr} {rr}   ?  ?     ?    x z >=   x z - y z - / {gg} {bb} - * {bb} + z y >  {rr}   {rr}            ? ? ?     ".format(exposure_bias=exposure_bias,rr=rr,gg=gg,bb=bb))
    	g1 = core.std.Expr(clips=[r,g,b], expr="x y >=   y z > y z - x z - / {rr} {bb} - * {bb} +  z x > {gg}      z y > {gg}  {gg}   ?  ?     ?    x z >=   {gg}  z y >  y x - z x - / {bb} {rr} - * {rr} +   {gg}            ? ? ?        ".format(exposure_bias=exposure_bias,rr=rr,gg=gg,bb=bb))
    	b1 = core.std.Expr(clips=[r,g,b], expr="x y >=   y z > {bb}   z x > {bb}      z y > z y -  x y - / {rr} {gg} - * {gg} +  {bb}   ?  ?     ?    x z >=   {bb}  z y >  {bb}   z x - y x - / {gg} {rr} - * {rr} +            ? ? ?    ".format(exposure_bias=exposure_bias,rr=rr,gg=gg,bb=bb))

    	crgb=core.std.ShufflePlanes(clips=[r1,g1,b1], planes=[0,0,0], colorfamily=vs.RGB)


    	lumtm = core.std.Expr(clips=[r1,g1,b1], expr="0.216 x * 0.715 y * + 0.0722 z * +")
    	lumtm=core.std.Limiter(lumtm, 0)
    	lumtm=core.std.ShufflePlanes(lumtm, planes=[0], colorfamily=vs.RGB)
    	clum = core.std.Expr(clips=[o,lum,lumtm], expr=" x {exposure_bias} *  y {exposure_bias} *  / z *  ".format(exposure_bias=exposure_bias))
    	clum=core.std.Limiter(clum, 0)    

    	mask=core.std.Expr(clips=[lum,lumtm], expr=" x {exposure_bias} * y - abs {exposure_bias}  1 - /  ".format(exposure_bias=exposure_bias))
    	mask=core.std.Limiter(mask, 0,1)

                       
    	ctemp=core.std.MaskedMerge(crgb, lumtm, mask)
    	c=core.std.Merge(clum, ctemp, 0.5)

	return c				

	
							 
def HableTonemap(clip="")							 
	source_peak=1200 
	matrix_in_s="2020ncl"
	transfer_in_s="st2084"


	c=core.resize.Bicubic(clip=c, format=vs.RGBS, filter_param_a=0, filter_param_b=0.75, matrix_in_s=matrix_in_s,chromaloc_in_s="center",chromaloc_s="center", range_in_s="limited",dither_type="none")

	c=core.resize.Bilinear(clip=c, format=vs.RGBS, transfer_in_s=transfer_in_s, transfer_s="linear",dither_type="none", nominal_luminance=source_peak)



	c=tonemapping.tm_hable(c,source_peak=source_peak )

	c=core.resize.Bilinear(clip=c, format=vs.RGBS, primaries_in_s="2020", primaries_s="709",dither_type="none")
	c=core.resize.Bilinear(clip=c, format=vs.RGBS, transfer_in_s="linear", transfer_s="709",dither_type="none")

	c=core.resize.Bicubic(clip=c, format=vs.YUV420P8,matrix_s="709", filter_param_a=0, filter_param_b=0.75, range_in_s="full",range_s="limited", chromaloc_in_s="center", chromaloc_s="center",dither_type="none")

	return c						 
							 
							 
