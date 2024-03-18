from . import ReadingPython, SelectQuestion, MultipleChoice, MCQ, MultiSelectQuestionWidget, MultiSelect

class ReadingPythonQuestion_f2024_V2(ReadingPython):
   
   def __init__(self,
            title = "Reading, Commenting, and Interpreting Python Code:",
            question_number = 4,
            key="READING1",
            options={
               # General list of 15 potential comments with only one correct per line
               "comments_options" : [
                  None,
                  "Initializes a list of numbers with integers and floats.",  
                  "Initializes the variable sum_ to 0.",  
                  "A while loop based on the condition of 'sum_' being less than 6.",  
                  "Iterates over each item in the 'numbers' list using a for loop.",  
                  "Checks if the current number is evenly divisible by 2.",  
                  "Add and assigns sum_ with 2 times the number, num if even.",
                  "Add and assigns sum_ with 2 times the number, num if odd.",
                  "Add and assigns sum_ with number, num if odd.",    
                  "Adds 2 times the number, num if even.",
                  "Adds 2 times the number, num if odd.", 
                  "Defines a function.",
                  "Imports a module.",
                  "Prints output to the console.",
                  "Catches an exception.",
                  "Returns a value from a function.",
                  "Initializes a dictionary of numbers with integers and floats.",
                  "Initializes a tuple of numbers with integers and floats.",
               ],
               # Define the number of rows you want ahead of time
               "n_rows" : 20,  # for example, 5 rows'
               "n_required" : 13,  # number of rows required to respond. 
               # Lines of code that require commenting
               "lines_to_comment" : [1, 2, 4, 5, 6, 7, 9],
               # Table headers
               "table_headers" : ['Step', 'Line Number', 'Variable Changed', 'Current Value', 'DataType'],
               # Variables Changed
               "variables_changed" : ["", 'None','numbers', 'num', 'sum_', 'if', 'else'],
               "current_values" : ["", "None", "[5, 2.0, 3.0]", "[5, 2, 3]", "3", "2", "2.0", "5", "3.0", "5.0", "2.0", "0", "0.0","9","9.0","12",'12.0',"True", "False"],
               "datatypes" : ["", "NoneType", "list", "dictionary", "tuple", "set", "string", "float", "integer", "boolean"],
               }, 
            solutions = {"comment" : [b'gAAAAABl6Sby9zpSpHL5RE96n2KQBeLoIhr6j824-nYPGMH0U6wISx1SyIn-A8-EBmA2QYJD3Pzz9qQpBMDMk6ph-tzlrDJYSQpX5Za3i-sT3ARggbhQA2Hq9jffC-m4JYCcbB5QHucTf8tFwzQ_XYx31EZLQ1dG4Q==',
            b'gAAAAABl6Sby7DVlIf5trTo7ND-Jgd9te3LXIfMCZp5lYbbFh9WS0_o1quAYWAqcIIhSgmrqYcdCwAPqDLLJ4M4SHnVAnaS1WxyVnM9Nj8o2BA_ufSbJCTKM0NHOep2u_14YPZKaRlTH',
            b'gAAAAABl6SbymKbdGlejbWvCks-N8cdojsItj3YLbuJ_8g3NqL0JSco0ji3sW59eEKtK7GgwI75ny12tDWdoT-L6ckXbtnQ5cZo8UJ561HXCdqqc3HD8NXipSfE4q1Aoo5n49nyM5apkG8rqwrhVGZkzGzvkDFtmQcoPDj_ixHkBOeyfCmYA3GM=',
            b'gAAAAABl6SbyMeOCqZ26QuGFde6lW_opoWG7GL3gZ4gtrH9_En5Z0XZDm7f4BPkUOVeR1Fucoi9xOV5G3Itxew477vUB6ccyLibXy3ZNDUbiQrtxewGjUY3msklIVUaEbh0FBxbVORv-ZMShQH0c5YqeixXC9fBy0A==',
            b'gAAAAABl6Sbyq9oISiwyNhvhhvZXEkvBOEXcAWC5hlvrReIpWqKA3adOXi7qjDix-pyt4wKkQ3VKPWvvpULtMq8p1CtJQDZRPMGAWy6dp3Ips9gAVjEsWG9yVaWISmFMno9ef2Ebyl0mzbojphbTjhRfD-sSjf0kgg==',
            b'gAAAAABl6SbyrGMnBfe5mqQ_E3G7V1qsJ4I4CZaKpwe4lsoBusm1Ej8Rl9fYNhJkDr7YQ9HZWbwUhuLO_tBXqdvVeC6NTegJAtwKcF8cQ6a-A6CoMzRm9u_IBcdPLDfU8GawI6yyUcYYnQx6Zxrsd7cRz0CV70ibNA==',
            b'gAAAAABl6Sby2EQKNOwFIy1dHMacKM-TNCgsRB3--UD0FDaCP-9oz7XDFQattQKRKQ24_JTB9NbCKw7HOCWP2yKfYpFduVDSDg7y_6pxn2BFnks8tkhM1m6sl6XeZLEqy0GPGEpINq8_'],
                  "execution" : [b'gAAAAABl6SaqVars33IauytpwB4YMAd7q0rdFIm5Vv_QUOEBfLsmMhmPgH7JmWk_hCcacTCzbQ6aJ7cucm-SObvNZMFcuIrfpOqD_EGx3rzue5m-i0OBeXxTZK8MFY8HHctcOZSCi1NN',
                                 b'gAAAAABl6SaqcyLUWdOHPahJ8fwzkvwomFNJd8xs_YlvU3J-w7HRJD9R29-TRGk7lujdQOL6coEeV0wNqh6JZ-FOgXhSkSrIWQkT8IhDH4czVsf5bFwIaP0=',
                                 b'gAAAAABl6SaqGORl4YEr60pSSI1DweaWgAuXLvpLMARtRIT2Z2c7c9H-6EE6Mu9t16vyb4SWmbYlGXfsu2ptRH0vfzD8GG9T8Shthr9vXYObwMGg2G1Sexw=',
                                 b'gAAAAABl6SaqRRx5JGdflGmLxBdbOGdT1ZGkXAodBAeMT5X4xr0RCu3SwEdPDSFMf3qNGd4r2e1ziUUirhl8JCvjiEn0Kdelm5W_15eOfvgWmY-Q_lz9IAk=',
                                 b'gAAAAABl6Saq-aI3wayGmPUuzmfr7dr_Du3gPeP23n9Q2slwJM_iKH2qosxIIYk30ya-2xxU7rx8oiu8mNTzE3xMXtXf_qHV9EepYByUie2qbrdLDOOVfFs=',
                                 b'gAAAAABl6SaqMxlrFfN5d6FmIZwBy9XaItNRgYSqbUI0u7KQkdgWZtpjgx0O6RqUPZFDOulKwxYLDarpIgNvDuUzbl-IuUS1L2m0MzIHDkb1uyajFhsX5Ik=',
                                 b'gAAAAABl6Saq0UaElDUuWL9dnxmroBJN6Ky3UnzDg3EfOgPSJT_bnqCEy8DANz__igKPDaNxH5eaNaFLEi8ofSdyusFORocj8snvCHhkbeOPCrsrc5sLuKU=',
                                 b'gAAAAABl6SaqY2J3YHEqjH0l_f8Dqf4pzUjMi4mCnzmmpbHnLvvNGoJTgN3w33E75FfXP5YJ7G_8RAdZzLclFt2SLNaNRcEWEoISid8x3n1Xfg9XgYPmLgo=',
                                 b'gAAAAABl6SaqJE89JKNY8KziSzKnFY0ai0a9YniQh2IP6HHDjC_xERTMF3NiwdOYJxfMhw8E0KHNkG-DaCy1NclIL66uZtxW8_oMp7puRwtHla_7-9idm_M=',
                                 b'gAAAAABl6SaqZxkeuqUpq6Szdsb4XrbUWX8x8coS78RyJXS_JxDeHg46RWA9YYAZTFRycmI4Gl70-PilyXHWSi3G2-m_ESd50_ODSM9jw8W_ahkhIAxxJ5Q=',
                                 b'gAAAAABl6Saq7TCH8RD9TKKlpq6sBQg0iDB__snSHZ34yb_4ewfj1o65pExVZ8kgMB9saigqzUz2-OWi_-1hV7scRFoPSTrnXRodPZJjk_stOsU30gj_drY=',
                                 b'gAAAAABl6Saq8ByLoR-O66qHCoPI10YKj5Sm5AI02NPFr7T4-oR1LczBA4u7ZATGAAMX-CS8eh1oC6tfuf2PWJDRSwqW-Mpdie9Z4qFIu-JjE6spZo0Fcvc=',
                                 b'gAAAAABl6SaqqWNpL_piiltaDRXlm0fPkl0ZiPa8kC0hPSrU2N6isj-sMBvYF1ftbZNhPrwUJCTPP_htc5PWCcGXQkKbHb9rFJ1CifoA1YxW78L8qJxKHjo=',
                                 b'gAAAAABl6SaqOeNkg1eQZWblMQ0_d3CZx3efZv1p0JQXNwA-A-AOFeJGmeXme-9wRN5Tsse-VoY5DFQaCMI0bu6bd0twZ9VooOvMwnL6N2CXPWlqeOtWsVQ=',
                                 b'gAAAAABl6Saqtnmh93O8TBTmJqrlWxiaE9DzZ_wb6rXsWMruuNTSSr4FkF7NzFTmgtAToE-cuWS140c_OjysGzAVTTClRaWwufUT8HIoHgkW24iRf7Y03Z8=',
                                 b'gAAAAABl6SarjnjZGASa7GvLA3Hkvmpt1OC-d8FHR18Lb3kLp58Kj_HfR5xhzPa7RQ64FCPIM1lVKsWW003g89EsEJ1T8bNZ5pGXdGkmNyrcL15QrfncD6E=',
                                 b'gAAAAABl6SarysJCNDzZo_G0SOjRhrt2KIA-IwqGJ3s29qyEcqQnCOpOGu5M4IUtcbo2N6FJC2DF3wf69jLCo2qWFKHPWk4yTmTzzIQcILXV4ohrq8TjduY=',
                                 b'gAAAAABl6SarD7mPF1funJ3A2a1OpEB5CKTiTuZwBlJzOKNzaPW_fo9GyHDf6hfXNetZC_aJdTcFcrW5WpHQMPjSOzXf4HdQoFwnvuiU-1vnTPFA9LbKH-M=',
                                 b'gAAAAABl6SarVN211aVEzb7YKh8JX5vK468Omr1joIcYerUCZTlRW75ptJqprSOfecz-Kogngco7pkiIkOZk-Z-dpLU1-5OMSpehP_PPz5F5xV7A-kCrSFg=',
                                 b'gAAAAABl6SarI5GvYySkISCo0ajZrxREw0WhJjgGTZ03RO7vaKSlTbNaTp36dZe2_Mq03TTM1d554ov0FiamLMe-Yydnv-xr8-FLw5cbfb5Ug_IPTUYfI_k=']},
            points = [15,25],
            default=None,
            **kwargs):
      
      
      
      super().__init__(
               title=title,
               question_number=question_number,
               key=key,
               options=options, 
               solutions=solutions, 
               points=points,
               default=default,
               **kwargs
            )

