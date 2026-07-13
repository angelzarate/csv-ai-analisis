from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider
from app.core.di.providers import AppProvider


container = make_async_container(
    AppProvider(), 
    FastapiProvider()
)

