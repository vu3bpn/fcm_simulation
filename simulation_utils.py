import pandas as pd
import os

def get_initial_simulation_values(output_dir,transform_mat):
    """
    Read initial values from an Excel file or create a new one if it does not exist.
    If the file exists, it reads the initial values; otherwise, it creates a new file with default values.
    The function also ensures that the output directory exists.
    It returns a DataFrame with the initial values for the simulation.
    
    Args:
        output_dir (str): Path to the output directory.
    """
    inital_values_filename = os.path.join(output_dir, 'initial_values.xlsx')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not os.path.exists(inital_values_filename):
        parameters = transform_mat.columns.tolist()
        values_dict = [{param: 1 for param in parameters}]
        initial_values = pd.DataFrame(values_dict)
        initial_values.to_excel(inital_values_filename, index=False)
    else:
        initial_values = pd.read_excel(inital_values_filename)
    return initial_values

def simulate(output_dir,
             transform_mat,
             name = 'simulation',
             decimation = 10
            ):
    results = pd.DataFrame()
    initial_values = get_initial_simulation_values(output_dir,transform_mat)
    idx2 = 1
    for initial_value in initial_values.iterrows():
        initial_value = initial_value[1] 
        values = initial_value.copy()
        #values = initial_values.copy()
        for idx in range(decimation):
            values = values + (1.0/decimation)*values.dot(transform_mat)
        rel_change = 100*(values-initial_value)/initial_value
        #result = pd.concat([initial_value,values,rel_change],ignore_index=True)
        #result.insert(0,"Parameter", [f'Initial Value {idx}','Simulated value {idx}', 'Relative change (%) {idx}'])
        result = pd.concat([initial_value,values,rel_change],axis=1,ignore_index=True).T
        description = pd.DataFrame({"Parameter": [f'Initial Value {idx2}',f'Simulated value {idx2}', f'Relative change (%) {idx2}']})
        #result.insert(0,description)
        result = pd.concat([description,result],axis=1)
        idx2+=1        
        results = pd.concat([results,result],axis=0,ignore_index=True)
    results.to_excel(os.path.join(output_dir,f"{name}_results.xlsx"))
    return results
    
    
    