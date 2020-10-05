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



def get_simulation_variants(dataframe, column):
    """
    combine random dates associated with individual observations
    into a list of simulations
    each simulation consists of a list containing one version of dates
    """
    random_dates_list = dataframe[column].tolist()
    simulations_list = []
    if isinstance(random_dates_list[0], list):
        random_size = len(random_dates_list[0])
    else:
        random_size = len(random_dates_list[1])
    for n in range(random_size):
        simulation = [random_dates[n] for random_dates in random_dates_list if isinstance(random_dates, list)]
        simulations_list.append(simulation)
    return simulations_list


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

def timeblocks_from_randoms(dataframe, column, min_max_step):
  """
  combine get_simulation_variants() and dates_per_block() into one functions
  """
  simulations_list = get_simulation_variants(dataframe, column)
  sim_tup_lists = []
  time_blocks_raw =[(n, n+min_max_step[2]) for n in range(min_max_step[0], min_max_step[1], min_max_step[2])]
  time_blocks = []
  for tup in time_blocks_raw:
    if tup[0]<0:
      time_blocks.append((tup[0], tup[1]-1))
    else:
      time_blocks.append((tup[0] + 1, tup[1]))
  for sim_list in simulations_list:
    sim_tup_list = dates_per_block(sim_list, time_blocks)
    sim_tup_lists.append(sim_tup_list)
  return sim_tup_lists

def plot_timeblocks_data(list_of_timeblocks_data, ax=None, color=None):
  """
  plot timeblocks data as a series of overlapping line plots 
  """
  for timeblocks in list_of_timeblocks_data:
    x = [np.mean(tuptup[0]) for tuptup in timeblocks]
    y = [tuptup[1] for tuptup in timeblocks]
    if ax != None:
        if color != None:
            ax.plot(x, y, color=color)
        else: 
            ax.plot(x, y)
    else:
        if color != None:
            plt.plot(x, y, color=color)
        else: 
            plt.plot(x, y)

def get_aoristic(startdate, enddate, timeblocks_tuples):
    aoristic_probs = {}
    try:
        startdate, enddate = int(startdate), int(enddate)
        ind_year_prob = np.round(1 / len([n for n in range(startdate, enddate)]), 5)
        for timeblock in timeblocks_tuples:
            possibledates = [n for n in range(startdate, enddate)]
            timeblock_range = [n for n in range(timeblock[0], timeblock[1])]
            aoristic_probs[timeblock] = len(set(possibledates) & set(timeblock_range)) * ind_year_prob
    except:
        for timeblock in timeblocks_tuples:
            aoristic_probs[timeblock] = 0
    return aoristic_probs    


def get_aoristic_sum(prob_dicts_list, timeblocks_tuples):
    aoristic_sum = {}
    for timeblock in timeblocks_tuples:
        aoristic_sum[timeblock] =  sum([probs[timeblock] for probs in prob_dicts_list])
    return aoristic_sum