numbers = [5, 4.0]
total = 0

for num in numbers:
   while total < 9:
      total += num + 1.0
   break


class ReadingPythonQuestion_f2024(ReadingPython):
   
   def __init__(self,
            title = "Reading, Commenting, and Interpreting Python Code:",
            question_number = 4,
            key="READING1",
            options={
               # General list of 15 potential comments with only one correct per line
               "comments_options" : [
                  None,
                  "Initializes a list `numbers` with integers and floats.",  
                  "Initializes the variable `total` with a value of 0.",  
                  "A `for` loop that iterates through an iterator `numbers`.",  
                  "`while` loop that continues to iterate until `total` is less than 9.",  
                  "Adds and assigns the variable `total` with the value of `num` plus 1.",  
                  "Statement that ends the `for` loop",
                  "Initializes a dictionary `numbers` with integers and floats.",
                  "Initializes the class `total` with a value of 0.",    
                  "A `for` loop that iterates through an iterator `num`.",
                  "`while` loop that continues to iterate until `total` is less than or equal to 9.", 
                  "Adds the variable `total` with the value of `num` plus 1.",
                  "Statement that ends the `while` loop",
                  "`while` loop that continues to iterate while `total` is less than 9.",
                  "Initializes a list `numbers` with integers and floats.",
               ],
               # Define the number of rows you want ahead of time
               "n_rows" : 12,  # for example, 5 rows'
               "n_required" : 9,  # number of rows required to respond. 
               # Lines of code that require commenting
               "lines_to_comment" : [1, 2, 4, 5, 6, 7],
               # Table headers
               "table_headers" : ['Step', 'Line Number', 'Variable Changed', 'Current Value', 'DataType'],
               # Variables Changed
               "variables_changed" : ["", 'None','numbers', 'num', 'total', 'if', 'else'],
               "current_values" : ["", "None", "[5, 4.0]", "[5.0, 4.0]", "5.0", "6.0", "5", "6", "4.0", "4", "11.0", "11", "12","12.0","0","0.0", "True", "False", "N/A"],
               "datatypes" : ["", "NoneType", "list", "dictionary", "tuple", "set", "string", "float", "integer", "boolean", "N/A"],
               }, 
            solutions = {"comment" : [b'gAAAAABl95p957tnUqYALjiKhMSlvd1M7DNMb7wINcL0rtrAlJ-1YGOn6AjwuADkveX4yk99-F6uE_m_ZKV47rFwzwSzl_x0G6DHFealifYuH8Ui6BT5w14qNLwfErxX1Ipkayp364phSfrXGsQU85I2fkSQVL8I7Q==',
 b'gAAAAABl95p9VM5An7xxKY1q8W8f5OvGyB7Tbc1ZzRkT_kHVMkFR51rKgo-3l7IwEizQPHbbdBVtG48dreSAm5DC80uk8gWBCafDYauZZc6Qah9QIQogTkCvviQZsqnr0SMiiS1fZmnRzmvRoR1koOJ_U-8LVHIZLQ==',
 b'gAAAAABl95p9lU2MCg3buMb3aVQNFRBRLyXNTG-qWGRzg4zpvBaBZ69202msyTWBjtc-lZVGQY6MxorbTRnHUjIIANSc0nqwxZ-kvKkxgTTIwNuye0L7LOs1gEmQSiHtJrhUevRo53vqVlq44iclp28zfBHr6y2rXQ==',
 b'gAAAAABl95p9xdSSC011LTvAg6IKd6k_qfA_lRuI51uOuIYyASXROYhMsCeQNzr1nzmL_N1Xk1Vg4njvul5wZ5D88qI7lbdzTHBUqUgxZPbSi0UQgrwedT9-XIaltCUC-lj6jwcsC-imjHAYjd299YHROAOC-YEmnyndiekx67XL6ZtEKrRBwrA=',
 b'gAAAAABl95p99ejaSdCd6uAz8Rs5xYqfu_krqbWk6ce5NEmSjXOU4sQpA8HbNlhZ06HZiQllzLCBIBoTXcJlfzpkEKLT6mZQWezl-G_gQpRm-nRtMRy7XBvRaZOYNCp800uwNdhhSmHnftuQWa_ZMcz44A0njMP1SakO4lgY6BWII9WC_eOWDD0=',
 b'gAAAAABl95p9dYfDTkFfI7AIHam7s143tCB-Y5-DZkbNsovfopSDp5gUNr-PWGsTMoaaSvMTxgrAMk7dBa1iXUZblj8zJple8wHZY_MUemkW3VwIGBdH3V8v7yahpF0yoV0mWsJc-LSJ'],
                  "execution" : [b'gAAAAABl9zAx5Bf7NfxV_yAnRPA9kOuTvu4FzPaEds6ihhks5ZoRDHhhtQgUILM7M4iVANEmIN3hIzflBuvuhGV9KeCMntk4ROf1MQSVHF49xOLn-CaYuIiMRCVrtvX4fmKf3MUJ20sz',
                                 b'gAAAAABl9zAxD18mpTURC7gdy1luJ8rzBolpvdYAzJL6Pk7FzKh5lZspZvArLI3WI5phYmFmq25bSaTfmGtQHb1k_71FoCMVviYcYi2HMWX2VaHfYH9fNIg=',
                                 b'gAAAAABl9zAxKNqc5-Q_UJiKe5VsMO5CKQiI5h2QAmd25rhFqgvlPUB5LmnclbByYrP322NP7GVcpcQYSFztQNI80K2NBvKPEyGapCPmgUjJ5PS79G_hmLE=',
                                 b'gAAAAABl9zAxyBfLZba_3WkfNwQwSeC1gO07tCzQ3nmR6H89Ghz6maK2aK6X80fWlBxech-CMgcp_pmSIOaSIx24jtm9FagFgDs-MVYY3VrrxPv8v74nBfU=',
                                 b'gAAAAABl9zAx5AH6kHsB4He7-HehRoUinbVRiI72qYBjez6qEK07DhuzJw0PEnXtkAyq_dSgZrm-FUbSYUinJBbmFcWD5oOPxnvd6RdIHBsRN3PzdHtq2dw=',
                                 b'gAAAAABl9zAxdkVl5j-QWtKuHTWkiivDylHK7yyYkJ4D1GMWTxVax1ec4AcbLGMr88fuXNJDfdvhQKMdcLiw1wuqNz80mdNjNZTbxepN46saHcSjewvlFR0=',
                                 b'gAAAAABl9zAxEv0ADL657BQ7GRNu1DQc35GuLRqlX3WT87tot_18LTYErPgccpKqaDkmPDMRhU9vo-_5OyLP8nupmGGor-J9ogOpWwYYHFs48mky0KlapPY=',
                                 b'gAAAAABl9zAxE0XhrCjqhWa9uZ-kH0i3iFG2I2f005pOSWDtvIE8G1F5LZuG5y-DkNhLas-huh17y4sGuTlgukDXX7th469RslTbsxoL5pOHlM1a__WOD0s=',
                                 b'gAAAAABl9zAxeRMGNlFi2QPPnQVinrAOb0jhAIzvEYRbP9maiU6G43GA-47DGy5zwjVan5HpFE-BaYxedfXtcq6R8wVCMHOz4wp69bcPY9LahMLOw_z7yic=',
                                 b'gAAAAABl9zAxRVAZ7kwmxN0hxHeUhRUN0Q-QpdPs0MDMuafNg6IakZBsO_kN9pdKmWe78TWmE0wK2HNScfIyGn7TsNpQBJDOwZRDuGsnqGXf5AIX7BfIKuE=',
                                 b'gAAAAABl9zAxMnr9H8K4yjqDU0lodVyx65cE-L8ZU6yckKFfuQNB_3Hx3sgqbNvDLlNzUYkPBy_MgXTUfvcm_ilGSJOaWMsmxLdgoi_mbO4HzCcapK6edNY=',
                                 b'gAAAAABl9zAxFXiQnLr1PxrT6yjBVUqkK-mQP5ZCiGUsHSZWxafEQYdgRqai_QpADSjxCT88Ob5xu8xsY3ICY4evXm6dh8yplpuInywTQh9DYx4tsB5B4tQ=']},
            points = [20,25],
            default=None,
            **kwargs):
      
      
      
      super().__init__(
               title=title,
               question_number=question_number,
               key=key,
               options=options, 
               solutions=solutions, 
               points=points,
               default=default,
               **kwargs
            )

