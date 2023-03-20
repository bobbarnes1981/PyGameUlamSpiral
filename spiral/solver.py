import logging
import pygame
import random
import time

class App(object):
    def __init__(self, delay: float) -> None:
        self._delay = delay

        self._rows = 127
        self._cols = 127
        self._cellheight = 5
        self._cellwidth = 5

        self._running = True
        self._display_surf = None
        self._width = self._cols * self._cellwidth
        self._height = self._rows * self._cellheight
        self._size = (self._width, self._height)
        self._time = time.time()
        self._counter = 0
        self._complete = False

        self._grid = []
        for r in range(0, self._rows):
            for c in range(0, self._cols):
                self._grid.append(0)
        print(self._grid)
        step_count = 0
        max_steps = 1
        loop_count = 0
        max_loops = 2
        x = self._rows//2
        y = self._cols//2
        dir_x = +1
        dir_y = 0
        for i in range(0, self._cols * self._rows):
            p = self.is_prime(i+1)
            print('{0}{1}'.format(i+1, 'P' if p else ''))
            index = x+(self._cols*y)
            print('num {0} coord ({1},{2}) index {3} [loop {4} of {5}][step {6} of {7}]'.format(i+1, x, y, index, loop_count, max_loops, step_count, max_steps))
            if p:
                self._grid[index] = i+1
            else:
                self._grid[index] = None
            x += dir_x
            y += dir_y
            step_count += 1
            if step_count >= max_steps:
                step_count = 0
                loop_count += 1
                if dir_x > 0:
                    print('n')
                    dir_x = 0
                    dir_y = -1
                elif dir_x < 0:
                    print('s')
                    dir_x  = 0
                    dir_y = +1
                elif dir_y > 0:
                    print('e')
                    dir_x = +1
                    dir_y = 0
                elif dir_y < 0:
                    print('w')
                    dir_x = -1
                    dir_y = 0
                if loop_count >= max_loops:
                    loop_count = 0
                    max_steps += 1
    def is_prime(self, num):
        # slow prime calc
        if num == 1:
            return False
        if num == 2:
            return True
        if num % 2 == 0:
            return False
        for i in range(3, num, 2):
            if num % i == 0:
                return False
        return True
    def on_init(self) -> None:
        pygame.init()
        pygame.display.set_caption("Title")
        self._display_surf = pygame.display.set_mode(self._size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        #self.font = pygame.font.SysFont('courier.ttf', 72)
        font_name = pygame.font.get_default_font()
        logging.info("System font: {0}".format(font_name))
        self.font_s = pygame.font.SysFont(None, 22)
        self.font_l = pygame.font.SysFont(None, 33)
        return True
    def on_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == 27:
                self._running = False
        else:
            logging.debug(event)
    def on_loop(self, elapsed: float) -> None:
        self._counter+=elapsed
        if self._counter > self._delay:
            logging.info("tick")
            self._counter = 0
            if self._complete == False:
                pass
    def on_render(self) -> None:
        self._display_surf.fill((0,0,0))
        for r in range(0, self._rows):
            for c in range(self._cols):
                num = self._grid[c+(r*self._cols)]
                if num != None:
                    pygame.draw.rect(self._display_surf, (255,255,255), (c*self._cellwidth, r*self._cellheight, self._cellwidth, self._cellheight), 0)
                    #text = str(self._grid[c+(r*self._cols)])
                    #img = self.font_s.render(text, True, (255,255,255))
                    #self._display_surf.blit(img, (c*self._cellwidth, r*self._cellheight))
        pygame.display.update()
    def on_cleanup(self) -> None:
        pygame.quit()
    def on_execute(self) -> None:
        if self.on_init() == False:
            self._running = False
        while self._running:
            current = time.time()
            elapsed = current - self._time
            self._time = current
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop(elapsed)
            self.on_render()
        self.on_cleanup()
