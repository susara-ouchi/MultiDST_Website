from fastapi import FastAPI
from pydantic import BaseModel
from multidst.functions import multitest
import random

class P_Values(BaseModel):
    p_values: str

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


#send p values and methods
@app.post("/analyze")
async def analyze(request:P_Values):
    #number_tuple = [random.uniform(0,0.03) for i in range(1000)]
    #p_values = "0.0000085,0.000023,0.000152,0.0016024,0.0040207,0.02212,0.024306,0.032078,0.036851"
    number_strings = request.p_values.split(',')
    number_list = [float(num) for num in number_strings]
    number_tuple = tuple(number_list)
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