class ReadingPythonQuestion_f2024_V2(ReadingPython):
   
   def __init__(self,
            title = "Reading, Commenting, and Interpreting Python Code:",
            question_number = 4,
            key="READING1",
            options={
               # General list of 15 potential comments with only one correct per line
               "comments_options" : [
                  None,
                  "Initializes a list of numbers with integers and floats.",  
                  "Initializes the variable sum_ to 0.",  
                  "A while loop based on the condition of 'sum_' being less than 6.",  
                  "Iterates over each item in the 'numbers' list using a for loop.",  
                  "Checks if the current number is evenly divisible by 2.",  
                  "Add and assigns sum_ with 2 times the number, num if even.",
                  "Add and assigns sum_ with 2 times the number, num if odd.",
                  "Add and assigns sum_ with number, num if odd.",    
                  "Adds 2 times the number, num if even.",
                  "Adds 2 times the number, num if odd.", 
                  "Defines a function.",
                  "Imports a module.",
                  "Prints output to the console.",
                  "Catches an exception.",
                  "Returns a value from a function.",
                  "Initializes a dictionary of numbers with integers and floats.",
                  "Initializes a tuple of numbers with integers and floats.",
               ],
               # Define the number of rows you want ahead of time
               "n_rows" : 20,  # for example, 5 rows'
               "n_required" : 13,  # number of rows required to respond. 
               # Lines of code that require commenting
               "lines_to_comment" : [1, 2, 4, 5, 6, 7, 9],
               # Table headers
               "table_headers" : ['Step', 'Line Number', 'Variable Changed', 'Current Value', 'DataType'],
               # Variables Changed
               "variables_changed" : ["", 'None','numbers', 'num', 'sum_', 'if', 'else'],
               "current_values" : ["", "None", "[5, 2.0, 3.0]", "[5, 2, 3]", "3", "2", "2.0", "5", "3.0", "5.0", "2.0", "0", "0.0","9","9.0","12",'12.0',"True", "False"],
               "datatypes" : ["", "NoneType", "list", "dictionary", "tuple", "set", "string", "float", "integer", "boolean"],
               },
            solutions = {"comment" : [b'gAAAAABl6Sby9zpSpHL5RE96n2KQBeLoIhr6j824-nYPGMH0U6wISx1SyIn-A8-EBmA2QYJD3Pzz9qQpBMDMk6ph-tzlrDJYSQpX5Za3i-sT3ARggbhQA2Hq9jffC-m4JYCcbB5QHucTf8tFwzQ_XYx31EZLQ1dG4Q==',
            b'gAAAAABl6Sby7DVlIf5trTo7ND-Jgd9te3LXIfMCZp5lYbbFh9WS0_o1quAYWAqcIIhSgmrqYcdCwAPqDLLJ4M4SHnVAnaS1WxyVnM9Nj8o2BA_ufSbJCTKM0NHOep2u_14YPZKaRlTH',
            b'gAAAAABl6SbymKbdGlejbWvCks-N8cdojsItj3YLbuJ_8g3NqL0JSco0ji3sW59eEKtK7GgwI75ny12tDWdoT-L6ckXbtnQ5cZo8UJ561HXCdqqc3HD8NXipSfE4q1Aoo5n49nyM5apkG8rqwrhVGZkzGzvkDFtmQcoPDj_ixHkBOeyfCmYA3GM=',
            b'gAAAAABl6SbyMeOCqZ26QuGFde6lW_opoWG7GL3gZ4gtrH9_En5Z0XZDm7f4BPkUOVeR1Fucoi9xOV5G3Itxew477vUB6ccyLibXy3ZNDUbiQrtxewGjUY3msklIVUaEbh0FBxbVORv-ZMShQH0c5YqeixXC9fBy0A==',
            b'gAAAAABl6Sbyq9oISiwyNhvhhvZXEkvBOEXcAWC5hlvrReIpWqKA3adOXi7qjDix-pyt4wKkQ3VKPWvvpULtMq8p1CtJQDZRPMGAWy6dp3Ips9gAVjEsWG9yVaWISmFMno9ef2Ebyl0mzbojphbTjhRfD-sSjf0kgg==',
            b'gAAAAABl6SbyrGMnBfe5mqQ_E3G7V1qsJ4I4CZaKpwe4lsoBusm1Ej8Rl9fYNhJkDr7YQ9HZWbwUhuLO_tBXqdvVeC6NTegJAtwKcF8cQ6a-A6CoMzRm9u_IBcdPLDfU8GawI6yyUcYYnQx6Zxrsd7cRz0CV70ibNA==',
            b'gAAAAABl6Sby2EQKNOwFIy1dHMacKFMCM-TNCgsRB3--UD0FDaCP-9oz7XDFQattQKRKQ24_JTB9NbCKw7HOCWP2yKfYpFduVDSDg7y_6pxn2BFnks8tkhM1m6sl6XeZLEqy0GPGEpINq8_'],
                  "execution" : [b'gAAAAABl6SaqVars33IauytpwB4YMAd7q0rdFIm5Vv_QUOEBfLsmMhmPgH7JmWk_hCcacTCzbQ6aJ7cucm-SObvNZMFcuIrfpOqD_EGx3rzue5m-i0OBeXxTZK8MFY8HHctcOZSCi1NN',
                                 b'gAAAAABl6SaqcyLUWdOHPahJ8fwzkvwomFNJd8xs_YlvU3J-w7HRJD9R29-TRGk7lujdQOL6coEeV0wNqh6JZ-FOgXhSkSrIWQkT8IhDH4czVsf5bFwIaP0=',
                                 b'gAAAAABl6SaqGORl4YEr60pSSI1DweaWgAuXLvpLMARtRIT2Z2c7c9H-6EE6Mu9t16vyb4SWmbYlGXfsu2ptRH0vfzD8GG9T8Shthr9vXYObwMGg2G1Sexw=',
                                 b'gAAAAABl6SaqRRx5JGdflGmLxBdbOGdT1ZGkXAodBAeMT5X4xr0RCu3SwEdPDSFMf3qNGd4r2e1ziUUirhl8JCvjiEn0Kdelm5W_15eOfvgWmY-Q_lz9IAk=',
                                 b'gAAAAABl6Saq-aI3wayGmPUuzmfr7dr_Du3gPeP23n9Q2slwJM_iKH2qosxIIYk30ya-2xxU7rx8oiu8mNTzE3xMXtXf_qHV9EepYByUie2qbrdLDOOVfFs=',
                                 b'gAAAAABl6SaqMxlrFfN5d6FmIZwBy9XaItNRgYSqbUI0u7KQkdgWZtpjgx0O6RqUPZFDOulKwxYLDarpIgNvDuUzbl-IuUS1L2m0MzIHDkb1uyajFhsX5Ik=',
                                 b'gAAAAABl6Saq0UaElDUuWL9dnxmroBJN6Ky3UnzDg3EfOgPSJT_bnqCEy8DANz__igKPDaNxH5eaNaFLEi8ofSdyusFORocj8snvCHhkbeOPCrsrc5sLuKU=',
                                 b'gAAAAABl6SaqY2J3YHEqjH0l_f8Dqf4pzUjMi4mCnzmmpbHnLvvNGoJTgN3w33E75FfXP5YJ7G_8RAdZzLclFt2SLNaNRcEWEoISid8x3n1Xfg9XgYPmLgo=',
                                 b'gAAAAABl6SaqJE89JKNY8KziSzKnFY0ai0a9YniQh2IP6HHDjC_xERTMF3NiwdOYJxfMhw8E0KHNkG-DaCy1NclIL66uZtxW8_oMp7puRwtHla_7-9idm_M=',
                                 b'gAAAAABl6SaqZxkeuqUpq6Szdsb4XrbUWX8x8coS78RyJXS_JxDeHg46RWA9YYAZTFRycmI4Gl70-PilyXHWSi3G2-m_ESd50_ODSM9jw8W_ahkhIAxxJ5Q=',
                                 b'gAAAAABl6Saq7TCH8RD9TKKlpq6sBQg0iDB__snSHZ34yb_4ewfj1o65pExVZ8kgMB9saigqzUz2-OWi_-1hV7scRFoPSTrnXRodPZJjk_stOsU30gj_drY=',
                                 b'gAAAAABl6Saq8ByLoR-O66qHCoPI10YKj5Sm5AI02NPFr7T4-oR1LczBA4u7ZATGAAMX-CS8eh1oC6tfuf2PWJDRSwqW-Mpdie9Z4qFIu-JjE6spZo0Fcvc=',
                                 b'gAAAAABl6SaqqWNpL_piiltaDRXlm0fPkl0ZiPa8kC0hPSrU2N6isj-sMBvYF1ftbZNhPrwUJCTPP_htc5PWCcGXQkKbHb9rFJ1CifoA1YxW78L8qJxKHjo=',
                                 b'gAAAAABl6SaqOeNkg1eQZWblMQ0_d3CZx3efZv1p0JQXNwA-A-AOFeJGmeXme-9wRN5Tsse-VoY5DFQaCMI0bu6bd0twZ9VooOvMwnL6N2CXPWlqeOtWsVQ=',
                                 b'gAAAAABl6Saqtnmh93O8TBTmJqrlWxiaE9DzZ_wb6rXsWMruuNTSSr4FkF7NzFTmgtAToE-cuWS140c_OjysGzAVTTClRaWwufUT8HIoHgkW24iRf7Y03Z8=',
                                 b'gAAAAABl6SarjnjZGASa7GvLA3Hkvmpt1OC-d8FHR18Lb3kLp58Kj_HfR5xhzPa7RQ64FCPIM1lVKsWW003g89EsEJ1T8bNZ5pGXdGkmNyrcL15QrfncD6E=',
                                 b'gAAAAABl6SarysJCNDzZo_G0SOjRhrt2KIA-IwqGJ3s29qyEcqQnCOpOGu5M4IUtcbo2N6FJC2DF3wf69jLCo2qWFKHPWk4yTmTzzIQcILXV4ohrq8TjduY=',
                                 b'gAAAAABl6SarD7mPF1funJ3A2a1OpEB5CKTiTuZwBlJzOKNzaPW_fo9GyHDf6hfXNetZC_aJdTcFcrW5WpHQMPjSOzXf4HdQoFwnvuiU-1vnTPFA9LbKH-M=',
                                 b'gAAAAABl6SarVN211aVEzb7YKh8JX5vK468Omr1joIcYerUCZTlRW75ptJqprSOfecz-Kogngco7pkiIkOZk-Z-dpLU1-5OMSpehP_PPz5F5xV7A-kCrSFg=',
                                 b'gAAAAABl6SarI5GvYySkISCo0ajZrxREw0WhJjgGTZ03RO7vaKSlTbNaTp36dZe2_Mq03TTM1d554ov0FiamLMe-Yydnv-xr8-FLw5cbfb5Ug_IPTUYfI_k=']},
            points = [15,25],
            default=None,
            **kwargs):
      
      
      
      super().__init__(
               title=title,
               question_number=question_number,
               key=key,
               options=options, 
               solutions=solutions, 
               points=points,
               default=default,
               **kwargs
            )
      
