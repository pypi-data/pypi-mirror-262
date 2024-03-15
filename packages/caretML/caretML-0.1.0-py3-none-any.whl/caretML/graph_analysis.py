import numpy as np
import networkx as nx
import community
import random
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigsh
from sklearn.metrics.pairwise import cosine_similarity
from itertools import combinations

def pagerank(adjacency_matrix, damping_factor=0.85, max_iter=100, tol=1e-6):
    """
    Compute PageRank scores for nodes in a graph represented by its adjacency matrix.

    Parameters:
        adjacency_matrix (ndarray): Adjacency matrix of the graph.
        damping_factor (float, optional): Damping factor (usually denoted as alpha). Default is 0.85.
        max_iter (int, optional): Maximum number of iterations for power iteration method. Default is 100.
        tol (float, optional): Tolerance to determine convergence. Default is 1e-6.

    Returns:
        ndarray: PageRank scores for each node.
    """
    n = adjacency_matrix.shape[0]
    A = csr_matrix(adjacency_matrix, dtype=float)
    A = A / A.sum(axis=1)
    v = np.ones(n) / n
    for _ in range(max_iter):
        next_v = (1 - damping_factor) / n + damping_factor * A.T.dot(v)
        if np.linalg.norm(next_v - v) < tol:
            break
        v = next_v
    return v

def markov_chain_simulation(transition_matrix, initial_state, n_steps):
    """
    Simulate a Markov chain for a given number of steps.

    Parameters:
        transition_matrix (ndarray): Transition matrix of the Markov chain.
        initial_state (int): Initial state of the Markov chain.
        n_steps (int): Number of steps to simulate.

    Returns:
        list: List of states visited during the simulation.
    """
    states = [initial_state]
    current_state = initial_state
    for _ in range(n_steps):
        probabilities = transition_matrix[current_state]
        next_state = np.random.choice(len(probabilities), p=probabilities)
        states.append(next_state)
        current_state = next_state
    return states

def eigenvalue_analysis(matrix, k=5):
    """
    Perform eigenvalue analysis of a matrix.

    Parameters:
        matrix (ndarray or scipy.sparse matrix): Input matrix.
        k (int): Number of eigenvalues to compute.

    Returns:
        tuple: Tuple containing eigenvalues and eigenvectors.
    """
    if isinstance(matrix, np.ndarray):
        eigenvalues, eigenvectors = np.linalg.eig(matrix)
    else:
        eigenvalues, eigenvectors = eigsh(matrix, k=k)
    sorted_indices = np.argsort(eigenvalues.real)[::-1]
    eigenvalues = eigenvalues.real[sorted_indices]
    eigenvectors = eigenvectors[:, sorted_indices]
    return eigenvalues[:k], eigenvectors[:, :k]

def louvain_community_detection(adjacency_matrix):
    """
    Detect communities in a graph using the Louvain algorithm.

    Parameters:
        adjacency_matrix (ndarray): Adjacency matrix of the graph.

    Returns:
        dict: A dictionary mapping nodes to community IDs.
    """
    G = nx.from_numpy_matrix(adjacency_matrix)
    partition = community.best_partition(G)
    return partition

def node_similarity(graph, method='cosine'):
    """
    Compute pairwise node similarity measures.

    Parameters:
        graph (networkx.Graph): Input graph.
        method (str, optional): Similarity measure to use ('cosine', 'jaccard', etc.). Default is 'cosine'.

    Returns:
        ndarray: Pairwise similarity matrix.
    """
    if method == 'cosine':
        adjacency_matrix = csr_matrix(nx.adjacency_matrix(graph))
        similarity_matrix = cosine_similarity(adjacency_matrix)
    elif method == 'jaccard':
        similarity_matrix = np.zeros((len(graph), len(graph)))
        for i, j in combinations(range(len(graph)), 2):
            common_neighbors = len(list(nx.common_neighbors(graph, i, j)))
            union_neighbors = len(set(graph.neighbors(i)) | set(graph.neighbors(j)))
            similarity_matrix[i, j] = similarity_matrix[j, i] = common_neighbors / union_neighbors if union_neighbors != 0 else 0
    # Add more similarity measures as needed
    return similarity_matrix

