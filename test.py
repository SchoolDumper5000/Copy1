
import survey

# Simple test
options = ["Option 1", "Option 2", "Option 3"]
print("About to show survey menu...")
try:
    index = survey.routines.select(
        'Please select an option:\n',
        options=options,
        focus_mark='> ',
        evade_color=survey.colors.basic('white'),
        insearch_color=survey.colors.basic('white')
    )
    print(f"You selected: {options[index]} (index: {index})")
except Exception as e:
    print(f"Error: {e}")
