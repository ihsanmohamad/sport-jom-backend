from db.models import Tournament
from tortoise.contrib.pydantic import pydantic_model_creator

Tournament_Pydantic = pydantic_model_creator(Tournament, name="Tournament")
TournamentIn_Pydantic = pydantic_model_creator(Tournament, name="TournamentIn", exclude_readonly=True)