def find_network_motifs(graph, motif_size=3):
    """
    Find network motifs in the graph.

    Parameters:
        graph (networkx.Graph): Input graph.
        motif_size (int, optional): Size of motifs to search for. Default is 3.

    Returns:
        list: List of network motifs found in the graph.
    """
    motifs = []
    for nodes in combinations(graph.nodes(), motif_size):
        subgraph = graph.subgraph(nodes)
        if nx.is_connected(subgraph) and len(subgraph) == motif_size:
            motifs.append(nodes)
    return motifs


def graph_partitioning(graph, method='spectral', k=2, **kwargs):
    """
    Partition the graph into disjoint subsets.

    Parameters:
        graph (networkx.Graph): Input graph.
        method (str, optional): Partitioning method ('spectral', 'multilevel', 'kernighan_lin', 'label_propagation', 'greedy_modularity', 'random', etc.). Default is 'spectral'.
        k (int, optional): Number of partitions. Default is 2.
        **kwargs: Additional arguments for specific partitioning methods.

    Returns:
        list of sets: Disjoint subsets of nodes representing the partitions.
    """
    if method == 'spectral':
        partitions = nx.algorithms.community.spectral_partitioning(graph, partitions=k, **kwargs)
    elif method == 'multilevel':
        partitions = nx.algorithms.community.modularity_max.greedy_modularity_communities(graph)
    elif method == 'kernighan_lin':
        partitions = nx.algorithms.community.kernighan_lin_bisection(graph)
    elif method == 'label_propagation':
        partitions = nx.algorithms.community.label_propagation.label_propagation_communities(graph)
    elif method == 'greedy_modularity':
        partitions = nx.algorithms.community.greedy_modularity_communities(graph)
    elif method == 'random':
        partitions = random_partitioning(graph, k)
    elif method == 'edge_betweenness':
        partitions = nx.algorithms.community.centrality.girvan_newman(graph)
    elif method == 'louvain':
        partitions = nx.algorithms.community.modularity_max.greedy_modularity_communities(graph)
    # Add more partitioning methods as needed
    return partitions

def random_partitioning(graph, k):
    """
    Randomly partition the graph into disjoint subsets.

    Parameters:
        graph (networkx.Graph): Input graph.
        k (int): Number of partitions.

    Returns:
        list of sets: Disjoint subsets of nodes representing the partitions.
    """
    nodes = list(graph.nodes())
    random.shuffle(nodes)
    partitions = [set(nodes[i::k]) for i in range(k)]
    return partitions


def graph_compression(graph, method='edge_betweenness', threshold=0.5, **kwargs):
    """
    Compress the graph while preserving its structural properties.

    Parameters:
        graph (networkx.Graph): Input graph.
        method (str, optional): Compression method ('edge_betweenness', 'degree', 'random', etc.). Default is 'edge_betweenness'.
        threshold (float, optional): Threshold value for compression. Default is 0.5.
        **kwargs: Additional keyword arguments specific to each compression method.

    Returns:
        networkx.Graph: Compressed graph.
    """
    if method == 'edge_betweenness':
        return compress_edges_by_betweenness(graph, threshold)
    elif method == 'degree':
        return compress_nodes_by_degree(graph, threshold)
    elif method == 'random':
        return random_graph_compression(graph, threshold)
    # Add more compression methods as needed
    else:
        raise ValueError("Unsupported compression method")

def compress_edges_by_betweenness(graph, threshold):
    """
    Compress graph edges based on betweenness centrality.

    Parameters:
        graph (networkx.Graph): Input graph.
        threshold (float): Threshold value for edge compression.

    Returns:
        networkx.Graph: Compressed graph.
    """
    betweenness = nx.edge_betweenness_centrality(graph)
    edges_to_compress = [(u, v) for (u, v), b in betweenness.items() if b <= threshold]
    return nx.contracted_nodes(graph, *zip(*edges_to_compress), self_loops=False)

def compress_nodes_by_degree(graph, threshold):
    """
    Compress graph nodes based on degree centrality.

    Parameters:
        graph (networkx.Graph): Input graph.
        threshold (float): Threshold value for node compression.

    Returns:
        networkx.Graph: Compressed graph.
    """
    degrees = dict(graph.degree())
    nodes_to_compress = [node for node, degree in degrees.items() if degree <= threshold]
    return nx.contracted_nodes(graph, *nodes_to_compress, self_loops=False)

