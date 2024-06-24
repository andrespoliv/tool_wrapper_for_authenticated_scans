from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from commands import BASE_NUCLEI_COMMAND, BASE_KATANA_COMMAND, BASE_SHORTSCAN_COMMAND
import chromedriver_autoinstaller, argparse, subprocess, os

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', help='Target website username.')
parser.add_argument('-p', "--password", help='Target website password.')
parser.add_argument('-t', '--tool', help='Tool to use, options available: katana, nuclei and shortscan.')
parser.add_argument('-a', '--arguments', help='Tool parameters, read the corresponding documentation for further information. Example of usage: "-a \"-v -o sample_001.txt\""')
parser.add_argument('-au', '--authurl', help='URL to authenticate against, you can only choose 1 URL, no files allowed. NOTE: Before scanning please check CSS selectors and adjust run function accordingly.')
parser.add_argument('-su', '--scanurl', help='URL to scan, you can enter TXT files as well for Nuclei and Katana. By default it will scan authurl. Notice that the scans will only make use of cookies, if more headers are needed please adjust run function accordingly.')
args = parser.parse_args()

def nuclei_cookie_processor(raw_data):
    result = ""
    try:
        for index in range(0, len(raw_data)):
            if index == 0:
                result = '-H "Cookie:'

            result =  result + raw_data[index]["name"] + "=" + raw_data[index]["value"] + ";"
        
        result = result + '"'

    except Exception as e:
        raise Exception(f"Cookie processor failed - {e}")
    return result

def shortscan_cookie_processor(raw_data):
    result = ""
    try:
        for index in range(0, len(raw_data)):
            if index == 0:
                result = '--header "Cookie:'

            result =  result + raw_data[index]["name"] + "=" + raw_data[index]["value"] + ";"
        
        result = result + '"'

    except Exception as e:
        raise Exception(f"Cookie processor failed - {e}")
    return result

def command_exec(command):
    result = ""
    try:
        env = os.environ
        process = subprocess.Popen(command, env=env, shell=True, stdout=subprocess.PIPE)
        result = process.communicate()[0].decode("utf-8")
    except Exception as e:
        print(f"Command execution failed: {e}")
    return result


def initialize_driver_options():
    result = Options()
    try:
        result.add_argument("User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/123.0.2420.97")
    except Exception as e:
        raise Exception(f"Driver options initialization failed: {e}")
    return result

def run(username, password, url):
    result = []
    try:
        print("\n[+] Authenticating...")
        chromedriver_autoinstaller.install()
        driver = webdriver.Chrome(options=initialize_driver_options())
        driver.get(url)
        
        # Login process
        username_input = driver.find_element(By.ID, "txtUser")
        username_input.send_keys(username)
        password_input = driver.find_element(By.ID, "txtPassword")
        password_input.send_keys(password)

        submit_button = driver.find_element(By.ID, "cmdSelect")
        submit_button.click()

        result = driver.get_cookies()

        driver.quit()
        print("\n[+] Authentication finished.")
    except Exception as e:
        raise Exception(f"Running failed - {e}")
    return result

def scan_url_handler(scan_url, default_url, tool):
    result = ""
    try:
        if tool == "shortscan":
            result = scan_url if scan_url else default_url
        else:
            if not scan_url:
                result = default_url
            else:
                if ".txt" in scan_url:
                    result = f"-l {scan_url}"
                else:
                    result = f"-u {scan_url}"
    except Exception as e:
        print(f"[!] Scan URL handler failed - {e}")
    return result

def main():
    try:
        print("\n[+] Tool wrapper: starting...")

        username = args.username
        password = args.password
        tool = args.tool
        authurl = args.authurl
        command = ""

        if username and password and tool and authurl:
            raw_cookies = run(username, password, authurl)
            scanurl = scan_url_handler(args.scanurl, authurl, tool)
            arguments = args.arguments if args.arguments else ""
            
            if tool == "nuclei":
                cookies = nuclei_cookie_processor(raw_cookies)
                command = BASE_NUCLEI_COMMAND + " " + scanurl + " " + arguments + " " + cookies 
            elif tool == "katana":
                cookies = nuclei_cookie_processor(raw_cookies)
                command = BASE_KATANA_COMMAND + " " + scanurl + " " + arguments + " " + cookies 
            elif tool == "shortscan":
                cookies = shortscan_cookie_processor(raw_cookies)
                command = BASE_SHORTSCAN_COMMAND + " " + scanurl + " " + arguments + " " + cookies 
            
            print("\n[+] Executing the following command: ", command)
            command_exec(command)

        print("\n[+] Tool wrapper: done")
    except Exception as e:
        print(f"\n[-] Tool wrapper failed: {e}")

if __name__ == "__main__":
    main()