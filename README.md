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

3. Install `git`, `python3-pip`, `python3-venv`, and `libyaml-dev`.

   ```shell
   $ sudo apt-get install git python3-pip python3-venv libyaml-dev
   ```

4. Clone this repository.

   ```shell
   $ git clone https://github.com/jarenglenn/hosting-script.git
   $ cd hosting-script
   ```

5. Set up the virtualenv using [Poetry](https://python-poetry.org/) and install Python dependencies:

   ```shell
   $ curl -sSL https://install.python-poetry.org | python3 -
   $ export PATH="/home/pi/.local/bin:$PATH"
   $ poetry shell
   $ poetry install
   ```

   > **_NOTE_**:
   >
   > - You'll want to add `export PATH="/home/pi/.local/bin:$PATH"` to `/home/pi/.bashrc` if you want to run Poetry in the future.
   > - `poetry shell` is a very buggy command so if you run into problems you may need to activate the virtualenv using `source $(poetry env info --path)/bin/activate` instead.

6. Change the default config values located in `./config.yaml`.

   Config values are explained in the config file.

   > **_NOTE_**: Pi-AP offers many different configuration values for the access point and while most can likely be left as default, they can optionally be configured  by adding them to this tool's `config.yaml` file under `access_point`. For example, to change the value of `USEREXECUTINGSCRIPT='pi'`:
   >
   > ```yaml
   > access_point:
   >  ssidname: RPI-AP1 # SSID of the new wifi network
   >  apwpa2passwd: cH4nG3M3 # Wifi network password
   >  ...
   >  userexecutingscript: user
   > ```

7. Run the script
   ```shell
   $ poetry run hosting_script
   ```
   
8. You should now be able to connect to the Pi using the access point information you provided in `config.yaml` and then up the webpage using the value of`ipv4ipwlan0`(without the subnet modifier). 
