from crewai.tools import BaseTool
from backend.bots.login_bot import login_signup  # Adjust path if needed

def get_signin_signup_tool():
    class SigninSignupTool(BaseTool):
        name: str = "SigninSignupTool"
        description: str = (
            "Handles user sign-in or sign-up by taking email and password."
        )

        def _run(self, email: str, password: str):
            print("🔧 Initializing SignIn/SignUp Tool...")
            print("Email received in tool:", email)
            print("Password received in tool:", password)
            result = login_signup(email, password)
            print("🟢 Tool Result:", result)
            return result

    return SigninSignupTool()
