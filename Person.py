class Person():
    def __init__(self,client,roomId,nickname) -> None:
        self.client=client
        self.roomId=roomId
        self.nickname=nickname
    def __str__(self) -> str:
        return self.nickname

    