import collections
import numpy as np
import pandas as pd
import scipy.io as sci
from itertools import islice

import seaborn as sns

import matplotlib.colors
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

import plotly
import chart_studio.plotly as py
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class CellLayersConfig(object):
    
    def __init__(self, sankey_dict, node_color='#F7ED32'):
        self.sankey_dict = sankey_dict
        self.starter_gene = [x for x in list(self.sankey_dict['data']) if 'hex' in x.split('_')][0].split('_')[0]
        self.node_color = node_color
    
    def _create_sankey_obj(self):
        return go.Figure(data=[dict(type='sankey', orientation='h', 
                node = dict(pad = 10, thickness=10,
                            label=self.sankey_dict['node_data']['node_labels'],
                            customdata = self.sankey_dict['node_data']['new_label'],
                            hovertemplate= '%{customdata}',
                            color = self.sankey_dict['node_data']['silhoutte_hex']),
                
                link = dict(source = self.sankey_dict['data']['source'],
                            target = self.sankey_dict['data']['target'],
                            color =  self.sankey_dict['data'][self.starter_gene+'_hex'],
                            value = self.sankey_dict['data']['value']))])
    
    def _create_gene_exp_buttons(self, fig):
        gene_buttons = []
        colorbar = []
        genes = [x.split('_')[0] for x in list(self.sankey_dict['data']) if 'hex' in x.split('_')]

        fig.add_trace(go.Scatter(x=[None],
                                 y=[None],
                                 mode='markers',
                                 visible=True,
                                 marker={'colorscale':self.sankey_dict['node_data']['silhoutte_hex'].tolist()}))
        for i in range(len(genes)):
            if i == 0:
                self._create_colorbar(fig, genes[i], True)
            else:
                self._create_colorbar(fig, genes[i], False)
            gene_bools = np.full(len(genes), False).tolist()
            # I think there is a problem if there is less than 2 genes
            gene_bools[i] = True
            gene_bools[0:0] = [True]
            gene_bools.insert(1, True)
            gene_dict = dict(label=genes[i], method='update', args=[{"visible":gene_bools,
                                                            
                                                                     'link' : dict(source = self.sankey_dict['data']['source'],
                                                                                   target = self.sankey_dict['data']['target'],
                                                                                   color = self.sankey_dict['data'][genes[i]+'_hex'], # Gene expression or largest dag trace parameter
                                                                                   value = self.sankey_dict['data']['value'])}])
            gene_buttons.append(gene_dict)
            
        return gene_buttons
    
    def _create_colorbar(self, fig, gene, visible=False):
        fig.add_trace(go.Scatter(x=[None],
                                 y=[None],
                                 mode='markers',
                                 visible=visible,
                                 marker=self.sankey_dict['exp_colorbar'][gene]))
    
    def _create_silhouette_colorbar(self, fig):

        fig.add_trace(go.Scatter(x=[None],
                   y=[None],
                   mode='markers',
                   visible=True,
                   marker={'colorscale':[mcolors.to_hex(self.sankey_dict['silhouette_mapper'].to_rgba(x)) 
                                         for x in self.sankey_dict['silhouette_list']],
                           'showscale':True, 'cmin':-1, 'cmax':1, 'colorbar': {'x':1.1}}))
    
    def _add_functionality(self, fig):
        
        gene_buttons = self._create_gene_exp_buttons(fig)
        fig.update_layout(
            updatemenus=[
                dict(y=0.9, buttons=list(gene_buttons)),
                
#                 dict(y=0.25, buttons=[dict(label='Silhouette Score', 
#                                            method='update', args=[{"visible":True}])]),
                
                dict(x=0, y=1.25,
                             buttons=[dict(label='Snap',method='restyle', args=['arrangement', 'snap']),
                                      dict(label='Perpendicular', method='restyle',args=['arrangement', 'perpendicular']),
                                      dict(label='Freeform', method='restyle',args=['arrangement', 'freeform']),
                                      dict(label='Fixed', method='restyle',args=['arrangement', 'fixed'])]),    
                
                dict(x=0.2, y=1.25,
                      buttons=[dict(label='Light', method='relayout', args=['paper_bgcolor', 'white']),
                               dict(label='Dark', method='relayout', args=['paper_bgcolor', 'black'])]),
                
                dict(x=0.4, y=1.25,
                     buttons=[dict(label='Thin', method='restyle',args=['node.thickness', 8]),
                              dict(label='Thick',method='restyle',args=['node.thickness', 15])]),
                
                dict(x=0.6, y=1.25,
                     buttons=[dict(label='Small gap',method='restyle',args=['node.pad', 15]),
                              dict(label='Large gap',method='restyle',args=['node.pad', 20])]),
                
                dict(x=0.8, y=1.25,
                     buttons=[dict(label='Horizontal', method='restyle', args=['orientation', 'h']),
                              dict(label='Vertical',method='restyle',args=['orientation', 'v'])])])

        
    def run(self):
        fig = self._create_sankey_obj()
        self._add_functionality(fig)
        self._create_silhouette_colorbar(fig)
        fig.update_xaxes(showticklabels=False) # hide all the xticks
        fig.update_yaxes(showticklabels=False) # hide all the xticks
        fig['layout']['showlegend'] = False
        fig['layout']['xaxis']['showgrid'] = False
        fig['layout']['yaxis']['showgrid'] = False
        fig.update_layout(xaxis_zeroline=False, yaxis_zeroline=False)
        fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)'
        })
        return fig