def random_graph_compression(graph, threshold):
    """
    Randomly compress edges or nodes from the graph.

    Parameters:
        graph (networkx.Graph): Input graph.
        threshold (float): Probability threshold for compression.

    Returns:
        networkx.Graph: Compressed graph.
    """
    if threshold < 0 or threshold > 1:
        raise ValueError("Threshold must be in the range [0, 1]")
    
    compressed_graph = graph.copy()
    for edge in graph.edges():
        if random.random() <= threshold:
            compressed_graph.remove_edge(*edge)

    return compressed_graph

def link_prediction(graph, method='common_neighbors'):
    """
    Predict missing or future links in the graph.

    Parameters:
        graph (networkx.Graph): Input graph.
        method (str, optional): Link prediction method ('common_neighbors', 'resource_allocation', 'jaccard_coefficient', 'preferential_attachment', etc.). Default is 'common_neighbors'.

    Returns:
        list of tuples: Predicted links.
    """
    if method == 'common_neighbors':
        return predict_links_common_neighbors(graph)
    elif method == 'resource_allocation':
        return predict_links_resource_allocation(graph)
    elif method == 'jaccard_coefficient':
        return predict_links_jaccard_coefficient(graph)
    elif method == 'preferential_attachment':
        return predict_links_preferential_attachment(graph)
    # Add more link prediction methods as needed
    else:
        raise ValueError("Unsupported link prediction method")

def predict_links_common_neighbors(graph):
    """
    Predict missing links using common neighbors method.

    Parameters:
        graph (networkx.Graph): Input graph.

    Returns:
        list of tuples: Predicted links.
    """
    predicted_links = []
    for u, v in combinations(graph.nodes(), 2):
        if not graph.has_edge(u, v):
            common_neighbors = len(set(graph.neighbors(u)) & set(graph.neighbors(v)))
            if common_neighbors > 0:
                predicted_links.append((u, v))
    return predicted_links

def predict_links_resource_allocation(graph):
    """
    Predict missing links using resource allocation method.

    Parameters:
        graph (networkx.Graph): Input graph.

    Returns:
        list of tuples: Predicted links.
    """
    predicted_links = []
    for u, v in combinations(graph.nodes(), 2):
        if not graph.has_edge(u, v):
            ra_score = sum(1 / graph.degree(w) for w in set(graph.neighbors(u)) & set(graph.neighbors(v)))
            if ra_score > 0:
                predicted_links.append((u, v))
    return predicted_links

def predict_links_jaccard_coefficient(graph):
    """
    Predict missing links using Jaccard coefficient method.

    Parameters:
        graph (networkx.Graph): Input graph.

    Returns:
        list of tuples: Predicted links.
    """
    predicted_links = []
    for u, v in combinations(graph.nodes(), 2):
        if not graph.has_edge(u, v):
            jac_coef = len(set(graph.neighbors(u)) & set(graph.neighbors(v))) / len(set(graph.neighbors(u)) | set(graph.neighbors(v)))
            if jac_coef > 0:
                predicted_links.append((u, v))
    return predicted_links

def predict_links_preferential_attachment(graph):
    """
    Predict missing links using preferential attachment method.

    Parameters:
        graph (networkx.Graph): Input graph.

    Returns:
        list of tuples: Predicted links.
    """
    predicted_links = []
    for u, v in combinations(graph.nodes(), 2):
        if not graph.has_edge(u, v):
            pref_attach_score = graph.degree(u) * graph.degree(v)
            if pref_attach_score > 0:
                predicted_links.append((u, v))
    return predicted_links

def graph_sampling(graph, method='random_node', k=100):
    """
    Sample a subgraph from the input graph.

    Parameters:
        graph (networkx.Graph): Input graph.
        method (str, optional): Sampling method ('random_node', 'random_edge', 'random_walk', 'ego_network', etc.). Default is 'random_node'.
        k (int, optional): Number of nodes/edges to sample. Default is 100.

    Returns:
        networkx.Graph: Sampled subgraph.
    """
    if method == 'random_node':
        sampled_nodes = np.random.choice(graph.nodes(), size=min(k, len(graph)), replace=False)
        sampled_subgraph = graph.subgraph(sampled_nodes)
    elif method == 'random_edge':
        sampled_edges = np.random.choice(list(graph.edges()), size=min(k, len(graph.edges())), replace=False)
        sampled_nodes = set().union(*sampled_edges)
        sampled_subgraph = graph.subgraph(sampled_nodes)
    elif method == 'random_walk':
        start_node = np.random.choice(graph.nodes())
        sampled_nodes = [start_node]
        current_node = start_node
        while len(sampled_nodes) < min(k, len(graph)):
            neighbors = list(graph.neighbors(current_node))
            if neighbors:
                next_node = np.random.choice(neighbors)
                sampled_nodes.append(next_node)
                current_node = next_node
            else:
                break
        sampled_subgraph = graph.subgraph(sampled_nodes)
    elif method == 'ego_network':
        ego_nodes = np.random.choice(graph.nodes(), size=min(k, len(graph)), replace=False)
        sampled_subgraph = nx.ego_graph(graph, np.random.choice(ego_nodes))
    else:
        raise ValueError("Unsupported sampling method")
        
    return sampled_subgraph

