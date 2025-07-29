import requests

def find_words(sequence):
    # Build the URL with the wildcard (*) around the sequence
    url = f"https://api.datamuse.com/words?sp=*{sequence}*"
    response = requests.get(url)
    
    if response.status_code == 200:
        # Parse JSON response
        words_data = response.json()
        return [word_info for word_info in words_data]
    else:
        print("Error fetching data from the API.")
        return []

def main():
    # Get user input
    user_input = input("Enter a 2-3 letter sequence (e.g., 'mpe'): ").strip()
    if not user_input:
        print("You did not enter any sequence!")
        return
    
    words = find_words(user_input)
    
    if words:
        print(f"Words containing '{user_input}':")
        print(words[2]['word'])
        # for word in words:
        #     print(word)
    else:
        print(f"No words found containing '{user_input}'.")

if __name__ == "__main__":
    main()
