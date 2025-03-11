from collections import defaultdict

def graph_generation(file_path: str, weighted=True) -> defaultdict:
    """
    Funzione per creare un grafo leggendo nodi e pesi dal file.
    - weighted=True → Mantiene i pesi (per Dijkstra).
    - weighted=False → Ignora i pesi (per BFS, DFS, DLS, IDS).
    """
    graph = defaultdict(list)
    
    try:
        
        with open(file_path, 'r') as file:
            for row in file:
                if row.startswith('#'):
                    continue

                parts = row.strip().split('\t')
                
                if len(parts) == 3:
                    from_node, to_node, weight = int(parts[0]), int(parts[1]), int(parts[2])

                    if weighted:
                        graph[from_node].append((to_node, weight))  # Mantiene peso

                    else:
                        graph[from_node].append(to_node)  # Ignora peso

                elif len(parts) == 2:  # Gestisce file senza peso
                    from_node, to_node = int(parts[0]), int(parts[1])
                    graph[from_node].append(to_node)
    
    except Exception as e:
        print(f"Errore nella lettura del file: {e}")
    
    return graph
