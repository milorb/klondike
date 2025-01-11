import random
from pygame import Rect, Vector2, sprite, transform
from card import Card, CardAssets, Rank
from input import InputManager
from scene import Scene
from ui import Button, UIAssets

class Board(Scene):
    """
    main gameplay scene layout:
    |[draw][dump]      [pile][pile][pile][pile]
    |[tab0][tab1][tab2][tab3][tab4][tab5][tab6]
    |
    |     
    """
    
    card_offset = 5
    draw_pile_loc = Vector2((22 + card_offset) * 2, (16 + card_offset) * 2)
    dump_loc = Vector2(draw_pile_loc.x + 150 + 24, draw_pile_loc.y)

    reset_button_loc = Vector2(dump_loc.x + 212, dump_loc.y)

    stack_loc: list[Vector2] = [Vector2(((283 + 5) * 2 + (i * (75 + 12)) * 2), (16 + 5) * 2) for i in range(4)]

    tableau_loc: list[Vector2] = [Vector2((22 + 5 + (i * (75 + 12))) * 2, (130 + 5) * 2) for i in range(7)]


    def __init__(self, game):
        super().__init__(game)

        random.seed()

        self.ranks = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
        self.suits = ["heart", "spade", "diamond", "club"]

        self.deck = [(rank, suit) for rank in self.ranks for suit in self.suits]

        self.card_back = transform.scale_by(CardAssets.card_back, 2)
        self.cards = CardAssets.get_cards(self.ranks, self.suits, scale=2)

        self.tableaux = [Tableau(pos) for pos in self.tableau_loc]
        self.stacks = [Stack(pos) for pos in self.stack_loc]

        self.selected_cards: list[Card] = []
        
        ui_assets = UIAssets()

        self.ui_elts = sprite.Group()
        self.ui_elts.add(
            Button(
                transform.scale_by(ui_assets.reset_button, 2), 
                transform.scale_by(ui_assets.reset_button_down, 2),
                self.reset_button_loc, 
                self.restart)
        )

        random.shuffle(self.deck)


    def restart(self):
        for tab in self.tableaux:
            tab.empty()

        for stack in self.stacks:
            stack.empty()

        self.draw_pile.empty()
        self.dump.empty()

        self.selected_cards = []

        self.deck = [(rank, suit) for rank in self.ranks for suit in self.suits]
        for r_n_a in self.deck:
            c = self.cards[r_n_a[0]][r_n_a[1]]
            if c.faceup:
                c.flip_back(self.card_back)

        random.shuffle(self.deck)
        self.setup()

    def get_card_from_deck(self):
        if self.deck:
            rank_and_suit = self.deck.pop(-1)
            rank = rank_and_suit[0]
            suit = rank_and_suit[1]

            card = self.cards[rank][suit]

            return card

    def setup(self):
        count = 1
        for tab in self.tableaux:
            for _ in range(count):
                tab.add(self.get_card_from_deck())
            tab.get_top_sprite().flip_up()    
            count += 1

        rem = len(self.deck)

        self.draw_pile = DrawPile(pos=self.draw_pile_loc, 
                                  back_img=self.card_back)
        self.dump = Dump(self.dump_loc)

        for _ in range(rem):
            c = self.get_card_from_deck()
            if c:
                self.draw_pile.add(c)

    def update(self):
        left_clicked = InputManager.MOUSE_LEFT_DOWN()
        left_lifted = InputManager.MOUSE_LEFT_UP()

        if left_lifted and self.selected_cards:
            if len(self.selected_cards) == 1:
                for stack in self.stacks:
                    if stack.drop(self.selected_cards[0]):
                        self.selected_cards = []
                        break

            if self.selected_cards:
                for tab in self.tableaux:
                    if tab.drop_stack(self.selected_cards):
                        self.selected_cards = []
                        break

            self.selected_cards = []

        self.ui_elts.update()

        for tab in self.tableaux:
            tab.update(self.selected_cards)

        for stack in self.stacks:
            stack.update(self.selected_cards)

        self.dump.update(self.selected_cards)
        self.draw_pile.update(self.dump)

    def draw(self):
        screen = self.game.screen

        self.draw_pile.draw(screen)
        self.dump.draw(screen)

        self.ui_elts.draw(screen)

        for tab in self.tableaux:
            tab.draw(screen)

        for stack in self.stacks:
            stack.draw(screen)

        for card in self.selected_cards:
            screen.blit(card.image, card.rect)

        
class DrawPile(sprite.LayeredUpdates):
    def __init__(self, *sprites, pos: Vector2, back_img):
        super().__init__(*sprites)

        self.back = back_img
        self.pos = pos
        self.rect = Rect(pos.x, pos.y, 130, 180)

    def update(self, dump):
        if InputManager.MOUSE_LEFT_DOWN() \
            and self.rect.collidepoint(InputManager.cursor_pos):

            if self.sprites():
                self.draw_one(dump)
            else:
                self.reshuffle(dump)

    def add(self, *sprites, **kwargs):
        super().add(*sprites, **kwargs)

        for sprite in sprites:
            if type(sprite) == Card:
                sprite.rect.x = self.pos.x
                sprite.rect.y = self.pos.y


    def draw_one(self, dump):
        card = self.get_top_sprite()
        card.flip_up()

        self.remove(card)
        dump.add(card)

    def draw_cards(self, num):
        pass 

    def reshuffle(self, dump):
        cards = dump.sprites()
        for card in cards:
            card.flip_back(self.back)

        random.shuffle(cards)

        dump.empty()
        self.add(cards)

