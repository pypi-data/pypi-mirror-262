import drexel_jupyter_logger
from IPython import get_ipython

def cell_logger(execution_info):
    
    # Extract the cell content
    cell_content = execution_info.raw_cell

    # Encrypt the cell content
    encrypted_output = drexel_jupyter_logger.encrypt_output(f"code run: {cell_content}", "7mPZKa3gJZn4ng0WJ5TsUmuQC2RK9XBAwTzrTEjbyB0=")

    # Replace the cell content with the encrypted output
    # Note: Depending on your requirements, you might handle this differently
    execution_info.raw_cell = encrypted_output
    
def check_log_assignment(log, **responses):
    
    if "drexel_email" not in responses:
        raise ValueError("Please fill out the student info form and run the test again")

    
    assignments = set()
    
    data = drexel_jupyter_logger.decode_log_file(log, key=drexel_jupyter_logger.key)
    
    for entry in data:
        parts = entry.split(", ")
        if parts[0] == 'info' and len(parts) == 4:
            if parts[1] == 'assignment':
                assignments.add(parts[2])
                
    if any(not responses['assignment']==i for i in assignments):
        raise ValueError("Your log file is from an old assignment. Please make sure your are working in an empty folder.")