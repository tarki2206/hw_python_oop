from dataclasses import dataclass
from typing import Type, Dict


@dataclass
class InfoMessage:
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    M_IN_KM: float = 1000
    LEN_STEP: float = 0.65
    HOUR_IN_MIN: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        raise NotImplementedError('The method "get_spent_calories" '
                                  'should be overridden in the subclasses.')

    def show_training_info(self) -> InfoMessage:
        distance: float = self.get_distance()
        speed: float = self.get_mean_speed()
        calories: float = self.get_spent_calories()
        return InfoMessage(type(self).__name__, self.duration,
                           distance, speed, calories)


class Running(Training):
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        return ((Running.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + Running.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / Training.M_IN_KM
                * (self.duration * 60))


class SportsWalking(Training):
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_HEIGHT_MULTIPLIER: float = 0.029
    METERS_IN_SEK: float = 0.278
    SM_TO_METERS: int = 100

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_WEIGHT_MULTIPLIER
                * self.weight + ((self.get_mean_speed()
                 * self.METERS_IN_SEK) ** 2
                 / (self.height / self.SM_TO_METERS))
                * self.CALORIES_HEIGHT_MULTIPLIER
                * self.weight) * (self.duration * 60))


class Swimming(Training):
    LEN_STEP: float = 1.38
    CALORIES_SWIM_ADDENDUM: float = 1.1
    CALORIES_SWIM_MULTIPLIER: int = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.CALORIES_SWIM_ADDENDUM)
                * self.CALORIES_SWIM_MULTIPLIER * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    workout_dict: Dict[str, Type[Training]] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }

    if workout_type not in workout_dict:
        raise ValueError(f"Unsupported workout type '{workout_type}'")

    workout_class: Type[Training] = workout_dict[workout_type]
    return workout_class(*data)


def main(training: Training) -> None:
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':

    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for training_type, data in packages:
        training = read_package(training_type, data)
        main(training)
