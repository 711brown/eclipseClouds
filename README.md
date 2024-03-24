Quick tool to plot the 2024 Total Eclipse Path with GFS Cloud Cover model outputs. 

# Installation
Works under linux environment (Windows + Geo is weird)

This assumes you have Python3 and Virtualenv already set up. 
```
git clone 
cd eclipse-cloud
sudo apt install libeccodes-dev
python3 -m venv .venv
./.venv/bin/activate
pip install -r requirements.txt
```

# Config `config.json`
Define the bounding box for the visual extent of the output.

```
{
    "CONUS": {
        "name": "CONUS",
        "lonMin": -67.0,
        "lonMax": -125.0,
        "latMin": 50.0,
        "latMax": 23.0,
        "markers": [
            {
                "lat": 35.47,
                "lon": -98.6
            }
        ],
        "showCounties": false
    }
}
```

# Usage
```
./.venv/bin/activate
python main.py [PROFILENAME]
```