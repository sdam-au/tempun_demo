from scipy.stats import trapz
from scipy.stats import halfnorm

def dist_range(start, stop, size=1, b=0): 
    """
    get random numbers of size = size on the basis of a start date and an end date
    by default: uniform distribution
    by specifying b parameter you get a trapezoidal distribution defined by the first turning point (lower bound)
    """
    r = trapz.rvs(b, 1-b, size=size)
    duration = abs((start)-stop)
    if duration == 0:
        random_values = [start] * size
        return random_values
    else:
        random_values = list(((r * duration) + start).round().astype(int))
    if size == 1: # if only one number, return it as a number
        return random_values[0]
    else: # otherwise return a list of values
        return random_values

def dist_ante_post(date, date_type, size=1, scale=50): # this function has been already implemented into modelling_distributions.py
    """
    get random numbers of size size ib on the basis of start date and end date and trapezoid distribution defined by first turn point (lower bound)
    """
    if "post" in date_type:
        r = halfnorm.rvs(date, scale, size)
        random_values = list(r.astype(int))
    if "ante" in date_type:
        r = halfnorm.rvs(scale=scale, size=size)
        random_values =  list((date - r).astype(int))
    if 0 in random_values:
        random_values_without_0 = []
        for value in random_values:
            if value < 0:
                random_values_without_0.append(value)
            else:
                random_values_without_0.append(value + 1)
        random_values = random_values_without_0
    if size == 1:
        return random_values[0]
    else:
        return random_values


def model_date(start, stop, size=1, scale=25, b=0):
    """
    combine dist_range() and dist_ante_post()
    """
    try:
        randoms = dist_range(int(start), int(stop), size=size, b=b)
    except:
        try:
            randoms =  dist_ante_post(int(start), "post", size=size, scale=scale)
        except:
            try:
                randoms =  dist_ante_post(int(stop), "ante", size=size, scale=scale)
            except:
                randoms = None
    return randoms



def get_simulation_variants(dataframe, column, random_size=100):
    """
    combine random dates associated with individual observations
    into a list of simulations
    each simulation consists of a list containing one version of dates
    """
    random_dates_list = dataframe[column].tolist()
    simulations_list = []
    if random_size==None:
        if isinstance(random_dates_list[0], list):
            random_size = len(random_dates_list[0])
        else:
            random_size = len(random_dates_list[1])
    for n in range(random_size):
        simulation = [random_dates[n] for random_dates in random_dates_list if isinstance(random_dates, list)]
        simulations_list.append(simulation)
    return simulations_list


def get_timeblocks(start, stop, step):
    time_blocks_raw =[(n, n+step) for n in range(start, stop, step)]
    time_blocks = []
    for tup in time_blocks_raw:
        if tup[0]<0:
            time_blocks.append((tup[0], tup[1]-1))
        else:
            time_blocks.append((tup[0] + 1, tup[1]))
    return time_blocks

def dates_per_block(list_of_dates, time_blocks):
  """
  count number of dates from a simulation within prespecified time blocks
  time blocks are defined as three-element list: [startdate, enddate, timestep]
  """
  dates_per_block = []
  dates_array = np.array(list_of_dates)
  for tup in time_blocks:
     dates_per_block.append((tup, len(dates_array[(dates_array >= tup[0]) & (dates_array <= tup[1])])))
  return dates_per_block

def timeblocks_from_randoms(dataframe, column, time_blocks, random_size=100):
  """
  combine get_simulation_variants() and dates_per_block() into one functions
  """
  simulations_list = get_simulation_variants(dataframe, column, random_size)
  sim_tup_lists = []
  if isinstance(time_blocks[0], int): # if first entry of timeblocks is not an integer (what indicates, that the input is a list of predefined timevlocks:
      time_blocks = get_timeblocks(time_blocks[0], time_blocks[1], time_blocks[2])
  for sim_list in simulations_list:
    sim_tup_list = dates_per_block(sim_list, time_blocks)
    sim_tup_lists.append(sim_tup_list)
  return sim_tup_lists

### PLOTTING TIMEBLOCKS DATA

