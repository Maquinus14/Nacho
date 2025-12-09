import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import Game

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_id = f"game_{self.room_id}"
        
        await self.channel_layer.group_add(
            self.room_group_id, self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_id, self.channel_name
        )
    
    async def receive(self, text_data):
        game_data = json.loads(text_data)
        user = self.scope["user"]
        
        # CAMBIO 1: Verificar que el usuario está autenticado
        if isinstance(user, AnonymousUser):
            await self.send(text_data=json.dumps({"error": "Not authenticated"}))
            return
        
        # CAMBIO 2: Procesar el movimiento
        processed_data = await self.process_move(game_data, user, self.room_id)
        
        # CAMBIO 3: Enviar los datos procesados a todos
        await self.channel_layer.group_send(
            self.room_group_id,
            {"type": "chat", "data": processed_data}
        )
    
    async def chat(self, event):
        data = event["data"]
        await self.send(text_data=json.dumps({"my_data": data}))
    
    # CAMBIO 4: Añadir función para procesar movimientos
    @database_sync_to_async
    def process_move(self, game_data, user, room_id):
        try:
            # Buscar el juego por room_id
            game = Game.objects.get(room_name=room_id)
            
            # Verificar si el usuario es jugador
            if user not in [game.owner, game.player2]:
                return {"error": "You are not a player in this game"}
            
            # Verificar turno
            current_player_user = game.owner if game.active_player == 1 else game.player2
            if user != current_player_user:
                return {"error": "Not your turn"}
            
            # Obtener posición del movimiento
            position = game_data.get('position')
            if position is None or position < 0 or position > 8:
                return {"error": "Invalid position"}
            
            # Verificar que la casilla está vacía
            board_list = list(game.board)
            if board_list[position] != ' ':
                return {"error": "Cell already taken"}
            
            # Hacer el movimiento
            token = 'X' if game.active_player == 1 else 'O'
            board_list[position] = token
            game.board = ''.join(board_list)
            
            # Verificar ganador
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
            
            winner = check_winner(game.board)
            if winner:
                game.game_state = 'won'
                game.winner = 1 if winner == 'X' else 2
            elif ' ' not in game.board:
                game.game_state = 'tie'
            else:
                # Cambiar turno
                game.active_player = 2 if game.active_player == 1 else 1
            
            game.save()
            
            # Preparar datos para enviar
            return {
                "board": list(game.board),
                "active_player": game.active_player,
                "game_state": game.game_state,
                "winner": game.winner,
                "room_id": room_id,
                "player1_id": game.owner.id,
                "player2_id": game.player2.id if game.player2 else None
            }
            
        except Game.DoesNotExist:
            return {"error": "Game not found"}
        except Exception as e:
            return {"error": str(e)}