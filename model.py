#!/usr/bin/env python
#coding:utf-8
import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy import create_engine,Column,Text,String,ForeignKey

dbPath = os.path.join(os.path.dirname(__file__),'pingtai.db')
engine = create_engine('sqlite:///%s'%dbPath)

DBsession = sessionmaker(bind=engine)
session = DBsession()

Base = declarative_base()

class FinancePlatform(Base):
    __tablename__ = 'basicinfo'

    id = Column(String(48),primary_key=True)
    name  = Column(String(48))
    grageFromThird = Column(String(48))
    profitAverage = Column(String(48))
    dateSale = Column(String(48))
    registeredCapital = Column(String(48))
    area = Column(String(48))
    url = Column(Text)
    startMoney = Column(String(48))
    managementFee = Column(String(48))
    cashTakingFee = Column(String(48))
    backGround = Column(String(48))
    provisionsOfRisk = Column(String(48))
    foundCustodian = Column(String(48))
    safeguardWay = Column(String(48))
    assignmentOfDebt = Column(String(48))
    automaticBidding = Column(String(48))
    cashTime = Column(String(48))
    persons = relationship('Person')
    #company_id = Column(String(48),ForeignKey('company.id'))


class Person(Base):
    __tablename__ = 'person'

    id = Column(String(48),primary_key=True)
    name = Column(String(48))
    curriculumVitae = Column(Text)
    finance_id = Column(String(48),ForeignKey('basicinfo.id'))


class Company(Base):
    __tablename__ = 'company'

    id = Column(String(48),primary_key=True)
    platfromName = Column(String(48))
    companyName = Column(String(48))
    legalRepresentative = Column(String(48))
    phone400 = Column(String(48))
    phone = Column(String(48))
    fax = Column(String(48))
    email = Column(String(48))
    note = Column(Text)
    #platforms = relationship('FinancePlatform')

def init_db():
    Base.metadata.create_all(engine)

def drop_db():
    Base.metadata.drop_all(engine)

if __name__ == '__main__':
    
    drop_db()
    init_db()




