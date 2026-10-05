import random
import copy
import math

class Chromosome:
    #create a class dynamically assigning attributes to its objects. The only mandatory attribute is genes, which let's be honest, you can't have a genetic algorithm without chromosomes having genes
    def __init__(self, genes, **attributes):
        self.genes = genes  # Store the genes
        for key, value in attributes.items():
            setattr(self, key, value)  # Dynamically add other attributes

def gen0_binary(population_number, genes_no):
    #create generation 0. given the number of parents and their genes number, this function creates chromosomes with the desired number of BINARY genes. This function returns a list of lists
    chromosome_list = []
    
    for i in range(population_number):  # Total number of generation 0 chromosomes
        genes = []
        
        for g in range(genes_no):  # Number of genes for each chromosome
            genes.append(random.randint(0, 1))
        
        chromosome_list.append(genes)

    return chromosome_list

def spc(population):
    # ------------------------Single Point Crossover-------------------------------
    # Select smallest parent. We need to trade equal genes between the two parents, so we can't select the biggest.
    
    smallest = len(population[0].genes)
    
    #check the length of the smallest parent
    for i in population:
        if len(i.genes) < smallest:
            smallest = i

    #generate a random crossover point within the range length of the smallest parent
    crossover_point = random.randint(1, smallest-1)#if we don't use smallest-1, the max length may be picked, assigning the whole parent to the corresponding first_half, while leaving second_half empty
    
    #break down the parents into two halves
    first_halves = []
    second_halves = []
    
    for i in population:
        first_half = i.genes[:crossover_point]
        first_halves.append(first_half)
        second_half = i.genes[crossover_point:]
        second_halves.append(second_half)
    
    
    #get all the chromosome sequences form the parents to check if there are offsprings with the same sequence. This helps not having offsprings same to the parents
    parents_genes_int = []

    for i in population:
        parents_genes_int.append(i.genes)
    
    new_offsprings = []
    
    #make the new offsprings
    for i in first_halves:
        second_half_to_use = random.randint(0,len(second_halves)-1)#pick a random second half to stitch to the first half. always use -1 when using the max length as an index. else you get out of indexes
        new_offspring = i+second_halves[second_half_to_use]#stitch them together
        
        if new_offspring not in new_offsprings:#check for duplicates
            if new_offspring not in parents_genes_int:#check if offsprings do not match parents
                new_offsprings.append(new_offspring)

    return new_offsprings

def kpc(parents,crossover_points_number):
#------------------------K Point Crossover-------------------------------
#select smallest parent. we need to trade equal genes between the two parents, so we can't select one just randomly
#the last index of a list is always len(list)-1. so, if you try to use list[len(list)] you get an error. you have to use length-1. THIS IS NOT TRUE IN CONJUCTION WITH range, because range(5) will reach up to 4
    
#the helper lists serve to collect all the genes in the in-between crosspoint spaces for all parents. 1st has all the genes for each parent from start to 1st crosspoint, while last has the genes from last
#crosspoint to the end of each parent.
    
#middle is a bit more complicated. It is meant to be a list of lists. Each outer list element holds lists with all genes for a given crossover space for each parent,
#but does so in a separate list for each parent. So, for crosspoints 4,5,8, middle[0] will hold the crosspoint space 4-5 for all parents, a separate list for each one.
#The second one will hold all genes from 5-8.
    
#Finally, we use 1st, last and the middle lists, which now hold the parents' gene sequences, to stitch together the offsprings
 
