from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine


DB_FILE = 'sqlite:///applications.db'

Base = declarative_base()

class Application(Base):
    __tablename__ = 'applications'
    
    id = Column(Integer, primary_key=True)
    company_name = Column(String, unique=True) # Enforce unique company names
    website = Column(String)
    all_emails = Column(Text)       
    target_email = Column(String)
    status = Column(String, default='pending') 
    sent_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Application(company='{self.company_name}', status='{self.status}')>"
    
    
def create_database():
    engine = create_engine(DB_FILE)
    Base.metadata.create_all(engine)
    print(f"Database {DB_FILE} created successfully!")
    
if __name__ == "__main__":
    create_database()
    