import os
import subprocess
import shutil
import argparse


def compile_makeheaders(basename="makeheaders"):
    execname = basename + "_exec"
    srcname = basename + ".c"

    print("Compile.")
    cmd = ["gcc", srcname, "-o", execname]
    p = subprocess.Popen(cmd)
    p.wait()

    return execname


def generate_headerfile(dirname,basefile="function"):
    execname = os.path.join(dirname,basefile + ".h")
    srcname =  os.path.join(dirname,basefile + ".c")

    print("Compile.")
    cmd = ["./makeheaders_exec", "-h", srcname]
    with open(execname, "w") as outfile:
        p = subprocess.Popen(cmd, stdout=outfile)

        p.wait()

    print("Done.")

def list_prototypes(dirname,base_function_name):
    header_file_full=os.path.join(dirname,base_function_name+".h")
    word=";"
    all_prototype_names=[]
    all_function_names = []
    with open(header_file_full) as f:
        lines = f.readlines()
        for line in lines:
            if line.find(word) != -1:
                # print(word, 'string exists in file')
                # print('Line Number:', lines.index(line))
                # print('Line:', line)

                value_function=line.strip().split("(")[0].split(" ")[1]
                all_function_names.append(value_function)
                all_prototype_names.append(line.strip())

    return all_function_names,all_prototype_names


def get_line_number(dirname,filename, funcnames):

    filename_full=os.path.join(dirname,filename+".c")
    function_names_line_list=[]


    for funcname in funcnames:
        funcname = funcname.strip().split("(")[0]
        # print(funcname)
        found = False
        with open(filename_full) as f:
            lines = f.readlines()
            for line in lines:
                if line.find(funcname) != -1:
                    if line.startswith(funcname+"("):
                        found = True
                        line_num=lines.index(line)
                        # print(funcname, 'string exists in file')
                        # print('Line Number:', line_num)
                        # print('Line:', line)
                        function_names_line_list.append(int(line_num))


        if found == False:
            function_names_line_list.append(-1)

    return function_names_line_list

def process_file(dirname,filename, line_num):
    filename_full=os.path.join(dirname,filename+".c")
    # print("opening " + filename_full + " on line " + str(line_num))

    code = ""
    cnt_braket = 0
    found_start = False
    found_end = False
    code_dict={}
    code_dict["line_start"]=line_num
    with open(filename_full, "r") as f:
        for i, line in enumerate(f):

            if(i >= (line_num - 1)):
                code += line

                if line.count("{") > 0:
                    found_start = True
                    cnt_braket += line.count("{")

                if line.count("}") > 0:
                    cnt_braket -= line.count("}")

                if cnt_braket == 0 and found_start == True:
                    found_end = True
                    # print("end_of_line: ",i)
                    code_dict["line_end"] = i
                    code_dict["code"]=code.strip()
                    return code_dict


def make_functions_multiple_architechture(dirname,base_function_name,multiple_architecture_list):
    base_function_name_full=os.path.join(dirname,base_function_name+".c")
    for architecture in multiple_architecture_list:
        shutil.copyfile(base_function_name_full, os.path.join(dirname,base_function_name+"_"+architecture+".c"))

def modify_multiple_architechture_files(dirname,line_number,all_prototype_names,multiple_architecture_list):
    for prototype in all_prototype_names:
        funcname = prototype.strip().split("(")[0].split(" ")[1]
        for architecture in multiple_architecture_list:
            architecture_file_name=os.path.join(dirname,base_function_name + "_" + architecture + ".c")
            replaced_content = ""
            with open(architecture_file_name, "r") as f:
                for i, line in enumerate(f):
                    
                    if (i == line_number):
                        new_line=line.replace(funcname, funcname+"_"+architecture)
                        
                    elif line.strip().startswith("printf") and i>line_number:

                        new_line=line.replace(f'"Using {funcname}()',f'"Using {architecture}_{funcname}()')
                        #new_line=line.replace(f'{funcname}()',f'{architecture}_{funcname}()')
                        #print("replaced: ", new_line)
                    else:
                        new_line=line
                    replaced_content = replaced_content + new_line
            # print(replaced_content)

            with open(architecture_file_name, "w") as f:
                f.write(replaced_content)


def compile_multiple_architechture_files(dirname,multiple_architecture_list):
    for architecture in multiple_architecture_list:
        architecture_file_name = os.path.join(dirname,base_function_name + "_" + architecture + ".c")
        architecture_file_name_exec = base_function_name + "_" + architecture + ".o"

        print("Compile.")
        if architecture=="asimd":
            cmd = ["gcc", "-g", "-O3", "-c","-march=armv8-a", architecture_file_name, "-o", architecture_file_name_exec]
        elif architecture=="sve":
            cmd = ["gcc", "-g", "-O3", "-c", "-march=armv8-a+sve", architecture_file_name, "-o",architecture_file_name_exec]

        elif architecture=="sve2":
            cmd = ["gcc", "-g", "-O3", "-c", "-march=armv8-a+sve2", architecture_file_name, "-o",architecture_file_name_exec]

        p = subprocess.Popen(cmd)
        p.wait()
        print("Done.")

