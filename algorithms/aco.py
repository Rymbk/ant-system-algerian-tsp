"""
Ant Colony Optimization Algorithm Implementation
"""
import numpy as np


class AntColonyOptimization:
    """
    Ant Colony Optimization algorithm for solving TSP.
    
    Attributes:
        distance_matrix (np.ndarray): Distance matrix between cities
        num_cities (int): Number of cities
        num_ants (int): Number of ants in the colony
        alpha (float): Pheromone importance weight
        beta (float): Distance importance weight
        evaporation_rate (float): Pheromone evaporation rate
        Q (float): Pheromone deposit factor
        pheromones (np.ndarray): Pheromone matrix
        best_tour (list): Best tour found so far
        best_distance (float): Best distance found so far
        history (list): History of best distances per iteration
    """
    
    def __init__(self, distance_matrix, num_ants, alpha, beta, evaporation_rate, Q):
        """
        Initialize ACO algorithm.
        
        Args:
            distance_matrix (np.ndarray): Distance matrix between cities
            num_ants (int): Number of ants in the colony
            alpha (float): Pheromone importance weight
            beta (float): Distance importance weight
            evaporation_rate (float): Pheromone evaporation rate (0-1)
            Q (float): Pheromone deposit factor
        """
        self.distance_matrix = distance_matrix
        self.num_cities = len(distance_matrix)
        self.num_ants = num_ants
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.Q = Q
        
        # Initialize pheromone matrix with uniform values
        self.pheromones = np.ones((self.num_cities, self.num_cities))
        
        self.best_tour = None
        self.best_distance = float('inf')
        self.history = []
    
    def calculate_distance(self, tour):
        """
        Calculate total distance of a tour.
        
        Args:
            tour (list): List of city indices representing the tour
        
        Returns:
            float: Total distance of the tour
        """
        distance = 0
        for i in range(len(tour) - 1):
            distance += self.distance_matrix[tour[i]][tour[i + 1]]
        return distance
    
    def construct_solution(self, start_city, end_city):
        """
        Construct a solution (tour) for a single ant.
        
        Args:
            start_city (int): Starting city index
            end_city (int): Ending city index
        
        Returns:
            list: Tour as a list of city indices
        """
        tour = [start_city]
        visited = {start_city}
        current_city = start_city
        
        # Build tour excluding end city until the end
        while len(tour) < self.num_cities - 1:
            next_city = self.select_next_city(current_city, visited, end_city)
            tour.append(next_city)
            visited.add(next_city)
            current_city = next_city
        
        # Add end city as the last city
        tour.append(end_city)
        return tour
    
    def select_next_city(self, current_city, visited, end_city):
        """
        Select the next city to visit based on pheromone and distance.
        
        Args:
            current_city (int): Current city index
            visited (set): Set of already visited cities
            end_city (int): End city index (to be excluded until last)
        
        Returns:
            int: Index of the next city to visit
        """
        probabilities = []
        
        for city in range(self.num_cities):
            if city not in visited and city != end_city:
                pheromone = self.pheromones[current_city][city] ** self.alpha
                distance = (1.0 / self.distance_matrix[current_city][city]) ** self.beta
                probabilities.append((city, pheromone * distance))
        
        if not probabilities:
            return end_city
        
        # Roulette wheel selection
        cities, probs = zip(*probabilities)
        probs = np.array(probs)
        probs = probs / probs.sum()
        
        return np.random.choice(cities, p=probs)
    
    def update_pheromones(self, all_tours):
        """
        Update pheromone matrix based on all ant tours.
        
        Args:
            all_tours (list): List of tuples (tour, distance)
        """
        # Evaporation
        self.pheromones *= (1 - self.evaporation_rate)
        
        # Deposit pheromones
        for tour, distance in all_tours:
            deposit = self.Q / distance
            for i in range(len(tour) - 1):
                self.pheromones[tour[i]][tour[i + 1]] += deposit
                self.pheromones[tour[i + 1]][tour[i]] += deposit
    
    def run_iteration(self, start_city, end_city):
        """
        Run one iteration of the ACO algorithm.
        
        Args:
            start_city (int): Starting city index
            end_city (int): Ending city index
        
        Returns:
            tuple: (best_tour, best_distance, avg_distance)
        """
        all_tours = []
        
        # Each ant constructs a solution
        for _ in range(self.num_ants):
            tour = self.construct_solution(start_city, end_city)
            distance = self.calculate_distance(tour)
            all_tours.append((tour, distance))
            
            # Update best solution if found
            if distance < self.best_distance:
                self.best_distance = distance
                self.best_tour = tour.copy()
        
        # Update pheromones
        self.update_pheromones(all_tours)
        self.history.append(self.best_distance)
        
        # Calculate average distance
        avg_distance = np.mean([d for _, d in all_tours])
        
        return self.best_tour, self.best_distance, avg_distance