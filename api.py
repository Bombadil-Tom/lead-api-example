from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set up SQLite database URL
DATABASE_URL = "sqlite:///./leads.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, index=True)
    resume = Column(Text)
    state = Column(String, default="PENDING")
    created_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)


class LeadCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    resume: str


class LeadUpdateState(BaseModel):
    state: str


class LeadOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    resume: str
    state: str
    created_at: datetime

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/leads/", response_model=LeadOut)
async def create_lead(lead: LeadCreate, db: Session = Depends(get_db)):
    try:
        db_lead = Lead(
            first_name=lead.first_name,
            last_name=lead.last_name,
            email=lead.email,
            resume=lead.resume,
        )
        db.add(db_lead)
        db.commit()
        db.refresh(db_lead)

        send_email_to_prospect(lead.email, lead.first_name)
        send_email_to_attorney(lead.email, lead.first_name, lead.last_name)
        return db_lead
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/leads/", response_model=List[LeadOut])
async def get_leads(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        leads = db.query(Lead).offset(skip).limit(limit).all()
        return leads
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.put("/leads/{lead_id}", response_model=LeadOut)
async def update_lead_state(lead_id: int, lead_update: LeadUpdateState, db: Session = Depends(get_db)):
    try:
        db_lead = db.query(Lead).filter(Lead.id == lead_id).first()
        if db_lead is None:
            raise HTTPException(status_code=404, detail="Lead not found")

        db_lead.state = lead_update.state
        db.commit()
        db.refresh(db_lead)
        return db_lead
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


def send_email_to_prospect(email: str, first_name: str):
    # should be environment variables
    sender_email = "your_email@example.com"
    receiver_email = email
    password = "your_password"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Lead Submission Confirmation"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"Hi {first_name},\n\nThank you for submitting your lead. We will get back to you soon."
    html = f"<html><body><p>Hi {first_name},<br><br>Thank you for submitting your lead. We will get back to you soon.</p></body></html>"

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


def send_email_to_attorney(prospect_email: str, first_name: str, last_name: str):
    # should be environment variables
    sender_email = "your_email@example.com"
    receiver_email = "attorney_email@example.com"
    password = "your_password"

    message = MIMEMultipart("alternative")
    message["Subject"] = "New Lead Submission"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"A new lead has been submitted by {first_name} {last_name}. You can contact them at {prospect_email}."
    html = f"<html><body><p>A new lead has been submitted by {first_name} {last_name}. You can contact them at {prospect_email}.</p></body></html>"

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
