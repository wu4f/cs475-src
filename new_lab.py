import os

lab_name = input("Enter the lab name: ")
lab_number = input("Enter the lab number: ")

def get_existing_labs():
    """Get all existing lab directories and their numbers"""
    labs = []
    for item in os.listdir('.'):
        if os.path.isdir(item) and item[0:2].isdigit() and item[2] == '_':
            labs.append((int(item[0:2]), item))
    return sorted(labs)

def increment_labs_from(start_number: int):
    """Increment lab numbers starting from the given number"""
    existing_labs = get_existing_labs()
    
    # Process labs in reverse order to avoid conflicts
    for lab_num, lab_dir in reversed(existing_labs):
        if lab_num >= start_number:
            new_num = lab_num + 1
            new_dir = f"{new_num:02d}_{lab_dir.split('_', 1)[1]}"
            print(f"Renaming {lab_dir} to {new_dir}")
            os.rename(lab_dir, new_dir)

def create_new_lab(lab_number: int, lab_name: str):
    """Create a new lab directory"""
    # Force camel case on lab_name (capitalize first letter of each word, remove spaces)
    camel_case_name = ""
    for word in lab_name.split(" "):
        if len(word) > 0:  # Skip empty strings
            if len(word) == 1:
                camel_case_name += word.upper()
            else:
                camel_case_name += word[0].upper() + word[1:]
    
    lab_dir = f"{int(lab_number):02d}_{camel_case_name}"
    
    # Check if directory already exists
    if os.path.exists(lab_dir):
        print(f"Directory {lab_dir} already exists!")
        return
    
    # Create the lab directory
    os.makedirs(lab_dir)
    print(f"Created directory: {lab_dir}")

# Main logic
try:
    target_number = int(lab_number)
    
    # Check if a lab with this number already exists
    existing_labs = get_existing_labs()
    existing_numbers = [num for num, _ in existing_labs]
    
    if target_number in existing_numbers:
        print(f"Lab {target_number:02d} already exists. Incrementing subsequent labs...")
        increment_labs_from(target_number)
    
    # Create the new lab
    create_new_lab(lab_number, lab_name)
    
    print(f"\nNew lab '{lab_name}' created successfully as {target_number:02d}_{lab_name}")
    print("\nUpdated lab structure:")
    updated_labs = get_existing_labs()
    for num, lab_dir in updated_labs:
        print(f"  {lab_dir}")
        
except ValueError:
    print("Error: Lab number must be a valid integer")
except Exception as e:
    print(f"Error: {e}")

