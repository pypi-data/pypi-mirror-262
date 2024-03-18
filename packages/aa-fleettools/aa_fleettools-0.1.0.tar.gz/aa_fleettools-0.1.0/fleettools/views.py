import re

from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache

from allianceauth.services.hooks import get_extension_logger

from esi.decorators import token_required
from esi.models import Token
from bravado.exception import HTTPNotFound

from .provider import esi
from .forms import SquadDestinationForm
from .models import ResetButton
from .utils import move_fleet_members

logger = get_extension_logger(__name__)

FLEET_STRUCTURE_CACHE_TIMEOUT = 60 * 60  # 60 minutes
FLEET_STRUCTURE_CACHE_PREFIX = 'fleet_structure'


@login_required
def index(request):
    return redirect('fleettools:fleetmoverlogin')


@login_required
@token_required(scopes=['esi-fleets.read_fleet.v1', 'esi-fleets.write_fleet.v1'])
def fleetmoverlogin(request, token: Token):
    return redirect('fleettools:fleetmover', token_pk=token.pk)


@login_required
def fleetmover(request, token_pk: int):
    token = get_object_or_404(Token, pk=token_pk)
    if token.user != request.user:
        return redirect('fleettools:fleetmoverlogin')

    if request.method == 'POST':
        wings = set()
        squads = set()

        if 'move-fleet' in request.POST and request.POST['move-fleet'] == 'on':
            move_fleet = True
        else:
            move_fleet = False
            wing_regex = re.compile(r'^wing-(?P<wing_id>\d+)$')
            squad_regex = re.compile(r'^squad-(?P<squad_id>\d+)$')

            for key, value in request.POST.items():
                if wing_regex.match(key) is not None and value == 'on':
                    wing_id = wing_regex.match(key).group('wing_id')
                    wings.add(int(wing_id))
                elif squad_regex.match(key) is not None and value == 'on':
                    squad_id = squad_regex.match(key).group('squad_id')
                    squads.add(int(squad_id))

        fleet_id = request.POST['fleet_id']

        squads_choices = cache.get(f"{FLEET_STRUCTURE_CACHE_PREFIX}-{token_pk}")
        if squads_choices is None:
            try:
                fleet_structure = (
                    esi.client
                    .Fleets
                    .get_fleets_fleet_id_wings(
                        fleet_id=fleet_id,
                        token=token.valid_access_token()
                    )
                    .results()
                )
            except HTTPNotFound:
                messages.error(request, 'You are not in a fleet or you are not its boss')
                return redirect('authentication:dashboard')

            squads_choices = [
                (f"{wing['id']}-{squad['id']}", f"{wing['name']} -> {squad['name']}") for wing in fleet_structure for squad in wing['squads']
            ]

        destination_form = SquadDestinationForm(
            squads_choices,
            request.POST,
        )

        if not destination_form.is_valid():
            messages.error(request, 'Invalid form data.')
            return redirect('fleettools:fleetmover', token_pk=token_pk)

        destination = destination_form.cleaned_data['squad_destination']

        wing_id, squad_id = destination.split('-')

        move_fleet_members(
            token,
            int(squad_id),
            int(wing_id),
            int(fleet_id),
            lambda member: move_fleet or member['wing_id'] in wings or member['squad_id'] in squads
        )

        messages.success(request, 'Fleet updated successfully.')
        return redirect('fleettools:fleetmover', token_pk=token_pk)

    fleet_info = (
        esi.client
        .Fleets
        .get_characters_character_id_fleet(
            character_id=token.character_id,
            token=token.valid_access_token()
        )
        .results()
    )

    try:
        fleet_structure = (
            esi.client
            .Fleets
            .get_fleets_fleet_id_wings(
                fleet_id=fleet_info['fleet_id'],
                token=token.valid_access_token()
            )
            .results()
        )
    except HTTPNotFound:
        messages.error(request, 'You are not in a fleet or you are not its boss')
        return redirect('authentication:dashboard')

    squads_choices = [
        (f"{wing['id']}-{squad['id']}", f"{wing['name']} -> {squad['name']}") for wing in fleet_structure for squad in wing['squads']
    ]

    cache.set(f"{FLEET_STRUCTURE_CACHE_PREFIX}-{token_pk}", squads_choices, FLEET_STRUCTURE_CACHE_TIMEOUT)

    destination_form = SquadDestinationForm(squads=squads_choices)

    destinations = {
        (wing['id'], squad['id']): squad['name']
        for wing in fleet_structure
        for squad in wing['squads']
        if ResetButton.objects.filter(wing_name=wing['name'], squad_name=squad['name']).exists()
    }

    reset_buttons = [
        [
            {
                'url': resolve_url(
                    'fleettools:buttonmover',
                    token_pk=token_pk,
                    fleet_id=fleet_info['fleet_id'],
                    wing_id=wing['id'],
                    squad_destination_id=destination_squad,
                    wing_destination_id=destination_wing
                ),
                'text': f"Reset {wing['name']} to {squad_name}",
            } for wing in fleet_structure
        ] for (destination_wing, destination_squad), squad_name in destinations.items()
    ]

    context = {
        'fleet': fleet_structure,
        'fleet_id': fleet_info['fleet_id'],
        'destination_form': destination_form,
        'reset_buttons': reset_buttons,
    }

    return render(request, 'fleettools/fleetmover.html', context=context)


@login_required
def buttonmover(request, token_pk: int, fleet_id: int, wing_id: int, squad_destination_id: int, wing_destination_id: int):
    token = get_object_or_404(Token, pk=token_pk)
    if token.user != request.user:
        return redirect('fleettools:fleetmoverlogin')

    move_fleet_members(
        token,
        squad_destination_id,
        wing_destination_id,
        fleet_id,
        lambda member: member['wing_id'] == wing_id
    )

    messages.success(request, 'Fleet updated successfully.')
    return redirect('fleettools:fleetmover', token_pk=token_pk)
