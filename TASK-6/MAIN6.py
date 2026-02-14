import streamlit as st
import random

# -------------------------
# Initialize session state
# -------------------------
if "user_history" not in st.session_state:
    st.session_state.user_history = []
if "user_score" not in st.session_state:
    st.session_state.user_score = 0
if "computer_score" not in st.session_state:
    st.session_state.computer_score = 0

# -------------------------
# AI logic: frequency-based
# -------------------------
def ai_move():
    """
    AI predicts the user's most frequent move so far
    and plays the move that beats it.
    """
    if not st.session_state.user_history:
        return random.choice(["rock", "paper", "scissors"])
    
    # Count frequency of moves
    move_counts = {"rock": 0, "paper": 0, "scissors": 0}
    for move in st.session_state.user_history:
        move_counts[move] += 1
    
    # Most common user move
    most_common = max(move_counts, key=move_counts.get)
    
    # Play move that beats user's most common move
    beats = {"rock": "paper", "paper": "scissors", "scissors": "rock"}
    return beats[most_common]

# -------------------------
# Decide winner
# -------------------------
def get_winner(user, computer):
    if user == computer:
        return "Draw"
    elif (user == "rock" and computer == "scissors") or \
         (user == "paper" and computer == "rock") or \
         (user == "scissors" and computer == "paper"):
        st.session_state.user_score += 1
        return "You Win!"
    else:
        st.session_state.computer_score += 1
        return "Computer Wins!"

# -------------------------
# Streamlit UI
# -------------------------
st.title("✊ Rule-Based Rock, Paper, Scissors Game")

user_choice = st.selectbox("Choose your move:", ["rock", "paper", "scissors"])

if st.button("Play"):
    # Save user move
    st.session_state.user_history.append(user_choice)
    
    # AI move
    computer_choice = ai_move()
    
    # Decide winner
    result = get_winner(user_choice, computer_choice)
    
    # Display results
    st.write(f"Your move: **{user_choice}**")
    st.write(f"Computer's move: **{computer_choice}**")
    st.write(f"Result: **{result}**")
    
    # Display scores
    st.write(f"Score — You: {st.session_state.user_score} | Computer: {st.session_state.computer_score}")