class TypesQuestion_f2024(SelectQuestion):
   
   def __init__(self,
            title = "Select the option that matches the definition:",
            style=MultipleChoice,
            question_number=1,
            keys=['types1','types2','types3','types4','types5','types6'],
            options = ['None','list', 'function', 'dictionary', 'array', 'variable', 'integer', 'string', 'tuple', 'iterator', 'float', 'object', 'class', 'module', 'package', 'instance'],
         descriptions = [
            "An ordered, mutable collection of items, defined with []",  
            "A file containing Python definitions and statements.",  
            "Collection of elements of the same type, which allows for efficient storage and manipulation of sequences of data",  
            "an immutable and ordered collection of elements in Python, which can contain mixed data types",
            "A sequence of Unicode characters.",
            "A data type that represents real numbers with a decimal point.",
            "a specific object created from a class, containing real values that follow the structure and behavior defined by the class"
         ],
         solutions = [b'gAAAAABl9ekaxrYI4hrSBMRIuf5e37C347faKQCrYzbcJUAyxb7_Cyt19mk7yB-TyYTB2ib9numxL9onKKo0Tpiep3VnVnwVLw==',
                     b'gAAAAABl9ekaM6ft9qYW-HK8iHT-TPW-laZN2GTMKEhD5guz8svXMUj1PZsZXTxupr1z7p_iqjyWAN3dog_kwuNEtR42j3f-vQ==',
                     b'gAAAAABl9ekaGYu-eF9cdBnHWRPt1ek2XWMd4IDYoKBuO4mzF9txxqwI6S9Irigx6XMlBuBCV3UjMnVofc-HGy9Eddck4jum5g==',
                     b'gAAAAABl9ekaIEd4nMQD_3qkBxZzuEBRETk-WJteNSTZpheelgu56Uu5KEyb76qSu9si5omJOWG3vKgloaXLqlgA5dKrHL2CNg==',
                     b'gAAAAABl9eka7dTSfs2Ge31JmG6w71jgLk2fJK2V9TC_09GwVBvPvBlOgOMJi5rapevxWKEGgYZQHm-oBPDMMNvpNiE4IK9zGA==',
                     b'gAAAAABl9ekayHSSYs-6X_YAUPFoKknFuPCfV5fRLtxz7VItgI_0TpHG4D5ZTUjp_u_-WMAp7xaO49oT_Iwr2Dlmc_IuPWcoOw=='],
            default=None, 
            points = 3,
            **kwargs):
      
      super().__init__(
               title=title,
               style=style,
               question_number=question_number,
               keys=keys,
               options=options,
               descriptions=descriptions,
               solutions=solutions,
               default=default,
               points=points,
               **kwargs
            )
      
