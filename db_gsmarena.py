import mysql.connector
import sqlalchemy as db
from sqlalchemy import String,Integer,VARCHAR,Float, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy.orm import sessionmaker
import csv
import pandas as pd


password_DB = input('Enter the MySQL password:\n')
connection_string = f'mysql+mysqlconnector://root:{password_DB}@localhost'
engine = db.create_engine(connection_string)

#---------------- create new DB-----------------

DB_name = 'gsmarena_db'
with engine.connect() as conn:
    conn.execute(db.text(f"DROP DATABASE IF EXISTS {DB_name}"))
    conn.execute(db.text(f"CREATE DATABASE {DB_name}"))
    conn.execute(db.text(f"USE {DB_name}"))

connection_string = f'mysql+mysqlconnector://root:{password_DB}@localhost/{DB_name}'
engine = db.create_engine(connection_string)
Session=sessionmaker(bind=engine)
#-------------------create Tables-----------------------
Base=declarative_base()

#---device Table-----
class Devices(Base):
    __tablename__ = 'device'
    id : Mapped [int] = mapped_column(Integer,primary_key=True)
    name: Mapped [str]= mapped_column(String(128),nullable=True)
    year : Mapped [int] = mapped_column(Integer,nullable=True)
    category : Mapped [str] = mapped_column(String(8),nullable=True)
    price : Mapped [int]= mapped_column(Float,nullable=True)
    battery_type : Mapped [str] = mapped_column(String(16),nullable=True)
    battery_capacity : Mapped [int] = mapped_column(Integer,nullable=True)
    main_camera_num : Mapped [int] = mapped_column(Integer,nullable=True)
    selfie_camera_num : Mapped [int] = mapped_column(Integer,nullable=True)

    BRAND : Mapped ["Brands"] = relationship(back_populates="DEVICE1")
    BODY : Mapped ["Bodies"] = relationship(back_populates="DEVICE2")
    DISPLAY : Mapped["Displays"] = relationship(back_populates="DEVICE3")
    NETWORK : Mapped["Networks"] = relationship(back_populates="DEVICE4")
    SENSOR: Mapped["Sensors"] = relationship(back_populates="DEVICE5")
    CPU: Mapped["Processors"] = relationship(back_populates="DEVICE6")
    MEMORY: Mapped["Memories"] = relationship(back_populates="DEVICE7")
    RAM: Mapped["Rams"] = relationship(back_populates="DEVICE8")
    SIM_T: Mapped ["Sim_Types"] = relationship(back_populates="DEVICE9")
    SIM_N : Mapped ["Sim_Nums"] = relationship(back_populates="DEVICE10")
    OS : Mapped["OSs"] = relationship(back_populates="DEVICE11")
    SOUND: Mapped["Sounds"] = relationship(back_populates="DEVICE12")
    COMMS : Mapped ["Communications"] = relationship(back_populates="DEVICE13")

#-------brand Table---------
class Brands(Base):
    __tablename__ = 'brand'
    id: Mapped [int] = mapped_column(Integer,primary_key=True,autoincrement=True,nullable=True)
    device_id: Mapped [int] = mapped_column(Integer,ForeignKey('device.id'),nullable=True)
    brand: Mapped [str] = mapped_column(String(16),nullable=True)

    DEVICE1: Mapped["Devices"] = relationship(back_populates="BRAND")

#-----------body Table-----------
class Bodies(Base):
    __tablename__ = 'body'
    id: Mapped [int] = mapped_column(Integer,primary_key=True,autoincrement=True,nullable=True)
    device_id: Mapped [int] = mapped_column(Integer,ForeignKey('device.id'),nullable=True)
    body_dims_mm : Mapped [str] = mapped_column(String(64),nullable=True)
    body_lenght_mm: Mapped[float] = mapped_column(Float, nullable=True)
    body_width_mm: Mapped[float] = mapped_column(Float, nullable=True)
    body_height_mm: Mapped[float] = mapped_column(Float, nullable=True)
    body_dims_inch : Mapped [str] = mapped_column(String(64),nullable=True)
    body_lenght_inch: Mapped[float] = mapped_column(Float, nullable=True)
    body_width_inch: Mapped[float] = mapped_column(Float, nullable=True)
    body_height_inch: Mapped[float] = mapped_column(Float, nullable=True)
    body_weight_g : Mapped [float] = mapped_column(Float,nullable=True)
    body_weight_oz : Mapped [float] = mapped_column(Float,nullable=True)

    DEVICE2 : Mapped ["Devices"] = relationship(back_populates="BODY")

