# btpfunc
A collection of vapoursynth functions. More functions will be added later. 
Currently the script does conditional debanding.
Syntax **clip=ConditionalDeband(clip,y1,y2,y3,cb1,cb2,cb3,cr1,cr2,cr3)**
What it does is conditional debanding based of Frametype B,P,I
y1=luma value of B frame
y2=luma value of P frame
y3=luma value of I frame
cb1,cr1=chroma values of B frame
cb2,cr2=chroma values of P frame
cb3,cr3=chroma values of I frame
for example clip=ConditionalDeband(clip,y1,y2,y3,cb1,cb2,cb3,cr1,cr2,cr3)



