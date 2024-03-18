from typing import Callable, Tuple, List

from esi.models import Token

from .provider import esi
from .tasks import move_fleet_member
from .models import ResetButton


def move_fleet_members(token: Token, destination_squad_id: int, destination_wing_id: int, fleet_id: int, check_func: Callable[[dict], bool]):
    fleet_members = (
        esi.client
        .Fleets
        .get_fleets_fleet_id_members(
            fleet_id=fleet_id,
            token=token.valid_access_token()
        )
        .results()
    )

    for member in fleet_members:
        if check_func(member):
            move_fleet_member.apply_async(
                kwargs={
                    'fleet_id': fleet_id,
                    'member_id': member['character_id'],
                    'squad_id': destination_squad_id,
                    'wing_id': destination_wing_id,
                    'token_pk': token.pk,
                },
                priority=1,  # Almost highest priority
            )
