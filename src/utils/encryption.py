from cryptography.fernet import Fernet
import dotenv
import os

dotenv.load_dotenv()
cipher = Fernet(os.environ["ENCRYPTION_KEY"])
