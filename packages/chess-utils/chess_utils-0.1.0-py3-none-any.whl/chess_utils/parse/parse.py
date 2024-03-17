import chess

def square(e4: str) -> chess.Square:
  """Like `chess.parse_square`, but ~1.8x faster (because it doesn't check and assumes `e4` is a valid string square)"""
  e, n = e4
  file = ord(e) - ord('a')
  rank = int(n)-1
  return chess.square(file, rank)

def uci(e2e4: str) -> chess.Move:
  """Like `chess.Move.from_uci` but ~50% faster"""
  e2 = e2e4[:2]
  e4 = e2e4[2:]
  return chess.Move(square(e2), square(e4))