from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base 


class CodeReview(Base):
    __tablename__ = "code_reviews"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255))
    original_code = Column(Text)
    refactored_code = Column(Text)
    documentation = Column(Text) 
    created_at = Column(DateTime, default=datetime.utcnow)
    
    findings = relationship("Vulnerability", back_populates="review")

class Vulnerability(Base):
    __tablename__ = "vulnerabilities"
    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey("code_reviews.id"))
    line_number = Column(Integer)
    severity = Column(String(50)) 
    description = Column(String(500))
    suggestion = Column(Text)
    
    review = relationship("CodeReview", back_populates="findings")


