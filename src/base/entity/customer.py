from sqlalchemy import Column, Integer, String
from src.base.entity.base import Base


class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

    def __int__(self, name, fullname, nickname):
        self.name = name
        self.nickname = nickname
        self.fullname = fullname

    def __repr__(self):
        return "<Customer(name='%s', fullname='%s', nickname='%s')>" % (
            self.name,
            self.fullname,
            self.nickname,
        )

    def create(self, session):
        session.add(self)
        session.flush()

    def update(self, session):
        session.query(Customer).filter(
            Customer.id == self.id
        ).update(
            name=self.name,
            fullname=self.fullname,
            nickname=self.nickname
        ).commit()


    @staticmethod
    def get_all(session):
        return session.query(Customer).all()
