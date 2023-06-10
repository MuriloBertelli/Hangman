import pygame
from kivy.core.audio import SoundLoader
from pygame import mixer
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.behaviors import DragBehavior
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.uix.actionbar import ActionBar


class TelaInicio(Screen):
    pass


class TelaTheme(Screen):
    theme = {'COR': 'VERDE',
             'ANIMAL': 'ELEFANTE',
             'FRUTA': 'MORANGO'
             }

    def __init__(self, **kwargs):
        super(TelaTheme, self).__init__(**kwargs)

    def theme_selecionado(self, theme):
        self.manager.current = 'Hangman'
        if theme == 'COR':
            self.manager.get_screen(
                'Hangman').palavra_selecionada = self.theme.get('COR')
        elif theme == 'FRUTA':
            self.manager.get_screen(
                'Hangman').palavra_selecionada = self.theme.get('FRUTA')
        elif theme == 'ANIMAL':
            self.manager.get_screen(
                'Hangman').palavra_selecionada = self.theme.get('ANIMAL')

        self.manager.get_screen('Hangman').startGame()


class Hangman(Screen):
    palavra_selecionada = ""
    current_word = StringProperty('')
    guessed_letters = []
    max_errors = 6
    current_errors = 0
    music_list = ['sounds/underworld.mp3', 'sounds/underworld2.mp3']
    music_index = 0

    # Esta função serve para que minha palavra selecionada anterior mente '_' * len ele passa cada letra e substitui por '_'

    def startGame(self):
        self.current_word = '_' * len(self.palavra_selecionada)

    def __init__(self, **kwargs):
        super(Hangman, self).__init__(**kwargs)

    def check_guess(self, letter):

        if letter in self.guessed_letters:  # verifica se o butto que foi clicado ja teria sido clicado antes
            self.ids.mensagem_wrong.text = '[font=fonts/error.ttf][color=#FF0000] A letra ja foi selecionada anteriormente, tente outra letra![/color][/font]'
            # limpa a mensagem exibida.
            Clock.schedule_once(lambda dt: self.clear_error_massage(), 2)
            # Reproduzir o som
            sound = mixer.Sound('sounds/dead.mp3')
            sound.play()
            return
        # se ele não foi clicado, a letra é adiciona a lista de letras que ja foram.
        self.guessed_letters.append(letter)

        if letter in self.palavra_selecionada:  # verifica se letter esta presente na palavra que esta sendo adivinhada, se estiver presente executa o bloco do if
            # Essa variável será usada para construir a palavra atualizada com as letras corretamente adivinhadas.
            guessed_word = ''
            # Itera sobre as letras da palavra selecionada (self.palavra_selecionada) e a palavra atual (self.current_word) simultaneamente usando a função zip().
            for char, guess in zip(self.palavra_selecionada, self.current_word):
                # verifica se o caracter 'char'(letra da palavra selecionada) é igual a letraa letter que esta sendo adivinhada. Se for igaual a letra adiciona a string 'guessed_word' usando o operador de concatenação.
                if char == letter:
                    guessed_word += char
                # Caso contrário, ou seja, se o caractere char não for igual à letra letter, o caractere guess (letra adivinhada anteriormente) é adicionado à string guessed_word. Isso preserva as letras corretamente adivinhadas até o momento.
                else:
                    guessed_word += guess

            # atualizando assim a palavra atual que está sendo mostrada ao jogador.
            self.current_word = guessed_word

            # verifica se ainda não existe mais underscores na palavra atualizaad. Isso significa que todas as letras foram corretamente adivinhadas e o jogador ganhou o jogo.
        if '_' not in self.current_word:
            # faz um carregar minha mensagem de pertidad ganha.
            self.ids.win.source = f'image/win.png'
            # reinicia o jogo apos 2 segundos
            Clock.schedule_once(lambda dt: self.restar(), 6)
            sound = mixer.Sound('sounds/level-complete.mp3')
            sound.play()

        # enquando a letra não estiver na palavra oculta, ele adiciona mais um erro e atuliza a imagem com a função criada anterior mente.
        if letter not in self.current_word:
            self.current_errors += 1
            self.atualiza_image()
            # verifica se chegou na contagem maxima de erros, e mostra a msg que o jogador perdeu.
            if self.current_errors == self.max_errors:
                # Faz eu carregar a minha imagem de partida perdida.
                self.ids.lost.source = f'image/lost.png'
                Clock.schedule_once(lambda dt: self.restar(), 4)
                # Reproduz o som que perdeu
                sound = mixer.Sound('sounds/game over.mp3')
                sound.play()

    def atualiza_image(self):

        self.ids.image_at.source = f'image/{self.current_errors}.png'

    def restar(self):

        # Para a musica atual
        pygame.mixer.music.stop()
        # Proxima musica
        self.music_index = (self.music_index + 1) % len(self.music_list)
        music_path = self.music_list[self.music_index]
        # carrega e reproduz a nova musica
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play()
        # Regulo o volume da minha musica
        pygame.mixer.music.set_volume(0.3)
        # Reseto a minha imagem que o jogador perdeu
        self.ids.lost.source = ''
        # Retira a imagem de que a pessoa ganhou.
        self.ids.win.source = ''
        # Volto a minha apalvra como vazio
        self.current_word = ''
        # Reseto minha lista de letra que ja foram diditadas anteriormente.
        self.guessed_letters = []
        # Volto o erros como vazio
        self.current_errors = 0
        # Reseta a imagem
        self.atualiza_image()
        # volta para a tela para selecionar um tema
        self.manager.current = 'TelaTheme'

    def clear_error_massage(self):
        self.ids.mensagem_wrong.text = ''


class GerenciadorTelas(ScreenManager):
    pass


class HangmanApp(App):
    def build(self):

        # Inicia a musica
        pygame.mixer.init()
        # Carrega e reproduz a primeira musica da lista
        pygame.mixer.music.load(Hangman.music_list[0])
        pygame.mixer.music.play()
        # Regulo o volume da minha musica
        pygame.mixer.music.set_volume(0.3)

        return GerenciadorTelas()


HangmanApp().run()
