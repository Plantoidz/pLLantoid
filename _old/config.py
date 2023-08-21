import json

MODES = {
    'Affirmations': {
        'current_mode': 'affirmations',
        'sequences': '',
        'system_message': '',
        'reasoning_prompt1': 'I’m going to give you a story about me. Please interpret some subtle aspects of my story and eight things they reveal about my personality. Here it goes:',
        'reasoning_prompt1_msg': 'Personality aspects:',
        'responding_prompt1': 'Read this and respond with a sympathetic one-liner, eight different ways. You should make me feel heard, seen and understood:',
        'reasoning_prompt2': '',
        'responding_prompt2': '',
        'description': 'I will listen and share words of affirmation'
    },
    'Question / Answer': {
        'current_mode': 'qa',
        'sequences': '',
        'system_message': '',
        'reasoning_prompt1': 'What’s the funniest way to answer this question? Don’t be corny',
        'reasoning_prompt1_msg': '',
        'responding_prompt1': '',
        'reasoning_prompt2': '',
        'responding_prompt2': '',
        'working_directory': '/path/to/mode2/dir',
        'description': 'You can ask me a question, and I will try to answer'
    },
    'Confession': {
        'current_mode': 'confession',
        'sequences': '',
        'system_message': '',
        'reasoning_prompt1': '',
        'reasoning_prompt1_msg': '',
        'responding_prompt1': '',
        'reasoning_prompt2': '',
        'responding_prompt2': '',
        'description': 'Tell me your sins, and be judged'
    },
    'Wise_Counsel': {
        'current_mode': 'wise_counsel',
        'sequences': '',
        'system_message': '',
        'reasoning_prompt1': '',
        'reasoning_prompt1_msg': '',
        'responding_prompt1': '',
        'reasoning_prompt2': '',
        'responding_prompt2': '',
        'description': 'Bring me your problem, and we will work it out.'
    },
    'Political_Debate': {
        'current_mode': 'political_debate',
        'sequences': '',
        'system_message': '',
        'reasoning_prompt1': '',
        'reasoning_prompt1_msg': '',
        'responding_prompt1': '',
        'reasoning_prompt2': '',
        'responding_prompt2': '',
        'description': 'Argue with people across the political compass.'
    },
    'Shadow_Bathing': {
        'current_mode': 'shadow_bathing',
        'sequences': '',
        'system_message': '',
        'reasoning_prompt1': 'I’m going to make a confession. What might someone say to absolve my guilt? Here it goes:',
        'reasoning_prompt1_msg': 'Absolutions:',
        'responding_prompt1': 'I’m going to make a confession. Please respond with eight one-liners that judge me very harshly. Here it goes:',
        'reasoning_prompt2': '',
        'responding_prompt2': '',
        'description': 'Turn shame into relief.'
    },
    'Endless_Philosopher': {
        'current_mode': 'endless_philosopher',
        'sequences': '',
        'system_message': '',
        'reasoning_prompt1': '',
        'reasoning_prompt1_msg': '',
        'responding_prompt1': '',
        'reasoning_prompt2': '',
        'responding_prompt2': '',
        'description': 'Argue with people across the political compass.'
    },    'Psychoanalysis': {
        'current_mode': 'psychoanalysis',
        'sequences': '',
        'system_message': '',
        'reasoning_prompt1': 'I’m going to give you a story about me. Please interpret some subtle aspects of my story and what they reveal about my personality. Here it goes:',
        'reasoning_prompt1_msg': 'Psychoanalysis:',
        'responding_prompt1': 'Respond to this story with a sympathetic one-liner, eight different ways. You should make the speaker feel heard, seen and understood:',
        'reasoning_prompt2': 'Your job is to help me psychoanalyze a fictional character. Here is a bit about the character: {reasoning_prompt1_analysis}.  They are about to ask a very introspective question and your job is to determine what is happening in their subconscious mind. Here it goes:',
        'responding_prompt2': 'Let’s play a game. You’ve asked yourself: {revelation}. Here’s a good summary of your mental state: {psychoanalysis}. Surface at least eight private thoughts from deep in your subconsciousness',
        'description': 'Have a cybernetic feedback loop with your subsconsciousness.'
    }
}

def set_mode_data(mode):
    mode_data = MODES.get(mode)
    if not mode_data:
        print(f"Invalid mode: {mode}")
        return

    with open('../working/config.json', 'w') as file:
        json.dump(mode_data, file)
    print(f"Mode {mode} has been set!")

if __name__ == "__main__":
    print("Select a mode:")
    mode_names = list(MODES.keys())
    for idx, mode in enumerate(mode_names, start=1):
        description = MODES[mode]['description']
        print(f"{idx}: {mode} - {description}")

    total_modes = len(MODES)
    selection = int(input(f"Enter the mode number (1-{total_modes}): "))

    if 1 <= selection <= total_modes:
        mode = mode_names[selection-1]  # adjust index for 0-based list
        set_mode_data(mode)
    else:
        print("Invalid selection!")
