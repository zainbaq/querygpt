# for mac install mssql driver
# /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
# brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
# brew update
# HOMEBREW_ACCEPT_EULA=Y brew install msodbcsql18 mssql-tools18

# sudo ln -s /usr/local/etc/odbcinst.ini /etc/odbcinst.ini
# sudo ln -s /usr/local/etc/odbc.ini /etc/odbc.ini

# Build virtual environment to run the application
python -m venv querygpt
source querygpt/bin/activate
pip install -r requirements.txt