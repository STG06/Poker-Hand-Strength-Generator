from cmd import PROMPT
from deuces import Card, Evaluator, card
import random
import streamlit as st
import requests
import os
import google.generativeai as genai

genai.configure(api_key="KEY")
model = genai.GenerativeModel("gemini-1.5-flash")

# Title Section
def title_section():
    st.header("Poker Hand Win Probability Generator")
    st.image("Images/poker.jpg", width=200)
    st.write("---")

title_section()

usedCards = set()

# Generate Deck
def generate_deck(deck_count=1):
    response = requests.get(f"https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count={deck_count}")
    if response.status_code == 200:
        deckData = response.json()
        return deckData["deck_id"]
    else:
        st.error("Error making a deck") #NEW
        return None

deck = generate_deck(deck_count=1)

# Function to get image path for each card
def get_card_image_path(card_str):
    if card_str[0] == '0':
        card_str = 'T' + card_str[1]
    return os.path.join("Images/cards", f"{card_str[0] + card_str[1].lower()}.png")

# Draw Cards
def drawCards(deck_id, count):
    response = requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count={count}")
    drawnCards = []
    rCount = count
    while rCount > 0:
        if response.status_code == 200:
            drawData = response.json()
            if drawData["success"]:
                for card in drawData["cards"]:
                    if card["code"] not in usedCards:
                        drawnCards.append(card["code"])
                        usedCards.add(card["code"])
                        rCount -= 1
                        if rCount == 0:
                            break
            else:
                st.error("Can't draw cards")
        else:
            st.error("Can't communicate with API")
            return []
    return drawnCards

# Calculate Hand Probability
def calculate_prob(hole_cards, community_cards):
    try:
        evaluator = Evaluator()

        def normalize_card(card):
            if len(card) == 2:
                rank, suit = card[0], card[1].lower()
                if rank == '0':  # If '0' is detected, convert it to 'T'
                    rank = 'T'
                if suit not in 'cdhs':  # Check for valid suit
                    return None
                return rank + suit
            return None

        # Apply normalization to hole cards and community cards
        hole_cards = [normalize_card(card) for card in hole_cards]
        community_cards = [normalize_card(card) for card in community_cards]

        # Remove any invalid cards from the lists
        hole_cards = [card for card in hole_cards if card]
        community_cards = [card for card in community_cards if card]

        player_cards = [Card.new(card) for card in hole_cards]
        board = [Card.new(card) for card in community_cards]

        score = evaluator.evaluate(board, player_cards)
        hand_class = evaluator.get_rank_class(score)
        hand_class_name = evaluator.class_to_string(hand_class)

        st.write(f"**Hand Strength:** {score} (1 = Strongest Hand, 7462 = Weakest Hand)")
        st.write(f"**Hand Class:** {hand_class_name}")
        st.write("---")

        return score, hand_class_name
    except Exception as e:
        st.error(f"Error occurred: {e}")
        return None, None

# AI Advice
def ai_advice(hand_strength, hand_class):
    if hand_strength is None:
        return "Error", "Unable to analyze hand."
    
    if hand_strength <= 200:  # Strong hands, top 3%
        return "Raise", "Your hand is very strong. You should raise!"
    elif 200 < hand_strength <= 1000:  # Medium hands, top 20%
        return "Call", "Your hand is decent. Calling would be a safe option."
    elif 1000 < hand_strength <= 3000:  # Weak hands, top 50%
        return "Call", "You have a decent hand. Calling might be a good option."
    else:  # Very weak hands
        return "Fold", "You have a weak hand. It's better to fold."

# Ask AI for strategy
def askAi(stage):
    try:
        playerInput = st.text_input("Ask AI for more detailed advice")
        response = model.generate_content(playerInput)
        return response.text
    except Exception as e:
        return f"Error occurred when asking AI: {e}"

