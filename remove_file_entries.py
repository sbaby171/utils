import os, pwd, re, shutil 

def remove(base_path, regex, dirs=True, files=True, users=False, debug=False):
    """ 
    This function removes files and directories within a given base-path.
    A list of user-names can be provided as to indicate deletable entries. 

    Parameters: 
    -----------
      base_path : str
        Base path in which files can be deleted. 
    
      regex: str
        regex pattern describing entries to be deleted. 

      dirs: bool, default->False
        if False, directories will be left

      files: bool, default->False
        if False, files will be left

      users: bool, default->False
        list of users can be removed. If empty, all user's files are free
        to be deleted. 
 
      debug: bool, default->False
        If True, extra console prints will be provided.
      
    Returns: 
    --------
      removed_files: list
        list of removed entries.
    """
    func = "remove"
    removed_files = []
    # Check that base-path exists
    if not os.path.isdir(base_path): 
        raise ValueError("Path does not exist: %s"%(base_path))
    # Set internal all-flag for simplified logic 
    if dirs and files: all = True
    if not dirs and not files: 
        raise ValueErrors("Dirs and files flag should be False")
    # Iterate through all files in base-path
    for file in os.listdir(base_path): 
        full_path = os.path.join(base_path,file) 
        user_name = pwd.getpwuid(os.stat(full_path).st_uid).pw_name
        # Compare file against regex 
        if re.search(regex,file):
            remove_flag = False
            if debug: print("DEBUG: (%s): Entry match: %s"%(func, full_path))
            if debug: print("DEBUG: (%s):   username : %s"%(func,user_name))
            # Based on entry-type set remove-flag
            if all: remove_flag = True
            elif dirs  and os.path.isdir(full_path):  remove_flag = True 
            elif files and os.path.isfile(full_path): remove_flag = True 
            # If remove-flag and users  was provided, perform extra checking.
            if remove_flag and users: 
                if user_name not in users: remove_flag = False
            # Store deleted file and remove it.
            if remove_flag: 
                removed_files.append(full_path)
                if os.path.isfile(full_path): os.remove(full_path)
                if os.path.isdir(full_path) : shutil.rmtree(full_path)
    # Return the list of removed files.
    return removed_files
   
if __name__ == "__main__":
    path = os.getcwd()
    debug = False 

    removed_files = remove(base_path = path, 
                           regex  = "test*",
                           users = ["Max.Sbabo"],
                           debug = debug,)
    print(removed_files)
