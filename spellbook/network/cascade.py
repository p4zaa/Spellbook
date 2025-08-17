"""
Independent cascade model simulations for network analysis.

This module provides functions for simulating information diffusion
and influence propagation in networks using the Independent Cascade model.
"""

import random
from typing import Set, List, Tuple, Any


def independent_cascade_once(
    G, 
    seeds: Set[Any], 
    max_steps: int = 10
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
        max_steps (int, optional): Maximum number of simulation steps. Defaults to 10.

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
        >>> active_nodes, step_activations = spellbook.network.independent_cascade_once(G, seeds)
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
