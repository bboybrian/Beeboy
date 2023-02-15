import pandas
import chess
import chess.svg
import os
import discord

vipsbin = r'C:/Users/tansz/OneDrive/Documents/Programming/discord-bot/Beeboy/chess_puzzles/libvips_bin'
add_dll_dir = getattr(os, 'add_dll_directory', None)
if callable(add_dll_dir):
    add_dll_dir(vipsbin)
else:
    os.environ['PATH'] = os.pathsep.join((vipsbin, os.environ['PATH']))

import pyvips

class ChessPuzzler:
    puzzle_embed = discord.Embed(
        title="White to Play",
        description="Rating: [r], 👍[80%]",
        color=0xffffff,
    )
    puzzle_embed.set_image(url="attachment://puzzle.png")   # look at https://discordpy.readthedocs.io/en/stable/faq.html#local-image
    
    puzzle_buttons = [discord.ui.Button(style=discord.ButtonStyle.grey, custom_id="hint", label="Hint"), discord.ui.Button(style=discord.ButtonStyle.grey, custom_id="hint", label="Answer")]
    
    puzzles = pandas.DataFrame()

    def __init__(self, puzzles='chess_puzzles/lichess_puzzles.csv'):
        print("INITIALIZING CHESS PUZZLER...")
        self.load_puzzles(puzzles)

    def load_puzzles(self, fname):
        print("LOADING PUZZLES...")
        self.puzzles = pandas.read_csv(fname)

    def generate_puzzle(self):
        imgname = "chess_puzzles/puzzle.png"
        print("GENERATING PUZZLE...")
        p = self.get_puzzle()
        if os.path.isfile(imgname):
            os.remove(imgname)

        # Make png image of puzzle
        fen = (p['FEN'].values[0])
        board = 0
        board = chess.Board(fen)
        turn = fen.split(' ')[1] != 'w' # True if white to move (Flipped because first move in FEN is played by opponent)
        moves = p['Moves'].values[0].split(' ')
        board.push_san(moves[0])

        svg = chess.svg.board(board=board, size=400, flipped=(not turn))
        f = open(imgname, "w")
        f.write(svg)
        f.close()
        image = pyvips.Image.new_from_file(imgname, dpi=300)
        image.write_to_file(imgname)

        # Parse hints
        hint = moves[1][:2]
        answer = hint + " -> " + moves[1][2:]
        # print(hint)
        # print(answer)

        # Make puzzle embed
        self.puzzle_embed.description = f"Rating: {p['Rating'].values[0]},   👍{p['Popularity'].values[0]}%"
        if turn:
            self.puzzle_embed.title = "White to Play"
            self.puzzle_embed.color = 0xffffff
        else:
            self.puzzle_embed.title = "Black to Play"
            self.puzzle_embed.color = 0x000000

        puzzle_img = discord.File(imgname, filename="puzzle.png")
        return puzzle_img, self.puzzle_embed, self.puzzle_buttons, hint, answer

    def get_puzzle(self):
        return self.puzzles.sample(n=1)

def filter_puzzles():
    puzzles = pandas.read_csv('lichess_db_puzzle.csv')
    puzzles = puzzles[puzzles['Rating'] > 1700]
    puzzles = puzzles[puzzles['Popularity'] > 70]
    puzzles = puzzles.drop(columns=['RatingDeviation', 'NbPlays','Themes','GameUrl','OpeningFamily','OpeningVariation'], axis=1)
    puzzles.to_csv('lichess_puzzles.csv', index=False)

if __name__ == '__main__':
    # load_puzzles()
    cp = ChessPuzzler()
    cp.generate_puzzle()