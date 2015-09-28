import sys
import copy
import os.path

"""" COMPUTE PROBABILITY FOR LINE 1"""
def compute_porbability(disease_name,list):

    product1=1
    probability_list=P_symptom_T_disease_T[disease_name]
    list_item=0
    for literal in list:
        if literal=="T":
            print 
            product1=product1*probability_list[list_item]
        if literal=="F":
            product1=product1*(1-probability_list[list_item])
        list_item=list_item+1
   
    product1=product1*P_disease[disease_name]


    product2=1
    probability_list=P_symptom_T_disease_F[disease_name]
    list_item=0
    for literal in list:
        if literal=="T":
            print 
            product2=product2*probability_list[list_item]
        if literal=="F":
            product2=product2*(1-probability_list[list_item])
        list_item=list_item+1
   
    product2=product2*(1-P_disease[disease_name])


    temp_probability=product1/(product1+product2)
    probability = float("{0:.4f}".format(temp_probability))
    probability=format(probability, '.4f')
    return probability

""" COMPUTE LIST COMBINATIONS"""
def compute_combinations(list):
    templist=[]
    for literal in list:
        if literal == "T" or literal=="F":
            if len(templist)==0:
                templist.append([literal])
            else:
                for list_x in templist:
                    list_x.append(literal)

        elif literal =="U":
            if len(templist)==0:
                templist.append(['T'])
                templist.append(['F'])
            else:
                templist_1=[]
                for list_x in templist:
                    list_t=copy.copy(list_x)
                    list_t.append('T')
                    list_f=copy.copy(list_x)
                    list_f.append('F')
                    templist_1.append(list_t)
                    templist_1.append(list_f)
                del templist[:]
                templist=copy.copy(templist_1)
                del templist_1[:]

    return templist

""" COMPUTE MAX_PROBABILITY"""
def compute_max_probability(disease_name,list_combinations):

    max_probabilty=0
    for list in list_combinations:
        probablity=compute_porbability(disease_name,list)
        if (float(probablity) > float(max_probabilty)):
            max_probabilty=probablity

    return max_probabilty

""" COMPUTE MIN_PROBABILITY"""
def compute_min_probability(disease_name,list_combinations):

    min_probabilty=1
    for list in list_combinations:
        probablity=compute_porbability(disease_name,list)
        if (float(probablity) < float(min_probabilty)):
            min_probabilty=probablity

    return min_probabilty

""" COMPUTE SINGULAR LIST COMBINATIONS"""
def compute_singular_combinations(disease_name,list):
    tempdict={}
    list_len=len(list)

    for i in range(0,list_len):
        if list[i]=="U":
          list_x=copy.copy(list)
          list_x[i]='T' 
          list_t=copy.copy(list_x)
          list_y=copy.copy(list)
          list_y[i]='F' 
          list_f=copy.copy(list_y)
          cur_symptom=symptoms[disease_name][i]
          tempdict[cur_symptom]=[list_t,list_f]
    return tempdict

""" COMPUTE PERCENTAGE INCREASE AND DECREASE"""
def compute_increase_deccrease_list(disease_name,probability,singular_dictionay_combinations):
    if len(singular_dictionay_combinations)==0:
        return ['none','N','none','N']

    max_increase=0
    max_symptom=""
    max_indicator=""

    max_decrease=0
    min_symptom=""
    min_indicator=""

    for key in singular_dictionay_combinations:
       values=singular_dictionay_combinations[key]
       for list in values:
           temp_probability=compute_porbability(disease_name,list)
           if(temp_probability > probability):
               increase=(float(temp_probability)-float(probability))/float(probability)
               if (float(increase) > float(max_increase)):
                  max_increase=increase
                  max_symptom=key
                  temp_index=symptoms[disease_name].index(key)
                  max_indicator=list[temp_index]
               elif (float(increase) == float(max_increase)):
                   temp_symptom=key
                   if(temp_symptom < max_symptom):
                       max_symptom=key
                       temp_index=symptoms[disease_name].index(key)
                       max_indicator=list[temp_index]
                   


    for key in singular_dictionay_combinations:
      values=singular_dictionay_combinations[key]
      for list in values:
          temp_probability=compute_porbability(disease_name,list)
          if(temp_probability < probability):
              decrease=(float(probability)-float(temp_probability))/float(probability)
              if (float(decrease) > float(max_decrease)):
                 max_decrease=decrease
                 min_symptom=key
                 temp_index=symptoms[disease_name].index(key)
                 min_indicator=list[temp_index]
              elif (float(decrease) == float(max_decrease)):
                   temp_symptom=key
                   if(temp_symptom < min_symptom):
                       min_symptom=key
                       temp_index=symptoms[disease_name].index(key)
                       min_indicator=list[temp_index]

    if (max_increase==0):
        max_symptom="none"
        max_indicator="N"
    if (max_decrease==0):
        min_symptom="none"
        min_indicator="N"

    return [max_symptom,max_indicator,min_symptom,min_indicator]


