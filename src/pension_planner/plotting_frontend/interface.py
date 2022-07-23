from abc import ABC, abstractmethod

from src.pension_planner.frontend.ipyvuetify.components.main.main import Main


class AbstractPlottingFrontend(ABC):
    main: Main

    @abstractmethod
    def update_with(self, x: list[float], y: list[float]) -> None:
        ...