# Player Input
def player_input(deck_id):
    if "community_cards" not in st.session_state:
        st.session_state["community_cards"] = [] #NEW
    if "pot_size" not in st.session_state:
        st.session_state["pot_size"] = 0
    if "current_bet" not in st.session_state:
        st.session_state["current_bet"] = 0
    if "player_action" not in st.session_state:
        st.session_state["player_action"] = None
    if "folded" not in st.session_state:
        st.session_state["folded"] = False

    st.subheader("Enter Your Cards")
    st.write("Input your cards in the format: RankSuit (e.g., Th for Ten of Hearts, Ah for Ace of Hearts)")
    player_cards = st.text_input("Input your cards here (separate with a space)")

    if player_cards:
        try:
            hole_cards = player_cards.split()
            if len(hole_cards) != 2:
                st.error("Please input exactly two cards.")
                return
            if not all(len(card) == 2 and card[0] in "23456789TJQKA" and card[1] in "cdhs" for card in hole_cards):
                st.error("Cards must be in the correct format (e.g., Ah, Ks).")
                return

            for card in hole_cards:
                usedCards.add(card)

            # Dealing Hole Cards
            st.write("**Your Hole Cards:**")
            cols = st.columns(len(hole_cards))
            for i, card in enumerate(hole_cards):
                cols[i].image(get_card_image_path(card), width=80)
            st.write("---")
            
            # Deal Community Cards
            if st.button("Deal Flop"): #NEW
                st.session_state["community_cards"].extend(drawCards(deck_id, 3))
            if st.button("Deal Turn"):
                st.session_state["community_cards"].extend(drawCards(deck_id, 1))
            if st.button("Deal River"):
                st.session_state["community_cards"].extend(drawCards(deck_id, 1))

            community_cards = st.session_state["community_cards"]
            if community_cards:
                st.write("**Community Cards:**")
                cols = st.columns(len(community_cards))
                for i, card in enumerate(community_cards):
                    cols[i].image(get_card_image_path(card), width=80)

                stage = "pre-flop" if len(community_cards) == 0 else "flop" if len(community_cards) == 3 else "turn" if len(community_cards) == 4 else "river"
                aiAdvice = askAi(stage)
                st.write(f"**AI Advice:** {aiAdvice}")
                
                hand_strength, hand_class_name = calculate_prob(hole_cards, community_cards)
                
               
                if hand_strength:
                    advice, advice_text = ai_advice(hand_strength, hand_class_name)
                    st.write(f"**AI Advice:** {advice} - {advice_text}")

                
                st.write("## Game Actions")
                st.write(f"**Current Pot Size:** {st.session_state['pot_size']}")
                col1, col2 = st.columns(2)

                # Raise Button
                with col1:
                    if st.button("Raise"):
                        st.session_state["raise_visible"] = True
                    if "raise_visible" in st.session_state and st.session_state["raise_visible"]:
                        raise_amount = st.number_input("Enter your raise amount:", min_value=1, step=1, key="raise_input")
                        if st.button("Confirm Raise"):
                            st.session_state["pot_size"] += raise_amount
                            st.session_state["current_bet"] += raise_amount
                            st.session_state["player_action"] = f"Raised by {raise_amount}"
                            st.session_state["raise_visible"] = False

                # Fold Button
                with col2:
                    if st.button("Fold"):
                        st.session_state["player_action"] = "Folded"
                        st.session_state["folded"] = True
                        st.write("**You have folded. Game over for you.**")
                        st.stop()

                # Display Player Action
                if st.session_state["player_action"]:
                    st.write(f"**Your Action:** {st.session_state['player_action']}")

        except Exception as e:
            st.error(f"An error occurred: {e}")

# Restart Game
if st.button("Reset Game"):
    st.session_state["community_cards"] = []
    st.session_state["pot_size"] = 0
    st.session_state["current_bet"] = 0
    st.session_state["player_action"] = None
    st.session_state["folded"] = False
    st.write("Game reset. You can now input new hole cards.")

# Run the App
player_input(deck)
