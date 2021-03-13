import pygame 
from config import *

def bind(window, font):
    return lambda text, color, pos: render_number(window, font, text, color, pos) if text.isdigit() else \
         render_text(window, font, text, color, pos)

def render_text(window, font, text : str, color, pos):
    time_text = font.render(text, True, color)
    time_text_rect = time_text.get_rect()
    time_text_rect.center = pos
    window.blit(time_text, time_text_rect)

def render_number(window, font, text : str, color, pos):
    textToPrint = text
    while len(textToPrint) < MAX_N_DIGITS:
        textToPrint = "0" + textToPrint
    render_text(window, font, textToPrint, color, pos)