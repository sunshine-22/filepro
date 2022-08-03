from django.shortcuts import render
from . datagraph import piegraph
import os

def home(request):
    if(request.method=="POST") and "sfile" in request.POST:
        commonwords=0
        file1=request.FILES.get("file1").read()
        file2=request.FILES.get("file2").read()
        profile1=file1.decode("utf-8")
        profile2=file2.decode("utf-8")
        sfile=profile1
        tfile=profile2
        profile1=profile1.split(" ")
        profile2=profile2.split(" ")
        profile1=[x.replace("files.\r\n\r\n","") for x in profile1]
        profile2=[x.replace("files.\r\n\r\n","") for x in profile2]
        profile1count=len(profile1)
        profile2count=len(profile2)
        for i in profile1[:]:
            if(i in profile2):
                commonwords+=1
                profile1.remove(i)
                profile2.remove(i)
        print(profile1)
        print(profile2)
        msg="Removals"
        msg2="Additions"
        fileid1="Source File"
        fileid2="Target File"
        removalcount=len(profile1)
        additioncount=len(profile2)
        text=""
        text2=""
        for i in profile2:
            text=text+i+" "
        for i in profile1:
            text2=text2+i+" "
        if(removalcount==0 and additioncount==0):
            text="Two Files are Identical"
            text2="Two Files are Identical"
        return render(request,"fileapp/home.html",{"msg":msg,"msg2":msg2,"data":text2,"words":text,"sfile":sfile,"tfile":tfile,"fileid1":fileid1,"fileid2":fileid2,
                                                   "profilecount":profile1count,"profile2count":profile2count,"commonwords":commonwords,"removalcount":removalcount,"additioncount":additioncount})
    return render(request,"fileapp/home.html")
def foldercompare(request):
    if(request.method=="POST"):
        sfolder=request.POST.get("sfolder")
        tfolder=request.POST.get("tfolder")
        sfolderfiles=[]
        tfolderfiles=[]
        sfolderfolder=[]
        tfolderfolder=[]
        commonsourcefiles=[]
        #commontargetfiles=[]
        smatch=[os.path.join(r,file) for r,d,f in os.walk(sfolder) for file in f]
        tmatch=[os.path.join(r,file) for r,d,f in os.walk(tfolder) for file in f]
        for i in smatch:
            with open(i,"rb") as f:
                data=f.readlines()
                for j in tmatch:
                    with open(j,"rb") as f2:
                        data2=f2.readlines()
                        if(data==data2):
                            temp=[i,j]
                            commonsourcefiles.append(temp)
                            
                            
        for i in range(len(smatch)):
            smatch[i]=smatch[i].replace(sfolder,"")
            smatch[i]=smatch[i].split("\\")
        for i in smatch:
            for j in i:
                if("." in j):
                    sfolderfiles.append(j)
                else:
                    if(j not in sfolderfolder):
                       sfolderfolder.append(j)
        

        for i in range(len(tmatch)):
            tmatch[i]=tmatch[i].replace(tfolder,"")
            tmatch[i]=tmatch[i].split("\\")
        
        for i in tmatch:
            for j in i:
                if("." in j):
                    tfolderfiles.append(j)
                else:
                    if(j not in tfolderfolder):
                       tfolderfolder.append(j)
        print(commonsourcefiles)
        #print(commontargetfiles)
        print(sfolderfolder)
        print(tfolderfolder)
        graph=piegraph(len(sfolderfiles),len(tfolderfiles),len(commonsourcefiles))
        msg="Source Folder Files"
        msg2="Target Folder Files"
        msg3="List of Folder's in Source"
        msg4="List of Folder's in Target"
        return render(request,"fileapp/folder.html",{"msg":msg,"msg2":msg2,"sfolderfiles":sfolderfiles,
                                                     "tfolderfiles":tfolderfiles,"commonsourcefiles":commonsourcefiles,"msg3":msg3,"msg4":msg4,"sfolderfolder":sfolderfolder,
                                                     "tfolderfolder":tfolderfolder,"graph":graph})
    return render(request,"fileapp/folder.html")