#---- PART 1--- GENERATE CROSSOVER POINTS
 
 #check if the given crossover points number is legit
    if crossover_points_number == 1:
        print("Son, if you want to use Single Point crossover just call spc! This function is designed for =>2 crossover points!")
        exit()
    elif crossover_points_number < 1:
        print("Stop messing around and provide a number => 2 for your crossover points!")
        exit()
 
    offspring_middle_groups_helper = [] 
    offspring_1st_genes_helper = []
    offspring_last_genes_helper = []
    
    #set random parent's length to later find smallest parent
    smallest_parent_len=len(parents[0].genes)
    
    for i in parents:
        if len(i.genes) < smallest_parent_len:
            smallest_parent_len = len(i.genes)    
    
    #check if crossover_points_number is higher than smallest_parent_len. if it is, the program exits because you cant request more crossover points than the parents length
    if smallest_parent_len <= crossover_points_number:
        print("You can't create more crossover points than the smallest parents length. This program will now exit.")
        exit()
    
    #create crossover points. the total number is given by the user. We create random crossover points and then sort them. Each crossover point is unique,
    #meaning each number will only appear once in the list. The numbers in this list will be used to break down the parents to random gene sequences.
    crossover_points= []
    while len(crossover_points) < crossover_points_number:
        crossover_index = random.randint(1,smallest_parent_len-1)#if the smallest parent has length 7, the parent's last element is [6]. if 7 gets picked by randit, then we have an error. So here we want to avoid the last crossovr gene being the last item of the list-parent. This is why we use -1
        if crossover_index not in crossover_points:
            crossover_points.append(crossover_index)
    
    crossover_points.sort()
    # print("--------------\ncrossover points:",crossover_points,"\n--------------")
    
    
    #below are some checks
    if smallest_parent_len < crossover_points[-1]:#we can't have the biggest crossover point not being able to be used as an index in the smallest parent
        print("Crossover points biggest index is bigger than smallest parent's length")
        exit()

    if crossover_points_number > smallest_parent_len: #if smallest parent's length is smaller than the amount of crossover points chosen you will get an error
        print("Wow! Easy there, lad. You can't have more crossover points than the smallest parent's elements! Get yourself serious, boy!")
        print("total crossover points chosen:",crossover_points_number)
        print("smallest parent length:",smallest_parent_len)
        exit()


#----PART 2 ----- SLICE THE PARENTS TO CREATE RANDOM GENE SEQUENCES

    #construct middle groups list. Add lists equal to the total crossover spaces, excluding [0]-1st crosspoint and [-1]-end of genes list
    for i in range(len(crossover_points)-1): #The crossover in-between spaces are always one less than the total crossover points => crossover spaces = len(crossover_points)-1
        offspring_middle_groups_helper.append(list())

    #we use list slicing on parents lists. To do so, we use as indexes the elements of the crossover_points list

    for j in range(len(parents)):

        offspring_1st_genes_helper.append(parents[j].genes[:crossover_points[0]]) #add to the list to construct the offsprings later

        for i in range(len(crossover_points)-1):#The crossover in-between spaces are always one less than the total crossover points #crossover spaces = len(crossover_points)-1

            offspring_middle_groups_helper[i].append(parents[j].genes[crossover_points[i]:crossover_points[i+1]])#add to the list to construct the offsprings later

        offspring_last_genes_helper.append(parents[j].genes[crossover_points[i+1]:])#add to the list to construct the offsprings later. If we allow kpc to take in only one point for crossover, this point hits a problem. because crossover points has only 1 element, there is no next element to acces with crossover_points[i+1]
    
#----- PART 3 --- STITCH 'EM TOGETHER

    #stitch the parent gene sequences together. it will be composed of an outer list, and each element will be another list. if you join all the inner lists of an elemenet together
    #you get the offspring.
    
    #at this point, we could implement a mechanism to choose how many offsprings will be generated. Currently one offspring gets generated for each parent.
    #To have a fuller, clearer image of if the above mechanism is needed or not, it would be best to finalize the selection methods first. This, because the selection method MAY take care of that
    #and so kpc won't need to decide how many parents to generate

    offsprings = []
    
    for x in range(len(parents)):#len(parents) to generate as many offsprings as parents we get

        offsprings_gene_seq_union = offspring_1st_genes_helper[x]
        
        for i in range(len(offspring_middle_groups_helper)):#to each offspring, add a gene sequence for each of the middle crossover spaces, from a random parent, thus creating a totally new offspring
            gene_seq_used=random.randint(0,len(offspring_middle_groups_helper[i])-1)#usage of variable to hold the selected index just to be able to print and report. -1 because, same as crossover points-1, if random gets the full length, we get an error, as the list has always one less index than its length. len(offspring_middle_groups_helper[i])-1 or parents-1 has to be used, because we need to pick a random element from each inner list. each len(offspring_middle_groups_helper[i])==  len(parents), so we can use either len(offspring_middle_groups_helper[i])-1 or parents-1. If offspring_middle_groups_helper[i] != len(parents) WE CAN NOT USE EITHER. WE MOST PROBABLY HAVE TO USE THE FIRST ONE. All this happens because each offspring_middle_groups_helper[i] grows or shrinks in length along with the parents. so if len(parents =30 then  len(offspring_middle_groups_helper[i])=30
            offsprings_gene_seq_union = offsprings_gene_seq_union + offspring_middle_groups_helper[i][gene_seq_used]

        #get new random index to use for getting the last part of the offsprings
        gene_seq_used=random.randint(0,len(parents)-1)#usage of variable to hold the selected index just to be able to print and report. As long as we are generating the same number of offsprings as parents, we can use the len(parents)-1 here
        offsprings_gene_seq_union = offsprings_gene_seq_union + offspring_last_genes_helper[gene_seq_used]

        offsprings.append(offsprings_gene_seq_union)

    
