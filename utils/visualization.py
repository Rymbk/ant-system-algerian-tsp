"""
Visualization utilities for TSP solutions
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch


def plot_tour(wilayas, best_tour, start_idx, end_idx):
    """
    Plot the tour on a map with cities and route.
    
    Args:
        wilayas (list): List of wilaya dictionaries with 'lat', 'lon', 'name'
        best_tour (list): Best tour as list of city indices
        start_idx (int): Starting city index
        end_idx (int): Ending city index
    
    Returns:
        matplotlib.figure.Figure: The figure object
    """
    fig, ax = plt.subplots(figsize=(16, 11))
    
    # Simple dark background
    ax.set_facecolor('#1a1a2e')
    fig.patch.set_facecolor('#1a1a2e')
    
    # Extract coordinates
    lats = [w['lat'] for w in wilayas]
    lons = [w['lon'] for w in wilayas]
    
    # Plot tour path
    if best_tour:
        tour_lons = [wilayas[city]['lon'] for city in best_tour]
        tour_lats = [wilayas[city]['lat'] for city in best_tour]
        
        # Simple line
        ax.plot(tour_lons, tour_lats, '-', color='#00ff88', 
                linewidth=2, alpha=0.9, zorder=3)
        
        # Draw arrows
        for i in range(len(best_tour) - 1):
            x1, y1 = wilayas[best_tour[i]]['lon'], wilayas[best_tour[i]]['lat']
            x2, y2 = wilayas[best_tour[i+1]]['lon'], wilayas[best_tour[i+1]]['lat']
            
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            dx, dy = x2 - x1, y2 - y1
            
            arrow = FancyArrowPatch(
                (mid_x - dx*0.1, mid_y - dy*0.1),
                (mid_x + dx*0.1, mid_y + dy*0.1),
                arrowstyle='->',
                mutation_scale=20,
                color='#00ff88',
                linewidth=2,
                zorder=5
            )
            ax.add_patch(arrow)
    
    # Plot cities
    for idx, wilaya in enumerate(wilayas):
        if idx == start_idx:
            color = '#ff4444'
            size = 120
        elif idx == end_idx:
            color = '#ffd700'
            size = 120
        else:
            color = '#4ecdc4'
            size = 70
        
        # Simple circles
        ax.scatter(wilaya['lon'], wilaya['lat'], c=color, s=size, 
                  edgecolors='white', linewidth=1.5, zorder=7, alpha=0.95)
        
        # Add order numbers
        if best_tour and idx in best_tour:
            order = best_tour.index(idx) + 1
            ax.text(wilaya['lon'], wilaya['lat'] + 0.3, str(order),
                   fontsize=10, ha='center', color='white', 
                   fontweight='bold', zorder=9)
    
    # Labels and styling
    ax.set_xlabel('Longitude', color='white', fontsize=12)
    ax.set_ylabel('Latitude', color='white', fontsize=12)
    ax.tick_params(colors='white', labelsize=10)
    ax.grid(True, alpha=0.2, color='gray', linestyle='-', linewidth=0.5)
    
    plt.tight_layout()
    return fig