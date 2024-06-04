import matplotlib.pyplot as plt
import random
from multidst.utils.visualization import sigindex_plot
from multidst.functions import multitest

# Create p_values
p_values = [random.uniform(0,0.04) for i in range(1000)]

# Carrying out MultiDST for a list of p_values
res = multitest(p_values, alpha=0.05,sigplot=False)
sig_bonf_p, sig_holm_p, sig_sgof_p, sig_bh_p, sig_by_p, sig_q = res['Bonferroni'], res['Holm'], res['SGoF'], res['BH'], res['BY'], res['Q-value']

methods = ['Bonferroni', 'Holm', 'SGoF', 'BH', 'BY', 'Q value']
sig_indices = [sig_bonf_p, sig_holm_p, sig_sgof_p, sig_bh_p, sig_by_p, sig_q]
sig_plot = sigindex_plot(methods, sig_indices, title="Significant Index Plot")

# Save the current figure
plt.savefig('sig_index_plot.png')
plt.close()  # Close the plot to free memory
print('Plot saved as sig_index_plot.png')

# Call the function to create the plot
print(f'Plot saved as {sig_plot}')



def plot01():
    # Create a sample plot
    # Carrying out MultiDST for a list of p_values
    res = multitest(p_values, alpha=0.05,sigplot=False)
    sig_bonf_p, sig_holm_p, sig_sgof_p, sig_bh_p, sig_by_p, sig_q = res['Bonferroni'], res['Holm'], res['SGoF'], res['BH'], res['BY'], res['Q-value']

    methods = ['Bonferroni', 'Holm', 'SGoF', 'BH', 'BY', 'Q value']
    sig_indices = [sig_bonf_p, sig_holm_p, sig_sgof_p, sig_bh_p, sig_by_p, sig_q]
    sig_plot = sigindex_plot(methods, sig_indices, title="Significant Index Plot")

    # Save the plot as an image file
    plot_filename = 'plot01.png'
    plt.savefig(plot_filename)
    
    # Close the plot to free memory
    plt.close()
    
    return plot_filename

# Call the function to create the plot
plot_filename = plot01()
print(f'Plot saved as {plot_filename}')