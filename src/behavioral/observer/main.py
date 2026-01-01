"""FastAPI application implementing the Observer pattern for newsletter management.

This API demonstrates how the Observer pattern allows objects (subscribers) to be
notified automatically when the subject (newsletter) changes state.
"""

from fastapi import APIRouter, FastAPI, HTTPException
from .observer import ClientSubscriber, EmployeeSubscriber, PartnerSubscriber, SupplierSubscriber
from .subject import Newsletter
from .schemas import (
    SubscriberCreate,
    SubscriberResponse,
    MessageCreate,
    MessageResponse,
    NewsletterStatus,
    UnsubscribeRequest,
    OperationResponse,
    SubscriberType
)
from typing import Dict


# Global newsletter instance (Subject)
newsletter = Newsletter()

# Registry to store observer references by email
observers_registry: Dict[str, object] = {}


# Helper functions shared by both router and app
def _get_status_logic() -> NewsletterStatus:
    """Business logic for getting newsletter status."""
    return NewsletterStatus(
        total_subscribers=newsletter.get_subscriber_count(),
        total_messages=len(newsletter.get_messages()),
        subscribers=newsletter.get_subscribers()
    )


def _subscribe_logic(subscriber: SubscriberCreate) -> SubscriberResponse:
    """Business logic for subscribing a new observer."""
    # Check if email is already registered
    if subscriber.email in observers_registry:
        raise HTTPException(
            status_code=400,
            detail=f"Email {subscriber.email} is already subscribed to the newsletter"
        )

    try:
        # Create appropriate observer based on type
        observer_classes = {
            SubscriberType.CLIENT: ClientSubscriber,
            SubscriberType.EMPLOYEE: EmployeeSubscriber,
            SubscriberType.PARTNER: PartnerSubscriber,
            SubscriberType.SUPPLIER: SupplierSubscriber
        }

        ObserverClass = observer_classes[subscriber.subscriber_type]
        observer = ObserverClass(subscriber.name, subscriber.email, newsletter)

        # Store observer reference
        observers_registry[subscriber.email] = observer

        return SubscriberResponse(
            name=subscriber.name,
            email=subscriber.email,
            subscriber_type=subscriber.subscriber_type.value
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error subscribing: {str(e)}"
        )


def _unsubscribe_logic(request: UnsubscribeRequest) -> OperationResponse:
    """Business logic for unsubscribing an observer."""
    if request.email not in observers_registry:
        raise HTTPException(
            status_code=404,
            detail=f"Email {request.email} not found in subscriber list"
        )

    try:
        observer = observers_registry[request.email]
        observer.unsubscribe()
        del observers_registry[request.email]

        return OperationResponse(
            success=True,
            message=f"Successfully unsubscribed {request.email}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error unsubscribing: {str(e)}"
        )


def _publish_message_logic(message: MessageCreate) -> MessageResponse:
    """Business logic for publishing a message."""
    try:
        # Publish message and notify all observers
        newsletter.publish_message(message.content)

        subscribers = newsletter.get_subscribers()
        subscriber_names = [s["name"] for s in subscribers]

        return MessageResponse(
            message=message.content,
            subscribers_notified=len(subscribers),
            subscriber_names=subscriber_names
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error publishing message: {str(e)}"
        )


def _list_messages_logic() -> dict:
    """Business logic for listing all messages."""
    messages = newsletter.get_messages()
    return {
        "total": len(messages),
        "messages": messages
    }


def _list_subscribers_logic() -> dict:
    """Business logic for listing all subscribers."""
    subscribers = newsletter.get_subscribers()
    return {
        "total": len(subscribers),
        "subscribers": subscribers
    }


# Create router for inclusion in main app
router = APIRouter(prefix="/observer", tags=["Observer Pattern"])


@router.get("/")
async def router_root():
    """Get API information and available endpoints."""
    return {
        "message": "Newsletter System - Observer Pattern",
        "pattern": "Observer",
        "description": "Defines one-to-many dependency between objects",
        "subscriber_types": {
            "client": "Company client",
            "employee": "Company employee",
            "partner": "Business partner",
            "supplier": "Supplier"
        },
        "endpoints": {
            "status": "/observer/status (GET)",
            "subscribe": "/observer/subscribers (POST)",
            "unsubscribe": "/observer/subscribers (DELETE)",
            "publish": "/observer/messages (POST)",
            "list_messages": "/observer/messages (GET)",
            "list_subscribers": "/observer/subscribers (GET)"
        }
    }


@router.get("/status", response_model=NewsletterStatus)
async def router_get_status():
    """Get current newsletter status.

    Shows total subscribers, published messages, and all registered subscribers.
    """
    return _get_status_logic()


