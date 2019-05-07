# Chess2Vec

Chess2Vec contains code to turn chessgames in the format pgn into numpy vectors suitable for machine learning projects. It utilises the chess-module: https://python-chess.readthedocs.io/en/v0.2.0/pgn.html

The generator Game2Vectors(,) takes a path to the pgn and a game number with which to start (as to be able to skip games already used) and outputs "position", "move" (as input), "move" (as output), "Elo", "Elo difference" and "result" as vectors. The output format is a list for each game that contains these vectors for each position in the game. Positions with black to move are mirrored, so it is always white to move. 

The move vector for input is basically the starting square and the target square both vectorised and concatenated. The move vector for output is a 64^2 vector which has a unique entry for each starting and target square combination. (If you think about it for a moment, you'll realize that you cannot use the input format for move prediction.)

Stellung2Vektor() can be used to turn a position into a vector.
Vektor2Stellung() can turn this vector back into a position. 
Spiegelung() mirrors a position.
For a nice position printing function you might want to pilfer the ascii-ouput from the WinningPy-repo. 

This has not been intensively tested with different game databases, but it might nevertheless be a good starting point for your chess machine learning project. 

