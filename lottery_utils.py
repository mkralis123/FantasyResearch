import copy
import random
import pandas as pd
import time
from playsound import playsound

def draft_sim(tickets, protections):

    temp_tickets = copy.deepcopy(tickets)
    selections = []

    for pick_no in range(1,len(temp_tickets)+1):

        if pick_no in protections:
            if protections[pick_no] not in selections:
                selection = protections[pick_no]
                selections.append(selection)
                temp_tickets.pop(selection)
                continue

        ticket_allotment = []
        for seed in temp_tickets:
            no_tickets = temp_tickets[seed]
            ticket_allotment.extend([seed]*no_tickets)

        rand_selection = random.randint(0,len(ticket_allotment)-1)
        selection = ticket_allotment[rand_selection]
        selections.append(selection)
        temp_tickets.pop(selection)

    return selections

def get_summary_total(sim_results, tickets, isProb = True):
    teams = copy.deepcopy(tickets)
    no_simulations = len(sim_results)
    summary = {}

    for team in teams:
        team_dict = dict(zip(list(range(1,len(teams)+1)),[0]*len(teams)))
        for i in range(no_simulations):
            team_dict[sim_results[i].index(team)+1] += 1
        if isProb:
            team_dict = {f'Pick #{key}' : team_dict[key]/no_simulations for key in team_dict}
        summary[team] = team_dict
    summary = pd.DataFrame.from_dict(summary)

    return summary

def print_draft(tickets,protections,year,next_pick_pause,team_names,play_draft_noise=True,play_music=True):
    simulation_results = draft_sim(tickets,protections)

    if play_draft_noise:
        print(f'COMMENCING THE {year} DYNOSHARKS DRAFT')
    else:
        print('COMMENCING MOCK DRAFT')
    print('\n')

    print(f'THE 6th PICK IN THE {year} DYNOSHARKS DRAFT GOES TO ....')
    print_pick(simulation_results, 6, next_pick_pause, team_names, play_draft_noise, play_music)
    print(f'AND THE 5th PICK IN THE {year} DYNOSHARKS DRAFT GOES TO ....')
    print_pick(simulation_results, 5, next_pick_pause, team_names, play_draft_noise, play_music)
    print(f'AND THE 4th PICK IN THE {year} DYNOSHARKS DRAFT GOES TO ....')
    print_pick(simulation_results, 4, next_pick_pause, team_names, play_draft_noise, play_music)
    print(f'AND THE 3rd PICK IN THE {year} DYNOSHARKS DRAFT GOES TO ....')
    print_pick(simulation_results, 3, next_pick_pause, team_names, play_draft_noise, play_music)
    print(f'AND THE 2nd PICK IN THE {year} DYNOSHARKS DRAFT GOES TO ....')
    print_pick(simulation_results, 2, next_pick_pause, team_names, play_draft_noise, play_music)
    print(f'LAST BUT NOT LEAST, THE 1st PICK IN THE {year} DYNOSHARKS DRAFT GOES TO ....')
    print_pick(simulation_results, 1, next_pick_pause, team_names, play_draft_noise, play_music)
    
def print_pick(sim_results, pick_no, next_pick_pause, names, play_draft_noise=True, play_song=True):
    
    if play_draft_noise:
        playsound('walkoutsongs/nfl-draft-chime.wav')
    print(f'THE {sim_results[pick_no-1]} SEED:', names[sim_results[pick_no-1]])
    
    if play_song:
        team = names[sim_results[pick_no-1]]
        try:
            playsound(f'walkoutsongs/{team}.mp3')
        except:
            playsound('walkoutsongs/womp.mp3')
    else:
        time.sleep(next_pick_pause)
        
    print('\n')