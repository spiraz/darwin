import darwin as dar

#----------initialization of first population-------------------------------

#gen0_binary creates lists of genes. 1st is the number of parents created. 2nd is the number of genes for each.
population = dar.gen0_binary(20, 10)

#10 generations in total
for generation in range(10000):

    #----------selection step----------------------------- 
    selection=dar.roulette_unique_parents(population,10)
    
    # crossover - produce offsprings
    offsprings=dar.kpc(population, 3)

    # mutation
    if offsprings:
        mutated = dar.mutation_binary(offsprings, 20)

        if mutated:
            offsprings = offsprings + mutated

    # cull population
    next_gen=dar.cull_by_percentage(offsprings, 20, 5)
    if next_gen:
        population = next_gen