def graph_alignment(graph1, graph2, method='greedy'):
    """
    Align two graphs to find corresponding nodes.

    Parameters:
        graph1 (networkx.Graph): First input graph.
        graph2 (networkx.Graph): Second input graph.
        method (str, optional): Graph alignment method ('greedy', 'spectral', etc.). Default is 'greedy'.

    Returns:
        dict: Mapping between nodes of the two graphs.
    """
    if method == 'greedy':
        mapping = nx.algorithms.isomorphism.GraphMatcher(graph1, graph2).mapping
    elif method == 'spectral':
        # Spectral alignment using Laplacian matrices
        # Compute Laplacian matrices
        L1 = nx.linalg.laplacianmatrix.laplacian_matrix(graph1).todense()
        L2 = nx.linalg.laplacianmatrix.laplacian_matrix(graph2).todense()
        # Compute eigenvectors
        _, U1 = np.linalg.eigh(L1)
        _, U2 = np.linalg.eigh(L2)
        # Align based on spectral embeddings
        mapping = {}
        for u, v in zip(graph1.nodes(), graph2.nodes()):
            sim_matrix = np.dot(U1.T, U2)
            best_match = np.argmax(sim_matrix[u])
            mapping[u] = graph2.nodes()[best_match]
    else:
        raise ValueError("Unsupported graph alignment method")
        
    return mapping

def community_evolution_analysis(graph_sequence):
    """
    Analyze the evolution of communities in a dynamic graph.

    Parameters:
        graph_sequence (list of networkx.Graph): Sequence of graphs representing the dynamic graph.

    Returns:
        dict: Evolutionary information about communities.
    """
    # Implement community evolution analysis algorithm
    # Example: Track community memberships over time
    community_memberships = {}
    for i, graph in enumerate(graph_sequence):
        for node, community in nx.algorithms.community.label_propagation.label_propagation_communities(graph):
            if community not in community_memberships:
                community_memberships[community] = []
            community_memberships[community].append((i, node))
    return community_memberships

def graph_anomaly_detection(graph, method='lof'):
    """
    Detect anomalies in the graph.

    Parameters:
        graph (networkx.Graph): Input graph.
        method (str, optional): Anomaly detection method ('lof', 'isolation_forest', 'degree_centrality', 'katz_centrality', 'betweenness_centrality', 'eigenvector_centrality', etc.). Default is 'lof'.

    Returns:
        list: Detected anomalies.
    """
    if method == 'lof':
        return [node for node, score in nx.algorithms.centrality.local_outlier_factor(graph).items() if score > 1]
    elif method == 'isolation_forest':
        return [node for node, score in nx.algorithms.centrality.isolation_forest(graph).items() if score < 0]
    elif method == 'degree_centrality':
        threshold = 2 * np.mean(list(nx.algorithms.centrality.degree_centrality(graph).values()))
        return [node for node, degree in nx.algorithms.centrality.degree_centrality(graph).items() if degree > threshold]
    elif method == 'katz_centrality':
        threshold = 2 * np.mean(list(nx.algorithms.centrality.katz_centrality(graph).values()))
        return [node for node, katz_centrality in nx.algorithms.centrality.katz_centrality(graph).items() if katz_centrality > threshold]
    elif method == 'betweenness_centrality':
        threshold = 2 * np.mean(list(nx.algorithms.centrality.betweenness_centrality(graph).values()))
        return [node for node, betweenness_centrality in nx.algorithms.centrality.betweenness_centrality(graph).items() if betweenness_centrality > threshold]
    elif method == 'eigenvector_centrality':
        threshold = 2 * np.mean(list(nx.algorithms.centrality.eigenvector_centrality(graph).values()))
        return [node for node, eigenvector_centrality in nx.algorithms.centrality.eigenvector_centrality(graph).items() if eigenvector_centrality > threshold]
    # Add more anomaly detection methods as needed
    return []


