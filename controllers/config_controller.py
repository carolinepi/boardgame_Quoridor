import dataclasses
import trafaret as t
# from trafaret_config import read_and_validate


CONFIG_TRAFARET = t.Dict({
    'app': t.Dict({
        'n': t.Int(),
        'square_size': t.Int(),
        'inner_size': t.Int(),
    })
})


@dataclasses.dataclass
class Config:
    n: int
    square_size: int
    inner_size: int


# class ConfigController:
#     def __init__(self, config_path: str):
#         self.config_path = config_path
#
#     def parse_config(self) -> Config:
#         config = read_and_validate(self.config_path, CONFIG_TRAFARET)
#         if config is None:
#             raise RuntimeError(f'Config not found: {config}')
#         return Config(**config['app'])
