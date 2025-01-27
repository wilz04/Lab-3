# IC 6101 1er Semestre 2017
# Nombre: Wilberth Castro
# Correo: wilz04@gmail.com

from util import INFINITY
from util import NEG_INFINITY

### 1. Escogencia multiple

# 1.1. Dos jugadores computarizados estan jugando un juego. El Jugador MM utiliza minimax
#      para buscar a una profundidad de 6 para decidir sobre una movida. El jugador AB utiliza alpha-beta
#      para buscar a una profundidad de 6.
#      El juego se lleva a cabo sin un limite de tiempo. Cual jugador jugara mejor?
#
#      1. MM jugara mejor que AB.
#      2. AB jugara mejor que  MM.
#      3. Ambos jugaran al mismo nivel de destreza.
ANSWER1 = 0

# 1.2. Dos jugadores computarizados juegan un juego con un limite de tiempo. El jugador MM
# hace busqueda minimax con profundidad iterativa, y el jugador AB hace busqueda alpha-beta
# con profundidad iterativa. Cada uno retorna un resultado despues de haber utilizado
# 1/3 de su tiempo restante. Cual jugador jugara mejor?
#
#      1. MM jugara mejor que AB.
#      2. AB jugara mejor que  MM.
#      3. Ambos jugaran al mismo nivel de destreza.
ANSWER2 = 0

### 2. Connect Four
from connectfour import *
from basicplayer import *
from util import *
import tree_searcher

## Esta seccion contiene lineas ocasionales que puede descomentar para jugar
## el juego interactivamente. Asegurese de re-comentar cuando ha terminado con
## ellos.  Por favor no entregue su tarea con partes de codigo que solicitan
## jugar interactivamente!
## 
## Descomente la siguiente linea para jugar el juego como las blancas:
#run_game(human_player, basic_player)

## Descomente la siguiente linea para jugar como las negras:
#run_game(basic_player, human_player)

## O bien vea a la computadora jugar con si misma:
#run_game(basic_player, basic_player)

## Cambie la siguiente funcion de evaluacion tal que trata de ganar lo mas rapido posible,
## o perder lentamente, cuando decide que un jugador esta destina a ganar.
## No tiene que cambiar como evalua posiciones que no son ganadoras.

def focused_evaluate(board):
	"""
	Dado un tablero, returna un valor numerico indicando que tan bueno
	es el tablero para el jugador de turno.
	Un valor de retorno >= 1000 significa que el jugador actual ha ganado;
	Un valor de retorno <= -1000 significa que el jugador actual perdio
	"""
	
	if board.is_game_over():
		# Si el juego ha sido ganado, sabemos que debe haber sido
		# ganado o terminado en la movida anterior.
		# La jugada anterior fue efectuada por nuestro oponente.
		# Por lo que no podemos haber ganado, asi que retornamos -1000.
		# (note que esto produce que un empate sea tratado como una perdida)
		score = -1000 + board.num_tokens_on_board()
	else:
		score = (
			board.longest_chain(board.get_current_player_id()) -
			board.longest_chain(board.get_other_player_id())
		)*10
		# Prefiere poner sus piezas en el centro del tablero
		for row in range(6):
			for col in range(7):
				if board.get_cell(row, col) == board.get_current_player_id():
					score -= abs(3-col)
				elif board.get_cell(row, col) == board.get_other_player_id():
					score += abs(3-col)
		
		score -= board.num_tokens_on_board()
	
	return score


## Crea una funcion "jugador" que utiliza la funcion focused_evaluate function
quick_to_win_player = lambda board: minimax(board, depth=4, eval_fn=focused_evaluate)

## Puede probar su nueva funcion de evaluacion descomentando la siguiente linea:
#run_game(basic_player, quick_to_win_player)

