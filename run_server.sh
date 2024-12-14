#!/bin/bash
export HOME=/home/seo
# Set PYENV_ROOT to the installation directory of pyenv
export PYENV_ROOT="$HOME/.pyenv"

# Check if the pyenv bin directory exists and add it to the PATH
if [[ -d "$PYENV_ROOT/bin" ]]; then
  export PATH="$PYENV_ROOT/bin:$PATH"
fi

# Initialize pyenv
eval "$(pyenv init -)"

cd $HOME/projects/raspitemperaturemonitor
poetry run streamlit run app.py

