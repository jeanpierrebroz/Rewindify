"""Setup for Rewindify billing."""
import stripe
from dotenv import dotenv_values

config = dotenv_values()

stripe.api_key= config.get("STRIPE_SECRET")
