"""
💰 Billing System with PayPal Integration
Pay-Per-Conversion + Premium Tiers + PayPal Payments
"""

from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ConversionTransaction(Base):
    """Track every conversion and charge"""
    __tablename__ = "conversion_transactions"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    conversion_type = Column(String)  # "csv_to_json", etc.
    amount = Column(Float)  # $0.05
    timestamp = Column(DateTime, default=datetime.utcnow)
    paid = Column(Boolean, default=False)

class PremiumSubscription(Base):
    """Premium subscribers"""
    __tablename__ = "premium_subscriptions"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    subscription_date = Column(DateTime, default=datetime.utcnow)
    next_billing_date = Column(DateTime)
    stripe_subscription_id = Column(String, nullable=True)
    amount = Column(Float, default=9.99)
    active = Column(Boolean, default=True)

class PayPalPayment(Base):
    """Track PayPal payments"""
    __tablename__ = "paypal_payments"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    email = Column(String)
    plan = Column(String)  # "pro" or "premium"
    amount = Column(Float)
    transaction_id = Column(String, nullable=True)
    status = Column(String, default="pending")  # pending, completed, failed
    payment_method = Column(String, default="paypal")  # paypal, upi, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    confirmed_at = Column(DateTime, nullable=True)

class UPIPayment(Base):
    """Track UPI payments (India)"""
    __tablename__ = "upi_payments"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    email = Column(String)
    plan = Column(String)  # "pro" or "premium"
    amount = Column(Float)
    upi_ref = Column(String, nullable=True)
    status = Column(String, default="pending")  # pending, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    confirmed_at = Column(DateTime, nullable=True)

def get_conversion_cost(user_plan: str) -> float:
    """Get cost per conversion based on plan"""
    
    if user_plan == "premium":
        return 0.0  # Free for premium users
    elif user_plan == "pro":
        return 0.03  # Discounted for pro
    else:
        return 0.05  # Standard: $0.05 per conversion

def get_monthly_conversions(user_id: int, db) -> int:
    """Get conversions used this month"""
    
    month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    count = db.query(ConversionTransaction).filter(
        ConversionTransaction.user_id == user_id,
        ConversionTransaction.timestamp >= month_start
    ).count()
    
    return count

def get_free_conversions_left(user_id: int, db) -> int:
    """Get remaining free conversions this month"""
    conversions_used = get_monthly_conversions(user_id, db)
    return max(0, 50 - conversions_used)

def can_convert(user_id: int, user_plan: str, db) -> tuple:
    """Check if user can convert (within limits)"""
    
    conversions_this_month = get_monthly_conversions(user_id, db)
    
    # Premium: unlimited
    if user_plan == "premium":
        return True, "unlimited"
    
    # Pro: 500/month
    if user_plan == "pro":
        if conversions_this_month >= 500:
            return False, "Pro plan limit (500/month) reached"
        return True, f"{500 - conversions_this_month} left"
    
    # Free: 50/month + pay-per-conversion
    if user_plan == "free":
        if conversions_this_month < 50:
            return True, f"{50 - conversions_this_month} free left"
        return True, "Will charge $0.05"
    
    return False, "Unknown plan"

def charge_user(user_id: int, conversion_type: str, user_plan: str, db) -> dict:
    """Charge user for conversion"""
    
    # Get cost
    cost = get_conversion_cost(user_plan)
    
    # Record transaction
    if cost > 0:
        transaction = ConversionTransaction(
            user_id=user_id,
            conversion_type=conversion_type,
            amount=cost
        )
        db.add(transaction)
        db.commit()
        
        return {
            "charged": True,
            "amount": cost,
            "message": f"Charged ${cost:.2f}"
        }
    else:
        return {
            "charged": False,
            "amount": 0,
            "message": "No charge (included in plan)"
        }

def get_user_monthly_bill(user_id: int, db) -> dict:
    """Calculate user's monthly bill"""
    
    month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    from main import User
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {
            "user_id": user_id,
            "plan": "free",
            "conversions": 0,
            "conversion_charge": 0,
            "plan_charge": 0,
            "total": 0,
            "currency": "USD"
        }
    
    transactions = db.query(ConversionTransaction).filter(
        ConversionTransaction.user_id == user_id,
        ConversionTransaction.timestamp >= month_start
    ).all()
    
    total = sum(t.amount for t in transactions)
    
    # Add plan cost if applicable
    if user.plan == "pro":
        total += 9.99
    elif user.plan == "premium":
        total += 29.99
    
    return {
        "user_id": user_id,
        "plan": user.plan,
        "conversions": len(transactions),
        "conversion_charge": sum(t.amount for t in transactions),
        "plan_charge": 9.99 if user.plan == "pro" else (29.99 if user.plan == "premium" else 0),
        "total": total,
        "currency": "USD"
    }

