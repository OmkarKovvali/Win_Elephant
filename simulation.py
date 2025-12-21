import random
import engine

def evaluate_state(state,player_id):
    # Goal for method is to find a player object that matches hero_id
    if !(state.players[player_id].held_gift):
        return 0
    else:
        return state.players[player_id].held_gift.value

def greedy_move(state):
    valid_moves = engine.get_valid_moves(state)
    if not valid_moves:
        return None

    best_move = None
    best_value = -1.0

    # Simple heuristic:
    # Value of 'steal' = Known Value of the gift
    # Value of 'open' = Estimated Average (e.g. 5.0)
    AVERAGE_WRAPPED_VALUE = 5.0

    for move in valid_moves:
        action, gift_id = move
        current_val = 0.0
        
        if action == 'open':
            current_val = AVERAGE_WRAPPED_VALUE
        elif action == 'steal':
            # Find the gift to get its value
            for g in state.gifts:
                if g.id == gift_id:
                    current_val = g.value
                    break
        
        # Greedy check
        if current_val > best_value:
            best_value = current_val
            best_move = move
            
    # Fallback: if moves have equal value (e.g. all 5.0), pick random to vary simulations
    if best_move is None: 
        return random.choice(valid_moves)
        
    return best_move

def simulate_game(state):
    """
     plays out the game to completion using greedy opponents.
    """
    # Clone is NOT needed here because we pass a clone INTO this function from monte_carlo
    # But if we want to be safe, we can just let 'state' mutate since it's a throwaway simulation
    
    sim_state = state # We will mutate this object directly for speed
    
    # Loop until the round counter exceeds the number of players
    # (Assuming standard game ends when everyone has had a turn)
    while sim_state.round_player_idx < len(sim_state.players):
        
        # Get decision for current player
        move = greedy_move(sim_state)
        
        if move:
            sim_state = engine.apply_move(sim_state, move)
        else:
            # No valid moves? (Shouldn't happen in standard game, but good safety)
            break
            
    return sim_state


def monte_carlo(current_state, hero_id, iterations=1000):
    """
    Runs N simulations for EACH valid move the Hero can make.
    Returns the best move tuple.
    """
    hero_moves = engine.get_valid_moves(current_state)
    if not hero_moves:
        return None
        
    results = {} # Map move -> average_score

    print(f"Analyzing {len(hero_moves)} possible moves with {iterations} sims each...")

    for move in hero_moves:
        total_score = 0.0
        
        for _ in range(iterations):
            # 1. Branch: Apply the Hero's specific move
            # Note: apply_move creates a DEEP COPY, so current_state is safe
            next_state = engine.apply_move(current_state, move)
            
            # 2. Simulate: Play the rest of the game out
            final_state = simulate_game(next_state)
            
            # 3. Score: How did the Hero do?
            score = evaluate_state(final_state, hero_id)
            total_score += score
            
        avg_score = total_score / iterations
        results[move] = avg_score
        print(f"  Move {move}: Expected Value = {avg_score:.2f}")

    # Find the move with the highest average score
    best_move = max(results, key=results.get)
    return best_move

