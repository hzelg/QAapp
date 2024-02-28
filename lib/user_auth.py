import pickle
from pathlib import Path

import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

# with open('../config.yaml') as file:
#     config = yaml.load(file, Loader=SafeLoader)

# authenticator = Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days'],
#     config['preauthorized']
# )

# name, authentication_status, username = authenticator.login('Login', 'main')