@router.post("/subscribers", response_model=SubscriberResponse, status_code=201)
async def router_subscribe(subscriber: SubscriberCreate):
    """Subscribe a new observer to the newsletter.

    The Observer pattern allows new observers (subscribers) to be added
    dynamically to the Subject (newsletter). When the Subject changes state
    (new message), all observers are automatically notified.
    """
    return _subscribe_logic(subscriber)


@router.delete("/subscribers", response_model=OperationResponse)
async def router_unsubscribe(request: UnsubscribeRequest):
    """Unsubscribe an observer from the newsletter.

    Removes the observer from the Subject's notification list.
    Demonstrates the Observer pattern's flexibility in removing observers dynamically.
    """
    return _unsubscribe_logic(request)


@router.post("/messages", response_model=MessageResponse, status_code=201)
async def router_publish_message(message: MessageCreate):
    """Publish a new message to the newsletter.

    When a message is published, the Subject (newsletter) automatically notifies
    all registered observers. This is the core of the Observer pattern:
    Subject state change -> automatic notification of all observers.
    """
    return _publish_message_logic(message)


@router.get("/messages")
async def router_list_messages():
    """List all published messages."""
    return _list_messages_logic()


@router.get("/subscribers")
async def router_list_subscribers():
    """List all newsletter subscribers."""
    return _list_subscribers_logic()


# Also create standalone app for independent use
app = FastAPI(
    title="Newsletter - Observer Pattern",
    description="API demonstrating the Observer pattern for newsletter management",
    version="1.0.0"
)


@app.get("/", tags=["Root"])
async def root():
    """Get API information and available endpoints."""
    return {
        "message": "Newsletter System - Observer Pattern",
        "pattern": "Observer",
        "description": "Defines one-to-many dependency between objects",
        "how_it_works": {
            "1": "Subscribers (observers) register with Newsletter (subject)",
            "2": "Newsletter publishes new message (state change)",
            "3": "Newsletter.notify_observers() is called automatically",
            "4": "Each observer.update() is executed",
            "5": "Observers process the notification (send emails)"
        },
        "subscriber_types": {
            "client": "Company client",
            "employee": "Company employee",
            "partner": "Business partner",
            "supplier": "Supplier"
        },
        "endpoints": {
            "status": "/status (GET)",
            "subscribe": "/subscribers (POST)",
            "unsubscribe": "/subscribers (DELETE)",
            "publish": "/messages (POST)",
            "list_messages": "/messages (GET)",
            "list_subscribers": "/subscribers (GET)"
        }
    }


@app.get("/status", response_model=NewsletterStatus, tags=["Newsletter"])
async def get_status():
    """Get current newsletter status.

    Shows total subscribers, published messages, and all registered subscribers.
    """
    return _get_status_logic()


@app.post("/subscribers", response_model=SubscriberResponse, status_code=201, tags=["Subscribers"])
async def subscribe(subscriber: SubscriberCreate):
    """Subscribe a new observer to the newsletter.

    The Observer pattern allows new observers (subscribers) to be added
    dynamically to the Subject (newsletter). When the Subject changes state
    (new message), all observers are automatically notified.

    Subscriber Types:
    - client: Company client
    - employee: Company employee
    - partner: Business partner
    - supplier: Supplier
    """
    return _subscribe_logic(subscriber)


@app.delete("/subscribers", response_model=OperationResponse, tags=["Subscribers"])
async def unsubscribe(request: UnsubscribeRequest):
    """Unsubscribe an observer from the newsletter.

    Removes the observer from the Subject's notification list.
    Demonstrates the Observer pattern's flexibility in removing observers dynamically.
    """
    return _unsubscribe_logic(request)


@app.post("/messages", response_model=MessageResponse, status_code=201, tags=["Messages"])
async def publish_message(message: MessageCreate):
    """Publish a new message to the newsletter.

    When a message is published, the Subject (newsletter) automatically notifies
    all registered observers. This is the core of the Observer pattern:
    Subject state change -> automatic notification of all observers.

    Flow:
    1. Newsletter receives new message
    2. Newsletter.notify_observers() is called
    3. Each observer.update() is executed
    4. Observers process the notification (send emails)
    """
    return _publish_message_logic(message)


@app.get("/messages", tags=["Messages"])
async def list_messages():
    """List all published messages."""
    return _list_messages_logic()


@app.get("/subscribers", tags=["Subscribers"])
async def list_subscribers():
    """List all newsletter subscribers."""
    return _list_subscribers_logic()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
