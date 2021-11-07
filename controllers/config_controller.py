import dataclasses
import trafaret as t


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