#----- PART 4 --- CHECKING FOR DUPLICATES IN THE OFFSPRINGS PLUS IF ANY OFFSPRINGS MATCH ANY OF THE PARENTS. THEN CREATING THE FINAL OFFSPRINGS LIST WHICH WILL RETURN TO THE MAIN PROGRAM
    
    
    # new list with parents.genes to easily check if offsprings match initial parents
    parents_genes_int = []
    
    for i in parents:
        parents_genes_int.append(i.genes)
    
    offsprings_to_keep = [] 
    
    for i in offsprings:
        if i not in offsprings_to_keep:#clear duplicates
            if i not in parents_genes_int:# check for any offsprings that may match any parent and add them to a new the list.
                offsprings_to_keep.append(i)
    
    #check if the final offsprings match any of the parents
    for i in offsprings_to_keep:
        if i in parents_genes_int:
            print("\n-----------THERE IS AN OFFSPRING MATCHING A PARENT!!!\n---------------------")
    
    #check if the final offsprings truly have no duplicates
    for i in range(len(offsprings_to_keep)):
        sublist = offsprings_to_keep[i]
        for j in range(i + 1, len(offsprings_to_keep)):
            if sublist == offsprings_to_keep[j]:
                print("\n-----------THERE IS A DUPLICATE OFFSPRING!!!\n---------------------")
                break
    
    if offsprings_to_keep:
        return offsprings_to_keep
    else:
        return

def mutation(population, gene_mutation_rate):
	mutated_chromosomes = []
	
	for parent in population:
		# Create a deep copy of the parent chromosome
		mutated_parent = copy.deepcopy(parent) #when you create a copy of a list or object, it creates a reference to the original data rather than creating a new independent copy. This means that if you modify the copied variable, the original variable will also be affected.
		
        #roll a number from 0 to 100 for each bit. if it's smaller than the mutation rate, flip the bit
		for i in range(len(mutated_parent)):
			if random.randrange(0, 100) < gene_mutation_rate:
				mutated_parent[i] = 1 - mutated_parent[i]  # Flip the bit
		
		# Check if mutated parent matches any original parent. If not add to the list to return
		if mutated_parent != parent:
			mutated_chromosomes.append(mutated_parent)
			# print(f"Mutated parent is different from original parent.", mutated_parent)
		# else:
			# print(f"Mutated parent matches original parent.", mutated_parent)
	
	if mutated_chromosomes:
		return mutated_chromosomes
	else:
		return

def mutation_2layer(population, gene_mutation_rate, parent_mutation_rate):			
	mutated_chromosomes = []
	
	for parent in population:
		# Create a deep copy of the parent chromosome
		mutated_parent = copy.deepcopy(parent) #when you create a copy of a list or object, it creates a reference to the original data rather than creating a new independent copy. This means that if you modify the copied variable, the original variable will also be affected.
		
        #roll a number from 0 to 100. if it is smaller than parent_mutation_rate, then roll a number for each bit of the chromosome. this is a 2layer mutation mechanic
		if random.randrange(0,100) < parent_mutation_rate:
			for i in range(len(mutated_parent)):
				if random.randrange(0, 100) < gene_mutation_rate:
					mutated_parent[i] = 1 - mutated_parent[i]  # Flip the bit

			# Check if mutated parent matches any original parent
			if mutated_parent != parent:
				mutated_chromosomes.append(mutated_parent)
				# print(f"Mutated parent is different from original parent. mut:", mutated_parent, "original parent:", parent )
			# else:
				# print(f"Mutated parent matches original parent. mut:", mutated_parent, "original parent:", parent)
	
	if mutated_chromosomes:
		return mutated_chromosomes
	else:
		return