def graph_visualization(graph, method='networkx', **kwargs):
    """
    Visualize the graph.

    Parameters:
        graph (networkx.Graph): Input graph.
        method (str, optional): Visualization method ('networkx', 'matplotlib', 'plotly', 'd3', etc.). Default is 'networkx'.
        **kwargs: Additional keyword arguments specific to each visualization method.
    """
    if method == 'networkx':
        nx.draw(graph, **kwargs)
        plt.show()
    elif method == 'matplotlib':
        pos = nx.spring_layout(graph)  # You can customize layout algorithms
        nx.draw(graph, pos, **kwargs)
        plt.show()
    elif method == 'plotly':
        pos = nx.spring_layout(graph, dim=2)  # You can customize layout algorithms
        edge_trace = go.Scatter(
            x=[],
            y=[],
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        for edge in graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace['x'] += [x0, x1, None]
            edge_trace['y'] += [y0, y1, None]

        node_trace = go.Scatter(
            x=[],
            y=[],
            text=[],
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                colorscale='YlGnBu',
                reversescale=True,
                color=[],
                size=10,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                ),
                line_width=2))

        for node in graph.nodes():
            x, y = pos[node]
            node_trace['x'].append(x)
            node_trace['y'].append(y)

        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            title='Graph Visualization',
                            titlefont_size=16,
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            annotations=[dict(
                                text="",
                                showarrow=False,
                                xref="paper", yref="paper",
                                x=0.005, y=-0.002)],
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                        )
        fig.show()
    elif method == 'graphviz':
        graphviz_graph = nx.drawing.nx_pydot.to_pydot(graph)
        graphviz_graph.set(**kwargs)
        graphviz_graph.render('graph', format='png', cleanup=True)
    elif method == 'd3':
        # Convert the networkx graph to JSON format
        json_data = nx.readwrite.json_graph.node_link_data(graph)
        with open('graph.json', 'w') as f:
            json.dump(json_data, f)

        # Open an HTML file with D3.js visualization
        html_content = """
        <html>
        <head>
            <title>Graph Visualization with D3.js</title>
            <script src="https://d3js.org/d3.v6.min.js"></script>
        </head>
        <body>
            <svg width="800" height="600"></svg>
            <script>
                d3.json('graph.json').then(function(graph) {
                    var svg = d3.select('svg');

                    var link = svg.append('g')
                        .selectAll('line')
                        .data(graph.links)
                        .enter()
                        .append('line')
                        .style('stroke', '#999')
                        .style('stroke-opacity', 0.6)
                        .style('stroke-width', function(d) { return Math.sqrt(d.value); });

                    var node = svg.append('g')
                        .selectAll('circle')
                        .data(graph.nodes)
                        .enter()
                        .append('circle')
                        .attr('r', 5)
                        .style('fill', '#1f77b4')
                        .call(d3.drag()
                            .on('start', dragstarted)
                            .on('drag', dragged)
                            .on('end', dragended));

                    var simulation = d3.forceSimulation()
                        .force('link', d3.forceLink().id(function(d) { return d.id; }))
                        .force('charge', d3.forceManyBody().strength(-100))
                        .force('center', d3.forceCenter(400, 300));

                    simulation
                        .nodes(graph.nodes)
                        .on('tick', ticked);

                    simulation.force('link')
                        .links(graph.links);

                    function ticked() {
                        link
                            .attr('x1', function(d) { return d.source.x; })
                            .attr('y1', function(d) { return d.source.y; })
                            .attr('x2', function(d) { return d.target.x; })
                            .attr('y2', function(d) { return d.target.y; });

                        node
                            .attr('cx', function(d) { return d.x; })
                            .attr('cy', function(d) { return d.y; });
                    }

                    function dragstarted(event, d) {
                        if (!event.active) simulation.alphaTarget(0.3).restart();
                        d.fx = d.x;
                        d.fy = d.y;
                    }

                    function dragged(event, d) {
                        d.fx = event.x;
                        d.fy = event.y;
                    }

                    function dragended(event, d) {
                        if (!event.active) simulation.alphaTarget(0);
                        d.fx = null;
                        d.fy = null;
                    }
                });
            </script>
        </body>
        </html>
        """

        with open('graph_d3.html', 'w') as f:
            f.write(html_content)

        # Open the HTML file in a web browser
        webbrowser.open_new_tab('graph_d3.html')
    # Add more visualization methods as needed