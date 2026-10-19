
import streamlit as st
import requests

st.title("Weather API Demo")

# Get API key from Streamlit secrets
API_KEY = st.secrets["API_KEY"]

# Enter city
city = st.text_input("Enter city", "Chennai")

if st.button("Get Weather"):

    if not API_KEY:
        st.error("Please add your OpenWeatherMap API key to secrets.toml.")

    else:
        url = "https://api.openweathermap.org/data/2.5/weather"

        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }

        try:
            with st.spinner("Fetching weather..."):
                response = requests.get(
                    url,
                    params=params,
                    timeout=10
                )

                response.raise_for_status()
                data = response.json()

            # Extract weather details
            temperature = data["main"]["temp"]
            condition = data["weather"][0]["main"]
            humidity = data["main"]["humidity"]

            st.subheader(f"Weather in {data['name']}")
            st.json({
                "city": data["name"],
                "temperature": temperature,
                "condition": condition,
                "humidity": humidity
            })

            # Display metrics
            c1, c2, c3 = st.columns(3)

            c1.metric("Temperature", f"{temperature} °C")
            c2.metric("Condition", condition)
            c3.metric("Humidity", f"{humidity}%")

        except requests.exceptions.Timeout:
            st.error("Request timed out. Try again.")

        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                st.error("Invalid API key or the key is not active yet.")
            elif response.status_code == 404:
                st.error("City not found. Check the city name.")
            else:
                st.error(f"HTTP error: {e}")

        except requests.exceptions.RequestException as e:
            st.error(f"Network error: {e}")

        except (KeyError, IndexError, ValueError):
            st.error("Could not read the weather data.")

st.markdown("---")
st.subheader("HTTP Methods")

st.markdown("""
- **GET** — Retrieve data
- **POST** — Send data
- **PUT** — Update data
- **DELETE** — Delete data
""")
