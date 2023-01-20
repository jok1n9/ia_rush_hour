"""Example client."""
import asyncio
import getpass
import json
import os
from common import *
from rush import *
from tree_search import *
from Cursor import *
# Next 4 lines are not needed for AI agents, please remove them from your code!
import time
import websockets


async def init_tree(map):

    domain = RushHour(map)
    problem = SearchProblem(domain, map)
    tree = SearchTree(problem, 'greedy')
    return tree.search()


def crazy_back(map1, map2):
    pieces = []
    actions = []
    for y, line in enumerate(map1.grid):
        for x, collumn in enumerate(line):
            char = map1.get(Coordinates(x, y))
            if char != map1.empty_tile and char != map1.wall_tile and char not in pieces:
                pieces.append(char)
    for piece in pieces:
        a = map1.piece_coordinates(piece)
        b = map2.piece_coordinates(piece)
        if a != b:
            actions.append(
                (piece, Coordinates(a[0].x-b[0].x,  a[0].y - b[0].y)))
    return actions


async def agent_loop(server_address="localhost:8000", agent_name="student"):
    """Example client loop."""
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
        last_level = None
        last_game = None
        next = 0
        while True:
            try:
                state = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server
                if (last_game != state.get("grid") and last_level != state.get("level")) or next == 1:

                    # cursor initialization and update each level
                    if last_game == None:
                        cursor = Cursor([3, 3])
                    else:
                        cursor.update(Coordinates(state.get("cursor")[
                                      0], state.get("cursor")[1]))

                        if state.get("selected") != 'None':
                            cursor.select()
                    # reset cycle conditions
                    next = 0
                    last_game = state.get("grid")
                    last_level = state.get("level")

                    # variable resetting(moves)
                    moves = []

                    # three initializing and obtaining actions
                    # moves are keys necessary to complete level
                    map = Map(state.get("grid"))
                    tree = await init_tree(map)
                    ok = 0
                    while (ok < 0.1):
                        time_before = time.time()
                        state = json.loads(await websocket.recv())
                        ok = time.time()-time_before

                    actions = tree[-1].actions
                    grids = [node.state for node in tree]
                    moves = cursor.movelevel(map, actions)

                    count = 0
                    # loops trough solution keys and sends them to server
                    for i, move in enumerate(moves):
                        last_state = state

                        if move == '1':  # if we enter a new action move=1
                            crazy = Map(state.get("grid"))
                            if str(crazy) != str(grids[count]):
                                try:
                                    act = crazy_back(grids[count], crazy)
                                    crazy_cursor = Cursor([
                                        state.get("cursor")[0], state.get("cursor")[1]])

                                    if state.get("selected") != 'None':
                                        crazy_cursor.select()
                                    keys = crazy_cursor.movelevel(crazy, act)
                                    for key in keys:
                                        await websocket.send(
                                            json.dumps(
                                                {"cmd": "key", "key": key})
                                        )
                                        state = json.loads(await websocket.recv())
                                except:
                                    next = 1
                                    break
                            count += 1
                        else:
                            if state.get("level") != last_level:
                                print("same level+")
                                next = 1
                                break

                            await websocket.send(
                                json.dumps({"cmd": "key", "key": move})
                            )  # send key command to server - you must implement this send in the AI agent
                            if i != len(moves)-1:
                                state = json.loads(await websocket.recv())

                    if (state.get("level") == last_level):
                        next = 1

            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return


# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