class Dump(sprite.LayeredUpdates):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.rect = Rect(pos.x, pos.y, 130, 180)
    
    def add(self, *sprites, **kwargs):
        super().add(*sprites, **kwargs)

        for sprite in sprites:
            if type(sprite) == Card:
                sprite.rect.x = self.pos.x
                sprite.rect.y = self.pos.y

    def update(self, selected_cards):
        super().update()

        cursor = InputManager.cursor_pos
        rel_cursor = InputManager.cursor_rel_pos

        left_clicked = InputManager.MOUSE_LEFT_DOWN()
        left_lifted = InputManager.MOUSE_LEFT_UP()

        sprites = self.sprites()

        x_offset = 24
        for i, card in enumerate(reversed(sprites[-1:-4:-1])):
            if not card.selected:
                card.rect.x = self.pos.x
                card.rect.x += x_offset * i
        
        if not sprites:
            return

        sprite = sprites[-1]

        if left_lifted and sprites[-1].selected:
            sprites[-1].selected = False
            sprites[-1].rect.x = self.pos.x
            sprites[-1].rect.y = self.pos.y
        elif sprites[-1].selected:
            sprites[-1].rect.x += rel_cursor[0]
            sprites[-1].rect.y += rel_cursor[1]

        if left_clicked and sprite.rect.collidepoint(cursor):
            selected_cards.append(sprites[-1])
            sprites[-1].selected = True

class Stack(sprite.LayeredUpdates):
    def __init__(self, pos):
        super().__init__()

        self.pos: Vector2 = pos
        self.rect = Rect(pos.x, pos.y, 130, 180)
        self.prev = 0

    def add(self, *sprite, **kwargs):
        super().add(*sprite, **kwargs)

        if sprite:
            sprite[0].rect.x = self.pos.x
            sprite[0].rect.y = self.pos.y

    def drop(self, card):
        cursor = InputManager.cursor_pos
        if self.rect.collidepoint(cursor):
            if self.sprites():
                top = self.get_top_sprite()
                rank_val = top.rank.value
                suit = top.suit

                if card.rank.value == rank_val + 1 and card.suit == suit:
                    g = card.groups()[0]
                    g.remove(card)
                    if g.sprites():
                        g.get_top_sprite().flip_up()

                    self.add(card)
                    return True
                else:
                    return False
            else: 
                if card.rank == Rank.ACE:
                    g = card.groups()[0]
                    g.remove(card)
                    if g.sprites():
                        g.get_top_sprite().flip_up()

                    self.add(card)
                    return True
                else:
                    return False

        return False

    def update(self, selected_cards):

        cursor = InputManager.cursor_pos
        rel_cursor = InputManager.cursor_rel_pos

        left_clicked = InputManager.MOUSE_LEFT_DOWN()
        left_lifted = InputManager.MOUSE_LEFT_UP()


        sprites = self.sprites()
        
        if not sprites:
            return

        if left_lifted and sprites[-1].selected:
            sprites[-1].selected = False
            sprites[-1].rect.x = self.pos.x
            sprites[-1].rect.y = self.pos.y
        elif sprites[-1].selected:
            sprites[-1].rect.x += rel_cursor[0]
            sprites[-1].rect.y += rel_cursor[1]

        if left_clicked and self.rect.collidepoint(cursor):
            selected_cards.append(sprites[-1])
            sprites[-1].selected = True


        
class Tableau(sprite.LayeredUpdates):
    """
    tableaux are the 7 lower card piles
    maintain the following invariants:
        1. each face-up card must be 1 rank lower 
            than the face-up card below it
        2. each face-up card must be the opposite 
            color (red/blue) of the face-up card below it
    """

    def __init__(self, pos: Vector2):
        super().__init__()

        self.pos: Vector2 = pos
        self.rect = Rect(pos.x, pos.y, 130, 180)

    def update(self, selected_cards):
        super().update(InputManager.cursor_pos)

        cursor = InputManager.cursor_pos
        rel_cursor = InputManager.cursor_rel_pos

        left_clicked = InputManager.MOUSE_LEFT_DOWN()
        left_lifted = InputManager.MOUSE_LEFT_UP()


        y_offset = 0
        sprites = self.sprites()

        if left_lifted:
            for card in sprites:
                card.selected = False

        for card in sprites:
            if not card.selected:
                card.rect.x = self.pos.x
                card.rect.y = self.pos.y + y_offset
            else:
                card.rect.move_ip(rel_cursor)

            y_offset += 24

        card_idx = len(sprites) - 1
        clicked_idx = -1


        if left_clicked:
            for card in reversed(sprites):
                if card.faceup and card.rect.collidepoint(cursor):
                    clicked_idx = card_idx
                    break
                    
                card_idx -= 1

            if clicked_idx != -1:
                for i in range(clicked_idx, len(sprites)):
                    selected_cards.append(sprites[i])
                    sprites[i].selected = True

    def drop_stack(self, selected_cards):
        cursor = InputManager.cursor_pos
        bot_select = selected_cards[0]

        if bot_select.groups()[0] == self:
            return False

        if not self.sprites():
            collider: Rect = self.rect
            if collider.collidepoint(cursor):
                if bot_select.rank != Rank.KING:
                    return False
                else:
                    tab: Tableau = selected_cards[0].groups()[0]
                    tab.remove(selected_cards)

                    if tab.sprites():
                        tab.get_top_sprite().flip_up()

                    self.add(selected_cards)
                    return True

        else:
            top_sprite = self.get_top_sprite() 
            collider = top_sprite.rect
            if collider.collidepoint(cursor):
                if top_sprite.rank.value - 1 != bot_select.rank.value:
                    return False
                if top_sprite.color == bot_select.color:
                    return False
                else:
                    tab: Tableau = selected_cards[0].groups()[0]
                    # want to reset the selected_cards array but not re-add these

                    tab.remove(selected_cards)

                    if tab.sprites():
                        tab.get_top_sprite().flip_up()

                    self.add(selected_cards)
                    return True

