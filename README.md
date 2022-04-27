# Access Point + Web Server Automation

When used on a raspberry pi, this tool automates most of the config and setup for turning your pi into an access point that also hosts a [Flask](https://flask.palletsprojects.com/en/2.1.x/) web server. It uses [pi-ap](https://github.com/f1linux/pi-ap) for the access point setup and configures the web server itself.

## Usage:

1. Connect your Pi to the internet via **Ethernet** cable (Pi-AP requires this and will fail if not connected this way).

2. Update your raspberry pi.

   ```shell
    $ sudo apt-get update
    $ sudo apt-get upgrade
    $ sudo reboot
   ```

   While not strictly required, this is always a good step to take before doing anything on a Pi.

3. Install `git` and `python3-pip`.

   ```shell
   $ sudo apt-get install git
   $ sudo apt-get install python3-pip
   ```

4. Clone this repository.

   ```shell
   $ git clone https://github.com/jarenglenn/hosting-script.git
   $ cd ./hosting-script
   ```

5. Change the default config values located in `./config.yaml`.

   Config values are explained in the config file.

   > **_NOTE_**: Pi-AP offers many different configuration values for the access point and while most can likely be left as default, they can optionally be configured simply by adding them to this tool's `config.yaml` file under `access_point`. For example, to change the value of `USEREXECUTINGSCRIPT='pi'`:
   >
   > ```yaml
   > access_point:
   >  ssidname: RPI-AP1 # SSID of the new wifi network
   >  apwpa2passwd: cH4nG3M3 # Wifi network password
   >  ...
   >  userexecutingscript: user
   > ```

6. Set up the virtualenv using [Poetry](https://python-poetry.org/) and install Python dependencies:

   > **_NOTE_**: You'll have to restart the shell or reconnect via ssh (depending on how you're running commands on the Pi) after installation to add `poetry` to your 'PATH'. Make sure you `cd` back into the `hosting-script` directory.

   ```shell
   $ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
   $ poetry shell
   $ poetry install
   ```

7. Run the script
   ```shell
   $ poetry run hosting_script
   ```
