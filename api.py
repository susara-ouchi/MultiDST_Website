from fastapi import FastAPI
from pydantic import BaseModel
from multidst.functions import multitest
from multidst.utils.visualization import multidst_hist , sigindex_plot
from fastapi.staticfiles import StaticFiles

import time 
class P_Values(BaseModel):
    p_values: str

app = FastAPI()

# Serve the images directory
app.mount("/images", StaticFiles(directory="images"), name="images")

# to run the uvicorn dev server uvicorn api:app
@app.get("/")
async def root():
    return {"message": "Hello World"}


#send p values and methods
@app.post("/analyze")
async def analyze(request:P_Values):
    number_strings = request.p_values.split(',')
    number_list = [float(num) for num in number_strings]
    number_tuple = tuple(number_list)
    #unique_plot_name
    ts = str(time.time())
    ts=ts.replace('.','')
    #Histogram
    g2_index = []
    multidst_hist(number_tuple, g2_index, title="Histogram of p-values",col1 = 'skyblue', col2 = 'purple', save_plot=True, timestamp=ts)
    #sigplot
    methods = ['Bonferroni', 'Holm', 'SGoF', 'BH', 'BY', 'Q value']
    res = multitest(number_tuple, alpha=0.05)
    sig_indices = [res['Bonferroni'], res['Holm'], res['SGoF'], res['BH'], res['BY'], res['Q-value']]
    sigindex_plot(methods, sig_indices, title=None, save_plot=True,timestamp=ts) 
    # Carry out MultiDST for a list of p_values
    res = multitest(number_tuple, alpha=0.05, sigplot=False)
    if isinstance(res, dict):
        return {
            "Bonferroni": res["Bonferroni"],
            "Holm": res["Holm"],
            "SGoF": res["SGoF"],
            "BH": res["BH"],
            "BY": res["BY"],
            "Q-value": res["Q-value"],
            "sigindexplot":f"sigplot{ts}",
            "hist":f"hist{ts}"
        }
    else:
        return {"error": "Unexpected result format from multitest"}
#get results  