import time
import vapoursynth as vs
import functools

core = vs.core

def FrameTypeDeband(n,clip,y1=0,y2=0,y3=0,cr1=0,cr2=0,cr3=0,cb1=0,cb2=0,cb3=0,gy1=0,gy2=0,gy3=0,gc1=0,gc2=0,gc3=0,dynamic_grain=False):
    if clip.get_frame(n).props._PictType.decode() == "B":
        return core.neo_f3kdb.Deband(clip, y=y1, cr=cr1, cb=cb1, grainy=gy1, grainc=gc1,keep_tv_range=True, dynamic_grain=dynamic_grain)
    elif clip.get_frame(n).props._PictType.decode() == "P":
        return core.neo_f3kdb(clip, y=y2, cr=cr2, cb=cb2, grainy=gy2, grainc=gc2,keep_tv_range=True, dynamic_grain=dynamic_grain)
    else:
        return core.neo_f3kdb(clip, y=y3, cr=cr3, cb=cb3, grainy=gy3, grainc=gc3,keep_tv_range=True, dynamic_grain=dynamic_grain)

def ConditionalDeband(clip,y1=0,y2=0,y3=0,cr1=0,cr2=0,cr3=0,cb1=0,cb2=0,cb3=0,gy1=0,gy2=0,gy3=0,gc1=0,gc2=0,gc3=0,dynamic_grain=False):
    try:
        clip=core.std.FrameEval(clip, functools.partial(FrameTypeDeband,clip,y1,y2,y3,cr1,cr2,cr3,cb1,cb2,cb3,gy1,gy2,gy3,gc1,gc2,gc3,dynamic_grain))
    except Exception:
        pass
    return clip						



def FrameInfo(n, f, clip, frame_num=True, frame_type=True, frame_format=True, frame_resol=True, frame_fps=True, frame_time=False, frame_primaries=False, frame_matrix=False, frame_transfer=False, frame_chromaloc=False, frame_colorrange=False, frame_interlaced=False, frame_sar=False, frame_fullformat=False, text=None, color='0000FFFF', size=20, numpad=7, top=10, left=10):
    # NOTE: color is in format AABBGGRR
    
    lines = []
    
    if text:
        lines.append(text)
        lines.append('')
    
    if frame_num:
        lines.append(f'Frame {n} of {len(clip) - 1}')
    
    if frame_type:
        lines.append(f'Frame type: {f.props["_PictType"].decode("utf-8")}')
    
    if frame_format:
        lines.append(f'Frame format: {f.format.name}')
    
    if frame_resol:
        lines.append(f'Resolution: {f.width} x {f.height}')
    
    if frame_fps:
        lines.append(f'FPS: {clip.fps}')
    
    if frame_time:
        t = f.props["_AbsoluteTime"]
        (h, m) = divmod(t, 3600)
        (m, s) = divmod(m, 60)
        (s, ms) = divmod(s, 1)
        h = int(h)
        m = int(m)
        s = int(s)
        ms = int(ms * 1000)
        lines.append(f'Time: {h:02d}:{m:02d}:{s:02d}.{ms:03d}')
    
    if frame_primaries:
        PRIMARIES = {
                0 : 'reserved',
                1 : 'BT.709',
                2 : 'undef',
                3 : 'reserved',
                4 : 'BT.470 M',
                5 : 'BT.470 B/G',
                6 : 'BT.601',
                7 : 'SMPTE ST 240',
                8 : 'Generic film',
                9 : 'BT.2020',
               10 : 'SMPTE ST 428',
               11 : 'P3DCI',
               12 : 'P3D65',
               22 : 'EBU Tech. 3213-E'
               }
        
        try:
            lines.append(f'Primaries: {PRIMARIES[f.props["_Primaries"]]}')
        except Exception as e:
            lines.append(f'Primaries: {str(e)}')
    
    if frame_matrix:
        COLORMATRIX = {
                0 : 'RGB',
                1 : 'BT.709',
                2 : 'undef',
                3 : 'reserved',
                4 : 'FCC T47',
                5 : 'BT.470 B/G',
                6 : 'BT.601',
                7 : 'SMPTE ST 240',
                8 : 'YCgCo',
                9 : 'BT.2020ncl',
               10 : 'BT.2020cl',
               11 : 'SMPTE ST 2085',
               12 : 'Chroma ncl',
               13 : 'Chroma cl',
               14 : 'BT.2100'
               }
        
        try:
            lines.append(f'Color matrix: {COLORMATRIX[f.props["_Matrix"]]}')
        except Exception as e:
            lines.append(f'Color matrix: {str(e)}')
    
    if frame_transfer:
        TRANSFER = {
                0 : 'reserved',
                1 : 'BT.709',
                2 : 'undef',
                3 : 'reserved',
                4 : 'BT.470 M',
                5 : 'BT.470 B/G',
                6 : 'BT.601',
                7 : 'SMPTE ST 240',
                8 : 'linear',
                9 : 'log100',
               10 : 'log316',
               11 : 'xvycc (IEC 61966-2-4)',
               12 : 'BT.1361',
               13 : 'IEC 61966 sRGB',
               14 : 'BT.2020_10',
               15 : 'BT.2020_12',
               16 : 'SMPTE ST 2084',
               17 : 'SMPTE ST 428',
               18 : 'BT.2100 HLG'
               }
        
        try:
            lines.append(f'Transfer: {TRANSFER[f.props["_Transfer"]]}')
        except Exception as e:
            lines.append(f'Transfer: {str(e)}')
    
    if frame_chromaloc:
        CHROMALOC = {
                0 : 'left',
                1 : 'center',
                2 : 'top-left',
                3 : 'top',
                4 : 'bottom-left',
                5 : 'bottom'
                }
        
        try:
            lines.append(f'Chroma location: {f.props["_ChromaLocation"]}; {CHROMALOC[f.props["_ChromaLocation"]]}')
        except Exception as e:
            lines.append(f'Chroma location: {str(e)}')
    
    if frame_colorrange:
        COLORRANGE = {
                0 : 'full (PC)',
                1 : 'limited (TV)'
                }
    
        try:
            lines.append(f'Color range: {f.props["_ColorRange"]}; {COLORRANGE[f.props["_ColorRange"]]}')
        except Exception as e:
            lines.append(f'Color range: {str(e)}')
    
    if frame_interlaced:
        FIELDBASED = {
                0 : 'progressive',
                1 : 'BFF (Bottom Field First)',
                2 : 'TFF (Top Field First)'
                }
        
        try:
            lines.append(f'Field type: {f.props["_FieldBased"]}; {FIELDBASED[f.props["_FieldBased"]]}')
        except Exception as e:
            lines.append(f'Field type: {str(e)}')
    
    if frame_sar:
        lines.append(f'SAR: {f.props["_SARNum"]}:{f.props["_SARDen"]}')
    
    if frame_fullformat:
        lines.append(f'\n{f.format}')
    
    return clip.sub.Subtitle(
        '\n'.join(lines),
        start=n,
        end=n + 1,
        style=f'sans-serif,{size},&H{color},&H00000000,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,2,0,{numpad},{left},10,{top},1'
    )