## Escriba un procedimiento de busqueda alpha-beta-search que actua como el procedimiento minimax-search
## pero que utiliza poda alpha-beta para evitar buscar por malas ideas
## que no pueden mejorar el resultado. El tester revisara la poda
## contando la cantidad de evaluaciones estaticas que hace
##
## Puede utilizar el minimax() que se encuentra basicplayer.py como ejemplo.
def alpha_beta_search(
	board,
	depth,
	eval_fn,
	# NOTA: usted debe utilizar get_next_moves_fn cuando genera
	# configuraciones de proximos tableros, y utilizar is_terminal_fn para
	# revisar si el juego termino.
	# Las funciones que por defecto se asignan aqui funcionarar 
	# para connect_four.
	get_next_moves_fn=get_all_next_moves,
	is_terminal_fn=is_terminal
):
	"""
	Hace una busqueda minimax con poda alpha-beta en el tablero a la profundidad especificada.

	board -- la instancia ConnectFourBoard a evaluar
	depth -- la profundidad del arbol de busqueda (medida como la distancia maxima de la raiz a una hoja)
	eval_fn -- (opcional) la funcion de evaluacion para utilizar en una hoja del arbol; revise "focused_evaluate" para ver un ejemplo

	Returna un entero, el numero de columna que la busqueda indica donde debe agregar su ficha
	"""
	if is_terminal_fn(depth, board):
		return eval_fn(board)
	
	best_val = (NEG_INFINITY, -1, None)

	for move, new_board in get_next_moves_fn(board):
		val = beta_find_board_value(new_board, depth-1, eval_fn, get_next_moves_fn, is_terminal_fn, best_val[0])
		if val > best_val[0] or best_val[1] == -1:
			best_val = (val, move, new_board)
	
	return best_val[1]

def beta_find_board_value(board, depth, eval_fn, get_next_moves_fn=get_all_next_moves, is_terminal_fn=is_terminal, alpha=NEG_INFINITY, beta=INFINITY): #min
	"""
	Funcion de ayuda a alpha_beta_search: Retorna el valor minimax con poda beta de un tablero particular,
	dado una profundidad con la cual estimar
	"""
	if is_terminal_fn(depth, board):
		return eval_fn(board)

	for move, new_board in get_next_moves_fn(board):
		val = alpha_find_board_value(new_board, depth-1, eval_fn, get_next_moves_fn, is_terminal_fn, alpha, beta)
		if val < beta:
			beta = val
		
		if beta <= alpha:
			break
	
	return beta

def alpha_find_board_value(board, depth, eval_fn, get_next_moves_fn=get_all_next_moves, is_terminal_fn=is_terminal, alpha=NEG_INFINITY, beta=INFINITY): #max
	"""
	Funcion de ayuda a alpha_beta_search: Retorna el valor minimax con poda alpha de un tablero particular,
	dado una profundidad con la cual estimar
	"""
	if is_terminal_fn(depth, board):
		return eval_fn(board)

	for move, new_board in get_next_moves_fn(board):
		val = beta_find_board_value(new_board, depth-1, eval_fn, get_next_moves_fn, is_terminal_fn, alpha, beta)
		if val > alpha:
			alpha = val
		
		if alpha >= beta:
			break
		
	return alpha


## Ahora deberia ser capaz de buscar al doble de profundidad en la misma cantidad de tiempo.
## (Claro que este jugador alpha-beta-player no funcionara hasta que haya definido
## alpha-beta-search.)
alphabeta_player = lambda board: alpha_beta_search(board, depth=8, eval_fn=focused_evaluate)

## Este jugador utiliza profundidad iterativa, asi que le puede ganar mientras hace uso 
## eficiente del tiempo:
ab_iterative_player = lambda board: run_search_function(
	board,
	search_fn=alpha_beta_search,
	eval_fn=focused_evaluate,
	timeout=5)

#run_game(ab_iterative_player, alphabeta_player)

## Finalmente, aqui debe crear una funcion de evaluacion mejor que focused-evaluate.
## By providing a different function, you should be able to beat
## simple-evaluate (or focused-evaluate) while searching to the
## same depth.

def better_evaluate(board):
	"""
	The original focused-evaluate function from the lab.
	The original is kept because the lab expects the code in the lab to be modified. 
	"""
	return player_evaluate(board, board.get_current_player_id()) - player_evaluate(board, board.get_other_player_id())

