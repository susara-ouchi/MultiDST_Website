from fastapi import FastAPI
from pydantic import BaseModel
from multidst.functions import multitest
from multidst.utils.visualization import multidst_hist , sigindex_plot

class P_Values(BaseModel):
    p_values: str

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


#send p values and methods
@app.post("/analyze")
async def analyze(request:P_Values):
    number_strings = request.p_values.split(',')
    number_list = [float(num) for num in number_strings]
    number_tuple = tuple(number_list)
    #Histogram
    g2_index = []
    multidst_hist(number_tuple, g2_index, title="Histogram of p-values",col1 = 'skyblue', col2 = 'purple')
    #sigplot
    methods = ['Bonferroni', 'Holm', 'SGoF', 'BH', 'BY', 'Q value']
    res = multitest(number_tuple, alpha=0.05, sigplot=True)
    sig_indices = [res['Bonferroni'], res['Holm'], res['SGoF'], res['BH'], res['BY'], res['Q-value']]
    sigindex_plot(methods, sig_indices, title=None, save_plot=True) 
    # Carry out MultiDST for a list of p_values
    res = multitest(number_tuple, alpha=0.05, sigplot=False)
    if isinstance(res, dict):
        return {
            "Bonferroni": res["Bonferroni"],
            "Holm": res["Holm"],
            "SGoF": res["SGoF"],
            "BH": res["BH"],
            "BY": res["BY"],
            "Q-value": res["Q-value"]
        }
    else:
        return {"error": "Unexpected result format from multitest"}
#get results  