from locust import LoadTestShape
from config.config import cfg


class CustomLoadShape(LoadTestShape):
    match cfg.loadshape_type:
        case "baseline":
            stages = [
                {"duration": 120, "users": 1, "sapwn_rate": 1}
            ]

        case "fixedload":
            stages = [
                {"duration": 300, "users": 10, "sapwn_rate": 2}
            ]

        case "stages":
            stages = [
                {"duration": 30, "users": 10, "sapwn_rate": 2},
                {"duration": 60, "users": 20, "sapwn_rate": 2},
                {"duration": 90, "users": 30, "sapwn_rate": 2},
                {"duration": 120, "users": 40, "sapwn_rate": 2},
                {"duration": 150, "users": 50, "sapwn_rate": 2}
            ]
    """
        Здесь должны быть описаны типы нагрузки с помощью stages
    """

    def tick(self): # стандартная функция локаста, взятая из документации, для работы с кастомными "Лоад-Шейпами"
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None


class CustomLoadShape:
    pass