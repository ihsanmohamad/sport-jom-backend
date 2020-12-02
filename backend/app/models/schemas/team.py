from db.models import Team
from tortoise.contrib.pydantic import pydantic_model_creator

Team_Pydantic = pydantic_model_creator(Team, name="Team")
TeamIn_Pydantic = pydantic_model_creator(Team, name="TeamIn", exclude_readonly=True)