def prototype_names_for_multiple_architechture(all_prototype_names,multiple_architecture_list):
    prototype_names_for_multiple_architechture_list=[]
    for prototype in all_prototype_names:
        for architecture in multiple_architecture_list:
            funcname = prototype.strip().split("(")[0]
            prototype_new=prototype.replace(funcname,funcname+"_"+architecture)
            prototype_names_for_multiple_architechture_list.append(prototype_new)
    return prototype_names_for_multiple_architechture_list



def make_ifunc(all_function_names, all_prototype_names,prototype_names_for_multiple_architechture_list,file_name="ifunc.c"):

    lines=[]
    with open(file_name, 'w') as f:
        lines.append('#include "ifunc.h"\n')
        lines.append('#include <sys/auxv.h>\n')
        lines.append('#include <stdio.h>\n')

        base_prototype_content=""
        for architecture_prototype in prototype_names_for_multiple_architechture_list:
            function_first_part =architecture_prototype.split("(")[0].split(" ")[1].split("_")[0]
            function_last_part = architecture_prototype.split("(")[0].split(" ")[1].split("_")[-1]
            function_return_type=architecture_prototype.split("(")[0].split(" ")[0]
            
            #print(function_first_part,function_last_part)
            
            base_prototype_content += f"{function_return_type} *{function_first_part}_{function_last_part}(unsigned char *image,int x_size,int y_size,float red_factor,float green_factor,float blue_factor)\n" + \
                                      "{\n" + \
                                      "\t" + architecture_prototype + \
                                      "\n}\n"

        lines.append(base_prototype_content)

        for i,prototype in enumerate(all_prototype_names):
            line_1 = f'__attribute__(( ifunc("resolver_{all_function_names[i]}") )) '+ prototype+"\n\n"

            
            line_2 = f'static void (*resolver_{all_function_names[i]} (void))\n' \
                    '{ \n' \
                        '   long hwcaps  = getauxval(AT_HWCAP);\n' \
                        '   long hwcaps2 = getauxval(AT_HWCAP2);\n' \
                        f'   printf("### Resolver function - selecting the implementation to use for  {all_function_names[i]}()");\n'\
                        '   if (hwcaps2 & HWCAP2_SVE2) {\n'\
                        f'          return {all_function_names[i]}_sve2;\n'\
                        '   }  else if (hwcaps & HWCAP_SVE) {\n' \
                        f'          return {all_function_names[i]}_sve;\n' \
                        '   }  else {\n'\
                        f'          return {all_function_names[i]}_asimd;\n'\
                        '   }\n'\
            '};\n'
            lines.append(line_1)
            lines.append(line_2)

        f.writelines(lines)


def make_ifunc_header(prototype_names_for_multiple_architechture_list,file_name="ifunc.h"):
    with open(file_name, 'w') as f:
        base_prototype_content = ""
        for architecture_prototype in prototype_names_for_multiple_architechture_list:

            base_prototype_content += architecture_prototype+"\n"

        f.write(base_prototype_content)

def final_compile_main(base_function_name="function",main_file_name="main",function_name="ifunc"):
    main_file_name_full=main_file_name+".c"
    function_name_full=function_name+".c"
    
    
    print("Compile.")
    #cmd = ["gcc", "-g", "-O3", "-march=armv8-a", main_file_name_full,function_name_full,"function_sve2.o","function_sve.o","function_asimd.o", "-o", main_file_name]
    cmd = ["gcc", "-g", "-O3", "-march=armv8-a", main_file_name_full,function_name_full,base_function_name+"_sve2.o",base_function_name+"_sve.o",base_function_name+"_asimd.o", "-o", main_file_name]

    p = subprocess.Popen(cmd)
    p.wait()
    print("Done.")

if __name__ == '__main__':
    
    # Create the parser
    parser = argparse.ArgumentParser()
    # Add an argument
    parser.add_argument('--inputfile',type=str, required=True)
    # Parse the argument
    args = parser.parse_args()
    
    base=os.path.basename(args.inputfile)
    function_dirname = os.path.dirname(args.inputfile)

    base_function_name=os.path.splitext(base)[0] #taking only the name
    basename = "makeheaders"
    execname = compile_makeheaders(basename)
    generate_headerfile(function_dirname,base_function_name)

    all_function_names,all_prototype_names=list_prototypes(function_dirname,base_function_name)
    print("function names: ",all_function_names)
    print("prototype names: ", all_prototype_names)

    multiple_architecture_list = ["sve2","sve","asimd"]
    make_functions_multiple_architechture(function_dirname,base_function_name, multiple_architecture_list)


    prototype_names_for_multiple_architechture_list=prototype_names_for_multiple_architechture(all_prototype_names,multiple_architecture_list)
    #print(prototype_names_for_multiple_architechture_list)


    start_line_numbers=get_line_number(function_dirname,base_function_name,all_prototype_names)
    # print(start_line_numbers)
    for line_number in start_line_numbers:
        if line_number > 0:
           code_dict_information=process_file(function_dirname,base_function_name, line_number)
           #print(code_dict_information)
           modify_multiple_architechture_files(function_dirname,line_number,all_prototype_names,multiple_architecture_list)

    compile_multiple_architechture_files(function_dirname,multiple_architecture_list)


    make_ifunc_header(prototype_names_for_multiple_architechture_list)
    make_ifunc(all_function_names,all_prototype_names,prototype_names_for_multiple_architechture_list)

    final_compile_main(base_function_name)





