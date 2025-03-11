from . import global_def
from nonebot import logger

group_guess_game = {}
draw_card_record = {}

def test_barrier(group_id: str) -> bool:
    if group_id in global_def.test_group_id:
        return True
    
    return False

def accept_group_barrier(group_id: str) -> bool:
    if group_id in global_def.accept_group_id:
        return True
    
    return False