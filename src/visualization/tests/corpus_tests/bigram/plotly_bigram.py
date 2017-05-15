from src.graph.lexical_graph.wordnet.other_wordnet_graph import wnGraph
from src.graph.ngram_graph.bigram_graph import WordGraph
import networkx as nx
import matplotlib.pyplot as plt
from plotly.graph_objs import *
import plotly.plotly as py
import plotly.tools as tls

py.sign_in(username='jamesoneill', api_key='9rlLUCVyiSpjWLlR86fM')
tls.set_credentials_file(username='jamesoneill', api_key='9rlLUCVyiSpjWLlR86fM')

docpath = "C:/Users/1/James/grctc/GRCTC_Project/Classification/Data/docs/"
bigraph = WordGraph(docpath)
ngram_g = bigraph.textrank_corpus_graph(save_image=True)

pos=nx.spring_layout(ngram_g)
nx.set_node_attributes(ngram_g, 'pos', pos)

edge_trace = Scatter(
    x=[],
    y=[],
    line=Line(width=0.5,color='#888'),
    hoverinfo='none',
    mode='lines')

for edge in ngram_g.edges():
    print (ngram_g.node[edge[0]]['pos'])
    print (ngram_g.node[edge[1]]['pos'])
    x0, y0 = ngram_g.node[edge[0]]['pos']
    x1, y1 = ngram_g.node[edge[1]]['pos']
    edge_trace['x'] += [x0, x1, None]
    edge_trace['y'] += [y0, y1, None]

# Visualizing textrank ngram graph with plotly
node_trace = Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    hoverinfo='text',
    marker=Marker(
        showscale=True,
        # colorscale options
        # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
        # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
        colorscale='YIGnBu',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=2)))

for node in ngram_g.nodes():
    x, y = ngram_g.node[node]['pos']
    node_trace['x'].append(x)
    node_trace['y'].append(y)

for (n,a) in enumerate(ngram_g.adjacency_list()):
    node_trace['marker']['color'].append(len(a))
    node_info = '# of connections: '+str(len(a))
    node_trace['text'].append(node_info)

# Create Network Graph
fig = Figure(data=Data([edge_trace, node_trace]),
             layout=Layout(
                title='<br>Bigram Corpus Graph',
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Python code: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))

py.iplot(fig, filename='networkx')
