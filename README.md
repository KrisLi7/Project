
# COMP3900 Project
# capstone-project-3900-f12a-plznobug


[![pytest](https://github.com/unsw-cse-comp3900-9900-22T2/capstone-project-3900-f12a-plznobug/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/unsw-cse-comp3900-9900-22T2/capstone-project-3900-f12a-plznobug/actions/workflows/python-app.yml)

<div class="mume markdown-preview  ">
<ul>
<li><a href="#8-user-documentationmanual">User documentation/manual</a>
<ul>
<li><a href="#setup-backend">Setup Backend</a>
<ul>
<li><a href="#windows">Windows</a></li>
<li><a href="#linux">Linux</a></li>
</ul>
</li>
<li><a href="#setup-frontend">Setup Frontend</a>
<ul>
<li><a href="#windows-1">Windows</a></li>
<li><a href="#linux-1">Linux</a></li>
</ul>
</li>
<li><a href="#available-scripts">Available Scripts</a></li>
</ul>
</li>
</ul>

## User documentation/manual


Firstly, before cloning this repository via Git. setup the SSH key is needed
And the instructions to do this can be accessed via: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account


And then, you can clone this repository as following command

```shell
# ~/whatever
git clone git@github.com:unsw-cse-comp3900-9900-22T2/capstone-project-3900-f12a-plznobug.git
# rename this floder
mv capstone-project-3900-f12a-plznobug movie_finder
cd movie_finder
```

### Setup Backend

The backend is mainly developed with `Python3 + SQLite`,
so a `Python3` environment is required.

##### Windows

Installing `Python3`, There are many methods to install Python3,
here are some recommend, as follows

From `Python` official website
[https://www.python.org/downloads/](https://www.python.org/downloads/)

From `Anaconda` official website
[https://www.anaconda.com/](https://www.anaconda.com/)

After the installation is completed
according to the steps on the official website
and `python3 --version` prints out the installed version,
the installation is successful

Next, use `virtualenv` to enable the virtual environment,
Run the following command

```shell
# ~/movie_finder
virtualenv --version
```

If no version information is printed,
`virtualenv` is not yet installed,
please install `virtualenv` with the following command

```shell
# ~/movie_finder
pip3 install virtualenv
```

Or refer to https://virtualenv.pypa.io/en/latest/installation.html

When `virtualenv` is ready.
Create a python virtual environment of the same version as virtualenv

```shell
# ~/movie_finder
virtualenv venv
```

Next, this project need to enable this virtual environment.
Please running the following command

```powershell
# ~/movie_finder
.\venv\Scripts\activate.ps1
```

When the command line is preceded by the word `(venv)`,
the virtual environment is successfully enabled.

Now you need to install the required packages in this virtual environment

```shell
# ~/movie_finder
pip3 install -r requirements.txt
```

Once everything is installed and ready to go,
you can run the following command to turn on the default backend services

```shell
# ~/movie_finder
cd backend
python3 server.py
```

##### Linux

`Python3` is usually installed on Linux machines,
if not, try the following command

```
sudo apt update
sudo apt install python3
```

When `python3 --version` prints out the installed version,
the installation is successful

Next, use `virtualenv` to enable the virtual environment,
Run the following command

```shell
# ~/movie_finder
virtualenv --version
```

If no version information is printed,
`virtualenv` is not yet installed,
please install `virtualenv` with the following command

```shell
# ~/movie_finder
pip3 install virtualenv
```

Or refer to https://virtualenv.pypa.io/en/latest/installation.html

When `virtualenv` is ready.
Create a python virtual environment of the same version as virtualenv

```shell
# ~/movie_finder
virtualenv venv
```

Next, this project need to enable this virtual environment.
Please running the following command

```shell
# ~/movie_finder
source venv/bin/activate
```

When the command line is preceded by the word `(venv)`,
the virtual environment is successfully enabled.

Now you need to install the required packages in this virtual environment

```shell
# (venv) ~/movie_finder
pip3 install -r requirements.txt
```

Once everything is installed and ready to go,
you can run the following command to turn on the default backend services


```shell
# (venv) ~/movie_finder
cd backend
python3 server.py
```

### Setup Frontend

The frontend of this project requires `Node.js` to start,

##### Windows

`NodeJS` [Download Address](https://nodejs.org/en/download/)

Of course, it is recommended to use `NVM`
.From `Windows development environment` document

https://docs.microsoft.com/en-us/windows/dev-environment/javascript/nodejs-on-windows
<br/>
<br/>
<br/>
After run `nvm current` show `v16.16.0` or higher version,
which means your node environment is ready.
and considering the following command.

```shell
# ~/movie_finder
npm version
```

When it runs successfully, `NodeJS` has been installed successfully.
Here we choose the most recent `LTS` version, `16.16.0`.

Next, we need `yarn` as the package manager.
Run the following command to install `yarn` globally


```shell
# ~/movie_finder
npm install -g yarn
```

Or refer to https://yarnpkg.com/getting-started/install


When the package manager is ready,
run the following command to install the required frontend environment

```shell
# ~/movie_finder
cd frontend && yarn
```

When prompted with `success`, the environment is ready,
now run the following command to start the frontend

```shell
# ~/movie_finder/frontend
yarn dev
```


##### Linux

In `Linux` environments, it is better to consider `NVM` or other `Node Version Manager`. Especially if you don't have installation rights on something like `UNSW CSE`.

The install description based on NVM is as follows, Please follow the https://github.com/nvm-sh/nvm to install nvm if you need

For convenience, we keep an executable script in our repository. Running it as follows should help you install faster


```shell
# ~/movie_finder
chmod +x ./install_nvm.sh && ./install_nvm.sh
```

After run `nvm current` show `v16.16.0` or higher version,
which means your node environment is ready.
and considering the following command.

```shell
# ~/movie_finder
npm version
```

When it runs successfully, `NodeJS` has been installed successfully.
Here we choose the most recent `LTS` version, `16.16.0`.

Next, we need `yarn` as the package manager.
Run the following command to install `yarn` globally

```shell
# ~/movie_finder
npm install -g yarn
```

Or refer to https://yarnpkg.com/getting-started/install


When the package manager is ready,
run the following command to install the required frontend environment

```shell
# ~/movie_finder
cd frontend && yarn
```

When prompted with `success`, the environment is ready,
now run the following command to start the frontend

```shell
# ~/movie_finder/frontend
yarn dev
```

### Available Scripts


```shell
# ~/movie_finder/frontend
yarn dev
```

Runs the frontend app in the development mode.
Open http://localhost:3000 to view it in the browser.

```shell
# ~/movie_finder/frontend
yarn preview
```

This will boot up local static web server that serves the files from dist at http://localhost:4173

```shell
# ~/movie_finder/frontend
yarn build
```

Builds the fronted app for production to the build folder.
It correctly bundles `Vue3` in production mode
and optimizes the build for the best performance.



