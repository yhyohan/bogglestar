
import json
import uuid
import time
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from boggle.apps.core import VALID_WORDS, board
from boggle.apps.core.models import Game, GameSerializer, GAMES

TIMEOUT = 300

@csrf_exempt
@require_http_methods(["POST"])
def game(request):
    # game_id = uuid.uuid4().hex[:10]

    if len(GAMES) >= 10**6:
        # TODO: attempt purge
        response = {'error': 'Unable to create a new game. Please try again later.'}
        return JsonResponse(response)

    # if not game_id:
    #     response = {'error': 'Unable to create a new game. Please try again later.'}
    #     return JsonResponse(response)

    # board_file = request.FILES.get('board')
    #
    # if board_file:
    #     board_text = board_file.read().decode()
    #     # track the game is using different board, and needs to be solved rather than using cached results

    g = Game()
    g.start(board)
    g.save()

    game_data = GameSerializer(g).data

    # import pprint
    # pprint.pprint(GAMES)

    response = {'data': game_data, 'message': 'Good luck playing Boggle!'}

    return JsonResponse(response)

@csrf_exempt
@require_http_methods(["POST"])
def game_dtl(request, id):
    data = json.loads(request.body.decode('utf-8'))
    message = None

    action = data.get('action')

    g = Game.get(id)

    if not g:
        response = {'error': 'Game not found!'}
        return JsonResponse(response)

    if not action:
        response = {'error': 'Action not recognized!'}
        return JsonResponse(response)

    if action.upper() == 'END':
        g.end()

    elif action.upper() == 'GUESS':
        time_now = time.time()

        if not g.active:
            message = 'Game already over!'

        elif time_now - g.gametime >= TIMEOUT:
            g.end()
            message = 'Game already over!'

        else: # ongoing game
            answers = data.get('answers', [])
            add_score = 0

            invalid_words = set()
            found_words = set()
            new_words = set()

            if isinstance(answers, str):
                answers = [answers]

            answers = list(map(str.upper, answers))

            # Classify each attempted answer -> new correct answer, had been found, or invalid
            for answer in answers:
                if answer in VALID_WORDS:
                    if answer not in g.found_words:
                        new_words.add(answer)
                    else:
                        found_words.add(answer)
                else:
                    invalid_words.add(answer)

            message_list = []

            if new_words:
                g.found_words.update(new_words)
                g.update_score()
                message_list.append("Congratulations! You guessed correctly for {}.".format(", ".join(new_words)))
            if found_words:
                message_list.append("You already guessed correctly for {}.".format(", ".join(found_words)))
            if invalid_words:
                message_list.append("Invalid answers for {}.".format(", ".join(invalid_words)))

            message = " ".join(message_list)

    game_data = GameSerializer(g).data

    # import pprint
    # pprint.pprint(GAMES)

    response = {'data': game_data}
    if message: response['message'] = message

    return JsonResponse(response)

def gamestats(request):
    return JsonResponse(json.dumps(str(GAMES)), safe=False)