def get_min_max_conf(sim_data, conf_int):
    min_max_conf = []
    for tb_n in range(len(sim_data[0])):
        tb_all_results = [sim[tb_n][1] for sim in sim_data]
        tb_all_results = sorted(tb_all_results)
        conf_int_d = (100 - conf_int) / 2 / 100
        conf_index = int(conf_int_d * len(sim_data))
        min_max_conf.append([tb_all_results[0], tb_all_results[-1], tb_all_results[conf_index], tb_all_results[-conf_index]])
    ys_min = [el[0] for el in min_max_conf]
    ys_max = [el[1] for el in min_max_conf]
    ys_conf_min = [el[2] for el in min_max_conf]
    ys_conf_max = [el[3] for el in min_max_conf]
    xs = [np.mean(el[0]) for el in sim_data[0]]
    return [xs, ys_min, ys_max, ys_conf_min, ys_conf_max]

def plot_timeblocks_data(sim_data, ax=None, color="black", **kwargs):
    """
    plot timeblocks data with confidence intervals 
    """
    if ax == None:
        fig, ax = plt.subplots()
    plot_data = get_min_max_conf(sim_data, 90)
    layers = []
    x = plot_data[0]
    layers.append(ax.fill(x + x[::-1], plot_data[1] +  plot_data[2][::-1], color="gray", alpha=0.5))
    layers.append(ax.fill(x + x[::-1], plot_data[3] +  plot_data[4][::-1], color=color, **kwargs))
    return layers

def plot_timeblocks_data_lines(list_of_timeblocks_data, ax=None, color=None):
  """
  plot timeblocks data as a series of overlapping line plots 
  """
  layers = []
  for timeblocks in list_of_timeblocks_data:
    x = [np.mean(tuptup[0]) for tuptup in timeblocks]
    y = [tuptup[1] for tuptup in timeblocks]
    if ax != None:
        if color != None:
            layer = ax.plot(x, y, color=color)
        else: 
            layer = ax.plot(x, y)
    else:
        if color != None:
            layer = plt.plot(x, y, color=color)
        else: 
            layer = plt.plot(x, y)
    layers.append(layer)
  return layers

### AORISTIC ANALYSIS

def get_aoristic(startdate, enddate, timeblocks_tuples):
    """calculate aorisitc probabilities for individual observation"""
    aoristic_probs = {}
    try:
        startdate, enddate = int(startdate), int(enddate)
        ind_year_prob = np.round(1 / len([n for n in range(startdate, enddate + 1)]), 5) # probability for each individual year
        for timeblock in timeblocks_tuples:
            possibledates = [n for n in range(startdate, enddate + 1)]
            timeblock_range = [n for n in range(timeblock[0], timeblock[1] + 1)]
            aoristic_probs[timeblock] = np.round(len(set(possibledates) & set(timeblock_range)) * ind_year_prob, 5)
    except:
        for timeblock in timeblocks_tuples:
            aoristic_probs[timeblock] = 0
    return aoristic_probs    


def get_aoristic_sum(prob_dicts_list, timeblocks_tuples):
    """summarize aoristic data for individual observations"""
    aoristic_sum = {}
    for timeblock in timeblocks_tuples:
        aoristic_sum[timeblock] =  np.round(sum([probs[timeblock] for probs in prob_dicts_list]), 5)
    return aoristic_sum

### SIM BY FUNTION

def get_date_from_randoms(value, n):
    """extract individual date on the basis of index
    (used in sim_data_by_function)"""
    try:
        return value[n]
    except:
        return None

def sim_data_by_function(df, n_sims, time_blocks, function, *args, random_dates_column="random_dates"):
    """
    retrieve simulation variants from random dates
    params:
        df : dataframe containing column with random dates (by default, named "random_dates")
        n_sims : number of simulation to produce (lower than- or equeal to the length "random_dates" array)
        timeblocks : list or tuple specifying startdate, enddate and steps of the timeblocks (e.g. "[-200, 600, 100]")
        function : any function taking a dataframe as its first and main input, using it for some computation (e.g. total number of words in certain column), and returning a numerical output
        *args : additional arguments to be used by the function
        random_dates_column : column containing the preassigned random dates 
    returns:
        list of simulation data of `n_sims` length
    """
    complete_sim_data = []
    for n in range(n_sims):
        sim = df[random_dates_column].apply(lambda x: get_date_from_randoms(x, n))
        sim_data = []
        if isinstance(time_blocks[0], int): # if first entry of timeblocks is an integer it means that it is actually not a timeblock, but only the starting date of the first timeblock
            time_blocks = get_timeblocks(time_blocks[0], time_blocks[1], time_blocks[2])
        for tb in time_blocks:
            mask = sim.between(tb[0], tb[1])
            df_tb = df[mask]
            function_output = function(df_tb, *args)
            sim_data.append((tb, function_output))
        complete_sim_data.append(sim_data)
    return complete_sim_data
