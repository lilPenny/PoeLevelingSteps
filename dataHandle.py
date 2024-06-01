import json
import os

# Ścieżki do plików JSON
change_file_path = os.path.join(os.path.dirname(__file__), 'json', 'change.json')
areas_file_path = os.path.join(os.path.dirname(__file__), 'json', 'areas.json')
quests_file_path = os.path.join(os.path.dirname(__file__), 'json', 'quests.json')

# Wczytanie plików JSON
with open(change_file_path, 'r') as change_file:
    change_data = json.load(change_file)

with open(areas_file_path, 'r') as areas_file:
    areas_data = json.load(areas_file)

with open(quests_file_path, 'r') as quests_file:
    quests_data = json.load(quests_file)

# Inicjalizacja pustej listy do przechowywania kroków
steps = []

# Funkcja do przetwarzania kroków
def process_steps(steps_data, current_steps):
    for step in steps_data:
        if 'parts' in step:
            for part in step['parts']:
                if isinstance(part, dict):
                    if part.get('type') == 'enter': # Handle enter area
                        area_id = part.get('areaId')
                        area_name = areas_data.get(area_id, {}).get('name', 'Unknown Area')
                        current_steps.append(f"{{{len(current_steps)}}} Enter {area_name}") 
                    
                    elif part.get('type') == 'quest': # Hadle Hand in quests
                        quest_id = part.get('questId')
                        quest_name = quests_data.get(quest_id, {}).get('name', 'Unknown Area')
                        current_steps.append(f"{{{len(current_steps)}}} Hand in {quest_name}")
                    
                    elif 'kill' in part.get('type'):  # Handle kill 
                        values = " ".join(value for key, value in part.items() if key != 'type')
                        current_steps.append(f"{{{len(current_steps)}}} Kill {values}") 
                   
                    elif part.get('type') == 'waypoint_get': # Handle get waypoint
                        current_steps.append(f"{{{len(current_steps)}}} Get Waypoint")
                   
                    elif part.get('type') == 'portal_use':  # Handle "portal_use"
                        area_id = part.get('dstAreaId')
                        area_name = areas_data.get(area_id, {}).get('name', 'Unknown Area')
                        current_steps.append(f"{{{len(current_steps)}}} Use portal to {area_name}")
                   
                    elif part.get('type') == "area": # Handle Place portal
                        area_id = part.get('areaId')
                        area_name = areas_data.get(area_id, {}).get('name', 'Unknown Area')
                        current_steps.append(f"{{{len(current_steps)}}} Find {area_name}, place portal")
                   
                    elif part.get('type') == 'arena':  # Hadnle Enter by type arena
                        values = " ".join(value for key, value in part.items() if key != 'type') 
                        current_steps.append(f"{{{len(current_steps)}}} Enter {values}")

                    elif part.get('type') == 'portal_set':  # Handle specific portal set instructions
                        value = step['parts'][0]
                        if value == "Place ":
                            value1 = step['parts'][2]
                            current_steps.append(f"{{{len(current_steps)}}} {value}portal{value1}")
                        elif "Find, bridge" in value:
                            current_steps.append(f"{{{len(current_steps)}}} {value}portal")
                                       
                    elif part.get('type') == 'generic':  # Handle type generic"
                        value = step['parts'][0]
                        values = " ".join(value for key, value in part.items() if key != 'type') 
                        current_steps.append(f"{{{len(current_steps)}}} {value}{values}")
                   
                    elif part.get('type') == 'quest_text':  # Handle specific kill instructions"
                        value = step['parts'][0]
                        if part.get('type') == 'kill':
                            values = " ".join(value for key, value in part.items() if key != 'type') 
                            current_steps.append(f"{{{len(current_steps)}}} {value}{values}")
                        elif part.get('value') == 'Slave Girl':
                            current_steps.append(f"{{{len(current_steps)}}} Find Slave Girl")
                        else:
                            values = " ".join(value for key, value in part.items() if key != 'type')
                            current_steps.append(f"{{{len(current_steps)}}} Take {values}")
                  
                    elif part.get('type') == 'trial':  # Handle Trials completion
                        current_steps.append(f"{{{len(current_steps)}}} Complete Trial of Ascendancy")
                    
                    elif part.get('type') == 'ascend':  # Handle Ascendent class labs"
                        current_steps.append(f"{{{len(current_steps)}}} Ascend")
                   
                    elif part.get('type') == 'crafting':  # Handle get crafting recipies
                        value = step['parts'][0]
                        values = part['crafting_recipes']
                        current_steps.append(f"{{{len(current_steps)}}} {value}crafting recipie {values}")
                  
                    elif part.get('type') == 'waypoint_use':  # Handle portal use with type dstArea
                        area_id = part.get('dstAreaId')
                        area_name = areas_data.get(area_id, {}).get('name', 'Unknown Area')
                        current_steps.append(f"{{{len(current_steps)}}} Use waypoint to {area_name}")
                    
                    elif part.get('type') == 'logout':  # Handle logout to town area
                        area_id = part.get('areaId')
                        area_name = areas_data.get(area_id, {}).get('name', 'Unknown Area')
                        current_steps.append(f"{{{len(current_steps)}}} Logout {area_name}")


               #     else:
               #         key_values = " ".join(f"{key} {value}" for key, value in part.items())
                #    current_steps.append(f"{{{len(current_steps)}}} {key_values}")
        if 'subSteps' in step:
            process_steps(step['subSteps'], current_steps)

# Przetwarzanie każdego aktu
for act in change_data:
    steps.append(f"[{act['name']}]")
    process_steps(act['steps'], steps)

# Wyświetlenie zawartości listy steps
for step in steps:
    print(step)
