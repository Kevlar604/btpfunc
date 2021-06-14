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
		return core.std.FrameEval(src, functools.partial(FrameTypeDeband,clip=clip,y1=y1,y2=y2,y3=y3,cr1=cr1,cr2=cr2,cr3=cr3,cb1=cb1,cb2=cb2,cb3=cb3,gy1=gy1,gy2=gy2,gy3=gy3,gc1=gc1,gc2=gc2,gc3=gc3,dynamic_grain=dynamic_grain)