def record_paypal_payment(user_id: int, email: str, plan: str, amount: float, transaction_id: str, db) -> dict:
    """Record a PayPal payment"""
    
    payment = PayPalPayment(
        user_id=user_id,
        email=email,
        plan=plan,
        amount=amount,
        transaction_id=transaction_id,
        status="pending",
        payment_method="paypal"
    )
    
    db.add(payment)
    db.commit()
    
    return {
        "status": "pending",
        "message": f"Payment recorded. Awaiting confirmation.",
        "transaction_id": transaction_id
    }

def confirm_paypal_payment(email: str, transaction_id: str, db) -> dict:
    """Confirm PayPal payment and upgrade user"""
    
    payment = db.query(PayPalPayment).filter(
        PayPalPayment.email == email,
        PayPalPayment.transaction_id == transaction_id
    ).first()
    
    if not payment:
        return {
            "status": "error",
            "message": "Payment not found"
        }
    
    # Update payment status
    payment.status = "completed"
    payment.confirmed_at = datetime.utcnow()
    
    # Upgrade user
    from main import User
    user = db.query(User).filter(User.email == email).first()
    
    if user:
        user.plan = payment.plan
        if payment.plan == "pro":
            user.conversions_limit = 500
        elif payment.plan == "premium":
            user.conversions_limit = 999999
    
    db.commit()
    
    return {
        "status": "success",
        "message": f"Payment confirmed! User upgraded to {payment.plan}",
        "user_plan": payment.plan
    }

def record_upi_payment(user_id: int, email: str, plan: str, amount: float, upi_ref: str, db) -> dict:
    """Record a UPI payment (India)"""
    
    payment = UPIPayment(
        user_id=user_id,
        email=email,
        plan=plan,
        amount=amount,
        upi_ref=upi_ref,
        status="pending"
    )
    
    db.add(payment)
    db.commit()
    
    return {
        "status": "pending",
        "message": f"UPI payment recorded. Awaiting confirmation.",
        "upi_ref": upi_ref
    }

def confirm_upi_payment(email: str, upi_ref: str, db) -> dict:
    """Confirm UPI payment and upgrade user"""
    
    payment = db.query(UPIPayment).filter(
        UPIPayment.email == email,
        UPIPayment.upi_ref == upi_ref
    ).first()
    
    if not payment:
        return {
            "status": "error",
            "message": "Payment not found"
        }
    
    # Update payment status
    payment.status = "completed"
    payment.confirmed_at = datetime.utcnow()
    
    # Upgrade user
    from main import User
    user = db.query(User).filter(User.email == email).first()
    
    if user:
        user.plan = payment.plan
        if payment.plan == "pro":
            user.conversions_limit = 500
        elif payment.plan == "premium":
            user.conversions_limit = 999999
    
    db.commit()
    
    return {
        "status": "success",
        "message": f"Payment confirmed! User upgraded to {payment.plan}",
        "user_plan": payment.plan
    }

def get_payment_history(user_id: int, db) -> list:
    """Get user's payment history"""
    
    paypal_payments = db.query(PayPalPayment).filter(
        PayPalPayment.user_id == user_id
    ).all()
    
    upi_payments = db.query(UPIPayment).filter(
        UPIPayment.user_id == user_id
    ).all()
    
    history = []
    
    for p in paypal_payments:
        history.append({
            "type": "paypal",
            "plan": p.plan,
            "amount": p.amount,
            "status": p.status,
            "created_at": p.created_at.isoformat(),
            "confirmed_at": p.confirmed_at.isoformat() if p.confirmed_at else None
        })
    
    for p in upi_payments:
        history.append({
            "type": "upi",
            "plan": p.plan,
            "amount": p.amount,
            "status": p.status,
            "created_at": p.created_at.isoformat(),
            "confirmed_at": p.confirmed_at.isoformat() if p.confirmed_at else None
        })
    
    return sorted(history, key=lambda x: x['created_at'], reverse=True)