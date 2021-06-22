# btpfunc
A collection of vapoursynth functions. More functions will be added later. 

## ConditionalDeband
Syntax **clip=btpfunc.ConditionalDeband(clip,y1,y2,y3,cb1,cb2,cb3,cr1,cr2,cr3,gy1,gy2,gy3,gc1,gc2,gc3,dynamic_grain)**

What it does is conditional debanding based of Frametype B,P,I

y1=luma value of B frame

y2=luma value of P frame

y3=luma value of I frame

cb1,cr1=chroma values of B frame

cb2,cr2=chroma values of P frame

cb3,cr3=chroma values of I frame

gy1=grain to be added to the luma plain of B frame

gy2=grain to be added to the luma plain of P frame

gy3=grain to be added to the luma plain of I frame

gc1=grain to be added to the chroma plain of B frame

gc2=grain to be added to the chroma plain of P frame

gc3=grain to be added to the chroma plain of I frame

bool dynamic_grain: If true grains added will be dynamic else if false it will be static

Usage example clip=ConditionalDeband(clip,64,32,20,32,0,0,32,0,0,0,0,0,0,0,0,True)

## FFInfo

Shows general information about the current frame.

Example 
**clip = btpfunc.FFInfo(clip, text='Flip da script', frame_num=False, frame_type=False, frame_format=False, frame_resol=False, frame_fps=False, frame_time=False, frame_primaries=False, frame_matrix=False, frame_transfer=False, frame_chromaloc=False, frame_interlaced=False, frame_sar=False, frame_fullformat=False, color='0000FFFF', size=20, top=8)

