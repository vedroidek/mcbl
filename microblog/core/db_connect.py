import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from microblog.config import confdict


Engine = create_engine(
    url=confdict[os.environ.get("CONFTYPE")].DATABASE_URI,
    echo=True,
    pool_size=10
    )

Session = sessionmaker(bind=Engine)
