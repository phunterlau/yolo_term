# YOLO Terminal Server

This directory contains the refactored server code for the YOLO Terminal game.

## Structure

The server code has been refactored into a modular structure:

- `__init__.py`: Package initialization, exports the `create_app` function
- `app.py`: Flask application setup and configuration
- `game_state.py`: Game state management functions
- `routes.py`: API routes and endpoints

## Running the Server

To run the server, use the `new_server.py` script in the root directory:

```bash
python new_server.py
```

Or make it executable and run directly:

```bash
chmod +x new_server.py
./new_server.py
```

The server will start on port 5001 by default.

## API Endpoints

The server provides the following API endpoints:

- `POST /api/new_game`: Create a new game
- `GET /api/game/<game_id>`: Get game state
- `POST /api/game/<game_id>/next_day`: Advance to the next day
- `POST /api/game/<game_id>/buy`: Buy stocks
- `POST /api/game/<game_id>/sell`: Sell stocks
- `POST /api/game/<game_id>/bank`: Perform bank actions
- `POST /api/game/<game_id>/hospital`: Visit the hospital
- `POST /api/game/<game_id>/broker`: Visit the student loan broker
- `POST /api/game/<game_id>/trading_app`: Use the trading app
- `POST /api/game/<game_id>/darkweb`: Visit the darkweb
- `GET /api/game/<game_id>/chart`: Get chart data for a game
- `GET /api/high_scores`: Get high scores

## Memory Usage

The server uses in-memory storage for game states, which is efficient for a small number of players. For a production environment with many users, it would be recommended to replace the in-memory storage with a database.

Estimated memory usage for 10 simultaneous players: ~30-40 MB
