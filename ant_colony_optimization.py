'''
    Ant colony optimization algorithm for:
    Shortest Route between Carnival Attractions Problem

    Visit each city once and find the shortest route between all attractions

    Author: Sebastian Castro
    Date: 8/20/2021
'''
import random

'''
Below you will find the Dictionary containing the distances
between the different attractions. We use the dictionary of 
dictionaries
'''
Distances = {
    'Circus':{
        'Ballons':8,
        'BumperCars' : 7,
        'Carousel':4,
        'Swings':6,
        'FerrisWheel':4
    },
    'Ballons':{
        'Circus':8,
        'BumperCars' : 5,
        'Carousel':7,
        'Swings':11,
        'FerrisWheel':5 
    },
    'BumperCars':{
        'Circus':7,
        'Ballons' : 5,
        'Carousel':9,
        'Swings':6,
        'FerrisWheel':7 
    },
    'Carousel':{
        'Circus':4,
        'Ballons' : 7,
        'BumperCars':9,
        'Swings':5,
        'FerrisWheel':6 
    },
    'Swings':{
        'Circus':6,
        'Ballons' : 11,
        'BumperCars':6,
        'Carousel':5,
        'FerrisWheel':3 
    },
    'FerrisWheel':{
        'Circus':4,
        'Ballons' : 5,
        'BumperCars':7,
        'Carousel':6,
        'Swings':3 
    }
}

'''
You will also find a list of the cities with their 
pheromone levels which are initialized to 1 to avoid
bias in any attraction
'''
phermones = {
    'Circus':{
        'Ballons':1,
        'BumperCars' : 1,
        'Carousel':1,
        'Swings':1,
        'FerrisWheel':1
    },
    'Ballons':{
        'Circus':1,
        'BumperCars' : 1,
        'Carousel':1,
        'Swings':1,
        'FerrisWheel':1 
    },
    'BumperCars':{
        'Circus':1,
        'Ballons' : 1,
        'Carousel':1,
        'Swings':1,
        'FerrisWheel':1 
    },
    'Carousel':{
        'Circus':1,
        'Ballons' : 1,
        'BumperCars':1,
        'Swings':1,
        'FerrisWheel':1 
    },
    'Swings':{
        'Circus':1,
        'Ballons' : 1,
        'BumperCars':1,
        'Carousel':1,
        'FerrisWheel':1 
    },
    'FerrisWheel':{
        'Circus':1,
        'Ballons' : 1,
        'BumperCars':1,
        'Carousel':1,
        'Swings':1 
    }
}

'''
Ant class which will represent an ant that will 
"walk around" through all attractions, visiting 
each attraction exactly once. The ants will record 
their distance travelled as fitness and the route taken 
@author Sebastian Castro
'''
class Ant:
    def __init__(self,attraction):
        '''
        Parameters: 
            attraction - a random attraction by which the any Ant starts its journey
        Attributes:
            attraction - the starting attraction where the atn starts its journey
            visited - a dictionary containing attractions which are visited (1) or not (0)
            fitness - the total distance travelled and is used to measure which ants are better or not
        '''
        self.attraction = attraction
        self.visited = {att:0 for att in Distances.keys()}
        self.visited[attraction] = 1
        self.fitness = 0
        self.route = [attraction]
    def random_attraction(self):
        '''
        This function will pick a random attraction for the ant to travel using
        the current list of attractions not visited
        Parameters: None
        Returns: None
        '''
        total = 0
        last_visited = self.route[-1]
        not_visited = [i for i in self.visited.keys() if self.visited[i] == 0]
        #print(not_visited)
        nonVisit = len(not_visited)
        #there could be four or two attractions left
        if nonVisit ==0:
            return None       
        piece = 1/nonVisit 
        spin = random.random()
        for i in not_visited:
            tup = (total, total + piece)
            total += piece
            if spin >= tup[0] and spin < tup[1]:
                self.visited[i] = 1
                self.route.append(i)
                #print(f'lastplace is {last_visited} and the i is {i}')
                self.fitness += Distances[last_visited][i]
                break 
    def pheromone_heuristic(self,phermones,heuristics):
        '''
        This function will calculate the probabilistic value of travelling
        a specific route using the heuristic value and the pheromone levels 
        Parameters:
            phermones - The phermone value between two cities 
            heuristic - the distance between two cities
        Returns: The probabilistic value of travelling between two cities 
        '''
        alpha = 4
        beta = 7
        finale  = phermones**alpha * (1/heuristics)**beta
        return finale

    def pheromone_attraction(self):
        '''
        This function will find the next attraction to visit 
        according to the pheromones found on all available 
        paths and the heuristic value.
        We will use the roulette wheel selection to pick the best route
        Parameters: None
        Returns: None
        '''
        global phermones
        last_place = self.route[-1]
        totale = 0
        total = 0
        #triplets - place, start, end
        spin = random.random()
        wheel = []
        wheels2 = []
        for i in self.visited.keys():
            if self.visited[i] == 0:
                addy = self.pheromone_heuristic(phermones[last_place][i],Distances[last_place][i])
                wheel.append([i,totale,totale+addy])
                totale += addy
        for i in self.visited.keys():
            if self.visited[i] == 0:
                addy = self.pheromone_heuristic(phermones[last_place][i],Distances[last_place][i])
                wheels2.append((i,total, total + addy/totale))
                total += addy/totale    
        check = False 
        for i in wheels2:
            if i[1] <= spin < i[2]:
                self.route.append(i[0])
                self.fitness += Distances[last_place][i[0]]
                self.visited[i[0]] = 1 #now we are visiting the place
                #print("We are now visiting " + i[0])
                check = True
                break

    def visit_attraction(self):
        '''
        Driver function for the above attraction visiter functions
        The function will spin the wheel and will decide whether the ant
        takes a random attraction or an attraction based on the pheromones
        and distance values
        Parameters: None
        Returns: None
        '''
        spin = random.random()
        if 0.00 <= spin < 0.15:
            #print("Entering random picking")
            self.random_attraction()
        else:
            #print("Entering pheromone based picking")
            self.pheromone_attraction()
    
    def make_trips(self):
        '''
        This function will make the ant make a complete trip across all
        attractions and is the main driver function in this class
        Parameters: None
        Returns: None
        '''
        count = 5
        while count !=0:
            #print(f'Current route is {self.route}, run: {5-count}')
            self.visit_attraction()
            count -= 1
        

    
    def __str__(self):
        '''
        A string representation of the ant class displaying its route 
        taken and the fitness (distance)
        '''
        return f'This ant has fitess {self.fitness} and route: {self.route}'
    
