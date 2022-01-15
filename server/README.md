# MinesweeperMulti Server

Here you will find the source for the MinesweeperMulti backend REST api.

MinesweeperMulti was primarily developed using `3.10` and backward compatibility, especially with type hints, is not gaurenteed.
For the smoothest possible experience try to use python3.10 or higher.

# Running
This sever runs on [flask](https://flask.palletsprojects.com/en/2.0.x/). To run be sure to install dependencies `pip3
install --requirement requirements.txt`. From here running the app is simple by following [Quickstart](https://flask.palletsprojects.com/en/2.0.x/quickstart/)
instructions, or following the steps below:

```bash
# when in the same directory as app.py you don't need to set the FLASK_APP
# environment variable
flask run

# or simply run using python
python app.py
```
