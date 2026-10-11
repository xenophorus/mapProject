from sqlalchemy import create_engine, Table, String, Integer, UUID, Column, Float
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, Session

DB_URL = "postgresql+psycopg2://alex:gigapass@localhost:5432/playground"

engine = create_engine(DB_URL, echo=True)

class Base(DeclarativeBase):
    pass

class PostOffice(Base):
    __tablename__ = "post_offices"
    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    region: Mapped[String] = mapped_column(String)
    district: Mapped[String] = mapped_column(String, nullable=True)
    settlementOrCity: Mapped[String] = mapped_column(String)
    settlementTypeOrCityType: Mapped[String] = mapped_column(String)
    shortAddress: Mapped[String] = mapped_column(String)
    postalCode: Mapped[String] = mapped_column(String)
    typeCode: Mapped[String] = mapped_column(String)
    typeId: Mapped[Integer] = mapped_column(Integer)
    latitude: Mapped[Float] = mapped_column(Float)
    longitude: Mapped[Float] = mapped_column(Float)

def add_data(offices):
    with Session(engine) as session:
        session.add_all(offices)
        session.commit()


if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

