# Chatbots scripts

You may use attached script to learn your own bot in Dialogflow.
Also here are two scripts which allows you to start and run chatbots for Telegram and Vk.

## How to install

* create an account on https://id.heroku.com and create you app APP_NAME
* create an account on https://github.com
* add this code to repository and commit & push it
* go to Settings => Buildpacks and choose python for your project
* create variables in Settings => Config Vars: "TG_API_KEY", "VK_COM", "DIALOGFLOW_PROJECT", "MY_CHAT_ID", "
  GOOGLE_APPLICATION_CREDENTIALS"
* go to Deploy tab and add your github repo to heroku account
* connect github to heroku and press "Deploy Brunch"
* then go to Resources section and run your Free Dyno via Edit & switch slider to ON state

## How to run local script

* brew update
  $ brew install pyenv
* brew update && brew upgrade pyenv
* echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
* echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
* echo 'export PATH="$PYENV_ROOT/shims:$PATH"' >> ~/.zshrc
* echo 'export TG_TOKEN=INSERT_YOUR_VALUE' >> ~/.zshrc
* echo 'export TG_CHAT_ID=INSERT_YOUR_VALUE' >> ~/.zshrc
* echo 'export DEVMAN_KEY=INSERT_YOUR_VALUE' >> ~/.zshrc
* source ~/.zshrc
* pyenv intall 3.9.11
* pyenv rehash
* mkdir ~/projects/devman_lessons
* cd ~/projects/devman_lessons
* pyenv local 3.9.11
* pip3 install pipenv
* pipenv shell $(which python3)
* git clone https://github.com/babrounik/devman_chatbots_lesson_3.git
* pipenv install -r requirements.txt
* python3 main_tg.py
*
    * python3 main_vk.py

## Example how TG bot works

![script started](https://github.com/babrounik/devman_chatbots_lesson_3/blob/master/img/tg_bot_example.gif?raw=true)

## Example how TG bot works

![script started](https://github.com/babrounik/devman_chatbots_lesson_3/blob/master/img/vk_bot_example.gif?raw=true)
