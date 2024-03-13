import inspect
import os
import sys
import pygame
from miniworldmaker_physics.physics_board import PhysicsBoard
from miniworldmaker_physics.physics_board_connector import PhysicsBoardConnector
from miniworldmaker_physics.physicsboard_event_manager import PhysicsBoardEventManager
from miniworldmaker_physics.token_physics_position_manager import PhysicsBoardPositionManager
from miniworldmaker_physics.token_physics import TokenPhysics

pygame.init()

# __import__('pkg_resources').declare_namespace(__name__)
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

__all__ = []


__all__.append(PhysicsBoard.__name__)
