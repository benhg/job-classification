"""Generates histograms for all percentile field outputs in directory."""
fields=["List","of","fields"]
for field in fields:
    d=json.loads(open("output_percentile_%s.json"%field).read())
    print(d)
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    plt.bar(list(d.keys()), list(d.values()), align='center')
    plt.xticks(list(range(len(d))), list(d.keys()))
    plt.yticks(np.arange(0,max(d.values()),.05))
    plt.xlabel('Number of Citations %ile')
    plt.ylabel('Email Coverage')
    plt.title('History')
    plt.savefig("%s.png"%field)