import sqlalchemy as sa
import sqlalchemy.ext.declarative as dec
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(db_file):
    global __factory
    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=True'
    print(f"Подключение к базе данных по адресу {conn_str}")

    try:
        engine = sa.create_engine(conn_str, echo=False)
        print('engine is', engine)
        __factory = orm.sessionmaker(bind=engine)

        SqlAlchemyBase.metadata.create_all(engine)
    except Exception as e:
        print("can't initialize the sql database, reason:", e)
        exit()

def create_session() -> Session:
    global __factory
    print('__factory is', __factory)
    return __factory()