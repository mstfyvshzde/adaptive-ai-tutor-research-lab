"""
Q-learning agent for the Adaptive AI Tutor Research Lab.

Goal:
Train a simple RL agent that learns which question difficulty to choose.
"""
# Q-learning: Tutor’ın hangi durumda hangi seçimin daha iyi olduğunu deneye deneye öğrenmesi.

from pathlib import Path

import numpy as np
import pandas as pd

from environment import ACTIONS, INPUT_PATH, TutorEnvironment, load_features


OUTPUT_DIR = Path("06_results/tables")
OUTPUT_PATH = OUTPUT_DIR / "q_learning_results.csv"

RANDOM_SEED = 17

EPISODES = 100
# EPISODES = 100 (Toplam Eğitim Turu): Yapay zekanın toplamda kaç kez sıfırdan başlayıp simülasyonu sonuna kadar (öğrenciyle 10 adım bitene kadar) oynayacağını belirler. Ajan, toplam 100 farklı öğrenci seansı üzerinden pratik yaparak deneyim kazanır.

ALPHA = 0.1
# ALPHA = 0.1 (Öğrenme Hızı - Learning Rate): Ajanın yeni yaşadığı deneyimlere ne kadar ağırlık vereceğini seçer. 0.1 değeri, ajanın eski bildiklerini %90 oranında koruyup, yeni bilgiyi %10 oranında hesaba katacağını gösterir. Yani ajan acele etmeden, sindire sindire öğrenir.

GAMMA = 0.9
# GAMMA = 0.9 (Gelecek Odaklılık - Discount Factor): Ajanın uzun vadeli ödülleri ne kadar önemsediğini gösterir. 0.9 yüksek bir değerdir; ajanın sadece o anki adımdan alacağı puana bakmayıp, gelecekteki adımlarda öğrenciye daha faydalı olmayı hedefleyen "ileri görüşlü" bir strateji izlemesini sağlar.

EPSILON = 0.2
# EPSILON = 0.2 (Keşif Oranı - Exploration Rate): Ajanın "yeni şeyler deneme" (keşif) ile "eski bildiği güvenli yoldan gitme" (sömürü) dengesidir. 0.2 değeri, ajanın %20 ihtimalle tamamen rastgele kararlar vererek yeni taktikler arayacağını, %80 ihtimalle ise hafızasındaki en iyi bildiği kararı uygulayacağını belirtir.


# state_to_key: Öğrencinin karmaşık durum bilgilerini (başarı oranı ve adım sayısı) basitleştirerek "low_step_3", "high_step_5" gibi metin tabanlı benzersiz durum etiketlerine (state_key) dönüştürür. Bu, ajanın hafızasında yer tutmasını kolaylaştırır.
def state_to_key(state: dict) -> str:
    recent_accuracy = state["recent_accuracy"]

    if recent_accuracy < 0.50:
        accuracy_level = "low"
    elif recent_accuracy < 0.75:
        accuracy_level = "medium"
    else:
        accuracy_level = "high"

    return f"{accuracy_level}_step_{state['step']}"


# choose_action: Ajanın karar mekanizmasıdır. Epsilon-Greedy yöntemiyle çalışır: %20 ihtimalle (EPSILON = 0.2) yeni şeyler denemek için rastgele bir zorluk seçer, %80 ihtimalle ise hafızasındaki tablodan (q_table) o durum için şimdiye kadar en yüksek puanı getirmiş en iyi kararı seçer.
def choose_action(
    q_table: dict,
    state_key: str,
    rng: np.random.Generator,
) -> str:
    if rng.random() < EPSILON:
        return str(rng.choice(ACTIONS))

    if state_key not in q_table:
        q_table[state_key] = {action: 0.0 for action in ACTIONS}

    return max(q_table[state_key], key=q_table[state_key].get)


# update_q_value: Ajanın hafıza tablosunu (q_table) güncelleyen öğrenme motorudur. Yapılan hamle sonrası alınan ödülü ve bir sonraki adımın potansiyel kazancını hesaba katarak, Bellman denklemi formülüyle (new_value=old_value+α×[reward+γ×max(Q)−old_value]) ilgili durum ve hamlenin kalıcılık puanını (Q değerini) günceller.
def update_q_value(
    q_table: dict,
    state_key: str,
    action: str,
    reward: float,
    next_state_key: str,
) -> None:
    if state_key not in q_table:
        q_table[state_key] = {action_name: 0.0 for action_name in ACTIONS}

    if next_state_key not in q_table:
        q_table[next_state_key] = {action_name: 0.0 for action_name in ACTIONS}

    old_value = q_table[state_key][action]
    best_next_value = max(q_table[next_state_key].values())

    new_value = old_value + ALPHA * (
        reward + GAMMA * best_next_value - old_value
    )

    q_table[state_key][action] = new_value


# train_q_learning_agent: Eğitimin döndüğü ana döngüdür. Belirlenen bölüm sayısı kadar (EPISODES = 100) öğrencileri sırayla sisteme alır; ajanın durumları gözlemlemesini, kararlar vermesini, ödüller toplamasını ve her adımda hafızasını eğitmesini sağlayarak tüm süreci bir veri tablosuna kaydeder.
def train_q_learning_agent(environment: TutorEnvironment) -> pd.DataFrame:
    rng = np.random.default_rng(RANDOM_SEED)
    q_table = {}
    rows = []

    for episode in range(1, EPISODES + 1):
        state = environment.reset()
        done = False
        total_reward = 0.0

        while not done:
            state_key = state_to_key(state)
            action = choose_action(q_table, state_key, rng)

            next_state, reward, done, info = environment.step(action)
            next_state_key = state_to_key(next_state)

            update_q_value(
                q_table=q_table,
                state_key=state_key,
                action=action,
                reward=reward,
                next_state_key=next_state_key,
            )

            total_reward += reward

            rows.append(
                {
                    "episode": episode,
                    "step": state["step"],
                    "state_key": state_key,
                    "action": action,
                    "reward": reward,
                    "total_reward_so_far": total_reward,
                    "recommended_question_id": info["recommended_question_id"],
                    "recommended_topic": info["recommended_topic"],
                    "recommended_difficulty": info["recommended_difficulty"],
                    "probability_correct": info["probability_correct"],
                    "is_correct": info["is_correct"],
                }
            )

            state = next_state

    return pd.DataFrame(rows)


# main: Simülasyonu tetikleyen, ortamı ve ajanı başlatan, eğitim bittikten sonra ajanın performans raporunu ekrana basıp tüm sonuçları bir .csv dosyası olarak bilgisayara kaydeden ana yönetim merkezidir.
def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    data = load_features(INPUT_PATH)
    environment = TutorEnvironment(data)

    results_df = train_q_learning_agent(environment)
    results_df.to_csv(OUTPUT_PATH, index=False)

    episode_summary = (
        results_df.groupby("episode")
        .agg(
            total_reward=("reward", "sum"),
            avg_correctness=("is_correct", "mean"),
        )
        .reset_index()
    )

    print("Q-learning training completed successfully.")
    print(f"Saved to: {OUTPUT_PATH}")
    print(f"Average reward per step: {results_df['reward'].mean():.3f}")
    print(f"Average correctness: {results_df['is_correct'].mean():.3f}")
    print("\nLast 5 episode summaries:")
    print(episode_summary.tail())


if __name__ == "__main__":
    main()