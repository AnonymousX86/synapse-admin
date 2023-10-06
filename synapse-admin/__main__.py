# -*- coding: utf-8 -*-
from re import match

from .config import ACCESS_TOKEN, REGISTRATION_SHARED_KEY
from .register import register_user
from .token import generate_token, get_tokens
from .utils import check_username

def main() -> None:
    if not ACCESS_TOKEN:
        print('Please set ACCESS_TOKEN environment variable!')
        return

    if not REGISTRATION_SHARED_KEY:
        print('Please set REGISTRATION_SHARED_KEY environment variable!')
        return

    print("""
   _____
  / ____|
 | (___  _   _ _ __   __ _ _ __  ___  ___
  \___ \| | | | '_ \ / _` | '_ \/ __|/ _ \\
  ____) | |_| | | | | (_| | |_) \__ \  __/
 |_____/ \__, |_| |_|\__,_| .__/|___/\___|
          __/ |           | |
         |___/_           |_|
     /\      | |         (_)
    /  \   __| |_ __ ___  _ _ __
   / /\ \ / _` | '_ ` _ \| | '_ \\
  / ____ \ (_| | | | | | | | | | |
 /_/    \_\__,_|_| |_| |_|_|_| |_|

""")
    print('Welcome to Synapse Admin by AnonymousX86!')
    try:
        while True:
            print('+----------------------+')
            print('| 1. Register new user |')
            print('| 2. Generate token    |')
            print('| 3. Show tokens       |')
            print('| 0. Exit              |')
            print('+----------------------+')
            choice = input('Choice: ')
            print('---')
            if choice == '0':
                break
            elif choice == '1':
                while True:
                    username = input('Provide user\'s username: ')
                    if not check_username(username):
                        print('Username should contains only lowercase letters and underscores')
                        continue
                    if len(username) < 3:
                        print('Ussername should be at least 3 characters long')
                        continue
                    break
                while True:
                    display_name = input('Provide user\'s display name: ')
                    if len(display_name) < 3:
                        print('Ussername should be at least 3 characters long')
                        continue
                    break
                result = register_user(username, display_name)
                if not result:
                    print('User creation failed!')
                    continue
                print('User created sccessfully!')
                print('Access token: {0.access_token}\n'
                      'User ID: {0.user_id}\n'
                      'Home server: {0.home_server}\n'
                      'Device ID: {0.device_id}'.format(result))
            elif choice == '2':
                while True:
                    valid_for = input('For hamy many seconds should be token valid? (default 120): ')
                    if not match('^[0-9]*$', valid_for):
                        print('It\'s not a number!')
                        continue
                    break
                print('Generaing registration token...')
                token = generate_token()
                if not token:
                    print('Generating failed')
                    continue
                print('Token generated!')
                print(token)
            elif choice == '3':
                tokens = get_tokens()
                if not tokens:
                    print('Gettings tokens failed')
                elif len(tokens) == 0:
                    print('No tokens to show')
                else:
                    print('---\n'.join(list(map(lambda t: str(t), tokens))))
            else:
                print('This fucntion is under construction')
            print('---')
            input('Press ENTER to continue...')
    except KeyboardInterrupt:
        print('')
    finally:
        print('Bye!')

if __name__ == '__main__':
    main()
