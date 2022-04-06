## Installation && Setup
```
pip install -r requirements.txt
```

the CLI uses [Click](https://click.palletsprojects.com/en/8.1.x/) which makes
makes it much easier to create CLI tools compared to `argparse`.

## Usage
```
python soccer_ranking.py -f samples/sample_input.txt
>>  1. Tarantulas, 6 pts
    2. Lions, 5 pts
    3. FC Awesome, 1 pt
    4. Snakes, 1 pt
    5. Grouches, 0 pts
```

## Run Tests
```
pytest
```

