#! /usr/bin/env python3
# coding: utf-8

""" This module gathers some functions to personalize matplotlib plot. 
"""
import os
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
    x_min, x_max = plot.get_xlim()
    y_min, y_max = plot.get_ylim()
    x_label = plot.get_xlabel()
    y_label = plot.get_ylabel()
    plot.set_xlabel(x_label, weight="bold")  
    plot.set_ylabel(y_label, weight="bold")  
    # Add a title and a subtitle
    title_x = x_min - (x_max-x_min)*.05
    title_y = y_max + (y_max-y_min)*.1
    subtitle_y = y_max + (y_max-y_min)*.05
    plot.text(x=title_x, y=title_y, s=title, fontsize=14,
                weight="bold")
    plot.text(x=title_x, y=subtitle_y, s=subtitle)
    # Add a grid
    plt.grid(linestyle='dashed')
    # Add a legend
    if legend:
        plt.legend(loc='best', facecolor='w', edgecolor='b')
    # Save the plot
    folder_path=os.path.join("charts")
    if not os.path.isdir(folder_path):
        os.makedirs(folder_path)
    plt.savefig("charts/{}.png".format(file), bbox_inches = "tight")
    plt.show()

def my_box_plot(data, num_features, by, file="boxplot"):
    """Get a nice box plot easy to read, giving both count of values and standard deviation for each category. 
    -----------
    Parameters :
    data: DataFrame
        the pandas object holding the data
    num_features: list
        list of all numerical feature to be used
    by: string
        name of the categorical feature
    file : String
        name of the png file
    -----------
    Return :
    axes : Matplotlib axis object
    """
    # Create a copy of the dataset including the selected features only
    features = [by] + num_features
    df = data.loc[:, features]
    classes = sorted(df.loc[:, by].unique())
    # figure initialization
    n = len(num_features)
    fig = plt.figure(figsize=(6, n*4))
    # personnalization of boxplot parameters
    medianprops = {'color':'black'}
    meanprops = {'marker':'o', 'markeredgecolor':'black', 'markeredgewidth':1, 'markerfacecolor':'peachpuff'}
    flierprops = {'marker':'+', 'markeredgecolor':'black', 'markeredgewidth':1}
    # boxplot Creation
    for i, att in enumerate(num_features):
        ax = fig.add_subplot(n, 1, i+1)
        values = [df[df[by]==c][att].dropna().values for c in classes]
        ax.boxplot(values, labels=classes, vert=False,
                   showfliers=True, showmeans=True, patch_artist=True,
                   medianprops=medianprops, meanprops=meanprops, flierprops=flierprops)
        ax.set_title("{} vs. {}".format(att, by))
        ax.grid(linestyle='dashed')
        # get the count values, std and first quartile
        f = lambda x: x.quantile(.25)
        props = df.groupby(by)[att].agg(["count", "std", f])
        # display count values and standard deviation
        for j in range(len(classes)):
            ax.text(props.iloc[j, 2], j+1.25+len(classes)/40,
                    '(n={}, std={})'.format(props.iloc[j, 0], round(props.iloc[j, 1], 2)),
                    verticalalignment='center', fontsize=11)
    #save the plot
    folder_path=os.path.join("charts")
    if not os.path.isdir(folder_path):
        os.makedirs(folder_path)
    plt.savefig("charts/{}.png".format(file), bbox_inches = "tight")
    plt.tight_layout()
    plt.show()
