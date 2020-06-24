from scipy.stats import trapz
from scipy.stats import halfnorm

def dist_range(start, stop, size=1, b=0.1): # this function has been implemented into already modelling_distributions.py
  """
  get random numbers of size size ib on the basis of start date and end date and trapezoid distribution defined by first turn point (lower bound)
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

def dist_ante_post(date, date_type, size=1, scale=25): # this function has been implemented into already modelling_distributions.py
  """
  get random numbers of size size ib on the basis of start date and end date and trapezoid distribution defined by first turn point (lower bound)
  """
  if "post" in date_type:
    r = halfnorm.rvs(date, scale, size)
    random_values = list(r.astype(int))
  if "ante" in date_type:
    r = halfnorm.rvs(scale=scale, size=size)
    random_values =  list((date - r).astype(int))
  if size == 1:
    return random_values[0]
  else:
    return random_values


def model_date(start, stop, size=1, scale=25, b=0.1):
    try:
      randoms = dist_range(int(start), int(stop), size=size, b=b)
    except:
      try:
        randoms =  dist_ante_post(start, "post", size=size, scale=scale)
      except:
        try:
          randoms =  dist_ante_post(stop, "ante", size=size, scale=scale)
        except:
          randoms = None
    return randoms
