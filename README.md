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
    3. Snakes, 1 pt
    5. Grouches, 0 pts
```

```
 python soccer_ranking.py -f samples/sample_input2.txt
>>  1. Spurs, 7 pts
    1. Tarantulas, 7 pts
    3. Lions, 5 pts
    4. Snakes, 4 pts
    5. FC Awesome, 1 pt
    6. Grouches, 0 pts
```

## Run Tests
```
pytest
```


## Potential Areas of Improvement
1. Even though it doesn't state that the inputs could be potentially malformed, it would be nice
   to add some error handling on mal-formed inputs
2. I didn't bother to package it. Normally you would add a `setup.py` and upload to a PyPi server
   which would allow to install using `pip install` and run like `soccer_ranking -f input.txt`.
