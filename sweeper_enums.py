from enum import Enum
import pygame
pygame.font.init()


class SweeperFonts(Enum):
    ARIAL_16 = pygame.font.Font(pygame.font.match_font("ArialRounded"), 16)
    ARIAL_18 = pygame.font.Font(pygame.font.match_font("ArialRounded"), 18)
    ARIAL_20 = pygame.font.Font(pygame.font.match_font("ArialRounded"), 20)
    ARIAL_22 = pygame.font.Font(pygame.font.match_font("ArialRounded"), 22)
    NOVA_16 = pygame.font.Font(pygame.font.match_font("NovaMono"), 16)
    NOVA_18 = pygame.font.Font(pygame.font.match_font("NovaMono"), 18)
    NOVA_20 = pygame.font.Font(pygame.font.match_font("NovaMono"), 20)
    NOVA_22 = pygame.font.Font(pygame.font.match_font("NovaMono"), 22)
    ANDALE_16 = pygame.font.Font(pygame.font.match_font("AndaleMono"), 16)
    ANDALE_18 = pygame.font.Font(pygame.font.match_font("AndaleMono"), 18)
    ANDALE_20 = pygame.font.Font(pygame.font.match_font("AndaleMono"), 20)
    ANDALE_22 = pygame.font.Font(pygame.font.match_font("AndaleMono"), 22)
    ACADEMY_16 = pygame.font.Font(pygame.font.match_font("AcademyEngravedLETFonts"), 16)
    ACADEMY_18 = pygame.font.Font(pygame.font.match_font("AcademyEngravedLETFonts"), 18)
    ACADEMY_20 = pygame.font.Font(pygame.font.match_font("AcademyEngravedLETFonts"), 20)
    ACADEMY_22 = pygame.font.Font(pygame.font.match_font("AcademyEngravedLETFonts"), 22)
    FUTURA_16 = pygame.font.Font(pygame.font.match_font("Futura"), 16)
    FUTURA_18 = pygame.font.Font(pygame.font.match_font("Futura"), 18)
    FUTURA_20 = pygame.font.Font(pygame.font.match_font("Futura"), 20)
    FUTURA_22 = pygame.font.Font(pygame.font.match_font("Futura"), 22)
