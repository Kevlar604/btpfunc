import vapoursynth as vs
core = vs.get_core()
import functools
def FrameTypeDeband(n,clip,y1=0,y2=0,y3=0,cr1=0,cr2=0,cr3=0,cb1=0,cb2=0,cb3=0,gy1=0,gy2=0,gy3=0,gc1=0,gc2=0,gc3=0,dynamic_grain=False):
	if clip.get_frame(n).props._PictType.decode() == "B":
		return core.neo_f3kdb.Deband(clip, y=y1, cr=cr1, cb=cb1, grainy=gy1, grainc=gc1,keep_tv_range=True, dynamic_grain=dynamic_grain)
	elif clip.get_frame(n).props._PictType.decode() == "P":
		return core.neo_f3kdb(clip, y=y2, cr=cr2, cb=cb2, grainy=gy2, grainc=gc2,keep_tv_range=True, dynamic_grain=dynamic_grain)
	else:
		return core.neo_f3kdb(clip, y=y3, cr=cr3, cb=cb3, grainy=gy3, grainc=gc3,keep_tv_range=True, dynamic_grain=dynamic_grain)
		
def ConditionalDeband(clip,y1=0,y2=0,y3=0,cr1=0,cr2=0,cr3=0,cb1=0,cb2=0,cb3=0,gy1=0,gy2=0,gy3=0,gc1=0,gc2=0,gc3=0,dynamic_grain=False):
	try:
		clip=core.std.FrameEval(clip, functools.partial(FrameTypeDeband,clip,y1,y2,y3,cr1,cr2,cr3,cb1,cb2,cb3,gy1,gy2,gy3,gc1,gc2,gc3,dynamic_grain)
	except Exception:
		pass
	return clip						
					
