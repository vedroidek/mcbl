import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from microblog import config


Engine = create_engine(
    url=config.confdict[os.environ["CONFTYPE"]].DATABASE_URI,
    echo=True,
    pool_size=10
    )

Session = sessionmaker(bind=Engine)
