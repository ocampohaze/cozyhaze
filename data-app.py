print("Local version")
import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="Hero & Farm Adventure", layout="wide")

if "hero_name" not in st.session_state:
    st.session_state.hero_name = ""
if "game_over" not in st.session_state:
    st.session_state.game_over = False

st.title("🛡️ Hero & Farm Adventure")
st.caption("Battle monsters, grow crops, complete missions, and upgrade your hero!")

if st.session_state.game_over:
    st.error("💀 GAME OVER! Your hero has been defeated.")
    if st.button("Restart Adventure"):
        st.session_state.clear()
        st.rerun()
    st.stop()

if not st.session_state.hero_name:
    hero_name_input = st.text_input("Enter your hero's name to start playing:")
    if hero_name_input:
        st.session_state.hero_name = hero_name_input
    else:
        st.warning("You must enter a hero name to start playing!")
        st.stop()

if "health" not in st.session_state:
    st.session_state.health = 100
    st.session_state.energy = 50
    st.session_state.gold = 50
    st.session_state.exp = 0
    st.session_state.level = 1
    st.session_state.crops = 0
    st.session_state.crop_progress = 0
    st.session_state.message = f"Welcome, {st.session_state.hero_name}! Start your adventure."
    st.session_state.monster_health = 0
    st.session_state.in_battle = False
    st.session_state.achievements = []
    st.session_state.strength = 5
    st.session_state.defense = 3
    st.session_state.auto_harvest = False
    st.session_state.current_monster = None
    st.session_state.crop_timer = 0
    st.session_state.missions = [
        {"desc": "Harvest crops", "type": "harvest", "target": 3, "progress": 0, "reward": 10, "completed": False, "collected": False},
        {"desc": "Defeat monsters", "type": "battle", "target": 2, "progress": 0, "reward": 15, "completed": False, "collected": False},
        {"desc": "Earn Gold", "type": "gold", "target": 20, "progress": 0, "reward": 5, "completed": False, "collected": False},
        {"desc": "Reach Level", "type": "level", "target": 3, "progress": st.session_state.level, "reward": 20, "completed": False, "collected": False}
    ]

def clamp():
    st.session_state.health = max(0, st.session_state.health)
    st.session_state.energy = max(0, st.session_state.energy)
    st.session_state.gold = max(0, st.session_state.gold)
    st.session_state.monster_health = max(0, st.session_state.monster_health)
    st.session_state.crops = max(0, st.session_state.crops)
    st.session_state.crop_progress = max(0, st.session_state.crop_progress)
    st.session_state.crop_timer = max(0, st.session_state.crop_timer)

page = st.sidebar.radio("Navigation", ["Game", "Missions", "Stats", "Shop", "About"])
st.sidebar.checkbox("Enable Auto-Harvest", key="auto_harvest")
monster_difficulty = st.sidebar.slider("Monster Difficulty", 1, 3, 1)