def FFInfo(clip, **kwargs):
    return clip.std.FrameEval(functools.partial(FrameInfo, clip=clip, f=[clip], **kwargs), [clip])
    

#!/usr/bin/python
# -*- coding: utf-8 -*-


def HableTonemap(
    clip,
    source_peak=1200,
    ldr_nits=100,
    tFormat=vs.YUV420P8,
    tMatrix='709',
    tRange='limited',
    color_loc='center',
    ):
    
    clip = core.resize.Bilinear(
        clip=clip,
        format=vs.YUV444PS,
        range_in_s='limited',
        range_s='full',
        chromaloc_in_s=color_loc,
        dither_type='none',
        )
    clip = core.resize.Bilinear(clip=clip, format=vs.RGBS,
                                matrix_in_s='2020ncl', range_in_s='full'
                                , dither_type='none')
    clip = core.resize.Bilinear(
        clip=clip,
        format=vs.RGBS,
        transfer_in_s='st2084',
        transfer_s='linear',
        dither_type='none',
        nominal_luminance=source_peak,
        )
    exposure_bias = source_peak / ldr_nits  # set 150 or 200 for lowering the brightness

      # hable tone mapping
      # ["A"] = 0.22
      # ["B"] = 0.3
      # ["C"] = 0.1
      # ["D"] = 0.2
      # ["E"] = 0.01
      # ["F"] = 0.3
      # ["W"] = 11.2
      # ((x * (A*x + C*B) + D*E) / (x * (A*x+B) + D*F)) - E/F"

    tm = core.std.Expr(clip,
                       expr='x    {exposure_bias} * 0.22 x    {exposure_bias} * * 0.03 + * 0.002 +    x   {exposure_bias} * 0.22 x   {exposure_bias} * * 0.3 + * 0.06 + / 0.01 0.30 / -  '.format(exposure_bias=exposure_bias),
                       format=vs.RGBS)  # 12=1200 nits / 100 nits

    w = core.std.Expr(clip,
                      expr='{exposure_bias} 0.15 {exposure_bias} * 0.05 + * 0.004 + {exposure_bias} 0.15 {exposure_bias} * 0.50 + * 0.06 + / 0.02 0.30 / -  '.format(exposure_bias=exposure_bias),
                      format=vs.RGBS)  #

    clip = core.std.Expr(clips=[tm, w], expr=' x  1 y  / *  ',
                         format=vs.RGBS)
    clip = core.resize.Bilinear(clip=clip, format=vs.RGBS,
                                primaries_in_s='2020',
                                primaries_s=tMatrix, dither_type='none')
    clip = core.resize.Bilinear(clip=clip, format=vs.RGBS,
                                transfer_in_s='linear',
                                transfer_s=tMatrix, dither_type='none')

    if format != vs.RGBS:
        clip = core.resize.Bilinear(
            clip=clip,
            format=tFormat,
            matrix_s=tMatrix,
            range_in_s='full',
            range_s=tRange,
            chromaloc_in_s=color_loc,
            )
    return clip

	