class MCQQuestion_f2024(SelectQuestion):
   
   def __init__(self,
            title = "Select the option that matches the definition:",
            style=MCQ,
            question_number=2,
            keys=['MC1','MC2','MC3', 'MC4'],
            options = [["List", "Dictionary", "Tuple", "Set"],
                       ["return", "continue", "pass", "break"],
                       ["*", "^", "**", "//"],
                       ['list.add(element)', 'list.append(element)', 'list.insert(element)', 'list.push(element)']],
         descriptions = [
            "Which of the following stores key:value pairs",
            "The following condition returns to the next iteration of the loop",
            "Which operator is used for an exponentiation in Python",
            "which method is used to add an element to the end of a list in Python",
         ],
         solutions = [b'gAAAAABl9evGYPzYfU5el0Z8WYDFRXFwYGFiOsD6Bi7IoAwQV8we4FcvfjSHBCTHtoesgJ1fX9aiFShklZo41mbwiWP63t3vRQ==',
                     b'gAAAAABl9evGrYA4DnXuZjotsn3clBHXmRUNn47uZb7Ca-RD7IuaFNYr_gycCcOzJwJdAdH31o7pNaVHamF8tvTtN_kVAzGMPA==',
                     b'gAAAAABl9evG5Pau4v3nIeX9FntVOJ1NuL_yXqXhR8hRW1C6kH4krWEWT0F_PW6SvoC6mDl5vFTfnlvTnEpKmXnr_jH3Yw0mYg==',
                     b'gAAAAABl9evGXsMp01zlBJZHKfyamq7yo2s4NK9sU4A5VH3Tk4BT0LVsMQoMVmWglOLgn0fh-aYV8a50fm26oleKUb550niBcYI6d6Wrd5yB8RzVhpN_41A='],
            default = None, 
            points = 2,
            **kwargs):
      
      
      
      super().__init__(
               title=title,
               style=style,
               question_number=question_number,
               keys=keys,
               options=options,
               descriptions=descriptions,
               solutions=solutions,
               default=default,
               points=points,
               **kwargs
            )
      
      
