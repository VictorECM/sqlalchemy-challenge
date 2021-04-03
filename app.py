{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [],
   "source": [
    "import datetime as dt\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "import sqlalchemy\n",
    "from sqlalchemy.ext.automap import automap_base\n",
    "from sqlalchemy.orm import Session\n",
    "from sqlalchemy import create_engine, func\n",
    "from flask import Flask, jsonify, render_template\n",
    "from datetime import datetime as dt2"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [],
   "source": [
    "engine = create_engine(\"sqlite:///Resources/hawaii.sqlite\")\n",
    "Base = automap_base()\n",
    "Base.prepare(engine, reflect=True)\n",
    "Measurement = Base.classes.measurement\n",
    "Station = Base.classes.station"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [],
   "source": [
    "session = Session(engine)\n",
    "app = Flask(__name__)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/\")\n",
    "def home():\n",
    "    return (\n",
    "        f\"Welcome to the SQL-Alchemy APP API!<br/>\"\n",
    "        f\"Available Routes:<br/>\"\n",
    "        f\"/api/v1.0/precipitation<br/>\"\n",
    "        f\"/api/v1.0/stations<br/>\"\n",
    "        f\"/api/v1.0/tobs<br/>\"\n",
    "        f\"/api/v1.0/temp/[start_date format:yyyy-mm-dd]<br/>\"\n",
    "        f\"/api/v1.0/temp/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]<br/>\"\n",
    "    )"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/api/v1.0/precipitation\")\n",
    "def prcp():\n",
    "    session = Session(engine)\n",
    "    result = session.query(Measurement.date, Measurement.prcp).all()\n",
    "    \n",
    "    #print(result)\n",
    "    json_row = {}\n",
    "    \n",
    "    for row in result:\n",
    "        json_row[row[0]] = row[1]\n",
    "        #print(json_row)\n",
    " \n",
    "    return jsonify(json_row)\n",
    "\n",
    "    session.close()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/api/v1.0/tobs\")\n",
    "def tobs():\n",
    "    session = Session(engine)\n",
    "\n",
    "    for row in session.\\\n",
    "                query(Measurement.date).\\\n",
    "                order_by(Measurement.date.desc()).\\\n",
    "                limit(1):\n",
    "        lastdate = row[0]\n",
    "                \n",
    "    print(lastdate)\n",
    "    finaldate = dt2.strptime(lastdate,'%Y-%m-%d')\n",
    "    print(finaldate)\n",
    "\n",
    "    new_day = finaldate.day\n",
    "    new_month = finaldate.month\n",
    "    new_year = finaldate.year-1\n",
    "\n",
    "    if new_day>9 and new_month>9:\n",
    "        initdate = (f'{new_year}-{new_month}-{new_day}')\n",
    "    elif new_day<9 and new_month>9:\n",
    "        initdate = (f'{new_year}-{new_month}-0{new_day}')\n",
    "    elif new_day>9 and new_month<9:\n",
    "        initdate = (f'{new_year}-0{new_month}-{new_day}')\n",
    "    else:\n",
    "        initdate = (f'{new_year}-0{new_month}-0{new_day}')\n",
    "\n",
    "    print(initdate) \n",
    "\n",
    "    result = session.query(Measurement.date, Measurement.tobs).\\\n",
    "                filter((Measurement.date >= initdate) & (Measurement.date <= lastdate)).\\\n",
    "                all()\n",
    "\n",
    "    tobs_all = []\n",
    "\n",
    "    for row in result:\n",
    "        tobs_all.append(row[1])\n",
    "\n",
    "\n",
    "    return jsonify(tobs_all)\n",
    "\n",
    "    session.close()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/api/v1.0/temp/<start_date>\")\n",
    "def start_temp(start_date):\n",
    "    session = Session(engine)\n",
    "    result = session.\\\n",
    "                query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\\\n",
    "                filter(Measurement.date >= start_date).\\\n",
    "                all()\n",
    "    print(result)\n",
    "    \n",
    "\n",
    "    json_row = []\n",
    "    for min, avg,max in result: \n",
    "        start_date_tobs_dict = {}\n",
    "        start_date_tobs_dict[\"min_temp\"] = min\n",
    "        start_date_tobs_dict[\"avg_temp\"] = avg\n",
    "        start_date_tobs_dict[\"max_temp\"] = max\n",
    "        json_row.append(start_date_tobs_dict)\n",
    "\n",
    "    return jsonify(json_row)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * Serving Flask app \"__main__\" (lazy loading)\n",
      " * Environment: production\n",
      "   WARNING: This is a development server. Do not use it in a production deployment.\n",
      "   Use a production WSGI server instead.\n",
      " * Debug mode: on\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " * Restarting with windowsapi reloader\n"
     ]
    },
    {
     "ename": "SystemExit",
     "evalue": "1",
     "output_type": "error",
     "traceback": [
      "An exception has occurred, use %tb to see the full traceback.\n",
      "\u001b[1;31mSystemExit\u001b[0m\u001b[1;31m:\u001b[0m 1\n"
     ]
    }
   ],
   "source": [
    "@app.route(\"/api/v1.0/temp/<start_date>/<end_date>\")\n",
    "def between_temp(start_date, end_date):\n",
    "    session = Session(engine)\n",
    "    result = session.\\\n",
    "                query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\\\n",
    "                filter( (Measurement.date >= start_date) & (Measurement.date <= end_date) ).\\\n",
    "                all()\n",
    "    \n",
    "\n",
    "    json_row = {}\n",
    "    json_row['start_date'] = start_date\n",
    "    json_row['end_date'] = end_date\n",
    "    json_row['tavg'] = result[0][0]\n",
    "    json_row['tmax'] = result[0][1]\n",
    "    json_row['tmin'] = result[0][2]\n",
    "\n",
    "    return jsonify(json_row)\n",
    "\n",
    "    \n",
    "\n",
    "\n",
    "if __name__ == '__main__':\n",
    "    app.run(debug=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:pythonData] *",
   "language": "python",
   "name": "conda-env-pythonData-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.10"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
