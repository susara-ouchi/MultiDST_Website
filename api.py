from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import matplotlib.pyplot as plt
import random
from multidst.utils.visualization import sigindex_plot
from multidst.functions import multitest
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

def generate_plot(p_values, methods):
    # Carry out MultiDST for a list of p_values
    res = multitest(p_values, alpha=0.05, sigplot=False)
    results = {method: res[method] for method in methods}
    
    sig_indices = [results[method] for method in methods]
    sig_plot = sigindex_plot(methods, sig_indices, title="Significant Index Plot")

    # Save the plot as an image file
    plot_filename = 'app/static/sig_index_plot.png'
    plt.savefig(plot_filename)
    plt.close()
    
    return plot_filename, results

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze", response_class=HTMLResponse)
async def analyze(request: Request, p_values: str = Form(...), methods: str = Form(...)):
    p_values = list(map(float, p_values.split(',')))
    methods = methods.split(',')
    plot_filename, results = generate_plot(p_values, methods)
    return templates.TemplateResponse("index.html", {"request": request, "plot_url": plot_filename, "significant_values": results})