def player_evaluate(board, player_id):
	if board.is_game_over():
		# Si el juego ha sido ganado, sabemos que debe haber sido
		# ganado o terminado en la movida anterior.
		# La jugada anterior fue efectuada por nuestro oponente.
		# Por lo que no podemos haber ganado, asi que retornamos -1000.
		# (note que esto produce que un empate sea tratado como una perdida)
		score = -1042 + board.num_tokens_on_board()
	else:
		score = board.longest_chain(player_id)*10
		# Prefiere poner sus piezas en el centro del tablero
		for row in range(6):
			for col in range(7):
				if board.get_cell(row, col) == player_id:
					score -= get_cell_val[row][col]
		
		score += 42 - board.num_tokens_on_board()
	
	return score

get_cell_val = [
	[0, 1, 2, 4, 2, 1, 0],
	[1, 3, 5, 7, 5, 3, 1],
	[2, 5, 8, 10, 8, 5, 2],
	[2, 5, 8, 10, 8, 5, 2],
	[1, 3, 5, 7, 5, 3, 1],
	[0, 1, 2, 4, 2, 1, 0]
]

# Comente esta linea una vez que ha implementado completamente better_evaluate
# better_evaluate = memoize(basic_evaluate)

# Descomente esta linea para hacer que su better_evaluate corra mas rapido.
# better_evaluate = memoize(better_evaluate)

# Para el debugging: Cambie este if-guard a True, para hacer unit-test
# de su funcion better_evaluate.
if False:
	board_tuples = (
		( 0,0,0,0,0,0,0 ),
		( 0,0,0,0,0,0,0 ),
		( 0,0,0,0,0,0,0 ),
		( 0,0,0,0,0,0,0 ),
		( 0,0,0,0,0,0,0 ),
		( 0,0,0,0,0,0,0 ),
	)
	test_board_1 = ConnectFourBoard(board_array = board_tuples, current_player = 1)
	test_board_2 = ConnectFourBoard(board_array = board_tuples, current_player = 2)
	# better evaluate de jugador 1
	print "%s => %s" %(test_board_1, better_evaluate(test_board_1))
	# better evaluate de jugador 2
	print "%s => %s" %(test_board_2, better_evaluate(test_board_2))

## Un jugador que utiliza alpha-beta y better_evaluate:
your_player = lambda board: run_search_function(
	board,
	search_fn=alpha_beta_search,
	eval_fn=better_evaluate,
	timeout=5)

#your_player = lambda board: alpha_beta_search(board, depth=4, eval_fn=better_evaluate)

## Descomente para ver su jugador jugar un juego:
#run_game(quick_to_win_player, your_player)
#run_game(your_player, your_player)

## Descomente esto (o corralo en una ventana) para ver como le va 
## en el torneo que sera evaluado.
#run_game(your_player, basic_player)

## Estas funciones son utilizadas por el tester, por favor no las modifique!
def run_test_game(player1, player2, board):
	assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
	return run_game(globals()[player1], globals()[player2], globals()[board])
	
def run_test_search(search, board, depth, eval_fn):
	assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
	return globals()[search](globals()[board], depth=depth, eval_fn=globals()[eval_fn])

## Esta funcion corre su implementacion de alpha-beta utilizando un arbol de busqueda 
## en vez de un juego en vivo de connect four. Esto sera mas facil de debuggear.
def run_test_tree_search(search, board, depth):
	return globals()[search](
		globals()[board],
		depth=depth,
		eval_fn=tree_searcher.tree_eval,
		get_next_moves_fn=tree_searcher.tree_get_next_move,
		is_terminal_fn=tree_searcher.is_leaf)
	
## Quiere utilizar su codigo en un torneo con otros estudiantes? Vea 
## la descripcion en el enunciado de la tarea. El torneo es opcional
## y no tiene efecto en su nota
COMPETE = (None)

## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = ""
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""
NAME = ""
EMAIL = ""

