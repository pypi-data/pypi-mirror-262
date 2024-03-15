from pydantic import BaseModel, field_validator

# class ScopedConfig(BaseModel):
#     host: str = '0.0.0.0'
#     port: int = 5180

#     @field_validator('port')
#     @classmethod
#     def check_port(cls, port: int):
#         assert 0 <= port <= 65535

#         if port <= 1024:
#             raise Warning('It is best to use a port number greater than 1024')

class Config(BaseModel):
    # wsshd: ScopedConfig
    pass
