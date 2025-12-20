class Gift:
    def __init__(self,value,name,id):
        self.value = value
        self.id = id
        self.name = name
        self.steal_count = 0
        self.is_dead = False
        self.is_open = False
        self.owner_index = -1
    
    def record_steal(self):
        self.steal_count +=1
        if self.steal_count >= 3:
            self.is_dead = True

class Player:
    def __init__(self,player_id):
        self.id = player_id
        self.held_gift = None

class GameState:
    def __init__(self,players,gifts):
        self.players = players
        self.gifts = gifts
        
        self.current_player_idx = -1
        self.round_player_idx = -1
        self.last_stolen_gift_id = None
         