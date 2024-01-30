import os

number_of_programs = 16
program_to_replicate = "one_million_constraint_program"
program_folder = "programs_to_deploy"

program_path_to_replicate = os.path.join(os.getcwd(), program_to_replicate)
path_to_program_folder = os.path.join(os.getcwd(), program_folder)

# create the folder if it does not exist
if not os.path.exists(path_to_program_folder):
    os.makedirs(path_to_program_folder)

programs_do_deploy = []

def get_program_name(i):
    name = ''
    while i >= 0:
        name = chr(ord('a') + i % 26) + name
        i = i // 26 - 1
    return name

for i in range(number_of_programs):
    # for program name get i-th letter of the alphabet, of if i >= 26, get the i-th letter of the alphabet + the i-th letter of the alphabet
    program_name = get_program_name(i)
    program_path = os.path.join(path_to_program_folder, program_name)
    os.system(f"cp -r {program_path_to_replicate} {program_path}")

    cmd = (
        f"find {program_path} -type f "
        f"-exec perl -i -pe 's/{program_to_replicate}/{program_name}/g' {{}} +"
    )
    os.system(cmd)



    print(f"Created program {program_name} at {program_path}")
    programs_do_deploy.append(program_name)

# create a file programs.txt with the names of the programs to deploy
with open(os.path.join(path_to_program_folder, "programs.txt"), "w") as f:
    f.write("\n".join(programs_do_deploy))