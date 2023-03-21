"""
	____          ____                __               __
   / __ \\ __  __ / __ \\ _____ ____   / /_ ___   _____ / /_
  / /_/ // / / // /_/ // ___// __ \\ / __// _ \\ / ___// __/
 / ____// /_/ // ____// /   / /_/ // /_ /  __// /__ / /_
/_/     \\__, //_/    /_/    \\____/ \\__/ \\___/ \\___/ \\__/
	   /____/

Made With ❤️ By Ghoul & Marci
"""

from pyprotector.keyauth import Keyauth
from pyprotector.keyauth.utils import getchecksum

auth = Keyauth(name="", ownerid="", secret="", version="", file_hash=getchecksum())

app = auth.initialize()
print(
    app
)  # "Keyauth App ({self.version}) with {self.users} users, {self.keys} keys and {self.onlineUsers} online users"

license = auth.license("LICENSE")
print(license.current_subscription)
print(license.last_login)
print(license.expiry)

### All Other Functions are documented.
