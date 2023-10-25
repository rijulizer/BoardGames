pip install snakeviz

step-1: 
    # create profile files from cProfile run
    python -m cProfile -o ./profile_reports/main_v3_3.prof main_agent_player_v3.py

Step-2: 
    snakeviz ./profile_reports/main_v3_3.prof