def classic_roulette(population):
	total_population_fitness = sum([i.fitness for i in population])#adds fitness values from all input parents together
	total_population_fitness = round(total_population_fitness, 3)#rounds it up
	chromosome_probabilities = [i.fitness/total_population_fitness for i in population]# if we round here, we put a hard cap on the number of the parents' population. This is because as the number of the populationn grows, the probabilities approach zero. So later at cumulative_probabilities = [round(i / cumulative_sum, 4) for i in cumulative_probabilities] we get a division by zero error.
	# print(total_population_fitness,"\n")
	# print(chromosome_probabilities,"\n")
	
	cumulative_probabilities = []
	cumulative_sum = 0.0
	
    #make the probability spaces. each space corresponds to one parent ex. [0.25, 0.5, 0.75, 1.0]
	for i in chromosome_probabilities:
		cumulative_sum += i
		cumulative_probabilities.append(cumulative_sum)

	# Normalize cumulative probabilities to ensure they add up to 1
	cumulative_probabilities = [i / cumulative_sum for i in cumulative_probabilities]# as the number of parents increases probabilities for each become smaller/approach zero, because the probabilities are normalized and sum up to 1. if we round, some of the probabilities number ends up being the same as the number of parents' population increases. if the probabilities become the same the roulette won't function properly
	
	# print(cumulative_probabilities,"\n")
	
    #get a random number
	random_number=round(random.random(), 3)

	# print(random_number,"\n")
    
    #check at which probability space the number falls into. then get the corrsponding parent
	for i in range(len(cumulative_probabilities)):
		if random_number <= cumulative_probabilities[i]:
			return population[i]

def roulette_multiparents_same_parent(population,no_of_parents_returned):
    #check if no_of_parents_returned is greater than population
	if len(population)<no_of_parents_returned:
		print("You can't get more parents than you are providing. Either increase the parents population or decrease the number of parents returned")
		exit()

	total_population_fitness = sum([i.fitness for i in population])#adds fitness values from all input parents together
	total_population_fitness = round(total_population_fitness, 3)#rounds it up
	chromosome_probabilities = [i.fitness/total_population_fitness for i in population]# if we round here, we put a hard cap on the number of the parents' population. This is because as the number of the populationn grows, the probabilities approach zero. So later at cumulative_probabilities = [round(i / cumulative_sum, 4) for i in cumulative_probabilities] we get a division by zero error.
	# print(total_population_fitness,"\n")
	# print(chromosome_probabilities,"\n")
	
	cumulative_probabilities = []
	cumulative_sum = 0.0
	
    #make the probability spaces. each space corresponds to one parent ex. [0.25, 0.5, 0.75, 1.0]
	for i in chromosome_probabilities:
		cumulative_sum += i
		cumulative_probabilities.append(cumulative_sum)

	# Normalize cumulative probabilities to ensure they add up to 1
	cumulative_probabilities = [i / cumulative_sum for i in cumulative_probabilities]# as the number of parents increases probabilities for each become smaller/approach zero, because the probabilities are normalized and sum up to 1. if we round, some of the probabilities number ends up being the same as the number of parents' population increases. if the probabilities become the same the roulette won't function properly
	
	# print(cumulative_probabilities,"\n")

	random_numbers = []

	#generate unique random numbers and add them to a list. this stops when the random numbers generated are more than no_of_parents_returned
	while len(random_numbers) < no_of_parents_returned:
		random_number=round(random.random(), 2)
		random_numbers.append(random_number)
	
	# print("ran:",random_numbers,"\n")
	
	parents_to_return = []

	#check at which cumulative probability range each above random numbers falls in. add corresponding parent to the selected population
	for x in random_numbers:
		for i in range(len(cumulative_probabilities)):
			if x <= cumulative_probabilities[i]:
				parents_to_return.append(population[i])
				break

	if parents_to_return:
		return parents_to_return
	else:
		print("No parents chosen to return")
		return

def roulette_unique_parents(population,no_of_parents_returned):
	#check if no_of_parents_returned is greater than population
	if no_of_parents_returned > len(population):
		print("You can't select more parents than the initially provided population, silly! Either increase the number of parents or decrease the the number of parents requested to return.")
		exit()
	
	total_population_fitness = sum([i.fitness for i in population])#adds fitness values from all input parents together
	total_population_fitness = round(total_population_fitness, 3)#rounds it up
	chromosome_probabilities = [i.fitness/total_population_fitness for i in population] # if we round here, we put a hard cap on the number of the parents' population. This is because as the number of the populationn grows, the probabilities approach zero. So later at cumulative_probabilities = [round(i / cumulative_sum, 4) for i in cumulative_probabilities] we get a division by zero error.
	# print("total_population_fitness:",total_population_fitness,"\n")
	# print("chromosome_probabilities:",chromosome_probabilities,"\n")
	
	cumulative_probabilities = []
	cumulative_sum = 0.0
	
    #make the probability spaces. each space corresponds to one parent ex. [0.25, 0.5, 0.75, 1.0]
	for i in chromosome_probabilities:
		cumulative_sum += i
		cumulative_probabilities.append(cumulative_sum)
	

	# Normalize cumulative probabilities to ensure they add up to 1
	cumulative_probabilities = [i / cumulative_sum for i in cumulative_probabilities]# as the number of parents increases probabilities for each become smaller/approach zero, because the probabilities are normalized and sum up to 1. if we round, some of the probabilities number ends up being the same as the number of parents' population increases. if the probabilities become the same the roulette won't function properly
	
	# print(cumulative_probabilities,"\n")

	#generate random numbers. each number corresponds to one specific cumulative probability range.
	#add the corresponding index of the specific probability range to unique indexes list, as long as the list does not already contain the index
	#use the unique indexes list to bring forth the selected parrents
	unique_indexes = []
	
	while len(unique_indexes) < no_of_parents_returned:
		random_number=round(random.random(), 2)
		for i in range(len(cumulative_probabilities)):
			if random_number <= cumulative_probabilities[i]:
				if i not in unique_indexes:
					unique_indexes.append(i)
				break
				

	#check if the indexes are unique_indexes
	if len(unique_indexes) != len(set(unique_indexes)):
		print("parents_to_return does not contain truly unique indexes")
	
	parents_to_return = []
	
	for i in unique_indexes:
		parents_to_return.append(population[i])
	
	if parents_to_return:
		return parents_to_return
	else:
		print("No parents chosen to return")
		return

