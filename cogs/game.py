#####################################################
import discord
from discord.ext import commands, tasks
import random
import asyncio
#####################################################

class Games(commands.Cog, description="Games you can play", name="Game"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Play a guessing game (Guess a number from 1 to 1000)")
    async def guess(self, ctx):
        # Simple guessing game
        embed = discord.Embed(colour=discord.Colour.blurple(), title="Guess a number between 1 and 1000.")
        await ctx.send(embed=embed)
        answer = random.randint(1, 1000)
        while True:
            def is_correct(m):
                return m.author == ctx.author and m.content.isdigit()
            embed = discord.Embed(colour=discord.Colour.blurple())

            try:
                guess = await self.bot.wait_for('message', check=is_correct, timeout=60.0)
            except asyncio.TimeoutError:
                embed.set_author(name=f'Sorry, you took too long it was {answer}.')
                await ctx.send(embed=embed)
                break

            if int(guess.content) == answer:
                embed.set_author(name = 'You are right!')
                await ctx.send(embed=embed)
                break
            if int(guess.content) > answer:
                embed.set_author(name='Lower!')
            if int(guess.content) < answer:
                embed.set_author(name ='Higher!')
            await ctx.send(embed=embed)

    @commands.command(help="2048")
    async def _2048(self, ctx):
        def init():
            """
            initialize a 2048 matrix. return a matrix list
            """
            matrix = [ 0 for i in range(16) ]
            random_lst = random.sample( list(range(16)), 2 ) # generate 2 different number
            matrix[random_lst[0]] = matrix[random_lst[1]] = 2
            return matrix

        def move(matrix,direction):
            """
            moving the matrix. return a matrix list
            """
            mergedList = [] #initial the merged index
            if direction == '⬆️':
                for i in range(16):
                    j = i
                    while j - 4 >= 0:
                        if matrix[j-4] == 0:
                            matrix[j-4] = matrix[j]
                            matrix[j] = 0
                        elif matrix[j-4] == matrix[j] and j not in mergedList:
                            matrix[j-4] *=2
                            matrix[j] = 0
                            mergedList.append(j-4)
                            mergedList.append(j)  #prevent the number to be merged twice
                        j -= 4
            elif direction == '⬇️':
                for i in range(15,-1,-1):
                    j = i
                    while j + 4 < 16:
                        if matrix[j+4] == 0:
                            matrix[j+4] = matrix[j]
                            matrix[j] = 0
                        elif matrix[j+4] == matrix[j] and j not in mergedList:
                            matrix[j+4] *=2
                            matrix[j] = 0
                            mergedList.append(j)
                            mergedList.append(j+4)
                        j += 4
            elif direction == '◀️':
                for i in range(16):
                    j = i
                    while j % 4 != 0:
                        if matrix[j-1] == 0:
                            matrix[j-1] = matrix[j]
                            matrix[j] = 0
                        elif matrix[j-1] == matrix[j] and j not in mergedList:
                            matrix[j-1] *=2
                            matrix[j] = 0
                            mergedList.append(j-1)
                            mergedList.append(j)
                        j -= 1
            elif direction == '▶️':
                for i in range(15,-1,-1):
                    j = i
                    while j % 4 != 3:
                        if matrix[j+1] == 0:
                            matrix[j+1] = matrix[j]
                            matrix[j] = 0
                        elif matrix[j+1] == matrix[j] and j not in mergedList:
                            matrix[j+1] *=2
                            matrix[j] = 0
                            mergedList.append(j)
                            mergedList.append(j+1)
                        j += 1
            return matrix

        def insert(matrix):
            """insert one 2 or 4 into the matrix. return the matrix list
            """
            getZeroIndex = []
            for i in range(16):
                if matrix[i] == 0:
                    getZeroIndex.append(i)
            randomZeroIndex = random.choice(getZeroIndex)
            matrix[randomZeroIndex] = 2
            return matrix

        async def output(matrix, ctx):
            """
            print the matrix. return the matrix list
            """
            max_num_width = len(str(max(matrix)))
            conver2char = lambda num :'{0:>{1}}'.format(num, max_num_width) \
                                         if num>0 else '⠀'*max_num_width
            demarcation = ( '+' + '-'*(max_num_width+4) ) * 4 + '+' #generate demarcation line like '+---+---+---+'
            return (('\n'+demarcation+'\n').join(['|⠀'+'⠀|⠀'.join([ conver2char(num)
                            for num in matrix[i*4:(i+1)*4]])+'⠀|' for i in range(4)]))

        def isOver(matrix):
            """is game over? return bool
            """
            if 0 in matrix:
                return False
            else:
                for i in range(16):
                    if i % 4 != 3:
                        if matrix[i] == matrix[i+1]:
                            return False
                    if i < 12:
                        if matrix[i] == matrix [i+4]:
                            return False
            return True

        def getchar(prompt="Wait input: "):
            import termios, sys
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            new = termios.tcgetattr(fd)
            new[3] = new[3] & ~termios.ICANON          # lflags
            try:
                termios.tcsetattr(fd, termios.TCSADRAIN, new)
                sys.stderr.write(prompt)
                sys.stderr.flush()
                c = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
            return c

        def is_correct(m):
            return m.author == ctx.author

        async def play():
            matrix = init()
            vim_map = {'h':'a', 'j':'s', 'k':'w', 'l':'d'}
            matrix_stack = [] # just used by back function
            matrix_stack.append(list(matrix))
            step = len(matrix_stack) - 1
            mat = await output(matrix, ctx)
            buttons = [ '◀️', '⬆️', '⬇️', '▶️', '❌']
            embed = discord.Embed(colour=discord.Colour.blurple(), description=mat)
            msg = await ctx.send(embed=embed)
            for button in buttons:
                await msg.add_reaction(button)

            while True:
                mat = await output(matrix, ctx)
                embed = discord.Embed(colour=discord.Colour.blurple(), description=mat)
                await msg.edit(embed=embed)
                if isOver(matrix) == False:
                    if max(matrix) == 2048:
                        await ctx.send('You won!')
                        return
                    while True:
                        try:
                            reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction , user: user==ctx.author and reaction.emoji in buttons, timeout=60.0)
                        except asyncio.TimeoutError:
                            embed = discord.Embed(color = discord.Colour.blurple())
                            embed.set_author(name=f'Time out!')
                            await ctx.send(embed=embed)
                            return
                        else:
                            if reaction.emoji in [ '◀️', '⬆️', '⬇️', '▶️']:
                                matrix = move(matrix, reaction.emoji)
                                if matrix == matrix_stack[-1]:
                                    await msg.edit(content='You can\'t move in that way anymore.', embed=embed)
                                else:
                                    insert(matrix)
                                for button in buttons:
                                    await msg.remove_reaction(button, ctx.author)
                                matrix_stack.append(list(matrix))
                                break
                            elif reaction.emoji == '❌':
                                return
                            else:
                                await msg.edit(content='That move is invaild.', embed=embed)
                else:
                    await ctx.send('You lose! Better luck next time!')
                    return
                step = len(matrix_stack) - 1

        await play()
        

def setup(bot):
    bot.add_cog(Games(bot))