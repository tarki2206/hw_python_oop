class InfoMessage:
    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    M_IN_KM = 1000
    LEN_STEP = 0.65
    H_IN_M = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        mean_speed = self.get_distance() / self.duration
        return round(mean_speed, 6)

    def get_spent_calories(self) -> float:
        pass

    def show_training_info(self) -> InfoMessage:
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(type(self).__name__, self.duration,
                           distance, speed, calories)


class Running(Training):
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self):
        spend_calories = \
            (Running.CALORIES_MEAN_SPEED_MULTIPLIER
             * self.get_mean_speed() + Running.CALORIES_MEAN_SPEED_SHIFT)\
            * self.weight / Training.M_IN_KM * (self.duration * 60)
        return round(spend_calories, 3)


class SportsWalking(Training):
    cal_op = 0.035
    cal_op2 = 0.029
    M_IN_SEK = 0.278
    S_TO_M = 100

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        spend_calories = \
            ((self.cal_op * self.weight + ((self.get_mean_speed()
              * self.M_IN_SEK) ** 2 / (self.height / self.S_TO_M))
              * self.cal_op2 * self.weight) * (self.duration * 60))
        return spend_calories


class Swimming(Training):
    LEN_STEP = 1.38
    M_SP = 1.1
    CON = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        mean_speed = \
            self.length_pool * self.count_pool / \
            self.M_IN_KM / self.duration
        return mean_speed

    def get_spent_calories(self):
        spend_calories = \
            (self.get_mean_speed() + self.M_SP)\
            * self.CON * self.weight * self.duration
        return spend_calories


def read_package(workout_type: str, data: list) -> Training:
    workout_dict = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }

    if workout_type not in workout_dict:
        raise ValueError(f"Unsupported workout type '{workout_type}'")

    workout_class = workout_dict[workout_type]
    workout = workout_class(*data)
    return workout


def main(training: Training) -> None:
    info = training.show_training_info()
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
