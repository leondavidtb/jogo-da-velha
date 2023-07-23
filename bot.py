import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import random

board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
player_symbol = 'X'
computer_symbol = 'O'
bot_token = ''
chat_id = ''
turn = 'player'

def display_board():
    global board
    board_string = f"{board[0]} | {board[1]} | {board[2]}\n---------\n{board[3]} | {board[4]} | {board[5]}\n---------\n{board[6]} | {board[7]} | {board[8]}"
    bot.send_message(chat_id=chat_id, text=board_string)

def check_game_over(symbol):
    global board
    
    for i in range(0, 9, 3):
        if board[i] == board[i+1] == board[i+2] == symbol:
            return True
    
    for i in range(3):
        if board[i] == board[i+3] == board[i+6] == symbol:
            return True
    
    if board[0] == board[4] == board[8] == symbol:
        return True
    
    if board[2] == board[4] == board[6] == symbol:
        return True
    
    return False

def computer_move():
    global board, computer_symbol
    valid_moves = [i for i in range(9) if board[i] == ' ']
    move = random.choice(valid_moves)
    board[move] = computer_symbol
    
    display_board()
    
    if check_game_over(computer_symbol):
        bot.send_message(chat_id=chat_id, text='O computador ganhou!')
        return
    
    if len(valid_moves) == 1:
        bot.send_message(chat_id=chat_id, text='Fim de jogo! Empate.')
        return
    
    global turn
    turn = 'player'

def handle_input(update, context):
    global board, player_symbol
    
    try:
        move = int(update.message.text)
        if move < 1 or move > 9:
            raise ValueError
        move -= 1
        if board[move] != ' ':
            raise ValueError
        board[move] = player_symbol
        display_board()
        
        if check_game_over(player_symbol):
            bot.send_message(chat_id=chat_id, text='Você ganhou!')
            return
        if ' ' not in board:
            bot.send_message(chat_id=chat_id, text='Fim de jogo! Empate.')
            return
        
        bot.send_message(chat_id=chat_id, text='Vez do computador: ')
        global turn
        turn = 'computer'
        computer_move()
        
        bot.send_message(chat_id=chat_id, text='Sua vez: ')
    except (ValueError, IndexError):
        bot.send_message(chat_id=chat_id, text='Movimento inválido. Por favor, entre com um número de 1 a 9.')
        display_board()

def start_game(update, context):
    global board, player_symbol, turn, chat_id
    board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    player_symbol = 'X'
    turn = 'player'
    chat_id = update.effective_chat.id

    display_board()
    bot.send_message(chat_id=chat_id, text='O jogo começou. Seu símbolo é o X. Por favor, entre com um número de 1 a 9.')

def unknown():
    bot.send_message(chat_id=chat_id, text="Ops, não reconheço este comando.")


def main():
    global bot
    bot = telegram.Bot(token=bot_token)
    updater = Updater(bot_token, use_context=True)

    start_handler = CommandHandler('start', start_game)
    updater.dispatcher.add_handler(start_handler)
    unknown_handler = MessageHandler(Filters.command, unknown)
    updater.dispatcher.add_handler(unknown_handler)

    message_handler = MessageHandler(Filters.text & ~Filters.command, handle_input)
    updater.dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()