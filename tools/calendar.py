from datetime import date, timedelta
from datetime import datetime
import random

def _get_fly_days(start,stop):
    """Takes start and stop as lists of the format [year:int, month:int, day:int]
    returns a list of tuples with datetime objects for each weekend inbetween
    start and stop like this [(saturday:datetime, sunday:datetime),(saturday:datetime, ...)]"""

    assert len(start) == len(stop) == 3, f'The two input lists must be formatted like this [year:int, month:int, day: int]. You submitted {start} and {stop}.'
    #assert all INT and so on...

    start_of_season = date(*start)
    end_of_season = date(*stop)

    diff = end_of_season - start_of_season

    fly_days = []

    for i in range(diff.days):
        sa = start_of_season + timedelta(i)
        if sa.weekday() == 6:
            so = sa + timedelta(1)
            #wochenenden.append((sa, so)) # One Windenfahrer for each weekend
            fly_days += [sa, so] # One Windenfahrer for each day of the weekend
    return fly_days

def make_example_set_of_assigned_fly_days():
    """Creates an example set of assigned fly days.
    No inputs.
    Outputs a tuple (assigned_weekends_named, windenfahrer)"""
    weekends = _get_fly_days([2019,3,1],[2019,10,1])
    namen = 'Hans Peter Jürgen Jan Erhard Werner Seppi Julian Rainer'.split(' ')

    def create_windenfahrer(name,weekends):
        cant = random.choice(range(len(weekends)-2))
        unavaliable_days = random.choices(weekends,k=cant)
        name = random.choice(namen) + str(cant)
        return {
            'name':name,
            'assigned':[],
            'not_avaliable':unavaliable_days,
               }
    windenfahrer = [create_windenfahrer(name=idx,weekends=weekends) for idx in range(20)]
    weekend_str = [we.strftime("%Y-%m-%d") for we in weekends]
    return assign_fly_days(weekend_str,windenfahrer)

def assign_fly_days(weekends,windenfahrer):
    """Takes a list of weekend-tuples and a list of windenfahrer-objects.
    Returns a list of assigned-weekend-tuples and an updated list of windenfahrer-objects.
    """

    #Parameters for while loop to find a solution, with maximum number of attempts
    double_assignment = True
    iter_count = 0
    max_iter_count = 50

    while double_assignment:
        double_assignment = False
        num_assignments = [len(wi['assigned']) for wi in windenfahrer]
        num_max_assignments = -1
        if not (max(num_assignments) == min(num_assignments)):
            num_max_assignments = max(num_assignments)
        avaliable_windenfahrer = [idx for idx, wi in enumerate(windenfahrer) if not len(wi['assigned'])==num_max_assignments]
        avaliable_windenfahrer_next_round = [x for x in range(len(windenfahrer))]
        we_idx = [x for x in range(len(weekends))]
        we_cant = [(idx,[wf_idx for wf_idx, wf in enumerate(windenfahrer) if weekends[idx] in wf['not_avaliable']]) for idx in we_idx]
        we_cant.sort(key = lambda x: len(x[1]),reverse=True)
        assigned_weekends = []
        for we in we_cant:
            we_idx, list_wf_cant_idx = we
            try:
                selected_windenfahrer_idx = random.choice(list(set(avaliable_windenfahrer)-set(list_wf_cant_idx)))
            except:
                try:
                    selected_windenfahrer_idx = random.choice(list(set(avaliable_windenfahrer_next_round)-set(list_wf_cant_idx)))
                except:
                    if not iter_count >= max_iter_count:
                        double_assignment = True
                        iter_count += 1
                        print(f'Could not find match, starting iteration {iter_count}')
            assigned_weekends.append((weekends[we_idx],windenfahrer[selected_windenfahrer_idx]))
            try:
                del avaliable_windenfahrer[avaliable_windenfahrer.index(selected_windenfahrer_idx)]
            except:
                double_assignment = True
            if len(avaliable_windenfahrer) == 0:
                avaliable_windenfahrer = avaliable_windenfahrer_next_round
                avaliable_windenfahrer_next_round = [x for x in range(len(windenfahrer))]

    if iter_count == max_iter_count:
        raise ValueError(f'Still found no solution aufter {max_iter_count} iterations... please try manually.')

    assigned_weekends.sort(key=lambda x: x[0])

    assigned_weekends_named = []
    for we in assigned_weekends:
        we, wi = we
        windenfahrer[windenfahrer.index(wi)]['assigned'].append(we)
        assigned_weekends_named.append((we,wi['name']))
    unassigned_next_round = [windenfahrer[wi] for wi in avaliable_windenfahrer]

    return (assigned_weekends_named, windenfahrer)
