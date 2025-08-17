"""
Independent cascade model simulations for network analysis.

This module provides functions for simulating information diffusion
and influence propagation in networks using the Independent Cascade model.
"""

import random
from typing import Set, List, Tuple, Any


def independent_cascade(
    G, 
    seeds: Set[Any], 
    max_steps: int = 99999
) -> Tuple[Set[Any], List[Set[Any]]]:
    """
    Run one Independent Cascade (IC) simulation and return the set of activated nodes 
    and per-step activations.

    The Independent Cascade model simulates how information or influence spreads through
    a network. Each activated node has one chance to activate its inactive neighbors
    based on edge probabilities. The process continues until no new activations occur
    or the maximum number of steps is reached.

    Parameters:
        G: NetworkX directed graph with edge attribute 'prob' containing activation probabilities
        seeds (Set[Any]): Set of seed nodes to start the cascade from
        max_steps (int, optional): Maximum number of simulation steps. Defaults to 99999.

    Returns:
        Tuple[Set[Any], List[Set[Any]]]: A tuple containing:
            - Set of all activated nodes at the end of simulation
            - List of sets, where each set contains the cumulative activated nodes at each step

    Raises:
        ValueError: If seeds set is empty or contains invalid nodes
        KeyError: If graph edges don't have 'prob' attribute

    Example:
        >>> import networkx as nx
        >>> import spellbook
        >>> 
        >>> # Build a simple directed triangle graph
        >>> G = nx.DiGraph()
        >>> edges = [("A", "B", 0.4), ("B", "C", 0.5), ("C", "A", 0.3)]
        >>> for u, v, p in edges:
        ...     G.add_edge(u, v, prob=p)
        >>> 
        >>> # Run simulation starting from node A
        >>> seeds = {"A"}
        >>> active_nodes, step_activations = spellbook.network.independent_cascade(G, seeds)
        >>> print(f"Final activated nodes: {active_nodes}")
        >>> print(f"Activations per step: {step_activations}")

    Use Case:
        - Social network influence analysis
        - Information diffusion modeling
        - Viral marketing campaign simulation
        - Disease spread modeling in contact networks
    """
    # Validate inputs
    if not seeds:
        raise ValueError("Seeds set cannot be empty")
    
    if not all(node in G.nodes() for node in seeds):
        raise ValueError("All seed nodes must exist in the graph")
    
    # Initialize simulation state
    active = set(seeds)
    newly_active = set(seeds)
    steps = [set(seeds)]  # Record per-step cumulative actives
    
    # Run simulation for max_steps or until no new activations
    for _ in range(max_steps):
        attempts_next = set()
        
        # Each newly active node attempts to activate its neighbors
        for u in newly_active:
            for v in G.successors(u):
                if v not in active:
                    try:
                        p = G[u][v]["prob"]
                    except KeyError:
                        raise KeyError(f"Edge ({u}, {v}) missing 'prob' attribute")
                    
                    # Attempt activation based on probability
                    if random.random() < p:
                        attempts_next.add(v)
        
        # If no new activations, stop simulation
        if not attempts_next:
            break
            
        # Update simulation state
        newly_active = attempts_next
        active |= newly_active
        steps.append(set(active))
    
    return active, steps


def celf(G, k: int) -> List[Any]:
    """
    Cost-Effective Lazy Forward (CELF) algorithm for influence maximization.
    
    CELF is an efficient algorithm for finding the k most influential nodes in a network
    for influence maximization under the Independent Cascade model. It uses the lazy
    evaluation technique to reduce the number of spread computations needed.
    
    Parameters:
        G: NetworkX directed graph with edge attribute 'prob' containing activation probabilities
        k (int): Number of seed nodes to select
        
    Returns:
        List[Any]: List of k seed nodes that maximize influence spread
        
    Raises:
        ValueError: If k is less than 1 or greater than number of nodes
        KeyError: If graph edges don't have 'prob' attribute
        
    Example:
        >>> import networkx as nx
        >>> import spellbook
        >>> 
        >>> # Build a simple directed graph
        >>> G = nx.DiGraph()
        >>> edges = [("A", "B", 0.4), ("B", "C", 0.5), ("C", "A", 0.3), ("A", "D", 0.6)]
        >>> for u, v, p in edges:
        ...     G.add_edge(u, v, prob=p)
        >>> 
        >>> # Find top 2 influential nodes
        >>> seeds = spellbook.network.celf(G, k=2)
        >>> print(f"Selected seed nodes: {seeds}")
        
    Use Case:
        - Social network influence maximization
        - Viral marketing campaign design
        - Information diffusion optimization
        - Network immunization strategies
        
    Reference:
        Leskovec, J., Krause, A., Guestrin, C., Faloutsos, C., VanBriesen, J., & Glance, N. (2007).
        Cost-effective outbreak detection in networks. In Proceedings of the 13th ACM SIGKDD
        international conference on Knowledge discovery and data mining (pp. 420-429).
    """
    import heapq
    
    # Validate input
    if k < 1:
        raise ValueError("k must be at least 1")
    
    if k > len(G.nodes()):
        raise ValueError(f"k ({k}) cannot be greater than number of nodes ({len(G.nodes())})")
    
    # Initial marginal gains
    pq = []
    for node in G.nodes():
        active_nodes, _ = independent_cascade(G, {node})
        spread = len(active_nodes)
        heapq.heappush(pq, (-spread, node, 0))  # max-heap, iteration=0
    
    seeds = []
    iter_num = 1
    
    while len(seeds) < k:
        gain, node, last_iter = heapq.heappop(pq)
        
        if last_iter == iter_num - 1:
            # This is the current best node, add it to seeds
            seeds.append(node)
        else:
            # Recompute marginal gain
            active_with_seeds, _ = independent_cascade(G, set(seeds + [node]))
            active_current, _ = independent_cascade(G, set(seeds))
            spread_with_seeds = len(active_with_seeds)
            spread_current = len(active_current)
            marginal_gain = spread_with_seeds - spread_current
            heapq.heappush(pq, (-marginal_gain, node, iter_num - 1))
        
        iter_num += 1
    
    return seeds
