from weatherGui import *
from datetime import date, datetime
import requests


class Weather(QMainWindow, Ui_weatherApp):
    GEO_API_KEY = 'f29b46cbefe1e994fbf1b88a650c086f'
    WEATHER_API_KEY = 'U79DVJVY6MZCKUSBGP4US2PAN'

    def __init__(self) -> None:
        """
        Initializes variables

        :returns None
        """
        super().__init__()
        self.setupUi(self)
        self.submitButton.clicked.connect(lambda: self.submit())

    def submit(self):
        """
        When the button is clicked all inputs are pulled and checked.
        Then data is pulled from the API and error checked if the location
        exists or not.

        :return None
        """
        try:
            city_input = str(self.cityInput.text().strip())
            state_input = str(self.stateInput.text().strip())
            country_input = str(self.countryInput.text().strip())
            if not city_input or not country_input:
                raise ValueError
            location_data = requests.get(
                f"http://api.openweathermap.org/geo/1.0/direct?q={city_input},{state_input}, {country_input}&limit=1&appid={Weather.GEO_API_KEY}")
            if not location_data.json():
                raise requests.exceptions.HTTPError("Invalid location entered")
            longitude = location_data.json()[0]['lon']
            latitude = location_data.json()[0]['lat']
            weather_data = requests.get(
                f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{latitude},{longitude}/{date.today()}?key={Weather.WEATHER_API_KEY}&limit=1&include=current")
            if 'currentConditions' in weather_data.json():
                data = weather_data.json()
                days_data = data.get('days', [])
                current_conditions = weather_data.json()['currentConditions']
                temp = current_conditions['temp']
                tempMax = days_data[0].get('tempmax')
                tempMin = days_data[0].get('tempmin')
                condition = current_conditions['conditions']
                precipitation = days_data[0].get('precip')
                if precipitation is not None:
                    precipitation *= 100
                else:
                    precipitation = 0.0
                precipType = current_conditions['preciptype']
                if precipType is not None:
                    precipType = ', '.join(map(str, precipType))
                sunrise = current_conditions['sunrise']
                sunset = current_conditions['sunset']
                dateToday = date.today()
                self.imageDisplayerCurrent(current_conditions)
                self.outputLabel.setVisible(True)
                self.imageLabel.setVisible(True)
                print(current_conditions)
            else:
                weather = weather_data.json()
                current_conditions = weather.get('days', [])
                #print(current_conditions)
                temp = current_conditions[0].get('temp')
                tempMax = current_conditions[0].get('tempmax')
                tempMin = current_conditions[0].get('tempmin')
                condition = current_conditions[0].get('conditions')
                precipitation = current_conditions[0].get('precip')
                if precipitation is not None:
                    precipitation *= 100
                else:
                    precipitation = 0.0
                precipType = current_conditions[0].get('preciptype')
                if precipType is not None:
                    precipType = ', '.join(map(str, precipType))
                sunrise = current_conditions[0].get('sunrise')
                sunset = current_conditions[0].get('sunset')
                dateToday = current_conditions[0].get('datetime')
                self.imageDisplayer(current_conditions)
                self.imageLabel.setVisible(True)
                print(current_conditions)

            if self.cRadioButton.isChecked():
                self.outputLabel.setText(
                    str(f"\t\tDate: {dateToday}\n Temperature: {self.celciusConversion(temp):.1f}°\t Condition: {condition}\n High: {self.celciusConversion(tempMax):.1f}°\t\t Precip: {precipitation:.1f}%\n Low: {self.celciusConversion(tempMin):.1f}°\t\t Precip Type: {precipType}\n Sunrise: {self.timeConversion(sunrise)}\t Sunset: {self.timeConversion(sunset)}"))
            elif self.fRadioButton.isChecked():
                self.outputLabel.setText(
                    str(f"\t\tDate: {dateToday}\nTemperature: {temp:.1f}°\t Condition: {condition}\n High: {tempMax:.1f}°\t\t Precip: {precipitation:.1f}%\n Low: {tempMin:.1f}°\t\t Precip Type: {precipType}\n Sunrise: {self.timeConversion(sunrise)}\t Sunset: {self.timeConversion(sunset)}"))
            else:
                error = 'Please choose a temperature scale'
                self.outputLabel.setText(str(error))
                self.outputLabel.setVisible(True)
                self.imageLabel.setVisible(False)

        except requests.exceptions.HTTPError as e:
            self.outputLabel.setText(str(f"{e}"))
            self.outputLabel.setVisible(True)
            self.imageLabel.setVisible(False)
        except ValueError:
            error = "Minimum required: input a city and a country."
            self.outputLabel.setText(f"{error}")
            self.outputLabel.setVisible(True)
            self.imageLabel.setVisible(False)
        finally:
            self.clearInput()
            self.cityInput.setFocus()

    def celciusConversion(self, temp) -> float:
        """
        Converts values from farenheit to celcius

        :return Float
        """
        return (temp - 32) * (5 / 9)

    def timeConversion(self, time) -> str:
        """
        Converts time from 24hr to 12hr format

        :return String
        """
        time_obj = datetime.strptime(time, '%H:%M:%S')
        time12 = time_obj.strftime('%I:%M %p')
        return time12

    def imageDisplayerCurrent(self, data) -> None:
        """
         Displays image based on the icon from the "current" library
         in the API

         :return None
         """
        if data.get('icon') == "clear-day":
            self.displayImage(self.imageLabel, "sunny.png")
            print('sunny')
        elif data.get('icon') == 'cloudy':
            self.displayImage(self.imageLabel, "cloudy.png")
            print('cloudy')
        elif data.get('icon') == 'partly-cloudy-day':
            self.displayImage(self.imageLabel, "partially cloudy.png")
            print('partially cloudy')
        elif data.get('icon') == 'snow':
            self.displayImage(self.imageLabel, "snowy.png")
            print('snow')
        elif data.get('icon') == 'rain':
            self.displayImage(self.imageLabel, "rainy.png")
            print('rain)')
        elif data.get('icon') == 'clear-night':
            self.displayImage(self.imageLabel, "night.png")
            print('night')
        elif data.get('icon') == 'partly-cloudy-night':
            self.displayImage(self.imageLabel, "partly cloudy night.png")
        elif data.get('icon') == 'wind':
            self.displayImage(self.imageLabel, "windy.png")
        elif data.get('icon') == 'fog':
            self.displayImage(self.imageLabel, 'fog.png')

    def imageDisplayer(self, data) -> None:
        """
        Displays an image based on the icon from the "days" library in
        the weather API

        :return None
        """
        if data[0].get('icon') == "clear-day":
            self.displayImage(self.imageLabel, "sunny.png")
            print('sunny')
        elif data[0].get('icon') == 'cloudy':
            self.displayImage(self.imageLabel, "cloudy.png")
            print('cloudy')
        elif data[0].get('icon') == 'partly-cloudy-day':
            self.displayImage(self.imageLabel, "partially cloudy.png")
            print('partially cloudy')
        elif data[0].get('icon') == 'snow':
            self.displayImage(self.imageLabel, "snowy.png")
            print('snow')
        elif data[0].get('icon') == 'rain':
            self.displayImage(self.imageLabel, "rainy.png")
            print('rain)')
        elif data[0].get('icon') == 'clear-night':
            self.displayImage(self.imageLabel, "night.png")
            print('night')
        elif data[0].get('icon') == 'partly-cloudy-night':
            self.displayImage(self.imageLabel, "partly cloudy night.png")
        elif data[0].get('icon') == 'wind':
            self.displayImage(self.imageLabel, "windy.png")
        elif data[0].get('icon') == 'fog':
            self.displayImage(self.imageLabel, 'fog.png')

    def clearInput(self) -> None:
        """
          This function clears all the input boxes when the button is pressed

          :return None
          """
        self.cityInput.clear()
        self.countryInput.clear()
        self.stateInput.clear()
        self.cRadioButton.setChecked(False)
        self.fRadioButton.setChecked(False)