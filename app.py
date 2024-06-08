import streamlit as st

# Attempt to import the package
try:
    from hyundai_kia_connect_api import VehicleManager
except ImportError as e:
    st.error("Required package is not installed. Please ensure 'hyundai_kia_connect_api' is listed in the requirements.txt file.")
    st.stop()

# Constants
REGIONS = {1: "Europe", 2: "Canada", 3: "USA", 4: "China", 5: "Australia"}
BRANDS = {1: "Kia", 2: "Hyundai", 3: "Genesis"}

# Function to display vehicle information
def print_vehicle_info(vehicle):
    st.write("### Vehicle Information:")
    st.write(f"**Model:** {vehicle.model}")
    st.write(f"**Name:** {vehicle.name}")
    st.write(f"**VIN:** {vehicle.VIN}")
    st.write(f"**Odometer:** {vehicle._odometer_value} {vehicle._odometer_unit}")
    aux_battery_level = vehicle.data.get('Electronics', {}).get('Battery', {}).get('Level', 'N/A')
    st.write(f"**12V Battery Level:** {aux_battery_level}%")
    st.write(f"**Battery Level:** {vehicle.ev_battery_percentage}%")
    st.write(f"**Last Update:** {vehicle.last_updated_at}")
    st.write("")

# Streamlit App
st.title("Hyundai Kia Connect API")

# Input fields for username, password, and PIN
username = st.text_input("Username")
password = st.text_input("Password", type="password")
pin = st.text_input("PIN")

# Dropdown selectors for region and brand
region = st.selectbox("Select Region", list(REGIONS.keys()), format_func=lambda x: REGIONS[x])
brand = st.selectbox("Select Brand", list(BRANDS.keys()), format_func=lambda x: BRANDS[x])

# Authenticate button
if st.button("Authenticate"):
    if username and password:
        try:
            vm = VehicleManager(region=region, brand=brand, username=username, password=password, pin=pin)
            vm.check_and_refresh_token()
            vm.update_all_vehicles_with_cached_state()
            vehicle_info = vm.vehicles
            st.success("Authentication Successful!")
                # Retrieve and print vehicle information
            try:
                vm.update_all_vehicles_with_cached_state()
                for vehicle_id in vm.vehicles:
                    vehicle = vm.get_vehicle(vehicle_id)
                    print_vehicle_info(vehicle)
            except Exception as e:
                print(f"Failed to retrieve vehicle information: {e}")
                for vehicle in vehicle_info:
                    print_vehicle_info(vehicle)
        except Exception as e:
            st.error(f"Failed to authenticate: {e}")
    else:
        st.error("Please enter your username and password")

# Refresh button
if st.button("Refresh Data"):
    try:
        vm.check_and_refresh_token()
        vm.update_all_vehicles_with_cached_state()
        vehicle_info = vm.vehicles
        for vehicle in vehicle_info:
            print_vehicle_info(vehicle)
    except Exception as e:
        st.error(f"Failed to refresh data: {e}")
