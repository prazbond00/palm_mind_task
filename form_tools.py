from pydantic import BaseModel, validator
from typing import Optional
from utils.validators import validate_email, validate_phone
from utils.date_parser import parse_natural_date
from datetime import datetime

# Call form data model


class CallForm(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

    @validator("email")
    def email_validator(cls, v):
        if v is not None and not validate_email(v):
            raise ValueError("Invalid email format")
        return v

    @validator("phone")
    def phone_validator(cls, v):
        if v is not None and not validate_phone(v):
            raise ValueError("Invalid phone number format")
        return v


# Booking form data model
class BookingForm(BaseModel):
    name: Optional[str] = None
    date: Optional[str] = None  # YYYY-MM-DD

    @validator("date")
    def date_validator(cls, v):
        if v is not None:
            try:
                datetime.strptime(v, "%Y-%m-%d")
            except Exception:
                raise ValueError("Date must be in YYYY-MM-DD format")
        return v


def collect_call_form():
    form = CallForm()
    print("Sure! I can help you with a call. May I have your name?")
    form.name = input("Name: ").strip()

    while True:
        print("Please provide your email:")
        email = input("Email: ").strip()
        if validate_email(email):
            form.email = email
            break
        print("Invalid email format. Try again.")

    while True:
        print("Please provide your phone number (include country code, e.g., +1234567890):")
        phone = input("Phone: ").strip()
        if validate_phone(phone):
            form.phone = phone
            break
        print("Invalid phone number format. Try again.")

    print(f"Thanks {form.name}, we will contact you soon!")
    return form.dict()


def collect_booking_form():
    form = BookingForm()
    print("Let's book your appointment. What is your name?")
    form.name = input("Name: ").strip()

    while True:
        print("Please enter the appointment date (you can say 'next Monday', '2025-06-10', etc.):")
        date_input = input("Date: ").strip()
        dt = parse_natural_date(date_input)
        if dt:
            form.date = dt.strftime("%Y-%m-%d")
            break
        print("Sorry, I couldn't understand the date. Try again.")

    print(f"Appointment booked for {form.name} on {form.date}")
    return form.dict()
