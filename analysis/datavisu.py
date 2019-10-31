#! /usr/bin/env python3
# coding: utf-8

""" This module gathers some functions to personalize matplotlib plot. 
"""

import numpy as np
import matplotlib.pyplot as plt

def nice_plot(plot, legend=False, title="", subtitle="", file=""):
    """get a plot in FiveThirtyEight format, making it easy to read. 
    -----------
    Parameters :
    plot: matplotlib.axes.Axes
        plot to be personnalized
    title: string
        title of chart
    subtitle: string
        subtitle of chart
    file : String
        name of the png file
    -----------
    Return :
    axes : Matplotlib axis object
    """
    # Set axis
    plot.tick_params(axis="both", which="both", labelsize=10, colors="#333333")
    x_min, x_max = plot.get_xlim()
    y_min, y_max = plot.get_ylim()
    x_label = plot.get_xlabel()
    y_label = plot.get_ylabel()
    plot.set_xlabel(x_label, color="#333333", weight="bold", fontsize=10)  
    plot.set_ylabel(y_label, color="#333333", weight="bold", fontsize=10)  
    # Add a title and a subtitle
    title_x = x_min - (x_max-x_min)*.05
    title_y = y_max + (y_max-y_min)*.13
    subtitle_y = y_max + (y_max-y_min)*.07
    plot.text(x=title_x, y=title_y, s=title, fontsize=15,
                weight="bold", color="#333333")
    plot.text(x=title_x, y=subtitle_y, s=subtitle, fontsize=10,
                color="#333333")    
    # Add a legend
    if legend:
        plt.legend(loc='best', fontsize=10, facecolor='w', edgecolor='#333333')
    # Save the plot
    plt.savefig(file + ".png", bbox_inches = "tight")
    plt.show()