class SelectMany_f2024(MultiSelectQuestionWidget):
   
   def __init__(self,
            title = "Select all statements which are TRUE:",
            style=MultiSelect,
            question_number=3,
            keys=['MS1','MS2','MS3',"MS4", "MS5"],
            options = [["`if` Statements.",
                        "`for` Loops.",
                        "`while` Loops.",
                        "`end` Statements."],
                       ["dictionaries",
                        "tuple",
                        "float",
                        "class"],
                       ["A class can inherit attributes and methods from another class.",
                        "The `self` keyword is used to access variables that belong to a class.",
                        "`__init__` runs on instantiation of a class.",
                        "Variables assigned in a class are always globally accessable."],
                       ["Keys in dictionaries are mutable.",
                        "It is possible to store a list of dictionaries in Python.",
                        "You can create multiple instances of a class with different values.",
                        "If `a` is a list, and you assign `b=a`, if you change the value of `b`, the value of `a` will also change."],
                       ['in `print(i)`, `i` must be a string.',
                        "`2day` is not a valid variable name.",
                        "`i` is not defined when evaluating the while loop.",
                        "`i < 5` is not valid syntax to compare a variable `i` to an integer `5`, if `i` is a float."],
                       ],
         descriptions = [
            "Which of the following control structures are used in Python? (Select all that apply)",
            "Which of the following are built-in data structures in Python? (Select all that apply)",
            "Concerning object-oriented programming in Python, which of the following statements are true? (Select all that apply)",
            "Select all of the TRUE statements",
            """
            Select all of the syntax errors in the following code
            <pre>
            <code class="language-python">
            2day = 'Tuesday'
            while i < 5:
               print(i)
               i += 1.0
            </code>
            </div>
            """,
         ],
         solutions =[b'gAAAAABl9fnXWL1wg3pRIycFoFNgWBwb8c3vorWXqE2AAqZRZLUgm-URMdthw61DeSqG9vJAtppZ4RmtGWwrSLytQ4pPI--Hn5FchcbC4PSHNtpJ5sBa3fA=',
                     b'gAAAAABl9fnXyrcRwDTks44mFhG0cLaRYFPR5WNDz7_C0WXG_jqJXHRo_q84cfBUWpfUeVRlwdvgG-2kedSJOz28kXvU4ifKw7GfG0WEZBBXzatDcE2QWl4=',
                     b'gAAAAABl9fnXwbT19VfSMMCE3xBKnEt9OObg59LdHb0DSqDOC6NQMCHySNDaNBu0D-5r362ps2Lhiereyuit_SZnU6aEB3Itdqqvo7rcRqxVHNQFw4KEjls=',
                     b'gAAAAABl9fnX6R1bDkH2P-tjK_k6FsaQ4isRrqNhD1V93Gu_ZhBVFAyYpt19Z0P4P1zL--cHXGRTrGOTCI84oR1mGdO8vjq_ikl3DT9nTS27g3CtvucHnsg=',
                     b'gAAAAABl9fnXT8glMmOmQA3K0jnm1qYNfyiScAGIzaQAU_LBREvW7yZrt0HdKG_kOcmdP9p2iP4jTBekcJoV6Q0sBkqCUKJgmOHenRlFsGFENRpsLSSLxQo='],
            default = None, 
            points = 1,
            **kwargs):
      
      
      
      super().__init__(
               title=title,
               style=style,
               question_number=question_number,
               keys=keys,
               options=options,
               descriptions=descriptions,
               solutions=solutions,
               default=default,
               points=points,
               **kwargs
            )