"""Algorithms module"""
import time
from multiprocessing import Pool

import metapy_toolbox.common_library as metapyco
import metapy_toolbox.simulated_annealing as metapysa
import metapy_toolbox.firefly_algorithm as metapyfa
import metapy_toolbox.genetic_algorithm as metapyga
import metapy_toolbox.differential_evolution as metapyde


def metaheuristic_optimizer(algorithm_setup, general_setup):
    """
    This function is responsible for the metaheuristic optimization process. 
    It is a general function that calls the specific algorithm functions.

    See documentation in https://wmpjrufg.github.io/METAPY/FRA_META_.html

    Args:
        algorithm_setup (Dictionary): Metaheuristic optimization setup. 
                                      See algorithms documentation for more details.
        general_setup (Dictionary): Optimization process setup.
            keys:
                - 'number of repetitions' (Integer): Number of repetitions.
                - 'type code' (String): Type of population. Options: 'real code' or 'combinatorial code'.
                - 'initial pop. seed' (List): Random seed. Use None in list for random seed.
                - 'algorithm' (String): Optimization algorithm. See the available metaheuristic algorithms.
    Returns:
        all_results_per_rep (list): All results for each repetition.
        best_population_per_rep (list): Best population for each repetition.
        reports (list): Reports for each repetition.
        status_procedure (int): Best repetition id.
    """

    try:
        # Check general parameters
        if not isinstance(general_setup, dict):
            raise TypeError('The general_setup parameter must be a dictionary.')

        for key in general_setup.keys():
            if key not in ['number of repetitions', 'type code', 'initial pop. seed', 'algorithm']:
                raise ValueError('The setup parameter must have the following keys:\n- "number of repetitions";\n- "type code";\n- "initial pop. seed";\n- "algorithm";')

        if not isinstance(general_setup['number of repetitions'], int):
            raise TypeError('The number of repetitions parameter must be an integer.')

        if not isinstance(general_setup['type code'], str):
            raise TypeError('The type code parameter must be a string.')

        if not isinstance(general_setup['initial pop. seed'], list):
            raise TypeError('The seed control parameter must be a list.')

        if not isinstance(general_setup['algorithm'], str):
            raise TypeError('The algorithm parameter must be a string.')

        # Check algorithms parameters
        if not isinstance(algorithm_setup['number of iterations'], int):
            raise TypeError('The number of iterations parameter must be an integer.')

        if not isinstance(algorithm_setup['number of population'], int):
            raise TypeError('The number of population parameter must be an integer.')

        if not isinstance(algorithm_setup['number of dimensions'], int):
            raise TypeError('The number of dimensions parameter must be an integer.')

        if not isinstance(algorithm_setup['x pop lower limit'], list):
            raise TypeError('The x pop lower limit parameter must be a list.')

        if not isinstance(algorithm_setup['x pop upper limit'], list):
            raise TypeError('The x pop upper limit parameter must be a list.')

        if len(algorithm_setup['x pop lower limit']) != len(algorithm_setup['x pop upper limit']):
            raise ValueError('The x pop lower limit and x pop upper limit parameters must have the same length.')

        if len(algorithm_setup['x pop lower limit']) != algorithm_setup['number of dimensions'] or len(algorithm_setup['x pop upper limit']) != algorithm_setup['number of dimensions']:
            raise ValueError('The x pop lower limit and x pop upper limit parameters must have \n the exact dimensions length.')

        if not callable(algorithm_setup['objective function']):
            raise TypeError('The objective function parameter must be a py function (def).')

        if not isinstance(algorithm_setup['algorithm parameters'], dict):
            raise TypeError('The algorithm parameters parameter must be a dictionary.')

        # if not isinstance(setup['algorithm'], str):
        #     raise TypeError('The algorithm parameter must be a string.')

        # if setup['algorithm'] not in ['hill_climbing_01', 'simulated_annealing_01', 'gender_firefly_algorithm_01', 'genetic_algorithm_01', 'differential_evolution_algorithm_01']:
        #     raise ValueError('This algorithm is not available. Availability Lists:\n- hill_climbing_01;\n- simulated_annealing_01.\n- gender_firefly_algorithm_01.\n- genetic_algorithm_01.\n-differential_evolution_algorithm_01')

        # if not isinstance(setup['algorithm parameters'], dict):
        #     raise TypeError('The algorithm parameters parameter must be a dictionary.')
        
        
        # if len(setup['seed control']) != setup['number of repetitions']:
        #     raise ValueError('The seed control parameter must have the same length of number of repetitions.')

        # # Check the algorithm parameters
        # if setup['algorithm'] == 'hill_climbing_01':
        #     expected_keys = {'cov (%)', 'pdf'}
        #     algorithm_params_keys = set(setup['algorithm parameters'].keys())

        #     if not expected_keys.issubset(algorithm_params_keys) or len(algorithm_params_keys) != len(expected_keys):
        #         raise ValueError('The algorithm parameters parameter must have 2 keys: sigma and pdf.')

        #     for key in setup['algorithm parameters'].keys():
        #         if key not in ['cov (%)', 'pdf']:
        #             raise ValueError('The algorithm parameters parameter must have the following keys: sigma, pdf.')

        #     if not isinstance(setup['algorithm parameters']['cov (%)'], float):
        #         raise TypeError('The standard deviation parameter must be a float.')

        #     if not isinstance(setup['algorithm parameters']['pdf'], str):
        #         raise TypeError('The probability density function parameter must be a string.')

        # elif setup['algorithm'] == 'simulated_annealing_01':
        #     expected_keys = {'cov (%)', 'pdf', 'temperature', 'temperature update', 'alpha'}
        #     algorithm_params_keys = set(setup['algorithm parameters'].keys())

        #     if not expected_keys.issubset(algorithm_params_keys) or len(algorithm_params_keys) != len(expected_keys):
        #         raise ValueError('The algorithm parameters parameter must have 5 keys: sigma, pdf, temperature, temperature update, alpha.')

        #     if not isinstance(setup['algorithm parameters']['cov (%)'], float):
        #         raise TypeError('The standard deviation parameter must be a float.')

        #     if not isinstance(setup['algorithm parameters']['pdf'], str):
        #         raise TypeError('The probability density function parameter must be a string.')

        #     if not isinstance(setup['algorithm parameters']['temperature'], int):
        #         raise TypeError('The temperature parameter must be a integer.')

        #     if not isinstance(setup['algorithm parameters']['temperature update'], str):
        #         raise TypeError('The annealing schedule parameter must be a string.')

        #     if not isinstance(setup['algorithm parameters']['alpha'], float):
        #         raise TypeError('The alpha parameter must be a float.')

        # Start variables
        initial_time = time.time()
        all_results_per_rep = []
        best_population_per_rep = []
        times_procedure = []
        reports = []

        # Initial population for each repetition
        population = metapyco.initial_pops(general_setup['number of repetitions'],
                                            algorithm_setup['number of population'],
                                            algorithm_setup['number of dimensions'],
                                            algorithm_setup['x pop lower limit'],
                                            algorithm_setup['x pop upper limit'],
                                            general_setup['type code'],
                                            general_setup['initial pop. seed'])

        # Algorithm selection and general results
        if general_setup['algorithm']=='hill_climbing_01':
            # Multiprocess
            with Pool() as p:
                settings = [[algorithm_setup, init_population, general_setup['initial pop. seed'][i]] for i, init_population in enumerate(population)]
                results = p.map_async(func=metapysa.hill_climbing_01, iterable=settings)
                for result in results.get():
                    all_results_per_rep.append(result[0])
                    best_population_per_rep.append(result[1])
                    times_procedure.append(result[2])
                    reports.append(result[3])
        elif general_setup['algorithm']=='simulated_annealing_01':
            # Multiprocess
            with Pool() as p:
                settings = [[algorithm_setup, init_population, general_setup['initial pop. seed'][i]] for i, init_population in enumerate(population)]
                results = p.map_async(func=metapysa.simulated_annealing_01, iterable=settings)
                for result in results.get():
                    all_results_per_rep.append(result[0])
                    best_population_per_rep.append(result[1])
                    times_procedure.append(result[2])
                    reports.append(result[3])
        elif general_setup['algorithm']=='gender_firefly_algorithm_01':
            # Multiprocess
            with Pool() as p:
                settings = [[algorithm_setup, init_population, general_setup['initial pop. seed'][i]] for i, init_population in enumerate(population)]
                results = p.map_async(func=metapyfa.gender_firefly_algorithm_01, iterable=settings)
                for result in results.get():
                    all_results_per_rep.append(result[0])
                    best_population_per_rep.append(result[1])
                    times_procedure.append(result[2])
                    reports.append(result[3])
        elif general_setup['algorithm']=='genetic_algorithm_01':
            # Multiprocess
            with Pool() as p:
                settings = [[algorithm_setup, init_population, general_setup['initial pop. seed'][i]] for i, init_population in enumerate(population)]
                results = p.map_async(func=metapyga.genetic_algorithm_01, iterable=settings)
                for result in results.get():
                    all_results_per_rep.append(result[0])
                    best_population_per_rep.append(result[1])
                    times_procedure.append(result[2])
                    reports.append(result[3])
        # elif general_setup['algorithm']=='differential_evolution_algorithm_01':
        #     # Multiprocess
        #     with Pool() as p:
        #         settings = [[algorithm_setup, init_population, general_setup['initial pop. seed'][i]] for i, init_population in enumerate(population)]
        #         results = p.map_async(func=metapyde.differential_evolution_algorithm_01, iterable=settings)
        #         for result in results.get():
        #             all_results_per_rep.append(result[0])
        #             best_population_per_rep.append(result[1])
        #             times_procedure.append(result[2])
        #             reports.append(result[3])
        # Best results
        status_procedure = metapyco.summary_analysis(best_population_per_rep)
        best_result = best_population_per_rep[status_procedure]
        last_line = best_result.iloc[-1]
        best_of = last_line['OF BEST']
        design_variables = last_line.iloc[:algorithm_setup['number of dimensions']].tolist()

        # Output details
        end_time = time.time()
        print(' Optimization results:', '\n')
        print(' - Best repetition id:   ', status_procedure)
        print(' - Best of:               {:.10e}'.format(best_of))
        print(' - Design variables:     ', design_variables)
        print(' - Process time (s):      {:.6f}'.format(end_time - initial_time))
        print(' - Best process time (s): {:.6f}'.format(times_procedure[status_procedure]))

        return all_results_per_rep, best_population_per_rep, reports, status_procedure

    except TypeError as te:
        print(f'Error: {te}')

    except ValueError as ve:
        print(f'Error: {ve}')

    return None, None, None, None