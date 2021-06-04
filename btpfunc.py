import vapoursynth as vs
core = vs.get_core()
import functools
def FrameTypeDeband(n,clip,y1,y2,y3,cr1,cr2,cr3,cb1,cb2,cb3):
	if clip.get_frame(n).props._PictType.decode() == "B":
		return core.neo_f3kdb.Deband(clip, y=y1, cr=cr1, cb=cb1, grainy=64, grainc=0,keep_tv_range=True, dynamic_grain=False)
	elif clip.get_frame(n).props._PictType.decode() == "P":
		return core.neo_f3kdb(clip, y=y2, cr=cr2, cb=cb2, grainy=64, grainc=0,keep_tv_range=True, dynamic_grain=False)
	else:
		return core.neo_f3kdb(clip, y=y3, cr=cr3, cb=cb3, grainy=64, grainc=0,keep_tv_range=True, dynamic_grain=False)
		
def ConditionalDeband(clip,y1,y2,y3,cr1,cr2,cr3,cb1,cb2,cb3):
	return core.std.FrameEval(src, functools.partial(FrameTypeDeband,clip=clip,y1=y1,y2=y2,y3=y3,cr1=cr1,cr2=cr2,cr3=cr3,cb1=cb1,cb2=cb2,cb3=cb3))
