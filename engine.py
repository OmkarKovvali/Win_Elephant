import copy

def get_valid_moves(state):
    curr = state.current_player_idx
    valid_moves = []
    for gift in state.gifts:
        if not gift.is_open:
            valid_moves.append(('open',gift.id))
        elif gift.is_open and (gift.owner_index != -1 and gift.owner_index != curr) and (gift.is_dead == False) and (gift.id != state.last_stolen_gift_id):
            valid_moves.append(('steal',gift.id))
    return valid_moves


def apply_move(state, move):
    new_state = copy.deepcopy(state)
    cp_idx = new_state.current_player_idx
    curr_player = new_state.players[cp_idx]

    action, gift_id = move
    target_gift = None
    for gift in new_state.gifts:
        if gift.id == gift_id:
            target_gift = gift
            break
    if action == 'open':
        target_gift.is_open = True
        curr_player.held_gift = target_gift
        target_gift.owner_index = cp_idx
        
        #passing turn to next person
        new_state.round_player_idx +=1
        new_state.current_player_idx = new_state.round_player_idx
        new_state.last_stolen_gift_id = None

    elif action == 'steal':
        
        victim_idx = target_gift.owner_index

        
        new_state.players[target_gift.owner_index].held_gift = None
        curr_player.held_gift = target_gift
        target_gift.owner_index = cp_idx
        target_gift.record_steal()

        new_state.current_player_idx = victim_idx

        new_state.last_stolen_gift_id = gift_id

    return new_state


    

