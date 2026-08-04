"""
Webdisplay Main Program File

Part of WebDisplay
Entrypoint

License: MIT license

Author: C2311231

Notes:
"""

import src.onboarding as onboarding

onboarding_handler = onboarding.OnboardingHandler("TestServer", "Arch", [], ["http://localhost:8080"])

onboarding_handler.start_onboarding()

while True:
    onboarding_handler.update()

