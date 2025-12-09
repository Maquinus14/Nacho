from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Game

@login_required
def game_list(request):
    games = Game.objects.all()
    return render(request, 'games/list.html', {'games': games})

@login_required
def create_game(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        
        if Game.objects.filter(room_name=room_name).exists():
            messages.error(request, 'Room name already exists.')
            return redirect('games:game_list')
        
        game = Game.objects.create(
            room_name=room_name,
            owner=request.user,
            board=' ' * 9,
            active_player=1,
            game_state='active'
        )
        
        return redirect('games:game_detail', game_id=game.id)
    
    return redirect('games:game_list')

@login_required
def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    
    # CAMBIO 1: Permitir que otro usuario se una como player2
    if not game.player2 and request.user != game.owner:
        game.player2 = request.user
        game.save()
    
    if request.method == 'POST':
        # CAMBIO 2: Verificar quién puede jugar
        # Ahora pueden jugar: owner (player1) o player2
        if request.user not in [game.owner, game.player2]:
            messages.error(request, 'You are not a player in this game.')
            return redirect('games:game_detail', game_id=game.id)
        
        # CAMBIO 3: Verificar si es el turno del jugador actual
        current_player_user = game.owner if game.active_player == 1 else game.player2
        if request.user != current_player_user:
            messages.error(request, 'Not your turn.')
            return redirect('games:game_detail', game_id=game.id)
        
        square_id = request.POST.get('submit')
        if square_id and square_id.isdigit():
            idx = int(square_id)
            board_list = list(game.board)
            
            if board_list[idx] == ' ' and game.game_state == 'active':
                token = 'X' if game.active_player == 1 else 'O'
                board_list[idx] = token
                game.board = ''.join(board_list)

                winner = check_winner(game.board)
                if winner:
                    game.game_state = 'won'
                    game.winner = 1 if winner == 'X' else 2
                elif ' ' not in game.board:
                    game.game_state = 'tie'
                else:
                    game.active_player = 2 if game.active_player == 1 else 1

                game.save()
    
    # CAMBIO 4: Pasar más información al template
    context = {
        'game': game,
        'your_player': 'player1' if request.user == game.owner else 'player2' if request.user == game.player2 else None,
        'is_your_turn': (game.active_player == 1 and request.user == game.owner) or 
                        (game.active_player == 2 and request.user == game.player2)
    }
    return render(request, 'games/game.html', context)

@login_required
def delete_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if request.user == game.owner:
        game.delete()
        messages.success(request, 'Game room deleted.')
    else:
        messages.error(request, 'You are not the owner.')
    return redirect('games:game_list')

def check_winner(board):
    lines = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    for a,b,c in lines:
        if board[a] == board[b] == board[c] and board[a] != ' ':
            return board[a]
    return None