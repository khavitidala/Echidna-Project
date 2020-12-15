import sys
import pygame
import time
import random

class Button:
    def __init__(self, sortApp, text, width, height, position, color, font):
        self.screen = sortApp.screen
        self.screenRect = self.screen.get_rect()

        #properti dan dimensi
        self.width, self.height = width, height
        self.buttonColor = color
        self.textColor = font[2]
        self.font = pygame.font.SysFont(font[0], font[1])

        #bikin objek rectangle dari button terus simpen di tengah bawah
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.x = position[0]
        self.rect.y = position[1]

        #The button message needs to be prepped only once.
        self._prep_msg(text)
    
    def _prep_msg(self, text):
        self.msg_image = self.font.render(text, True, self.textColor, self.buttonColor)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #draw blank button and then draw message.
        self.screen.fill(self.buttonColor, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

class Sort_screen:
    def __init__(self, sortApp, width, height, border, color, border_color, position):
        self.screen = sortApp.screen
        self.x = position[0]
        self.y = position[1]
        self.color = color
        self.width = width
        self.height = height
        self.border = border
        self.border_color = border_color
        self.surf = pygame.Surface((self.width+self.border*2, self.height+self.border*2), pygame.SRCALPHA)
    
    def create_rect(self):
        pygame.draw.rect(self.surf, self.color, (self.border, self.border, self.width, self.height), 0)
        for i in range(1, self.border):
            pygame.draw.rect(self.surf, self.border_color, (self.border-i, self.border-i, self.width+5, self.height+5), 1)
        return self.surf
    
    def draw_rect(self):
        self.rect_surf1 = self.create_rect()
        self.screen.blit(self.rect_surf1, (self.x , self.y))

class Sort_Object:
    def __init__(self, sortApp, position, color, maxwidth, maxheight):
        self.screen = sortApp.screen
        self.start_x = position[0]
        self.start_y = position[1]
        self.color = color
        self.maxwidth = maxwidth-3
        self.maxheight = float(maxheight-3)
        self.list_object = self.generate_list_of_rect()
        self.list_of_rect = self.generate_rect()

    def generate_list_of_rect(self):
        self.list_object = []
        random.seed(5)
        partHeight = self.maxheight/100
        for i in range(0, 101):
            partWidth = random.randint(2, self.maxwidth-1)
            if i == 0:
                posX = float(self.start_x)
                posY = float(self.start_y)
            else:
                posY += partHeight
            self.list_object.append({"width": partWidth, "color": self.color, "height": partHeight,"posX": posX,"posY": posY})
        return self.list_object
    
    def generate_rect(self):
        self.list_of_rect = []
        for i in self.list_object:
            self.rect = pygame.Rect(0, 0, i["width"], i["height"])
            self.rect.x = i["posX"]
            self.rect.y = i["posY"]
            self.list_of_rect.append(self.rect)
        return self.list_of_rect
            
    def draw_sort(self):
        for i in range(len(self.list_object)):
            pygame.draw.rect(self.screen, self.list_object[i]["color"], self.list_of_rect[i])
    
    #self.screen.fill(i["color"], self.rect)

class Sorting:
    def __init__(self, sortApp, defaultColor):
        self.sortApp = sortApp
        self.color = (0, 0, 0)
        self.bg_color = sortApp.bg_color
        self.screen = sortApp.screen
        self.sel_listObject = sortApp.sel_list
        self.ins_listObject = sortApp.ins_list
        self.sel_listOfRect = sortApp.sel_rect
        self.ins_listOfRect = sortApp.ins_rect
        self.defaultColor = defaultColor

    def sel_draw_obj(self, index):
        self.rect = pygame.Rect(0, 0, self.sel_listObject[index]["width"], self.sel_listObject[index]["height"])
        self.rect.x = self.sel_listObject[index]["posX"]
        self.rect.y = self.sel_listObject[index]["posY"]
        self.sortApp._reset_screen_without_sortObj()
        self.sel_listOfRect[index] = self.rect
        for i in range(len(self.sel_listObject)):
            pygame.draw.rect(self.screen, self.sel_listObject[i]["color"], self.sel_listOfRect[i])
        self.change_rect2 = pygame.Rect(20, 80, 320, 500)
        pygame.display.update(self.change_rect2)

    def selection_sort(self):
        self.size = len(self.sel_listObject)
        for step in range(self.size):
            min_idx = step
            self.sel_listObject[step]["color"] = (0, 0, 0)
            self.sel_draw_obj(step)
            for i in range(step + 1, self.size):
                self.sel_listObject[i]["color"] = (255, 255, 255)
                self.sel_draw_obj(i)
                self.sel_listObject[min_idx]["color"] = (0, 0, 0)
                self.sel_draw_obj(min_idx)
                if self.sel_listObject[i]["width"] < self.sel_listObject[min_idx]["width"]:
                    self.sel_listObject[min_idx]["color"] = self.defaultColor
                    self.sel_draw_obj(min_idx)
                    min_idx = i
                    self.sel_listObject[min_idx]["color"] = (0, 0, 0)
                    self.sel_draw_obj(min_idx)
                self.sel_listObject[i]["color"] = self.defaultColor
                self.sel_draw_obj(i)
            temp_index = step
            t = self.sel_listObject[step]["width"]
            self.sel_listObject[step]["width"] = self.sel_listObject[min_idx]["width"]
            self.sel_listObject[min_idx]["width"] = t
            self.sel_draw_obj(step)
            self.sel_draw_obj(min_idx)
            self.sel_listObject[temp_index]["color"] = self.defaultColor
            self.sel_draw_obj(temp_index)
            
    
    def ins_draw_obj(self, index):
        self.rect = pygame.Rect(0, 0, self.ins_listObject[index]["width"], self.ins_listObject[index]["height"])
        self.rect.x = self.ins_listObject[index]["posX"]
        self.rect.y = self.ins_listObject[index]["posY"]
        self.sortApp._reset_screen_without_sortObj()
        self.ins_listOfRect[index] = self.rect
        for i in range(len(self.sel_listObject)):
            pygame.draw.rect(self.screen, self.ins_listObject[i]["color"], self.ins_listOfRect[i])
        self.change_rect = pygame.Rect(self.sortApp.ins_dinst, 80, 320, 500)
        pygame.display.update(self.change_rect)

    def insertionSort(self):
        self.size = len(self.ins_listObject)  
        for i in range(1, self.size): 
            key = self.ins_listObject[i]["width"] 
            self.ins_listObject[i]["color"] = (0, 0, 0)
            self.ins_draw_obj(i)
            j = i-1
            while j >= 0 and key < self.ins_listObject[j]["width"]  :
                    self.ins_listObject[j]["color"] = (0, 0, 0)
                    self.ins_draw_obj(i) 
                    self.ins_listObject[j + 1]["width"] = self.ins_listObject[j]["width"]
                    self.ins_draw_obj(j+1)
                    self.ins_listObject[j]["color"] = self.defaultColor
                    self.ins_draw_obj(i) 
                    j -= 1
            self.ins_listObject[i]["color"] = self.defaultColor
            self.ins_draw_obj(i)
            self.ins_listObject[j + 1]["width"] = key
            self.ins_draw_obj(j+1)
            

class Echidna:
    def __init__(self):
        pygame.init()
        self.width = 720
        self.height = 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Selection and Insertion Sorting Algorithm Visualizer")
        self.bg_color = (230, 230, 230)
        self.selection_screen = Sort_screen(self, 320, 500, 5, self.bg_color, (0, 0, 0), (20, 80))
        self.sel_surf = self.selection_screen.surf.get_rect()
        self.ins_dinst = 30+self.selection_screen.width+20
        self.insertion_screen = Sort_screen(self, 320, 500, 5, self.bg_color, (0, 0, 0), (self.ins_dinst, 80))
        self.ins_surf = self.insertion_screen.surf.get_rect()
        self.selection_obj = Sort_Object(self, (25, 85), (4, 133, 253), self.selection_screen.width, self.selection_screen.height)
        self.insertion_obj = Sort_Object(self, (35+self.selection_screen.width+20, 85), (4, 133, 253), self.insertion_screen.width, self.insertion_screen.height)
        self.sel_rect = self.selection_obj.list_of_rect
        self.ins_rect = self.insertion_obj.list_of_rect
        self.sel_list = self.selection_obj.list_object
        self.ins_list = self.insertion_obj.list_object
        self.sel_sorting = Sorting(self, (4, 133, 253))
        #button
        self.sort_button = Button(self, "Sort", 200, 50, (self.screen.get_rect().centerx-100,self.height-10-80), (0, 0, 0), ("Arial", 48, (255, 255, 255)))
        self.sel_title = Button(self, "Selection", 200, 50, (75,25), self.bg_color, ("Arial", 32, (0, 0, 0)))
        self.ins_title = Button(self, "Insertion", 200, 50, (self.selection_screen.width+30+75,25), self.bg_color, ("Arial", 32, (0, 0, 0)))

    def run_app(self):
        while True:
            self._check_events()
            self._update_screen()
            
    
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                button_clicked = self.sort_button.rect.collidepoint(mouse_pos)
                if button_clicked:
                    self.sel_sorting.selection_sort()
                    self.sel_sorting.insertionSort()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.sel_sorting.selection_sort()
                if event.key == pygame.K_w:
                    self.sel_sorting.insertionSort()
                

    #def _check_button(self, mouse_pos):
    def _reset_screen_without_sortObj(self):
        self.screen.fill(self.bg_color)
        self.selection_screen.draw_rect()
        self.insertion_screen.draw_rect()
        self.sort_button.draw_button()
        self.sel_title.draw_button()
        self.ins_title.draw_button()

    def _update_screen(self):
        self._reset_screen_without_sortObj()
        self.selection_obj.draw_sort()
        self.insertion_obj.draw_sort()
        pygame.display.flip()

if __name__ == '__main__':
    echidna = Echidna()
    echidna.run_app()