def cull_by_percentage(parents, percentage_to_cull, no_of_parents_to_select):
#cull_by_percentage function has to return enough parents to pass the checks of the other functions (crossover and selection). Naturally, crossover cant return more parents than it gets.
#kpc needs at least 2 parents to function. so we put a hard limit to this. if the population is thinned too much, there is a chance less parents will be left for selection.
#so if, for example, 2 parents are left, and we have determined 3 to be chosen at the selection stage, then we get an error.
#Using no_of_parents_to_select we secure this won't happen, because the selection stage gets the same number of parents as the condition to apply or not cull below => if len(next_gen) >= no_of_parents_to_select
    
    sorted_individuals = sorted(parents, key=lambda x: x.fitness, reverse=True)#reverse=True => highest to lowest
    
    next_gen = []
    #turn given percentage to the corresponding number of parents that should be removed
    no_of_parents_removed = math.floor((percentage_to_cull / 100) * len(sorted_individuals))
    print("initial of cull:",len(sorted_individuals))
    print("parents removed:",no_of_parents_removed)
    # print("===============")
    
    if no_of_parents_removed != 0:
        next_gen = sorted_individuals[:len(sorted_individuals)-no_of_parents_removed]#keep all except no_of_parents_removed last individuals
        print("next gen:",len(next_gen))
        if len(sorted_individuals) - len(next_gen) != no_of_parents_removed:
            print("Culling does not remove parents as expected. It is supposed to remove no_of_parents_removed from the bottom of the parents' list and return the rest, but there is a mixup in the calculations within the function")
        if len(next_gen) >= no_of_parents_to_select:#kpc needs at least no_of_parents_to_select parents to function, so we put a hard limit to this.
            return next_gen
		
    else:
        print("total parents", len(sorted_individuals))
        print("parents to remove:",no_of_parents_removed)
        print("If the designated number of offsprings is removed the program will break. No offsprings will be removed")
        return sorted_individuals



#gen0_binary creates lists of genes. 1st is the number of parents created. 2nd is the number of genes for each.
gen0 = gen0_binary(20, 10)

#after gen0_binary, the parents are mere lists of genes. We have to turn them into objects
gen0_objects = []

for i in gen0:
    #i=genes. you can enter any other desired attributes like this. You can also do it for each parent separately
    individual = Chromosome(i, fitness=1, mutation=0.85)
    gen0_objects.append(individual)

for iterator in range(5):
# while True:
    # offs=spc(gen0_objects)

# for i in offs:
    # print(i)

# while True:
    
    # uni=roulette_unique_parents(gen0_objects,3)
    
    offsprings=kpc(gen0_objects, 3)

    offsprings_obj = []

    if offsprings:
        mutated = mutation(offsprings, 20)
        # print("offsprings:",len(offsprings))

        if mutated:
            
            # print("mutated:",len(mutated))
            offsprings = offsprings + mutated
            # print("total:",len(offsprings))

    if offsprings:
        # print(type(offsprings))
        for i in offsprings:
            individual = Chromosome(i, fitness=1, mutation=0.85)
            offsprings_obj.append(individual)

    # print(len(offsprings))
    next_gen=cull_by_percentage(offsprings_obj, 20, 10)
    if next_gen:
        next_gen_obj = []
        for i in next_gen:
            individual = Chromosome(i, fitness=1, mutation=0.85)
            next_gen_obj.append(individual)
        print("before cull:",len(offsprings_obj))
        gen0_objects = next_gen
        print("after cull:",len(gen0_objects))
        print("====================")