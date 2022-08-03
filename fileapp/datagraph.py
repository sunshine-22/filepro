import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas as pd
import numpy as np

def piegraph(profile1count,profile2count,commonwords):
    listdata=[]
    listdata.append(profile1count)
    listdata.append(profile2count)
    listdata.append(commonwords)
    graphdata=np.array(listdata)
    mylabels=["Source File Count","Target File Count","Common files"]
    plt.switch_backend("AGG")
    plt.figure(figsize=(6,5))
    plt.title("File Compare")
    plt.pie(graphdata,labels=mylabels)
    plt.legend()
    #plt.xticks(rotation=45)
    #plt.xlabel("File Data")
    #plt.ylabel("File Count")
    plt.tight_layout()
    buffer=BytesIO()
    plt.savefig(buffer,format="png")
    buffer.seek(0)
    image_png=buffer.getvalue()
    graph=base64.b64encode(image_png)
    graph=graph.decode("utf-8")
    buffer.close()
    return graph
