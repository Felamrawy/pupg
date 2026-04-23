# 🎮 PUBG Weapon Stats Analysis & Interactive Dashboard

A data analysis project focused on analyzing PlayerUnknown's Battlegrounds (PUBG) weapon mechanics, performance metrics, and lethality through Exploratory Data Analysis (EDA) and an interactive web dashboard.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Plotly](https://img.shields.io/badge/Visualization-Plotly-orange.svg)
![Dash](https://img.shields.io/badge/Framework-Dash-008080.svg)

## 📌 Project Overview
This project explores how different weapon classes and bullet types perform in PUBG. It investigates damage efficiency, range, and protection level impacts to help players understand the "meta" of the game.

### Key Questions Answered:
* How do weapon classes differ in performance metrics?
* What role does bullet type play in determining damage efficiency?
* Which features (fire rate, damage, etc.) most strongly explain a weapon's lethality?

## 📂 Project Structure
* `PUBG_EDA.ipynb`: Full data cleaning, preprocessing, and exploratory analysis.
* `PUBG_Dashboard.py`: An interactive Dash application to visualize weapon stats dynamically.
* `pubg-weapon-stats.csv`: The raw dataset containing 44 observations and 20 variables.
* `pubg-clean.csv`: The processed dataset used for the dashboard.
* `requirements.txt`: List of necessary Python libraries.

## 📊 Features
### 1. Exploratory Data Analysis (EDA)
* **Data Cleaning:** Handled missing values (NaNs) and corrected data types (e.g., Bullet Type, Fire Mode).
* **Visual Analysis:** Distribution of damage across different weapon classes using Plotly and Matplotlib.
* **Comparative Studies:** Analyzing damage against different armor levels (Level 0 to Level 3).

### 2. Interactive Dashboard
The dashboard allows users to filter and compare weapons in real-time:
* **Weapon Class Filtering:** Compare ARs, SRs, SMGs, etc.
* **Visualizations:** Includes weapon ranking charts, combat performance, ballistics analysis, and armor protection comparisons.
* **Local Hosting:** Runs on a local server for easy access.

## ⚙️ Setup & Installation

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/Felamrawy/pupg.git](https://github.com/Felamrawy/pupg.git)
    cd pupg
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Dashboard:**
    You can run the dashboard by opening `PUBG_Dashboard.ipynb` in VS Code/Jupyter or by converting it to a script:
    ```bash
    # To run as a script 
    python Pubg_Dashboard.py
    ```
    Once running, access the dashboard at: `http://127.0.0.1:8052`

## 🛠️ Built With
* **Pandas & NumPy:** Data manipulation.
* **Plotly & Matplotlib:** Advanced data visualization.
* **Dash & Dash Bootstrap Components:** Web application framework.
* **Scikit-Learn:** Data preprocessing.

## 📝 Findings
* **Lethality:** Analysis showed that certain sidearms like the *Skorpion* and *P18C* maintain high damage output regardless of the opponent's protection level.
* **Protection:** Armor Level 3 significantly changes the "Time to Kill" for most standard ARs.


**Developed by [Felamrawy](https://github.com/Felamrawy)**