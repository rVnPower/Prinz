from discord import Embed, Colour
from config import MAIN_COLOR, RED_COLOR, YELLOW_COLOR, EMPTY_CHARACTER

def success_embed(title=EMPTY_CHARACTER, description=EMPTY_CHARACTER):
	return Embed(
		title=title,
		description=description,
		color=Colour.green()
	).set_footer(text= f"{ctx.author} | {ctx.message.created_at}", icon_url=ctx.author.display_avatar.url)


def normal_embed(title=EMPTY_CHARACTER, description=EMPTY_CHARACTER):
	return Embed(
		title=title,
		description=description,
		color=MAIN_COLOR
	).set_footer(text= f"{ctx.author} | {ctx.message.created_at}", icon_url=ctx.author.display_avatar.url)

def warn_embed(title=EMPTY_CHARACTER, description=EMPTY_CHARACTER):
	return Embed(
		title=title,
		description=description,
		color=YELLOW_COLOR
	).set_footer(text= f"{ctx.author} | {ctx.message.created_at}", icon_url=ctx.author.display_avatar.url)

def error_embed(title=EMPTY_CHARACTER, description=EMPTY_CHARACTER):
	return Embed(
		title=title,
		description=description,
		color=RED_COLOR
	)