'''
This class will hold a colony of ants and will hold the best route and 
best fitness (shortest route) every generation 
'''
class AntColony:
    def __init__(self,attractions,ant_factor):
        '''
        Parameters:
            attractions - number of attractions in carnival
            ant_factor - an integer used to get the total number of ants
        Attributes:
            antTotal - number of ants in the colony
            bestFitness - the best route with the shortest distance travelling
            antColony - The ant colony
            bestRoute - The current best route travelling each attraction once
        '''
        self.antTotal = attractions * ant_factor
        self.bestFitness = None
        self.antColony = []
        self.bestRoute = []
    def initializeAntColony(self):
        '''
        Intializes the ant colony so all ants will start at a random 
        route
        Parameters: None
        Returns: None
        '''
        for i in range(self.antTotal):
            ant = Ant(self.random_attraction())
            self.antColony.append(ant)

    def findBestFitness(self):
        '''
        Finds the ant with the shortest route and updates the 
        bestFitness and bestRoute attributes
        Parameters: None
        Returns: None
        '''
        best_ant = min(self.antColony, key = lambda x: x.fitness)
        if self.bestFitness == None:
            self.bestFitness = best_ant
            self.bestRoute = best_ant.route
        elif best_ant.fitness < self.bestFitness.fitness:
            self.bestFitness = best_ant
            self.bestRoute = best_ant.route
        print(f'The best solution is: {best_ant.fitness}')
        print(f'The current best solution is: {self.bestFitness.fitness}')    

    def random_attraction(self):
        '''
        Used to initialize individual ants with a random location
        Parameters: None
        Returns: The random attraction
        '''
        total = 0
        piece = 1/6
        spin = random.random()
        for i in Distances.keys():
            tup = (i,total, total + piece)
            total += piece
            if spin >= tup[1] and spin < tup[2]:
                return tup[0] 
                break

    def update_Pheromones(self,evaportation_Rate):
        '''
        This function will update the pheromone numbers per generation after
        all ants have changed the pheromones levels per trip
        Parameters:
            evaporation_rate: The percentage by which the pheromone strength gets reduced
        Returns: None
        '''
        for i in phermones.keys():
                for j in phermones[i].keys():
                    phermones[i][j] *= evaportation_Rate
        for ant in self.antColony:
            for i in range(len(ant.route)-1):
                phermones[ant.route[i]][ant.route[i+1]] += 1/ant.fitness
            phermones[ant.route[len(ant.route)-1]][ant.route[0]] += 1/ant.fitness

    def run_Simulation(self,generations = 10):
        '''
        The driver function that will run a certain amount of simulations
        Parameters: 
            generations: The number of generations the simulation will run
        Returns: None
        '''
        for i in range(generations):
            self.initializeAntColony()
            for ant in self.antColony:
                #print("Im here")
                ant.make_trips()
                #print(ant)
            self.update_Pheromones(0.50)
            self.findBestFitness()
            print("generation NUMBER :" + str(i))
            print(f'The best solution is: {self.bestFitness.fitness} and the best route is: {self.bestRoute}')
            self.antColony.clear()

def main():
    '''
    Driver function for overall function that will
    initialize the ant colony class and run a certain
    number of simulations
    '''
    Ant_colony = AntColony(6,5)
    Ant_colony.run_Simulation(1000)


main()