# Darwin

Darwin is a collection of independent, autonomous Python functions that can be combined to build a complete genetic algorithm (GA). Each function is designed to operate independently, offering flexibility, configurability, and scalability while addressing each fundamental component of the genetic algorithm workflow.

## What Is a Genetic Algorithm?

Genetic algorithms are optimization and search techniques inspired by Charles Darwin's theory of evolution by natural selection.

In nature, individuals within a population share common characteristics but differ in the degree to which they express particular traits. Individuals with traits that improve their chances of survival and reproduction are more likely to pass those traits on to subsequent generations. Over time, these advantageous traits become more prevalent within the population, gradually driving adaptation and evolution.

Genetic algorithms apply this principle to computational problems. A population of candidate solutions evolves over successive generations through processes such as selection, crossover, and mutation. By favoring better-performing solutions while maintaining genetic diversity, a GA progressively explores the solution space in search of increasingly optimal results.

## Project Background

Darwin is a simplified, generalized rework of the software originally developed for my master's thesis, *"Exploring Cryptographic Boolean Functions Using Genetic Algorithms."*

The original implementation has been adapted for broader, more generic use, with an emphasis on modularity and flexibility.

## How to use each function



# gen0_binary(population_number, genes_no)

E.x.

Generate 10 individuals with 20 binary genes each. Returns the individuals as a list. Each element is an object. The genes are also a list, accessed by the gene attribute.
population=gen0_binary(10, 20)
print(population[0].genes)


All functions from now on accept and return a list of objects, unless otherwise stated. Each object has a genes attribute which should hold the list of the genes. All functions also contain duplicate checks so they produce unique offsprings unless stated.

# spc(population)

Single point crossover. Slices parents in pieces of 2. Joins them together to create new offsprings.

offsprings=spc(population)
print(offsprings[0].genes)

# kpc(parents,crossover_points_number)

K-point crossover. Here, the caller selects in how many pieces the parents will be sliced to produce the offsprings.

E.x.
offsprings=kpc(population,10)
print(offsprings[0].genes)

Slice the parents in 10 points. The indexes are decided randomly. The same indexes are used for each parents. If each individual has let's say 30 genes(list), kpc will decide 10 indexes within that range and slice every parent
at the exact same index. So, all the parents pieces have the same length. If one parent happens to be longer than the others, its last piece will also be longer.

E.x
print(len(parents[0].genes))=10
print(len(parents[1].genes))=15

offsprings=kpc(population,3)
Let's say the chosen indexes are 3, 6, 9.

parent[0] will be cut into 4 pieces on the following indexdes: 0-3,4-6,7-9,10.
parent[1] will be cut into 4 pieces on the following indexdes: 0-3,4-6,7-9,10-14 because it's longer than the first one.


# mutation_binary(population, gene_mutation_rate)

mutations=mutation_binary(population, 70)

The function is suppossed to be applied on bits, not characters or other numbers. gene_mutation_rate applies to each gene/bit specifically and can be a float between 0 and 100. The function rolls for a number between 0 and 100. If it's smaller than the number of gene_mutation_rate, the corresponding bit is flipped. If any mutations happen that do not match already existing individuals, they are returned in a list.

# mutation_2layer_binary(population, gene_mutation_rate, parent_mutation_rate)

Same as above but there are two percentages rolled here. First, parent_mutation_rate is checked. If the caller has provided let's say 70 and the functons rolls for 45, the function then proceeds in the same operation as above.
Essentially, a first check happens for each parent to see if the program will move on the actual mutation operation.

mutations=mutation_2layer_binary(population, 30, 45)



Roulettes are one of the basic mechanisms for selecting which individuals will provide offsprings. Inidividuals with better fitness have more chances of being selected. I provide 3 different variations.

# classic_roulette(population)

selection=classic_roulette(population)

Returns 1 individual(object)

# roulette_multiparents_same_parent(population,no_of_parents_returned)

Returns a list of parents(objects) equal to the number passed in no_of_parents_returned. A parent can be chosen more than once.

selection=roulette_multiparents_same_parent(population,3)

# roulette_unique_parents(population,no_of_parents_returned)

Returns a list of parents(objects) equal to the number of passed in no_of_parents_returned. Parents chosen are unique.

selection=roulette_unique_parents(population,3)

# cull_by_percentage(parents, percentage_to_cull, no_of_minimum_parents_to_keep)

next_generation=cull_by_percentage(parents, 50, 5)

This function culls the current population to create the next generation. It accepts the population, the percentage of parents to be culled and a threshold value. If the parents passed are 8 and you chose a percentage to be culled 50, then that means that 4 of them should go. But if you have set no_of_minimum_parents_to_keep to 5, then no culling will happen, as that would bring the culled population/next generation under the threshold vvalue of 4. This is a very important check and culling's no_of_minimum_parents_to_keep is supposed to work in conjuction with whatever selection you use. The selection method (kpc, spc or some other) should require equal to or less parents than culling's no_of_minimum_parents_to_keep, otherwise the function will throw a message.

# fitness

You will have to implement your own fitness calculation method.