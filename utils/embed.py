from discord import Embed, Colour
from config import MAIN_COLOR, RED_COLOR, YELLOW_COLOR

def success_embed(title, description):
	return Embed(
		title=title,
		description=description,
		color=Colour.green()
	)


def normal_embed(title, description):
	return Embed(
		title=title,
		description=description,
		color=MAIN_COLOR
	)

def warn_embed(title, description):
	return Embed(
		title=title,
		description=description,
		color=YELLOW_COLOR
	)

def error_embed(title, description):
	return Embed(
		title=title,
		description=description,
		color=RED_COLOR
	)