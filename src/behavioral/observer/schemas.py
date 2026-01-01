"""Pydantic schemas for request/response validation in the Observer pattern API."""

from pydantic import BaseModel, Field, EmailStr
from typing import List
from enum import Enum


class SubscriberType(str, Enum):
    """Enumeration of available subscriber types."""

    CLIENT = "client"
    EMPLOYEE = "employee"
    PARTNER = "partner"
    SUPPLIER = "supplier"


class SubscriberCreate(BaseModel):
    """Schema for creating a new subscriber."""

    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Subscriber's name"
    )
    email: EmailStr = Field(
        ...,
        description="Subscriber's email address"
    )
    subscriber_type: SubscriberType = Field(
        ...,
        description="Type of subscriber (client, employee, partner, supplier)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Silva",
                "email": "john.silva@email.com",
                "subscriber_type": "client"
            }
        }


class SubscriberResponse(BaseModel):
    """Schema for subscriber response."""

    name: str = Field(..., description="Subscriber's name")
    email: str = Field(..., description="Subscriber's email")
    subscriber_type: str = Field(..., description="Type of subscriber")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Silva",
                "email": "john.silva@email.com",
                "subscriber_type": "client"
            }
        }


class MessageCreate(BaseModel):
    """Schema for creating a new newsletter message."""

    content: str = Field(
        ...,
        min_length=10,
        max_length=1000,
        description="Message content to be sent to all subscribers"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "content": "New products on sale! Check out our latest promotions!"
            }
        }


class MessageResponse(BaseModel):
    """Schema for message publication response."""

    message: str = Field(..., description="Published message content")
    subscribers_notified: int = Field(..., description="Number of subscribers notified")
    subscriber_names: List[str] = Field(..., description="Names of notified subscribers")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "New products on sale! Check out our latest promotions!",
                "subscribers_notified": 3,
                "subscriber_names": ["John Silva", "Maria Santos", "Tech Corp"]
            }
        }


class NewsletterStatus(BaseModel):
    """Schema for newsletter status."""

    total_subscribers: int = Field(..., description="Total number of subscribers")
    total_messages: int = Field(..., description="Total messages published")
    subscribers: List[dict] = Field(..., description="List of all subscribers")

    class Config:
        json_schema_extra = {
            "example": {
                "total_subscribers": 5,
                "total_messages": 3,
                "subscribers": [
                    {"name": "John Silva", "email": "john.silva@email.com"},
                    {"name": "Maria Santos", "email": "maria.santos@email.com"}
                ]
            }
        }


class UnsubscribeRequest(BaseModel):
    """Schema for unsubscribe request."""

    email: EmailStr = Field(..., description="Email of subscriber to unsubscribe")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.silva@email.com"
            }
        }


class OperationResponse(BaseModel):
    """Generic schema for operation responses."""

    success: bool = Field(..., description="Whether operation was successful")
    message: str = Field(..., description="Operation result message")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Operation completed successfully"
            }
        }