#--------display Table-------------
class Displays(Base):
    __tablename__ = 'display'
    id: Mapped [int] = mapped_column(Integer,primary_key=True,autoincrement=True,nullable=True)
    device_id: Mapped [int] = mapped_column(Integer,ForeignKey('device.id'),nullable=True)
    type: Mapped [str] = mapped_column(String(128),nullable=True)
    type_specific :Mapped [str] = mapped_column(String(128),nullable=True)
    size_inch: Mapped [float] = mapped_column(Float,nullable=True)
    size_cm2: Mapped [float] = mapped_column(Float,nullable=True)
    screen_body_ratio: Mapped [float] = mapped_column(Float,nullable=True)
    resolution_pixel: Mapped[str] = mapped_column(String(64), nullable=True)
    resolution_p_width: Mapped[float] = mapped_column(Float, nullable=True)
    resolution_p_lenght: Mapped[float] = mapped_column(Float, nullable=True)
    resolution_ppi: Mapped[float] = mapped_column(Float, nullable=True)
    resolution_ratio: Mapped[str] = mapped_column(String(64), nullable=True)

    DEVICE3: Mapped["Devices"] = relationship(back_populates="DISPLAY")

#------network Table-------------
class Networks(Base):
    __tablename__ = 'network'
    id: Mapped [int] = mapped_column(Integer,primary_key=True,autoincrement=True,nullable=True)
    device_id: Mapped [int] = mapped_column(Integer,ForeignKey('device.id'),nullable=True)
    network: Mapped [str] = mapped_column(String(128),nullable=True)

    DEVICE4: Mapped["Devices"] = relationship(back_populates="NETWORK")

#--------sensor Table-------------
class Sensors(Base):
    __tablename__ = 'sensor'
    id: Mapped [int] = mapped_column(Integer,primary_key=True,autoincrement=True,nullable=True)
    device_id: Mapped [int] = mapped_column(Integer,ForeignKey('device.id'),nullable=True)
    sensor : Mapped [str] = mapped_column(String(128),nullable=True)

    DEVICE5: Mapped["Devices"] = relationship(back_populates="SENSOR")

#--------processor Table-------------
class Processors(Base):
    __tablename__ = 'processor'
    id: Mapped [int] = mapped_column(Integer,primary_key=True,autoincrement=True,nullable=True)
    device_id: Mapped [int] = mapped_column(Integer,ForeignKey('device.id'),nullable=True)
    cpu_core: Mapped [int] = mapped_column(Integer,nullable=True)

    DEVICE6 : Mapped ["Devices"] = relationship(back_populates="CPU")

#--------memory Table-------------
class Memories(Base):
    __tablename__ = 'memory'
    id: Mapped [int] = mapped_column(Integer,primary_key=True,autoincrement=True,nullable=True)
    device_id: Mapped [int] = mapped_column(Integer,ForeignKey('device.id'),nullable=True)
    internal_memory : Mapped [str] = mapped_column(String(64), nullable=True)

    DEVICE7: Mapped["Devices"] = relationship(back_populates="MEMORY")

#--------ram Table-------------
class Rams(Base):
    __tablename__ = 'ram'
    id: Mapped [int] = mapped_column(Integer,primary_key=True,autoincrement=True,nullable=True)
    device_id: Mapped [int] = mapped_column(Integer,ForeignKey('device.id'),nullable=True)
    ram : Mapped [str] = mapped_column(String(128),nullable=True)

    DEVICE8 : Mapped ["Devices"] = relationship(back_populates="RAM")

#--------sim_type Table-------------
class Sim_Types(Base):
    __tablename__ = 'sim_type'
    id: Mapped [int] = mapped_column(Integer,primary_key=True,autoincrement=True,nullable=True)
    device_id: Mapped [int] = mapped_column(Integer,ForeignKey('device.id'),nullable=True)
    s_type: Mapped [str] = mapped_column(String(64), nullable=True)

    DEVICE9: Mapped["Devices"] = relationship(back_populates="SIM_T")

