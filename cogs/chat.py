#####################################################
import discord
from discord.ext import commands, tasks
import json
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

greetingsAndQuestion = json.loads(open('intents/greet.json', 'r').read())
trainList = []
for row in greetingsAndQuestion:
    trainList.append(row['question'])
    trainList.append(row['answer'])
chatbot = ChatBot('Prinz', logic_adapters=[
                        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand.',
            'maximum_similarity_threshold': 0.90
        }
                ])
trainer = ListTrainer(chatbot)
trainer.train(trainList)

class Chat(commands.Cog, description="Chat with the AI"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def chat(self, ctx, *, words:str):
        '''Chit chat'''
        response = chatbot.get_response(words)
        await ctx.send(response)

def setup(bot):
    bot.add_cog(Chat(bot))