if page == "Game":
    tab1, tab2 = st.tabs(["⚔️ Battle", "🌾 Farm"])

    # ----------------- Battle -----------------
    with tab1:
        st.header("Battle Arena")
        col_stats, col_actions, col_messages = st.columns([1,1,1])

        with col_stats:
            st.metric("Health", st.session_state.health)
            st.metric("Energy", st.session_state.energy)
            st.metric("Gold", st.session_state.gold)
            st.metric("EXP", st.session_state.exp)
            st.metric("Level", st.session_state.level)
            st.metric("Strength", st.session_state.strength)
            st.metric("Defense", st.session_state.defense)
            if st.session_state.achievements:
                st.write("🏆 Achievements:", ", ".join(st.session_state.achievements))

        with col_actions:
            if not st.session_state.in_battle:
                if st.button("Encounter Monster"):
                    monsters = ["Goblin","Orc","Dragon"]
                    st.session_state.current_monster = random.choice(monsters)
                    base_hp = {"Goblin":20,"Orc":35,"Dragon":50}
                    st.session_state.monster_health = base_hp[st.session_state.current_monster] * monster_difficulty
                    st.session_state.in_battle = True
                    st.session_state.message = f"A wild {st.session_state.current_monster} appears! HP: {st.session_state.monster_health}"

            if st.session_state.in_battle:
                st.subheader(f"{st.session_state.current_monster} HP: {st.session_state.monster_health}")
                st.progress(st.session_state.monster_health/150)

                if st.button("Attack"):
                    damage = random.randint(5,15) + st.session_state.strength
                    st.session_state.monster_health -= damage
                    st.session_state.energy -= 5
                    st.session_state.message = f"You dealt {damage} damage!"

                if st.button("Defend"):
                    heal = random.randint(3,8) + st.session_state.defense
                    st.session_state.health += heal
                    st.session_state.message = f"You defended and healed {heal} HP!"

                if st.button("Run"):
                    st.session_state.in_battle = False
                    st.session_state.message = "You ran away!"

                clamp()

                if st.session_state.monster_health > 0:
                    monster_damage = random.randint(5,12) * monster_difficulty
                    st.session_state.health -= monster_damage
                    st.session_state.message += f" Monster dealt {monster_damage} damage!"
                else:
                    gold_earned = random.randint(5,15) * monster_difficulty
                    exp_earned = random.randint(5,10) * monster_difficulty
                    st.session_state.gold += gold_earned
                    st.session_state.exp += exp_earned
                    st.session_state.message += f" Monster defeated! +{gold_earned} Gold, +{exp_earned} EXP"
                    st.session_state.in_battle = False
                    if "First Kill" not in st.session_state.achievements:
                        st.session_state.achievements.append("First Kill")

                clamp()
                if st.session_state.health <= 0:
                    st.session_state.game_over = True
                    st.rerun()

            if st.session_state.exp >= st.session_state.level * 20:
                st.session_state.exp -= st.session_state.level * 20
                st.session_state.level += 1
                st.session_state.message += f" Level Up! You are now level {st.session_state.level}"
                st.session_state.health += 10
                st.session_state.energy += 10

        with col_messages:
            st.subheader("Messages")
            with st.expander("View Battle / Event Log"):
                st.success(st.session_state.message)

    # ----------------- Farm -----------------
    with tab2:
        st.header("Farm Management")
        st.write(f"Crops planted: {st.session_state.crops}")
        st.progress(st.session_state.crop_progress/10)
        st.write(f"Crop Timer: {st.session_state.crop_timer}/10")

        col1,col2 = st.columns(2)
        with col1:
            if st.button("Plant Crops (5 Gold each)"):
                if st.session_state.gold >= 5:
                    st.session_state.gold -= 5
                    st.session_state.crops += 1
                    st.session_state.crop_progress = 0
                    st.session_state.crop_timer = 0
                    st.session_state.message = "You planted a crop!"
                else:
                    st.session_state.message = "Not enough Gold to plant!"

        with col2:
            if st.button("Harvest Crops"):
                if st.session_state.crop_progress >= 10 or st.session_state.auto_harvest:
                    gold_earned = st.session_state.crops * random.randint(2,5)
                    st.session_state.gold += gold_earned
                    st.session_state.message = f"You harvested {st.session_state.crops} crops and earned {gold_earned} Gold!"
                    for mission in st.session_state.missions:
                        if mission["type"]=="harvest" and not mission["completed"]:
                            mission["progress"] += st.session_state.crops
                            if mission["progress"]>=mission["target"]:
                                mission["completed"]=True
                    st.session_state.crops = 0
                    st.session_state.crop_progress = 0
                    st.session_state.crop_timer = 0
                    if "First Harvest" not in st.session_state.achievements:
                        st.session_state.achievements.append("First Harvest")
                else:
                    st.session_state.message = "Crops are not ready yet!"

        if st.button("Wait/Pass Time"):
            if st.session_state.crops > 0:
                growth = random.randint(1,3)
                st.session_state.crop_progress += growth
                st.session_state.crop_timer += growth
                if st.session_state.crop_progress > 10:
                    st.session_state.crop_progress = 10
                    st.session_state.crop_timer = 10
                if random.random() < 0.2:
                    lost_crops = min(st.session_state.crops, random.randint(1,st.session_state.crops))
                    lost_gold = min(st.session_state.gold, random.randint(1,st.session_state.gold//2+1))
                    st.session_state.crops -= lost_crops
                    st.session_state.gold -= lost_gold
                    st.warning(f"⚠️ Monster Raid! You lost {lost_crops} crops and {lost_gold} Gold!")

            st.session_state.energy += 5
            st.session_state.health += 2

            # Auto-Harvest when timer is full
            if st.session_state.auto_harvest and st.session_state.crop_progress >=10:
                gold_earned = st.session_state.crops * random.randint(2,5)
                st.session_state.gold += gold_earned
                st.session_state.message += f" Auto-Harvested {st.session_state.crops} crops for {gold_earned} Gold!"
                for mission in st.session_state.missions:
                    if mission["type"]=="harvest" and not mission["completed"]:
                        mission["progress"] += st.session_state.crops
                        if mission["progress"]>=mission["target"]:
                            mission["completed"]=True
                st.session_state.crops = 0
                st.session_state.crop_progress = 0
                st.session_state.crop_timer = 0

        clamp()
        st.success(st.session_state.message)
        st.metric("Player Level",st.session_state.level)
        st.metric("Crops Growth",st.session_state.crop_progress)

# ----------------- Missions -----------------
elif page == "Missions":
    st.header("🎯 Missions")
    active_mission = None
    for mission in st.session_state.missions:
        if not mission["completed"] or (mission["completed"] and not mission["collected"]):
            active_mission = mission
            break
    if not active_mission:
        new_missions = [
            {"desc": "Harvest crops", "type": "harvest", "target": random.randint(2,5), "progress": 0, "reward": 10, "completed": False, "collected": False},
            {"desc": "Defeat monsters", "type": "battle", "target": random.randint(1,3), "progress": 0, "reward": 15, "completed": False, "collected": False},
            {"desc": "Earn Gold", "type": "gold", "target": random.randint(10,30), "progress": 0, "reward": 5, "completed": False, "collected": False},
            {"desc": "Reach Level X", "type": "level", "target": st.session_state.level + random.randint(1,3), "progress": st.session_state.level, "reward": 20, "completed": False, "collected": False}
        ]
        new_mission = random.choice(new_missions)
        st.session_state.missions.append(new_mission)
        active_mission = new_mission
    status = "✅ Completed" if active_mission["completed"] else f"Progress: {active_mission['progress']}/{active_mission['target']}"
    st.write(f"Current Mission: {active_mission['desc']} — {status}")
    if active_mission["completed"] and not active_mission["collected"]:
        if st.button("Collect Reward"):
            st.session_state.gold += active_mission["reward"]
            active_mission["collected"] = True
            st.success(f"Collected {active_mission['reward']} Gold!")
            new_missions = [
                {"desc": "Harvest crops", "type": "harvest", "target": random.randint(2,5), "progress": 0, "reward": 10, "completed": False, "collected": False},
                {"desc": "Defeat monsters", "type": "battle", "target": random.randint(1,3), "progress": 0, "reward": 15, "completed": False, "collected": False},
                {"desc": "Earn Gold", "type": "gold", "target": random.randint(10,30), "progress": 0, "reward": 5, "completed": False, "collected": False},
                {"desc": "Reach Level X", "type": "level", "target": st.session_state.level + random.randint(1,3), "progress": st.session_state.level, "reward": 20, "completed": False, "collected": False}
            ]
            st.session_state.missions.append(random.choice(new_missions))

# ----------------- Stats -----------------
elif page == "Stats":
    st.header("📊 Player Stats")
    data = {
        "Stat":["Health","Energy","Gold","EXP","Level","Strength","Defense","Crops","Crop Growth"],
        "Value":[st.session_state.health,st.session_state.energy,st.session_state.gold,st.session_state.exp,st.session_state.level,st.session_state.strength,st.session_state.defense,st.session_state.crops,st.session_state.crop_progress]
    }
    st.dataframe(pd.DataFrame(data))

# ----------------- Shop -----------------
elif page == "Shop":
    st.header("🛒 Shop")
    st.write("Upgrade your hero using Gold!")
    col1,col2 = st.columns(2)
    with col1:
        if st.button("Buy +2 Strength (10 Gold)"):
            st.session_state.gold -= 10
            st.session_state.strength += 2
        if st.button("Buy +2 Defense (10 Gold)"):
            st.session_state.gold -= 10
            st.session_state.defense += 2
    with col2:
        if st.button("Buy +20 Health (15 Gold)"):
            st.session_state.gold -= 15
            st.session_state.health += 20
        if st.button("Buy +20 Energy (15 Gold)"):
            st.session_state.gold -= 15
            st.session_state.energy += 20
    clamp()

# ----------------- About -----------------
elif page == "About":
    st.header("About This Game")
    st.write(f"""
**Hero & Farm Adventure** is a text-based interactive game built in Streamlit.  

**Use Case:**  
Players manage a hero, fight monsters, grow a farm, complete dynamic missions, and purchase upgrades to improve stats.  

**Target Users:**  
Students, casual gamers, and anyone who enjoys interactive text-based games.  

**Inputs Collected:**  
- Hero name  
- Actions: Attack, Defend, Run, Plant Crops, Harvest Crops  
- Mission progress (automatically tracked)  
- Mission reward collection  
- Shop purchases  
- Auto-harvest toggle  

**Outputs Displayed:**  
- Player stats (Health, Energy, Gold, EXP, Level, Strength, Defense)  
- Crop growth progress  
- Battle results (damage dealt, damage received)  
- Mission completion and rewards  
- Achievements and event messages  
- Notifications for monster raids  

**Goal:**  
Maximize your hero’s level, stats, and farm productivity while surviving battles and completing missions indefinitely.
""")
print("Remote version")
