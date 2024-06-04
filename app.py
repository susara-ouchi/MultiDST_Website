from flask import Flask, render_template
from io import BytesIO
import matplotlib.pyplot as plt

app = Flask(__name__)

# Define the desired position (pixels) for the plot
plot_top = 100
plot_left = 50

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot')
def plot():
    # Generate some sample data
    x = [1, 2, 3, 4, 5]
    y = [4, 6, 5, 8, 2]

    # Create a Matplotlib plot
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title('Sample Plot')

    # Save plot as PNG image in memory
    img_io = BytesIO()
    fig.savefig(img_io, format='png')
    img_io.seek(0)
    plot_data = img_io.getvalue().decode('base64')  # Encode for HTML

    return render_template('plot.html', plot_data=plot_data, plot_top=plot_top, plot_left=plot_left)

if __name__ == '__main__':
    app.run(debug=True)
