
from collections import deque, defaultdict
import sys
import time
import heapq

sys.setrecursionlimit(500000)  # Imposta il limite di ricorsione a 500000 (adattare in base alle necessità)


def configure_recursion_limit(new_limit: int) -> bool:
    """
    Imposta un nuovo limite di ricorsione per evitare RecursionError nelle ricerche DFS.
    """
    try:

        if new_limit > 1:
            sys.setrecursionlimit(new_limit)
            return True
        
    except (TypeError, RecursionError):
        print("Il limite di ricorsione deve essere un intero maggiore o uguale a 2.")

    return False



#BREADTH-FIRST SEARCH
def breadth_first_search(graph: defaultdict, start: int, goal: int) -> tuple | None:
    """
    Algoritmo di ricerca Breadth-First Search (BFS).
    """
    iterations = 1
    memory_used = 1
    
    if start == goal:
        return ("Breadth-First Search", [start], iterations, memory_used)
    
    queue = deque([(start, [start])])
    explored = set()
    
    while queue:

        current_node, path = queue.popleft()
        
        if current_node in explored:
            continue
        
        explored.add(current_node)
        
        for nearby in graph[current_node]:
            iterations += 1
            memory_used = max(memory_used, len(queue))
            
            if nearby == goal:
                return ("Breadth-First Search", path + [nearby], iterations, memory_used)
            
            queue.append((nearby, path + [nearby]))
    
    return None # Nessun percorso trovato




#DIJKSTRA ALGORITHM
def dijkstra_search(graph, start, goal):
    """
    Algoritmo di Dijkstra per la ricerca del percorso ottimo
    """
    priority_queue = [(0, start, [start])]  # (costo, nodo corrente, percorso)
    explored = set()
    iterations = 1
    memory_used = 1
    
    while priority_queue:

        cost, current_node, path = heapq.heappop(priority_queue)
        
        if current_node in explored:
            continue
        
        explored.add(current_node)
        
        if current_node == goal:
            return ("Dijkstra Search", path, iterations, memory_used)
        
        for neighbor, weight in graph.get(current_node, []):
            if neighbor not in explored:
                new_cost = cost + weight
                heapq.heappush(priority_queue, (new_cost, neighbor, path + [neighbor]))
                
                iterations += 1
                memory_used = max(memory_used, len(priority_queue))
    
    return None  # Nessun percorso trovato




#DEPTH-FIRST SEARCH
def depth_first_search(graph: defaultdict, start_node: int, goal_node: int) -> tuple | None:
    """
    Algoritmo di ricerca Depth-First Search (DFS).
    """
    explored = set()
    path = []
    performance = [0, 0]  # Iterazioni, Memoria usata
    
    if dfs_recursion(graph, start_node, goal_node, path, explored, performance):
        return ("Depth-First Search", path, *performance)
    
    return None # Nessun percorso trovato


def dfs_recursion(graph: defaultdict, current_node: int, goal_node: int, path: list, explored: set, performance: list[int]) -> bool:
    """
    Funzione ricorsiva per la ricerca Depth-First Search (DFS).
    """
    # Aggiungi il nodo corrente al percorso e all'insieme esplorato
    path.append(current_node)
    explored.add(current_node)
    
    # Incrementa il numero di iterazioni e monitora la memoria
    performance[0] += 1  # Iterazioni
    performance[1] = max(performance[1], len(path))  # Memoria usata
    
    # Se il nodo corrente è il nodo obiettivo, termina la ricerca
    if current_node == goal_node:
        return True
    
    # Esplora i nodi adiacenti
    for nearby in graph[current_node]:   # Controlla se il nodo adiacente non è stato ancora esplorato

        if nearby not in explored:   # Prosegui la ricerca in modo ricorsivo
            if dfs_recursion(graph, nearby, goal_node, path, explored, performance):
                return True
    
    # Rimuovi il nodo corrente dal percorso se non è stato trovato il percorso
    path.pop()

    return False




#DEPTH-LIMITED SEARCH
def depth_limited_search(graph: defaultdict, start_node: int, goal_node: int, recursion_limit: int) -> tuple | None:
    """
    Algoritmo di ricerca Depth-Limited Search (DLS).
    """
    explored = set()
    path = []
    performance = [0, 0, -1, recursion_limit]  # Iterazioni, Memoria, Profondità attuale, Limite profondità
    
    if dls_recursion(graph, start_node, goal_node, path, explored, performance):
        return (f"Depth-Limited Search [LIMITE: {recursion_limit}]", path, *performance)
    

    return None  # Nessun percorso trovato


def dls_recursion(graph: defaultdict, current_node: int, goal_node: int, path: list, explored: set, performance: list[int]) -> bool:
    """
    Funzione ricorsiva per la ricerca Depth-Limited Search (DLS).
    """
    path.append(current_node)
    explored.add(current_node)
    performance[2] += 1  # Profondità attuale
    performance[0] += 1  # Iterazioni
    performance[1] = max(performance[1], len(path))
    
    if current_node == goal_node:
        return True
    
    if performance[2] < performance[3]:  # Controllo del limite di profondità
        for nearby in graph[current_node]:
            if nearby not in explored and dls_recursion(graph, nearby, goal_node, path, explored, performance):
                return True
    
    performance[2] -= 1
    path.pop()

    return False




#ITERATIVE-DEEPING SEARCH
def iterative_deepening_search(graph: defaultdict, start_node: int, goal_node: int) -> tuple | None:
    """
    Algoritmo di ricerca Iterative Deepening Search (IDS).
    """
    recursion_limit = 0
    start_time = time.time()
    
    while True:

        result = depth_limited_search(graph, start_node, goal_node, recursion_limit)
        
        if result:
            return (f"Iterative Deepening Search [PROFONDITÀ SOLUZIONE: {recursion_limit}]", result[1], *result[2:])
        
        recursion_limit += 1
        
        if time.time() - start_time > 1800:  # Failsafe dopo 30 minuti
            return None  # Nessun percorso trovato




def search(start_node : int, goal_node : int, graph : defaultdict, search_type : str, depth : int, start_time : float) -> None:
    """
    Funzione principale per eseguire la ricerca basata sul tipo di algoritmo selezionato.
    """
    result = ()

    #CHOICE
    match search_type:
        case "BFS":
            result = breadth_first_search(graph, start_node, goal_node)
        case "DFS":
            result = depth_first_search(graph, start_node, goal_node)
        case "DLS":
            result = depth_limited_search(graph, start_node, goal_node, depth)
        case "IDS":
            result = iterative_deepening_search(graph, start_node, goal_node)
        case "Dijkstra":
            result = dijkstra_search(graph, start_node, goal_node)
    
    timer = time.time()
    
    if result:
        print(f"\n\n-- RESULT --\nPath from Node {start_node} to Node {goal_node}: \n{result[1]}"
            f"\n\nPATH LENGTH: {len(result[1])} nodes\nTIME COMPLEXITY: {result[2]} iterations\nEXECUTION TIME: {timer - start_time}s\nMAXIMUM MEMORY USAGE: {result[3]} queue elements\nALGORITHM USED: {result[0]}\n\n")
    
    else:
        print(f"\nNo path found from Node {start_node} to Node {goal_node}\n")
