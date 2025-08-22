from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import text
from sqlalchemy.ext.declarative import declarative_base

class SQLConst:
    __BASE = declarative_base()


class Summoners(SQLConst._SQLConst__BASE):
    __tablename__ = "Summoners"

    id = Column(Integer, primary_key=True, index=True)
    assists = Column(Integer)
    championName = Column(String[32])
    champLevel = Column(Integer)
    championId = Column(Integer)
    deaths = Column(Integer)
    individualPosition = Column(String[8])
    item0 = Column(Integer)
    item1 = Column(Integer)
    item2 = Column(Integer)
    item3 = Column(Integer)
    item4 = Column(Integer)
    item5 = Column(Integer)
    item6 = Column(Integer)
    kills = Column(Integer)
    totalHeal = Column(Integer)
    totalHealsOnTeammates = Column(Integer)
    magicDamageDealt = Column(Integer)
    magicDamageDealtToChampions = Column(Integer)
    magicDamageTaken = Column(Integer)
    physicalDamageDealt = Column(Integer)
    physicalDamageDealtToChampions = Column(Integer)
    physicalDamageTaken = Column(Integer)
    trueDamageDealt = Column(Integer)
    trueDamageDealtToChampions = Column(Integer)
    trueDamageTaken = Column(Integer)
    teamId = Column(Integer)
    summoner1Id = Column(Integer)
    summoner2Id = Column(Integer)
    puuid = Column(String[78])
    match_id = Column(String[16])
    main_runes_style = Column(Integer)
    second_runes_style = Column(Integer)
    main_rune1 = Column(Integer)
    main_rune2 = Column(Integer)
    main_rune3 = Column(Integer)
    main_rune4 = Column(Integer)
    secondary_rune1 = Column(Integer)
    secondary_rune2 = Column(Integer)

class Matches(SQLConst._SQLConst__BASE):
    __tablename__ = "Matches"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(String[16])
    gameDuration = Column(Integer)
    gameMode = Column(String[16])
    gameVersion = Column(String[16])
    queueId = Column(Integer)
    winnerId = Column(Integer)


class LoLdatabase:
    def __init__(self, logi="lol_analytic", passw="D73e55g6t08ru!", db="lol_db"):
        self.__DATABASE_URL = f"postgresql://{logi}:{passw}@localhost/{db}"
        self.__ENGINE = create_engine(self.__DATABASE_URL, echo=True)
        
    def make_db(self) -> None:
        SQLConst._SQLConst__BASE.metadata.create_all(self.__ENGINE)
    
    def truncate_db(self) -> None:
        with self.__ENGINE.connect() as connection:
            with connection.begin():
                for table in reversed(SQLConst._SQLConst__BASE.metadata.sorted_tables):
                    connection.execute(text(f"TRUNCATE TABLE \"{table.name}\" CASCADE;"))
                    connection.execute(text(f'DROP TABLE IF EXISTS "{table}" CASCADE;'))
    
    def add_data(self, summoner_data, match_data):
        summoner_data.to_sql("Summoners", self.__ENGINE, if_exists="append", index=False)
        match_data.to_sql("Matches", self.__ENGINE, if_exists="append", index=False)
        