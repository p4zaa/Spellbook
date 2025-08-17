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
    max_steps: int = 99999,
    prob_attr: str = 'weight',
    default_prob: float = 0.1
) -> Tuple[Set[Any], List[Set[Any]]]:
    """
    Run one Independent Cascade (IC) simulation and return the set of activated nodes 
    and per-step activations.

    The Independent Cascade model simulates how information or influence spreads through
    a network. Each activated node has one chance to activate its inactive neighbors
    based on edge probabilities. The process continues until no new activations occur
    or the maximum number of steps is reached.

    Parameters:
        G: NetworkX directed graph with edge attributes containing activation probabilities
        seeds (Set[Any]): Set of seed nodes to start the cascade from
        max_steps (int, optional): Maximum number of simulation steps. Defaults to 99999.
        prob_attr (str, optional): Name of edge attribute containing activation probabilities. Defaults to 'weight'.
        default_prob (float, optional): Default probability to use for edges without probability attribute. Defaults to 0.1.

    Returns:
        Tuple[Set[Any], List[Set[Any]]]: A tuple containing:
            - Set of all activated nodes at the end of simulation
            - List of sets, where each set contains the cumulative activated nodes at each step

    Raises:
        ValueError: If seeds set is empty or contains invalid nodes, or if default_prob is not between 0 and 1

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
        >>> 
        >>> # Use custom probability attribute name
        >>> G2 = nx.DiGraph()
        >>> for u, v, p in edges:
        ...     G2.add_edge(u, v, weight=p)
        >>> active_nodes, step_activations = spellbook.network.independent_cascade(G2, seeds, prob_attr='weight')
        >>> 
        >>> # Use default probability for all edges
        >>> G3 = nx.DiGraph()
        >>> for u, v in [("A", "B"), ("B", "C"), ("C", "A")]:
        ...     G3.add_edge(u, v)
        >>> active_nodes, step_activations = spellbook.network.independent_cascade(G3, seeds, default_prob=0.5)

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
    
    if not 0 <= default_prob <= 1:
        raise ValueError("default_prob must be between 0 and 1")
    
    # Initialize simulation state
    active = set(seeds)
    newly_active = set(seeds)
    steps = [set(seeds)]  # Record per-step cumulative actives
    
    # Run simulation for max_steps or until no new activations
    for _ in range(max_steps):
        attempts_next = set()
        
        # Each newly active node attempts to activate its neighbors
        for u in newly_active:
            if G.is_directed():
                neighbors = G.successors(u)
            else:
                neighbors = G.neighbors(u)
            for v in neighbors:
                if v not in active:
                    # Get probability from edge attribute or use default
                    try:
                        p = G[u][v][prob_attr]
                    except KeyError:
                        p = default_prob
                    
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

def estimate_spread(G, seeds, mc=100, **kwargs):
    """Estimate expected spread with Monte Carlo."""
    return sum(len(independent_cascade(G, set(seeds), **kwargs)[0]) for _ in range(mc)) / mc

def celf(G, k, prob_attr='weight', default_prob=0.1, mc=100, **kwargs):
    """
    Cost-Effective Lazy Forward (CELF) algorithm for influence maximization.
    
    CELF is an efficient greedy algorithm to select the k most influential nodes in a network
    under the Independent Cascade (IC) model. It improves computational efficiency compared 
    to naive greedy by using lazy evaluations of marginal gains.

    Parameters:
        G: NetworkX directed graph
            Graph where edges represent influence links and may contain activation probabilities
            as attributes (e.g., 'weight').
        k (int):
            Number of seed nodes to select.
        prob_attr (str, optional):
            Name of the edge attribute storing activation probabilities. Defaults to 'weight'.
        default_prob (float, optional):
            Default probability used for edges without the probability attribute. Must be between 0 and 1.
            Defaults to 0.1.
        mc (int, optional):
            Number of Monte Carlo simulations per marginal gain estimation. Higher values give more
            accurate expected spread estimates but increase runtime. Defaults to 100.
        **kwargs:
            Additional arguments passed to `independent_cascade` (e.g., `max_steps`).

    Returns:
        List[Any]:
            List of k seed nodes that maximize expected influence spread.

    Raises:
        ValueError: If `k < 1`, if `k > number of nodes in G`, or if `default_prob` is not between 0 and 1.

    Example:
        >>> import networkx as nx
        >>> # Build a directed graph with probabilities
        >>> G = nx.DiGraph()
        >>> edges = [("A", "B", 0.4), ("B", "C", 0.5), ("C", "A", 0.3), ("A", "D", 0.6)]
        >>> for u, v, p in edges:
        ...     G.add_edge(u, v, weight=p)
        >>> 
        >>> # Select top-2 influential nodes
        >>> seeds = celf(G, k=2, mc=200, prob_attr='weight')
        >>> print(seeds)
        ['A', 'B']

    Use Case:
        - Viral marketing: selecting users to maximize product adoption
        - Social influence analysis: identifying opinion leaders
        - Epidemiology: finding critical nodes for immunization
        - Rumor spreading / misinformation containment

    Reference:
        Leskovec, J., Krause, A., Guestrin, C., Faloutsos, C., VanBriesen, J., & Glance, N. (2007).
        Cost-effective outbreak detection in networks. In *Proceedings of the 13th ACM SIGKDD 
        international conference on Knowledge discovery and data mining* (pp. 420–429).
    """

    import heapq

    if k < 1:
        raise ValueError("k must be at least 1")
    if k > len(G.nodes()):
        raise ValueError(f"k ({k}) cannot exceed number of nodes ({len(G)})")

    # Step 1: initial marginal gains
    pq = []
    for node in G.nodes():
        spread = estimate_spread(G, [node], mc=mc, prob_attr=prob_attr, default_prob=default_prob, **kwargs)
        heapq.heappush(pq, (-spread, node, 0))  # negative for max-heap

    seeds = []
    spread_S = 0

    # Step 2: lazy selection
    while len(seeds) < k:
        gain, node, last_eval = heapq.heappop(pq)
        gain = -gain

        if last_eval == len(seeds):  # already evaluated w.r.t current S
            seeds.append(node)
            spread_S += gain
        else:
            # recompute marginal gain
            spread_with_node = estimate_spread(G, seeds + [node], mc=mc, prob_attr=prob_attr, default_prob=default_prob, **kwargs)
            marginal_gain = spread_with_node - spread_S
            heapq.heappush(pq, (-marginal_gain, node, len(seeds)))

    return seeds

def _celf_deprecated(G, k: int, prob_attr: str = 'weight', default_prob: float = 0.1, **kwargs) -> List[Any]:
    """
    Cost-Effective Lazy Forward (CELF) algorithm for influence maximization.
    
    CELF is an efficient algorithm for finding the k most influential nodes in a network
    for influence maximization under the Independent Cascade model. It uses the lazy
    evaluation technique to reduce the number of spread computations needed.
    
    Parameters:
        G: NetworkX directed graph with edge attributes containing activation probabilities
        k (int): Number of seed nodes to select
        prob_attr (str, optional): Name of edge attribute containing activation probabilities. Defaults to 'weight'.
        default_prob (float, optional): Default probability to use for edges without probability attribute. Defaults to 0.1.
        
    Returns:
        List[Any]: List of k seed nodes that maximize influence spread
        
    Raises:
        ValueError: If k is less than 1 or greater than number of nodes, or if default_prob is not between 0 and 1
        
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
        >>> 
        >>> # Use custom probability attribute
        >>> G2 = nx.DiGraph()
        >>> for u, v, p in edges:
        ...     G2.add_edge(u, v, weight=p)
        >>> seeds = spellbook.network.celf(G2, k=2, prob_attr='weight')
        >>> 
        >>> # Use default probability for all edges
        >>> G3 = nx.DiGraph()
        >>> for u, v in [("A", "B"), ("B", "C"), ("C", "A"), ("A", "D")]:
        ...     G3.add_edge(u, v)
        >>> seeds = spellbook.network.celf(G3, k=2, default_prob=0.5)
        
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
    
    if not 0 <= default_prob <= 1:
        raise ValueError("default_prob must be between 0 and 1")
    
    # Initial marginal gains
    pq = []
    for node in G.nodes():
        active_nodes, _ = independent_cascade(G, {node}, prob_attr=prob_attr, default_prob=default_prob, **kwargs)
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
            active_with_seeds, _ = independent_cascade(G, set(seeds + [node]), prob_attr=prob_attr, default_prob=default_prob)
            active_current, _ = independent_cascade(G, set(seeds), prob_attr=prob_attr, default_prob=default_prob)
            spread_with_seeds = len(active_with_seeds)
            spread_current = len(active_current)
            marginal_gain = spread_with_seeds - spread_current
            heapq.heappush(pq, (-marginal_gain, node, iter_num - 1))
        
        iter_num += 1
    
    return seeds