#--------sim_num Table-------------
class Sim_Nums(Base):
    __tablename__ = 'sim_num'
    id: Mapped [int] = mapped_column(Integer,primary_key=True,autoincrement=True,nullable=True)
    device_id: Mapped [int] = mapped_column(Integer,ForeignKey('device.id'),nullable=True)
    s_num: Mapped [str] = mapped_column(String(64),nullable=True)

    DEVICE10: Mapped["Devices"] = relationship(back_populates="SIM_N")

#--------os Table-------------
class OSs(Base):
    __tablename__ = 'os'
    id: Mapped [int] = mapped_column(Integer,primary_key=True,autoincrement=True,nullable=True)
    device_id: Mapped [int] = mapped_column(Integer,ForeignKey('device.id'),nullable=True)
    name: Mapped [str] = mapped_column(String(64),nullable=True)
    version : Mapped [str] = mapped_column(String(64),nullable=True)

    DEVICE11: Mapped["Devices"] = relationship(back_populates="OS")

#--------sound Table-------------
class Sounds (Base):
    __tablename__ = 'sound'
    id: Mapped [int] = mapped_column(Integer,primary_key=True,autoincrement=True,nullable=True)
    device_id: Mapped [int] = mapped_column(Integer,ForeignKey('device.id'),nullable=True)
    sound: Mapped[str] = mapped_column(String(128),nullable=True)

    DEVICE12: Mapped["Devices"] = relationship(back_populates="SOUND")

#--------communication Table-------------
class Communications(Base):
    __tablename__ = 'communication'
    id: Mapped [int] = mapped_column(Integer,primary_key=True,autoincrement=True,nullable=True)
    device_id: Mapped [int] = mapped_column(Integer,ForeignKey('device.id'),nullable=True)
    comms_type : Mapped [str] = mapped_column(String(64),nullable=True)

    DEVICE13: Mapped["Devices"] = relationship(back_populates="COMMS")


Base.metadata.create_all(engine)
#-----------------------INSERT DATA------------------------
session=Session()

device_df = pd.read_csv('./Tables/Device.csv')
brand_df = pd.read_csv('./Tables/Brand.csv')
body_df = pd.read_csv('./Tables/Body.csv')
display_df = pd.read_csv('./Tables/Display.csv')
network_df = pd.read_csv('./Tables/Network.csv')
sensor_df = pd.read_csv('./Tables/Sensor.csv')
processor_df = pd.read_csv('./Tables/Processor.csv')
memory_df = pd.read_csv('./Tables/Memory.csv')
ram_df = pd.read_csv('./Tables/RAM.csv')
sim_type_df = pd.read_csv('./Tables/SIM_Type.csv')
sim_num_df = pd.read_csv('./Tables/SIM_num.csv')
os_df = pd.read_csv('./Tables/OS.csv')
sound_df = pd.read_csv('./Tables/Sound.csv')
communication_df = pd.read_csv('./Tables/Communications.csv')


with engine.connect() as conn:
    device_df.to_sql('device',conn,if_exists='append',index=False)
    brand_df.to_sql('brand',conn,if_exists='append',index=False)
    body_df.to_sql('body',conn,if_exists='append',index=False)
    display_df.to_sql('display',conn,if_exists='append',index=False)
    network_df.to_sql('network',conn,if_exists='append',index=False)
    sensor_df.to_sql('sensor',conn,if_exists='append',index=False)
    processor_df.to_sql('processor',conn,if_exists='append',index=False)
    memory_df.to_sql('memory',conn,if_exists='append',index=False)
    ram_df.to_sql('ram',conn,if_exists='append',index=False)
    sim_type_df.to_sql('sim_type',conn,if_exists='append',index=False)
    sim_num_df.to_sql('sim_num',conn,if_exists='append',index=False)
    os_df.to_sql('os',conn,if_exists='append',index=False)
    sound_df.to_sql('sound',conn,if_exists='append',index=False)
    communication_df.to_sql('communication',conn,if_exists='append',index=False)


session.commit()

session.close()