""" PERFORM INFERENCE"""
def perform_inference(diseases_number,patients_number,filename):
     filename=filename[:-4]
     output_filename=filename+"_inference.txt"
     outputFile = open(output_filename,'a')
     curr_patient_no=1
     for i in range(0,patients_number):
         #Line1
         P_diseases_for_patient={}
         P_disease_max_min={}
         P_disease_inc_dec={}
         outputFile.write("Patient-"+curr_patient_no)
         
         for j in range(0, diseases_number):
             disease_name=diseases[j]

             #Line2
             probability=compute_porbability(disease_name,patient_disease_list[(i*diseases_number)+j])
             P_diseases_for_patient[disease_name]=probability  
             
             #Line3
             list_combinations=compute_combinations(patient_disease_list[(i*diseases_number)+j])    
             max_probability=compute_max_probability(disease_name,list_combinations)
             min_probability=compute_min_probability(disease_name,list_combinations)
             P_disease_max_min[disease_name]=[min_probability,max_probability]

             #Line4
             singular_dictionay_combinations=compute_singular_combinations(disease_name,patient_disease_list[(i*diseases_number)+j])  
             increase_decrease_list=compute_increase_deccrease_list(disease_name,probability,singular_dictionay_combinations)
             P_disease_inc_dec[disease_name]=increase_decrease_list

         dictionary_string_1=str(P_diseases_for_patient)  
         dictionary_string_2=str(P_disease_max_min)
         dictionary_string_3=str(P_disease_inc_dec)
         outputFile.write("\n")     
         outputFile.write(dictionary_string_1)
         outputFile.write("\n")
         outputFile.write(dictionary_string_2)
         outputFile.write("\n")
         outputFile.write(dictionary_string_3)
         outputFile.write("\n")
         curr_patient_no=curr_patient_no+1

     outputFile.close()

""" READ THE INPUT FILE """
def read_input():
    filename=sys.argv[2]
    inputFile = open(sys.argv[2])
    clear(filename)
    line_number=1
    diseases_number=0                     
    patients_number=0
    disease_name=""
    for line in inputFile:
        if line_number==1:
            spl = line.strip().split(' ')
            diseases_number=int(spl[0])
            patients_number=int(spl[1])
            line_number=line_number+1
        elif line_number <=((4*diseases_number)+1):
            if line_number % 4 == 2:
               spl = line.strip().split(' ')
               disease_name=spl[0]
               diseases.append(disease_name)
               symptom_number[disease_name]=int(spl[1])
               P_disease[disease_name]=float(spl[2])
               P_N_disease[disease_name]=1-float(spl[2])
            elif line_number % 4 ==3:
               symptom_list=eval(line)
               symptoms[disease_name]=symptom_list
            elif line_number % 4 ==0:
               symptom_list=eval(line)
               P_symptom_T_disease_T[disease_name]=symptom_list
            elif line_number % 4 ==1:
               symptom_list=eval(line)
               P_symptom_T_disease_F[disease_name]=symptom_list
            line_number=line_number+1
        else:
          P_list=eval(line)
          patient_disease_list.append(P_list)
    
    inputFile.close()  
    perform_inference(diseases_number,patients_number,filename)

""" GLOBAL VARIABLES """
diseases=[]                                         #List of diseases
symptom_number={}                                   #Dictionary of (NO_symptoms)/disease
symptoms={}                                         #Dictionary of (List of Symptoms)/disease
P_disease={}                                        #Dictionary of (probability of disease)/disease
P_N_disease={}                                      #Dictionary of (probability of not_disease)/disease
P_symptom_T_disease_T={}                            #Dictionary of (List of CP of symptom/disease )/disease
P_symptom_T_disease_F={}                            #Dictionary of (List of CP of symptom/~disease )/disease
patient_disease_list=[]                             #List of Patient Fndindgs

""" CLEAR THE OUTPUT FILE """
def clear(filename):
    filename=filename[:-4]
    output_filename=filename+"_inference.txt"
    outputFile = open(output_filename,'w')
    outputFile.truncate()
    outputFile.close()

""" PROGRAM BEGINING """
#read_input()


