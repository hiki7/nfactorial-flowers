from fastapi import FastAPI, Response, Form
from attrs import define, asdict
from typing import Union


@define
class Flower:
    id: int
    title: str
    color: str
    count: int


class FlowersRepository:
    def __init__(self):
        self.flowers = [
            Flower(id=1, title="rozy", color="blue", count=1),
            Flower(id=2, title="tulpan", color="red", count=2),
            Flower(id=3, title="cart", color="yellow", count=3),
        ]

    def get_all(self) -> list[Flower]:
        return self.flowers

    def get_one(self, id: int) -> Union[Flower, None]:
        for flower in self.flowers:
            if flower.id == id:
                return flower
        return None

    def save(self, flower: Flower):
        flower.id = len(self.flowers) + 1
        self.flowers.append(flower)

    def update(self, id: int, input: Flower):
        #v.1
        # for flower in self.flowers:
        #     if flower.id == id:
        #         flower = input

        #v.2
        # for i in range(len(self.flowers)):
        #     if self.flowers[i].id == id:
        #         input.id = id
        #         self.flowers[i] = input

        #v.3
        for i, flower in enumerate(self.flowers):
            if flower.id == id:
                input.id = id
                self.flowers[i] = input

    def delete(self, id: int):
        for i, flower in enumerate(self.flowers):
            if flower.id == id:
                del self.flowers[i]

app = FastAPI()
repo = FlowersRepository()

@app.get("/flowers")
def get_flowers():
    flowers = repo.get_all()

    results = []
    for flower in flowers:
        dict_flower = asdict(flower)
        results.append(dict_flower)
    return results

@app.post('/flowers')
def post_flowers(
    title: str,
    color: str,
    count: int,
):
    tmp = Flower(id=0, title=title, color=color, count=count)
    repo.save(tmp)
    return Response(status_code=200)


@app.patch('/flowers/{id}')
def patch_flower(
        id: int,
        title: str = Form(),
        color: str = Form(),
        count: int = Form(),
):
    tmp = Flower(title=title, color=color, count=count)
    repo.update(id, tmp)
    return {}


@app.delete('/flowers/{id}')
def delete_flower(id: int):
    repo.delete(id)
    return {}