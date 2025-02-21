from pydantic import BaseModel, Field
from typing import List, Literal, Union, Annotated


class PRRTest(BaseModel):
    type: Literal["PRR"]
    part_number: int = Field(ge=-2_147_483_648, le=2_147_483_647)
    pass_fail: int = Field(ge=0, le=1)


class PTRTest(BaseModel):
    type: Literal["PTR"]
    test_name: str = Field(max_length=20)
    test_value: float = Field(ge=-3.40282e38, le=3.40282e38)
    low: float = Field(ge=-3.40282e38, le=3.40282e38)
    high: float = Field(ge=-3.40282e38, le=3.40282e38)
    pass_fail: int = Field(ge=0, le=1)

Test = Annotated[Union[PRRTest, PTRTest], Field(discriminator="type")]

class EditFileRequest(BaseModel):
    filename: str
    operator: str = Field(max_length=20)
    temperature: int =  Field(ge=-273, le=2_147_483_647)
    tests: List[Test]

