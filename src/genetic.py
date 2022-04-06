import random
import math

class Genetic:
    def __init__(self, map, num_iteration, mutation_rate) -> None:
        self._map = map  # MAY NEED UPDATE
        self.is_visited = [[0] * self._map.height for _ in range(self._map.width)]
        self.routes = []
        self.actions = []
        self.num_population = 20
        self.num_iteration = num_iteration #100 # could change, depend on running time
        self.mutation_rate = mutation_rate #0.3 # chould change

    def clear_visited(self):
        self.is_visited = [[0] * self._map.height for _ in range(self._map.width)]
    
    def find_path(self, src, dest):
        """
        Find a path to the opponent.
        """
        self.routes = []
        if src == dest:
            return [src, dest]
        elif dest in self._map.neighbors(src):
            return [src, dest]

        # Generate the initial population
        for _ in range(self.num_population):
            self.clear_visited()
            self.is_visited[src[0]][src[1]] = 1
            route = []
            route.append(src)
            self.generate_random_route(src, dest, 0, route)

        routes_ = sorted(self.routes, key=lambda route: self.fitness_score(dest, route))
        best_route = routes_[0]
        #print("best_route")
        #print(best_route)
        #best_score = self.fitness_score(dest, best_route)

        # REPEAT
        iteration = 0
        while iteration < self.num_iteration:
            #Selection: select parent routes for cross over next generation
            parent_routes = self.selection(dest, routes_)
            
            #Crossover: get child routes' actions
            child_actions = self.cross_over(parent_routes)
            
            #Mutation: mutated child route action
            child_actions = self.mutation(child_actions)
            
            #generate new routes from child_actions
            child_routes = []
            for i in range(len(child_actions)):
                action = child_actions[i]
                child_routes.append(self.direction_to_route(src,action))
            
            #combine parent routes and child routes
            routes_ = parent_routes + child_routes

            #remove possible duplicate routes
            routes_ = self.remove_duplicates(routes_)

            #store valid routes only
            routes_ = self.validate_route(dest, routes_)

            #sorted all the left routes by their fitness score again
            routes_ = sorted(routes_, key=lambda route: self.fitness_score(dest, route))
            
            #update best_route and best_score
            best_route = routes_[0]
            #best_score = self.fitness_score(dest, best_route)

            #keep the number of routes in population stable, not over producing
            routes_ = self.reduce_population(routes_, self.num_population)

            iteration += 1
        return best_route

    # Convert direction to coordinate
    def direction_to_route(self, src, dir):
        route = []
        route.append(src)
        prev = src
        for i in range(len(dir)):
            if dir[i] == 1:
                prev = (prev[0], prev[1] - 1)
                route.append(prev)
            elif dir[i] == 2:
                prev = (prev[0], prev[1] + 1)
                route.append(prev)
            elif dir[i] == 3:
                prev = (prev[0] - 1, prev[1])
                route.append(prev)
            elif dir[i] == 4:
                prev = (prev[0] + 1, prev[1])
                route.append(prev)
        return route

    # Convert coordinate to direction
    def route_to_direction(self, route):
        # 1,2,3,4: left right up down
        dir = []
        for i in range(1, len(route)):
            prev = route[i - 1]
            curr = route[i]
            if prev[0] == curr[0] and prev[1] == curr[1] + 1:
                dir.append(1)
            elif prev[0] == curr[0] and prev[1] == curr[1] - 1:
                dir.append(2)
            elif prev[0] == curr[0] + 1 and prev[1] == curr[1]:
                dir.append(3)
            elif prev[0] == curr[0] - 1 and prev[1] == curr[1]:
                dir.append(4)
        return dir

    # Generate a 10-step route using coordinates
    def generate_random_route(self, src, dest, step, route):
        if src == dest:
            self.routes.append(route)
            print(route)
            return True
        elif step == 10:
            self.routes.append(route)
            print(route)
            return True
        neighbors_ = self._map.neighbors(src)
        random.shuffle(neighbors_)
        for neighbor in neighbors_:
            x = neighbor[0]
            y = neighbor[1]
            if self.is_visited[x][y] == 0:
                self.is_visited[x][y] = 1
                route.append(neighbor)
                if self.generate_random_route(neighbor, dest, step + 1, route):
                    return True
                route = route[:len(route) - 1]
                self.is_visited[x][y] = 0
                return False
        return False

    #the fitness score for each route is its length + distance between end point and destination
    def fitness_score(self, dest, route):
        ans = math.inf
        x = route[len(route) - 1][0] - dest[0]
        y = route[len(route) - 1][1] - dest[1]
        ans = min(len(route) + math.sqrt(math.pow(x, 2) + math.pow(y, 2)), ans)
        return ans

    #select fittest routes from population, delete ones with inf score
    def selection(self, dest, routes):
        i = len(routes) - 1
        score = self.fitness_score(dest, routes[i])
        while score == math.inf:
            routes = routes[:len(routes)-1]
            i -= 1
            score = self.fitness_score(dest,routes[i])
        return routes

    #parameter: parent_routes   return: child_actions
    #pairing parents and cross over at random point to produce new child actions
    def cross_over(self,routes):
        #get parent routes' actions
        parent_actions = []
        [parent_actions.append(self.route_to_direction(r)) for r in routes]
        #print("parent direction")
        #print(parent_actions)
        #print()
        i = 0
        child_actions = []
        while i < len(parent_actions):
            if i != len(parent_actions) - 1:
                action1 = parent_actions[i]
                action2 = parent_actions[i + 1]
                cross_over_point = random.randint(1, min(len(action1) - 1,len(action2) - 1) )
                tmp = action1[:cross_over_point]
                action1[:cross_over_point] = action2[:cross_over_point]
                action2[:cross_over_point] = tmp
                child_actions.append(action1)
                child_actions.append(action2)
            i += 2
        #print("child direction")
        #print(child_actions)
        #print()
        return child_actions

    #parameter: child_actions return: mutated_actions
    #randomly mutate child actions to increase diversity
    def mutation(self, actions):
        for action in actions:
            #print("original action: "+str(action))
            mutation_count = math.floor(len(action) * self.mutation_rate)
            mutation_point = []
            for n in range(mutation_count):
                mutation_point.append(random.randint(0, len(action) - 1))
            for p in mutation_point:
                new_action = random.randint(1,4)
                action[p] = new_action
            #print("mutated action: " + str(action))
            #print()
        return actions

    #keep population contains the same amount of (best) routes
    def reduce_population(self, routes, num_population):
        if num_population < len(routes):
            num_to_delete = len(routes) - num_population
            for _ in range(num_to_delete):
                routes = routes[:len(routes)-1]
        return routes

    #remove duplicate route in the routes
    def remove_duplicates(self, routes):
        unique_routes = []
        [unique_routes.append(x) for x in routes if x not in unique_routes]
        return unique_routes

    #validate routes, remove ones walk through wall and walk outside map
    def validate_route(self, dest, routes):
        valid_routes = []
        is_valid = True
        for route in routes:
            i = 0
            while i < len(route) and is_valid:
                if route[i] == (dest):
                    route = route[:i+1]
                    break
                if not self._map.valid(route[i]):
                    is_valid = False
                if i < len(route)-1 and route[i+1] not in self._map.neighbors(route[i]):
                    is_valid = False
                i += 1
            if is_valid:
                valid_routes.append(route)
            is_valid = True
        return valid_routes