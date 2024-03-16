from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import logging
import os
import subprocess
import time
import requests

"""
MK-AI is a Python package that allows you to classify stars using the MK system and machine learning.
Created by Jaymin Ding, 2024.
"""

class MKAI:
    """
    MKAI is the main class of the MK-AI package.
    """
    def __init__(self, headless: bool=True, verbose: bool=False, timeout: float=30) -> None:
        """
        Construct a new 'MKAI' object.
        :param headless: Whether or not to use a headless Chrome webdriver (whether or not Chrome will show up on your screen when you run the module).
        :param verbose: Whether or not to print out information about the module's progress.
        :param timeout: The maximum amount of time (in seconds) to wait for the classification to be retrieved.
        :return: returns nothing
        """
        if not isinstance(headless, bool):
            raise TypeError("Parameter \"headless\" must be a boolean.")
        if not isinstance(verbose, bool):
            raise TypeError("Parameter \"verbose\" must be a boolean.")
        if not (isinstance(timeout, int) or isinstance(timeout, float)):
            raise TypeError("Parameter \"timeout\" must be an integer or float.")

        try:
            import chromedriver_autoinstaller
        except Exception:
            print("Chromedriver Autoinstaller not found. Attempting to install...")
            command = 'pip install chromedriver-autoinstaller'

            # Run the command
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Print the output and error messages
            print(result.stdout)
            print("Errors:", result.stderr)

            # Print the return code
            print("Return code:", result.returncode)
            import chromedriver_autoinstaller

        self.verbose = verbose
        chromedriver_autoinstaller.logging.disable()
        # chromedriver_autoinstaller.install()

        if self.verbose:
            print("Using Chrome webdriver v" + chromedriver_autoinstaller.get_chrome_version())
        else:
            logging.info("Using Chrome webdriver v" + chromedriver_autoinstaller.get_chrome_version())
        options = Options()
        options.add_argument("--no-sandbox")

        if headless:
            options.add_argument("--headless")
            if self.verbose:
                print("Using headless Chrome webdriver (Chrome will not show up on screen).")
            else:
                logging.info("Using headless Chrome webdriver (Chrome will not show up on screen).")
        else:
            if self.verbose:
                print("Using Chrome webdriver (Chrome will show up on screen).")
            else:
                logging.info("Using Chrome webdriver (Chrome will show up on screen).")
        
        self.driver = webdriver.Chrome(options=options)
        self.timer = 0
        self.initial_time = 0
        self.timeout = timeout
    

    def get_spectral_class(self, image_path: str, url: bool=False) -> tuple:
        """
        Makes a request call to the MK-AI website and returns the classification and confidence of the star.
        :param image_path: The path to the image of the star.
        :param url: Whether or not the image_path is a URL.
        :return: A tuple containing the classification and confidence of the star.
        """
        if not isinstance(image_path, str):
            raise TypeError("Parameter \"image_path\" must be a string.")
        if not isinstance(url, bool):
            raise TypeError("Parameter \"url\" must be a boolean.")
        if not os.path.isfile(image_path) and not url:
            raise FileNotFoundError(f"Image does not exist at path {image_path}. Please check your image path again.")
        
        self.initial_time = time.perf_counter()
        self.driver.get("https://starclassification.pages.dev/")
        if url:
            if self.verbose:
                print("Downloading image...")
            picture_req = requests.get(image_path)
            if self.verbose:
                print(f"Image downloaded with status {picture_req.status_code}.")
            if picture_req.status_code == 200:
                image_path = os.path.join(os.getcwd(), "image.jpg")
                with open(image_path, 'wb') as f:
                    f.write(picture_req.content)
        self.driver.find_element(By.ID, "imageUpload").send_keys(image_path)
        if url:
            os.remove(image_path)
            if self.verbose:
                print("Deleted image.")
        i = 0
        
        while True:
            try:
                result = self.driver.find_element(By.ID, "result").text
                classification = result.split("\n")[0].split(": ")[1].strip()
                confidence = float(str(float(result.split("\n")[1].split(": ")[1].replace("%", "")) / 100)[:6])
                # self.driver.quit()
                if self.verbose:
                    print(f"Successfully retrieved classification in {self.timer} seconds.")
                return classification, confidence
            except NoSuchElementException:
                if self.timer > self.timeout:
                    self.driver.quit()
                    raise TimeoutError("Request timed out. Please try again or increase the request time limit.")
                if i == 0 and self.verbose:
                    print("Awaiting classification...")
            
            i += 1
            self.timer = time.perf_counter() - self.initial_time
    
    def get_luminosity_class(self, image_path: str, url: bool=False) -> tuple:
        """
        Makes a request call to the MK-AI website and returns the classification and confidence of the star.
        :param image_path: The path to the image of the star.
        :param url: Whether or not the image_path is a URL.
        :return: A tuple containing the classification and confidence of the star.
        """
        if not isinstance(image_path, str):
            raise TypeError("Parameter \"image_path\" must be a string.")
        if not isinstance(url, bool):
            raise TypeError("Parameter \"url\" must be a boolean.")
        if not os.path.isfile(image_path) and not url:
            raise FileNotFoundError(f"Image does not exist at path {image_path}. Please check your image path again.")
        
        self.initial_time = time.perf_counter()
        self.driver.get("https://starclassification.pages.dev/")
        if url:
            if self.verbose:
                print("Downloading image...")
            picture_req = requests.get(image_path)
            if self.verbose:
                print(f"Image downloaded with status {picture_req.status_code}.")
            if picture_req.status_code == 200:
                image_path = os.path.join(os.getcwd(), "image.jpg")
                with open(image_path, 'wb') as f:
                    f.write(picture_req.content)
        self.driver.find_element(By.ID, "imageUpload").send_keys(image_path)
        if url:
            os.remove(image_path)
            if self.verbose:
                print("Deleted image.")
        i = 0
        
        while True:
            try:
                result = self.driver.find_element(By.ID, "result2").text
                classification = result.split("\n")[0].split(": ")[1].strip()
                confidence = float(str(float(result.split("\n")[2].split(": ")[1].replace("%", "")) / 100)[:6])
                # self.driver.quit()
                if self.verbose:
                    print(f"Successfully retrieved classification in {self.timer} seconds.")
                return classification, confidence
            except NoSuchElementException:
                if self.timer > self.timeout:
                    # self.driver.quit()
                    raise TimeoutError("Request timed out. Please try again or increase the request time limit.")
                if i == 0 and self.verbose:
                    print("Awaiting classification...")
            
            i += 1
            self.timer = time.perf_counter() - self.initial_time
    
    def get_spectral_subclass(self, image_path: str, url: bool=False) -> tuple:
        """
        Makes a request call to the MK-AI website and returns the classification and confidence of the star.
        :param image_path: The path to the image of the star.
        :param url: Whether or not the image_path is a URL.
        :return: A tuple containing the classification and confidence of the star.
        """
        if not isinstance(image_path, str):
            raise TypeError("Parameter \"image_path\" must be a string.")
        if not isinstance(url, bool):
            raise TypeError("Parameter \"url\" must be a boolean.")
        if not os.path.isfile(image_path) and not url:
            raise FileNotFoundError(f"Image does not exist at path {image_path}. Please check your image path again.")
        
        self.initial_time = time.perf_counter()
        self.driver.get("https://starclassification.pages.dev/")
        if url:
            if self.verbose:
                print("Downloading image...")
            picture_req = requests.get(image_path)
            if self.verbose:
                print(f"Image downloaded with status {picture_req.status_code}.")
            if picture_req.status_code == 200:
                image_path = os.path.join(os.getcwd(), "image.jpg")
                with open(image_path, 'wb') as f:
                    f.write(picture_req.content)
        self.driver.find_element(By.ID, "imageUpload").send_keys(image_path)
        if url:
            os.remove(image_path)
            if self.verbose:
                print("Deleted image.")
        i = 0
        
        while True:
            try:
                result = self.driver.find_element(By.ID, "result3").text
                classification = result.split("\n")[0].split(": ")[1].strip()
                confidence = float(str(float(result.split("\n")[1].split(": ")[1].replace("%", "")) / 100)[:6])
                # self.driver.quit()
                if self.verbose:
                    print(f"Successfully retrieved classification in {self.timer} seconds.")
                return classification, confidence
            except NoSuchElementException:
                if self.timer > self.timeout:
                    # self.driver.quit()
                    raise TimeoutError("Request timed out. Please try again or increase the request time limit.")
                if i == 0 and self.verbose:
                    print("Awaiting classification...")
            
            i += 1
            self.timer = time.perf_counter() - self.initial_time
    
    def quit(self) -> None:
        """
        Quits the Chrome webdriver.
        :return: returns nothing
        """
        self.driver.quit()

    def get_apparent_magnitude(self, image_path: str, url: bool=False):
        if not isinstance(image_path, str):
            raise TypeError("Parameter \"image_path\" must be a string.")
        if not isinstance(url, bool):
            raise TypeError("Parameter \"url\" must be a boolean.")
        if not os.path.isfile(image_path) and not url:
            raise FileNotFoundError(f"Image does not exist at path {image_path}. Please check your image path again.")
        
        self.initial_time = time.perf_counter()
        if url:
            if self.verbose:
                print("Downloading image...")
            picture_req = requests.get(image_path)
            if self.verbose:
                print(f"Image downloaded with status {picture_req.status_code}.")
            if picture_req.status_code == 200:
                image_path = os.path.join(os.getcwd(), "image.jpg")
                with open(image_path, 'wb') as f:
                    f.write(picture_req.content)
        


    def get_absolute_magnitude(self, spectral_class, luminosity_class):
        # Example coefficients for illustrative purposes
        spectral_coefficients = {'O': -5, 'B': -3, 'A': -1, 'F': 0, 'G': 2, 'K': 4, 'M': 6}
        luminosity_coefficients = {'I': -4, 'II': 0, 'III': 2, 'IV': 4, 'V': 6}

        try:
            spectral_factor = spectral_coefficients[spectral_class]
            luminosity_factor = luminosity_coefficients[luminosity_class]
        except KeyError:
            return None  # Handle unknown spectral or luminosity class

        absolute_magnitude = spectral_factor + luminosity_factor
        return absolute_magnitude

if __name__ == "__main__":
    test = MKAI(verbose=True)
    spectral_class, _ = test.get_spectral_class("https://jminding.github.io/StarPhotos/Alnitak.jpg", url=True)
    luminosity_class, _ = test.get_luminosity_class("https://jminding.github.io/StarPhotos/Alnitak.jpg", url=True)
    spectral_subclass, _ = test.get_spectral_subclass("https://jminding.github.io/StarPhotos/Alnitak.jpg", url=True)
    print(spectral_class, spectral_subclass, luminosity_class)
    # print(test.get_absolute_magnitude(spectral_class, luminosity_class))
    test.quit()